
# 📚 Literature Review Organization for Multi-Agent LLM Test Generation

## 🎯 Paper Target: 6-Page Conference Paper Structure

**Suggested Breakdown:**
- **Introduction + Motivation** (0.5 pages)
- **Related Work** (1.5 pages) ← *This document*
- **Methodology** (2 pages)
- **Evaluation & Results** (1.5 pages)
- **Conclusion** (0.5 pages)

**For Related Work (1.5 pages), prioritize:**
1. **Topic 1.1 + 1.3** (LLM Test Generation + Existing Tools) - **0.5 pages**
2. **Topic 2.2** (Role-Based Prompting) - **0.3 pages** ← CRITICAL
3. **Topic 2.1 + 2.3** (Multi-Agent + Council) - **0.4 pages**
4. **Topic 3.1** (Clustering) - **0.2 pages**
5. **Brief mentions** (Topics 1.2, 3.2, 4.1, 4.2) - **0.1 pages**

---

## 🔥 CRITICAL - Must Include (for 6-page paper)

### **1. LLM-Based Test Generation (Topic 1.1 + 1.3)**
**Why This Matters:** Establishes the foundation and shows you understand the state-of-the-art. This is your "Related Work" baseline.

**What to Write:** "Recent advances in LLM-based test generation have shown promising results [cite 3-4 papers]. Tools like X, Y, Z use single models with prompting strategies A, B, C [cite]. However, they face limitations in test diversity and coverage [cite]. Our approach differs by..."

**Papers to Include:**

Paper Title,Relevance
ChatUniTest: A Framework for LLM-Based Test Generation,"- **Relevance Score:** 92/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Provides an LLM-driven test generation framework with adaptive prompting, thorough evaluation, open-source code, and real-world case studies, but lacks multi-model analysis."
  An empirical evaluation of using large language models for automated unit test generation,"- **Relevance Score:** 85/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses GPT‑3.5 (and others) to generate JavaScript unit tests via detailed prompts; evaluates coverage vs baselines; compares multiple LLMs, showing single‑model focus with cross‑model analysis."
  "An Empirical Evaluation of Using Large Language Models for Automated
  Unit Test Generation","- **Relevance Score:** 85/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses GPT‑3.5 to generate JavaScript unit tests, employs few‑shot and re‑prompting, reports coverage metrics versus baselines, compares three LLMs but no ensemble."
  An initial investigation of ChatGPT unit test generation capability,"- **Relevance Score:** 83/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate Java unit tests and evaluates them with coverage and mutation scores, but provides limited prompting detail and no multi‑model analysis; lacks open‑source code and real‑world case studies."
  CoverUp: Effective High Coverage Test Generation for Python,"- **Relevance Score:** 83/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLM‑driven iterative prompting to generate high‑coverage Python tests; achieves 80‑89% line/branch coverage; benchmarks against CodaMosa and MuTAP; evaluates on open‑source projects."
  Aster: Natural and multi-language unit test generation with llms,"- **Relevance Score:** 82/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLMs to generate multi‑language unit tests, designs prompting techniques, reports coverage and fault‑detection metrics, primarily a single‑model approach, mentions related tools but lacks open source, real‑world case studies, and dedicated limitation discussion."
  Adaptive Test Generation Using a Large Language Model,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses Codex to generate tests with detailed prompts and adaptive re‑prompting; reports coverage and assertion metrics; focuses on a single LLM without multi‑model comparison."
  ChatUniTest: a ChatGPT-based automated unit test generation tool,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate unit tests, designs prompting techniques, reports coverage and fault‑detection results, but focuses on a single model without extensive multi‑model comparison."
  "TestART: Improving LLM-based Unit Test via Co-evolution of Automated
  Generation and Repair Iteration","- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLMs with prompt injection and repair loops; reports coverage and pass rates versus baselines; mentions multiple LLM versions but no ensemble design."
  Unit test generation using generative AI: A comparative performance analysis of autogeneration tools,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate Python unit tests, evaluates prompt engineering for coverage gains, reports quantitative coverage and correctness, and suggests combining with Pynguin, though multi‑LLM methods aren’t explored."
  ChatUniTest: a ChatGPT-based automated unit test generation tool,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate unit tests, designs prompting techniques, reports coverage and fault‑detection results, but focuses on a single model without extensive multi‑model comparison."
  No more manual tests? evaluating and improving chatgpt for unit test generation,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT as the core generator (ChatTESTER); evaluates coverage, readability, and correctness; mentions iterative prompting but lacks detailed prompting methodology; focuses on a single LLM without multi‑model comparison."
  AgentTester: An LLM-Based Tool for Unit Test Generation with Automatically Generated Prompts,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses an LLM as the core engine for unit test generation, designs automatically generated prompts to steer test creation, evaluates coverage and fault detection, but focuses on a single model without extensive multi‑model comparison."
  An initial investigation of ChatGPT unit test generation capability,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses OpenAI LLM to auto‑generate Java unit tests and reports line coverage, mutation score, and execution success. Varies API parameters but lacks detailed prompting methods. Employs a single LLM without multi‑model comparison."
  "TestWeaver: Execution-aware, Feedback-driven Regression Testing Generation with Large Language Models","- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLM with execution‑aware prompts to generate regression tests, provides coverage and fault‑detection metrics, but does not discuss single vs multi‑model setups."
  Evaluating and improving chatgpt for unit test generation,"- **Relevance Score:** 80/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to build ChatTester, a dedicated test generation system; provides extensive quantitative evaluation (coverage, compilation, readability) showing effectiveness. Explores prompting via iterative refinement and tests multiple LLMs, lacking deep multi‑model ensemble analysis."
  "System Test Case Design from Requirements Specifications: Insights and
  Challenges of Using ChatGPT","- **Relevance Score:** 77/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate system test cases from SRS, refines prompts, evaluates redundancy and false positives, discusses limitations; lacks multi‑model comparison and open‑source release."
  ChatUniTest: a ChatGPT-based automated unit test generation tool,"- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT to generate unit tests, designs adaptive prompts, reports coverage metrics versus EvoSuite and other LLM tools, but lacks detailed prompting methods and multi‑model analysis."
  "No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test
  Generation","- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ChatGPT as the central engine for automatic unit test creation, designs prompting techniques to guide test synthesis, and reports coverage and fault‑detection metrics; does not explore multi‑model ensembles."

AI-Driven and Autonomous Testing,"- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Provides a systematic 2020‑2024 review of AI testing evolution, compares ML techniques, identifies research gaps, includes industry case data, but lacks single‑model limitation discussion."
  The Integration of Machine Learning into Automated Test Generation: A Systematic Literature Review,"- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses ML (neural nets, RL) for test generation, maps evolution from classic automation; systematic review of 97 papers (2020‑2022); categorizes techniques but lacks direct head‑to‑head AI comparisons; clearly lists research gaps and future work; does not present industry case studies; does not focus on single‑model vs multi‑model limitations."
  AI-powered software testing tools: A systematic review and empirical assessment of their features and limitations,"- **Relevance Score:** 72/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses systematic review to map AI testing evolution, covers 2020‑2024 literature, highlights research gaps, mentions several AI tools, but lacks deep side‑by‑side performance comparison and detailed industry case studies; does not discuss single‑model vs. multi‑model strategies."
  "The Integration of Machine Learning into Automated Test Generation: A
  Systematic Mapping Study","- **Relevance Score:** 71/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides a thorough 2020‑2022 survey of ML techniques (RL, supervised, clustering) for test generation, highlights gaps, but lacks direct performance comparisons and industry case studies."
  "The Integration of Machine Learning into Automated Test Generation: A
  Systematic Mapping Study","- **Relevance Score:** 71/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses reinforcement learning, supervised and unsupervised ML for test generation; systematic mapping of 2020‑2022 literature; reports technique frequencies but lacks direct performance comparison; highlights research gaps and future work; no industry case studies; does not discuss single‑model vs multi‑model limitations."
  Machine learning algorithms for automated software testing: A comprehensive review of current trends and challenges,"- **Relevance Score:** 67/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides a comprehensive 2020‑2024 survey of ML/DL in testing, outlines future challenges, but lacks detailed comparative results, industry case data, and discussion of single‑model limits."
  An examination of the integration of artificial intelligence techniques in software testing: A comparative analysis,"- **Relevance Score:** 61/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses AI techniques (ML/DL) to trace testing evolution; compares neural‑network and transformer test generators with results; outlines research gaps; lacks industry case data; briefly mentions single‑model limits."
  The role of ai in software test automation - a systematic literature review,"- **Relevance Score:** 57/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses AI methods (ML, neural nets, genetic algorithms) to discuss test automation evolution; systematic review covering 2020‑2024; identifies research gaps and future directions; lacks direct comparative AI approach analysis, real‑world adoption data, and discussion of single‑model vs multi‑model strategies."
  A Systematic Review of AI Based Software Test Case Optimization,"- **Relevance Score:** 56/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Systematic review of AI‑fuzzing methods, identifies research gaps, but lacks detailed comparative results, evolutionary context, and real‑world industry evidence."
  The integration of machine learning into automated test generation: A systematic mapping study,"- **Relevance Score:** 55/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses ML (neural nets, RL) to generate tests, mapping study of 124 papers (2020‑2022). Identifies challenges and future work. Lacks direct AI‑approach comparisons, industry case data, and explicit single‑model vs multi‑model discussion."


**📝 Writing Strategy:** Group similar approaches together. E.g., "Single-model approaches like ChatUniTest [X], TestPilot [Y], and AthenaTest [Z] achieve 60-80% coverage but lack diversity. Tools using Codex [A] show strong performance but..."

---

### **2. Role-Based Prompting (Topic 2.2) - YOUR WEAKEST POINT**
**Why This Matters:** This is your main novelty's justification. You MUST cite research showing role-based prompting improves LLM outputs. Without this, reviewers will say "why roles? prove it."

**What to Write:** "Assigning specialized roles or personas to LLMs has been shown to improve output diversity and quality across multiple domains [cite]. Studies in X domain [cite] and Y domain [cite] demonstrate that role-based prompting leads to Z% improvement. We adapt this approach to test generation by defining four specialized roles..."

**Papers to Include:**

Large language model-based agents for software engineering: A survey,"- **Relevance Score:** 60/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Survey covers LLM agents, multi‑agent collaboration, and role‑play prompting, but lacks direct focus on unit‑test generation, adversarial evaluation, and new empirical measurements."
  LLM Harmony: Multi-Agent Communication for Problem Solving,"- **Relevance Score:** 59/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses distinct personas for LLM agents, enabling role‑play prompting; leverages multiple specialized agents to solve tasks, boosting output quality. Shows empirical gains over baselines. Lacks unit‑test focus, adversarial critique, and human studies; only briefly mentions prompting variants; no released tool."
  "Unleashing the Emergent Cognitive Synergy in Large Language Models: A
  Task-Solving Agent through Multi-Persona Self-Collaboration","- **Relevance Score:** 58/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses multi‑persona prompting to create a cognitive synergist; demonstrates strong empirical gains across diverse tasks; releases code and data; does not target unit‑test generation or adversarial evaluation."
  "Rolellm: Benchmarking, eliciting, and enhancing role-playing abilities of large language models","- **Relevance Score:** 56/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides extensive role‑based prompting framework, benchmarks, and empirical gains, but does not target unit‑test generation or adversarial evaluation."
  MapCoder: Multi-Agent Code Generation for Competitive Problem Solving,"- **Relevance Score:** 53/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses role‑specific agents for recall, planning, coding, debugging; shows strong empirical gains on code benchmarks; releases open‑source framework; does not target unit‑test generation or adversarial testing, and lacks human studies."
  "TestART: Improving LLM-based Unit Test via Co-evolution of Automated
  Generation and Repair Iteration","- **Relevance Score:** 52/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Shows strong empirical gains in unit-test generation via LLM prompts and repair, but lacks explicit role‑based or adversarial prompting strategies."
  The Oscars of AI Theater: A Survey on Role-Playing with Language Models,"- **Relevance Score:** 49/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Survey details role‑play prompting for LLMs, discusses strategies, but lacks unit‑test focus, empirical gains, or released tools."
  Pioneering Autonomous Penetration Testing with Large Language Models through Prompt Engineering and Agentic System Design,"- **Relevance Score:** 48/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses role‑based prompts to orchestrate multiple AI agents for autonomous penetration testing; evaluates agents adversarially and reports performance gains, but does not target unit test generation."
  "Large language model agent: A survey on methodology, applications and challenges","- **Relevance Score:** 47/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Survey extensively covers role‑based and multi‑agent prompting, discusses various role‑play strategies, and mentions adversarial robustness testing, but lacks unit‑test focus, empirical improvement data, human studies, or released tools."
  "LLM Economist: Large Population Models and Mechanism Design in
  Multi-Agent Generative Simulacra","- **Relevance Score:** 47/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses persona‑conditioned prompts for economic agents; applies multiple specialized roles (workers, planner) to solve policy design; shows empirical welfare gains versus baselines, but does not target unit‑test generation or adversarial prompt evaluation."


**📝 Writing Strategy:** "While role-based prompting has been explored in [domain A] for [task X] [cite], and [domain B] for [task Y] [cite], it has not been systematically applied to test generation. Our work adapts these insights by..."

---

### **3. Multi-Agent LLM Systems (Topic 2.1)**
**Why This Matters:** Justifies using multiple DIFFERENT models instead of one model multiple times.

**What to Write:** "Ensemble and multi-agent LLM approaches have shown improvements over single-model systems [cite]. Studies demonstrate that different LLMs have complementary strengths [cite], and heterogeneous ensembles outperform homogeneous ones [cite]. Our council architecture leverages model diversity to..."

**Papers to Include:**

Synergistic minds: A collaborative multi-agent framework for integrated AI tool development using diverse large language models,"- **Relevance Score:** 85/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses multi-agent LLM orchestration with specialized models; outperforms single-model baselines; evaluates code generation/unit tests; notes complementary agents; discusses scalability; no diversity theory."
  XUAT-Copilot: Multi-Agent Collaborative System for Automated User Acceptance Testing with Large Language Model,"- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses three LLM agents for collaborative UAT test script generation, shows significant Pass@1 gains over a single-agent baseline, provides quantitative software‑engineering results, mentions modest improvement reasons but lacks deep analysis of complementary strengths, diversity, or formal scalability discussion."
  MAS-ZERO: Designing Multi-Agent Systems with Zero Supervision,"- **Relevance Score:** 75/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** MAS-ZERO offers a self‑evolving multi‑agent LLM system with strong software‑engineering results and cost‑efficiency, but lacks detailed analysis of complementary strengths or test‑generation gains."
  "Diversity Empowers Intelligence: Integrating Expertise of Software
  Engineering Agents","- **Relevance Score:** 73/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Shows diverse SWE agents improve bug-fixing on SWE‑Bench via hierarchical collaboration and ensemble, but lacks explicit complementary strength analysis, test‑generation results, and scalability discussion."
  Automated Summarization of Software Documents: An LLM-based Multi-Agent Approach,"- **Relevance Score:** 72/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses a Teacher‑Student multi‑agent LLM to summarize software docs, outperforming single‑model baselines; evaluates on SE documentation tasks; mentions complementary agent roles and diversity but lacks detailed analysis of heterogeneity, test‑generation, theory, or deep scalability discussion."
  "Ensemble Learning for Large Language Models in Text and Code Generation:
  A Survey","- **Relevance Score:** 71/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Surveys LLM ensemble methods, detailing multi‑model collaboration, performance gains, and diversity concepts; lacks original software‑engineering experiments or formal theory."
  Trae agent: An llm-based agent for software engineering with test-time scaling,"- **Relevance Score:** 71/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Highly Relevant: Demonstrates ensemble outperforms single LLMs on software‑engineering benchmarks, especially test generation, and details complementary strengths of each model. Somewhat Relevant: Employs multiple LLMs as agents but collaboration is limited; discusses diversity without deep wisdom‑of‑crowds validation; mentions scalability but lacks formal resource analysis."
  Multi-Agent Software Development through Cross-Team Collaboration,"- **Relevance Score:** 56/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Introduces a cross‑team LLM framework that improves software generation quality and discusses scalability, but does not address model‑specific complementarity or test‑generation benchmarks."
  Large Language Models-Based Agents in Software Development,"- **Relevance Score:** 56/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses multi-agent LLMs to support requirements, coding, and testing phases, showing collaborative workflows and software‑engineering experiments. Mentions combining agents and complementary abilities, but lacks concrete ensemble benchmarks, test‑generation results, formal diversity theory, or detailed scalability analysis."
  "Diversity Empowers Intelligence: Integrating Expertise of Software
  Engineering Agents","- **Relevance Score:** 55/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses diverse SWE agents and hierarchical ensembling to improve bug‑fixing on SWE‑Bench, showing some ensemble gains and diversity analysis, but lacks multiple distinct LLMs, test‑generation results, and detailed scalability discussion."


**📝 Writing Strategy:** "Recent work shows ensemble LLM approaches outperform single models [cite, cite]. Specifically, [Paper X] demonstrated that combining models A and B improved accuracy by Z%. We extend this to test generation by..."

---

### **4. Council/Debate Architectures (Topic 2.3)**
**Why This Matters:** Justifies your "independent generation → aggregation" pipeline.

**What to Write:** "Debate and council-based architectures, where agents contribute independently before synthesis, have shown benefits in reasoning tasks [cite]. Constitutional AI [cite] and self-consistency methods [cite] demonstrate that aggregating diverse perspectives improves robustness. We apply this pattern to test generation..."

**Papers to Include:**
An argumentation-based framework for deliberation in multi-agent systems,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses AMAL argumentation framework for committee deliberation, includes argument exchange, confidence‑based voting, and shows higher judgment accuracy versus single‑agent baselines."
  "Improving Factuality and Reasoning in Language Models through Multiagent
  Debate","- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses multiple LLM instances to debate and iteratively refine answers, implements voting/consensus to select final response, and shows empirical gains in reasoning and factuality versus single‑shot baselines."
  NomicLaw: Emergent Trust and Strategic Argumentation in LLMs During Collaborative Law-Making,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses a council of LLMs to draft laws, debates proposals, votes on them, and shows higher quality outcomes versus single‑shot baselines."
  Decision Protocols in Multi-Agent Large Language Model Conversations,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Implements a council of LLM agents with voting, consensus, and judge mechanisms; agents debate and critique proposals; uses explicit aggregation methods; reports higher quality outputs versus single‑shot baselines."
  Minimizing hallucinations and communication costs: Adversarial debate and voting mechanisms in llm-based multi-agents,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses a council of LLM agents with adversarial debate and voting to detect hallucinations; implements structured argumentation and aggregation; reports lower error rates versus single‑shot baselines."
  Corex: Pushing the Boundaries of Complex Reasoning through Multi-Model Collaboration,"- **Relevance Score:** 91/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Corex builds a council of persona‑assigned LLM agents that debate, review, and retrieve, employing voting‑like aggregation and showing gains versus single‑shot baselines."
  "Enhancing Multi-Agent Consensus through Third-Party LLM Integration:
  Analyzing Uncertainty and Mitigating Hallucinations in Large Language Models","- **Relevance Score:** 91/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses third‑party LLMs as council members with a neutral moderator, conducts multi‑round debates, applies uncertainty‑based weighting to aggregate answers, and reports better results than single‑shot baselines."
  "Adversarial Multi-Agent Evaluation of Large Language Models through
  Iterative Debates","- **Relevance Score:** 91/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses council of advocate agents with judge/jury debates; implements iterative argumentative exchange; aggregates via judge decision; shows empirical error reduction versus single-shot."
  "Improving Factuality and Reasoning in Language Models through Multiagent
  Debate","- **Relevance Score:** 87/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses a council of LLMs that debate to converge on answers, showing empirical gains over single‑shot generation; lacks explicit voting mechanisms."
  Simulating Expert Discussions with Multi-agent for Enhanced Scientific Problem Solving,"- **Relevance Score:** 86/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses multiple LLMs as domain experts organized in a council, employs collaborative discussion to resolve disagreements, applies agreement checks as consensus, and reports higher accuracy versus single‑shot baselines."

**📝 Writing Strategy:** "Multi-agent debate systems [cite] and constitutional approaches [cite] show that independent contribution followed by synthesis outperforms sequential processing. We adopt a council pattern where..."

---

## 🔧 SUPPORTING - Brief Mentions (for 6-page paper)

### **5. Semantic Clustering (Topic 3.1)**
**Why This Matters:** Justifies your deduplication approach.

**What to Write (1-2 sentences):** "We employ semantic embeddings for test deduplication, as embedding-based approaches have been shown to capture functional similarity better than syntactic methods [cite]."

**Papers to Include (Pick 1-2):**

Text Similarity Analysis for Test Suite Minimization,"- **Relevance Score:** 48/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Outperforms syntactic baselines; evaluated on open-source test suites. Uses clustering for test minimization with semantic text similarity (no code embeddings)."
  A Comparative Analysis of Clone Detection Techniques on SemanticCloneBench,"- **Relevance Score:** 28/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses CodeBERT for clone detection on SemanticCloneBench; no clustering or deduplication focus; compares semantic vs token baselines; lacks scalability or ablation analysis."
  "Source Code is a Graph, Not a Sequence: A Cross-Lingual Perspective on Code Clone Detection","- **Relevance Score:** 28/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses CodeBERT and CodeGraph embeddings; compares graph vs sequence models on real code clone benchmarks, showing graph superiority, but lacks clustering, deduplication, scalability, and ablation analyses."
  GraphCode2Vec,"- **Relevance Score:** 27/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Shows strong semantic embedding superiority over syntax‑only baselines, uses CodeBERT/GraphCodeBERT for comparison, but lacks clustering, deduplication, scalability, and ablation analyses."
  TCCCD: Triplet-Based Cross-Language Code Clone Detection,"- **Relevance Score:** 27/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses UniXcoder embeddings for cross-language clone detection; no clustering or deduplication focus; compares to baselines, uses a clone dataset, lacks scalability or ablation analysis."
  GraphCode2Vec,"- **Relevance Score:** 27/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Shows strong semantic embedding vs. syntactic baselines, uses CodeBERT/GraphCodeBERT references, but lacks clustering, deduplication, scalability, and ablation analyses."


---

### **6. Test Synthesis (Topic 3.2) - OPTIONAL for 6-page**
**Why This Matters:** Your synthesis step is novel, but might be cut for space.

**What to Write (1 sentence):** "Following clustering, we synthesize tests within clusters using LLM-based aggregation, similar to ensemble knowledge distillation approaches [cite]."

**Papers to Include (Pick 1 if space allows):**

"RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement
Learning","- **Relevance Score:** 70/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses multiple test sets and iterative code drafts to guide generation, preserves correctness via held‑out tests, resolves limited conflicts through feedback loops, and refines code across several LLM attempts."
  MapCoder: Multi-Agent Code Generation for Competitive Problem Solving,"- **Relevance Score:** 70/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses retrieval, planning, coding, and debugging agents to combine multiple LLM outputs; ensures generated code passes original sample I/O, preserving intent; limited explicit conflict‑resolution mechanisms; iteratively refines drafts via LLM agents."
  "Seed-CTS: Unleashing the Power of Tree Search for Superior Performance
  in Competitive Coding Tasks","- **Relevance Score:** 68/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses token-level MCTS to explore many LLM drafts, selects consistent paths, refines code iteratively, and checks correctness via tests, though intent preservation is implicit."
  Improving Code Refinement for Code Review Via Input Reconstruction and Ensemble Learning,"- **Relevance Score:** 67/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses multiple LLM-generated code drafts and ensemble selection, directly matching multi-source synthesis and LLM refinement; retains functionality but lacks explicit intent preservation or conflict resolution mechanisms."
  "Can Pre-trained Language Models be Used to Resolve Textual and Semantic
  Merge Conflicts?","- **Relevance Score:** 66/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses few‑shot prompts with multiple examples to guide LM fixes; ensures semantic correctness of merged code; directly tackles detection and resolution of merge conflicts; does not refine multiple AI‑generated drafts, only single‑prompt generation."
  "Software Testing with Large Language Model: Survey, Landscape, and Vision","- **Relevance Score:** 64/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses search‑based test generation plus LLM suggestions to fuse multiple test sources, aims to keep coverage and assertions, iteratively fixes compilation conflicts, and applies LLM refinement on generated tests, though not explicitly handling multiple draft versions."
  Autocoderover: Autonomous program improvement,"- **Relevance Score:** 62/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Highly relevant: merges LLM‑generated patches with code‑search results and test‑based fault localization, preserving intent via test suites and evaluating on SWE‑bench. Somewhat relevant: offers limited conflict handling, no explicit resolution."
  "ASSERTIFY: Utilizing Large Language Models to Generate Assertions for
  Production Code","- **Relevance Score:** 54/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses retrieved similar tests as multiple inputs and adapts them with LLMs, ensuring compiled, semantically aligned assertions; adapts token discrepancies but lacks explicit multi‑draft LLM refinement."
  RLTF: Reinforcement Learning from Unit Test Feedback,"- **Relevance Score:** 53/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses RL with fine-grained unit test feedback to improve code generation and preserve functional intent; lacks explicit multi‑source synthesis, draft aggregation, and conflict‑resolution mechanisms."
  "A Strategic Coordination Framework of Small LLMs Matches Large LLMs in
  Data Synthesis","- **Relevance Score:** 51/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses coordinated small LLMs to aggregate outputs and resolve conflicts via an Adjudicator, but does not preserve original input intent, lacks SE benchmark tests, and offers no formal analysis."


---

### **7. Evaluation Metrics (Topic 4.1) - OPTIONAL for 6-page**
**Why This Matters:** You'll cite these in your evaluation section, not related work.

**What to Write:** Cite these in your **Evaluation** section when describing your metrics, not in Related Work.

**Papers to Include (Cite in Evaluation section):**

Llms and prompting for unit test generation: A large-scale evaluation,"- **Relevance Score:** 83/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Evaluates LLM-generated unit tests, reports bug detection and mutation scores on Defects4J, directly compares with human tests; lacks human user study."
  Llms for intelligent software testing: a comparative study,"- **Relevance Score:** 76/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLMs to generate and rank tests, reports effectiveness and validity metrics, evaluates on Defects4J, includes limited human test comparison, lacks human assessment."
  Multi-language Unit Test Generation using LLMs,"- **Relevance Score:** 73/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Evaluates LLM-generated tests with mutation score and coverage, includes a developer user study, but uses custom benchmarks rather than standard datasets and lacks direct human‑vs‑AI test comparison."
  Large Language Models are Few-shot Testers: Exploring LLM-based General Bug Reproduction,"- **Relevance Score:** 68/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses LLMs to generate bug‑reproducing tests evaluated on Defects4J (perfect match). Reports bug‑reproduction rate as quantitative quality metric (close match). Lacks human‑written test comparison and human evaluation."
  Exploring Automated Assertion Generation via Large Language Models,"- **Relevance Score:** 68/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Evaluates LLM-generated assertions, reports bug detection rates on Defects4J, but lacks human‑written test comparison and human‑based quality assessment."
  Automated Unit Test Generation and Improvement with Large Language Models (LLMs)/submitted by Florian Stifter,"- **Relevance Score:** 66/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides LLM-generated test evaluation with quality metrics and benchmark datasets, includes some human comparison, but lacks human user study and uses non‑standard benchmarks."
  Effective test generation using pre-trained Large Language Models and mutation testing,"- **Relevance Score:** 62/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Uses LLMs to generate tests and assesses them with mutation testing, reporting mutation scores and bug detection improvements. Does not employ standard benchmarks like HumanEval, and lacks a human study; only loosely compares against human‑written code snippets."


---

### **8. Broader AI Testing Context (Topic 1.2) - OPTIONAL**
**Why This Matters:** Good for introduction/motivation, not critical for 6-page Related Work.

**What to Write (in Introduction, not Related Work):** "AI-assisted testing has evolved from symbolic execution [cite] to neural approaches [cite]."

**Papers to Include (1-2 for Introduction):**

Code-Aware Prompting: A study of Coverage Guided Test Generation in Regression Setting using LLM,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses CodeGen2 and GPT‑4 to generate unit tests via multi‑stage, code‑aware prompts; reports coverage gains and bug detection; compares two LLMs quantitatively; mentions validity, tool release, and scaling only briefly."
  "Code-Aware Prompting: A study of Coverage Guided Test Generation in
  Regression Setting using LLM","- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses CodeGen2 and GPT‑4 to generate unit tests via multi‑stage, code‑aware prompting; reports coverage improvements and directly compares the two LLMs with quantitative results."
  "Impact of Code Context and Prompting Strategies on Automated Unit Test
  Generation with Modern General-Purpose Large Language Models","- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses LLMs with chain‑of‑thought prompting to generate unit tests, reports coverage/mutation scores, compares several models, and releases code publicly."
  Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting using LLM,"- **Relevance Score:** 100/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Provides code‑aware, multi‑stage prompting for unit‑test generation, evaluates coverage on Python methods, and directly compares CodeGen2 with GPT‑4, but lacks validity discussion, open‑source release, and scalability study."
  "Large-scale, Independent and Comprehensive study of the power of LLMs
  for test case generation","- **Relevance Score:** 99/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Uses four LLMs and five prompting techniques to generate 216k unit tests for 690 Java classes, reporting coverage, correctness, and bug detection, and compares results against EvoSuite and across LLMs."
  "TestBench: Evaluating Class-Level Test Case Generation Capability of
  Large Language Models","- **Relevance Score:** 97/100
- **Relevance Tag:** Highly Relevant
- **Reasoning:** Benchmarks class‑level test generation, compares GPT‑4, GPT‑3.5, Codellama with coverage and mutation metrics, includes prompting details and validity discussion."

---

### **9. Ensemble Theory (Topic 4.2) - OPTIONAL for 6-page**
**Why This Matters:** Theoretical backing, but might be cut for space.

**What to Write (1 sentence if space):** "Ensemble learning theory [cite] suggests diversity in model capabilities leads to complementary errors and improved performance."

**Papers to Include (Pick 1 classic if space):**

"Neural Network Ensembles: Theory, Training, and the Importance of Explicit Diversity","- **Relevance Score:** 53/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides explicit diversity‑accuracy trade‑off theory and bounds, proposes a diversity‑encouraging training algorithm, and characterises when ensembles beat single models; bias‑variance analysis is limited, and it does not cover MoE, uncertainty quantification, or multi‑agent links."
  Efficient Estimation of Generalization Error and Bias-Variance Components of Ensembles,"- **Relevance Score:** 52/100
- **Relevance Tag:** Somewhat Relevant
- **Reasoning:** Provides bias‑variance estimators and variance‑based uncertainty, plus efficient algorithms; lacks explicit diversity‑accuracy theory, MoE treatment, and formal superiority conditions or error bounds."
  Balancing Selection and Diversity in Ensemble Learning with Exponential Mixture Model,"- **Relevance Score:** 48/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Uses exponential mixture model to balance weight concentration and diversity, proving equal balance boosts accuracy and outlines conditions for ensemble superiority; related but lacks bias‑variance, MoE details; no uncertainty analysis."
  Research status and prospect of ensemble learning,"- **Relevance Score:** 47/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Survey discusses ensemble concepts, mentions bias‑variance, diversity, MoE, uncertainty, and superiority conditions, but lacks formal proofs or detailed theoretical treatment."
  "Inspect, Understand, Overcome: A Survey of Practical Methods for AI Safety","- **Relevance Score:** 47/100
- **Relevance Tag:** Marginally Relevant
- **Reasoning:** Survey discusses ensemble types, MoE, and uncertainty uses, but lacks formal bias‑variance analysis, proven diversity‑accuracy trade‑offs, rigorous MoE theory, uncertainty bounds, or formal superiority conditions."


---

## 📊 Priority Matrix for 6-Page Paper

| Topic | Priority | Space Allocation | # Papers to Cite |
|-------|----------|------------------|------------------|
| 1.1 + 1.3 (LLM Test Gen + Tools) | 🔴 CRITICAL | 0.5 pages | 4-6 papers |
| 2.2 (Role-Based Prompting) | 🔴 CRITICAL | 0.3 pages | 3-4 papers |
| 2.1 (Multi-Agent) | 🔴 CRITICAL | 0.2 pages | 3 papers |
| 2.3 (Council) | 🟡 HIGH | 0.2 pages | 2-3 papers |
| 3.1 (Clustering) | 🟡 HIGH | 0.2 pages | 1-2 papers |
| 1.2 (AI Testing Landscape) | 🟢 LOW | 0.1 pages (Intro) | 1-2 papers |
| 3.2 (Synthesis) | 🟢 LOW | 1 sentence | 1 paper |
| 4.1 (Metrics) | 🟢 LOW | In Evaluation | 2-3 papers |
| 4.2 (Theory) | 🟢 LOW | 1 sentence | 0-1 paper |

---

## ✍️ Writing Template for Each Citation

When adding papers, use this format to stay concise:

**Long form (for key papers):**
"ChatUniTest [12] uses GPT-3.5 with few-shot prompting to generate JUnit tests,
achieving 72% branch coverage on open-source Java projects. However, it lacks
mechanisms for test diversity..."


**Short form (for supporting papers):**
"Recent tools like TestPilot [8], AthenaTest [9], and TOGLL [10] demonstrate
the effectiveness of LLMs for test generation but rely on single-model approaches."


**Comparison form:**
"While X [5] achieves Y% coverage using approach A, and Z [6] reports W% using
approach B, neither explores multi-model architectures..."


---

## 🎓 Quick Start Guide

1. **Fill in the CRITICAL sections first** (1.1, 1.3, 2.2, 2.1, 2.3)
2. **For each paper, write the "How I'll cite it" line** - this will become your actual text
3. **Group similar papers** - cite 3-4 papers in one sentence when possible
4. **Identify the gap** - every subsection should end with "However, none of these approaches..."
5. **Keep it concise** - each paper gets 1-2 sentences max in a 6-page format

---

## 📝 Next Steps

1. Fill in all the paper details above
2. Write the "How I'll cite it" lines for each paper
3. Copy those lines into a draft Related Work section
4. Add 1-2 sentences at the end of each subsection contrasting with your approach
5. Done! You'll have 1.5 pages of solid related work

Good luck! 🚀