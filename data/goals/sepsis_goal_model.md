# Sepsis Goal Model (Step G) — Emergency-Department Sepsis Pathway

**Status:** **Draft**, version 1.0, 2026-08-19. Frozen by project-owner decision for pipeline-development
purposes, in the same spirit as `rtfm_goal_model.md` v1.0 — not yet reviewed by a treating physician for
*this specific* goal-task decomposition. §8 states exactly what is, and is not, already grounded.
**Target log:** `data/logs/sepsis.xes.gz` — the Sepsis Cases event log (Mannhardt, 2016), 1,050 traces,
846 unique variants, 15,214 events, 16 activities — counts verified directly against the file's own
embedded XES metadata (`meta_concept:named_events_total`) and a direct trace/variant scan, 2026-08-19.
Ghasemi (2021, Ch. 8, p. 147) reports 846 unique traces (matches exactly) but 15,124 events from a raw
CSV export of the same dataset — a small (0.6%) discrepancy against this project's XES copy, plausibly a
preprocessing or export-version difference; not investigated further here.
**Provenance:** Unlike `rtfm_goal_model.md`, this draft's most load-bearing content — the three
guideline-timed KPIs in §6 — is not a fresh statutory reconstruction. It is reused, with attribution,
from a prior study that already ran the domain-expert consultation this kind of artifact needs: Ghasemi
(2021, Ch. 8) derived three KPIs for this exact log from guideline windows reported in Mannhardt & Blinde
(2017) — the log's own co-author's process-mining study of it — and refined them "after consultation with
a physician" at the University of Ottawa (Ghasemi, 2021, Acknowledgments; §8.4). Mannhardt & Blinde
(2017, §2, referencing Rhodes et al., 2017) trace those windows to the Surviving Sepsis Campaign's 2016
international guideline. What is *not* reused from any source is the AND/OR goal-task decomposition
itself (§3–§4): no source builds a task-alternative taxonomy for this log — Ghasemi's own goal model
(2021, Fig. 37) is a flat set of three KPI-linked goals, not an OR-decomposition of care-pathway
alternatives, because GoPED's filtering purpose never needed one. §8 states this gap plainly.

---

## 1. Purpose and scope

This model declares what the emergency-department sepsis pathway is *for*, independently of the log, so
that its OR-decomposition can serve as the taxonomy axis for intent-guided variant categorization
(Step 5a) — the same role `rtfm_goal_model.md` plays for RTFM. It covers a patient's trajectory from
emergency-room registration, through sepsis screening and guideline-timed treatment, to ward admission
and eventual discharge, as recorded by a Dutch hospital's information system (Mannhardt & Blinde, 2017,
§2). It does not model control flow, timing, or exceptions beyond what a goal-task decomposition
requires — that is the job of the per-category process model discovered downstream (Step 7), not of this
artifact.

## 2. Actors

| Actor | Role | Type |
|---|---|---|
| Emergency Department (ED) care team | Registers, triages, tests, treats, and dispositions the patient | Primary |
| Patient | Presents with suspected sepsis; may return to the ED after discharge | External |
| Inpatient ward (Normal Care / Intensive Care) | Receives the patient if admitted; the ward stay itself is outside the log's scope | External |

Only the ED care team owns goals in this model; the other two are external actors it depends on or acts
upon, not goal-bearing participants — the same asymmetry `rtfm_goal_model.md` §2 draws for RTFM's
Prefecture, Judge, and Credit Collection Agent.

## 3. Goal–task decomposition

```mermaid
flowchart TD
    subgraph ACTOR["Actor: Emergency Department care team"]
        G0("G0: Every patient with suspected sepsis<br/>is screened, treated within guideline<br/>windows, and reaches a documented disposition")
        G1("G1: Patient is registered<br/>and screened for sepsis")
        G2("G2: Sepsis workup and treatment<br/>are performed")
        G3("G3: Patient is admitted<br/>to an inpatient ward")
        G4("G4: Admitted case reaches<br/>a captured discharge")
        T1{{"T1: ER Registration"}}
        T2{{"T2: ER Triage"}}
        T3{{"T3: ER Sepsis Triage"}}
        T4{{"T4: Leucocytes"}}
        T5{{"T5: CRP"}}
        T6{{"T6: LacticAcid"}}
        T7{{"T7: IV Liquid"}}
        T8{{"T8: IV Antibiotics"}}
        T9{{"T9: Admission NC"}}
        T10{{"T10: Admission IC"}}
        TA{{"Release A"}}
        TB{{"Release B"}}
        TC{{"Release C"}}
        TD{{"Release D"}}
        TE{{"Release E"}}
    end
    SG1(["SG1: Minimize<br/>time-to-treatment"])
    SG2(["SG2: Avoid post-discharge<br/>deterioration"])

    G0 -->|AND| G1
    G0 -->|AND| G2
    G0 -->|AND| G3
    G0 -->|AND| G4
    G1 -->|AND| T1
    G1 -->|AND| T2
    G1 -->|AND| T3
    G2 -->|AND| T4
    G2 -->|AND| T5
    G2 -->|AND| T6
    G2 -->|AND| T7
    G2 -->|AND| T8
    G3 -->|OR| T9
    G3 -->|OR| T10
    G4 -->|OR| TA
    G4 -->|OR| TB
    G4 -->|OR| TC
    G4 -->|OR| TD
    G4 -->|OR| TE

    T8 -.->|"Make +100 (KPI1)"| SG1
    T6 -.->|"Make +100 (KPI2)"| SG1
    T10 -.->|"SomeNeg -25"| SG1
    TA -.->|"Help +50 (low KPI3 rate)"| SG2
    TB -.->|"Help +50 (low KPI3 rate)"| SG2

    classDef goal fill:#e8f0fe,stroke:#3367d6,stroke-width:2px
    classDef task fill:#f1f3f4,stroke:#5f6368,stroke-width:2px
    classDef softgoal fill:#fff4e5,stroke:#e8710a,stroke-width:2px
    class G0,G1,G2,G3,G4 goal
    class T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,TA,TB,TC,TD,TE task
    class SG1,SG2 softgoal
```

**Reading the decomposition.** G0 requires screening (G1), treatment (G2), *and* a documented disposition
(G3 admission, then G4 discharge) — a case that is treated but never reaches a captured discharge does
not satisfy G0, mirroring how RTFM's G0 withholds satisfaction from a fine that is never formally
communicated. G3 is OR, not XOR: exactly one of Normal Care or Intensive Care admission is expected per
episode, but the axis is a genuine alternative (severity-driven), not a business-intent split like RTFM's
TP/TA. G4 is OR across five discharge dispositions (Release A–E) — structurally the same shape as RTFM's
five-way OR at G4 (TA, G5, TD and its two appeal leaves), though here the five alternatives are not
independently decoded (see §4's note). G1 and G2 are AND, matching the guideline: registration, triage,
and sepsis-specific triage are each required steps, and diagnostic workup (T4–T6) plus treatment (T7–T8)
are jointly expected within the treatment window, not alternatives to one another.

## 4. Decomposition table

| ID | Type | Label | Operator | Children |
|---|---|---|---|---|
| G0 | Goal | Every patient with suspected sepsis is screened, treated within guideline windows, and reaches a documented disposition | AND | G1, G2, G3, G4 |
| G1 | Goal | Patient is registered and screened for sepsis | AND | T1, T2, T3 |
| G2 | Goal | Sepsis workup and treatment are performed | AND | T4, T5, T6, T7, T8 |
| G3 | Goal | Patient is admitted to an inpatient ward | OR | T9, T10 |
| G4 | Goal | Admitted case reaches a captured discharge | OR | Release A, Release B, Release C, Release D, Release E |
| T1 | Task | ER Registration | leaf | — |
| T2 | Task | ER Triage | leaf | — |
| T3 | Task | ER Sepsis Triage | leaf | — |
| T4 | Task | Leucocytes (blood test) | leaf | — |
| T5 | Task | CRP (blood test) | leaf | — |
| T6 | Task | LacticAcid (blood test) | leaf, guideline-timed (KPI2) | — |
| T7 | Task | IV Liquid | leaf | — |
| T8 | Task | IV Antibiotics | leaf, guideline-timed (KPI1) | — |
| T9 | Task | Admission NC (Normal Care) | leaf | — |
| T10 | Task | Admission IC (Intensive Care) | leaf | — |
| Release A–E | Task | Five distinct discharge dispositions | leaf | — |

G3→G4 is empirically, not just declaratively, sequential in this log: of the 1,050 traces in
`data/logs/sepsis.xes.gz`, every trace containing a Release activity also contains an Admission (NC or
IC) activity beforehand (782 of 1,050 traces, 74.5%) — zero traces reach a Release without a prior
Admission (verified by direct scan, 2026-08-19). This project's `data/logs/` copy therefore does not
support a "direct release without ward admission" alternative at G3, unlike what its logical OR shape
might suggest; none is declared here.

The five Release labels (A–E) are carried unchanged from the published dataset's own activity names.
Neither Ghasemi (2021), Mannhardt & Blinde (2017), nor the 4TU.ResearchData listing decodes what
clinically distinguishes them beyond frequency — Release A is by far the most common (671 of 15,214
events, 63.9% of cases per Ghasemi 2021, Table 17), Release E the rarest (6 events, 0.6%). This model
declares them as five alternative closure tasks because the log itself treats them as five distinct
labels, not because their clinical meaning has been established; a domain-expert pass should either
confirm this five-way split or collapse/relabel it.

## 5. Contribution links (softgoals)

| Source | Target | Value | Rationale |
|---|---|---|---|
| T8 (IV Antibiotics) | SG1 (time-to-treatment) | Make (+100) | Directly satisfies the guideline's 1-hour antibiotic window (KPI1) |
| T6 (LacticAcid) | SG1 (time-to-treatment) | Make (+100) | Directly satisfies the guideline's 3-hour lactate window (KPI2) |
| T10 (Admission IC) | SG1 (time-to-treatment) | SomeNegative (-25) | Intensive Care admission is associated with more severe, harder-to-treat-within-window presentations |
| Release A | SG2 (avoid post-discharge deterioration) | Help (+50) | The modal discharge outcome; no claim beyond frequency (see §4) |
| Release B | SG2 (avoid post-discharge deterioration) | Help (+50) | Second most frequent discharge outcome; no claim beyond frequency (see §4) |

This table is thinner and more illustrative than `rtfm_goal_model.md`'s §5, deliberately: RTFM's
contribution values are grounded in statute and an expert-authored normative model (Mannhardt et al.,
2016); no equivalent source assigns contribution weights for this log's discharge dispositions, so this
draft does not manufacture the missing three rows (Release C/D/E) rather than invent values with no
basis. A domain-expert pass is the right place to complete or revise this table, not this draft.

## 6. Indicators

| KPI | Formula | Worst | Threshold | Target | Provenance |
|---|---|---|---|---|---|
| KPI1 — Time to antibiotics | hours, `ER Sepsis Triage` → `IV Antibiotics` | 3 h | 1.8 h | ≤ 1 h | Guideline-grounded: Rhodes et al. (2017), Surviving Sepsis Campaign 2016 guidelines, cited by Mannhardt & Blinde (2017, §2) as the source of the 1-hour antibiotic-administration rule for this exact log; worst/threshold/target values reused verbatim from Ghasemi (2021, Ch. 8, Table 19), set after physician consultation |
| KPI2 — Time to lactate measurement | hours, `ER Sepsis Triage` → `LacticAcid` | 7 h | 5 h | ≤ 3 h | Same chain: Rhodes et al. (2017) via Mannhardt & Blinde (2017, §2) for the 3-hour rule; worst/threshold/target reused verbatim from Ghasemi (2021, Ch. 8, Table 19), physician-consulted |
| KPI3 — Post-discharge ER return | binary, `Return ER` present in trace | 1 (returned) | — | 0 (no return) | Reused from Ghasemi (2021, Ch. 8) as "a common goal of any healthcare system" rather than a cited guideline window; not itself traced to Rhodes et al. (2017) |

These three indicators are the most reliably grounded part of this entire artifact — more so than any
single indicator in `rtfm_goal_model.md`, whose third KPI remains an acknowledged invented placeholder
even at v1.1. They are reused, not re-derived: this draft did not re-run physician consultation, only
carried Ghasemi (2021)'s already-consulted values forward with attribution. KPI1 and KPI2 are not
attached to G0 as a whole but to T8 and T6 individually (§5), the same way RTFM's indicators attach to
specific tasks rather than to G0.

## 7. Traceability to observed Sepsis activity labels (non-binding)

This table exists only to make the model legible against the actual log vocabulary; it is not part of
the goal model's authority and must not be used to pre-filter or pre-match narratives lexically — per
`project/OVERVIEW.md`, Step 6 matching is semantic ("does this narrative realize this declared
alternative?"), not a string match against this table. Because every task in §3–§4 is already named
after its activity label, this table is close to an identity map; it is included for consistency with
`rtfm_goal_model.md`'s §7, not because Sepsis activity names need decoding.

| Task | Sepsis activity label |
|---|---|
| T1–T10 | Identical string (see §4) |
| Release A–E | Identical string (see §4) |

Two behaviors deliberately fall outside this table, by design rather than by omission — the same
distinction `rtfm_goal_model.md` §7 draws for RTFM:

- **Right-censored (incomplete) cases** — 28 of 1,050 traces (2.7%) reach an Admission (NC or IC) but no
  captured Release; a further 240 of 1,050 (22.9%) end before reaching either an Admission or a Release
  activity at all (both counts verified by direct scan of `data/logs/sepsis.xes.gz`, 2026-08-19). These
  represent cases still open, transferred, or otherwise not captured to closure when the log was
  extracted — not a violation of G0; they should be treated as *not yet satisfied*, not as anomalies,
  exactly as RTFM's still-open `A1`/`V0001` variant is treated in `rtfm_goal_model.md` §7.
- **`Return ER`** — present in 294 of 1,050 traces (28.0%, Ghasemi 2021, Table 17) — is not a task in
  §3–§4's decomposition; it is the observable behind KPI3 (§6), a quality signal about the *prior*
  discharge, not a step toward G0.

## 8. Limitations of the draft artifact

**What is already grounded.** §6's KPI1 and KPI2 — the artifact's most consequential content, since they
are what a category's alignment against this goal model would actually be checked against — are reused
from Ghasemi (2021, Ch. 8), whose worst/threshold/target values were set "after consultation with a
physician" (Ghasemi 2021, Acknowledgments; §8.4) specifically for this log, and are traceable to the
Surviving Sepsis Campaign's 2016 international guideline (Rhodes et al., 2017) via Mannhardt & Blinde
(2017, §2), the log's own co-author's process-mining study of it. This is a stronger evidentiary chain
than `rtfm_goal_model.md` has for any of its own three KPIs — RTFM's third KPI remains an invented
placeholder even after its v1.1 revision.

**What is still open.** The physician consultation behind KPI1/KPI2 was scoped to those two flat,
KPI-linked goals (Ghasemi 2021, Fig. 37) — not to the AND/OR goal-task decomposition (§3–§4), the actor
structure (§2), or the softgoal contribution links (§5) built in this draft. Those three pieces are this
draft's own construction, built to give Step 5a the task-alternative taxonomy shape it needs (an
OR-decomposition into alternative tasks) that no prior source for this log provides — Ghasemi's own goal
model has no such structure, because GoPED's case-filtering purpose never required one. Concretely:

- §3's G3 (ward-admission OR) and G4 (discharge OR) are grounded only in this log's own observed
  structure (the admission-before-release ordering verified in §4, and the five Release labels the
  dataset itself uses), not in any clinical-guideline or physician source.
- §4's discharge-disposition alternatives (Release A–E) are declared as five distinct tasks because the
  log treats them as five distinct labels — their clinical meaning beyond frequency is not established
  by any source consulted here (§4).
- §5's softgoal contribution values are illustrative and incomplete by explicit choice (three of five
  plausible rows omitted rather than invented), not a physician- or guideline-sourced judgment.
- No domain-expert review of this specific decomposition, as distinct from the KPI reuse above, has
  occurred. Mirroring `rtfm_goal_model.md` §8's own framing of the equivalent gap: this is "artificial
  but reasonable," not yet a genuinely sourced Step G artifact for the parts beyond §6.

This artifact should be treated as a first-pass draft, frozen for pipeline-development purposes only, in
the same sense as `rtfm_goal_model.md` v1.0 — a future domain-expert pass, should one occur, supersedes
this version rather than editing it in place.

## 9. References

```bibtex
@misc{mannhardt2016sepsis,
  author       = {Mannhardt, Felix},
  title        = {Sepsis Cases - Event Log},
  year         = {2016},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460}
}

@inproceedings{mannhardt2017trajectories,
  author       = {Mannhardt, Felix and Blinde, Diana},
  title        = {Analyzing the Trajectories of Patients with Sepsis using Process Mining},
  booktitle    = {RADAR+EMISA Workshop @ CAiSE Forum},
  series       = {CEUR Workshop Proceedings},
  volume       = {1859},
  pages        = {72--80},
  year         = {2017},
  note         = {https://ceur-ws.org/Vol-1859/bpmds-08-paper.pdf}
}

@article{rhodes2017survivingsepsis,
  author       = {Rhodes, Andrew and others},
  title        = {Surviving Sepsis Campaign: International Guidelines for Management of Sepsis and Septic Shock: 2016},
  journal      = {Intensive Care Medicine},
  volume       = {43},
  number       = {3},
  pages        = {304--377},
  year         = {2017},
  doi          = {10.1007/s00134-017-4683-6}
}

@phdthesis{ghasemi2021dissertation,
  author       = {Ghasemi, Mahdi},
  title        = {Goal-oriented Process Mining},
  school       = {University of Ottawa},
  year         = {2021},
  doi          = {10.20381/ruor-27301}
}
```
