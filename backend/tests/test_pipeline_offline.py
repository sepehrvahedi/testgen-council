"""The whole council pipeline, end to end, with the model calls replaced by canned answers.

Three "models" each return a few tests, with overlap between them (the redundancy the synthesis step exists to
remove). The fake synthesiser keeps one test per distinct test body. Everything else is the real code: parsing
model output, classification, clustering, final file assembly and coverage measured by running pytest.
"""
import asyncio
import re

import pytest
from fastapi.testclient import TestClient

from app.core.llm_council import LLMCouncil
from app.core.services.test_generation_service import TestGenerationService
from app.core.test_synthesizer import TestSynthesizer
from app.models.requests import TestGenerationRequest
from conftest import CLASSIFY

ANSWERS = {
    "gemini-2.0-flash": """Here are the tests:
```python
def test_classify_negative():
    assert classify(-5) == "negative"

def test_classify_zero():
    assert classify(0) == "zero"
```""",
    "deepseek-chat": """```python
def test_classify_negative():
    assert classify(-5) == "negative"

def test_classify_even():
    assert classify(10) == "even"
```""",
    "qwen3-235b-a22b": """```python
import pytest

def test_classify_odd():
    assert classify(3) == "odd"

def test_classify_rejects_strings():
    with pytest.raises(TypeError):
        classify("3")

def test_classify_zero():
    assert classify(0) == "zero"
```""",
}


@pytest.fixture
def offline(monkeypatch):
    calls = {"models": [], "synthesis": 0}

    async def fake_model(self, model_id, role_id, prompt):
        calls["models"].append((model_id, role_id))
        assert "classify" in prompt
        return ANSWERS[model_id], 100

    async def fake_synthesis(self, prompt, context_info="Synthesis", stream_thinking=False):
        calls["synthesis"] += 1
        seen, kept = set(), []
        for body in re.findall(r"(def test_\w+\(\):\n(?:    .*\n?)+)", prompt):
            if "classify(" in body and body.strip() not in seen:
                seen.add(body.strip())
                kept.append(body.strip())
        return "```python\nimport pytest\n\n" + "\n\n".join(kept) + "\n```"

    monkeypatch.setattr(LLMCouncil, "_call_llm_api", fake_model)
    monkeypatch.setattr(TestSynthesizer, "_call_synthesis_llm", fake_synthesis)
    return calls


def test_council_pipeline_end_to_end_without_network(offline):
    request = TestGenerationRequest(function_code=CLASSIFY, function_name="classify", clustering_method="hash",
                                    enable_coverage=True, enable_mutation=False)
    result = asyncio.run(TestGenerationService().generate_tests_batch(request))

    assert result.success and result.function_name == "classify"
    assert {m for m, _ in offline["models"]} == set(ANSWERS)            # every council member was asked
    assert len(offline["models"]) == 6                                  # three models, two roles each
    assert result.statistics.total_raw_tests == 14                      # (2 + 2 + 3 tests) x 2 roles
    assert result.statistics.final_tests < result.statistics.total_raw_tests   # duplicates were removed
    assert "def test_classify_rejects_strings" in result.final_tests
    assert result.coverage is not None and result.coverage.coverage_percentage == 100


def test_one_model_alone_covers_less_than_the_council(offline):
    def coverage(models):
        request = TestGenerationRequest(function_code=CLASSIFY, function_name="classify", clustering_method="hash",
                                        models=models, enable_coverage=True, enable_mutation=False)
        return asyncio.run(TestGenerationService().generate_tests_batch(request)).coverage.coverage_percentage

    alone = [coverage([m]) for m in ANSWERS]
    assert max(alone) < 100 and coverage(None) == 100                   # the thesis result, in miniature


def test_api_starts_and_describes_itself_without_a_key():
    from app.main import app
    client = TestClient(app)
    assert client.get("/api/v1/health").json()["status"] == "healthy"
    cfg = client.get("/api/v1/config").json()
    assert len(cfg["models"]) == 3 and len(cfg["roles"]) == 6


def test_tests_are_extracted_from_answers_wrapped_in_prose():
    council = LLMCouncil()
    tests = council._extract_tests("Sure! Here you go:\n```python\nimport pytest\n\ndef test_a():\n    assert 1\n```\nHope it helps.")
    assert len(tests) == 1 and "import pytest" in tests[0] and "def test_a" in tests[0] and "Hope" not in tests[0]
    bare = council._extract_tests("def test_b():\n    assert 2\n")
    assert len(bare) == 1 and "def test_b" in bare[0]
