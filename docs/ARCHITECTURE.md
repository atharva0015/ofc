# Architecture

Fail-closed autonomous self-healing and code optimality framework for test suites and codebases.

## 1. High-Level System Architecture

The framework comprises two complementary healing loops operating under strict fail-closed safety policies:

```text
                                +-----------------------------+
                                |  Target Codebase / Test Run |
                                +--------------+--------------+
                                               |
                     +-------------------------+-------------------------+
                     |                                                   |
                     v                                                   v
      [1. Test Locator & API Healing]                     [2. Codebase Auto-Healing & Optimality]
  failing test / locator drift / API diff                  source code scanner / syntax / complexity
                     |                                                   |
                     v                                                   v
             `healing/classifier/`                               `healing/codebase/scanner.py`
      (classifies failure, blocks regressions)               (detects bugs & performance bottlenecks)
                     |                                                   |
                     v                                                   v
              `healing/matching/`                             `healing/codebase/llm_client.py`
      (Healenium / AST / similarity ranking)                 (Local LLM via Ollama + AST fallback)
                     |                                                   |
                     v                                                   v
              `healing/sandbox/`                                 `healing/codebase/sandbox.py`
      (isolated replay of up to 3 attempts)                  (isolated pytest & execution verification)
                     |                                                   |
                     v                                                   v
               `healing/critic/`                                `healing/codebase/optimizer.py`
      (deterministic, state, network, intent)                (O(N^2)->O(1), memoization, buffer joins)
                     |                                                   |
                     v                                                   v
               `healing/policy/`                                   `healing/codebase/xai.py`
      (confidence gating, human review L3)                  (XAI structured audit record & diffs)
                     |                                                   |
                     v                                                   v
               `healing/gitops/`                            `healing/codebase/studio.html`
      (reviewed PRs with diff & evidence)                   (3-stage wizard UI on port 8081)
```

## 2. Microservice Layout & Ports

| Service | Port | Path | Purpose |
|---|---|---|---|
| **Codebase Auto-Healing Studio** | `8081` | `healing/codebase/app.py` | 3-stage upload wizard, animated 5.2s radar scanner, defect & algorithmic optimization, XAI audit diff viewer, Dark/Light theme. |
| **Quality Gates Dashboard** | `8080` | `healing/dashboard/app.py` | Read-only local dashboard showing quality gates (11 PASS / 0 FAIL / 1 UNVERIFIED), recent explanation records, and metrics. |
| **NovaMart Demo Storefront** | `8082` | `demo_app/app.py` | Standalone e-commerce demo application with real-world business logic and seeded defect injection for live testing (strictly decoupled). |

## 3. Core Modules

### 3.1 Test Healing Engine
- `healing/adapters/`: Normalizes runner events from pytest/Selenium and API tests.
- `healing/classifier/`: Assigns failures into 6 distinct classes; immediately escalates genuine regressions, API contract violations, and environment failures.
- `healing/matching/`: Proposes locator candidates using Healenium algorithms, AST structural matching, and weighted feature rescoring.
- `healing/sandbox/`: Executes in-process re-execution in isolated environments with allowlists and state resets.
- `healing/critic/`: Four-layer validation (deterministic checks, DOM state, network state, user intent).
- `healing/policy/`: Confidence gating ($\tau_A$, $\tau_S$), ambiguity margins, budget caps, and A0–A4 autonomy policy.
- `healing/gitops/`: AST-based locator replacement, bot branch generation, and pull request assembly.

### 3.2 Codebase Auto-Healing & Optimality Engine (`healing/codebase/`)
- `scanner.py`: Inspects Python code using AST and dynamic checks. Classifies bugs (zero division, mutable default parameters, unclosed file descriptors, missing imports) and performance bottlenecks ($O(N^2) \rightarrow O(1)$ linear lookups in loops, unmemoized exponential recursion, string concatenation loops).
- `healer.py` & `llm_client.py`: Synthesizes bug fixes using local free LLMs (via Ollama at `http://localhost:11434`) or deterministic rule-based AST synthesis fallback for 100% offline reliability.
- `optimizer.py`: Transforms inefficient algorithms into optimal structures (pre-allocated sets for constant-time membership lookups, `@lru_cache` dynamic programming memoization, and list buffer joining).
- `app.py`: FastAPI backend exposing `/api/upload`, `/api/heal/{id}`, `/api/optimize/{id}`, `/api/download/{id}`, and `/api/status`.

### 3.3 Explainable AI (XAI) & Audit
- Structured XAI record emitted prior to any human-readable narrative.
- Records failure class, candidate scores, rejected candidates with reasons, Critic verification layers, applied policy thresholds, model/prompt versions, and SHA-256 integrity hashes.
- Interactive syntax-highlighted unified diffs for developer review.

## 4. Safety Invariants
1. **Deterministic Core, Probabilistic Edges**: Scoring, gating, policies, and code modifications are plain code; AI models only propose candidates.
2. **Fail Closed**: Unknown, low-confidence, or conflicting inputs immediately fail the test and escalate to a human.
3. **No Contract Mutation**: API contracts, assertions, and performance thresholds are never auto-healed.
4. **Security & Privacy by Default**: Secrets originate from environment variables; personal identifiable information (PII) is masked before external calls; AST transformations modify only targeted definitions.
