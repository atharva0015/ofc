# KINTSUGI: AN LLM DRIVEN SELF HEALING FRAMEWORK

**Submitted in partial fulfillment of the requirements for the degree of**  
**B.E. Computer Engineering**

**By:**  
- **Atharva Chavan** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Roll No: 11 &nbsp;&nbsp;&nbsp;&nbsp; Exam No: 232015  
- **Prem Sontakke** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Roll No: 43 &nbsp;&nbsp;&nbsp;&nbsp; Exam No: 232165  
- **Aditya Bagad** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Roll No: 45 &nbsp;&nbsp;&nbsp;&nbsp; Exam No: 232006  
- **Sophia Dsilva** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Roll No: 52 &nbsp;&nbsp;&nbsp;&nbsp; Exam No: 232035  

**Guide:** Ms. Prapti Sawant  
**Designation:** Assistant Professor  

<br>

**Department of Computer Engineering**  
**St. Francis Institute of Technology (Engineering College)**  
*(An Autonomous Institute, Affiliated to University of Mumbai)*  
**2026–2027**

---

## CERTIFICATE

This is to certify that the project entitled **“KINTSUGI: AN LLM DRIVEN SELF HEALING FRAMEWORK”** is a bonafide work of **Atharva Chavan (11)**, **Prem Sontakke (43)**, **Aditya Bagad (45)**, and **Sophia Dsilva (52)** submitted to the University of Mumbai in partial fulfillment of the requirement for the award of the degree of **B.E. in Computer Engineering**.

<br><br>

---------------------------------------------  
**(Ms. Prapti Sawant)**  
**Guide**  

<br>

--------------------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ---------------------------------------------  
**(Dr. Dakshata Panchal)** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **(Dr. Deepak Jayaswal)**  
**Head of Department** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Principal**  

---

## Project Approval Report for B.E.

This project report entitled **“KINTSUGI: AN LLM DRIVEN SELF HEALING FRAMEWORK”** by **Atharva Chavan (11)**, **Prem Sontakke (43)**, **Aditya Bagad (45)**, and **Sophia Dsilva (52)** is approved for the degree of **B.E. in Computer Engineering**.

<br>

**Examiners:**  
1. ----------------------------------------------------------------------  
2. ----------------------------------------------------------------------  

**Date:**  
**Place:** Mumbai  

---

## Declaration

We declare that this written submission represents our ideas in our own words and where others' ideas or words have been included, we have adequately cited and referenced the original sources. We also declare that we have adhered to all principles of academic honesty and integrity and have not misrepresented or fabricated or falsified any idea/data/fact/source in our submission. We understand that any violation of the above will be cause for disciplinary action by the Institute and can also evoke penal action from the sources which have thus not been properly cited or from whom proper permission has not been taken when needed.

- **Atharva Chavan (11)**  
- **Prem Sontakke (43)**  
- **Aditya Bagad (45)**  
- **Sophia Dsilva (52)**  

**Date:**  

---

## Abstract

Automated web UI tests often fail after harmless changes to a page, even when the feature under test still works. Empirical studies attribute most such breakages to locators, the expressions a test uses to find page elements, and repairing them by hand slows down releases. Existing self-healing tools repair broken locators automatically, but a repair accepted without checking the test’s intent can hide a genuine defect.

This project proposes **Kintsugi**, an AI-assisted self-healing framework for Selenium-based web UI tests in which every repair is independently validated and every code change is approved by a human. When a locator fails, the framework classifies the failure, collects the DOM, accessibility tree and screenshot with sensitive data masked, and generates candidate locators: first with a deterministic similarity matcher and, only when confidence is low, with a large language model (LLM). A candidate must match exactly one interactable element with a compatible role and accessible name, and a sandbox replay must pass the test’s own assertions. An LLM critic may veto a candidate but cannot approve one. A calibrated, confidence-gated policy then heals at run time, only suggests a repair, or fails the test as a probable defect. Repairs are proposed as pull requests; merging is always done by a human, and assertions, expected values and test data are never changed.

This report covers **Major Project Part 1 (Semester VII)**: literature survey, requirements, architecture, algorithms, autonomy, security, risk and cost analysis, and a reproducible evaluation plan on the open-source Spring PetClinic application with injected locator drift, genuine regressions and API schema changes. Implementation and experiments are planned for Semester VIII; no experimental results are reported here.

**Keywords:** *Self-healing test automation, web UI testing, Selenium, locator repair, large language models, human-in-the-loop, software quality assurance*

---

## Contents

### Chapter 1: Introduction ................................................................................................... 14
- **1.1 Introduction** ................................................................................................................. 14
- **1.2 Background Study** ....................................................................................................... 15
  - 1.2.1 From manual testing to automated UI testing ........................................................... 15
  - 1.2.2 Selenium and locator-based testing ........................................................................... 15
  - 1.2.3 Flaky tests .................................................................................................................. 16
  - 1.2.4 Test maintenance as a persistent problem ................................................................. 16
  - 1.2.5 Self-healing and AI-assisted testing .......................................................................... 16
- **1.3 Terminologies and Definitions of New Terms** ............................................................ 17
- **1.4 Fundamental Concepts of the Selected Topic and Domain** ......................................... 18
  - 1.4.1 How a UI test finds an element ................................................................................. 18
  - 1.4.2 DOM versus accessibility tree ................................................................................... 18
  - 1.4.3 Element re-identification by similarity ...................................................................... 18
  - 1.4.4 Large language models and agents ............................................................................ 19
  - 1.4.5 Tool integration through MCP .................................................................................. 19
  - 1.4.6 Levels of automation and human oversight ............................................................... 19
- **1.5 Identification of Challenges in the Selected Topic** ...................................................... 19
- **1.6 Motivation** ................................................................................................................... 20
- **1.7 Problem Statement** ....................................................................................................... 20
- **1.8 Proposed Solution** ........................................................................................................ 21

### Chapter 2: Literature Survey .............................................................................................. 23
- **2.1 Survey of Existing Systems** ......................................................................................... 23
- **2.2 Review of Relevant Research Papers** .......................................................................... 24
- **2.3 Existing Tools and Frameworks** .................................................................................. 29
  - 2.3.1 Selenium WebDriver ................................................................................................. 29
  - 2.3.2 Playwright ................................................................................................................. 29
  - 2.3.3 Cypress ..................................................................................................................... 29
  - 2.3.4 Healenium ................................................................................................................. 30
  - 2.3.5 Other components used by the proposed system ....................................................... 30
- **2.4 Comparative Analysis** ................................................................................................. 30
- **2.5 Limitations of Existing Systems** .................................................................................. 32
- **2.6 Identified Research Gaps** ............................................................................................. 33
- **2.7 Scope of the Proposed System** .................................................................................... 34

### Chapter 3: Proposed System ............................................................................................... 35
- **3.1 Detailed Explanation of Proposed System** .................................................................. 35
  - 3.1.1 Design principles ....................................................................................................... 35
  - 3.1.2 Modules ..................................................................................................................... 35
  - 3.1.3 Autonomy model and human-in-the-loop policy ...................................................... 37
  - 3.1.4 Safeguards against critical technical risks ................................................................. 38
- **3.2 Block Diagram and System Workflow** ........................................................................ 41
- **3.3 Working Principles and Algorithms** ............................................................................ 44
- **3.4 Phase/Module-wise Explanation** ................................................................................. 45
- **3.5 System Analysis** .......................................................................................................... 47
  - 3.5.1 Functional requirements ............................................................................................ 47
  - 3.5.2 Non-functional requirements .................................................................................... 48
  - 3.5.3 Specific requirements ............................................................................................... 49
  - 3.5.4 Software requirements .............................................................................................. 49
  - 3.5.5 Hardware requirements ............................................................................................. 50
- **3.6 Use Case Modelling** .................................................................................................... 50
- **3.7 Proposed System: Analysis, Modelling and Design** .................................................... 52
  - 3.7.1 Activity diagram ........................................................................................................ 52
  - 3.7.2 Statechart diagram .................................................................................................... 52
  - 3.7.3 Class diagram ........................................................................................................... 53
  - 3.7.4 Sequence diagram ..................................................................................................... 54
  - 3.7.5 Component diagram ................................................................................................. 55
  - 3.7.6 Deployment diagram ................................................................................................ 56
  - 3.7.7 ER diagram and sample schema ............................................................................... 56
- **3.8 Data Flow Diagrams** .................................................................................................... 58
- **3.9 Architectural View** ...................................................................................................... 61
  - 3.9.1 Security and privacy architecture ............................................................................. 62
- **3.10 Algorithms and Methodology** .................................................................................... 63
  - 3.10.1 Similarity model ..................................................................................................... 63
  - 3.10.2 Hard gates and confidence ...................................................................................... 64
  - 3.10.3 Threshold calibration .............................................................................................. 65
  - 3.10.4 Latency model ........................................................................................................ 65
  - 3.10.5 Algorithms .............................................................................................................. 66
- **3.11 UI/UX Design** ............................................................................................................ 68

---

## List of Figures

- **Figure 1.1:** Overview of the proposed VeriHeal workflow ................................................... 21
- **Figure 3.1:** Block diagram of the proposed system ............................................................... 42
- **Figure 3.2:** End-to-end healing workflow with decision points and human approval ............ 43
- **Figure 3.3:** Planned Semester VIII roadmap with go/no-go gates (relative weeks) ................ 45
- **Figure 3.4:** Use case diagram of the proposed system ........................................................... 50
- **Figure 3.5:** Activity diagram of candidate validation and healing decision ............................ 52
- **Figure 3.6:** Statechart diagram of a heal request .................................................................... 53
- **Figure 3.7:** Class diagram of the core framework ................................................................. 54
- **Figure 3.8:** Sequence diagram of a run-time heal and repair PR ............................................ 55
- **Figure 3.9:** Component diagram ........................................................................................... 55
- **Figure 3.10:** Deployment diagram ......................................................................................... 56
- **Figure 3.11:** Entity–relationship diagram ............................................................................. 57
- **Figure 3.12:** DFD Level 0 (context diagram) ....................................................................... 58
- **Figure 3.13:** DFD Level 1 .................................................................................................... 58
- **Figure 3.14:** DFD Level 2: process 4.0 Generate and Validate Candidates ........................... 59
- **Figure 3.15:** DFD Level 2: process 6.0 Create Repair Pull Request ...................................... 60
- **Figure 3.16:** Layered architectural view ............................................................................... 61
- **Figure 3.17:** Design mock-up: dashboard with test execution monitor and execution history . 68
- **Figure 3.18:** Design mock-up: failure report, healing suggestion, confidence and approval interface ................................................................................................................................ 69
- **Figure 3.19:** Design mock-up: audit log ............................................................................... 69

---

## List of Tables

- **Table 1.1:** Terminology used in this report .......................................................................... 17
- **Table 2.1:** Paper review: Hammoudi et al. (ICST 2016) [3] ................................................. 24
- **Table 2.2:** Paper review: Leotta et al., ROBULA+ (JSEP 2016) [9] ..................................... 24
- **Table 2.3:** Paper review: Choudhary et al., WATER (ETSE 2011) [17] ............................. 25
- **Table 2.4:** Paper review: Hammoudi et al., WATERFALL (FSE 2016) [39] ....................... 25
- **Table 2.5:** Paper review: Stocco et al., VISTA (ESEC/FSE 2018) [40] .............................. 25
- **Table 2.6:** Paper review: Nass et al., Similo (TOSEM 2023) [18] ....................................... 26
- **Table 2.7:** Paper review: Nass et al., VON Similo (ICST 2023) [19] .................................. 26
- **Table 2.8:** Paper review: Nass et al., LLM-assisted localisation (STVR 2024) [6] ............. 26
- **Table 2.9:** Paper review: Kluge and Stocco (EMSE 2026) [32] ........................................... 27
- **Table 2.10:** Paper review: Romano et al. (ICSE 2021) [14] ................................................. 27
- **Table 2.11:** Paper review: Saarathy et al. (IJSM 2024) [22] ................................................ 27
- **Table 2.12:** Paper review: Kavuri (IJISAE 2023) [23] ......................................................... 28
- **Table 2.13:** Paper review: Abhichandani et al. (ICICI 2025) [41] ........................................ 28
- **Table 2.14:** Paper review: Huang et al. (ICLR 2024) [31] ................................................... 28
- **Table 2.15:** Capability comparison of existing tools and the proposed system .................... 31
- **Table 2.16:** Comparison of research approaches to broken web tests ................................. 31
- **Table 2.17:** Quantitative claims found in self-healing sources and how this report treats them .................................................................................................................................................. 33
- **Table 2.18:** Research gaps and how the proposed system addresses them .......................... 33
- **Table 2.19:** Scope of the proposed system ........................................................................... 34
- **Table 3.1:** Modules of the proposed system ......................................................................... 36
- **Table 3.2:** Project-defined autonomy levels A0–A4 ............................................................ 37
- **Table 3.3:** Human-in-the-loop policy ................................................................................... 37
- **Table 3.4:** Distinguishing locator drift from genuine regressions ......................................... 38
- **Table 3.5:** Phase-wise implementation plan ......................................................................... 46
- **Table 3.6:** Go/no-go gates (proposed targets, fixed before each phase) ............................... 46
- **Table 3.7:** Functional requirements ...................................................................................... 47
- **Table 3.8:** Non-functional requirements ............................................................................... 48
- **Table 3.9:** Software requirements (planned) ........................................................................ 49
- **Table 3.10:** Hardware requirements (estimates) .................................................................. 50
- **Table 3.11:** Use case UC-01: Heal broken locator ............................................................... 51
- **Table 3.12:** Use case UC-02: Review and approve or reject a repair PR ............................ 51
- **Table 3.13:** Use case UC-03: Classify API contract failure (extension E2) ......................... 51
- **Table 3.14:** DFD elements .................................................................................................... 60
- **Table 3.15:** Security and privacy controls ........................................................................... 62
- **Table 3.16:** Fingerprint attributes, similarity functions and initial weights ......................... 64

---

<!-- Page 14 -->

# Chapter 1: Introduction 
## 1.1 Introduction 
Modern web applications change continuously. Teams release new versions every few days or 
even several times a day, and every release must be checked so that existing features keep 
working. Automated regression tests that drive the application through its user interface (UI), 
in the same way as a real user, are a common way to do this. Selenium WebDriver is one of the 
most widely used tools for writing such tests; its browser -automation protocol has been 
standardised by the W3C as WebDriver [1]. 
A UI test is a script: it opens a page, finds elements such as text boxes and buttons, performs 
actions on them and then checks (asserts) that the application responded correctly. To find an 
element, the script uses a locator, for example an element id, a CSS selector or an XPath 
expression [2]. Locators depend on the internal structure of the page. When developers rename 
an id, add a wrapper element or change a CSS class, the locator may stop matching, and the 
test fails even though the feature still works for the user. An empirical study of record/replay 
web tests across 453 versions of eight web applications found that locato rs caused more than 
73% of the 1,065 test breakages observed [3]. 
Such false failures have two costs. First, engineers spend time diagnosing and repairing tests 
instead of building features. Second, frequent false alarms reduce trust in the test suite, so real 
failures may be ignored. Self-healing test automation  tries to reduce this cost by detecting a 
broken locator during the test run and replacing it with one that finds the intended element. 
Open-source tools such as Healenium already do this for Selenium  [4], [5], mainstream 
frameworks have started to offer L LM-based healing [?playwright_agents], [?cypress_aigen], 
and recent research uses large language models (LLMs) to choose among candidate 
elements [6]. 
Automatic repair, however, introduces a new risk. If a button was removed by mistake, a tool 
that "heals" the test by clicking some other similar-looking element turns a correctly failing test 
into a passing one, and the defect reaches users. This project therefore treats self-healing as a 
validation problem as much as a search problem. The proposed framework, VeriHeal, repairs

<!-- Page 15 -->

only locators, accepts a repair only after independent execution-based checks, and leaves every 
change to the test code to a human reviewer. 
This chapter introduces the background (Section  1.2), defines the terms used in the report 
(Section 1.3), explains the fundamental concepts of the domain (Section  1.4), identifies the 
main challenges (Section  1.5), and presents the motivation, problem stat ement and proposed 
solution (Sections 1.6-1.8). 
## 1.2 Background Study 
### 1.2.1 From manual testing to automated UI testing 
In manual testing a tester follows written test cases, clicks through the application and compares 
what happens with the expected result. Manual testing is flexible and good at finding 
unexpected problems, but it is slow, it is hard to repeat identically, and its cost grows with every 
release. Automated testing replaces the repetitive part with scripts. Unit and integration tests 
run quickly and are relatively stable; end-to-end UI tests exercise the whole system through the 
browser and therefore catch integration problems that lower-level tests miss, but they are slower 
and more fragile. Deciding when and what to automate is itself a trade -off; a multi -vocal 
literature review by Garousi and Mäntylä consolidates the factors behind this decision into a 
checklist for practitioners [7]. 
### 1.2.2 Selenium and locator-based testing 
Selenium WebDriver controls a real browser through a driver program. A test finds elements 
using one of eight traditional locator strategies (class name, CSS selector, id, name, link text, 
partial link text, tag name and XPath)  [2]. Two broad families exis t: attribute-based locators 
(for example id or name) and structure-based locators (for example an XPath that follows the 
path from the page root). Both families break when the page changes in the corresponding way. 
Early research compared capture-replay and programmable web tests during the evolution of 
applications [8], and later work proposed algorithms that generate more robust XPath locators. 
ROBULA+, for example, reduced the number of broken locators on eight PHP applications 
compared with several existing locator generators  [9]. Newer frameworks also give guidance: 
Playwright recommends locating elements by user -facing attributes such as their ARIA 
role [10], and Cypress recommends dedicated data-* attributes that are isolated from CSS and

<!-- Page 16 -->

JavaScript changes [11]. These practices reduce fragility but do not remove it, especially in 
large existing test suites. 
### 1.2.3 Flaky tests 
A flaky test passes and fails on the same code without any change. Luo et al. studied 201 
commits that fixed flaky tests in 51 open -source projects; of the 161 commits they could 
classify, asynchronous waiting (45%), concurrency (20%) and test -order dependency (1 2%) 
were the most common root causes  [12]. A survey by Parry et al. reviews 76 papers on the 
causes, costs, detection and repair of flaky tests [13]. Romano et al. analysed 235 flaky UI tests 
from 62 web and Android projects and argue that UI tests deserve separate study because their 
inputs and running conditions are more varied than those of unit tests  [14]. Flakiness matters 
for self-healing because a timing failure can look like a missing element; a healing tool must 
not "repair" a locator that was never broken. 
### 1.2.4 Test maintenance as a persistent problem 
A systematic literature review by Nass, Alégroth and Feldt synthesised 24 challenges of GUI -
based test automation from 49 publications with empirical evidence from practice, and found 
that four of them have existed for almost two decades  [15]. Repair of GU I and web tests has 
been researched for a long time: Memon proposed automatic repair of event -sequence-based 
GUI test suites  [16], and WATER suggested repairs for broken web tests by comparing the 
behaviour of a test on two consecutive versions of an application [17]. 
### 1.2.5 Self-healing and AI-assisted testing 
Self-healing tools store information about each element while tests pass and use it to find the 
element again when its locator breaks. Healenium, for instance, saves successful locators as a 
baseline, catches the NoSuchElement exception, compares the current page with the stored data 
to produce a ranked list of healed locators, continues the test with the highest -scoring one and 
produces a report with screenshots  [5]. Research prototypes such as Similo and VON Similo 
score many element properties at once to re-identify elements across application versions [18], 
[19], and an LLM has been used to choose among the top candidates produced by such a 
method [6]. More broadly, surveys show rapid growth in the use of LLMs for software t esting 
and software engineering tasks [20], [21]. Some recent articles on AI-based self-healing report 
large reductions in maintenance effort  [22], [23]; as Chapter  2 explains, these figures come

<!-- Page 17 -->

from a single case study or from abstracts without a disclosed measurement protocol, so this 
report does not adopt them as expected outcomes. 
## 1.3 Terminologies and Definitions of New Terms 
Table 1.1 defines the terms used throughout the report. Terms marked "project -defined" are 
introduced by this report and are not industry standards. 
Table 1.1: Terminology used in this report 
Term Definition 
Locator An expression (id, CSS selector, XPath, role and name, etc.) that a test uses to find 
an element on a web page [2]. 
DOM Document Object Model: the tree of elements that the browser builds from a page 
and that locators are evaluated against. 
Accessibility tree A tree of accessible objects that represents the structure of the user interface; each 
node represents a UI element exposed through an accessibility API [24]. 
Role and accessible 
name 
The semantic type of an element (for example button, textbox) and the name that 
assistive technologies read for it [24]. 
Locator drift A change in the page that breaks a locator while the intended element still exists 
with the same purpose and behaviour (for example a renamed id). 
Genuine regression A change in which the intended element or its behaviour is actually missing or 
wrong. A test should fail. 
Flaky test A test that passes and fails on the same code without changes [13]. 
Self-healing Automatic detection of a broken locator and its replacement during or after a test 
run. 
Element fingerprint (Project-defined) the set of attributes, structural position, role, accessible name, 
text and bounding box recorded for an element during a passing run. 
Candidate locator A proposed replacement locator produced by the Similarity Matcher or the LLM 
Generator. 
Hard gate (Project-defined) a check that a candidate must pass to be eligible for healing (H1-
H5 in Chapter 3). 
Heal / false heal A heal replaces a broken locator. A false heal is a heal that targets the wrong 
element or makes a test pass on a genuine regression. 
PASSED-HEALED (Project-defined) the status of a test that passed only because a validated heal was 
applied at run time. It is reported separately from PASSED. 
Generator-Critic An arrangement in which one LLM agent proposes outputs and another reviews 
them. In this project the Critic is advisory only. 
LLM agent A program that uses a large language model to decide on actions, typically by 
calling tools. 
MCP Model Context Protocol: an open protocol, based on JSON-RPC 2.0, through 
which LLM applications (hosts) connect to servers that expose resources, prompts 
and tools [25]. MCP is an interface standard; it does not itself analyse or modify 
code. 
Autonomy level (Project-defined, A0-A4) how much of the repair process the system performs 
without a human decision. Based on the idea of levels of automation from human -
factors research [26]. 
OpenAPI A standard, language-agnostic description of HTTP APIs [27], used here to detect 
API schema changes.

<!-- Page 18 -->

Term Definition 
Pull request (PR) A proposed change to a repository that is reviewed before it is merged. 
CI/CD Continuous integration and delivery: automatic building and testing of every 
change. 
## 1.4 Fundamental Concepts of the Selected Topic and Domain 
### 1.4.1 How a UI test finds an element 
The test calls the WebDriver protocol  [1] to send a "find element" command with a strategy 
and a value. The browser evaluates the locator against the current DOM. If no element matches, 
Selenium raises NoSuchElementException; if several elements match, find_element silently 
returns the first one, which may be the wrong element. A self-healing framework must therefore 
handle both "not found" and "ambiguous" cases. 
### 1.4.2 DOM versus accessibility tree 
The DOM contains every element, including purely presentational wrappers. The accessibility 
tree is a simplified, semantic view: it exposes roles, names and states of the elements that matter 
to a user [24]. Two pages that differ greatly in their DOM can h ave very similar accessibility 
trees, which is why role and accessible name are useful, stable signals for re -identifying an 
element. In Chromium -based browsers the full accessibility tree can be read through the 
Chrome DevTools Protocol (CDP) method Accessibility.getFullAXTree [28]. Selenium 
supports sending CDP commands to Chrome and Edge, but its documentation states that CDP 
support is temporary until WebDriver BiDi is implemented  [29]; the design in Chapter  3 
accounts for this. 
### 1.4.3 Element re-identification by similarity 
When a locator breaks, the old element can often be found again by comparing many of its 
properties with those of every element on the new page. Similo computes a weighted similarity 
over several locator attributes and, on 801 element pairs from 48 website s, failed in 11% of 
cases compared with 27% for its baseline, with an average localisation time of 4 ms [18]. Such 
methods are fast and explainable, but they can choose a wrong element when several elements 
look alike.

<!-- Page 19 -->

### 1.4.4 Large language models and agents 
LLMs are trained on large text and code corpora and can read HTML, reason about the purpose 
of an element and propose locators. They can also be used as agents that call tools, for example 
to query a page or run a test. LLM output is not guaranteed to be correct: models can produce 
fluent but wrong content (hallucination)  [30], and an LLM asked to check its own reasoning 
without external feedback often fails to improve and sometimes gets worse [31]. These findings 
are central to the design choice in this project that LLM output is always checked by execution, 
not by another LLM alone. 
### 1.4.5 Tool integration through MCP 
MCP standardises how an LLM application connects to external tools and data. Servers expose 
resources, prompts and tools; the protocol uses JSON -RPC 2.0, and its specification requires 
user consent and treats tools as arbitrary code execution that must be handled with caution [25]. 
In VeriHeal, MCP is an optional interface through which agents may call well -defined tools 
(query DOM, run a test step, read a file). The actual code change is produced by a dedicated 
Repair & PR Agent with restricted repository permissions. 
### 1.4.6 Levels of automation and human oversight 
Parasuraman, Sheridan and Wickens describe automation along stages (information acquisition, 
analysis, decision selection and action implementation) and levels, from fully manual to fully 
automatic [26]. This view is useful here because different stages of  test repair carry different 
risks. Diagnosing a failure automatically is low -risk; changing the test code without review is 
high-risk. VeriHeal  therefore automates the analysis stages fully and keeps the final action 
(merging a change) with a human. 
## 1.5 Identification of Challenges in the Selected Topic 
1. Locator fragility.  Locators break under routine changes to ids, classes and page 
structure [3]. 
2. Drift versus genuine regression.  A missing element may be locator drift or a real 
defect. Healing a real defect hides it. 
3. Flakiness as a confounder. Timing problems produce the same exception as a broken 
locator [12], [14].

<!-- Page 20 -->

4. Ambiguous candidates.  Similar elements (for example two "Save" buttons) can 
mislead similarity-based matching; a replication study reported that VON Similo tends 
to produce more false positives than Similo [32]. 
5. Reliability of AI output. LLM proposals can be wrong [30], and an LLM critic is not 
a reliable judge of its own or another model's reasoning without external feedback [31], 
[33]. 
6. Privacy and security.  DOM snapshots and screenshots may contain personal data or 
secrets, and page content is untrusted input that can carry prompt -injection text [34], 
[35]. 
7. Safe code modification.  Automatic changes to the repository must be minimal, 
reviewable and reversible, with least-privilege access. 
8. Cost and latency.  LLM calls and test replays add time and money, which must fit 
within CI time limits. 
9. Measurable benefit. Claimed maintenance savings in the literature are often reported 
without baselines or protocols, so the benefit must be measured on a reproducible 
benchmark. 
## 1.6 Motivation 
Locator maintenance is a well-documented, long-standing cost of UI test automation [3], [15]. 
Research has produced strong techniques for re -identifying elements  [18], [19], [6], and 
practical tools exist  [4], [?playwright_agents], [?cypress_aigen]. What i s less developed is a 
safety-first combination of these techniques: a framework that (i) heals only when there is 
independent execution-based evidence that the test's intent is preserved, (ii) explicitly separates 
locator drift from genuine regressions, (iii) treats LLMs as proposal genera tors rather than as 
judges, (iv) protects sensitive data, and (v) integrates repairs into the normal code -review 
workflow. This combination is technically challenging, directly useful to development teams, 
and well suited to a final -year project because each part can be built, measured and improved 
in stages. 
## 1.7 Problem Statement 
Automated web UI tests break when developers change the structure or attributes of a page, 
even when the feature under test still works. Repairing these locators by hand is repetitive and

<!-- Page 21 -->

costly. Existing self -healing approaches can find a replacement element automatically. 
However, a replacement that is accepted without checking the test's intent can make a test pass 
on a genuine defect. 
The problem addressed by this project is: 
To design and evaluate a framework that automatically detects, diagnoses and 
repairs broken locators in Selenium-based web UI tests, such that (a) every repair is 
validated by independent, execution -based evidence, (b) genuine regressions are 
reported as failures rather than healed, (c) no assertion, expected value or test data 
is ever changed automatically, and (d) every change to the test code is approved by 
a human. 
## 1.8 Proposed Solution 
The proposed solution, VeriHeal, is a plug -in framework for Selenium and pytest. Figure  1.1 
shows its seven-step workflow; Chapter 3 describes each module in detail. 
 
Figure 1.1: Overview of the proposed VeriHeal workflow 
The main elements of the solution are: 
1. Failure classification. Each failure is classified first. Only locator failures (element not 
found, or ambiguous match) enter the healing pipeline; timing, assertion, HTTP and 
environment failures are reported normally. 
2. Context collection with redaction.  The DOM, accessibility tree and screenshot are 
captured, and personal data and secrets are masked before any data leaves the test 
environment.

<!-- Page 22 -->

3. Deterministic first, LLM second. A similarity matcher compares page elements with 
the element fingerprint recorded in the last passing run. An LLM Generator is used only 
when this matcher is not confident. 
4. Independent validation. A candidate must resolve to exactly one interactable element 
with a compatible role and accessible name, and a sandbox replay of the test must pass 
the test's own assertions. An LLM Critic may veto a candidate but cannot approve one. 
5. Confidence-gated decisions.  A decision engine heals at run time (marking the test 
PASSED-HEALED), only suggests a repair, or fails the test as a probable defect. 
6. Reviewed repairs. A Repair & PR Agent creates a minimal patch on a separate branch, 
re-runs the affected tests and opens a pull request with evidence. Only a human can 
merge it. 
7. Measured evaluation. The framework will be evaluated on Spring PetClinic [36], [37] 
with injected locator drift, genuine regressions and API schema changes, against 
Selenium without healing and against Healenium. 
Objectives of Major Project Part 1 (Semester VII).  (1) Survey existing research and tools; 
(2) define the problem, scope and autonomy policy; (3) specify requirements; (4) design the 
architecture, algorithms and data model; (5) design the benchmark, metrics and go/no-go gates; 
(6) analyse risks, cost and security. Implementation and experiments are planned for Semester 
VIII (Section 3.4).

<!-- Page 23 -->

# Chapter 2: Literature Survey 
This chapter surveys existing systems through research papers and real tools. Section 2.1 groups 
the existing approaches; Section  2.2 reviews the most relevant papers in a common format; 
Section 2.3 describes the tools and frameworks; Section 2.4 compares them; and Sections 2.5-
2.7 derive the limitations, research gaps and the scope of the proposed system. 
Survey method. Papers were identified through targeted searches on the topics of web test 
breakage, locator robustness, web test repair, flaky UI tests, LLM -based software testing and 
LLM reliability. Bibliographic details of every reference (authors, venue, year, pages , DOI) 
were checked against Crossref records, publisher pages or official proceedings before inclusion. 
Findings are reported only as stated in the paper's abstract or main text. Where a paper reports 
a number without a disclosed measurement protocol, this is stated explicitly. 
## 2.1 Survey of Existing Systems 
Existing work that addresses broken UI tests falls into five groups. 
1. Empirical studies of why tests break.  These studies quantify the causes of breakage. 
Hammoudi et al. built a taxonomy of record/replay test breakages from 1,065 breakages 
and found locators to be the dominant cause  [3]. Studies of flaky tests explain non -
deterministic failures [12], [13], [14]. 
2. Robust locator generation (prevention). These approaches generate locators that are 
less likely to break, for example ROBULA+ for XPath  [9], and the use of contextual 
clues to identify elements [38]. 
3. Test repair (correction after breakage).  These approaches repair a test after the 
application changes. WATER uses differential testing between two versions  [17]; 
WATERFALL applies repair incrementally across fine -grained versions [39]; VISTA 
uses visual information captured during execution  [40]. Earlier work repaired event -
sequence-based GUI test suites [16]. 
4. Element re -identification by similarity.  Similo [18], VON Similo  [19], an LLM -
assisted variant [6] and a recent replication and extension study [32] locate the intended 
element in a new version of the page by comparing many properties.

<!-- Page 24 -->

5. AI-based self-healing frameworks and tools.  Healenium is an open -source runtime 
self-healing library for Selenium  [4], [5]; Playwright's healer agent and Cypress's 
cy.prompt add LLM -based healing to mainstream frameworks  [?playwright_agents], 
[?cypress_aigen]. Several recent articles describe AI/ML -based self -healing 
frameworks [22], [23] or review the area [41]. 
Related work on LLMs is also relevant, because VeriHeal uses LLMs as generators and critics: 
surveys of LLMs in software testing and software engineering [20], [21], LLM-based program 
repair [42], LLM agents that operate software tools  [43], multimodal web  agents [44], and 
studies of LLM reliability [30], [31], [33]. For visual element detection, Chen et al. compared 
traditional image processing and deep-learning detectors for GUI elements [45]. 
## 2.2 Review of Relevant Research Papers 
Tables 2.1-2.14 summarise fourteen papers in a common format. "Limitations" marked (our 
assessment) are the authors' of this report, not limitations stated in the paper. 
Table 2.1: Paper review: Hammoudi et al. (ICST 2016) [3] 
Parameter Details 
Paper title Why do Record/Replay Tests of Web Applications Break? 
Authors M. Hammoudi, G. Rothermel, P. Tonella 
Year; venue 2016; IEEE Int. Conf. on Software Testing, Verification and Validation (ICST), pp. 
180-190 
Methodology Selenium IDE test suites were created for 300 versions of five open-source web 
applications and repaired whenever they broke; the resulting taxonomy was validated 
on 153 versions of three further applications. 
Key findings 1,065 breakages were analysed (722 + 343). Locator-related causes accounted for more 
than 73% of breakages; attribute-based locators were involved in the majority of 
locator breakages. 
Limitations Eight applications; Selenium IDE (record/replay) only; one author wrote the tests 
(threats discussed in the associated thesis). 
Project relevance Provides the empirical motivation that locators are the dominant cause of web test 
breakage, and a taxonomy used to design the mutation operators in Chapter  4. 
Table 2.2: Paper review: Leotta et al., ROBULA+ (JSEP 2016) [9] 
Parameter Details 
Paper title ROBULA+: An algorithm for generating robust XPath locators for web testing 
Authors M. Leotta, A. Stocco, F. Ricca, P. Tonella 
Year; venue 2016; Journal of Software: Evolution and Process, vol. 28, no. 3, pp. 177-204 
Methodology Starts from the most general XPath //* and specialises it with transformations 
(attribute prioritisation, attribute black-listing, text and multi-attribute predicates) until 
it uniquely selects the target. Evaluated on 1,110 elements from eight PHP applications, 
each with two releases.

<!-- Page 25 -->

Parameter Details 
Key findings ROBULA+ broke on 91 of 1,110 locators (8%), compared with 78% for absolute 
FirePath XPaths and 22% for Selenium IDE locators. 
Limitations Prevention only (does not repair); XPath only; manually defined attribute priorities; 
exponential worst-case complexity (stated by the authors). 
Project relevance Shows that attribute choice strongly affects robustness; the attribute priorities inform 
the weights of the Similarity Matcher (M5a) and the locator form produced by the 
Repair Agent. 
Table 2.3: Paper review: Choudhary et al., WATER (ETSE 2011) [17] 
Parameter Details 
Paper title WATER: Web Application TEst Repair 
Authors S. R. Choudhary, D. Zhao, H. Versee, A. Orso 
Year; venue 2011; Proc. 1st Int. Workshop on End-to-End Test Script Engineering (ETSE), pp. 24-
29 
Methodology Differential testing: runs the test on the version where it passes and the version where it 
fails, analyses the differences between the two executions and suggests repairs. 
Key findings The authors report that WATER suggested meaningful repairs on real web applications, 
many of which matched the changes developers later made. 
Limitations Requires the old version to be executable; repairs are suggestions; small workshop -
scale evaluation (our assessment). 
Project relevance Early evidence that breakages can be repaired automatically and that repairs should be 
presented as suggestions for a developer. 
Table 2.4: Paper review: Hammoudi et al., WATERFALL (FSE 2016) [39] 
Parameter Details 
Paper title WATERFALL: an incremental approach for repairing record-replay tests of web 
applications 
Authors M. Hammoudi, G. Rothermel, A. Stocco 
Year; venue 2016; Proc. 24th ACM SIGSOFT Int. Symp. on Foundations of Software Engineering 
(FSE), pp. 751-762 
Methodology Applies a repair technique incrementally across fine-grained intermediate versions (for 
example commits) instead of only between two releases. 
Key findings On seven web applications, WATERFALL repaired 4,420 of 4,948 locator breakages 
(89.3%) compared with 1,431 (28.9%) for the coarse-grained approach. 
Limitations Needs access to many intermediate versions; targets record/replay tests (our 
assessment). 
Project relevance Supports repairing tests close to the change that broke them; VeriHeal runs in CI on 
every commit for the same reason. 
Table 2.5: Paper review: Stocco et al., VISTA (ESEC/FSE 2018) [40] 
Parameter Details 
Paper title Visual web test repair 
Authors A. Stocco, R. Yandrapally, A. Mesbah 
Year; venue 2018; Proc. 26th ACM ESEC/FSE, pp. 503-514 
Methodology Captures visual information during test execution, analyses it with an image -processing 
pipeline to detect breakages and propose fixes, and uses local crawling to repair broken 
workflows.

<!-- Page 26 -->

Parameter Details 
Key findings On 2,672 test cases across 86 releases of four web applications, VISTA repaired about 
81% of breakages, a 41% improvement over existing techniques. 
Limitations Visual matching depends on rendering stability; four subject applications (our 
assessment). 
Project relevance Justifies an optional visual signal (extension E1) for cases where DOM -based matching 
fails. 
Table 2.6: Paper review: Nass et al., Similo (TOSEM 2023) [18] 
Parameter Details 
Paper title Similarity-based Web Element Localization for Robust Test Automation 
Authors M. Nass, E. Alégroth, R. Feldt, M. Leotta, F. Ricca 
Year; venue 2023; ACM Transactions on Software Engineering and Methodology, vol. 32, no. 3, 
pp. 1-30 
Methodology Scores the similarity between the target element and every candidate element using a 
weighted combination of multiple locator attributes, and selects the most similar 
element. 
Key findings On 801 element pairs from 48 popular websites, Similo failed in 91 cases (11%) versus 
214 (27%) for the baseline; average localisation time was 4 ms. 
Limitations About one in nine elements is still mislocated; selection is by best score without 
checking the test's intent (our assessment). 
Project relevance Direct basis of the deterministic Similarity Matcher (M5a). 
Table 2.7: Paper review: Nass et al., VON Similo (ICST 2023) [19] 
Parameter Details 
Paper title Robust web element identification for evolving applications by considering visual 
overlaps 
Authors M. Nass, E. Alégroth, R. Feldt, R. Coppola 
Year; venue 2023; IEEE Conf. on Software Testing, Verification and Validation (ICST), pp. 258-
268 
Methodology Extends Similo with "visually overlapping nodes": one visible element is often built 
from several overlapping DOM nodes, so candidates are grouped by visual overlap. 
Key findings On 1,163 manually collected element pairs from 40 web applications, accuracy was 
94.7% for VON Similo versus 83.8% for Similo. 
Limitations A later replication found that VON Similo tends to produce more false positives than 
Similo [32]. 
Project relevance Shows the value of bounding-box information in the fingerprint and the need to guard 
against false positives. 
Table 2.8: Paper review: Nass et al., LLM-assisted localisation (STVR 2024) [6] 
Parameter Details 
Paper title Improving web element localization by using a large language model 
Authors M. Nass, E. Alégroth, R. Feldt 
Year; venue 2024; Software Testing, Verification and Reliability, vol. 34, no. 7, Art. e1893 
Methodology Uses GPT-4 to choose the most likely element among the top-ranked candidates 
produced by VON Similo; the model's stated motivations were also analysed. 
Key findings On 804 element pairs from 48 web applications, failed localisations fell from 70 to 40 
(a 43% reduction), at the cost of slower execution and API fees.

<!-- Page 27 -->

Parameter Details 
Limitations Single proprietary model; added cost and latency; LLM choice not independently 
validated by execution (our assessment). 
Project relevance Closest prior work to the Generator (M5b): an LLM re-ranks deterministic candidates. 
VeriHeal adds execution-based validation and a policy layer. 
Table 2.9: Paper review: Kluge and Stocco (EMSE 2026) [32] 
Parameter Details 
Paper title Web element relocalization in evolving web applications: A comparative analysis and 
extension study 
Authors A. Kluge, A. Stocco 
Year; venue 2026; Empirical Software Engineering, vol. 31, no. 6, Art. 175 
Methodology Replicates the Similo and VON Similo studies, refines the algorithms and parameters, 
builds a benchmark 23 times larger than the original, and proposes HybridSimilo. 
Key findings VON Similo tends to produce more false positives than Similo; refinements improved 
Similo's accuracy on the original benchmark by 5.62%; HybridSimilo located 98.8% of 
elements with broken locators on the extended benchmark. 
Limitations Localisation accuracy only; does not address whether the test should have failed (our 
assessment). 
Project relevance Confirms that similarity-based relocalisation is strong but can produce false positives, 
motivating hard gates and replay. 
Table 2.10: Paper review: Romano et al. (ICSE 2021) [14] 
Parameter Details 
Paper title An Empirical Analysis of UI-Based Flaky Tests 
Authors A. Romano, Z. Song, S. Grandhi, W. Yang, W. Wang 
Year; venue 2021; IEEE/ACM 43rd Int. Conf. on Software Engineering (ICSE), pp. 1585-1597 
Methodology Analysed 235 flaky UI test samples from 62 web and Android projects to identify root 
causes, how flakiness is exposed, and how it is fixed. 
Key findings Identifies common root causes and fixing strategies for UI-test flakiness and argues that 
rerun-based detection is a poor fit for expensive UI tests. 
Limitations Focuses on flakiness, not on locator repair (our assessment). 
Project relevance Motivates the Failure Classifier (M2) separating timing failures from locator failures 
before any healing. 
Table 2.11: Paper review: Saarathy et al. (IJSM 2024) [22] 
Parameter Details 
Paper title Self-Healing Test Automation Framework using AI and ML 
Authors S. C. P. Saarathy, S. Bathrachalam, B. K. Rajendran 
Year; venue 2024; International Journal of Strategic Management, vol. 3, no. 3, pp. 45-77 
Methodology Describes a framework combining AI/ML models for dynamic locator identification, 
intelligent waiting and anomaly detection, with an architecture and a case study on an 
e-commerce web application. 
Key findings Reports, for one case study, a 70% reduction in maintenance time (about 40 to 12 hours 
per month), reliability rising from about 70% to 90%, an 85% fix success rate, and 
estimated cost savings of about 60%. 
Limitations No suite size, study duration or measurement protocol reported; the 80% "reliability 
improvement" stated in the case study is inconsistent with the 70%->90% figures; 
published in a management journal (our assessment).

<!-- Page 28 -->

Parameter Details 
Project relevance Illustrates the claimed benefits of self-healing; its figures are not adopted as targets for 
this project (see Table 2.17). 
Table 2.12: Paper review: Kavuri (IJISAE 2023) [23] 
Parameter Details 
Paper title Self-Healing Test Automation Framework Using Autonomous ML Agents for Real -
Time Test Maintenance and Failure Recovery 
Authors S. Kavuri 
Year; venue 2023; International Journal of Intelligent Systems and Applications in Engineering, vol. 
11, no. 4, pp. 1089-1098 
Methodology Proposes ML agents that combine anomaly detection, flexible locator strategies and 
reinforcement learning to find and repair broken tests. 
Key findings The abstract reports a 38% drop in manual test maintenance and a 45% improvement in 
test execution stability on "industry-standard applications". 
Limitations Applications, baseline and measurement method are not described in the abstract (our 
assessment). 
Project relevance Treated as a literature-reported claim only (Table 2.17). 
Table 2.13: Paper review: Abhichandani et al. (ICICI 2025) [41] 
Parameter Details 
Paper title AI-Driven Self-Healing in Test Automation: A Review of Autonomous Quality 
Assurance 
Authors S. Abhichandani, N. R. T. Vadrevu, V. Bagmar 
Year; venue 2025; 3rd Int. Conf. on Inventive Computing and Informatics (ICICI), pp. 1601-1608 
Methodology Review of AI-based test automation frameworks published from 2021 to 2025 that use 
ML, anomaly detection, NLP and reinforcement learning to create, run and update test 
scripts. 
Key findings Concludes that AI-driven frameworks improve efficiency and reliability in CI/CD 
pipelines; the abstract reports no quantitative results. 
Limitations Review-level evidence; no new measurements (our assessment). 
Project relevance Confirms the topic's relevance; used only for context. 
Table 2.14: Paper review: Huang et al. (ICLR 2024) [31] 
Parameter Details 
Paper title Large Language Models Cannot Self-Correct Reasoning Yet 
Authors J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, D. Zhou 
Year; venue 2024; Int. Conf. on Learning Representations (ICLR) 
Methodology Studies intrinsic self-correction, where an LLM revises its answer using only its own 
capabilities, on reasoning tasks. 
Key findings LLMs struggle to self-correct reasoning without external feedback, and performance 
sometimes degrades after self-correction. 
Limitations Reasoning benchmarks, not software testing (our assessment). 
Project relevance Key justification for treating the LLM Critic (M6c) as advisory and using execution 
results as the external feedback that decides acceptance.

<!-- Page 29 -->

## 2.3 Existing Tools and Frameworks 
### 2.3.1 Selenium WebDriver 
Selenium automates browsers through the WebDriver protocol  [1] and offers eight traditional 
locator strategies plus relative locators  [2]. It has no built -in self-healing. It can send Chrome 
DevTools Protocol commands to Chromium -based browsers, which allo ws reading the 
accessibility tree, but the Selenium documentation describes this CDP support as temporary 
until WebDriver BiDi is implemented [29]. VeriHeal targets Selenium because it is widely used 
and because it allows a direct comparison with Healenium. 
### 2.3.2 Playwright 
Playwright recommends prioritising user -facing attributes and explicit contracts such as role 
locators, re-locates elements on every action (auto -waiting and retry), and is strict: an action 
throws an exception if more than one element matches  [10]. These locator design choices 
reduce fragility and ambiguity. In addition, Playwright now ships three Test Agents (planner, 
generator and healer) that are driven from an AI tool of the user's choice; the agent definitions 
are collections of instructions and MCP tools  [?playwright_agents]. The healer "executes the 
test suite and automatically repairs failing tests": it replays the failing steps, inspects the current 
UI to find equivalent elements or flows, suggests a patch such as a locator update, a wait 
adjustment or a data fix, and re -runs the test until it passes or guardrails stop the loop; if the 
healer believes that functionality is broken, the test is skipped  [?playwright_agents]. The 
documentation reviewed does not describe a confidence policy, an independent check that the 
test's intent is preserved, or a review and commit process. Two design choices differ fr om 
VeriHeal: the healer may change waits and data, which VeriHeal's locator -only invariant 
forbids, and the decision that functionality is broken is left to the agent, whereas 
VeriHeal decides it by explicit gates and reports the test as failed rather than  skipped. 
Playwright support is listed as future scope for VeriHeal. 
### 2.3.3 Cypress 
Cypress recommends dedicated data-* attributes such as data-cy so that selectors are isolated 
from CSS and JavaScript changes  [11]. Cypress also offers cy.prompt, a beta command 
(requiring a Cypress Cloud account) that turns natural -language test steps into Cypress 
commands for end-to-end tests in Chromium-based browsers [?cypress_prompt]. Its generated

<!-- Page 30 -->

code is cached; according to the documentation, "cy.prompt self -heals when a selector or its 
text content changes between runs", either through the cached mapping or through a new AI 
call, and healed steps are tagged "Self -healed" in the command log and ca n be filtered in 
Cypress Cloud [?cypress_aigen]. The documentation recommends replacing the cy.prompt call 
with the generated commands for predictable, version-controlled tests [?cypress_aigen]. It does 
not describe an execution-based check of test intent before a heal is accepted. 
### 2.3.4 Healenium 
Healenium is an open-source (Apache-2.0) self-healing library for Selenium. It works with all 
Selenium-supported languages through a proxy between the client and the Selenium server, and 
stores reference selectors and healing data in PostgreSQL  [4]. On a successful run it saves the 
locator as a baseline; on NoSuchElement it compares the current page with the stored data, 
produces a list of healed locators, continues the test with the highest-scoring one, and generates 
a report with the healed locator, a screenshot and a feedback button [5]. An IDE plug-in is also 
offered [4]. The reviewed documentation does not describe an execution -based check that the 
healed test still exercises the intended behaviour, nor a mechanism that explicitly classifies a 
missing element as a probable defect. Healenium is used as an external base line in the 
evaluation (Chapter 4). 
### 2.3.5 Other components used by the proposed system 
MCP [25] for optional tool access by agents; OpenAPI 3.1 [27] and the oasdiff tool, which 
compares OpenAPI specifications and reports breaking changes  [46], for API schema -drift 
detection; Pact, a code -first contract -testing tool, as a reference for contract -testing 
concepts [47]; and GitHub branch protection , which can require approving reviews and 
passing status checks before merging [48]. 
Commercial platforms. Several commercial test platforms advertise AI -based self-healing. 
Their algorithms are proprietary and are not documented in peer-reviewed sources, so they are 
not included in the quantitative comparison. 
## 2.4 Comparative Analysis 
Table 2.15 compares the tools on capabilities relevant to this project, and Table 2.16 compares 
the research approaches. Entries for existing tools are based only on the cited documentation;

<!-- Page 31 -->

"not documented" means the reviewed documentation does not describe the capability, not that 
it is impossible. 
Table 2.15: Capability comparison of existing tools and the proposed system 
Capability Selenium Playwright Cypress Healenium 
VeriHeal (pr
oposed) 
Runtime locator 
healing 
No Healer agent 
repairs failing 
tests (AI tool) 
cy.prompt 
self-heals 
steps (beta, 
Cloud) 
Yes Yes (A3, 
gated) 
Preventive locator 
guidance 
Locator 
strategies 
Role locators, 
strictness 
data-* 
attributes 
- Recommends 
role/data-* 
in repaired 
locators 
Stored element 
baseline 
No No No Yes 
(PostgreSQL) 
Yes 
(fingerprint 
incl. role, 
name, bbox) 
Independent check of 
test intent before 
accepting a heal 
- Not 
documented 
(re-runs until 
pass) 
Not 
documented 
Not 
documented 
Yes (H5 
replay with 
test's own 
assertions) 
Explicit "probable 
defect" outcome 
- Test skipped 
if healer 
believes 
functionality 
is broken 
Not 
documented 
Not 
documented 
Yes 
(FAIL_DEFE
CT; test fails) 
Uses LLMs for 
healing 
No Yes (Test 
Agents) 
Yes 
(cy.prompt
) 
Not 
documented 
Yes 
(generator, 
advisory 
critic) 
Healed status distinct 
from pass 
- Not 
documented 
"Self-healed" 
tag 
Report marks 
healed 
locators 
Yes 
(PASSED-
HEALED) 
Code update path Manual Healer 
suggests 
patch; commit 
process not 
documented 
Export 
generated 
commands 
IDE plug-in PR with 
evidence; 
human merge 
Table 2.16: Comparison of research approaches to broken web tests 
Approach Main idea Signals used 
Guards against 
healing a real 
defect? 
Reported 
evaluation 
ROBULA+ [9] Generate robust 
XPath 
DOM attributes, 
text 
Not applicable 
(prevention) 
8% broken vs 22-
78% 
WATER [17] Differential repair 
suggestions 
Two executions 
(old, new) 
Suggestions only Qualitative 
WATERFALL [39] Incremental repair Fine-grained 
versions 
Not discussed in 
reviewed text 
89.3% vs 28.9% 
repaired 
VISTA [40] Visual repair Screenshots, 
crawling 
Not discussed in 
reviewed text 
81% repaired

<!-- Page 32 -->

Approach Main idea Signals used 
Guards against 
healing a real 
defect? 
Reported 
evaluation 
Similo [18] Weighted multi-
attribute similarity 
DOM attributes No 11% vs 27% 
failures 
VON Similo [19] Similarity + visual 
overlap 
DOM + bounding 
boxes 
No 94.7% vs 83.8% 
LLM + VON 
Similo [6] 
LLM picks among 
top candidates 
DOM + LLM 
reasoning 
No 70 -> 40 failures of 
804 
Playwright 
healer [?playwright_
agents] 
LLM agent repairs 
failing test 
Live UI, test 
failure 
Skips test if it 
judges 
functionality 
broken 
No published 
evaluation 
identified 
cy.prompt [?cypr
ess_aigen] 
Cached AI-
generated steps re-
generated on 
change 
Prompt, DOM, 
cache 
Not documented No published 
evaluation 
identified 
Healenium [5] Runtime healing, 
best score 
Stored locator 
path 
Not documented No peer-reviewed 
evaluation 
identified in this 
survey 
VeriHeal (proposed) Deterministic + 
LLM candidates, 
validated 
DOM, a11y tree, 
fingerprint, replay 
Yes: H4 semantic 
gate, H5 replay, 
FAIL_DEFECT 
To be measured 
(Ch. 4-5) 
## 2.5 Limitations of Existing Systems 
1. Localisation is not the same as correct healing.  The strongest research methods 
measure whether the intended element is found  [18], [19], [32]. They do not measure 
whether the test should have passed. On a page where the element was removed, the 
most similar remaining element can still be returned. 
2. False positives. Similarity methods can select the wrong element, and VON Similo was 
found to produce more false positives than Similo [32]. 
3. Unvalidated LLM decisions. LLM-based selection improves localisation but adds cost 
and latency [6], and LLMs are not reliable judges without external feedback [31], [33]. 
Recent framework features such as the Playwright healer agent and Cypress cy.prompt 
bring LLM -based healing into mainstream tools  [?playwright_agents], 
[?cypress_aigen], but their documentation does not describe confidence thresholds or 
an independent acceptance check, and the Playwright healer may also adjust waits and 
data.

<!-- Page 33 -->

4. Weak evidence for headline benefits. The large maintenance savings reported in some 
self-healing articles come from single case studies or abstracts without disclosed 
protocols [22], [23]. Table 2.17 summarises how such claims are treated. 
5. Limited governance. Runtime healing tools continue the test with the best candidate; 
the reviewed documentation does not describe autonomy levels, approval policies or 
audit trails [5]. 
6. Privacy. Sending DOM content and screenshots to external LLM services raises data -
protection and prompt-injection risks [34], [35] that are rarely discussed in self-healing 
literature. 
7. Schema and data changes.  API contract changes are handled by separate contract -
testing tools [47], [46]; automatically generating new test data to make a failing API test 
pass would hide contract violations. 
Table 2.17: Quantitative claims found in self-healing sources and how this report treats them 
Claim Source Evidence basis Treatment in this report 
70% less maintenance 
time 
[22] One e-commerce case study 
(40 -> 12 h/month); suite size 
and protocol not reported 
Literature-reported only; not a 
target 
60% cost saving [22] Described by the authors as 
an estimate 
Literature-reported only 
38% less manual 
maintenance; 45% more 
stability 
[23] Abstract; applications and 
method not described 
Literature-reported only 
"60% fewer false 
positives"; "40-60% less 
locator flakiness" 
Earlier project 
drafts 
No source could be traced Removed 
"Zero overhead"; 
"Level-4 autonomy" 
Earlier project 
drafts 
Not defined or measurable Replaced by measured 
overhead (Eq. 4.6) and the 
A0-A4 taxonomy (Table 3.2) 
## 2.6 Identified Research Gaps 
The limitations above lead to six gaps. Table  2.18 maps each gap to the part of VeriHeal  that 
addresses it. 
Table 2.18: Research gaps and how the proposed system addresses them 
ID Gap Addressed by 
RG1 No explicit separation of locator drift from genuine 
regressions in healing tools 
M2 classifier, H4 semantic gate, 
FAIL_DEFECT outcome (M7)

<!-- Page 34 -->

ID Gap Addressed by 
RG2 Heals accepted by best score, or by re-running until 
the test passes, without independent evidence that 
the test's intent is preserved 
M6 hard gates H1-H5 with sandbox replay of 
the test's own assertions 
RG3 LLMs used as decision-makers without 
independent verification 
M5b used only for proposals; M6c Critic is 
advisory; acceptance requires H5 
RG4 No defined autonomy levels, approval policy or 
audit trail 
A0-A4 taxonomy, confidence thresholds, PR-
only changes, M8 audit store 
RG5 Privacy and prompt-injection risks of sending page 
data to LLMs are not addressed 
M3 Redaction Filter, LLM Gateway checks, 
least-privilege design (Section 3.9.1) 
RG6 Benefits reported without reproducible baselines Benchmark with injected drift and regressions, 
five baselines, metric definitions (Chapter 4) 
## 2.7 Scope of the Proposed System 
Table 2.19 separates the core functionality, supporting components, gated extensions and future 
scope. Only the core and supporting components are committed deliverables for the project. 
Table 2.19: Scope of the proposed system 
Category Included Notes 
Core (MVP) Locator failure detection and classification; 
context collection with redaction; fingerprint 
store; deterministic similarity matching; 
independent validation (H1-H5); decision 
engine; audit and metrics store 
Selenium 4 + pytest (Python); 
Chromium; Spring PetClinic 
Core (later phase) LLM Generator and advisory Critic; Repair 
& PR Agent 
LLM provider selected by the team; PRs 
never auto-merged 
Supporting Review dashboard; GitHub Actions 
integration; optional MCP tool interface 
 
Gated extensions E1 visual fallback (multimodal LLM first; 
CNN only if justified); E2 API contract-drift 
classifier (report-only) 
Built only if gate G3 is passed 
(Section 3.4) 
Future scope Synthetic test-data generation with contract 
checks; LLM-based test generation; 
Playwright, Cypress and Appium adapters 
Not part of this project's deliverables 
Out of scope Automatic changes to assertions, expected 
values or test data; automatic merging; 
healing of non-locator failures 
Prohibited by design

<!-- Page 35 -->

# Chapter 3: Proposed System 
This chapter describes VeriHeal in detail. It is the reference for all later chapters: module names 
(M1-M11, E1, E2), autonomy levels (A0-A4), gates (H1-H5, G1-G4) and thresholds defined 
here are used unchanged in Chapters 4-6. 
## 3.1 Detailed Explanation of Proposed System 
### 3.1.1 Design principles 
1. Locator-only repair (safety invariant). The system may change locators only. It never 
changes assertions, expected values, waits that encode business timing, or test data. If a 
heal would require such a change, the test fails normally. 
2. Evidence over opinion.  A repair is accepted only on execution -based evidence 
(Section 3.10). LLM outputs are proposals; an LLM's opinion is never sufficient on its 
own. 
3. Deterministic first. A fast, explainable similarity matcher runs first; the LLM is called 
only when the matcher is not confident. This limits cost, latency and data exposure. 
4. Fail safe. When evidence is incomplete or contradictory, the system reports a failure. A 
missed heal costs an engineer some minutes; a false heal can hide a defect. 
5. Human authority over code.  All repository changes go through pull requests on 
separate branches. Merging is always a human action. 
6. Privacy by default.  Page data is redacted before storage or transmission, and page 
content is treated as untrusted input. 
7. Measurability. Every decision is logged with enough detail to compute the metrics in 
Section 4.4. 
### 3.1.2 Modules 
Table 3.1 lists the modules and their responsibilities. Figure  3.1 (Section 3.2) shows how they 
are connected.

<!-- Page 36 -->

Table 3.1: Modules of the proposed system 
ID Module Responsibility Tier / phase 
M1 Test Execution 
Adapter 
Wraps Selenium WebDriver 
(HealingDriver) and pytest; records 
element fingerprints on passing steps; intercepts 
locator exceptions; continues a test after an A3 
heal and marks it PASSED-HEALED. 
Core, P1 
M2 Failure Classifier Assigns each failure to one class (C1 not found, 
C2 ambiguous, C3 timing, C4 assertion, C5 
HTTP/navigation, C6 API contract, C7 
environment). Only C1/C2 enter healing. 
Core, P1 
M3 Context Collector + 
Redaction Filter 
Captures the DOM, accessibility tree, 
screenshot and step metadata; masks personal 
data and secrets; prunes the DOM for the LLM. 
Core, P1 
M4 Element Fingerprint 
Store 
Stores, per test step, the last-known-good 
fingerprint of the target element (attributes, role, 
accessible name, text, XPath, neighbours, 
bounding box, app version). 
Core, P1 
M5a Similarity Matcher Scores every candidate element against the 
fingerprint (Eq. 3.1) and returns the top-𝑘 
candidates with locators. 
Core, P1 
M5b LLM Generator 
Agent 
Proposes candidate locators from the redacted 
context when M5a is not confident; output must 
follow a JSON schema. 
Core, P2 
M6 Independent 
Validator 
Applies hard gates H1-H4 to every candidate 
and the replay gate H5 to the best gate-passing 
candidate. 
Core, P1 
M6c LLM Critic Agent Reviews an evidence summary and returns 
accept / reject / uncertain. Advisory: it can veto, 
never approve. 
Core, P2 
M7 Healing Decision 
Engine 
Computes confidence (Eq. 3.7), applies the 
policy thresholds and the regression 
discrimination rules, and outputs HEAL (A3), 
SUGGEST (A2), FAIL_DEFECT or 
FAIL_UNCERTAIN. 
Core, P1 
M8 Audit and Metrics 
Store 
Append-only record of every failure, candidate, 
gate result, LLM call, decision and review. 
Core, P1 
M9 Repair & PR Agent Locates the locator definition in the test source 
(AST), creates a minimal patch on a bot branch, 
re-runs affected tests in a sandbox and opens a 
PR with evidence. 
Core, P3 
M10 Review Dashboard Shows runs, failures, heal evidence and 
confidence; lets a reviewer approve or reject; 
shows the audit log and history. 
Supporting, P2 
M11 CI Integration GitHub Actions workflow, status check, report 
artifact and job summary. 
Supporting, P3 
- LLM Gateway Single exit point for LLM calls: redaction 
check, schema enforcement, timeouts, rate and 
cost limits, logging. 
Supporting, P2 
- MCP Tool Gateway Optional MCP interface through which agents 
call allow-listed tools. 
Supporting (optional), P3

<!-- Page 37 -->

ID Module Responsibility Tier / phase 
E1 Visual Fallback Uses a screenshot when DOM-based matching 
fails; multimodal LLM first, CNN detector only 
if justified by measurement. 
Extension, P4 (gated) 
E2 API Contract-Drift 
Classifier 
Classifies API test failures as contract violation, 
unapproved breaking change or approved 
change. Report-only. 
Extension, P4 (gated) 
### 3.1.3 Autonomy model and human-in-the-loop policy 
"Autonomous" is not a useful description unless it says which decisions are automated. 
Following the stage-and-level view of automation of Parasuraman et al. [26], VeriHeal defines 
five project-specific autonomy levels (Table 3.2). They are not an industry standard; they exist 
to make the policy of this project precise and testable. 
Table 3.2: Project-defined autonomy levels A0-A4 
Lev
el Name What the system does Used for 
A0 Report Reports the failure only. Non-healable classes C3-C5, 
C7 
A1 Diagnose Classifies the failure and explains it with 
evidence. 
API contract failures (E2); 
FAIL_DEFECT; 
FAIL_UNCERTAIN 
A2 Suggest Proposes a validated repair; the test still fails 
in this run; a PR is opened for review. 
Locator failures with 𝜏𝑆<=
𝑐<𝜏𝐴, or any high-risk 
case (below) 
A3 Heal and propose Applies a validated repair at run time (test 
marked PASSED-HEALED) and opens a PR 
for review. 
Locator failures with 𝑐>=𝜏𝐴 
and all gates H1-H5 passed 
A4 Autonomous change Commits or merges changes without review. Prohibited in this project 
Table 3.3 states the human-in-the-loop policy decision by decision. 
Table 3.3: Human-in-the-loop policy 
Question Policy 
Which activities are fully automated? Failure classification, context capture, redaction, candidate 
generation, gate checks, sandbox replay, confidence scoring, 
PR preparation, logging. 
Which decisions are made by AI agents? Only proposals: the Generator proposes candidates; the Critic 
may veto. Acceptance is decided by the deterministic policy 
in M7 using execution evidence. 
Which corrections require independent 
validation? 
All of them. No candidate from any source can be applied 
without H1-H4, and A3 additionally requires H5. 
Which operations require human approval? Any change to the repository (merge of a repair PR), changes 
to policy thresholds, and enabling extensions E1/E2. 
Are pull requests generated automatically? Yes, for A3 and A2 decisions, after the sandbox re-run passes.

<!-- Page 38 -->

Question Policy 
Can the system modify the repository 
automatically? 
Only by pushing to its own branch veriheal/heal-
<id>. Branch protection on the main branch requires an 
approving review and a passing status check [48]. 
Is automatic merging permitted? No. Auto-merge is disabled and the bot account has no 
permission to bypass branch protection. 
When is A3 downgraded to A2 (mandatory 
review before any run-time heal)? 
(i) the candidate came only from the LLM Generator and was 
not in M5a's top-𝑘; (ii) the element's role changed; (iii) the 
locator is shared by more than 𝑁𝑠ℎ𝑎𝑟𝑒 tests (default 5); (iv) 
the page URL pattern differs from the fingerprint; (v) the 
Critic returned "uncertain". 
What happens after a rejected PR? The candidate is blacklisted for that step and application 
version; later runs fail normally until a human fixes the test. 
### 3.1.4 Safeguards against critical technical risks 
Incorrect self-healing. 
Five layers protect against a wrong heal: (1) hard gates H1 -H4 reject candidates that do not 
resolve, are ambiguous, are not interactable or are semantically incompatible; (2) the replay 
gate H5 re-runs the test in a separate browser session with the candidate and requires the test's 
own assertions to pass; (3) the confidence threshold 𝜏𝐴 is calibrated so that the measured false-
heal rate stays below a target (Algorithm 3.8); (4) the A3-to-A2 downgrade rules force review 
for high-risk cases; (5) a run-time heal never changes the code, and a rejected PR blacklists the 
candidate, which acts as the rollback mechanism. Every decision can be traced in M8. 
Genuine application defects. 
Table 3.4 shows how the system distinguishes the change types listed in the project brief. The 
key idea is that locator drift changes how an element is addressed but not what it is or what it 
does; a regression changes what it is or what it does. 
Table 3.4: Distinguishing locator drift from genuine regressions 
Change Observable signals Expected decision 
Locator drift 
(renamed id, name) 
Unique candidate with same role and 
accessible name; high attribute 
similarity elsewhere; replay passes 
A3 heal (or A2 if below 𝜏𝐴) 
DOM restructuring 
(wrapper added, 
reordering) 
XPath similarity drops; role, name, text, 
neighbours unchanged; replay passes 
A3 / A2 
CSS selector change 
(class renamed) 
Class similarity drops; other signals 
unchanged 
A3 / A2 
Accessibility 
attribute change 
(aria-label edited) 
Name similarity lower but above 
𝜏𝑛𝑎𝑚𝑒; role unchanged; replay passes 
A2 by default (name change is a semantic 
signal); A3 only if 𝑐>=𝜏𝐴

<!-- Page 39 -->

Change Observable signals Expected decision 
Element removed No candidate with compatible role and 
name (H4 fails for all) 
FAIL_DEFECT 
Element hidden or 
disabled 
Candidate found but H3 fails FAIL_DEFECT 
Element replaced by 
a different control 
(e.g. "Delete" where 
"Save" was) 
Role may match, but name similarity 
below 𝜏𝑛𝑎𝑚𝑒 
FAIL_DEFECT 
Behaviour broken 
(handler removed) 
H1-H4 pass, but replay H5 fails the 
test's own assertion 
FAIL_UNCERTAIN (reported as possible 
defect; no heal) 
Duplicate look-alike 
elements 
H2 fails (ambiguous) or margin 𝛥 small A2 at most; usually FAIL_UNCERTAIN 
Timing / flakiness Element appears within extended wait C3: no heal; reported as flaky 
Synthetic test data and API schema healing. 
Schema healing is the most dangerous capability proposed in the original project idea, because 
generating new data to make a failing API test pass can hide exactly the contract violations that 
regression tests exist to catch. VeriHeal therefore limits it to the report-only extension E2 with 
this policy: 
1. Schema validation. Each API response in an API test is validated against the OpenAPI 
specification of the build under test [27]. 
2. Version comparison.  The specification is compared with the baseline specification 
using an OpenAPI diff tool that reports breaking changes [46]. 
3. Classification. (a) Response violates the current specification ⇒ contract violation  
(defect). (b) Specification changed in a breaking way without an approval record 
(version bump plus an approved change label or changelog entry) ⇒ unapproved 
breaking change  (defect, API owner notified). (c) Specification changed, change 
approved, response conforms ⇒ intended change. 
4. Approval policy. Even for an intended change, VeriHeal  only suggests updated test 
data or expectations (A1/A2). It never edits expected values automatically. 
5. Failure handling. If the specification cannot be retrieved or parsed, the test fails as C6 
with the reason recorded. 
Synthetic data generation itself (for example payloads for a new required field) is future scope 
and, if built, would produce fixture changes as PRs only.

<!-- Page 40 -->

Generator-Critic reliability. 
The Generator (M5b) proposes locators; the Critic (M6c) reviews an evidence summary. Both 
are LLMs and may share blind spots, especially if they are the same model. Self -correction 
without external feedback is unreliable  [31], LLM judges show position, ver bosity and self -
enhancement biases [33], and hallucination is a known failure mode [30]. The design therefore: 
(i) gives the Critic the evidence (gate results, replay outcome, attribute differences), not the 
Generator's reasoning, to reduce anchoring; (ii) lets the Critic veto but not approve; (iii) uses 
execution results (H1 -H5) as the ground truth for acceptance; (iv) measures the Critic's 
usefulness separately (veto precision on the benchmark) and removes it if it adds no value; (v) 
prefers a different model or prompt for the Critic where the budget allows. Recorded baselines 
(fingerprints) are updated only after a human-approved merge, so they do not drift silently. 
MCP and code modification. 
MCP is a protocol through which an LLM host connects to tool servers [25]; it does not refactor 
code. In VeriHeal: (i) code analysis and modification are performed by the Repair & PR Agent 
(M9) using Python's abstract syntax tree to find the single assignm ent that defines the broken 
locator and to replace only that string; (ii) repository access uses a dedicated bot identity with 
a token restricted to one repository and to the permissions needed to push branches and open 
PRs; (iii) the patch is executed only in an ephemeral CI sandbox; (iv) the PR includes the diff, 
evidence and confidence, and requires an approving review. MCP, if adopted in P3, only 
exposes allow-listed tools ("query DOM", "run step in sandbox", "read file") to the agents; the 
MCP specific ation itself requires explicit user consent and treats tool descriptions from 
untrusted servers as untrusted [25]. 
Computer vision architecture. 
Four information sources were considered. DOM analysis is required: locators are evaluated on 
the DOM, and DOM attributes are the main similarity signals  [18]. The accessibility tree  is 
required: role and accessible name are the semantic signals that separate drift from regression 
(Table 3.4). A multimodal LLM on screenshots is not in the MVP; web-agent research reports 
that grounding a model's visual understanding into the correct page element remains a major 
challenge [44], so it is an extension (E1) to be tried only on cases the DOM -based pipeline 
cannot solve. A CNN-based GUI element detector  is not justified for the MVP: GUI element 
detection is a specialised problem; a large empirical study of seven detection methods led its

<!-- Page 41 -->

authors to combine a traditional method for non -text elements with a deep -learning model for 
text [45], it needs training data and GPU hosting, and the DOM already provides exact element 
boundaries. It will be considered only if E1 shows a measurable gap that a detector could close. 
Performance and infrastructure. 
The healing latency of one failure is the sum of its parts (Eq.  3.10). Deterministic matching is 
expected to be small; Similo reported about 4 ms per localisation [18]. LLM calls and sandbox 
replays are expected to dominate; their actual values depend on t he model, network and test 
length and will be measured rather than assumed. To respect CI time limits, VeriHeal caps the 
number of LLM-assisted heals per run (𝑁𝐿𝐿𝑀, default 10), applies a per-call timeout, and runs 
PR creation as a separate asynchronous job. Cost is estimated in Section 4.5.1. 
## 3.2 Block Diagram and System Workflow 
Figure 3.1 shows the block diagram. Blue blocks are deterministic components, orange blocks 
use an LLM, green blocks involve the human reviewer, and grey cylinders are data stores. Solid 
arrows are the main data flow; dashed arrows are optional paths (LLM use only on low 
confidence).

<!-- Page 42 -->

Figure 3.1: Block diagram of the proposed system 
Figure 3.2 shows the complete workflow with its decision points.

<!-- Page 43 -->

Figure 3.2: End-to-end healing workflow with decision points and human approval 
Workflow explanation. 
1. Normal step.  The test calls find_element. If the element is found, M1 records or 
refreshes its fingerprint in M4 and the test continues. 
2. Failure classification.  If the element is not found (or several match where one is 
expected), M2 waits for an extended period and checks page load and network state. If

<!-- Page 44 -->

the element appears, the failure is C3 (timing) and is reported as flaky; other classes are 
reported normally. Only C1/C2 continue. 
3. Context. M3 captures the DOM, accessibility tree and screenshot, masks sensitive 
values and prunes the DOM. 
4. Candidates. M5a scores page elements against the fingerprint. If the best score is at 
least 𝜏𝑔𝑒𝑛 and the margin over the second -best is at least 𝛿, its top -𝑘 candidates go 
straight to validation; otherwise M5b is also asked for candidates. 
5. Hard gates.  M6 checks H1-H4 for every candidate. If none passes, the element is 
considered missing or semantically changed and the decision is FAIL_DEFECT. 
6. Replay and critique. The best gate-passing candidate is replayed in a sandbox session 
(H5), and M6c reviews the evidence. 
7. Decision. M7 computes the confidence 𝑐 and applies the policy: A3 heal (test continues 
as PASSED -HEALED), A2 suggestion (test fails, repair proposed), or 
FAIL_UNCERTAIN. 
8. Repair proposal. For A3/A2, M9 patches the locator on a bot branch, re-runs affected 
tests and opens a PR. 
9. Human review. The reviewer approves (and merges) or rejects. Merging updates the 
fingerprint baseline; rejection blacklists the candidate. 
10. Audit. Every outcome is logged in M8. 
## 3.3 Working Principles and Algorithms 
The working principle of VeriHeal rests on four ideas. 
(1) Remember what the element looked like when the test passed. During every passing step 
M1 records an element fingerprint 𝐹: tag, id, name, class list, visible text, selected attributes 
(type, placeholder, href path, data-*), ARIA role and accessible name, absolute and robust 
XPath, texts of nearby labels and siblings, bounding box and page URL pattern. This turns "the 
locator broke" into "find the element that best matches 𝐹". 
(2) Search widely but cheaply first. Every visible element of a compatible tag family is scored 
against 𝐹 by a weighted similarity (Eq.  3.1), following the multi -attribute approach of

<!-- Page 45 -->

Similo [18]. The LLM is consulted only when the deterministic search is not clearly decisive, 
because LLM-assisted selection improves accuracy but costs time and money [6]. 
(3) Accept nothing without execution evidence. A candidate is a hypothesis: "this is the same 
element". The hard gates test whether it is uniquely addressable, usable for the step's action, 
and semantically the same kind of element with the same name. The replay gate tests the 
stronger hypothesis that  the test, with this locator, still verifies what it was written to verify, 
using the test's own assertions as the oracle. 
(4) Make the decision policy explicit.  The final decision combines the evidence into a 
confidence score and compares it with calibrated thresholds (Eqs. 3.7-3.9). The policy, not the 
LLM, decides; and when in doubt, the test fails. 
The algorithms for each step are given in Section 3.10. Ordinary LLM prompting is used inside 
Algorithm 3.5 as one component; it is not presented as an original algorithm. The project's 
algorithmic contribution lies in the combination of the fingerprint, t he gate design, the replay-
based oracle and the calibrated decision policy. 
## 3.4 Phase/Module-wise Explanation 
The work is split into a completed study phase (P0) and four implementation phases. Each 
implementation phase ends with a go/no-go gate whose criteria are fixed before the phase starts; 
any later change is recorded with its justification. Table 3.5 describes each phase and Figure 3.3 
shows the planned Semester VIII timeline; calendar dates will be fixed with the guide. 
 
Figure 3.3: Planned Semester VIII roadmap with go/no-go gates (relative weeks)

<!-- Page 46 -->

Table 3.5: Phase-wise implementation plan 
Phase Modules and purpose 
Technical 
implementation 
Inputs -> 
outputs Deliverables 
P0 
(Sem 
VII, 
done) 
Study and design Literature survey, 
requirements, 
architecture, algorithms, 
benchmark design 
Project idea -> 
design 
This report 
P1 
MVP 
pilot 
(W1-
W5) 
M1-M4, M5a, M6 
(H1-H5), M7 (without 
critic), M8; benchmark 
harness 
Python, Selenium 4, 
pytest plug-in, CDP 
accessibility tree, 
PostgreSQL/SQLite, 
mutation scripts for 
PetClinic 
Test runs -> 
decisions + audit 
records 
Working pipeline on one 
app; benchmark v1; G1 
report 
P2 
(W6-
W9) 
M5b, M6c, LLM 
Gateway, M10 
Provider-agnostic 
gateway with JSON 
schema output, 
redaction checks, cost 
limits; FastAPI 
dashboard 
Context -> LLM 
candidates, 
verdicts 
LLM-assisted pipeline; 
dashboard; ablation B2 
vs B3 vs B4; G2 report 
P3 
(W10-
W12) 
M9, M11, security 
hardening, optional 
MCP 
Python ast patcher, 
GitHub REST API, 
GitHub Actions, branch 
protection, secrets 
Decisions -> PRs 
with evidence 
End-to-end CI 
integration; security 
tests; G3 report 
P4 
(W13-
W14, 
gated) 
E1, E2 Multimodal LLM 
fallback; oasdiff-based 
classifier 
Screenshots / 
specs -> 
suggestions 
Extension prototypes; G4 
report 
Eval 
(W13-
W16) 
Full evaluation Benchmark runs for B0-
B4, statistics 
Runs -> metrics Chapter 5 results; final 
report 
Dependencies. P2 depends on the fingerprint store and validator from P1; P3 depends on stable 
decisions from P2 (or from P1 if G2 fails); P4 runs only if G3 passes. If G2 fails, the project 
continues with the deterministic pipeline (B2 configuration) and reports the LL M result as a 
negative finding. 
Table 3.6: Go/no-go gates (proposed targets, fixed before each phase) 
Gat
e Criteria (all must hold) If not met 
G1 (a) Regression Masking Rate =0 on the regression set; (b) False-Heal 
Rate at A3 <=5%; (c) Locator Recovery Rate of M5a >=0.80 on the 
drift calibration set; (d) classifier precision for C1/C2 >=0.95; (e) p95 
healing latency excluding replay <=2 s 
Fix and re-run P1 (one-
week buffer); do not start 
P2 
G2 (a) RMR =0; (b) FHR at A3 <=2% with Wilson 95% upper bound 
<=5%; (c) LLM-assisted LRR >= M5a LRR +5 percentage points; 
(d) mean LLM cost per LLM-assisted heal within the budget in 
Section 4.5.1; (e) 100% of redaction test cases pass 
Keep LLM disabled; 
continue with B2 
configuration

<!-- Page 47 -->

Gat
e Criteria (all must hold) If not met 
G3 (a) 100% of PRs carry diff, evidence and confidence; (b) zero direct 
pushes to the protected branch; (c) sandbox re-run before every PR; (d) 
CI overhead on fully passing runs <=10% (Eq. 4.6); (e) audit records 
complete for 100% of decisions 
Fix before any extension 
work; P4 cancelled if 
unresolved 
G4 E1: built only if at least 10% of residual unhealed drift cases are 
visually identifiable. E2: zero contract violations classified as "intended 
change"; overall classification accuracy >=90% 
Extension reported as not 
adopted 
The target values are engineering targets chosen for this project, not literature results. The 0.80 
recovery target for M5a is set below the localisation rates reported for similarity-based methods 
on their own benchmarks  [18], [19] because the PetClinic b enchmark also contains harder 
mutation operators. The zero -tolerance target for regression masking reflects design principle 
DP4. 
## 3.5 System Analysis 
### 3.5.1 Functional requirements 
Table 3.7 lists the functional requirements, each traced to the module that implements it. 
Table 3.7: Functional requirements 
ID Requirement Module 
FR-01 The system shall intercept every element lookup made through the Selenium 
WebDriver during a pytest run. 
M1 
FR-02 The system shall record an element fingerprint for every successful lookup and 
keep the latest fingerprint per test step and application version. 
M1, M4 
FR-03 The system shall classify every failed step into exactly one class C1-C7. M2 
FR-04 The system shall start the healing pipeline only for classes C1 (not found) and C2 
(ambiguous). 
M2 
FR-05 The system shall capture the DOM, accessibility tree, screenshot, URL and step 
metadata at the moment of failure. 
M3 
FR-06 The system shall mask configured sensitive values (input values, emails, phone 
numbers, tokens, elements marked sensitive) before storing or transmitting context. 
M3 
FR-07 The system shall rank candidate elements by the similarity score of Eq.  3.1 and 
synthesise a locator for each of the top-𝑘. 
M5a 
FR-08 The system shall request LLM candidates only when the top score is below 𝜏𝑔𝑒𝑛 
or the margin is below 𝛿, and only within the per-run cap 𝑁𝐿𝐿𝑀. 
M5b 
FR-09 The system shall reject any LLM output that does not conform to the response 
JSON schema. 
LLM 
Gateway 
FR-10 The system shall evaluate hard gates H1-H4 on every candidate and the replay gate 
H5 on the best gate-passing candidate. 
M6 
FR-11 The system shall obtain an advisory verdict from the Critic for candidates that pass 
H1-H4 (from P2 onwards). 
M6c

<!-- Page 48 -->

ID Requirement Module 
FR-12 The system shall compute a confidence score and output exactly one of HEAL, 
SUGGEST, FAIL_DEFECT, FAIL_UNCERTAIN according to the policy. 
M7 
FR-13 The system shall continue a test after a HEAL decision and report its status as 
PASSED-HEALED. 
M1 
FR-14 The system shall never modify assertions, expected values or test data. All 
FR-15 The system shall create a patch only when exactly one source definition of the 
broken locator is found. 
M9 
FR-16 The system shall re-run the affected tests with the patch in an isolated environment 
before opening a PR. 
M9 
FR-17 The system shall open a PR containing the diff, gate results, confidence, redacted 
before/after crops and a link to the run. 
M9 
FR-18 The system shall let an authorised reviewer approve or reject a heal and shall 
blacklist rejected candidates. 
M10 
FR-19 The system shall log every failure, candidate, gate result, LLM call, decision, PR 
and review in an append-only store. 
M8 
FR-20 The system shall export run and decision data for computing the metrics of 
Section 4.4. 
M8 
FR-21 (E2) The system shall classify API test failures as contract violation, unapproved 
breaking change or intended change, and shall not modify expectations. 
E2 
### 3.5.2 Non-functional requirements 
Table 3.8 lists the non-functional requirements with measurable targets where possible. 
Table 3.8: Non-functional requirements 
ID Quality Requirement (measurable where possible) 
NFR-01 Safety Regression Masking Rate on the benchmark regression set shall be 0 
(Eq. 4.4). 
NFR-02 Correctness False-Heal Rate at A3 shall not exceed the gate targets (Table 3.6). 
NFR-03 Performance Deterministic matching (M5a) for one failure shall take <=2 s at p95 on the 
reference hardware; LLM calls shall time out after a configurable limit 
(default 30 s). 
NFR-04 CI overhead On runs with no failures, total suite time shall increase by <=10% (Eq. 4.6). 
NFR-05 Reliability A failure of any healing component shall never crash the test run; the step 
shall then fail with the original exception. 
NFR-06 Security The bot token shall have access to one repository only, without permission to 
bypass branch protection; secrets shall be stored in the CI secret store, never 
in code. 
NFR-07 Privacy No unredacted DOM, screenshot or API payload shall leave the test 
environment; redaction test suite must pass 100%. 
NFR-08 Auditability 100% of decisions shall be reconstructable from M8 records (inputs hash, 
candidates, gates, model, decision, reviewer). 
NFR-09 Cost LLM spending shall be capped per run and per month; the cap is 
configurable. 
NFR-10 Maintainability Modules shall communicate through typed interfaces; the LLM provider 
shall be replaceable by changing only the LLM Gateway configuration. 
NFR-11 Portability The complete environment shall start with one Docker Compose command 
on Linux, macOS or Windows (WSL2).

<!-- Page 49 -->

ID Quality Requirement (measurable where possible) 
NFR-12 Usability A reviewer shall be able to see the evidence for a heal and decide on one 
screen (Figure 3.18). 
### 3.5.3 Specific requirements 
1. Test code must follow the Page Object Model, with locators defined as module- or class-
level constants of the form NAME = (By.X, "value") , so that M9 can locate a unique 
definition. 
2. The accessibility tree is read through CDP and therefore requires a Chromium -based 
browser in P1-P3 [28], [29]. A JavaScript fallback that computes role and accessible 
name for candidate elements will be implemented for robustness. 
3. The application under test must run in a reproducible version -controlled state so that 
mutations can be applied and reverted (Section 4.2). 
4. An LLM provider (hosted API or locally hosted model) must be available from P2; its 
data-retention terms must be checked by the team before use. 
### 3.5.4 Software requirements 
Table 3.9 lists the planned software components. 
Table 3.9: Software requirements (planned) 
Component Choice Purpose 
Programming language Python 3 (version fixed at P1 start) Framework, plug-in, scripts 
Browser automation Selenium WebDriver 4, 
Chrome/Chromium 
Test execution, CDP access 
Test runner pytest Test discovery, plug-in hooks 
Application under test Spring PetClinic REST [36] + 
Angular front end [37] 
Benchmark subject 
Database PostgreSQL (SQLite allowed in P1) M4, M8 
Web framework FastAPI (planned) Healing service, dashboard 
LLM access Provider-agnostic gateway; provider 
[TEAM DECISION] 
M5b, M6c 
API tooling OpenAPI 3.1 specification [27]; 
oasdiff [46] 
E2 
Baseline tool Healenium (proxy mode) [4] Baseline B1 
Containerisation Docker, Docker Compose Reproducible environment 
CI/CD GitHub Actions; GitHub branch 
protection [48] 
M11, governance 
Diagramming / docs PlantUML, Graphviz, LaTeX This report

<!-- Page 50 -->

### 3.5.5 Hardware requirements 
Table 3.10 gives the estimated hardware needs. 
Table 3.10: Hardware requirements (estimates) 
Resource Minimum / recommended Reason 
Developer machine 4 CPU cores, 8 GB RAM minimum; 
16 GB recommended; 30 GB free disk 
Runs browser, PetClinic (two 
containers), PostgreSQL and the 
healing service together 
CI runner GitHub-hosted Linux runner Test and sandbox jobs 
Server for dashboard Any machine or small cloud VM able 
to run Docker Compose (2 vCPU, 
4 GB RAM estimate) 
Persistent M4/M8 data across CI runs 
GPU Not required for the MVP No CNN; LLM via API. Needed only 
if a local model is chosen (size depends 
on the model) 
Network Internet access to the LLM provider 
and GitHub 
P2 onwards 
These figures are planning estimates; actual usage will be measured in Semester VIII. 
## 3.6 Use Case Modelling 
Figure 3.4 shows the actors and use cases. The three major use cases are specified in 
Tables 3.11, 3.12 and 3.13. 
 
Figure 3.4: Use case diagram of the proposed system

<!-- Page 51 -->

Table 3.11: Use case UC-01: Heal broken locator 
Use case ID UC-01 
Name Heal broken locator 
Primary actor CI/CD Pipeline (test run); secondary: LLM Service 
Preconditions The test step has a stored fingerprint from an earlier passing run; the healing service is 
reachable; policy thresholds are configured. 
Main flow 1. Test step requests an element. 2. Lookup fails with NoSuchElement. 3. M2 classifies 
the failure as C1. 4. M3 captures and redacts context. 5. M5a returns top-𝑘 candidates 
with sufficient score and margin. 6. M6 applies H1-H4; at least one passes. 7. M6 
replays the test with the best candidate (H5) and it passes. 8. M6c returns "accept". 9. 
M7 computes 𝑐>=𝜏𝐴 and decides HEAL (A3). 10. M1 returns the element; the test 
continues and is reported PASSED-HEALED. 11. M8 logs the decision; a repair job is 
queued for M9. 
Alternative flows 5a. Score or margin too low: M5b is called (within 𝑁𝐿𝐿𝑀); its candidates join the set. 
9a. 𝜏𝑆 <=𝑐<𝜏𝐴, or a downgrade rule applies: decision SUGGEST (A2); test fails; 
repair job queued. 8a. Critic returns "uncertain": A3 downgraded to A2. 
Exception flows 3a. Class C3-C7: no healing; reported normally. 6a. No candidate passes H1-H4: 
FAIL_DEFECT. 7a. Replay fails: FAIL_UNCERTAIN. E1. Healing service 
unreachable or timeout: original exception re-raised (NFR-05). E2. LLM response 
invalid: discarded, logged, pipeline continues with M5a candidates only. 
Postconditions Exactly one decision record exists in M8; the test status is PASSED-HEALED, 
FAILED (with suggestion) or FAILED; no source file has been modified. 
Table 3.12: Use case UC-02: Review and approve or reject a repair PR 
Use case ID UC-02 
Name Review and approve / reject repair PR 
Primary actor QA Engineer (reviewer with write permission) 
Preconditions M9 has opened a PR on a bot branch; sandbox re-run passed; the PR is linked to a 
decision record. 
Main flow 1. Reviewer opens the heal in the dashboard or the PR in GitHub. 2. System shows 
original and proposed locator, failure class, gate results, confidence, critic verdict, 
redacted before/after crops and diff. 3. Reviewer checks that the element and the test 
intent are unchanged. 4. Reviewer approves; required status checks pass. 5. Reviewer 
merges. 6. System records the review, marks the decision "approved" and updates the 
fingerprint baseline. 
Alternative flows 3a. Reviewer edits the proposed locator in the PR before approving; the edited version 
is re-tested by CI. 4a. Reviewer rejects: PR closed; candidate blacklisted; reason 
recorded. 
Exception flows 4b. Status check fails after rebase: merge blocked by branch protection; PR returned to 
reviewer. E1. Reviewer lacks permission: GitHub blocks approval. 
Postconditions The PR is merged by a human or closed; the review outcome is stored in M8. 
Table 3.13: Use case UC-03: Classify API contract failure (extension E2) 
Use case ID UC-03 
Name Classify API contract failure 
Primary actor CI/CD Pipeline; secondary: API Owner 
Preconditions E2 enabled (gate G3 passed); baseline and current OpenAPI specifications retrievable. 
Main flow 1. An API test fails on status code or response schema. 2. E2 validates the response 
against the current specification. 3. E2 diffs current and baseline specifications. 4. E2

<!-- Page 52 -->

Use case ID UC-03 
checks the approval record (version bump and approved change label). 5. E2 classifies 
the failure and reports it with evidence to the API owner and QA engineer. 
Alternative flows 5a. Intended change: E2 proposes updated test data or expectations as an A2 
suggestion; a human applies it. 
Exception flows 2a. Specification unavailable or invalid: failure recorded as C6 with reason. 5b. 
Classification ambiguous: reported as "needs review"; no suggestion. 
Postconditions The API test remains failed until a human acts; no expectation is changed 
automatically. 
## 3.7 Proposed System: Analysis, Modelling and Design 
Only the diagrams that add information are included. A collaboration diagram is omitted 
because the sequence diagram (Figure 3.8) already shows the same interactions in time order. 
### 3.7.1 Activity diagram 
Figure 3.5 details the validation and decision activities (M6, M6c, M7) with swimlanes. 
 
Figure 3.5: Activity diagram of candidate validation and healing decision 
### 3.7.2 Statechart diagram 
Figure 3.6 shows the life cycle of a heal request from detection to merge, rejection or failure.

<!-- Page 53 -->

Figure 3.6: Statechart diagram of a heal request 
### 3.7.3 Class diagram 
Figure 3.7 shows the main classes. CandidateGenerator is an interface implemented by the 
Similarity Matcher and the LLM Generator, so further generators (for example E1) can be 
added without changing the validator or decision engine.

<!-- Page 54 -->

Figure 3.7: Class diagram of the core framework 
### 3.7.4 Sequence diagram 
Figure 3.8 shows UC-01 followed by the asynchronous repair and review steps.

<!-- Page 55 -->

Figure 3.8: Sequence diagram of a run-time heal and repair PR 
### 3.7.5 Component diagram 
 
Figure 3.9: Component diagram 
Figure 3.9 shows that the test runner talks to the healing service through one REST interface 
(/heal) and that all LLM calls pass through the LLM Gateway.

<!-- Page 56 -->

### 3.7.6 Deployment diagram 
 
Figure 3.10: Deployment diagram 
In CI (Figure 3.10), the browser and PetClinic run as containers on the GitHub -hosted runner. 
The healing service, dashboard and PostgreSQL run on a persistent team server or small VM, 
so fingerprints and audit data survive between runs. During local development all components 
run on one laptop with Docker Compose. 
### 3.7.7 ER diagram and sample schema 
Figure 3.11 shows the data model. audit_log is linked to other entities through (entity_type, 
entity_id) rather than a foreign key, so that it can record events for every table. Listing  3.1 
gives part of the schema.

<!-- Page 57 -->

Figure 3.11: Entity-relationship diagram 
Listing 3.1: Sample PostgreSQL schema (part) 
CREATE TABLE test_step ( 
  step_key    VARCHAR PRIMARY KEY,          -- e.g. "tests/test_owner.py::test_add_owne
r#7" 
  test_id     VARCHAR NOT NULL, 
  step_index  INT     NOT NULL, 
  locator     TEXT    NOT NULL,             -- e.g. "id=save-owner" 
  action      VARCHAR NOT NULL              -- click | type | select | read 
); 
CREATE TABLE element_fingerprint ( 
  fp_id       UUID PRIMARY KEY, 
  step_key    VARCHAR NOT NULL REFERENCES test_step(step_key), 
  attributes  JSONB   NOT NULL,             -- tag, id, name, classes, text, data-* 
  role        VARCHAR, acc_name TEXT, xpath TEXT, bbox JSONB, 
  app_version VARCHAR NOT NULL, 
  valid_from  TIMESTAMP NOT NULL DEFAULT now() 
); 
CREATE TABLE heal_decision ( 
  decision_id      UUID PRIMARY KEY, 
  failure_id       UUID NOT NULL REFERENCES failure_event(failure_id), 
  chosen_candidate UUID REFERENCES candidate(candidate_id),  -- NULL for FAIL_* 
  kind        VARCHAR NOT NULL CHECK (kind IN 
              ('HEAL','SUGGEST','FAIL_DEFECT','FAIL_UNCERTAIN')), 
  confidence  NUMERIC(4,3), 
  policy_version VARCHAR NOT NULL, 
  latency_ms  INT 
);

<!-- Page 58 -->

## 3.8 Data Flow Diagrams 
The DFDs use rectangles for external entities, numbered rounded boxes for processes and two-
part boxes for data stores. Figure  3.12 is the context diagram, Figure  3.13 decomposes the 
system into seven processes, and Figures  3.14 and 3.15 decompose processe s 4.0 and 6.0 to 
Level 2. 
 
Figure 3.12: DFD Level 0 (context diagram) 
 
Figure 3.13: DFD Level 1

<!-- Page 59 -->

Figure 3.14: DFD Level 2: process 4.0 Generate and Validate Candidates

<!-- Page 60 -->

Figure 3.15: DFD Level 2: process 6.0 Create Repair Pull Request 
Table 3.14 explains the entities, processes and data stores used in the DFDs. 
Table 3.14: DFD elements 
Type Name Description 
External entity CI/CD Pipeline Triggers runs; receives results, status check and report. 
External entity Application Under Test Receives WebDriver commands and API requests; returns 
page state and responses. 
External entity LLM Service Receives redacted prompts; returns candidates and verdicts. 
External entity Code Repository Provides test source and specifications; receives bot 
branches and PRs. 
External entity QA Engineer Configures policy; reviews and approves or rejects repairs; 
merges PRs. 
Process 1.0-7.0 See Figure 3.13 Execute and monitor; classify; collect and redact; generate 
and validate; decide; create PR; review, report and audit. 
Process 4.1-4.7 See Figure 3.14 Prune DOM and build pool; similarity scores; LLM 
candidates; hard gates; replay; critic; assemble evidence. 
Process 6.1-6.5 See Figure 3.15 Locate definition; patch; sandbox run; open PR; route to 
manual fix. 
Data store D1 Element Fingerprint Store Last-known-good fingerprints per step and app version 
(M4). 
Data store D2 Run and Failure Log Step results and failure classes. 
Data store D3 Heal Decision and Audit 
Store 
Candidates, gates, decisions, PRs, reviews (M8). 
Data store D4 Policy Configuration Thresholds, weights, autonomy settings, caps.

<!-- Page 61 -->

## 3.9 Architectural View 
VeriHeal combines four architectural styles, each chosen for a specific reason (Figure 3.16). 
 
Figure 3.16: Layered architectural view 
1. Layered architecture (overall). Five layers (integration, healing pipeline, intelligence 
services, repair and governance, data) with dependencies pointing downwards. This 
separates the parts that change for different reasons: the LLM provider can change 
without affecting the pipeline, a nd the test framework adapter can change without 
affecting decisions. 
2. Interceptor / plug -in (integration layer).  The HealingDriver wraps the WebDriver, 
and a pytest plug-in hooks into test reporting. Existing tests need only a fixture change, 
which keeps adoption cost low. 
3. Pipe-and-filter (healing pipeline).  Classification, context collection, matching, 
validation and decision are filters with typed inputs and outputs. Each filter can be tested 
alone and replaced (for example M5a versions in ablation runs). 
4. Client-server with a gateway (intelligence services).  All LLM calls go through one 
gateway that enforces redaction checks, JSON schemas, timeouts and cost limits. If 
MCP is adopted, the gateway acts as the MCP host and connects to allow -listed tool 
servers [25].

<!-- Page 62 -->

5. Asynchronous jobs (repair). PR creation runs as a separate CI job so that it does not 
delay the test run. 
Agent interaction. The Generator and Critic do not talk to each other directly. M6 builds an 
evidence summary from execution results and passes it to the Critic; this avoids the Critic 
simply agreeing with the Generator's argument. Service communication. The plug-in calls the 
healing service over HTTP (REST/JSON); the service uses SQL for storage and HTTPS for 
LLM and GitHub APIs. Data management. Fingerprints and decisions are in PostgreSQL; 
screenshots and DOM snapshots are stored redacted as artifacts with a retention period; only 
hashes are kept after expiry. Repository integration. Only M9 writes to the repository, only to 
bot branches, using a dedicated token. Deployment. See Figure 3.10. 
### 3.9.1 Security and privacy architecture 
Table 3.15: Security and privacy controls 
Concern Control 
Screenshot and DOM 
privacy 
Redaction before storage or transmission: input value attributes removed; text 
matching e-mail, phone, card-like and token patterns masked; elements marked 
data-sensitive blanked in DOM and blurred in screenshots. Only the 
pruned DOM region is sent to the LLM. 
API payload protection E2 sends only schema paths and types to an LLM, never payload values. 
PII and secret masking Pattern- and configuration-based masking (above) plus a secret scanner on 
prompts in the LLM Gateway; prompts failing the check are not sent (logged as 
blocked). Addresses sensitive-information disclosure risk [35]. 
Prompt injection Page text is untrusted data [34]: it is placed in clearly delimited data fields; 
outputs must match a JSON schema; agents have no tool that can change state 
outside the sandbox; every proposed locator is verified by execution (addresses 
prompt injection and excessive agency [35]). 
Credential management LLM keys and the bot token are stored as CI secrets / environment variables, 
never in code or logs; keys rotated at the end of each phase. 
Repository access 
control 
Dedicated bot identity; token restricted to the single test repository with only the 
permissions needed to push branches and open PRs; branch protection requires an 
approving review and passing checks [48]; auto-merge disabled. 
Least privilege Healing service database user has insert-only rights on audit_log; dashboard 
reviewers authenticated; read-only role for analysts. 
Sandboxed execution Replays (H5) run in a new browser session; repair re-runs in an ephemeral CI 
container with network access limited to the application under test. 
Audit logs Append-only table with payload hashes; every LLM call logged with model, 
prompt hash, token counts and latency. 
Secure communication HTTPS/TLS for LLM, GitHub and dashboard traffic; database not exposed 
publicly. 
Data retention Redacted artifacts deleted after a configured period (default 30 days); provider 
data-retention terms reviewed before selecting an LLM.

<!-- Page 63 -->

## 3.10 Algorithms and Methodology 
### 3.10.1 Similarity model 
Let 𝐹 be the stored fingerprint and 𝑣 a candidate element with the same attributes extracted. 
For each attribute 𝑘 with weight 𝑤𝑘 and similarity function 𝑠𝑘  in [0,1], and with 𝟏[𝐹𝑘] equal to 
1 when the attribute was present in the fingerprint, the similarity score is  
𝑆(𝑣)= ∑ 𝑤𝑘𝑘  𝟏[𝐹𝑘] 𝑠𝑘(𝐹𝑘,𝑣𝑘) ∑ 𝑤𝑘𝑘  𝟏[𝐹𝑘] . 
 (3.1) 
Set-valued attributes (class lists, tokenised text) use the Jaccard index  
𝑠𝐽(𝐴,𝐵)= |𝐴 intersect 𝐵| |𝐴 U 𝐵|,  𝑠𝐽(∅,∅)=1, 
 (3.2) 
string attributes (id, name, accessible name, XPath) use normalised edit similarity  
𝑠𝐸(𝑎,𝑏)=1− lev(𝑎,𝑏) max(|𝑎|,|𝑏|), 
 (3.3) 
where lev is the Levenshtein edit distance, and position uses the distance between bounding -
box centres 𝐩:  
𝑠𝐿(𝐹,𝑣)=max(0, 1−∥𝐩𝐹−𝐩𝑣 ∥2 𝑑𝑚𝑎𝑥 ). 
 (3.4) 
Role uses an exact -match or compatibility table (for example button is compatible with an 
element having role="button"). The decisiveness of the ranking is measured by the margin 
between the best and second-best candidates:  
𝛥=𝑆(𝑣(1))−𝑆(𝑣(2)). 
 (3.5)

<!-- Page 64 -->

Table 3.16: Fingerprint attributes, similarity functions and initial weights 
Attribute Function Initial 𝑤𝑘 Rationale 
data-* test id exact (1/0) 1.5 Intended to be stable when present [11] 
id 𝑠𝐸 1.5 Strong identifier, but renamed often [3] 
name 𝑠𝐸 1.2 High robustness priority in ROBULA+ [9] 
role compatibility 1.5 Semantic type; also a hard gate (H4) 
accessible name 𝑠𝐸 1.5 What the user sees/hears; also in H4 
visible text 𝑠𝐽 (tokens) 1.0 Often stable; may change with wording 
tag exact 0.5 Weak alone 
class list 𝑠𝐽 0.5 Changes with styling 
XPath (absolute) 𝑠𝐸 0.5 Breaks under restructuring 
neighbour texts 𝑠𝐽 1.0 Context near the element (cf. contextual clues [38]) 
bounding-box centre 𝑠𝐿 0.8 Layout usually changes less than markup 
Table 3.16 lists, for each attribute, the similarity function (Jaccard, Eq.  3.2; edit similarity, 
Eq. 3.3; position, Eq.  3.4) and its initial weight. The initial weights are design choices, not 
measured values. They will be tuned on the calibration split o f the benchmark only (never on 
the evaluation split). 
### 3.10.2 Hard gates and confidence 
Each candidate 𝑘 is eligible only if all applicable gates hold:  
𝐺(𝑘)=ℎ1(𝑘) ℎ2(𝑘) ℎ3(𝑘) ℎ4(𝑘) in {0,1}, 
 (3.6) 
where ℎ1: the locator is valid and resolves; ℎ2: it resolves to exactly one element; ℎ3: the 
element is displayed and enabled (and editable for typing actions); ℎ4: the role is compatible 
with 𝐹 and the accessible -name similarity is at least 𝜏𝑛𝑎𝑚𝑒. Eq. 3.6 therefore acts as a filter 
before any scoring decision. The replay gate ℎ5 is evaluated on the best eligible candidate only, 
because it is expensive. Candidates are ranked by Eq.  3.1, and the margin of Eq.  3.5 decides 
whether the LLM Generator is called. 
For an eligible candidate the evidence vector is 𝐞=(𝑆,𝑠𝑛𝑎𝑚𝑒,𝛥,𝑎𝑔𝑒𝑛,𝑟𝑐𝑟𝑖𝑡), where 𝑎𝑔𝑒𝑛 in 
{0,1} indicates that the deterministic matcher and the Generator agree on the element, and 
𝑟𝑐𝑟𝑖𝑡  in {0,0.5,1} encodes the critic verdict (reject, uncertain, accept). The confidence is a 
logistic model

<!-- Page 65 -->

𝑐=𝜎(𝛽0+𝛃⊤𝐞),  𝜎(𝑥)= 1 1+𝑒−𝑥, 
 (3.7) 
whose coefficients are fitted on the calibration split so that 𝑐 approximates the probability that 
the heal is correct. In P1, before enough labelled data exists, a fixed weighted average of the 
same features is used. Because modern models are often poorly calibrated  [49], calibration is 
checked on held-out data, not assumed. 
### 3.10.3 Threshold calibration 
The run-time threshold 𝜏𝐴 is chosen as the smallest value for which the false -heal rate on the 
calibration split is acceptably low with statistical confidence:  
𝜏𝐴 =min{𝜏 : 𝑈0.95(FHR̂(𝜏),𝑛(𝜏))<=𝜀,  𝑛(𝜏)>=𝑛𝑚𝑖𝑛}, 
 (3.8) 
where 𝑛(𝜏) is the number of heals with 𝑐>=𝜏, 𝜀 is the false-heal target (Table 3.6) and 𝑈0.95 is 
the upper bound of the Wilson score interval [50] for a proportion 𝑝̂ observed in 𝑛 trials:  
𝑈(𝑝̂,𝑛)=
𝑝̂+𝑧2 2𝑛+𝑧√𝑝̂(1−𝑝̂) 𝑛 + 𝑧2 4𝑛2
1+𝑧2 𝑛 ,  𝑧=1.96. 
 (3.9) 
𝜏𝑆 is chosen similarly with a looser target, because A2 suggestions are always reviewed. 
### 3.10.4 Latency model 
The healing latency of one failure is  
𝐿=𝑡𝑐𝑙𝑠+𝑡𝑐𝑡𝑥+𝑡𝑚𝑎𝑡𝑐ℎ+𝟏𝐿𝐿𝑀 𝑡𝑔𝑒𝑛+𝑡𝑔𝑎𝑡𝑒𝑠+𝑡𝑟𝑒𝑝𝑙𝑎𝑦+𝟏𝑐𝑟𝑖𝑡 𝑡𝑐𝑟𝑖𝑡, 
 (3.10) 
and the run-level constraint is ∑ 𝐿𝑓𝑓 <=𝐵𝐶𝐼, where 𝐵𝐶𝐼 is the time budget allowed for healing in 
one CI run. Each term is logged separately in M8.

<!-- Page 66 -->

### 3.10.5 Algorithms 
Algorithms 3.1-3.9 give the pseudocode of the main processes: failure detection and 
classification (Algorithm  3.1), context extraction and redaction (Algorithm  3.2), fingerprint 
capture for element identification (Algorithm  3.3), similarity -based locator r ecovery 
(Algorithm 3.4), LLM candidate generation (Algorithm  3.5), independent validation 
(Algorithm 3.6), confidence scoring and decision (Algorithm  3.7), threshold calibration 
(Algorithm 3.8) and pull request generation (Algorithm 3.9). 
Algorithm 3.1: Failure detection and classification (M1, M2) 
Input : step s (locator l, action a), exception x, driver d 
Output: failure class in {C1..C7} 
if x is WebDriverException indicating crash/session loss then return C7 
if x is AssertionError then return C4 
if last navigation returned HTTP status >= 400 or URL not in s.expected_urls then retur
n C5 
if x is NoSuchElement or Timeout on lookup: 
    wait until document.readyState == "complete" and no pending requests (max T_ext) 
    m <- d.find_elements(l) 
    if |m| == 1 then return C3            // element appeared late: timing / flaky 
    if |m| == 0 then return C1            // not found 
if s.expects_unique and |d.find_elements(l)| > 1 then return C2   // ambiguous 
return C7 
Algorithm 3.2: Context extraction and redaction (M3) 
Input : driver d, policy P 
Output: redacted context ctx 
dom  <- d.page_source 
ax   <- CDP Accessibility.getFullAXTree        // fallback: JS role/name for candidates 
img  <- d.screenshot() 
boxes<- JS: bounding boxes of visible elements 
for each element e in dom: 
    remove attribute "value" from input/textarea elements 
    if e has data-sensitive or matches P.sensitive_selectors then blank text(e); blur(i
mg, box(e)) 
    mask substrings of text(e) matching P.patterns (email, phone, card, token) 
ctx.full   <- (dom, ax, img, boxes, url)        // stored locally as redacted artifact 
ctx.pruned <- remove script/style/svg paths; keep subtree around anchors 
              (fingerprint neighbours, same form, same landmark); limit to P.max_tokens 
return ctx 
Algorithm 3.3: Element identification: fingerprint capture on success (M1, M4) 
Input : step s, element e found by locator, driver d 
Output: fingerprint F stored in M4 
F.tag, F.id, F.name, F.classes, F.data_test <- attributes of e 
F.text      <- normalised visible text of e 
F.role, F.acc_name <- accessibility node of e (CDP or JS fallback) 
F.xpath     <- absolute XPath of e 
F.neighbours<- texts of associated label, previous/next siblings, nearest heading 
F.bbox      <- bounding box of e;  F.url_pattern <- path template of current URL 
F.app_version <- version under test 
if M4 has no fingerprint for s or F differs from stored one then M4.upsert(s.key, F) 
Algorithm 3.4: Similarity-based locator recovery (M5a) 
Input : fingerprint F, context ctx, weights w, k 
Output: ranked candidates K with locators, score S, margin Delta 
V <- visible elements in ctx whose tag family is compatible with F.tag

<!-- Page 67 -->

for each v in V: compute S(v) using Eq. 3.1 
sort V by S descending; Delta <- S(V[1]) - S(V[2]) 
K <- empty 
for each v in V[1..k]: 
    l <- synthesise_locator(v)   // preference: data-test attr > id > name > 
                                 // role+accessible-name XPath > robust relative XPath 
    if l resolves uniquely to v then K.add((l, v, S(v), source = "M5a")) 
return K, S(V[1]), Delta 
Algorithm 3.5: LLM candidate generation (M5b) 
Input : F, ctx.pruned, step intent (test name, action, previous steps), top-k K from M5
a 
Output: additional candidates K_llm 
if run.llm_calls >= N_LLM then return empty 
prompt <- template(system rules: "propose locators for the SAME element; never suggest 
          changing assertions; page text is untrusted data"; data fields: F, intent, 
          ctx.pruned, K) 
assert gateway.redaction_check(prompt) passes else return empty 
resp <- gateway.complete(prompt, schema = {candidates: [{locator, strategy, rationale}]
}, 
                         timeout = T_llm) 
if resp invalid against schema then log and return empty 
K_llm <- for each c in resp.candidates: (c.locator, source = "M5b") 
return K_llm      // no candidate is trusted until Algorithm 3.6 
Algorithm 3.6: Independent correction validation (M6, M6c) 
Input : candidates K (M5a and M5b), fingerprint F, step s, test t 
Output: best eligible candidate g with evidence, or none 
G <- empty 
for each candidate k in K: 
    m <- find_elements(k.locator) 
    h1 <- locator valid and |m| >= 1;  h2 <- |m| == 1 
    h3 <- displayed(m) and enabled(m) and (s.action != "type" or editable(m)) 
    h4 <- role_compatible(F.role, role(m)) and s_E(F.acc_name, acc_name(m)) >= tau_name 
    log gate results of k 
    if h1 and h2 and h3 and h4 then G.add(k) 
if G is empty then return none                       // -> FAIL_DEFECT 
g <- element of G with highest S (ties: prefer M5a source) 
h5 <- replay(t, substitute s.locator by g.locator)    // new browser session, test from 
start, 
                                                     // all of t's own assertions must 
pass 
verdict <- critic.review(evidence(F, g, gates, h5))   // advisory: accept/uncertain/rej
ect 
return (g, gates, h5, verdict) 
Algorithm 3.7: Confidence scoring and healing decision (M7) 
Input : result of Algorithm 3.6, policy P (tau_A, tau_S, downgrade rules) 
Output: decision in {HEAL, SUGGEST, FAIL_DEFECT, FAIL_UNCERTAIN} 
if result is none then return FAIL_DEFECT 
(g, gates, h5, verdict) <- result 
c <- confidence(e(g))                                 // Eq. 3.7 
if verdict == reject then return FAIL_UNCERTAIN       // critic veto 
if h5 == fail then return FAIL_UNCERTAIN              // behaviour differs: possible de
fect 
if c >= P.tau_A and not any_downgrade_rule(g) then return HEAL     // A3 
if c >= P.tau_S then return SUGGEST                                 // A2 
return FAIL_UNCERTAIN 
// every return is preceded by M8.log(decision, c, policy version, latencies) 
Algorithm 3.8: Threshold calibration (offline) 
Input : calibration records R = {(c_i, correct_i)}, target eps, n_min 
Output: tau_A 
for tau in sorted distinct values of c_i (ascending): 
    H <- {i in R : c_i >= tau};  n <- |H|

<!-- Page 68 -->

if n < n_min then break 
    p <- (number of i in H with correct_i = false) / n 
    if WilsonUpper(p, n) <= eps then return tau        // Eq. 3.9 
return +infinity                                       // A3 disabled: only A2 allowed 
Algorithm 3.9: Pull request generation (M9) 
Input : decision d (HEAL or SUGGEST) with old locator (by, value) and new locator l 
Output: PR id or manual-fix task 
S <- AST search in page-object modules for assignments NAME = (By.<by>, "<value>") 
if |S| != 1 then create manual-fix task with reason; return 
diff <- replace only the locator tuple at S[0] by l (formatting preserved) 
branch <- "veriheal/heal-" + d.id ; commit diff to branch with bot identity 
T <- tests that import the module of S[0] 
r <- run T in ephemeral CI sandbox 
if r has any failure then create manual-fix task with r; return 
pr <- open PR(branch -> main, title, body = evidence(d), labels = ["veriheal"], 
              auto_merge = false) 
M8.log(pr); return pr.id 
## 3.11 UI/UX Design 
The interface is planned as a small web dashboard (M10). Figures 3.17-3.19 are design mock-
ups produced for this report; they are not screenshots of an implemented system, and all values 
in them are placeholders. 
 
Figure 3.17: Design mock-up: dashboard with test execution monitor and execution history

<!-- Page 69 -->

Figure 3.18: Design mock-up: failure report, healing suggestion, confidence and approval interface 
 
Figure 3.19: Design mock-up: audit log 
Design decisions.  (1) PASSED -HEALED, suggested and probable -defect outcomes use 
distinct labels as well as colours, so status is never shown by colour alone. (2) The review screen 
puts the evidence (gates, replay, critic, crops, diff) next to the approve/reject buttons so that a 
decision can be made on one screen (NFR -12). (3) The reject action states its consequence 
(candidate blacklisted). (4) The audit log is filterable by date, test, decision type and actor and

<!-- Page 70 -->

can be exported for analysis. (5) Merge is possible only through GitHub's protected -branch 
rules; the dashboard does not bypass them.
