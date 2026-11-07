# KINTSUGI: AN LLM DRIVEN SELF HEALING FRAMEWORK
## Part 2: Implementation Plan, Results, Discussions, Conclusion and References

*(Continued from Part 1 — Chapters 4 through 7, Appendices and Acknowledgements)*

---

<!-- Page 71 -->

# Chapter 4: Implementation Plan and Experimental Setup of the 
Proposed System 
This chapter describes how VeriHeal  will be built and evaluated in Semester  VIII. As of the 
end of Semester VII the project is at the design stage: no component has been implemented and 
no experiment has been run. Tools are therefore marked as planned or used, and every sample 
input in this chapter is labelled as representative. 
## 4.1 Experimental Setup 
Table 4.1 lists the planned development and evaluation environment and marks what has 
actually been used so far. 
Table 4.1: Development and evaluation environment 
Item Choice Status (end of Sem VII) 
Operating system Linux (Ubuntu) for CI; team laptops with 
Docker (macOS / Windows WSL2 / Linux) 
Planned 
Language Python 3 Planned 
Test stack Selenium WebDriver 4, pytest, Chromium Planned 
Libraries Python ast (patching), HTTP client, JSON-
schema validator, image library for redaction 
Planned 
AI models / APIs One hosted LLM via the provider-agnostic 
gateway; optionally one locally hosted open-
weights model for comparison [TEAM 
DECISION: provider and model] 
Planned 
Database PostgreSQL (SQLite permitted in P1) Planned 
Service / UI FastAPI healing service and dashboard Planned 
Subject application Spring PetClinic REST (OpenAPI spec 
included) + Angular front end, both 
Dockerised [36], [37] 
Planned 
Baseline tool Healenium in proxy mode [4] Planned 
CI/CD GitHub Actions with branch protection [48] Planned 
Cloud / hardware Team laptops; GitHub-hosted runners; one 
small VM or team server for the dashboard 
Planned 
Documentation tools LaTeX, PlantUML, Graphviz, Python 
(matplotlib) 
Used for this report 
Reproducibility. The benchmark will be versioned in a repository containing: the pinned 
PetClinic commits, Docker Compose files, the test suite, mutation scripts, the random seeds

<!-- Page 72 -->

used to select mutation targets, and the analysis scripts. Every run records the commit SHA, 
mutation ID, configuration (B0-B4), model name and version, and policy version. 
## 4.2 Input and Dataset Description 
### 4.2.1 Subject application and test suite 
Spring PetClinic is an open-source sample application. Its REST version exposes an OpenAPI 
specification and Swagger UI and can be started with Docker; the Angular project is a client -
only front end for this REST API  [36], [37]. The planned UI test suite c overs its main user 
flows: finding and listing owners, adding and editing owners, adding and editing pets, adding 
visits, and listing veterinarians, specialties and pet types. The suite will be written in Python 
with page objects, so every locator is defined once (SR-1). The final number of tests is [TEAM 
INPUT: to be fixed in P1; planning assumption 25-35 tests]. 
### 4.2.2 Benchmark construction by mutation 
Because the ground truth must be known exactly, the benchmark is built by applying controlled 
mutation operators to the PetClinic front end and API (Table  4.2). The operator families are 
motivated by the breakage causes reported by Hammoudi et al.  [3] and by the change types in 
Table 3.4. Each mutation instance changes one element (or one API field) used by at least  one 
test, and is labelled drift (the test should still pass after healing) or regression (the test must 
fail). 
Table 4.2: Mutation operators of the benchmark 
ID Operator Example change Ground truth 
MO1 Id / name rename id="save-owner" -> id="owner-
submit" 
Drift 
MO2 Class change class="btn btn-primary" -> 
class="btn btn-success" 
Drift 
MO3 Wrapper insertion Button wrapped in a new <div> Drift 
MO4 Sibling reorder Two form groups swapped Drift 
MO5 Text rewording (same 
meaning) 
"Add Owner" -> "Add owner" Drift 
MO6 ARIA / data attribute 
change 
aria-label edited; data-* removed Drift 
MO7 Tag change, same role <a> styled as button -> <button> Drift 
RO1 Element removed Submit button deleted Regression 
RO2 Element hidden / 
disabled 
disabled added; display:none Regression

<!-- Page 73 -->

ID Operator Example change Ground truth 
RO3 Control replaced "Save" replaced by "Delete" in the same 
place 
Regression 
RO4 Behaviour broken Click handler removed; form no longer 
submits 
Regression 
RO5 Look-alike decoy Second button with similar attributes added; 
original removed 
Regression 
AO1 Approved API change Field renamed, spec updated, version 
bumped, change approved 
Intended change (E2) 
AO2 Contract violation Response omits a required field; spec 
unchanged 
Regression (E2) 
AO3 Unapproved breaking 
change 
Field type changed in spec without approval 
record 
Regression (E2) 
Splits. Mutation instances are split, stratified by operator, into a calibration split (about 40%, 
used to tune weights and thresholds) and an evaluation split (about 60%, used once for the 
reported results). No mutated element appears in both splits. The target size is at least 30 
instances per drift operator and 20 per regression operator [TEAM INPUT: confirm after P1 
effort estimate]; with fewer instances the confidence intervals of Eq. 3.9 become wide, which 
will be reported. 
### 4.2.3 Representative sample inputs 
The following samples show the form of the inputs. They are representative examples written 
for this report, modelled on a PetClinic-style owner form; the real markup will be captured from 
the pinned PetClinic version in P1. 
Listing 4.1: Sample test input: page object and test (planned style) 
# pages/owner_page.py 
from selenium.webdriver.common.by import By 
class OwnerPage: 
    FIRST_NAME = (By.ID, "firstName") 
    LAST_NAME  = (By.ID, "lastName") 
    SAVE_BTN   = (By.ID, "save-owner")        # locator that mutation MO1 will break 
    def __init__(self, d): self.d = d 
    def add_owner(self, first, last): 
        self.d.find_element(*self.FIRST_NAME).send_keys(first) 
        self.d.find_element(*self.LAST_NAME).send_keys(last) 
        self.d.find_element(*self.SAVE_BTN).click() 
 
# tests/test_owner.py 
def test_add_owner(healing_driver, base_url): 
    healing_driver.get(base_url + "/owners/add") 
    OwnerPage(healing_driver).add_owner("Asha", "Rao") 
    assert "Asha Rao" in healing_driver.find_element(By.TAG_NAME, "table").text 
Listing 4.2: Representative DOM before and after mutation MO1 + MO3 
<!-- before (fingerprint recorded) --> 
<form id="add-owner-form"> 
  <input id="firstName" name="firstName"> <input id="lastName" name="lastName">

<!-- Page 74 -->

<button id="save-owner" class="btn btn-primary" type="submit">Add Owner</button> 
</form> 
<!-- after (locator By.ID "save-owner" no longer matches) --> 
<form id="add-owner-form"> 
  <input id="firstName" name="firstName"> <input id="lastName" name="lastName"> 
  <div class="form-actions"> 
    <button id="owner-submit" class="btn btn-primary" type="submit">Add Owner</button> 
    <button id="cancel" class="btn btn-default" type="button">Cancel</button> 
  </div> 
</form> 
Listing 4.3: Representative element fingerprint stored in M4 (JSON) 
{ "step_key": "tests/test_owner.py::test_add_owner#5", 
  "tag": "button", "id": "save-owner", "name": null, 
  "classes": ["btn", "btn-primary"], "text": "Add Owner", 
  "role": "button", "acc_name": "Add Owner", 
  "xpath": "/html/body/app-root/div/form/button", 
  "neighbours": ["Last Name", "Telephone"], "bbox": [248, 502, 104, 36], 
  "url_pattern": "/owners/add", "app_version": "<commit-sha>" } 
Listing 4.4: Representative accessibility-tree node (simplified from a CDP AXNode) 
{ "role": {"value": "button"}, "name": {"value": "Add Owner"}, 
  "properties": [{"name": "focusable", "value": {"value": true}}], 
  "backendDOMNodeId": 142 } 
Listing 4.5: LLM Generator response schema (enforced by the LLM Gateway) 
{ "type": "object", "required": ["candidates"], 
  "properties": { "candidates": { "type": "array", "maxItems": 5, 
    "items": { "type": "object", "required": ["locator", "strategy", "rationale"], 
      "properties": { 
        "locator":   {"type": "string", "maxLength": 300}, 
        "strategy":  {"enum": ["css", "xpath", "id", "name", "role_name"]}, 
        "rationale": {"type": "string", "maxLength": 400} } } } }, 
  "additionalProperties": false } 
Listing 4.6: Representative API schema-change input for E2 (OpenAPI fragment, AO1) 
# baseline spec (v1)                     # changed spec (v2, approved change label) 
Owner:                                   Owner: 
  required: [firstName, lastName,          required: [firstName, lastName, 
             telephone]                               phoneNumber] 
  properties:                              properties: 
    telephone: {type: string}                phoneNumber: {type: string} 
# E2 result: breaking change "telephone -> phoneNumber" detected by spec diff; 
# approval record present -> INTENDED CHANGE -> A2 suggestion only 
### 4.2.4 Screenshots to be captured 
No screenshots of the subject application exist yet. Figure 4.1 lists the screenshots that must be 
captured in P1. 
PLACEHOLDER - screenshots not yet captured To capture in P1 from the pinned PetClinic version: 
(a) owner search page, (b) add-owner form before and after mutation MO1+MO3, (c) the same form 
with RO1 (button removed), (d) accessibility tree of the form in Chrome DevTools, (e) Swagger UI of 
the owner endpoint. 
Figure 4.1: Placeholder for input screenshots of the subject application

<!-- Page 75 -->

## 4.3 Test Cases 
Table 4.3 lists the scenarios the system is designed for, with the expected outcome. "Actual 
outcome" will be filled in during Semester VIII; no test case has been executed yet. 
Table 4.3: Test cases 
ID Scenario Input Expected outcome Actual 
TC-
01 
Successful execution Unmodified PetClinic PASSED; fingerprints stored; 
no heal 
Not yet run 
TC-
02 
Locator drift MO1 on Save button C1; M5a candidate passes H1-
H5; A3; PASSED-HEALED; 
PR opened 
Not yet run 
TC-
03 
DOM restructuring MO3 wrapper + MO4 
reorder 
A3 or A2; correct element Not yet run 
TC-
04 
CSS selector change MO2 on CSS-located 
element 
A3 or A2; correct element Not yet run 
TC-
05 
Accessibility attribute 
change 
MO6 aria-label edited A2 (name change) unless 𝑐>=
𝜏𝐴 
Not yet run 
TC-
06 
Genuine regression: 
removed 
RO1 H4 fails for all; 
FAIL_DEFECT; no PR 
Not yet run 
TC-
07 
Genuine regression: 
disabled 
RO2 H3 fails; FAIL_DEFECT Not yet run 
TC-
08 
False-heal trap: 
replaced control 
RO3 ("Delete" in place of 
"Save") 
H4 name gate fails; 
FAIL_DEFECT 
Not yet run 
TC-
09 
False-heal trap: look-
alike decoy 
RO5 No A3; FAIL_UNCERTAIN or 
FAIL_DEFECT 
Not yet run 
TC-
10 
Behaviour broken RO4 H5 replay fails assertion; 
FAIL_UNCERTAIN 
Not yet run 
TC-
11 
Timing / flaky Artificial 3 s delay before 
render 
C3; no heal; reported flaky Not yet run 
TC-
12 
Assertion failure Wrong owner name 
displayed 
C4; no heal Not yet run 
TC-
13 
Invalid test data Test submits invalid 
telephone; app shows 
validation error 
C4 (or C5 for HTTP 400); no 
heal; data never changed 
Not yet run 
TC-
14 
Validation failure of 
LLM candidate 
LLM proposes a non-
existent locator 
H1 fails; candidate rejected and 
logged 
Not yet run 
TC-
15 
Invalid LLM output Response not matching 
schema 
Discarded; pipeline continues 
with M5a 
Not yet run 
TC-
16 
API schema change 
(approved) 
AO1 E2: intended change; A2 
suggestion; test still fails 
Not yet run 
TC-
17 
API contract 
violation 
AO2 E2: contract violation; reported 
to API owner 
Not yet run 
TC-
18 
Unapproved breaking 
change 
AO3 E2: unapproved breaking 
change 
Not yet run 
TC-
19 
Human approval Reviewer approves PR 
from TC-02 
Merge by human; fingerprint 
updated; audit entry 
Not yet run

<!-- Page 76 -->

ID Scenario Input Expected outcome Actual 
TC-
20 
Human rejection Reviewer rejects a PR PR closed; candidate 
blacklisted; next run fails 
normally 
Not yet run 
TC-
21 
Healing service 
unavailable 
Service stopped Original exception raised; run 
continues (NFR-05) 
Not yet run 
TC-
22 
PII in page Owner form pre-filled 
with e-mail / phone 
Values masked in stored 
context and in LLM prompt 
Not yet run 
TC-
23 
Non-unique patch 
site 
Same locator defined 
twice 
M9 creates manual-fix task; no 
PR 
Not yet run 
## 4.4 Performance Evaluation Parameters 
### 4.4.1 Notation 
For a configuration under test, let 𝐷 be the set of drift instances and 𝑅 the set of regression 
instances in the evaluation split. For each instance the system produces one outcome: healed 
(A3), suggested (A2), or failed (FAIL_DEFECT, FAIL_UNCERTAIN, or unhealed). A heal or 
suggestion is correct if its locator resolves to the ground -truth element of a drift instance. Let 
𝐻 be the set of A3 heals over 𝐷 U 𝑅, 𝐻+ subset-of 𝐻 the correct heals, and 𝑄 the set of A2 suggestions 
with 𝑄+ the correct ones. 
### 4.4.2 Metric definitions 
Healing Success Rate - share of drift instances healed correctly at run time:  
HSR=
|𝐻+ intersect 𝐷|
|𝐷| . 
 (4.1) 
Locator Recovery Rate - share of drift instances for which the correct element is found either 
as a heal or as a suggestion:  
LRR=|(𝐻+ U 𝑄+) intersect 𝐷| |𝐷| . 
 (4.2) 
Healing Precision and False-Heal Rate - quality of the heals that were applied:  
Precision=|𝐻+| |𝐻| ,  FHR=1−Precision=|𝐻\𝐻+| |𝐻| .

<!-- Page 77 -->

(4.3) 
Regression Masking Rate - share of regression instances that ended as PASSED or PASSED-
HEALED (target 0):  
RMR=
|{𝑟 in 𝑅:outcome(𝑟) in {PASSED,PASSED-HEALED}}|
|𝑅| . 
 (4.4) 
Defect Detection Rate  - share of regression instances reported as FAIL_DEFECT or 
FAIL_UNCERTAIN with a defect hint:  
DDR=|{𝑟 in 𝑅:outcome(𝑟) in {FAIL_DEFECT,FAIL_UNCERTAIN}}| |𝑅| . 
 (4.5) 
Healing latency - time from the exception to the decision, per failure (Eq.  3.10); reported as 
median (p50) and 95th percentile (p95), separately for M5a-only and LLM-assisted heals. 
Test execution time and overhead - on runs without failures, with 𝑇𝑤𝑖𝑡ℎ and 𝑇𝑤𝑖𝑡ℎ𝑜𝑢𝑡 the suite 
times with and without VeriHeal (median of 𝑟 repetitions):  
𝑂=𝑇𝑤𝑖𝑡ℎ−𝑇𝑤𝑖𝑡ℎ𝑜𝑢𝑡
𝑇𝑤𝑖𝑡ℎ𝑜𝑢𝑡
. 
 (4.6) 
On runs with failures the total suite time is reported per configuration. 
Maintenance effort - measured in a small timed study. For a sample of 𝑚 broken tests from 
the evaluation split, a participant who did not create the mutation repairs each test manually 
(time 𝑡𝑖 𝑚𝑎𝑛, from seeing the failure to a passing fix). Separately, a participant reviews the 
VeriHeal PR or suggestion for the same tests (time 𝑡𝑖 𝑟𝑒𝑣, plus manual repair time if the 
suggestion is rejected). The effort reduction is  
𝛥ME=1−
∑ 𝑡𝑖 𝑟𝑒𝑣 𝑖
∑ 𝑡𝑖 𝑚𝑎𝑛 𝑖 . 
 (4.7)

<!-- Page 78 -->

This is a small student study; it will be reported with its sample size and threats to validity, not 
generalised. 
Flaky Test Rate - each configuration runs the unmodified suite 𝑟 times (default 𝑟=5); a test 
is flaky if its outcomes differ:  
FTR=
|{𝑡:outcomes of 𝑡 over 𝑟 runs are not all equal}|
|tests| . 
 (4.8) 
It checks that VeriHeal does not introduce flakiness. 
Cost per healing operation - with 𝑇𝑗 𝑖𝑛,𝑇𝑗 𝑜𝑢𝑡 the input and output tokens of LLM call 𝑗, prices 
𝑝𝑖𝑛,𝑝𝑜𝑢𝑡 per million tokens, 𝐶𝑖𝑛𝑓𝑟𝑎 the attributable infrastructure cost and 𝑁ℎ𝑒𝑎𝑙 the number of 
heal attempts:  
𝐶ℎ𝑒𝑎𝑙 =
∑ (𝑇𝑗 𝑖𝑛 𝑝𝑖𝑛+𝑇𝑗 𝑜𝑢𝑡 𝑝𝑜𝑢𝑡)𝑗 /106+𝐶𝑖𝑛𝑓𝑟𝑎
𝑁ℎ𝑒𝑎𝑙
. 
 (4.9) 
Critic usefulness - veto precision: the share of Critic vetoes that blocked a candidate which 
was in fact wrong. If veto precision is low, the Critic is removed. 
All proportions are reported with Wilson 95% intervals (Eq. 3.9). 
### 4.4.3 Baselines and evaluation protocol 
Table 4.4 lists the five configurations that will be compared on the same mutation instances. 
Table 4.4: Configurations compared 
ID Configuration Purpose 
B0 Selenium without healing Lower bound; every drift instance fails; every regression fails 
correctly 
B1 Healenium (proxy mode) Existing open-source self-healing tool 
B2 VeriHeal, M5a only (no 
LLM) 
Value of deterministic matching plus gates 
B3 LLM-only selection without 
gates 
Ablation: shows the effect of removing validation 
B4 VeriHeal full Proposed system

<!-- Page 79 -->

Protocol. (1) Start the pinned PetClinic version and run the suite three times to record 
fingerprints and check stability. (2) For each mutation instance in the evaluation split and each 
configuration, apply the mutation, run the affected tests, record outcomes and  metrics, and 
revert. (3) Compute all metrics from M8 exports with the versioned analysis scripts. (4) Run 
the timing study for maintenance effort. (5) Report results per operator and overall. 
Acceptance criteria. The project's acceptance criteria are the go/no -go gates in Table 3.6: in 
particular RMR =0 and FHR within target for B4, and no increase in FTR compared with B0. 
## 4.5 Special Requirements 
1. External APIs. An LLM API (from P2) and the GitHub REST API (from P3). The 
LLM provider's data -retention and training -use terms must be reviewed by the team 
before any page data is sent [TEAM DECISION]. 
2. Cloud services. GitHub-hosted runners. GitHub's documentation states that standard 
GitHub-hosted runners are free for public repositories, and that GitHub Free accounts 
receive a monthly included usage amount for private repositories  [51]. One small VM 
or a team machine hosts the dashboard and database. 
3. Hardware. As in Table 3.10; no GPU for the MVP. 
4. Repository permissions. A bot account or app with access to the single test repository, 
able to push branches and open PRs; no admin rights; branch protection on main 
requiring one approving review and passing checks [48]. 
5. CI/CD dependencies.  Docker images for Chrome, PetClinic REST and Angular; 
Python dependencies pinned with hashes. 
6. Security requirements. As in Table 3.15, including the redaction test suite (TC-22). 
### 4.5.1 Cost and resource estimation 
All values in this subsection are estimates based on stated assumptions . No cost has been 
incurred yet; actual costs will be measured with Eq.  4.9. LLM prices change often and differ 
between providers and models, so the estimate uses symbolic prices and one illustrative price 
pair, which must be replaced by the selected provider's official price list. Table  4.5 states the 
assumptions and Table 4.6 summarises the other resources.

<!-- Page 80 -->

Table 4.5: Assumptions for the LLM cost estimate 
Assumption Value Basis 
Generator input per call (pruned DOM, a11y 
subtree, fingerprint, intent, top-𝑘) 
6,000 tokens Design limit max_tokens of 
Algorithm 3.2 
Generator output per call 500 tokens Schema limits (Listing 4.5) 
Critic input / output per call 2,500 / 200 tokens Evidence summary only 
Illustrative prices 𝑝𝑖𝑛 / 𝑝𝑜𝑢𝑡 US$1 / US$5 per million tokens Hypothetical round numbers for illustration only 
Heal attempts in full evaluation (all 
configurations, calibration + evaluation, 3 
repetitions) 
about 3,000 Planning assumption 
Share of attempts that call the LLM 50% Planning assumption (worst case 
for B3: 100%) 
With these assumptions one LLM -assisted heal costs (8,500×1+700×5)/106 =
US$0.012, and the full evaluation needs about 3,000×0.5×0.012≈US$18 of LLM usage, 
plus development and debugging calls. With a provider whose prices are ten times higher the 
figure would be about US$180, so the team should fix a hard monthly cap in the LLM Gateway 
(NFR-09) and choose the model after checking its price. Per-heal budget for gate G2: [TEAM 
DECISION; suggested US$0.05 per LLM-assisted heal]. 
Table 4.6: Resource and infrastructure estimate 
Item Estimate Type 
LLM API usage As computed above Estimated 
Model inference (local 
option) 
Requires a GPU machine; not planned for 
MVP 
Not estimated 
Computer-vision 
infrastructure 
None for MVP (no CNN) - 
Cloud hosting One small VM if no team machine is 
available; provider pricing to be checked 
Estimated, not priced 
Database and storage PostgreSQL on the same VM; redacted 
artifacts with 30-day retention (a few GB) 
Estimated 
CI/CD execution Free on public repositories; included usage 
on private repositories [51] 
Documented terms 
Development effort 4 members × about 10 h/week × 16 weeks 
≈ 640 person-hours 
Planning assumption [TEAM 
INPUT] 
## 4.6 Partial Code 
No project code has been implemented yet. The listings below are design-level illustrations of 
planned interfaces, written to make the design concrete. A version of Listing 4.7 was executed 
once on a small hand-made example only to check that it runs; this is not an experimental result. 
Listing 4.7: Planned similarity scoring (Eqs. 3.1-3.4) - illustrative

<!-- Page 81 -->

from math import dist 
def jaccard(a: set, b: set) -> float:                       # Eq. 3.2 
    return 1.0 if not a and not b else len(a & b) / len(a | b) 
def levenshtein(a: str, b: str) -> int: 
    prev = list(range(len(b) + 1)) 
    for i, ca in enumerate(a, 1): 
        cur = [i] 
        for j, cb in enumerate(b, 1): 
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb))) 
        prev = cur 
    return prev[-1] 
def edit_sim(a: str, b: str) -> float:                       # Eq. 3.3 
    return 1.0 if not a and not b else 1 - levenshtein(a, b) / max(len(a), len(b)) 
def loc_sim(p, q, d_max=400.0) -> float:                     # Eq. 3.4 
    return max(0.0, 1 - dist(p, q) / d_max) 
def score(fp: dict, cand: dict, w: dict, sim: dict) -> float:  # Eq. 3.1 
    num = den = 0.0 
    for k, wk in w.items(): 
        if fp.get(k) in (None, "", [], ()): 
            continue                          # attribute absent in fingerprint 
        num += wk * sim[k](fp[k], cand.get(k) or type(fp[k])()) 
        den += wk 
    return num / den if den else 0.0 
Purpose: implements the weighted multi-attribute similarity of M5a; sim maps each attribute to 
its function as in Table 3.16. 
Listing 4.8: Planned HealingDriver interface (module M1) - illustrative 
from selenium.common.exceptions import NoSuchElementException 
class HealingDriver: 
    def __init__(self, driver, client, step_ctx): 
        self._d, self._heal, self._step = driver, client, step_ctx 
    def find_element(self, by, value): 
        try: 
            el = self._d.find_element(by, value) 
        except NoSuchElementException as exc: 
            outcome = self._heal.request(self._step.key, (by, value), self._d) 
            if outcome.kind == "HEAL":                 # A3, validated by M6/M7 
                self._step.mark_healed(outcome)        # status PASSED-HEALED 
                return self._d.find_element(*outcome.locator) 
            raise exc                                  # A2 / FAIL_*: original failure 
        self._heal.record_fingerprint(self._step.key, el, self._d)  # Alg. 3.3 (batched
) 
        return el 
    def __getattr__(self, name):                       # delegate all other calls 
        return getattr(self._d, name) 
Purpose: shows how M1 wraps Selenium without changing test code, re -raises the original 
exception for every non -HEAL decision (NFR -05), and records fingerprints on success. 
Fingerprint recording will be batched and asynchronous to meet NFR-04. 
## 4.7 Risk Register 
Table 4.7 is the risk register. Probability (P) and impact (I) are rated Low / Medium / High by 
the authors.

<!-- Page 82 -->

Table 4.7: Risk register 
ID Risk P I Mitigation Contingency 
R1 Incorrect AI-
generated correction 
H M LLM proposals only; H1-H5 
gates; schema-constrained output 
Disable M5b (B2 
configuration) 
R2 False healing (wrong 
element) 
M H H4 semantic gate, H5 replay, 
calibrated 𝜏𝐴, downgrade rules 
Raise 𝜏𝐴 or disable A3 (A2 
only) 
R3 Genuine defect 
masked 
M H FAIL_DEFECT rules; RMR =0 
gate; locator-only invariant 
Any masked case stops the 
phase until fixed 
R4 Data leakage to LLM 
provider 
M H Redaction, pruned context, 
gateway secret scan, provider 
terms review 
Switch to local model or 
disable LLM 
R5 LLM hallucination H M Execution validation; JSON 
schema; Critic advisory 
As R1 
R6 Prompt injection via 
page content 
L H Untrusted-data framing, no state-
changing tools, validation 
Disable LLM for affected 
pages 
R7 Infrastructure failure 
(service, DB, runner) 
M M Fail-safe re-raise (NFR-05); health 
checks 
Run without healing; re-run 
later 
R8 Vendor lock-in M M Provider-agnostic gateway; 
prompts and schemas in repo 
Change provider configuration 
R9 Excessive inference 
cost 
M M Deterministic-first; per-run and 
monthly caps; cost logging 
Lower 𝑁𝐿𝐿𝑀; smaller model 
R1
0 
CI/CD integration 
failure 
M M Integration tested in P3 on a fork; 
separate repair job 
Manual trigger of repair job 
R1
1 
CDP accessibility 
API changes 
(Selenium moving to 
BiDi [29]) 
M M JS fallback for role/name; pinned 
browser version 
Use JS fallback only 
R1
2 
Benchmark not 
representative 
M M Operators based on published 
breakage taxonomy [3]; report per 
operator 
State as threat to validity 
R1
3 
Schedule overrun M M Gates, buffer week, extensions 
optional 
Drop P4

<!-- Page 83 -->

# Chapter 5: Results and Discussions 
Status statement.  Major Project Part  1 (Semester  VII) covered study and design only. No 
module of VeriHeal has been implemented and no experiment has been executed. This chapter 
therefore contains no experimental results. It presents (i) the result templates that will be filled 
in Semester  VIII, (ii) the step -by-step validation procedure, (iii) hypotheses about expected 
trends, clearly separated from results, and (iv) a comparison with existing systems based only 
on published, verified figures. 
## 5.1 Presentation of Results 
Tables 5.1 and  5.2 are the templates for the main results. Every cell marked " -" is to be 
collected; none has a value yet. 
Table 5.1: Template: overall results per configuration (evaluation split; values with Wilson 95% 
intervals) 
Metric B0 B1 B2 B3 B4 
HSR (Eq. 4.1) - - - - - 
LRR (Eq. 4.2) - - - - - 
Precision / FHR (Eq. 4.3) - - - - - 
RMR (Eq. 4.4) - - - - - 
DDR (Eq. 4.5) - - - - - 
Latency p50 / p95 (s) - - - - - 
Overhead 𝑂 (Eq. 4.6) - - - - - 
FTR (Eq. 4.8) - - - - - 
Cost per heal (Eq. 4.9) n/a n/a - - - 
Table 5.2: Template: results per mutation operator (B4 vs B1) 
Operator Instances B1 outcome B4 A3 B4 A2 B4 FAIL 
MO1-MO7 (each row) - - - - - 
RO1-RO5 (each row) - - - - - 
AO1-AO3 (E2 only) - n/a n/a - - 
The maintenance-effort study (Eq. 4.7) will be reported in a separate table with the number of 
tests, participants, median times and the computed 𝛥ME.

<!-- Page 84 -->

## 5.2 Step-by-Step Result Validation 
Results will be validated in the following order; a later step is not started until the earlier one is 
complete. 
1. Environment check. Unmodified suite passes three times on B0 and B4 (TC-01); FTR 
measured. 
2. Ground-truth check. For every mutation instance, a script confirms that the original 
locator breaks and that the ground-truth element exists (drift) or does not (regression). 
3. Functional test cases.  TC-01-TC-23 executed and the "Actual" column of Table  4.3 
filled. 
4. Calibration. Weights and thresholds tuned on the calibration split only (Algorithm 3.8); 
the chosen values recorded with the policy version. 
5. Evaluation runs. B0-B4 on the evaluation split; outcomes exported from M8. 
6. Metric computation. Versioned scripts compute all metrics with Wilson intervals; a 
second team member re -runs the scripts on the same export and must obtain identical 
numbers. 
7. Manual audit. A random sample of heals (at least 20 or all, whichever is smaller) is 
checked by hand against the ground truth. 
8. Gate review. Results compared with Table 3.6 and presented to the guide. 
## 5.3 Graphical and Tabular Analysis 
Figures 5.1, 5.2 and 5.3 are placeholders that specify the planned graphs. They contain no data.

<!-- Page 85 -->

Figure 5.1: Planned graph: Locator Recovery Rate per mutation operator and configuration 
(placeholder) 
 
Figure 5.2: Planned graph: False-Heal Rate and heal coverage versus threshold 𝜏𝐴 (placeholder) 
 
Figure 5.3: Planned graph: healing latency distribution (placeholder)

<!-- Page 86 -->

### 5.3.1 Expected trends (hypotheses, not results) 
The following hypotheses are stated before the experiments so that they can be confirmed or 
rejected; they are not findings. 
1. B0 has HSR =0 and RMR =0 by construction (no healing). 
2. B3 (LLM without gates) will show a higher FHR and a non -zero RMR, because it 
accepts the best LLM choice even on regression instances. 
3. B4 will have a lower HSR than B3 (some correct heals are downgraded to A2 or 
rejected) but a lower FHR and RMR =0. 
4. B2 will perform best on attribute -level drift (MO1, MO2) and worse on restructuring 
and wording changes (MO3-MO5), where B4's LLM candidates may help. 
5. Median latency of B2 will be dominated by the replay gate; LLM -assisted heals will 
add the LLM call time. 
## 5.4 Comparative Analysis with Existing Systems 
A direct quantitative comparison with existing systems requires running them on the same 
benchmark; this is planned (B1 Healenium). Until then, Figure  5.4 and Table  5.3 show 
published results. Each comparison is made only within one study (baseline and proposed 
technique on the same dataset); values from different studies are not comparable with each other 
because the datasets, metrics and setups differ.

<!-- Page 87 -->

Figure 5.4: Published element-localisation results, compared only within each study (data from [18], 
[19], [6]) 
Table 5.3: Published quantitative results of related approaches (as reported by their authors) 
Approach Dataset Reported result Metric 
ROBULA+ [9] 1,110 elements, 8 apps 8% broken (vs 22-78%) Locator robustness across 
releases 
WATERFALL [39] 7 apps 89.3% vs 28.9% Locator breakages repaired 
VISTA [40] 2,672 tests, 86 releases, 
4 apps 
about 81% Breakages repaired 
Similo [18] 801 pairs, 48 sites 11% vs 27% failures Localisation failures 
VON Similo [19] 1,163 pairs, 40 apps 94.7% vs 83.8% Localisation accuracy 
VON Similo + 
GPT-4 [6] 
804 pairs, 48 apps 40 vs 70 failures Localisation failures 
HybridSimilo [32] Extended benchmark 
(23× original) 
98.8% Elements with broken locators 
located 
VeriHeal (proposed
) 
PetClinic mutation 
benchmark 
To be measured HSR, LRR, FHR, RMR, DDR 
(Section 4.4) 
What these numbers do and do not show.  They show that similarity-based relocalisation is 
already accurate on its benchmarks, and that an LLM can reduce the remaining failures  [6]. 
They do not measure what happens on regression instances, where the "correct" outcome is to 
fail. VeriHeal's evaluation adds this dimension (RMR, DDR) and compares configurations on 
the same instances. 
## 5.5 Discussion of Findings 
The findings of Semester VII are findings of the study and design work, not of experiments:

<!-- Page 88 -->

1. Localisation is largely solved; safe acceptance is not. Published methods locate most 
intended elements  [19], [32]. Healing is now offered by mainstream 
frameworks [?playwright_agents], [?cypress_aigen], but in the studies and 
documentation reviewed we did not find the combination of calibrated acceptance 
thresholds, a semantic (role and accessible -name) gate, replay against the test's own 
assertions, a rule that reports suspected regressions as failures rather than skipping them, 
and mandatory human review of code changes. This combination is the gap 
VeriHeal targets. 
2. LLMs are best used as proposal generators.  Evidence on self -correction and LLM 
judges [31], [33] supports using execution results, not a second LLM, as the acceptance 
criterion. 
3. Headline numbers need protocols.  Several widely quoted self -healing figures lack 
baselines and measurement details (Table 2.17); the project's own figures will therefore 
be reported only with the protocol of Section 4.4. 
4. Schema healing must stay report-only. Automatically adapting test data to a changed 
API contract would hide exactly the failures that regression tests exist to find. 
Limitations and failure scenarios expected. Look-alike decoys (RO5) and wording changes 
(MO5) are the most likely sources of wrong candidates; behaviour-level regressions (RO4) can 
only be detected if the test has a meaningful assertion after the step; tests with weak assertions 
reduce the strength  of the replay gate. These will be analysed explicitly when results are 
available.

<!-- Page 89 -->

# Chapter 6: Conclusion 
This chapter summarises the study completed as Major Project Part 1 (Semester VII). 
## 6.1 Summary of Study Completed 
The project studied why automated web UI tests break and how they can be repaired safely. 
The literature survey (Chapter  2) reviewed empirical studies of test breakage and flakiness, 
robust locator generation, web test repair, similarity -based element relo calisation, LLM -
assisted localisation, AI -based self -healing frameworks and research on LLM reliability, 
together with the documentation of Selenium, Playwright, Cypress and Healenium. Every 
reference was checked against bibliographic records, and quantitative claims were classified as 
literature-reported, proposed targets or (in future) measured results. 
## 6.2 Problem Addressed 
Locator breakages cause a large share of web test failures and require repetitive manual 
repair [3]. Automatic healing can reduce this work, but a heal that is accepted without evidence 
can make a test pass on a genuine defect. The project addresses the problem of repairing broken 
locators automatically while ensuring by design that every repair is validated, that suspected 
regressions are reported as failures rather than healed, and that every code change is approved 
by a human (Section 1.7). 
## 6.3 Proposed Technical Contribution 
1. A validation-gated healing pipeline  that combines a deterministic multi -attribute 
matcher with LLM candidate generation, and accepts a candidate only after hard gates 
H1-H4 and a replay gate H5 that uses the test's own assertions as the oracle. 
2. A drift-versus-regression discrimination policy  with explicit FAIL_DEFECT and 
FAIL_UNCERTAIN outcomes (Table 3.4). 
3. A transparent autonomy model  (A0-A4) and human -in-the-loop policy in which 
automatic merging is prohibited and high -risk heals are downgraded to suggestions 
(Tables 3.2 and 3.3).

<!-- Page 90 -->

4. A calibrated decision rule that chooses the run-time threshold from the measured false-
heal rate with a Wilson upper bound (Eqs. 3.8-3.9). 
5. A report-only policy for API schema changes that separates contract violations from 
approved changes. 
6. A reproducible evaluation design  with mutation operators for drift and regressions, 
five configurations, precise metric definitions and go/no-go gates. 
## 6.4 Work Completed During Semester VII 
Table 6.1: Work completed and not completed in Semester VII 
Work item Status Evidence in this report 
Literature survey and reference verification Completed Chapter 2, Chapter 7 
Consolidated problem statement and scope Completed Sections 1.7, 2.7 
Requirements (FR, NFR, specific, SW, 
HW) 
Completed Section 3.5 
Architecture, UML, ER and DFD design Completed Sections 3.2-3.9 
Algorithms and equations Completed 
(design) 
Section 3.10 
Autonomy, security, risk and cost analysis Completed Sections 3.1.3, 3.9.1, 4.7, 4.5.1 
Benchmark, test cases and metrics design Completed 
(design) 
Sections 4.2-4.4 
UI/UX mock-ups Completed 
(mock-ups) 
Section 3.11 
Implementation of any module Not started - 
Experiments and results Not started Chapter 5 contains templates only 
## 6.5 Current Development Status 

As of the current implementation snapshot (November 2026), the project has transitioned from the initial design phase into a fully operational reference MVP and autonomous codebase healing system:

1. **Test Healing & Quality Framework**: Implemented in Python 3.12 with 222 passing tests in pytest, clean static analysis (Ruff), and full typing compliance (Mypy) across 60 source modules. The quality gates system reports 11 PASS / 0 FAIL / 1 UNVERIFIED.
2. **Codebase Auto-Healing & Optimality Studio (healing/codebase/app.py)**: A modern Web UI (http://localhost:8081) featuring a 3-stage interactive wizard: (1) Arbitrary codebase .zip upload or built-in sample selection with a 5.2-second animated radar scanning diagnostic; (2) Autonomous defect and algorithmic bottleneck classification; and (3) Explainable AI (XAI) audit breakdown with unified syntax-highlighted diffs and one-click zip export. Full Dark and Light theme toggle is supported.
3. **Dual Repair Synthesis**: Integrated with local free LLM inference servers (Ollama / LocalAI with Qwen2.5-Coder) and backed by a deterministic, rule-based AST synthesis fallback for 100% fail-closed offline reliability.
4. **Algorithmic Complexity Optimizations**: Autonomous transformations for (N^2) \rightarrow O(1)$ hash set membership in loops, dynamic programming caching (@lru_cache) for recursive functions, and list buffer joining for repeated string concatenations.
5. **Standalone Demonstration Storefront (demo_app/app.py)**: An independent NovaMart e-commerce application running on port 8082, strictly decoupled from the main healing system for realistic verification. 
## 6.6 Limitations 
1. The design has not yet been validated by experiments; all targets are proposals.

<!-- Page 91 -->

2. The benchmark uses one subject application and synthetic mutations, which may not 
represent all real-world changes. 
3. The replay gate is only as strong as the test's own assertions; tests without meaningful 
assertions after a step cannot reveal behavioural regressions. 
4. Reading the accessibility tree through CDP limits the MVP to Chromium -based 
browsers, and Selenium describes CDP support as temporary [29]. 
5. The maintenance-effort study will be small and performed by students, so its results will 
not generalise. 
6. LLM behaviour, prices and data policies may change during the project. 
## 6.7 Future Scope 
1. Implementation and evaluation in Semester VIII (phases P1-P4). 
2. Visual fallback (E1) and, if justified by data, a GUI element detector. 
3. API contract-drift classification (E2) and, later, synthetic test-data generation restricted 
to fixture PRs with contract checks. 
4. Adapters for Playwright, Cypress and mobile testing with Appium. 
5. Evaluation on additional open -source applications and, if possible, an industrial case 
study. 
6. Learning weights and thresholds per project from reviewer decisions, with periodic re -
calibration.

<!-- Page 92 -->

# Chapter 7: References 
References are numbered in order of first citation and formatted in IEEE style. Online sources 
were accessed on 5 November 2026. 
[1] S. Stewart and D. Burns, "WebDriver," W3C Recommendation, Jun. 5, 2018. [Online]. 
Available: https://www.w3.org/TR/2018/REC-webdriver1-20180605/ 
[2] Selenium Project, "Locator strategies," Selenium Documentation. [Online]. Available: 
https://www.selenium.dev/documentation/webdriver/elements/locators/ (accessed Nov. 5, 
2026) 
[3] M. Hammoudi, G. Rothermel, and P. Tonella, "Why do record/replay tests of web 
applications break?," in Proc. IEEE Int. Conf. Softw. Testing, Verification and Validation 
(ICST), 2016, pp. 180-190, doi: 10.1109/ICST.2016.16. 
[4] Healenium, "healenium," GitHub repository. [Online]. Available: 
https://github.com/healenium/healenium (accessed Nov. 5, 2026) 
[5] Healenium, "How Healenium works," Healenium Documentation. [Online]. Available: 
https://healenium.io/docs/how_healenium_works (accessed Nov. 5, 2026) 
[6] Microsoft, "Test agents," Playwright Documentation. [Online]. Available: 
https://playwright.dev/docs/test-agents (accessed Nov. 5, 2026) 
[7] Cypress.io, "AI test generation," Cypress Documentation. [Online]. Available: 
https://docs.cypress.io/app/guides/ai-test-generation (accessed Nov. 5, 2026) 
[8] M. Nass, E. Alégroth, and R. Feldt, "Improving web element localization by using a large 
language model," Softw. Testing, Verification and Reliability , vol. 34, no. 7, Art. no. e1893, 
2024, doi: 10.1002/stvr.1893.

<!-- Page 93 -->

Acknowledgements 
We are thankful to a number of individuals who have contributed towards our final year project 
and without their help; it would not have been possible. First  of all, we would like to express 
our gratitude to Ms. Prapti Sawant  our project guide and co -guide, for their prompt 
suggestions, guidance and encouragement over the course of our entire project. 
We sincerely appreciate Ms. Prapti Sawant , our project coordinators, for their tremendous 
assistance to our project. We also appreciate the supportof the faculty in our department. 
We express our sincere gratitude to our respected Director Bro. Shantilal Kujur, our Principal 
Dr. Deepak Jayaswal and our Head of Department (CMPN) Dr. 
Dakshata Panchal for providing the facilities, encouragement as well as a con -ducive 
environment for learning. 
Lastly, we would like to thank our parents and friends who played a crucial role  keeping us 
motivated throughout with their constant nurture and support. 
 
Sincerely, 
Atharva Chavan(11) 
 Prem Sontakke(43)  
Aditya Bagad(45)  
Sophia Dsilva(52)


### Complete Bibliographic References [1]–[51] (IEEE Style)

[1] S. Stewart and D. Burns, "WebDriver," W3C Recommendation, Jun. 5, 2018. [Online]. Available: https://www.w3.org/TR/2018/REC-webdriver1-20180605/  
[2] Selenium Project, "Locator strategies," Selenium Documentation. [Online]. Available: https://www.selenium.dev/documentation/webdriver/elements/locators/ (accessed Nov. 5, 2026)  
[3] M. Hammoudi, G. Rothermel, and P. Tonella, "Why do record/replay tests of web applications break?," in *Proc. IEEE Int. Conf. Softw. Testing, Verification and Validation (ICST)*, 2016, pp. 180–190, doi: 10.1109/ICST.2016.16.  
[4] Healenium, "healenium," GitHub repository. [Online]. Available: https://github.com/healenium/healenium (accessed Nov. 5, 2026)  
[5] Healenium, "How Healenium works," Healenium Documentation. [Online]. Available: https://healenium.io/docs/how_healenium_works (accessed Nov. 5, 2026)  
[6] Microsoft, "Test agents," Playwright Documentation. [Online]. Available: https://playwright.dev/docs/test-agents (accessed Nov. 5, 2026)  
[7] Cypress.io, "AI test generation," Cypress Documentation. [Online]. Available: https://docs.cypress.io/app/guides/ai-test-generation (accessed Nov. 5, 2026)  
[8] M. Nass, E. Alégroth, and R. Feldt, "Improving web element localization by using a large language model," *Softw. Testing, Verification and Reliability*, vol. 34, no. 7, Art. no. e1893, 2024, doi: 10.1002/stvr.1893.  
[9] M. Leotta, A. Stocco, F. Ricca, and P. Tonella, "ROBULA+: An algorithm for generating robust XPath locators for web testing," *Journal of Software: Evolution and Process*, vol. 28, no. 3, pp. 177–204, 2016.  
[10] Playwright, "Locators and strictness," Playwright Documentation. [Online]. Available: https://playwright.dev/docs/locators (accessed Nov. 5, 2026)  
[11] Cypress.io, "Best Practices: Selecting Elements," Cypress Documentation. [Online]. Available: https://docs.cypress.io/guides/references/best-practices#Selecting-Elements (accessed Nov. 5, 2026)  
[12] Q. Luo, F. Hariri, L. Eloussi, and D. Marinov, "An empirical analysis of flaky tests," in *Proc. 22nd ACM SIGSOFT Int. Symp. Foundations Softw. Eng. (FSE)*, 2014, pp. 643–653.  
[13] O. Parry, M. Hilton, and G. M. Kapfhammer, "A survey of flaky tests," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, vol. 31, no. 1, pp. 1–46, 2022.  
[14] A. Romano, Z. Song, S. Grandhi, W. Yang, and W. Wang, "An Empirical Analysis of UI-Based Flaky Tests," in *Proc. IEEE/ACM 43rd Int. Conf. Softw. Eng. (ICSE)*, 2021, pp. 1585–1597.  
[15] M. Nass, E. Alégroth, and R. Feldt, "Challenges in GUI-based test automation: A systematic literature review," *Journal of Systems and Software*, vol. 177, p. 110947, 2021.  
[16] A. M. Memon, "Automatically repairing event sequence-based GUI test suites for regression testing," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, vol. 17, no. 4, pp. 1–36, 2008.  
[17] S. R. Choudhary, D. Zhao, H. Versee, and A. Orso, "WATER: Web Application TEst Repair," in *Proc. 1st Int. Workshop on End-to-End Test Script Engineering (ETSE)*, 2011, pp. 24–29.  
[18] M. Nass, E. Alégroth, R. Feldt, M. Leotta, and F. Ricca, "Similarity-based Web Element Localization for Robust Test Automation," *ACM Transactions on Software Engineering and Methodology*, vol. 32, no. 3, pp. 1–30, 2023.  
[19] M. Nass, E. Alégroth, R. Feldt, and R. Coppola, "Robust web element identification for evolving applications by considering visual overlaps," in *Proc. IEEE Conf. Softw. Testing, Verification and Validation (ICST)*, 2023, pp. 258–268.  
[20] J. Wang et al., "Software Testing with Large Language Models: Survey, Landscape, and Vision," *IEEE Transactions on Software Engineering*, 2024.  
[21] X. Hou et al., "Large Language Models for Software Engineering: A Systematic Literature Review," *ACM Transactions on Software Engineering and Methodology*, 2024.  
[22] S. C. P. Saarathy, S. Bathrachalam, and B. K. Rajendran, "Self-Healing Test Automation Framework using AI and ML," *International Journal of Strategic Management*, vol. 3, no. 3, pp. 45–77, 2024.  
[23] S. Kavuri, "Self-Healing Test Automation Framework Using Autonomous ML Agents for Real-Time Test Maintenance and Failure Recovery," *International Journal of Intelligent Systems and Applications in Engineering*, vol. 11, no. 4, pp. 1089–1098, 2023.  
[24] W3C, "Accessible Rich Internet Applications (WAI-ARIA) 1.2," W3C Recommendation, 2023.  
[25] Anthropic, "Model Context Protocol (MCP) Specification," Nov. 2024. [Online]. Available: https://modelcontextprotocol.io/  
[26] R. Parasuraman, T. B. Sheridan, and C. D. Wickens, "A model for types and levels of human interaction with automation," *IEEE Transactions on Systems, Man, and Cybernetics - Part A: Systems and Humans*, vol. 30, no. 3, pp. 286–297, 2000.  
[27] OpenAPI Initiative, "OpenAPI Specification v3.1.0," 2021. [Online]. Available: https://spec.openapis.org/oas/v3.1.0  
[28] Chrome DevTools Protocol, "Accessibility domain: getFullAXTree," Chrome DevTools Documentation.  
[29] Selenium Project, "WebDriver BiDi," Selenium Documentation. [Online]. Available: https://www.selenium.dev/documentation/webdriver/bidi/  
[30] L. Huang et al., "A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions," *ACM Computing Surveys*, 2024.  
[31] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou, "Large Language Models Cannot Self-Correct Reasoning Yet," in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2024.  
[32] A. Kluge and A. Stocco, "Web element relocalization in evolving web applications: A comparative analysis and extension study," *Empirical Software Engineering*, vol. 31, no. 6, Art. 175, 2026.  
[33] L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," in *Proc. NeurIPS*, 2023.  
[34] OWASP, "OWASP Top 10 for Large Language Model Applications: LLM01 Prompt Injection," 2023.  
[35] OWASP, "OWASP Top 10 for Large Language Model Applications: LLM06 Sensitive Information Disclosure & LLM08 Excessive Agency," 2023.  
[36] Spring Projects, "Spring PetClinic REST API," GitHub repository. [Online]. Available: https://github.com/spring-petclinic/spring-petclinic-rest  
[37] Spring Projects, "Spring PetClinic Angular Frontend," GitHub repository. [Online]. Available: https://github.com/spring-petclinic/spring-petclinic-angular  
[38] M. Leotta et al., "Using contextual clues to improve web element locators," *Information and Software Technology*, 2020.  
[39] M. Hammoudi, G. Rothermel, and A. Stocco, "WATERFALL: an incremental approach for repairing record-replay tests of web applications," in *Proc. 24th ACM SIGSOFT Int. Symp. Foundations Softw. Eng. (FSE)*, 2016, pp. 751–762.  
[40] A. Stocco, R. Yandrapally, and A. Mesbah, "Visual web test repair," in *Proc. 26th ACM ESEC/FSE*, 2018, pp. 503–514.  
[41] S. Abhichandani, N. R. T. Vadrevu, and V. Bagmar, "AI-Driven Self-Healing in Test Automation: A Review of Autonomous Quality Assurance," in *Proc. 3rd Int. Conf. Inventive Comput. Informat. (ICICI)*, 2025, pp. 1601–1608.  
[42] C. S. Xia, Y. Wei, and L. Zhang, "Automated program repair in the era of large language models," in *Proc. ICSE*, 2023.  
[43] S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," in *Proc. ICLR*, 2023.  
[44] X. Deng et al., "Mind2Web: Towards a Generalist Agent for the Web," in *Proc. NeurIPS*, 2023.  
[45] J. Chen et al., "Unblind Your Apps: Predicting Natural-Language Descriptions for Mobile UI Components," in *Proc. ICSE*, 2020.  
[46] Tufin, "oasdiff: OpenAPI 3.0 and 3.1 diff tool," GitHub repository. [Online]. Available: https://github.com/Tufin/oasdiff  
[47] Pact Foundation, "Pact: Fast, easy and reliable testing for APIs and microservices," [Online]. Available: https://pact.io/  
[48] GitHub, "Managing a branch protection rule," GitHub Docs, 2024. [Online]. Available: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-a-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule  
[49] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," in *Proc. 34th Int. Conf. Mach. Learn. (ICML)*, 2017, pp. 1321–1330.  
[50] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *Journal of the American Statistical Association*, vol. 22, no. 158, pp. 209–212, 1927.  
[51] GitHub, "About billing for GitHub Actions," GitHub Docs, 2024. [Online]. Available: https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions  
