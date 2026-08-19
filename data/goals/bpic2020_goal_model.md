# BPIC 2020 Goal Model (Step G) — Travel Permit Data

**Status:** **Draft**, version 1.0, 2026-08-19. Authored for pipeline-development purposes, in the same
spirit as `rtfm_goal_model.md` v1.0 and `sepsis_goal_model.md` v1.0 — not yet reviewed by a TU/e travel-
or finance-administration practitioner. §8 states exactly what is, and is not, already grounded.
**Target log:** `data/logs/bpic2020_permit.xes.gz` — the BPI Challenge 2020 Travel Permit Data event log
(van Dongen, 2020), 7,065 cases (travel permits) · 86,581 events · 51 activity labels · 1,478 variants —
counts verified directly against the log file itself (`pm4py.read_xes`, direct scan, 2026-08-19).
**Tool-notation copy:** [`bpic2020_goal_model.jucm`](bpic2020_goal_model.jucm) — the full model
serialized as jUCMNav's native URN/GRL XMI format: §2's actor, §3–§4's goals/tasks and AND/OR
decomposition links, §5's softgoals and contribution links, and §6's three indicators (as
`grl.ecore`'s `kpimodel:Indicator`, each carrying its target/threshold/worst as a `KPIEvalValueSet`
inside an `EvaluationStrategy`, grouped under two `IndicatorGroup`s — "Time" for the reimbursement-delay
KPI, "Control" for the overspend/rejection-rate KPIs), generated against the same `grl.ecore`/
`urncore.ecore`/`urn.ecore` metamodel definitions used for `rtfm_goal_model.jucm`, and checked for XML
well-formedness and referential integrity of every ID — but not round-trip verified by opening it in
jUCMNav itself (Eclipse RCP is not available in this environment). Per §4's own caveat, TAppr's internal
approval-chain steps are **not** further decomposed into separate task nodes in this `.jucm` (unlike
RTFM's TB) — §8 explains why: the Budget Owner/Supervisor merge condition and Pre-Approver's trigger are
undocumented, so this artifact declares TAppr a single leaf task rather than asserting a sub-structure
no source supports.
**Provenance:** The approval-chain structure in §3–§4 is grounded in the official BPI Challenge 2020
process description (ICPM, 2020; corroborated by Klein et al., 2020, who built and validated a reference
BPMN model against that same text), which names Eindhoven University of Technology (TU/e) as the source
organization and describes the routing order (Administration → Budget Owner → Supervisor, with an
optional Director step) and the domestic/international permit distinction. The same source explicitly
flags a gap this model inherits rather than papers over: **PRE_APPROVER's role and trigger condition are
not documented anywhere in the official narrative** (Klein et al., 2020, §12) — see §8. The G4/G5 cost-
settlement split (Declaration vs. Request For Payment) and §6's overspend indicator are grounded directly
in this log's own schema (`case:Overspent`) and the official description's statement that RFPs are also
how non-TU/e-employee trip costs are claimed, not in a separate cited source. The actor structure and
softgoal contribution values (§2, §5) are this project's own construction, the same kind of gap
`rtfm_goal_model.md` §8 and `sepsis_goal_model.md` §8 disclose for their own non-KPI content.

---

## 1. Purpose and scope

This model declares what the travel-permit authorization and cost-settlement process is *for*,
independently of the log, so that its OR-decomposition can serve as the taxonomy axis for intent-guided
variant categorization (Step 5a) — the same role `rtfm_goal_model.md` and `sepsis_goal_model.md` play for
their own logs. It covers the lifecycle of a single travel permit at TU Eindhoven (ICPM, 2020; Klein et
al., 2020): submission, routing through an approval chain, the trip itself, and the declarations and/or
requests for payment through which the trip's costs are eventually paid. This log — one of five
correlated BPIC 2020 sub-logs, the only one staged in this project (`project/OVERVIEW.md`, "Data
sources") — is scoped to cases that have a travel permit; per the official description, domestic trips
do not require one and so are, by construction, under-represented or absent here relative to the full
BPIC 2020 collection (see §8). It does not model control flow, timing, or exceptions beyond what a
goal-task decomposition requires — that is the job of the per-category process model discovered
downstream (Step 7), not of this artifact.

## 2. Actors

| Actor | Role | Type |
|---|---|---|
| Travel & Finance Administration (TU/e) | Receives, routes for approval, tracks, and pays travel permits and the declarations/payment requests arising from them | Primary |
| Employee | Submits the permit, undertakes the trip, and files the declarations and/or requests for payment that settle its costs | External |
| Supervisor | Line-manager approver; issues the chain's final approval unless a Director step applies; merges with the Budget Owner step when the same person holds both roles (ICPM, 2020) | External |
| Budget Owner | Approves against the relevant project or cost-center budget | External |
| Pre-Approver | An approval role observed directly in the log (`org:role = PRE_APPROVER`, 627 of 7,065 cases); its trigger condition is undocumented in any source found for this model (§8) | External |
| Director | Final approver for a minority of permits (676 of 6,960 approved permits reach `Permit FINAL_APPROVED by DIRECTOR` rather than `...by SUPERVISOR`, direct scan) | External |

Only the Travel & Finance Administration owns goals in this model — the ADMINISTRATION role that appears
directly in the log's own `org:role` field — while Employee and the approval-chain roles are external
actors it depends on or routes work through, the same asymmetry `rtfm_goal_model.md` §2 and
`sepsis_goal_model.md` §2 draw for their own external actors.

## 3. Goal–task decomposition

```mermaid
flowchart TD
    subgraph ACTOR["Actor: Travel &amp; Finance Administration"]
        G0("G0: Every submitted permit reaches a<br/>documented authorization outcome, and every<br/>cost from an approved trip is paid")
        G1("G1: Permit is submitted<br/>for authorization")
        G2("G2: Permit reaches a<br/>closed resolution")
        G3("G3: Permit is approved and its<br/>trip/costs are settled")
        G4("G4: Trip is undertaken and<br/>its costs are settled")
        G5("G5: Costs arising from the trip<br/>are declared or requested, and paid")
        T1{{"T1: Permit SUBMITTED<br/>by EMPLOYEE"}}
        TR{{"TR: Permit is rejected<br/>and not further pursued"}}
        TAppr{{"TAppr: Permit is approved<br/>through the required chain"}}
        TTrip{{"TTrip: Start trip &#8594; End trip"}}
        TDecl{{"TDecl: Declaration submitted,<br/>approved, and paid"}}
        TRFP{{"TRFP: Request For Payment<br/>submitted, approved, and paid"}}
    end
    SG1(["SG1: Minimize approval-chain<br/>overhead"])
    SG2(["SG2: Maintain budgetary<br/>control"])
    SG3(["SG3: Minimize employee<br/>reimbursement delay"])

    G0 -->|AND| G1
    G0 -->|AND| G2
    G1 -->|AND| T1
    G2 -->|OR| TR
    G2 -->|OR| G3
    G3 -->|AND| TAppr
    G3 -->|AND| G4
    G4 -->|AND| TTrip
    G4 -->|AND| G5
    G5 -->|OR| TDecl
    G5 -->|OR| TRFP

    TAppr -.->|"SomeNeg -25"| SG1
    TAppr -.->|"Help +50"| SG2
    TR -.->|"Help +50"| SG2
    TR -.->|"SomeNeg -25"| SG1
    TDecl -.->|"Help +50"| SG3
    TRFP -.->|"Help +50"| SG3

    classDef goal fill:#e8f0fe,stroke:#3367d6,stroke-width:2px
    classDef task fill:#f1f3f4,stroke:#5f6368,stroke-width:2px
    classDef softgoal fill:#fff4e5,stroke:#e8710a,stroke-width:2px
    class G0,G1,G2,G3,G4,G5 goal
    class T1,TR,TAppr,TTrip,TDecl,TRFP task
    class SG1,SG2,SG3 softgoal
```

**Reading the decomposition.** G0 requires both submission (G1) and a closed resolution (G2) — a permit
is not satisfied merely by existing in the system without ever reaching a rejection or an approval
outcome. G2 is OR, not XOR: rejection (TR) and approval-and-settlement (G3) are the two closing
alternatives, and — per the official description's own account of rejection ("either the employee
resubmits the request, or the employee also [withdraws] it," ICPM, 2020) — TR is not necessarily
terminal: direct scan finds 319 of 7,065 permits (4.5%) rejected at least once before eventually reaching
`FINAL_APPROVED`, i.e., TR followed by a resubmission that satisfies G3 instead, and 88 permits (1.2%)
rejected with no later approval. G3→G4→G5 cascades the same way RTFM's G3→G4 does
(`rtfm_goal_model.md` §3): an approved permit (TAppr) is not itself the end state, because its whole
point is the trip and cost settlement that follow. G5 is OR, and deliberately inclusive rather than
exclusive — 1,157 of 7,065 permits (16.4%, direct scan) carry *both* at least one Declaration and at
least one Request For Payment, consistent with the official description's statement that RFPs cover
costs unrelated to a specific trip (e.g., project hardware) in addition to being the reimbursement
mechanism for non-TU/e employees who cannot file a declaration (ICPM, 2020) — the two settlement channels
are not mutually exclusive alternatives for the same cost, matching how `sepsis_goal_model.md` §3
describes its own G4 discharge alternatives as non-exclusive by the log's own evidence.

## 4. Decomposition table

| ID | Type | Label | Operator | Children |
|---|---|---|---|---|
| G0 | Goal | Every submitted permit reaches a documented authorization outcome, and every cost from an approved trip is paid | AND | G1, G2 |
| G1 | Goal | Permit is submitted for authorization | AND | T1 |
| G2 | Goal | Permit reaches a closed resolution | OR | TR, G3 |
| G3 | Goal | Permit is approved and its trip/costs are settled | AND | TAppr, G4 |
| G4 | Goal | Trip is undertaken and its costs are settled | AND | TTrip, G5 |
| G5 | Goal | Costs arising from the trip are declared or requested, and paid | OR | TDecl, TRFP |
| T1 | Task | Permit SUBMITTED by EMPLOYEE | leaf | — |
| TR | Task | Permit is rejected and not further pursued | leaf, repeatable (resubmission after rejection observed in 319 of 7,065 cases) | — |
| TAppr | Task | Permit is approved through the required chain (Administration → [Budget Owner] → Supervisor or Director final approval) | AND (internal steps) | administration approval, budget-owner approval (merged with supervisor's step if the same person holds both roles), supervisor or director final approval |
| TTrip | Task | Start trip → End trip | leaf | — |
| TDecl | Task | Declaration submitted, approved through the same chain, and paid | leaf, repeatable (up to 17 declarations observed per permit; present in 5,608 of 7,065 cases) | — |
| TRFP | Task | Request For Payment submitted, approved through the same chain, and paid | leaf, repeatable (up to 15 RFPs observed per permit; present in 1,325 of 7,065 cases) | — |

G1 has a single child (T1) rather than being folded directly into G0, kept as its own goal for structural
symmetry with RTFM's and Sepsis's own "issuance" goals and because 17 of 7,065 permits (0.2%, direct
scan) are preceded by an optional `Permit SAVED by EMPLOYEE` draft step not otherwise represented in the
decomposition.

TAppr's internal AND is a composite in the same sense `rtfm_goal_model.md` §4 declares TB (the
Prefecture-appeal task) a composite of internal steps rather than a single atomic activity: the official
description states the routing order explicitly (Administration, then Budget Owner, then Supervisor,
with Director only "in some cases," ICPM, 2020) but does not state the condition under which the Director
step applies, nor — critically — does it mention Pre-Approver at all (§8). This model does not invent
those conditions; TAppr is declared satisfied by reaching either `Permit FINAL_APPROVED by SUPERVISOR`
(6,286 of 6,960 approved permits) or `Permit FINAL_APPROVED by DIRECTOR` (676), without asserting *why*
one path is taken over the other.

## 5. Contribution links (softgoals)

| Source | Target | Value | Rationale |
|---|---|---|---|
| TAppr (approval chain) | SG1 (approval overhead) | SomeNegative (-25) | A multi-step routing chain (Administration, Budget Owner, Supervisor, occasionally Director) adds processing steps relative to a single-approver process |
| TAppr (approval chain) | SG2 (budgetary control) | Help (+50) | The chain is itself the control mechanism that checks a request against budget and organizational authority before it is approved |
| TR (rejection) | SG2 (budgetary control) | Help (+50) | Rejecting a non-compliant or over-budget request is the control mechanism working as intended |
| TR (rejection) | SG1 (approval overhead) | SomeNegative (-25) | A rejection-and-resubmission cycle (observed in 319 of 7,065 cases, §3) adds processing steps beyond a single pass through the chain |
| TDecl (Declaration) | SG3 (reimbursement delay) | Help (+50) | Enables eventual `Payment Handled`, but does not guarantee promptness — see §6's own throughput figures |
| TRFP (Request For Payment) | SG3 (reimbursement delay) | Help (+50) | Same relationship as TDecl, for the second settlement channel |

Qualitative scale follows the GRL/URN standard (Make = 100, Help = 50, SomePositive = 25, Unknown = 0,
SomeNegative = -25, Hurt = -50, Break = -100), as used in the IMS example (Amyot et al., 2022) and reused
by `rtfm_goal_model.md` §5, `sepsis_goal_model.md` §5, and `bpic2019_goal_model.md` §5. This table is
thinner than RTFM's, for the same reason `sepsis_goal_model.md` §5 gives for its own thin table: no
domain-expert or organizational source assigns contribution weights for this process, so this draft does
not manufacture values for TTrip (the trip itself has no clear softgoal relevance beyond enabling G5) or
for finer distinctions within TAppr (e.g., Director involvement specifically) rather than invent judgments
with no basis.

## 6. Indicators

| KPI | Formula | P50 | P75 | P90/P95 | Provenance |
|---|---|---|---|---|---|
| Time to reimbursement | days, first(`Declaration SUBMITTED by EMPLOYEE`, `Request For Payment SUBMITTED by EMPLOYEE`) → last `Payment Handled` | 13.3 | 31.1 | 80.0 / 105.2 | Formula grounded in the official challenge's own process question: "What is the throughput of a travel declaration from submission (or closing) to paying?" (ICPM, 2020, reproduced in Klein et al., 2020, §3, Q1). Percentiles (n = 5,721 cases) are this project's own computation directly against the log, not an organizational target — see §8. |
| Budget overspend rate | share of permits with `case:Overspent = True` | — | — | 26.8% (1,894 / 7,065) | Directly the log's own case-level attribute, not derived — the same "reused straight from the log's own schema" grounding `sepsis_goal_model.md` §6 uses for its KPI3 (`Return ER`). No externally published target exists for what an acceptable overspend rate should be. |
| Approval-chain rejection rate | share of eventually-approved permits rejected at least once before `FINAL_APPROVED` | — | — | 4.6% (319 / 6,960) | Illustrative operational-quality indicator on SG1; no external source defines this as a formal KPI — this project's own construction, flagged as such per the same candor `rtfm_goal_model.md` §6 applies to its own third, unsourced KPI. |

The first indicator's *formula* traces to the official challenge's own process question (ICPM, 2020;
Klein et al., 2020), the same grounding tier `bpic2019_goal_model.md` §6 reports for its own throughput
KPIs — stronger than an invented metric, weaker than a domain-expert-set threshold. The second indicator
is the strongest-grounded of the three in one specific sense: it requires no formula invention at all,
since `Overspent` is already a boolean the log's own publisher computed and attached to each case — but,
as with `sepsis_goal_model.md`'s equivalent case, no source states what overspend *rate* the organization
considers acceptable, so no worst/threshold/target judgment is asserted here. The third indicator has no
external grounding at all, matching RTFM's own third-KPI candor.

## 7. Traceability to observed BPIC2020 activity labels (non-binding)

This table exists only to make the model legible against the actual log vocabulary; it is not part of
the goal model's authority and must not be used to pre-filter or pre-match narratives lexically — per
`project/OVERVIEW.md`, Step 6 matching is semantic ("does this narrative realize this declared
alternative?"), not a string match against this table.

| Task | Typically realized by (BPIC2020 activity labels) |
|---|---|
| T1 | `Permit SUBMITTED by EMPLOYEE` (optionally preceded by `Permit SAVED by EMPLOYEE`) |
| TR | `Permit REJECTED by ADMINISTRATION` / `BUDGET OWNER` / `SUPERVISOR` / `PRE_APPROVER` / `DIRECTOR` / `EMPLOYEE` / `MISSING` |
| TAppr | `Permit APPROVED by ADMINISTRATION` / `BUDGET OWNER` / `SUPERVISOR` / `PRE_APPROVER`, `Permit FOR_APPROVAL by ADMINISTRATION` / `SUPERVISOR`, `Permit FINAL_APPROVED by SUPERVISOR` / `DIRECTOR` |
| TTrip | `Start trip`, `End trip` |
| TDecl | `Declaration SUBMITTED by EMPLOYEE`, `Declaration APPROVED by ...`, `Declaration FINAL_APPROVED by ...`, `Declaration REJECTED by ...`, `Payment Handled` |
| TRFP | `Request For Payment SUBMITTED by EMPLOYEE`, `Request For Payment APPROVED by ...`, `Request For Payment FINAL_APPROVED by ...`, `Request For Payment REJECTED by ...`, `Request Payment`, `Payment Handled` |

Two behaviors deliberately fall outside this table, by design rather than by omission — the same
distinction `rtfm_goal_model.md` §7 and `sepsis_goal_model.md` §7 draw for their own logs:

- **`Send Reminder`** — present in 1,381 of 7,065 cases (19.5%, direct scan) — is not a task in this
  decomposition; it is a system-generated nudge about an already-pending declaration or payment request,
  not a business step toward G0, the same distinction `sepsis_goal_model.md` §7 draws for `Return ER`.
- **`Start trip`/`End trip` occurring regardless of the permit's authorization outcome** — direct scan
  finds both activities present in essentially every one of the 7,065 cases (7,065/7,065), including
  cases where the permit was ultimately rejected and never resubmitted (e.g., a case observed directly
  during this model's authoring: submitted, rejected by Administration, rejected again by the employee,
  yet still carries a `Start trip`/`End trip` pair). This does not match the official description's own
  framing that international-trip permission "should be approved before making any arrangements" (ICPM,
  2020), and is retained here as observable evidence rather than silently normalized away — the same
  treatment RTFM's out-of-sequence `Payment` example receives in `rtfm_goal_model.md` §7. A plausible,
  unverified explanation is that `Start trip`/`End trip` are derived from the permit's *planned* travel
  dates rather than independently timestamped operational events, which would make TTrip's placement in
  §3's decomposition (as gated behind TAppr) a normative statement of intended business logic that this
  specific log's own event-generation mechanism does not enforce — see §8.

## 8. Limitations of the draft artifact

**What is already grounded.** §2–§4's actor set and approval-chain routing order (Administration →
Budget Owner → Supervisor, with an optional Director step) reproduce the official BPI Challenge 2020
process description verbatim in its key claims (ICPM, 2020), independently corroborated by Klein et al.
(2020), who built a reference BPMN model from that same text and reconciled it against the actual log.
§6's overspend indicator requires no invented formula at all — it is the log's own published attribute.
Every quantitative claim in §3, §4, §6, and §7 (the 4.5%/1.2% rejection outcomes, the 16.4%
both-Declaration-and-RFP rate, the 26.8% overspend rate, the 0.2% SAVED-draft rate, the 19.5%
Send-Reminder rate, the near-universal Start-trip/End-trip presence) was computed directly against
`data/logs/bpic2020_permit.xes.gz` during this model's authoring, not taken on faith from a secondary
source.

**What is still open.**

- **Pre-Approver is an acknowledged, unresolved gap, not an oversight.** Klein et al. (2020, §12) state
  directly that "an involvement of this entity is never mentioned in the textual description," despite
  `PRE_APPROVER` appearing in 627 of 7,065 cases (8.9%, direct scan) in this project's own copy of the
  log. TAppr (§4) is declared satisfied by reaching a final-approval activity without asserting where in
  the chain Pre-Approver sits or what triggers its involvement — this model does not paper over that gap
  with an invented rule.
- **Budget Owner/Supervisor merge and Director-step conditions are stated qualitatively, not
  quantitatively, by the official source.** The description states that "if the budget owner and
  supervisor are the same person, then only one of these steps is taken" and that the Director approves
  "in some cases" (ICPM, 2020), without stating a budget threshold or other rule; no source found during
  this model's authoring supplies one. TAppr's internal composite (§4) reflects only the documented
  routing order, not any threshold logic.
- **TTrip's placement in §3–§4 is a normative statement of intended business logic, not a description of
  what this log's `Start trip`/`End trip` events actually encode.** §7's traceability note above reports
  that these two activities occur in nearly every case regardless of the permit's approval outcome — a
  pattern more consistent with derived/planned-date fields than with independently gated operational
  events. A future revision should either confirm this interpretation against TU/e's actual system
  behavior or restructure G4 to not assert a dependency the data does not support.
- **This log's own scope is narrower than "the travel process" as a whole.** Because a case here is a
  travel *permit*, and the official description states domestic trips do not require one (ICPM, 2020),
  this model — and any category discovered from it — describes only the permit-requiring (predominantly
  international) subset of TU/e travel, not domestic travel covered by the separate BPIC 2020 Domestic
  Declarations sub-log, which this project does not stage (`project/OVERVIEW.md`, "Data sources").
- **Compliance-question wording beyond Q1 (§6) was not independently re-verified against the live
  challenge page during this model's authoring** — Klein et al. (2020) and a second independent BPIC 2020
  report (Nikolayuk et al., 2020) are cited as challenge technical reports, not as confirmed peer-reviewed
  proceedings papers (neither was found in the DBLP table of contents for the ICPM 2020 workshop
  proceedings, Leemans & Leopold, 2021); their empirical findings beyond Q1 should be treated as
  well-informed secondary analysis, not as organizer-published fact.
- No domain-expert (TU/e travel- or finance-administration practitioner) review of §2–§5 has occurred,
  mirroring the open gap `rtfm_goal_model.md` §8 and `sepsis_goal_model.md` §8 disclose for their own
  non-KPI-grounded content.

This artifact should be treated as a first-pass draft, authored for pipeline-development purposes only,
in the same sense as `rtfm_goal_model.md` v1.0 and `sepsis_goal_model.md` v1.0 — a future domain-expert
pass, should one occur, supersedes this version rather than editing it in place.

## 9. References

```bibtex
@misc{vandongen2020bpic,
  author       = {van Dongen, Boudewijn F.},
  title        = {BPI Challenge 2020: Travel Permit Data},
  year         = {2020},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:ea03d361-a7cd-4f5e-83d8-5fbdf0362550}
}

@misc{icpm2020bpic,
  author       = {{ICPM Conference}},
  title        = {BPI Challenge 2020},
  year         = {2020},
  howpublished = {\url{https://icpmconference.org/2020/bpi-challenge/}}
}

@misc{klein2020bpic20,
  author       = {Klein, Sabrina and Lahann, Johannes and Mayer, Lukas and Neu, Daniel and Pfeiffer, Philip and Rebmann, Adrian and Scheid, Miriam and Willems, Benjamin and Fettke, Peter},
  title        = {Business Process Intelligence Challenge 2020: Analysis and Evaluation of a Travel Process},
  year         = {2020},
  howpublished = {ICPM 2020 challenge report, DFKI / Saarland University / University of Mannheim, \url{https://icpmconference.org/2020/wp-content/uploads/sites/4/2020/10/ICPM_2020_paper_99.pdf}}
}

@misc{nikolayuk2020bpic20,
  author       = {Nikolayuk, Anna and Sdvizhkova, Ekaterina and Khabarova, Yulia and Shtokolova, Anastasiia and Tarasov, Yaroslav},
  title        = {BPI Challenge 2020 Report: Analyzing International and Domestic Travel Processes},
  year         = {2020},
  howpublished = {ICPM 2020 challenge report, PJSC Sberbank, \url{https://icpmconference.org/2020/wp-content/uploads/sites/4/2020/10/ICPM_2020_paper_100.pdf}}
}

@book{leemans2021pmworkshops,
  editor    = {Leemans, Sander J. J. and Leopold, Henrik},
  title     = {Process Mining Workshops: ICPM 2020 International Workshops, Padua, Italy, October 5--8, 2020, Revised Selected Papers},
  series    = {LNBIP},
  volume    = {406},
  publisher = {Springer},
  year      = {2021},
  doi       = {10.1007/978-3-030-72693-5}
}

@article{amyot2022urnsurvey,
  author  = {Amyot, Daniel and Akhigbe, Okhaide and Baslyman, Malak and Ghanavati, Sepideh and Ghasemi, Mahdi and Hassine, Jameleddine and Lessard, Lysanne and Mussbacher, Gunter and Shen, Kairui and Yu, Eric},
  title   = {Combining Goal Modelling with Business Process Modelling: Two Decades of Experience with the User Requirements Notation Standard},
  journal = {Enterprise Modelling and Information Systems Architectures (EMISAJ)},
  volume  = {17},
  number  = {2},
  pages   = {2:1--2:38},
  year    = {2022},
  doi     = {10.18417/emisa.17.2}
}
```
