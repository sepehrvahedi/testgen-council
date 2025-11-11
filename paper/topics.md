# 🎯 Standalone SciSpace Prompts for Your Bachelor Thesis

Each prompt below is **self-contained** and can be used in a fresh SciSpace chat session. They include full context about your project.

---

## Phase 1: Foundation - Building Your Literature Base

### **Topic 1.1: LLM-Based Test Generation Fundamentals**

I'm writing a bachelor thesis on automated unit test generation using a novel multi-agent LLM architecture. My system uses multiple large language models (Gemini, Claude, DeepSeek, Qwen) working together in a "council" to generate comprehensive test suites. Each model is assigned different roles (QA Engineer, Security Auditor, Agent of Chaos, Abstract Thinker) to promote test diversity. The generated tests are then clustered semantically and synthesized into a final test suite.

For the literature review, I need to understand the current state-of-the-art in LLM-based test generation. Please find papers from 2020-2024 that cover:

1. How large language models (like GPT-4, Codex, Claude, Gemini, or other transformers) are used to generate unit tests automatically
2. Different prompting strategies for test generation (few-shot, zero-shot, chain-of-thought, role-based prompting)
3. Empirical evaluations showing the effectiveness of LLM-generated tests (test coverage, bug detection rates, mutation scores)
4. Common challenges and limitations in using LLMs for test generation
5. Comparison studies between different LLM models for code generation tasks

I specifically need papers that provide quantitative results and discuss the practical applicability of LLM-generated tests. Focus on papers in top software engineering conferences (ICSE, FSE, ASE) or journals (TSE, TOSEM, EMSE). Include both survey papers for overview and specific implementation papers with empirical evaluations.


---

### **Topic 1.2: AI-Assisted Software Testing Landscape**

I'm developing a bachelor thesis on a multi-agent LLM system for automated unit test generation. My approach uses multiple models (Gemini, Claude, DeepSeek, Qwen) with assigned roles working together in a council architecture to generate diverse, high-quality tests.

To position my work within the broader AI testing landscape, I need to conduct a comprehensive literature review. Please search for papers from 2020-2024 about:

1. Survey papers or systematic literature reviews about machine learning and deep learning applications in software testing
2. Papers discussing the evolution from traditional automated testing (symbolic execution, search-based) to AI-assisted testing
3. Comparative studies evaluating different AI approaches (neural networks, transformers, reinforcement learning, genetic algorithms) for test generation
4. Papers that identify current gaps, challenges, and future directions in AI-based software testing
5. Empirical studies on the adoption and effectiveness of AI testing tools in industry vs. academia

I need these papers to establish the motivation for my multi-model approach and show why diversity in test generation matters. Look for papers that discuss limitations of single-model approaches, brittleness of AI-generated tests, or the need for diverse testing perspectives. Include papers from ICSE, FSE, ASE, ISSTA, ICST, and relevant journals.


---

### **Topic 1.3: Existing LLM Test Generation Tools and Systems**

I'm conducting research for my bachelor thesis on a multi-agent LLM test generation system. My approach differs from existing tools by using multiple LLM models (Gemini, Claude, DeepSeek, Qwen) in specialized roles (QA Engineer, Security Auditor, Agent of Chaos, Abstract Thinker) that work together in a council architecture. Tests are generated independently, then clustered semantically and synthesized into a final suite.

I need to conduct a thorough related work analysis comparing my approach to existing systems. Please find papers from 2020-2024 about specific LLM-based test generation tools:

1. ChatGPT/GPT-4 for test generation - any empirical studies or evaluations
2. GitHub Copilot for testing - effectiveness studies, user studies
3. Academic tools: TestPilot, CodaMosa, AthenaTest, ChatUniTest, A3Test, TOGLL, ToolGen, TestSpark, TELPA, LIBRO, TESTMATE
4. Commercial AI testing tools (Tabnine, Cursor, Replit AI, Amazon CodeWhisperer for testing)
5. Any other academic prototypes or industry tools using LLMs for unit test generation

For each system, I need to know: (1) which LLM models they use, (2) their prompting strategy, (3) whether they use single or multiple models, (4) how they evaluate test quality, (5) their reported performance metrics, and (6) their stated limitations. I want to identify what makes my multi-agent council approach novel and potentially better than existing single-model approaches.


---

## Phase 2: Core Methodology - Justifying Your Architecture

### **Topic 2.1: Multi-Agent LLM Systems and Ensemble Approaches**

For my bachelor thesis, I'm building a multi-agent LLM system for automated test generation. My architecture uses four different LLM models (Gemini Flash 2.0, Claude Sonnet 4.5, DeepSeek Chat, Qwen 2.5 Coder) working collaboratively in a council to generate unit tests. Each model generates tests independently, then their outputs are clustered and synthesized into a final test suite.

I need strong scientific justification for this multi-model design choice. My hypothesis is that different LLMs have complementary strengths and using them together produces better, more diverse tests than any single model alone. Please find papers from 2018-2024 about:

1. Multi-agent systems using multiple large language models working collaboratively or in parallel
2. Ensemble methods combining different LLM models for improved performance (not just multiple runs of the same model)
3. Papers showing that different LLMs have complementary strengths (e.g., GPT-4 good at reasoning, Codex/Qwen good at code, Claude good at instruction following)
4. Heterogeneous agent systems where diversity in agent capabilities improves outcomes
5. Empirical evidence that multi-model approaches outperform single-model approaches in software engineering or code generation tasks
6. Papers discussing "wisdom of crowds" effects in AI systems or model ensembles

I need papers with experimental results showing performance improvements from using multiple different models together, not just self-consistency with one model. Focus on papers from ML/AI conferences (NeurIPS, ICML, ICLR, ACL, EMNLP) and software engineering venues (ICSE, FSE, ASE). Include theoretical papers about ensemble diversity and empirical papers with ablation studies comparing single vs. multi-model performance.


---

### **Topic 2.2: Role-Based Prompting and Persona-Driven LLM Systems (CRITICAL)**

THIS IS THE MOST CRITICAL SEARCH FOR MY THESIS. I'm building a multi-agent LLM test generation system where I assign different specialized roles to LLMs: QA Engineer (generates comprehensive functional tests), Security Auditor (generates security-focused tests), Agent of Chaos (generates edge cases and adversarial tests), and Abstract Thinker (generates conceptual/design-level tests).

Currently, these role definitions are my own design, but I need strong scientific justification for using role-based prompting to improve test diversity and quality. Please find papers from 2020-2024 about:

1. Role-based prompting or persona-driven prompts with LLMs for ANY task (not necessarily testing)
2. Studies showing that assigning specialized roles, perspectives, or personas to LLMs improves output diversity, quality, or coverage
3. Papers about adversarial prompting or red-team/blue-team approaches using AI agents
4. Research on multi-perspective problem solving with language models (e.g., "think from the perspective of X")
5. Papers about perspective-taking, viewpoint diversity, or cognitive role-playing in AI systems
6. Role-play prompting strategies for LLMs (e.g., "You are a helpful assistant", "Act as an expert in X")
7. Papers that give LLMs different "hats," identities, or viewpoints to solve problems differently

I need papers from any domain (not just software engineering) that use roles/personas with LLMs and show it improves results. I will adapt their findings to justify my test generation role choices. This is essential for my methodology section—I need to prove my roles aren't arbitrary but are based on established prompting research showing that role-based diversity improves LLM outputs.

Focus on papers from ACL, EMNLP, NeurIPS, ICLR that study prompting strategies, as well as software engineering papers if they use role-based approaches for code generation or testing.


---

### **Topic 2.3: Council, Debate, and Deliberative Multi-Agent Architectures**

I'm developing a bachelor thesis on a "council-based" LLM architecture for test generation. In my system, multiple LLM models (Gemini, Claude, DeepSeek, Qwen) act as independent agents, each assigned a specialized role (QA Engineer, Security Auditor, Agent of Chaos, Abstract Thinker). They generate tests independently (in parallel), then their outputs are aggregated through semantic clustering and LLM-based synthesis to produce a final test suite. This mimics a council meeting where experts contribute independently, then their ideas are integrated.

I need papers justifying this deliberative, council-based architecture. Please find papers from 2018-2024 about:

1. "Council" or "committee" approaches in multi-agent AI systems (where agents contribute independently, then aggregate)
2. Debate-based methods where multiple LLMs discuss, reason, or argue together to reach better solutions
3. Consensus mechanisms in multi-agent LLM systems (voting, weighted aggregation, synthesis)
4. Self-consistency or self-refinement methods in LLMs (including multi-agent self-consistency)
5. Constitutional AI or other approaches where multiple AI perspectives are combined or synthesized
6. Papers showing that disagreement and agreement between LLM agents improves robustness or quality
7. Comparative studies showing that council/debate approaches outperform single-agent or sequential approaches

I need to show that having agents contribute independently (like a council) and then synthesizing their contributions is a valid and effective architectural pattern. Look for papers with empirical results showing that agent deliberation, debate, or independent contribution + aggregation improves final outputs compared to single-shot generation or sequential processing.

Focus on papers from NeurIPS, ICML, ICLR, ACL, EMNLP (for multi-agent LLM research) and ICSE, FSE, ASE (for software engineering applications). Include papers about multi-agent collaboration, ensemble decision-making, and synthesis of diverse AI outputs.


---

## Phase 3: Technical Components - Justifying Implementation Details

### **Topic 3.1: Semantic Clustering and Deduplication of Tests**

I'm building a multi-agent LLM test generation system for my bachelor thesis. After multiple LLM models generate tests independently (in assigned roles), my system clusters similar tests using semantic embeddings to identify duplicates and redundancies. I use sentence-transformers (all-MiniLM-L6-v2) to create embeddings of test descriptions and code, then apply clustering algorithms (DBSCAN, HDBSCAN, or Hierarchical) to group semantically similar tests together.

I need papers supporting this semantic deduplication approach. Please find papers from 2018-2024 about:

1. Papers using semantic similarity or embeddings (BERT, CodeBERT, GraphCodeBERT, UniXcoder) to deduplicate test cases
2. Clustering algorithms applied to source code, test suites, or software artifacts
3. Vector embeddings for measuring code similarity (not just syntactic diff)
4. Test suite minimization or reduction using semantic analysis (beyond coverage-based reduction)
5. Papers about identifying redundant, duplicate, or overlapping tests using NLP or ML techniques
6. Code clone detection using semantic embeddings or learned representations

I need to justify why semantic clustering is better than simple string matching, AST-based comparison, or coverage-based deduplication. Look for papers showing that embedding-based or semantic approaches capture functional/behavioral similarity better than syntactic approaches. I need this to justify my deduplication pipeline.

Focus on papers from software engineering conferences (ICSE, FSE, ASE, ISSTA, ICSME) and NLP/ML conferences if they apply embeddings to code understanding. Include papers about test suite reduction, test prioritization using semantic similarity, and code similarity metrics.


---

### **Topic 3.2: Test Synthesis and Aggregation from Multiple Sources**

I'm developing a multi-agent LLM test generation system for my bachelor thesis. A key novelty of my approach is the synthesis step: after clustering similar tests from multiple models/roles, I use an LLM (Claude Sonnet 4.5) to synthesize tests within each cluster. Instead of just picking the "best" test, I take multiple similar test ideas and create one comprehensive test that captures all insights, assertions, and edge cases from the clustered tests.

I need papers justifying this synthesis/aggregation approach. Please find papers from 2018-2024 about:

1. Test synthesis from multiple sources or examples (e.g., synthesizing a better test from several drafts)
2. Knowledge distillation or aggregation in ensemble learning (combining insights from multiple models)
3. Merging or fusing test cases while preserving coverage, intent, and assertions
4. LLM-based code refinement or improvement from multiple drafts (iterative refinement, self-refinement)
5. Synthesizing insights from multiple AI-generated outputs (code, text, or structured data)
6. Conflict resolution when combining multiple generated artifacts
7. Program synthesis from multiple examples or specifications

This is a novel contribution of my work—instead of voting or selecting, I synthesize. I need papers showing that synthesis/aggregation is effective, even if they're not specifically about testing (e.g., summarization from multiple sources, multi-document synthesis, program repair from multiple patches).

Focus on software engineering papers (ICSE, FSE, ASE) about test improvement, program synthesis, or code fusion, and ML/NLP papers (NeurIPS, ACL, EMNLP) about aggregation, fusion, or synthesis from ensemble outputs.


---

## Phase 4: Supporting Concepts

### **Topic 4.1: Test Quality Metrics and Evaluation of LLM-Generated Tests**

I'm developing a bachelor thesis on a multi-agent LLM test generation system (using Gemini, Claude, DeepSeek, Qwen in specialized roles with clustering and synthesis). I need to rigorously evaluate my generated tests and compare them to baselines (single-model generation, EvoSuite, manually-written tests).

Please find papers from 2018-2024 about evaluating test quality and LLM-generated code:

1. Metrics for evaluating LLM-generated test quality beyond just code coverage (mutation score, bug detection rate, assertion strength, readability)
2. Benchmark datasets for test generation (HumanEval, MBPP, CodeXGLUE, Methods2Test, or test-specific benchmarks like Defects4J)
3. Papers comparing test effectiveness: mutation testing, real bug detection, fault localization capability
4. Human evaluation protocols for AI-generated tests (correctness, maintainability, usefulness)
5. Best practices for evaluating automated test generation systems (what metrics matter, how to design fair comparisons)
6. Papers about test oracle quality, assertion adequacy, or flakiness in AI-generated tests

I need to design a robust evaluation methodology for my thesis showing that multi-model generation is actually better than single-model. I need papers that describe what makes a "good" test beyond coverage, and how to measure improvements in test quality.

Focus on software engineering papers (ICSE, FSE, ASE, ISSTA) about test evaluation, test quality metrics, and LLM code generation evaluation. Include papers that compare human-written vs. AI-generated tests or evaluate tools like ChatGPT, Copilot, or Codex for testing.


---

### **Topic 4.2: Theoretical Foundations of Ensemble and Multi-Model Systems**

I'm writing a bachelor thesis on a multi-agent LLM test generation system that uses multiple different models (Gemini, Claude, DeepSeek, Qwen) in specialized roles. To strengthen my theoretical foundation, I need papers explaining WHY multi-model approaches should work better than single-model approaches from a theoretical perspective.

Please find papers from 2015-2024 about the theoretical foundations of ensemble and multi-model systems:

1. Ensemble learning theory—why combining multiple models works (bias-variance tradeoff, diversity-accuracy tradeoff)
2. Mixture of Experts (MoE) architectures and when to use different specialized models
3. Multi-model aggregation strategies and uncertainty estimation from ensembles
4. The relationship between model diversity and ensemble performance (mathematical/theoretical analysis)
5. Theoretical analysis of why heterogeneous systems outperform homogeneous systems
6. Conditions under which ensembles improve over single models (complementary errors, diversity measures)
7. Theoretical foundations of multi-agent systems and collective intelligence

These papers will help me explain theoretically WHY my multi-agent approach should work better than using a single model multiple times (self-consistency) or just using one model. I need theoretical backing to complement my empirical evaluation.

Focus on machine learning theory papers from JMLR, MLJ, and conferences like NeurIPS, ICML, COLT. Include papers about ensemble methods, mixture of experts, diversity in ensembles, and theoretical analysis of multi-model systems. Also include relevant papers about multi-agent systems theory if they provide mathematical foundations for why agent diversity helps.


---

## 🎯 Usage Tips for Each Standalone Prompt

**When using each prompt in a new SciSpace chat:**

1. **Copy the entire prompt verbatim** into SciSpace
2. **After initial results**, ask targeted follow-ups:
    - "Which of these papers have the highest citation counts?"
    - "Show me empirical studies with experimental results"
    - "Are there any survey or systematic literature review papers here?"
    - "Which papers are from top-tier conferences (ICSE, FSE, NeurIPS, ICLR)?"
    - "Find papers with open-source implementations or replication packages"

3. **Request specific refinements**:
    - "Find more papers from 2023-2024 specifically"
    - "Show papers that compare multiple approaches with quantitative results"
    - "Which papers include ablation studies?"
    - "Find papers that discuss limitations of current approaches"

4. **Export and organize** findings immediately after each search

---

## ⚡ Priority Execution Order

**START HERE (MOST CRITICAL):**
1. **Topic 2.2 (Role-Based Prompting)** ← Your weakest point scientifically

**Then do these in Week 1:**
2. Topic 1.1 (LLM Test Generation Fundamentals)
3. Topic 1.3 (Existing Tools - for Related Work)
4. Topic 2.1 (Multi-Agent Systems)

**Week 2:**
5. Topic 2.3 (Council Architecture)
6. Topic 3.1 (Clustering)
7. Topic 4.1 (Evaluation Metrics)

**Week 3:**
8. Topic 1.2 (Broader AI Testing Context)
9. Topic 3.2 (Synthesis)
10. Topic 4.2 (Theory)

Good luck! 🚀
