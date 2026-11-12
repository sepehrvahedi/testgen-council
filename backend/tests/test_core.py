"""The deterministic parts of the pipeline: code analysis, clustering and coverage measurement."""
import asyncio

import pytest

from app.core.ast_clusterer import ASTClusterer
from app.core.code_analyzer import CodeAnalyzer
from app.core.coverage_analyzer import CoverageAnalyzer
from conftest import CLASSIFY

T_NEG = "def test_negative():\n    assert classify(-3) == 'negative'\n"
T_NEG_AGAIN = "def test_negative_number():\n    assert classify(-8) == 'negative'\n"
T_ZERO = "def test_zero():\n    assert classify(0) == 'zero'\n"
T_EVEN_ODD = "def test_even_and_odd():\n    assert classify(4) == 'even'\n    assert classify(7) == 'odd'\n"
T_RAISES = "def test_type_error():\n    import pytest\n    with pytest.raises(TypeError):\n        classify('x')\n"


def test_code_analyzer_reads_signature_and_complexity():
    analyzer = CodeAnalyzer()
    meta = analyzer.analyze_function(CLASSIFY)
    assert meta["name"] == "classify"
    assert [p["name"] for p in meta["parameters"]] == ["n"]
    assert "TypeError" in meta["raises"]
    context = analyzer.generate_test_context()
    assert "classify" in context and "TypeError" in context


def test_code_analyzer_rejects_code_without_a_function():
    from app.utils.exceptions import CodeAnalysisError
    with pytest.raises(CodeAnalysisError):
        CodeAnalyzer().analyze_function("x = 1\n")


@pytest.mark.parametrize("method", ["hash", "vector"])
def test_clustering_covers_every_test_exactly_once(method):
    tests = [T_NEG, T_NEG_AGAIN, T_ZERO, T_EVEN_ODD, T_RAISES]
    clusters = ASTClusterer(method=method).cluster_tests(tests)
    members = sorted(i for group in clusters.values() for i in group)
    assert members == list(range(len(tests)))


def test_hash_clustering_groups_structurally_identical_tests():
    clusters = ASTClusterer(method="hash").cluster_tests([T_NEG, T_NEG_AGAIN, T_RAISES])
    groups = sorted(sorted(g) for g in clusters.values())
    assert [0, 1] in groups and [2] in groups          # same shape, different literals -> one cluster


def test_clustering_empty_input():
    assert ASTClusterer().cluster_tests([]) == {}


def run_coverage(tests: str) -> dict:
    return asyncio.run(CoverageAnalyzer().analyze_coverage(
        function_code=CLASSIFY, test_code=tests, function_name="classify", enable_mutation=False))


def test_coverage_is_partial_for_a_partial_suite_and_full_for_a_full_one():
    partial = run_coverage(T_NEG + "\n" + T_ZERO)
    full = run_coverage("\n".join([T_NEG, T_ZERO, T_EVEN_ODD, T_RAISES]))
    assert 0 < partial["coverage_percentage"] < 100
    assert full["coverage_percentage"] == 100
    assert partial["missing_lines"] and not full["missing_lines"]


def test_coverage_reports_syntax_errors_instead_of_crashing():
    broken = run_coverage("def test_broken(:\n    assert classify(1) ==\n")
    assert broken["coverage_percentage"] == 0.0
