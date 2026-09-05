# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep3` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt payment by the offender, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement costs, evaluated against indicators such as time to fine dispatch and average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12 as seen in frequent variants like V0002, V0004, and V0007 where payment successfully closes the case.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 52/231 variants (22.5%) · micro 66878/150370 cases (44.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.53, nearest other category `administrative_appeal` at mean distance 5.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.215, nearest other category `merged_closure` at mean distance 0.396

## Merged 13+20 (`merged_closure`)

Resolution of the fine case through alternative closure mechanisms, helping maximize timely fine revenue while hurting the minimization of administrative and enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13 representing merged closure paths found in credit collection variants such as V0001, V0009, and V0010.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 10/231 variants (4.3%) · micro 76/150370 cases (0.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.76, nearest other category `timely_payment` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.443, nearest other category `timely_payment` at mean distance 0.396

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case through an administrative appeal submitted to the Prefecture, preserving the offender's due-process rights while incurring some negative effects on administrative costs and timely revenue, judged against the time to appeal filing indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14, evidenced by variants containing appeal tracking steps directed to the Prefecture such as V0008, V0057, and V0137.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 82/231 variants (35.5%) · micro 3888/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.30, nearest other category `timely_payment` at mean distance 5.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.386, nearest other category `judicial_appeal` at mean distance 0.412

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the fine case through a judicial appeal to the Judge, making a strong positive contribution to preserving the offender's due-process rights while hurting administrative costs and timely revenue, measured against the judicial appeal timing indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19, supported by variants explicitly logging judicial appeals such as V0103, V0176, and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 71/231 variants (30.7%) · micro 536/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.62, nearest other category `administrative_appeal` at mean distance 5.23

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.411, nearest other category `administrative_appeal` at mean distance 0.412

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`timely_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`timely_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019
- `V0005` (`timely_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060
- `V0006` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.390
- `V0006` (`timely_payment`) / `V0205` (`judicial_appeal`): structural=1, profile=0.737
- `V0007` (`timely_payment`) / `V0063` (`judicial_appeal`): structural=1, profile=0.354

## Residual

16/231 variants (6.9%), 78992/150370 cases (52.5%) unassigned.

- `V0001`: The case ends with Send for Credit Collection without payment or appeal resolution, falling outside the defined categories.
- `V0003`: The case terminates at Send Fine without any payment or appeal closure.
- `V0009`: Despite a payment step, the case ultimately goes to credit collection.
- `V0010`: The case ends with Send for Credit Collection despite an intermediate payment.
- `V0026`: The narrative ends with Send for Credit Collection, which does not fit any of the four resolution categories of timely payment, merged closure, administrative appeal, or judicial appeal.
- `V0051`: The case ends with Send for Credit Collection, which does not fit prompt payment, administrative appeal, or judicial appeal as a resolution path.
- `V0057`: The case ends with Send for Credit Collection after a series of appeal and collection steps.
- `V0059`: The case involves an administrative appeal sequence but ultimately ends with Send for Credit Collection.
- `V0067`: The process ends in Send for Credit Collection after repeated payments.
- `V0071`: The case ends with Send for Credit Collection.
- `V0160`: The case ends with Send for Credit Collection, which does not fit any of the resolution categories.
- `V0161`: The process terminates with Send for Credit Collection rather than a standard resolution category.
- `V0163`: The case concludes via Send for Credit Collection.
- `V0169`: The case ends with Send for Credit Collection despite prior payments.
- `V0170`: The process ultimately results in Send for Credit Collection.
- `V0173`: The case terminates with Send for Credit Collection.