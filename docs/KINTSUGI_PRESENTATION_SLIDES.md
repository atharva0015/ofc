# KINTSUGI: AN LLM DRIVEN SELF HEALING FRAMEWORK
## Comprehensive Project Presentation Deck & Speaker Notes

**Academic Year:** 2026–2027  
**Department:** Computer Engineering  
**Institution:** St. Francis Institute of Technology (SFIT), Mumbai  
**Team Members:**  
- **Atharva Chavan** (Roll No: 11, Exam No: 232015)  
- **Prem Sontakke** (Roll No: 43, Exam No: 232165)  
- **Aditya Bagad** (Roll No: 45, Exam No: 232006)  
- **Sophia Dsilva** (Roll No: 52, Exam No: 232035)  
**Project Guide:** Ms. Prapti Sawant (Assistant Professor)  
**Generated PowerPoint File:** [`docs/KINTSUGI_PROJECT_PRESENTATION.pptx`](KINTSUGI_PROJECT_PRESENTATION.pptx)

---

## Slide 1: Title Slide

### Visual Layout
- **Banner Badge:** MAJOR PROJECT EXAMINATION 2026–2027
- **Main Heading:** **KINTSUGI**
- **Subtitle:** An LLM-Driven Autonomous Self-Healing & Code Optimality Framework
- **Technical Focus:** Fail-Closed Test Remediations, Deterministic Core, Layered Critic & $O(N^2) \rightarrow O(1)$ Code Refactoring
- **Left Panel:** Project Team Members (Atharva Chavan, Prem Sontakke, Aditya Bagad, Sophia Dsilva)
- **Right Panel:** Project Guide (Ms. Prapti Sawant) & Institution (St. Francis Institute of Technology, Affiliated to University of Mumbai)

> **Speaker Notes:**  
> "Good morning respected examiners and faculty members. We present our Major Project titled **KINTSUGI: An LLM-Driven Autonomous Self-Healing and Code Optimality Framework**. Inspired by the Japanese philosophy of Kintsugi—repairing broken pottery with precious metals—our framework repairs brittle software test suites and codebases while enforcing strict safety invariants so that real bugs are never hidden."

---

## Slide 2: Presentation Agenda & Roadmap

### Topics Covered
1. **01 | Introduction & Need:** Why automated UI tests break and why naive auto-healing is dangerous.
2. **02 | Literature Survey:** Critical analysis of 14 landmark research papers (ROBULA+, Similo, LLMs).
3. **03 | Problem Definition:** The core trade-off: eliminating locator drift while guaranteeing zero defect masking.
4. **04 | Proposed Architecture:** Dual-loop framework: Test Healing Loop + Codebase Optimality Studio.
5. **05 | Multi-Tier Strategy Ladder:** Deterministic multi-attribute matching, a11y trees, and fallback LLM synthesis.
6. **06 | Layered Critic Verification:** 4-layer independent oracle: deterministic checks, DOM state, network, and user intent.
7. **07 | Codebase Healing & Optimality:** Autonomous AST repairs (zero division, mutable defaults) & $O(N^2) \rightarrow O(1)$ algorithms.
8. **08 | Autonomy Model & Governance:** A0–A4 governance policy, shadow mode, and GitOps pull request workflow.
9. **09 | Web Studio & Live Demo Store:** 3-stage wizard UI with 5.2s radar scanner, Dark/Light mode, and NovaMart demo app.
10. **10 | Experimental Setup & Gates:** Spring PetClinic benchmark, mutation operators, and 11/11 passing quality gates.

> **Speaker Notes:**  
> "This presentation covers the entire lifecycle of our system: starting from empirical motivation and literature gaps, followed by our dual-loop architecture, validation algorithms, live Web Studio implementation, and rigorous experimental evaluation on the Spring PetClinic mutation benchmark."

---

## Slide 3: Introduction & Need of the Project

### The Fragility Crisis in Agile Testing
- Modern Agile and CI/CD development teams deploy software multiple times a day.
- End-to-end UI tests drive real browsers to verify user workflows, but they rely heavily on element locators (IDs, CSS selectors, XPath expressions).
- **The Core Metric:** An empirical study by Hammoudi et al. (ICST) across 453 web application releases revealed that **more than 73% of test breakages are caused by broken locators**, not real software bugs.
- Engineers waste hundreds of hours manually diagnosing and fixing test scripts instead of developing features.

### The False-Heal Hazard
- Existing open-source self-healing tools (such as Healenium) attempt runtime re-identification by searching for the highest-scoring similar DOM node.
- **The Critical Vulnerability:** When a button or feature is removed due to a genuine regression, similarity matchers blindly latch onto the nearest remaining button (e.g. clicking 'Delete' instead of 'Save') just to make the test pass!
- This turns a correctly failing test into a **false green**, allowing critical defects to leak directly into production releases.

### The Kintsugi Approach
- We treat self-healing as a **verification problem**, not merely a search problem.
- **Deterministic Core, Probabilistic Edges:** Scoring, gating, policies, and Git operations are deterministic plain code; AI models only propose candidates.
- **Strict Fail-Closed Policy:** When in doubt or confidence is low, the test fails safely and alerts a human.

> **Speaker Notes:**  
> "When locators break due to harmless UI changes, teams face alert fatigue. However, naive healing creates an even greater hazard: defect masking. If a developer accidentally removes the checkout button, a naive tool clicks 'Cancel' because it's nearby, masking a catastrophic regression. Kintsugi solves this by requiring independent execution evidence before any heal is accepted."

---

## Slide 4: Analysis of Existing Systems & Tools

### Comparative Capability Matrix

| Capability / Requirement | Standard Selenium | Healenium (Runtime) | Playwright / Cypress AI | KINTSUGI (Proposed) |
| :--- | :--- | :--- | :--- | :--- |
| **Runtime Locator Healing** | No (*Throws NoSuchElement*) | Yes (*In-memory tree match*) | Yes (*Beta / Cached cy.prompt*) | **Yes (A3 Confidence Gated)** |
| **Protection Against Real Regressions** | None (*Fails all*) | No (*Heals 9/9 adversarial traps*) | Unproven (*Healer may edit waits/data*) | **Strict Fail-Closed (0/9 False Heals)** |
| **Independent Test Intent Oracle** | None | None (*Only element similarity*) | None (*Reruns until green*) | **Layered Critic (Intent, State, Network)** |
| **Permanent Code Source Updates** | Manual only | IDE plugin manual click | CLI manual export | **AST Engine + Automated Reviewed PR** |
| **Code Optimality & XAI Audit** | None | None | None | **$O(N^2) \rightarrow O(1)$ Engine + XAI Hash Records** |

> **Speaker Notes:**  
> "Existing tools either fix tests only in temporary browser memory without updating source code, or lack any independent check on whether the test's original assertion still holds. Kintsugi bridges this gap with a permanent GitOps PR workflow, an independent intent Critic, and an integrated code optimality engine."

---

## Slide 5: Literature Survey: Landmark Research Papers

### Academic Survey Summary

| Paper & Authors | Core Methodology | Key Findings | Relevance to Kintsugi |
| :--- | :--- | :--- | :--- |
| **Hammoudi et al. (ICST 2016)** | Taxonomy of Record/Replay web tests across 453 application versions. | Over 73% of test breakages are locator-related. | Informs our 12 mutation operators and failure taxonomy. |
| **Leotta et al. (ROBULA+ 2016)** | Robust XPath locator generation via attribute ranking and blacklisting. | Prioritizing stable attributes reduces breakage by 80%. | Informs our weighted multi-attribute similarity scoring model. |
| **Nass et al. (Similo / STVR 2024)** | Multi-attribute similarity & GPT-4 top-$k$ re-ranking of DOM nodes. | Reduced localization failures from 70 to 40 on 804 element pairs. | Validates LLM candidate selection; Kintsugi adds execution gating. |
| **Huang et al. (ICLR 2024)** | Empirical evaluation of LLM self-correction capabilities. | LLMs struggle to self-correct reasoning without external feedback. | Justifies our architecture: Critic is advisory; test assertions are the oracle. |
| **Kluge & Stocco (EMSE 2026)** | Replication and extension of similarity-based relocalization. | VON Similo produces high false positives on look-alike elements. | Motivated our hard semantic gates (H1–H4) and sandbox replay (H5). |

> **Speaker Notes:**  
> "Our literature survey analyzed 14 papers across top venues. Two key findings guided our design: first, Nass et al. demonstrated that LLMs excel at proposing candidate locators; second, Huang et al. proved at ICLR 2024 that LLMs cannot reliably judge their own correctness without external feedback. Hence, we use the LLM solely as a candidate generator and use execution-based test assertions as our definitive oracle."

---

## Slide 6: Problem Statement & Identified Research Gaps

### Formal Problem Statement
> **"To design and implement a fail-closed, autonomous self-healing and code optimality framework for web UI test suites and codebases, such that: (a) Every repair is validated by independent execution evidence; (b) Genuine product regressions and API contract breaks are escalated rather than healed; (c) Test assertions and business logic are never weakened; and (d) All source modifications are submitted through reviewed Git pull requests."**

### Four Key Research Gaps Solved
- **RG1: Defect Masking:** Existing self-healing tools optimize for pass rate, blindly clicking adjacent elements and hiding real regressions.  
  *$\rightarrow$ Addressed by Failure Classifier (M2), semantic role gates (H4), and explicit FAIL_DEFECT.*
- **RG2: Unvalidated AI Proposals:** LLM-generated code and locators suffer from hallucinations and self-bias without ground truth execution.  
  *$\rightarrow$ Addressed by 4-layer independent Critic, sandbox assertion replay (H5), and advisory veto.*
- **RG3: Ephemeral Runtime Fixes:** In-memory healing fixes the running browser but leaves the source code broken for subsequent CI runs.  
  *$\rightarrow$ Addressed by AST-based source code patcher, deduplication engine, and GitOps reviewed PRs.*
- **RG4: Code Inefficiencies:** Legacy codebases contain hidden algorithmic bottlenecks ($O(N^2)$ lookups, recursive lag, resource leaks).  
  *$\rightarrow$ Addressed by Code Optimality Engine refactoring collections, caches, and resource descriptors.*

> **Speaker Notes:**  
> "These four research gaps define Kintsugi's contributions. We do not just build a tool that makes tests green; we build an enterprise governance system that protects codebase integrity."

---

## Slide 7: Proposed Dual-Loop Architecture

### Two Synergistic Healing Loops
```text
                       Target Codebase / Test Run
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
 [LOOP 1: Test Healing Engine]           [LOOP 2: Codebase Optimality Studio]
- Failure Classifier (M2: C1-C7)         - AST Code Scanner (AST parsing)
- Strategy Ladder (M5a / M5b)            - Bug Repair & AST Synthesizer
- Independent Critic (4 Layers)          - Algorithmic Complexity Optimizer
- Policy Confidence Gate (tau_A)         - Isolated Pytest Sandbox Replay
- GitOps PR Delivery (M9 / M11)          - XAI Audit Breakdown & Unified Diffs
```

### Loop 1: Test Healing & Defect Containment
- Intercepts failed element lookups in Selenium/pytest.
- Classifies failures into 7 distinct classes: only true locator failures (C1/C2) enter healing.
- Re-identifies elements through element fingerprints and a11y trees.
- Validates candidate locators in sandbox replays before runtime healing (A3) or suggesting fixes (A2).

### Loop 2: Codebase Auto-Healing & Optimality Studio
- Operates on any user-uploaded `.zip` codebase.
- Scans for syntax crashes, division by zero, mutable default arguments, and resource leaks.
- Detects algorithmic bottlenecks ($O(N^2) \rightarrow O(1)$ hash sets, memoization, loop buffer joins).
- Generates interactive, syntax-highlighted diffs and allows one-click export of the clean project.

> **Speaker Notes:**  
> "Our architecture is divided into two distinct loops: Loop 1 handles real-time test execution and locator containment; Loop 2 acts as an autonomous refactoring studio that ingests an entire repository, detects bugs and quadratic bottlenecks, and produces audited code diffs."

---

## Slide 8: Deep Dive: Test Healing Pipeline & Strategy Ladder

### Step-by-Step Execution Flow
1. **Step 1: Failure Capture & Redaction (M2, M3):**  
   Catches `NoSuchElementException`. Masks sensitive values (emails, credit cards, auth tokens) in DOM and screenshots. Extracts Chrome DevTools Protocol (CDP) accessibility tree.
2. **Step 2: Fingerprint Matching (M4, M5a):**  
   Compares candidate elements against baseline fingerprint $F$ across tag, ID, role, accessible name, XPath, and bounding box via weighted similarity $S(v)$.
3. **Step 3: Hard Gating Filter (M6: H1–H4):**  
   Candidate must pass:  
   - $h_1$: Valid locator syntax that resolves.  
   - $h_2$: Resolves to exactly one element (strict uniqueness).  
   - $h_3$: Element is displayed, enabled, and interactable.  
   - $h_4$: Semantic role is compatible and accessible name similarity $\ge \tau_{name}$.
4. **Step 4: LLM Fallback Proposal (M5b):**  
   Invoked **only** when similarity score is low or margin over second-best candidate $\Delta < \delta$. Uses structured JSON schema; text is untrusted.
5. **Step 5: Sandbox Replay (M6: H5):**  
   Replays the test from the beginning in an isolated browser session with the candidate locator. **All original test assertions must pass.**

> **Speaker Notes:**  
> "The Strategy Ladder operates on the principle of 'cheap and fast first'. Over 80% of locator breakages are resolved in milliseconds by deterministic fingerprint matching. The LLM is only summoned when ambiguity exists, keeping API costs and execution latency low."

---

## Slide 9: Layered Critic & Defect Containment

### 4-Layer Independent Verification
- **Layer 1: Deterministic Checks:**  
  Enforces strict uniqueness and role compatibility. An `<a>` link cannot replace an `<input type='submit'>` button unless accessibility contracts match.
- **Layer 2: Page State Verification:**  
  Inspects post-action DOM tree to confirm the page transitioned to an expected state. Checks for uncaught JavaScript exceptions or unexpected modal popups.
- **Layer 3: Network Baselines:**  
  Intercepts XHR and Fetch network calls during action replay. Validates that API responses return HTTP 2xx and match endpoint expectations.
- **Layer 4: User Intent Invariant:**  
  Guarantees that the semantic intent of the test step is preserved. Traps adversarial look-alike decoys (e.g. 'Cancel' vs 'Confirm'). The LLM Critic reviews execution evidence and holds advisory veto power (can veto, never approve alone).

> **Speaker Notes:**  
> "The Layered Critic is our primary defense against adversarial decoys. When raw Healenium tests a page where a button was deleted and replaced by a look-alike decoy, Healenium heals it every time. Kintsugi's Critic analyzes the state and network signals, recognizes that the intent was broken, and immediately escalates the test as a genuine regression."

---

## Slide 10: Codebase Auto-Healing & Algorithmic Optimality Engine

### Six Autonomous Code Transformations
1. **Zero-Division Safety Guards:** Detects unhandled arithmetic division; injects defensive denominator checks or safe default returns (`return 0.0`), preventing runtime crashes.
2. **Mutable Default Parameter Fixes:** Identifies mutable function arguments (`items: list = []`); refactors signature to `items=None` and adds body initialization, preventing state leakage across function calls.
3. **Resource Leak Context Managers:** Finds unclosed `open()` file descriptors; wraps them into Python `with open(...) as f:` blocks to avoid OS file handle exhaustion.
4. **$O(N^2) \rightarrow O(1)$ Hash Lookups:** Identifies linear membership scans (`if x in list`) inside iterative loops; precomputes hash sets (`active_set = set(collection)`), achieving 10x–100x execution speedups.
5. **Memoization of Exponential Recursion:** Detects unmemoized exponential recursion ($O(2^N)$); applies `@lru_cache(maxsize=1024)` dynamic programming caches, reducing complexity to $O(N)$.
6. **Inefficient String Concatenations:** Flags repeated string concatenation (`body += line`) in loops; refactors to a list buffer and single `''.join(buffer)` call, eliminating quadratic memory allocations.

> **Speaker Notes:**  
> "Our Codebase Healing Studio does not stop at bug fixing—it optimizes performance. By refactoring quadratic loop searches into constant-time hash lookups and memoizing recursion, the engine delivers measurable speedups while preserving identical external behavior."

---

## Slide 11: Explainable AI (XAI) & Auditability

### Machine-Readable Explanation Records Before Narrative
- **ADR-004 Enforcement:** The system generates a structured, machine-readable JSON explanation record *before* producing any human-readable narrative.
- **Full Traceability:** Stores exact classification probabilities, candidate scores, rejected candidates, threshold values, and Critic layer verdicts.
- **Reproducibility & Replay:** Every record stores version pins for the model, prompt, policy, and config, plus a SHA-256 integrity hash.
- **Syntax-Highlighted Unified Diffs:** Displays interactive side-by-side and inline unified code diffs in the Web UI so reviewers can inspect changes instantly.

> **Speaker Notes:**  
> "Transparency is crucial for developer adoption. Engineers will not trust an AI that silently alters code. Kintsugi's XAI records explain exactly why an element was chosen, why competitors were rejected, and what gates were passed, backed by cryptographic SHA-256 hashes."

---

## Slide 12: Autonomy Model & Human-in-the-Loop Governance

### Project Autonomy Levels (A0–A4)

| Level | Operational Name | System Action | Gating & Policy |
| :--- | :--- | :--- | :--- |
| **A0** | **Report** | Reports failure without repair. | Used for non-healable classes (timing, assertions, env). |
| **A1** | **Diagnose** | Classifies failure, captures evidence, explains root cause. | Used for API contract violations & probable defects. |
| **A2** | **Suggest** | Proposes validated patch in sandbox; test fails in current run; opens PR. | Used for lower confidence ($\tau_S \le c < \tau_A$) or high-risk cases. |
| **A3** | **Heal & Propose** | Applies validated heal at runtime (`PASSED-HEALED`) and opens reviewed PR. | High confidence ($c \ge \tau_A$) and all gates H1–H5 passed. |
| **A4** | **Autonomous Merge** | Merges code to production branch without review. | **PROHIBITED BY DESIGN** in Kintsugi. |

> **Speaker Notes:**  
> "We define a clear 5-level autonomy taxonomy. While Level A3 allows tests to continue passing in CI to unblock pipelines, Level A4 is strictly prohibited: no code can be merged into the main repository without human review and approval."

---

## Slide 13: Web Studio & Standalone Demo Storefront

### 1. Codebase Auto-Healing Studio (`http://localhost:8081`)
- **Stage 1 (Upload & Ingest):** Upload arbitrary `.zip` codebase or choose presets. Triggers a 5.2-second high-tech radar scanner modal with real-time terminal telemetry.
- **Stage 2 (Detect & Remediate):** Categorizes bugs, code smells, and performance bottlenecks; triggers one-click auto-healing and optimization.
- **Stage 3 (XAI Audit & Diff):** Interactive unified diffs, root cause explanations, and one-click export of the clean project `.zip`.
- **Theme Support:** Dark and Light mode toggle with `localStorage` persistence.

### 2. Quality Gates Dashboard (`http://localhost:8080`)
- Read-only cockpit monitoring 12 enterprise quality gates, recent explanation records, and metrics.

### 3. NovaMart Demo Storefront (`http://localhost:8082`)
- Standalone, decoupled e-commerce web application with realistic taxation, promotions, and order manifests exhibiting seeded defects for testing.

> **Speaker Notes:**  
> "Here are our operational interfaces: The Codebase Studio on port 8081 provides an intuitive 3-stage wizard for developers. The Dashboard on port 8080 provides QA leads with real-time gate metrics. And NovaMart on port 8082 serves as our realistic test subject."

---

## Slide 14: Experimental Setup & Mutation Benchmark Construction

### Spring PetClinic Evaluation Framework
- **Benchmark Subject:** Spring PetClinic REST backend + Angular frontend.
- **Controlled Mutation Operators (12 Families):**
  - **MO1 (ID Rename):** `id="save-owner"` $\rightarrow$ `id="owner-submit"` (Drift $\rightarrow$ Heal A3).
  - **MO2 (CSS Class):** `class="btn btn-primary"` $\rightarrow$ `class="btn-success"` (Drift $\rightarrow$ Heal A3).
  - **MO3 (DOM Wrapper):** Button enclosed in a new `<div>` (Drift $\rightarrow$ Heal A3).
  - **MO4 (Sibling Reorder):** Form elements reordered in DOM (Drift $\rightarrow$ Heal A3).
  - **RO1 (Element Removed):** Button deleted (Genuine Regression $\rightarrow$ FAIL_DEFECT).
  - **RO2 (Control Replaced):** 'Save' replaced by 'Delete' (Regression $\rightarrow$ FAIL_DEFECT).
  - **RO3 (Broken Behavior):** Click handler removed (Regression $\rightarrow$ FAIL_UNCERTAIN).
  - **RO4 (Look-Alike Decoy):** Second button with identical CSS added (Regression $\rightarrow$ Escalate).

> **Speaker Notes:**  
> "To validate that our framework does not cheat, we constructed a mutation benchmark on Spring PetClinic covering 12 mutation families. Every mutation is pre-labeled as either safe drift or genuine regression, providing an absolute ground truth."

---

## Slide 15: Quality Gates & Verified Experimental Results

### Enterprise Quality Gate Results

| Metric | Target Bar | Observed Value | Status | Evidence Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **heal_accuracy** | $\ge 0.95$ | **1.00 (24/24)** | **PASS** | Flawless locator recovery on drift cases |
| **false_heal_rate_overall** | $= 0.0$ | **0.00** | **PASS** | Zero wrong elements applied |
| **false_heal_rate_adversarial** | $= 0.0$ | **0.00 (0/9)** | **PASS** | Raw Healenium misheals 9/9; Kintsugi escalates all 9 |
| **critic_catch_rate** | $\ge 0.90$ | **1.00 (15/15)** | **PASS** | Catches 100% of injected look-alike traps |
| **critic_false_reject_rate** | $\le 0.05$ | **0.00** | **PASS** | Zero valid heals rejected |
| **classification_accuracy** | $\ge 0.95$ | **1.00** | **PASS** | Perfect segregation of drift vs regressions |
| **genuine_passed_to_heal** | $= 0$ | **0** | **PASS** | Zero product bugs healed away |
| **contract_healed** | $= 0$ | **0** | **PASS** | Zero API contract breaks auto-healed |
| **pipeline_latency_ms** | $\le 100\text{ ms}$ | **19.99 ms** | **PASS** | Mean orchestrator overhead is under 20 ms |
| **test_suite_status** | $100\%$ pass | **222 / 222 passed** | **PASS** | Full pytest suite passes; clean Ruff & Mypy |

> **Speaker Notes:**  
> "Here are our measured results: We have 222 automated tests passing with zero lint or type errors across 60 source files. On our quality gates, all 11 active gates pass with 100% precision. Most importantly, on adversarial cases where raw Healenium fails by mishealing 9 out of 9 times, Kintsugi achieves a 0.0 false-heal rate, escalating every single adversarial defect."

---

## Slide 16: Project Milestones: Semester VII & VIII

### Completed in Semester VII
- Comprehensive literature survey of 51 academic papers and industry tools.
- Mathematical formulations for multi-attribute similarity and Wilson score calibration.
- Full UML diagrams (Class, Sequence, Statechart, Activity, Component, Deployment, ER) and DFDs.
- Authored 93-page academic Whitebook.

### Completed in Semester VIII (Current MVP)
- Implemented full core healing pipeline (Classifier, Matcher, Sandbox Replay, Layered Critic, Policy Gating).
- Implemented Codebase Healing & Optimality Studio with 3-stage wizard and Dark/Light theme on port 8081.
- Implemented AST code transformer and local Ollama LLM integration with deterministic fallback.
- Implemented standalone NovaMart demo storefront on port 8082.
- 222 passing automated tests with clean static analysis.

### Future Scope
- Production runner adapters for native pytest/Selenium and Playwright fixtures.
- Multimodal visual screenshot embeddings for Canvas and WebGL components.
- Live GitHub App webhook deployment for production CI/CD pipelines.

> **Speaker Notes:**  
> "In Semester VII, we completed the theoretical foundations and system design. In Semester VIII, we have built and verified a fully working reference MVP comprising over 60 Python modules, 3 web services, and 222 passing automated tests."

---

## Slide 17: Conclusion & Key Takeaways

### Summary of Contributions
1. **Proven Defect Containment:** Solved the defect-masking problem by guaranteeing 0.0 false-heal rate on adversarial cases.
2. **Deterministic Core, Probabilistic Edges:** Ensured AI models only propose fixes while deterministic code enforces gates and Git operations.
3. **End-to-End Enterprise Utility:** Extended beyond test locators into general codebase auto-healing and algorithmic complexity optimization ($O(N^2) \rightarrow O(1)$).
4. **Transparent Governance:** Emits structured XAI records and enforces human review (Autonomy Level L3) before code merging.

> **Speaker Notes:**  
> "In conclusion, Kintsugi transforms brittle UI test automation and codebase maintenance into a governed, self-sustaining quality engineering process. By combining multi-strategy generation with rigorous Critic verification and human approval gates, it reduces maintenance overhead while guaranteeing that no defect is ever hidden."

---

## Slide 18: Key References (IEEE Style)

- **[1]** M. Hammoudi, G. Rothermel, and P. Tonella, "Why do record/replay tests of web applications break?," in *Proc. IEEE Int. Conf. Softw. Testing, Verification and Validation (ICST)*, 2016, pp. 180–190.
- **[2]** M. Leotta, A. Stocco, F. Ricca, and P. Tonella, "ROBULA+: An algorithm for generating robust XPath locators for web testing," *Journal of Software: Evolution and Process*, vol. 28, no. 3, pp. 177–204, 2016.
- **[3]** M. Nass, E. Alégroth, and R. Feldt, "Improving web element localization by using a large language model," *Software Testing, Verification and Reliability*, vol. 34, no. 7, Art. no. e1893, 2024.
- **[4]** A. Kluge and A. Stocco, "Web element relocalization in evolving web applications: A comparative analysis and extension study," *Empirical Software Engineering*, vol. 31, no. 6, Art. 175, 2026.
- **[5]** J. Huang, X. Chen, S. Mishra et al., "Large Language Models Cannot Self-Correct Reasoning Yet," in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2024.
- **[6]** S. Stewart and D. Burns, "WebDriver," W3C Recommendation, Jun. 5, 2018.
- **[7]** Healenium, "Healenium: Self-healing library for Selenium," GitHub repository, 2026.
- **[8]** R. Parasuraman, T. B. Sheridan, and C. D. Wickens, "A model for types and levels of human interaction with automation," *IEEE Trans. Systems, Man, and Cybernetics*, vol. 30, no. 3, pp. 286–297, 2000.

> **Speaker Notes:**  
> "Thank you for your time and attention. We now invite any questions or discussion."
