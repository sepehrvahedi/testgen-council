## TL;DR

LLM-based test generators in the supplied corpus are mostly single‑model systems that use iterative prompting, validation/repair loops, or coverage‑guided feedback to improve tests. Coverage and pass‑rate improvements are frequently reported, but few systems employ multi‑model ensembles or councils; some papers report cross‑model comparisons instead.

----

## Single model LLM generators

This section groups tools that primarily run a single LLM (or one LLM per run) to generate and refine tests; most rely on re‑prompting, iterative refinement, or self‑repair loops to fix failing tests. The entries summarize publication year, models actually used (when reported), prompting strategy, evaluation datasets/metrics, headline results, limitations, and distinguishing features.

- **System name** TestPilot  
  - **Publication year** 2023 (original arXiv description) and evaluated in the 2024 IEEE TSE article [1] [2].  
  - **Model(s) used** Codex in the original description and later experiments with gpt‑3.5‑turbo, code‑cushman‑002, and StarCoder were reported [2] [1].  
  - **Single vs multiple models** Single‑model operational design; authors evaluated multiple distinct models separately but did not build an ensemble [1] [2].  
  - **Prompting strategy** Prompts include the function signature and implementation plus usage examples; adaptive re‑prompting is used to repair failing tests [2].  
  - **Evaluation methods** Evaluated on 25 npm packages (1,684 API functions); metrics include statement and branch coverage and similarity to existing tests (normalized edit distance) [1].  
  - **Key results** Median statement coverage ≈70.2% and branch coverage ≈52.8% (with gpt‑3.5‑turbo); similar performance with code‑cushman‑002 and lower with StarCoder [1].  
  - **Limitations** Generation still produces failing/invalid tests that require repair; effectiveness depends on model size/training data but does not require fine‑tuning [1] [2].  
  - **Unique features** Adaptive generate–validate–repair loop with re‑prompting based on failing test and error messages [2].

- **System name** ChatUniTest  
  - **Publication year** 2023 (arXiv) and further work in 2024 [3].  
  - **Model(s) used** ChatGPT as the generator in the reported implementation [3].  
  - **Single vs multiple models** Single‑model framework (ChatGPT) per run; no ensemble reported [3].  
  - **Prompting strategy** An adaptive focal context selects the focal method and dependencies within token limits; follows a generation‑validation‑repair pipeline combining rule‑based fixes and ChatGPT‑based repair [3].  
  - **Evaluation methods** Compared against EvoSuite, AthenaTest, and A3Test on Java projects; metrics include line/branch coverage and focal method coverage [3].  
  - **Key results** Outperforms EvoSuite on branch and line coverage and surpasses AthenaTest/A3Test on focal method coverage in the authors’ experiments [3].  
  - **Limitations** Dependence on prompt context size (token limits), and the evaluation focuses on a single LLM without deep multi‑model exploration [3].  
  - **Unique features** Adaptive focal context construction plus a combined rule‑based and LLM‑based repair toolchain and an extensible ChatUniTest Core and Toolchain [3].

- **System name** ChatTESTER / ChatTester  
  - **Publication year** 2023 (arXiv) with later published results in 2024 [4] [5].  
  - **Model(s) used** ChatGPT as the primary engine; authors also applied the method to open LLMs (CodeLlama‑Instruct, CodeFuse) to show generalization [4] [5].  
  - **Single vs multiple models** Designed as a single‑model approach per run; evaluation showed generalization across multiple LLMs but no council or ensemble architecture [4] [5].  
  - **Prompting strategy** Two‑phase approach: an initial test generator and an iterative test refiner that leverages the same LLM to improve its own outputs (self‑refinement) [4].  
  - **Evaluation methods** Quantitative metrics (compilation/pass rates, assertion correctness), coverage, and a user study on generated test quality [4].  
  - **Key results** Iterative refinement (ChatTESTER) produced 34.3% more compilable tests and 18.7% more tests with correct assertions compared to the default ChatGPT generator [4].  
  - **Limitations** Generated tests still suffer from compilation errors and incorrect assertions; improvements rely on iterative refinement cost and LLM availability [4].  
  - **Unique features** Uses the LLM itself to iteratively refine and repair its outputs (meta‑refinement) and demonstrates applicability across multiple LLMs [4] [5].

- **System name** Chat‑like Asserts Prediction (asserts generator)  
  - **Publication year** 2024 [6].  
  - **Model(s) used** LLM(s) used but the paper focuses on prompt design (persona, chain‑of‑thought, one‑shot); a specific commercial model is not hard‑specified in the abstract [6].  
  - **Single vs multiple models** Single‑model inference design in experiments (no ensemble) [6].  
  - **Prompting strategy** Persona framing, Chain‑of‑Thought, and one‑shot prompts; interactive rounds with an interpreter for execution‑aware assertion generation [6].  
  - **Evaluation methods** A mined Python assert dataset; accuracy measured for single and overall assert generation [6].  
  - **Key results** Achieves 64.7% accuracy for single assert generation and 62% overall, outperforming prior approaches on the dataset [6].  
  - **Limitations** Paper focuses on asserts (not full test-suite generation); model identity and multi‑model comparisons are limited in the reported summary [6].  
  - **Unique features** Execution‑aware loop coupling LLM prompts with interpreter execution and using CoT persona prompts for assert prediction [6].

- **System name** AgentTester  
  - **Publication year** 2025 (conference chapter) [7].  
  - **Model(s) used** Uses an LLM as the core engine; the summary emphasizes auto‑generated prompts rather than naming a specific model [7].  
  - **Single vs multiple models** Single‑model operation per run is described; no ensemble is reported [7].  
  - **Prompting strategy** Automatically generated initial prompts and a preset test generation instruction to query the LLM [7].  
  - **Evaluation methods** Reported to evaluate coverage and fault detection (paper excerpt) but full benchmark details are not in the provided summary [7].  
  - **Key results** Authors report improvement in test generation when using automatically generated prompts (no numeric summary given in the provided excerpt) [7].  
  - **Limitations** The provided summary lacks model‑level detail and full quantitative results in the excerpt [7].  
  - **Unique features** Emphasis on automatic generation of the prompts given to the LLM to reduce manual prompt engineering [7].

----

## Coverage‑guided and execution‑aware systems

This section covers systems that interleave program analysis (coverage, slicing, execution traces) with LLM prompting to drive targeted test generation and avoid coverage plateaus. These systems typically emphasize iterative feedback loops rather than multi‑model ensembles.

- **System name** CoverUp / CoverUp (Coverage‑guided LLM testing)  
  - **Publication year** 2024 [8].  
  - **Model(s) used** Uses an LLM as the generative engine, but the specific model is not specified in the paper abstract/summaries provided; the system pairs coverage analysis with LLM dialogs [8].  
  - **Single vs multiple models** Single LLM per generation run is used in the architecture described; no ensemble/council design reported [8].  
  - **Prompting strategy** Iterative, coverage‑guided dialog: coverage analysis identifies uncovered lines/branches and the system focuses LLM prompts on those regions to guide further test generation [8].  
  - **Evaluation methods** Benchmarked on challenging open‑source Python modules and compared to hybrid systems like CodaMosa and mutation/LLM systems such as MuTAP; metrics include line and branch coverage [8].  
  - **Key results** Reports substantial improvements over prior hybrid and LLM approaches; e.g., per‑module median line coverage ≈81% vs 62% (CodaMosa) and strong line+branch metrics reported by the authors [8].  
  - **Limitations** The precise LLM choice is not emphasized, and authors attribute gains to the combination of analysis + prompting (i.e., not solely the underlying LLM) [8].  
  - **Unique features** Tight coupling of coverage analysis with targeted LLM dialogs that iterate until coverage goals are met [8].

- **System name** TestART  
  - **Publication year** 2024 [9].  
  - **Model(s) used** Employs LLMs in experiments and reports comparisons with ChatGPT‑4.0 and ChatGPT‑3.5 variants in ablations [9].  
  - **Single vs multiple models** Single‑model usage with iterative repair; the contribution is the co‑evolution loop rather than an ensemble [9].  
  - **Prompting strategy** Co‑evolution of generation and repair iterations, template‑based repair, prompt‑injection to avoid repetition suppression, and incorporation of coverage feedback into subsequent prompts [9].  
  - **Evaluation methods** Measurement of pass rate, line coverage on focal methods, and comparisons to EvoSuite and ChatGPT baselines [9].  
  - **Key results** Pass rate of generated test cases ≈78.55% (≈18% higher than ChatGPT‑4.0 and ChatUniTest in the reported comparison) and focal‑method line coverage of 90.96% on passed methods (≈3.4% higher than EvoSuite) [9].  
  - **Limitations** Complexity in avoiding repetitive self‑repair loops and reliance on templates/coverage extraction; evaluation mainly contrasts specific baselines [9].  
  - **Unique features** Template‑based repair coupled with prompt injection and coverage extraction to guide evolution of tests [9].

- **System name** TestWeaver  
  - **Publication year** 2025 (preprint) [10].  
  - **Model(s) used** Integrates an LLM but the provided summary focuses on program‑analysis inputs rather than specifying the LLM family used [10].  
  - **Single vs multiple models** Single LLM usage is implied; the novelty is in how program analysis constructs the prompt context rather than multi‑model designs [10].  
  - **Prompting strategy** Supplies backward slices, close test cases (control‑flow similar tests), and execution inline annotations (variable states) to the LLM to reduce hallucinations and improve execution reasoning [10].  
  - **Evaluation methods** Coverage growth tracking and effectiveness versus prior LLM‑based approaches on regression/regression‑test generation tasks [10].  
  - **Key results** Demonstrates accelerated coverage growth and generation of more effective regression tests than baseline LLM approaches in the authors’ experiments [10].  
  - **Limitations** The approach assumes availability of execution traces and close test cases; exact LLM choices are not the reported focus [10].  
  - **Unique features** Execution‑aware prompts with inline variable annotations and backward slicing to ground LLM reasoning in concrete executions [10].

----

## Commercial tools and empirical comparative studies

This section summarizes empirical studies of commercial or closed‑source LLMs and hybrid baselines, plus feasibility studies that used multiple LLMs for specific tasks. It also notes when requested tools (AthenaTest, A3Test, CodaMosa, etc.) appear only as baselines with limited public detail.

- **System name** GitHub Copilot (empirical study)  
  - **Publication year** 2024 [11].  
  - **Model(s) used** GitHub Copilot (proprietary closed‑source code generation model); the study evaluates Copilot’s in‑editor test suggestions rather than exposing the underlying LLM name [11].  
  - **Single vs multiple models** Treated as a single proprietary model per experiment [11].  
  - **Prompting strategy** Leveraged in‑context signals such as code comments and existing test suites; the study measured the impact of comment strategies on Copilot’s test output [11].  
  - **Evaluation methods** Usability and quality analysis of Python tests generated by Copilot, both with and without existing test suites; qualitative and quantitative measures reported [11].  
  - **Key results** Copilot can accelerate test writing and produce usable tests, but generated tests often require nontrivial modification and can be hard to understand without editing [11].  
  - **Limitations** Generated tests may be difficult to understand or require manual corrections; the closed‑source nature limits reproducibility and fine‑grained model analysis [11].  
  - **Unique features** Study focuses on in‑editor usage patterns and the practical developer experience of test generation with Copilot [11].

- **System name** LLMs from bug‑report inputs (ChatGPT and CodeGPT study)  
  - **Publication year** 2023 [12].  
  - **Model(s) used** ChatGPT (online) and a fine‑tuned CodeGPT model used for the task [12].  
  - **Single vs multiple models** Experiments used each model separately (no ensemble); both were evaluated for feasibility [12].  
  - **Prompting strategy** Treats bug reports as inputs (natural language specifications) and prompts the LLM to produce executable test cases that reproduce the bug scenario [12].  
  - **Evaluation methods** Defects4J bugs as the benchmark; measured whether LLM prompts produced executable tests and usefulness for downstream tasks (fault localization, patch validation) [12].  
  - **Key results** ChatGPT generated executable test cases for up to ≈50% of Defects4J bugs in the authors’ experiments and proved useful for downstream program‑repair workflows [12].  
  - **Limitations** Not all bug reports led to executable tests; performance depends on report quality and model capability [12].  
  - **Unique features** Demonstrates feasibility of deriving executable, bug‑reproducing tests directly from natural bug reports [12].

- **System name** CodaMosa, AthenaTest, A3Test (baseline mentions)  
  - **Publication year** various; in the provided corpus these systems are cited as baselines rather than fully described. The corpus includes comparative mentions but not the original CodaMosa/AthenaTest/A3Test papers for detailed system specifications [3] [8].  
  - **Model(s) used** For CodaMosa the literature describes it as a hybrid search/LLM test generator in the context of CoverUp comparisons; AthenaTest and A3Test are referenced as prior LLM or ML‑based test generators in ChatUniTest and ChatGPT evaluation papers [3] [8].  
  - **Single vs multiple models** Insufficient evidence in the supplied excerpts to characterize internal model architectures or prompting strategies for these baselines; the cited papers use them as comparative baselines [3] [8].  
  - **Prompting strategy** Not specified in the provided summaries for those baseline systems in this corpus [3] [8].  
  - **Evaluation methods** Used as baselines for coverage and focal method coverage comparisons in the cited works [3] [8].  
  - **Key results** CoverUp and other LLM‑guided systems report substantial improvements over CodaMosa in coverage in the supplied comparisons [8].  
  - **Limitations** The supplied corpus excerpts do not provide internal design details for these baselines; therefore finer claims about their models or prompting are not supported by the provided texts [3] [8].  
  - **Unique features** CodaMosa is described as a hybrid search/LLM tool in comparative discussions [8]; AthenaTest/A3Test are used as earlier LLM‑based baselines [3].

- **Cross‑model comparisons and ensemble absence**  
  - Multiple papers run the same pipeline with different LLMs to evaluate sensitivity (for example, TestPilot evaluated gpt‑3.5‑turbo, code‑cushman‑002, StarCoder; ChatTester was applied to CodeLlama‑Instruct and CodeFuse) but do not report multi‑model ensembles or council architectures as part of the tool designs [1] [4] [5].  
  - **Implication** Within this corpus, LLM test‑generation tools largely use a single LLM per execution and only rarely run cross‑model comparisons; explicit ensemble or multi‑agent council architectures are not prominent in the supplied studies [1] [4].

----

For systems or names that were requested but do not appear with implementation details in the supplied papers (for example TOGLL or ToolGen), there is insufficient evidence in the provided corpus to describe publication year, model choices, prompting strategies, or quantitative evaluations — the supplied documents do not include those tools’ technical descriptions.