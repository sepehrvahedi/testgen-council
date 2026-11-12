# Backend

FastAPI service that runs the council pipeline. Setup, configuration and the API are described in the
[main README](../README.md).

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest                      # offline: the model calls are replaced with canned answers
cp app/.env.example .env              # then add your endpoint and key
uvicorn app.main:app --reload         # http://127.0.0.1:8000/api/docs
```

| Path | What it does |
|---|---|
| `app/core/code_analyzer.py` | Parses the function under test: signature, parameters, raised exceptions, complexity |
| `app/core/llm_council.py` | Asks every model (and role) for tests in parallel and extracts the test functions |
| `app/core/ast_clusterer.py` | Groups similar tests by AST structure (hashing) or AST features (DBSCAN) |
| `app/core/test_synthesizer.py` | LLM synthesis: improves each group, then merges everything into one suite |
| `app/core/coverage_analyzer.py` | Runs the suite with pytest and coverage.py; line and branch coverage |
| `app/core/services/` | The streaming pipeline (web UI) and the batch pipeline (experiments) |
| `app/scripts/run_batch_experiments.py` | Runs the ablation configurations over a dataset CSV |
| `tests/` | Offline tests, including the whole pipeline end to end |
