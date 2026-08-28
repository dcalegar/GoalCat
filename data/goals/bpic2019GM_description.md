# BPIC 2019 Goal Model — Purchase Order Handling (Procure-to-Pay)

**Target log:** `data/logs/bpic2019.xes.gz` — the BPI Challenge 2019 event log (van Dongen, 2019):
251,734 purchase-order line items · 1,595,923 events · 42 activity labels · 11,973 variants (counts
verified against the log with `pm4py.read_xes`).

**Tool-notation copy:** [`bpic2019_goal_model.jucm`](bpic2019_goal_model.jucm) — the model in jUCMNav's
URN/GRL XMI format: the actor, the goal/task decomposition, the softgoal contribution links, and §6's
five indicators (each a `grl.kpimodel:Indicator` with a `KPIEvalValueSet` conversion, a `goalcat:*`
measurement binding, and a contribution link to a softgoal). Checked for XML well-formedness and
referential integrity; not round-trip verified in jUCMNav (Eclipse RCP unavailable here).

**What is grounded, and what is not.** The organizing axis — four item-resolution regimes at G2
(§3–§4) — comes from the official challenge description: the process comprises exactly four item
categories and "at least 4 models are needed" to describe them (ICPM, 2019), and `case:Item Category`
carries those four labels verbatim. Every quantitative claim in §3–§4 and §7 was computed directly
against the log. §6's indicator *formulas* trace to the challenge's own process questions and their
time-KPI value sets to EU late-payment law (§6); the compliance/exception rates and the softgoal
contribution values (§5) are this project's construction, informed by general procure-to-pay
internal-control reasoning, not a domain-expert consultation. No procurement or accounts-payable
practitioner has reviewed §2–§5.

---

## 1. Purpose and scope

This model declares what the purchase-order handling process is *for*, independently of the log, so
its OR-decomposition can serve as the taxonomy axis for intent-guided variant categorization (Step 5a).
It covers the lifecycle of a single purchase-order line item — the log's own case granularity — from
creation through whatever value-matching and payment-clearance mechanism its item category requires,
at "a large multinational company operating from The Netherlands in the areas of coatings and paints"
(ICPM, 2019), across 60 subsidiaries. It does not model control flow, timing, or exceptions beyond
what a goal-task decomposition requires — that is the job of the per-category process model discovered
at Step 7.

## 2. Actors

| Actor | Role | Type |
|---|---|---|
| Purchase-to-Pay (P2P) Back-Office | Creates, releases, receives, matches, and clears purchase order items across the company's subsidiaries | Primary |
| Requesting Business Unit | Originates the purchasing need; occasionally raises a formal Purchase Requisition | External |
| Vendor | Supplies the ordered goods or services; issues invoices, debit memos, and order confirmations | External |

Only the P2P Back-Office owns goals; the other two are external actors it depends on. This model does
not split the internal side into purchasing vs. accounts-payable sub-actors.

## 3. Goal–task decomposition

```mermaid
flowchart TD
    subgraph ACTOR["Actor: Purchase-to-Pay Back-Office"]
        G0("G0: Every purchase order item reaches<br/>a matched, compliant closure")
        G1("G1: Item is created and,<br/>where applicable, requisitioned")
        G2("G2: Item is resolved per<br/>its matching regime")
        G3("G3: 3-way matched,<br/>invoice recorded after goods receipt")
        G4("G4: 3-way matched,<br/>invoice recorded before goods receipt")
        G5("G5: 2-way matched<br/>(no goods receipt required)")
        T1{{"T1: Create Purchase Order Item"}}
        T2{{"T2: Requisition &amp; release<br/>(optional upstream gate)"}}
        T3{{"T3: Record Goods Receipt"}}
        T4{{"T4: Record invoice"}}
        T5{{"T5: Clear Invoice"}}
        T9{{"T9: Resolve via consignment<br/>consumption"}}
    end
    SG1(["SG1: Minimize procurement<br/>&amp; matching overhead"])
    SG2(["SG2: Maximize working-capital<br/>efficiency (timely clearance)"])
    SG3(["SG3: Preserve value-matching<br/>control integrity"])

    G0 -->|AND| G1
    G0 -->|AND| G2
    G1 -->|AND| T1
    G1 -->|AND| T2
    G2 -->|OR| G3
    G2 -->|OR| G4
    G2 -->|OR| G5
    G2 -->|OR| T9
    G3 -->|AND| T3
    G3 -->|AND| T4
    G3 -->|AND| T5
    G4 -->|AND| T3
    G4 -->|AND| T4
    G4 -->|AND| T5
    G5 -->|AND| T4
    G5 -->|AND| T5

    T5 -.->|"Make +100"| SG2
    G3 -.->|"Make +100"| SG3
    G3 -.->|"SomeNeg -25"| SG1
    G4 -.->|"Help +50"| SG3
    G4 -.->|"Help +50"| SG2
    G5 -.->|"Help +50"| SG1
    G5 -.->|"SomeNeg -25"| SG3
    T9 -.->|"Help +50"| SG1
    T9 -.->|"SomeNeg -25"| SG3

    classDef goal fill:#e8f0fe,stroke:#3367d6,stroke-width:2px
    classDef task fill:#f1f3f4,stroke:#5f6368,stroke-width:2px
    classDef softgoal fill:#fff4e5,stroke:#e8710a,stroke-width:2px
    class G0,G1,G2,G3,G4,G5 goal
    class T1,T2,T3,T4,T5,T9 task
    class SG1,SG2,SG3 softgoal
```

G0 requires both creation (G1) and resolution (G2). G2 is OR across G3, G4, G5, and T9, reproducing
the official description's four item categories one-to-one (ICPM, 2019). G3 and G4 share the same three
leaf tasks (T3, T4, T5): what distinguishes them is the *relative order* of T3 (Record Goods Receipt)
and T4 (Record invoice), which the log's `case:GR-Based Inv. Verif.` attribute encodes structurally.
G5 has no T3 child — direct scan confirms 0.0% of 2-way-match items ever record a Goods Receipt,
matching the official description that 2-way matching checks the invoice value against the
order-creation value alone. T9 (Consignment) is a leaf: "no invoices exist at the PO level" for
consigned stock (ICPM, 2019), confirmed by direct scan — 0.0% of Consignment items reach Clear Invoice
versus 92.9% that record a Goods Receipt.

## 4. Decomposition table

| ID | Type | Label | Operator | Children |
|---|---|---|---|---|
| G0 | Goal | Every purchase order item reaches a matched, compliant closure | AND | G1, G2 |
| G1 | Goal | Item is created and, where applicable, requisitioned | AND | T1, T2 |
| G2 | Goal | Item is resolved per its matching regime | OR | G3, G4, G5, T9 |
| G3 | Goal | 3-way matched, invoice recorded after goods receipt | AND | T3, T4, T5 |
| G4 | Goal | 3-way matched, invoice recorded before goods receipt | AND | T4, T3, T5 |
| G5 | Goal | 2-way matched (no goods receipt required) | AND | T4, T5 |
| T1 | Task | Create Purchase Order Item | leaf | — |
| T2 | Task | Requisition & release (optional upstream gate) | leaf, optional/conditional | — |
| T3 | Task | Record Goods Receipt | leaf, repeatable | — |
| T4 | Task | Record invoice (vendor invoice / invoice receipt / subsequent invoice) | leaf, repeatable | — |
| T5 | Task | Clear Invoice | leaf | — |
| T9 | Task | Resolve via consignment consumption | leaf | — |

T2 folds two genuinely optional low-frequency sub-flows into one leaf: an upstream Purchase-Requisition
sub-flow precedes order creation in 18.5% of items (46,592 / 251,734), and an explicit
`Release Purchase Order` gate is logged for only 0.4% (961). G4's row lists its children as "T4, T3, T5"
to signal the reversed order that is G4's defining feature relative to G3, even though the AND operator
does not itself encode sequencing.

## 5. Contribution links (softgoals)

| Source | Target | Value | Rationale |
|---|---|---|---|
| T5 (Clear Invoice) | SG2 (working-capital efficiency) | Make (+100) | Clearing is where the item's cash obligation is settled, regardless of matching regime |
| G3 (3-way, invoice after GR) | SG3 (control integrity) | Make (+100) | Canonical sequencing — physical receipt confirmed before the invoice is accepted for matching |
| G3 | SG1 (procurement overhead) | SomeNegative (-25) | An independent goods-receipt reconciliation step adds effort relative to a 2-way check |
| G4 (3-way, invoice before GR) | SG3 (control integrity) | Help (+50) | Still 3-way matched, but the invoice is accepted ahead of physical confirmation |
| G4 | SG2 (working-capital efficiency) | Help (+50) | Invoice processing can start before the goods-receipt message arrives |
| G5 (2-way match) | SG1 (procurement overhead) | Help (+50) | No goods-receipt reconciliation step at all |
| G5 | SG3 (control integrity) | SomeNegative (-25) | Invoice value checked against the order alone, no independent physical-receipt confirmation |
| T9 (Consignment) | SG1 (procurement overhead) | Help (+50) | No per-item invoice-clearance cycle at all |
| T9 | SG3 (control integrity) | SomeNegative (-25) | Item-level financial visibility is lower — settlement is not captured here |

Qualitative scale is the GRL/URN standard (Make = 100, Help = 50, SomePositive = 25, Unknown = 0,
SomeNegative = -25, Hurt = -50, Break = -100; Amyot et al., 2022). No cited internal-control standard
backs the 3-way > 2-way > none ordering — it follows the general logic of matching-based internal
control and should be read as this project's own qualitative judgment.

## 6. Indicators

Five indicators in two groups (`Time`, `Quality`). Each carries a `KPIEvalValueSet` (the
measurement → satisfaction conversion), a `goalcat:*` measurement binding (how Step 7b obtains the
value from the log), and a contribution link giving the converted value somewhere to propagate.

### 6.1 Time to clearance (three regimes)

| Indicator | Binding (`goalcat:*`) | target / threshold / worst |
|---|---|---|
| id 17 — 3-way, invoice after GR | `duration_days`, `Record Invoice Receipt` → `Clear Invoice` (first) | 30 / 60 / 120 days |
| id 18 — 3-way, invoice before GR | `duration_days`, `Record Goods Receipt` → `Clear Invoice` (first) | 30 / 60 / 120 days |
| id 19 — 2-way match | `duration_days`, `Record Invoice Receipt` → `Clear Invoice` (first) | 30 / 60 / 120 days |

**Value set — provenance `external-by-analogy`.** Directive 2011/7/EU on combating late payment in
commercial transactions sets the default B2B payment term at 30 days (art. 3(3)) and caps the term an
agreement may set at 60 days unless expressly agreed and not grossly unfair (art. 3(5)); it is
transposed in Dutch law (BW 6:119a, "Wet tegengaan van onredelijk lange betaaltermijnen"). `target`
30 and `threshold` 60 are those two legal points; `worst` 120 is illustrative (2× the maximum). The
term runs from the *later* of goods receipt or invoice receipt (art. 3(3)(b)) — hence id 17 and id 19
start from `Record Invoice Receipt`, id 18 from `Record Goods Receipt`. The measurement *frame* (a
clock between goods receipt, invoice receipt, and payment) is the challenge's own process question 2
(ICPM, 2019). Contribution: each → SG2 (working-capital efficiency), Help (+50).

Contrast with RTFM's clearance KPI, whose bounds are statutory day-counts, and with the earlier draft
of this model, whose bounds were log percentiles scored against the same log — the circularity the
Directive anchor removes.

### 6.2 Quality (two rates)

| Indicator | Binding (`goalcat:*`) | target / threshold / worst |
|---|---|---|
| id 20 — 3-way matching compliance (violation rate) | `case_fraction`, `among` = `Clear Invoice`, `numerator` = `lacks:Record Goods Receipt` | 0 / 1 / 5 % |
| id 21 — Exception/rework rate | `case_fraction`, `numerator` = `has:Cancel Invoice Receipt \| Cancel Goods Receipt \| Block Purchase Order Item \| Set Payment Block` | 0 / 5 / 15 % |

**Value sets — provenance `illustrative`.** id 20's denominator is items that reach `Clear Invoice`;
its numerator is those cleared with no `Record Goods Receipt` ever logged — the deviation the
challenge's process question 3 asks about (ICPM, 2019). id 21 is the share of items carrying at least
one cancellation or block event. No organizer-published or external target exists for either rate; the
bounds bracket the observed full-log rates (0.31% and 3.39%). Contributions: id 20 → SG3 (control
integrity), Help (+50); id 21 → SG1 (procurement overhead), Help (+50).

## 7. Traceability to observed activity labels (non-binding)

For legibility against the log vocabulary only — not part of the model's authority, and not to be used
for lexical pre-matching (Step 6 matching is semantic).

| Task | Typically realized by |
|---|---|
| T1 | `Create Purchase Order Item` |
| T2 | `Create Purchase Requisition Item`, `Release Purchase Requisition`, `Release Purchase Order`, `Change Approval for Purchase Order` |
| T3 | `Record Goods Receipt`, `Record Service Entry Sheet` |
| T4 | `Vendor creates invoice`, `Record Invoice Receipt`, `Record Subsequent Invoice`, `Vendor creates debit memo` |
| T5 | `Clear Invoice` |
| T9 | no dedicated label — identified by `case:Item Category = "Consignment"` |

Three behaviors sit outside this table by design: **right-censored (still-open) items** — the majority
of items have not reached `Clear Invoice` at extraction time (e.g. 63.7% of "3-way after GR" and 29.0%
of 2-way items do); these are *not yet satisfied*, not anomalies. **The self-service (SRM) sub-flow** —
1,440 items (0.57%) carry `SRM: ...` status events and never co-occur with `Create Purchase Requisition
Item`; a low-frequency channel this model does not decompose. **Goods-receipt-after-clearance
sequencing** — 566 of 183,374 cleared 3-way items (0.31%) reach `Clear Invoice` with no goods receipt
logged (§6.2's id 20 quantity), retained as observable evidence.

## 8. Limitations

- §5's contribution ordering (3-way > 2-way > none) reflects standard procure-to-pay reasoning but no
  specific citable internal-control standard was found for it.
- §6.1's value set is `external-by-analogy`: an employee/vendor invoice clearance under EU late-payment
  law, applied to this process. §6.2's rate bounds are `illustrative` — no external target exists.
- T9 (Consignment) has no task-realizing activity label; its place in the decomposition rests on the
  official description's prose plus the corroborating 0%-clearance / 92.9%-GR pattern.
- The challenge page states three organizer-posed process questions (model coverage, invoicing
  throughput, Purchasing-Document-level deviations). Any segregation-of-duties framing seen elsewhere
  is participant interpretation, not the challenge brief.
- No procurement or accounts-payable practitioner has reviewed §2–§5.

## 9. References

```bibtex
@misc{vandongen2019bpic,
  author       = {van Dongen, Boudewijn F.},
  title        = {BPI Challenge 2019},
  year         = {2019},
  publisher    = {4TU.ResearchData},
  doi          = {10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1}
}

@misc{icpm2019bpic,
  author       = {{ICPM Conference}},
  title        = {BPI Challenge 2019},
  year         = {2019},
  howpublished = {\url{https://icpmconference.org/2019/icpm-2019/contests-challenges/bpi-challenge-2019/}}
}

@misc{eu2011latepayment,
  author       = {{European Union}},
  title        = {Directive 2011/7/EU on combating late payment in commercial transactions},
  year         = {2011},
  howpublished = {Official Journal of the European Union L 48/1; transposed in NL as BW art. 6:119a}
}

@techreport{gutermuth2019bpic19,
  author      = {Gutermuth, Ottmar and Lahann, Johannes and Rehse, Jana-Rebecca and Scheid, Miriam and Schuhmann, Sarah and Stephan, Sabrina and Fettke, Peter},
  title       = {Efficient and Compliant Purchase Order Handling: A Contribution to BPI Challenge 2019},
  institution = {Saarland University},
  year        = {2019},
  doi         = {10.22028/D291-34142}
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
