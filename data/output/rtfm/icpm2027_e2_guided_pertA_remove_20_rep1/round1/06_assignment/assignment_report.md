# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing Maximize timely fine revenue and Minimize administrative & enforcement cost, judged against Time to fine dispatch and Average time to case closure indicators.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12. Supported by variants like V0002 and V0007 where payment occurs shortly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49944/150370 cases (33.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.68, nearest other category `delinquent_payment` at mean distance 5.20

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.355, nearest other category `delinquent_payment` at mean distance 0.331

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after notification and penalty application, helping Maximize timely fine revenue, judged against Average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13. Evidenced by variants such as V0004, V0005, and V0006 where payments happen subsequent to Insert Fine Notification and Add penalty activities.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 51/231 variants (22.1%) · micro 75456/150370 cases (50.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.22, nearest other category `administrative_appeal` at mean distance 4.93

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.282, nearest other category `timely_payment` at mean distance 0.331

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving administrative appeals to the Prefecture, preserving offender's due-process rights while potentially impacting enforcement cost and revenue, judged against Time to appeal filing, Prefecture.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14. Supported by variants like V0008, V0057, and V00137 containing activities related to the Prefecture appeal process.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 96/231 variants (41.6%) · micro 3975/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.31, nearest other category `delinquent_payment` at mean distance 4.93

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.381, nearest other category `judicial_appeal` at mean distance 0.416

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving judicial appeals to a judge, strongly advancing offender's due-process rights and hurting administrative cost, judged against Time to appeal filing, Judge.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19. Evidenced in variants like V0103, V0176, and V0140 containing Appeal to Judge activities.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 66/231 variants (28.6%) · micro 525/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.71, nearest other category `administrative_appeal` at mean distance 5.30

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.417, nearest other category `administrative_appeal` at mean distance 0.416

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal`): structural=17, profile=0.698
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`delinquent_payment`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019
- `V0005` (`delinquent_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060
- `V0006` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.390

## Residual

10/231 variants (4.3%), 20470/150370 cases (13.6%) unassigned.

- `V0003`: The case ends after sending the fine without any payment or appeal recorded.
- `V0026`: The case ends with Send for Credit Collection, which does not fit timely payment, delinquent payment, administrative appeal, or judicial appeal.
- `V0040`: The process ends with sending for credit collection after a judicial appeal, which does not fit any standard resolution category.
- `V0043`: Ends in credit collection, which is outside the main resolution categories.
- `V0106`: The case ends by being sent for credit collection after an administrative appeal, which does not cleanly fit any single resolution category.
- `V0108`: The case features both payment and subsequent credit collection following an administrative appeal.
- `V0111`: The case goes through administrative appeal and ends in credit collection without resolving by payment or appeal closure.
- `V0123`: The case involves payments and ultimately ends up sent for credit collection.
- `V0193`: The process exhibits anomalous early payment before the fine is even sent, fitting none of the standard resolution categories.
- `V0196`: The variant contains an unusual flow where appeal steps happen before fine dispatch, fitting none of the categories.