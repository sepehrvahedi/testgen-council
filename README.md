# TestCouncil

**Three different LLMs write unit tests for the same function. A synthesis step merges their work into one
suite.** On 135 Python functions, the council covered 36 to 46 more percentage points of the code than any
of its members working alone.

[![tests](https://github.com/sepehrvahedi/testgen-council/actions/workflows/tests.yml/badge.svg)](https://github.com/sepehrvahedi/testgen-council/actions/workflows/tests.yml)

This is the code for my BSc thesis at the Software Quality Research Lab, Sharif University of Technology
(supervisor: Prof. Seyed-Hassan Mirian-Hosseinabadi): a FastAPI backend that runs the pipeline, a React
front end that streams it live, and the notebooks and data behind the evaluation.

## The result

135 functions: 45 each from HumanEval, MBPP and TheAlgorithms. Averages over all three:

| Configuration | Line coverage | Time per function |
|:--|--:|--:|
| Qwen 3 235B, alone | 43.0% | 157 s |
| DeepSeek, alone | 38.6% | 9 s |
| Gemini 2.0 Flash, alone | 49.0% | 9 s |
| **Council of the three, generic prompts** | **84.9%** | 175 s |
| **Council of the three, with roles** | **84.6%** (92.5% branch) | 187 s |

Per dataset (line coverage):

| Dataset | Best single model | Council, no roles | Council, with roles |
|:--|--:|--:|--:|
| HumanEval | 75.4% | 92.4% | 94.6% |
| MBPP | 63.0% | 95.9% | 93.3% |
| TheAlgorithms | 22.6% | 66.8% | 65.9% |

Three things I took from it:

1. **Model diversity does the work.** The council beats each single model by 35.6 to 46.0 points of line
   coverage (p < 0.001 in every comparison). Different models miss different things.
2. **Role prompts barely matter.** Giving each model a persona (Coverage Hunter, Assertion Booster, Error
   Finder, Security Checker, Property Tester, Usage Tester) moved line coverage by between -2.6 and +2.2
   points depending on the dataset. The difference is not statistically significant (p > 0.05).
3. **It is not free.** The council takes about three minutes per function, roughly twenty times the fastest
   single model. The synthesis step also has real work to do: about 85% of the raw tests it receives are
   redundant.

The harder the functions, the bigger the gap: on TheAlgorithms, single models average under 20% line
coverage and the council reaches 66%.

## How it works

![Pipeline](./flow-diagrams/summary.png)

1. **Analyse** the function: signature, parameters, exceptions it can raise, branching.
2. **Generate** in parallel: every model is asked for tests, optionally once per role.
3. **Group** similar tests by their AST (structural hashing, or DBSCAN over AST features).
4. **Synthesise** with an LLM: fix and complete each test, then merge everything into one runnable suite,
   keeping tests that add coverage and dropping duplicates.
5. **Measure** by actually running the suite with pytest and coverage.py (line and branch).

The web UI streams every stage over Server-Sent Events, so you can watch each model write.
Step-by-step diagrams are in [`flow-diagrams/`](flow-diagrams).

## Run it

You need Python 3.9+, Node 18+ and an OpenAI-compatible endpoint that serves the three models.

```bash
# backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp app/.env.example .env          # add OPENAI_API_KEY and OPENAI_BASE_URL
uvicorn app.main:app --reload     # API docs at http://127.0.0.1:8000/api/docs
```

```bash
# frontend, in a second terminal
cd frontend
npm install
npm run dev                       # http://localhost:5173
```

Model ids live in [`backend/app/config.py`](backend/app/config.py). The thesis runs used a gateway that
exposes the models as `gemini-2.0-flash`, `deepseek-chat` and `qwen3-235b-a22b`; with another provider,
change each model's `api_name`.

> **This executes model-written code.** Coverage is measured by running the generated tests on your
> machine. Run the backend in a container or a throwaway VM, not next to anything you care about.

### Without an API key

The test suite runs the whole pipeline offline, with the model calls replaced by canned answers:

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

`tests/test_pipeline_offline.py` is the thesis result in miniature: three fake models each cover part of a
function, and only the merged suite reaches 100%.

## API

| Endpoint | |
|:--|:--|
| `GET /api/v1/health` | Liveness and how many models and roles are configured |
| `GET /api/v1/config` | Models, roles and clustering methods |
| `POST /api/v1/generate-tests` | Runs the pipeline and streams it as Server-Sent Events |

```json
{
  "function_code": "def divide(a, b):\n    if b == 0:\n        raise ValueError('b is zero')\n    return a / b",
  "clustering_method": "hash",
  "enable_coverage": true,
  "enable_mutation": false
}
```

Events arrive in order: `pipeline_start`, `llm_start` / `llm_chunk` / `llm_complete` per model,
`clustering_*`, `synthesis_*`, `coverage_*`, `pipeline_complete`.

## Reproducing the evaluation

- Datasets: [`backend/app/data/input/`](backend/app/data/input) (functions drawn from HumanEval, MBPP and TheAlgorithms).
- Batch runner for the five configurations: [`backend/app/scripts/run_batch_experiments.py`](backend/app/scripts/run_batch_experiments.py).
- Raw results and analysis notebooks: [`notebooks/`](notebooks).
- The numbers above were produced at the commit tagged `thesis-results`. Later commits add tests and fix
  parsing of model answers that wrap code in prose; they do not change the method.

Model outputs are not deterministic, so a re-run will land near these numbers, not on them.

## Repository layout

```
backend/     FastAPI service: analysis, council, clustering, synthesis, coverage, experiments, tests
frontend/    React + Vite UI that streams the pipeline
notebooks/   Dataset preparation, experiment results, analysis
flow-diagrams/
```

## Limits

- Python functions only, one function at a time.
- Coverage is the metric. High coverage does not prove the assertions are good; mutation testing is in the
  code but is not part of the reported results.
- Three models from one gateway, on small benchmark functions. Whether the role result holds for larger
  code bases is an open question, and counter-examples are welcome.

## Licence

MIT
