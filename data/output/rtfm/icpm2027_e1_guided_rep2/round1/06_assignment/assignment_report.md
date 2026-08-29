# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case via prompt payment made by the offender. Advances the 'Maximize timely fine revenue' softgoal and helps 'Minimize administrative & enforcement cost'. Judged against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 12 (Resolve via timely payment). The narrative sample shows frequent realization of this alternative (e.g. variant V0002).

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 6/231 variants (2.6%) · micro 49579/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.60, nearest other category `administrative_appeal` at mean distance 5.19

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.269, nearest other category `delinquent_payment` at mean distance 0.256

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case via payment made after penalties and enforcement notifications have been issued. Helps 'Maximize timely fine revenue'. Judged against indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 13 (Resolve via delinquent payment). The narrative sample shows cases realizing delinquent payments after penalties (e.g. variants V0004, V0005, V0006).

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 60/231 variants (26.0%) · micro 16971/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.04, nearest other category `administrative_appeal` at mean distance 5.06

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.176, nearest other category `timely_payment` at mean distance 0.256

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the case through an administrative appeal filed with the Prefecture. Preserves offender's due-process rights (Help +50) but can negatively impact enforcement cost and timely revenue. Judged against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 14 (Resolve via administrative appeal to the Prefecture). The narrative sample confirms cases following the administrative appeal pathway via variants like V0008 and V0057.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 69/231 variants (29.9%) · micro 3675/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.80, nearest other category `coercive_credit_collection` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.356, nearest other category `judicial_appeal` at mean distance 0.407

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the case through a judicial appeal to the Judge. Maximizes offender's due-process rights (Make +100) and hurts administrative enforcement cost. Judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 19 (Resolve via judicial appeal to the Judge), which is mutually exclusive under the XOR parent node 7. Observed in variants such as V0103 and V0176.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 48/231 variants (20.8%) · micro 380/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.57, nearest other category `administrative_appeal` at mean distance 5.08

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.372, nearest other category `delinquent_payment` at mean distance 0.377

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the case through coercive credit collection measures after standard resolution paths fail. Helps maximize timely fine revenue but hurts minimization of administrative costs. Judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 20 (Resolve via coercive credit collection). The narrative sample shows numerous cases ending in credit collection (e.g. variants V0001, V0009, V0135).

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 44/231 variants (19.0%) · micro 59013/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `administrative_appeal` at mean distance 0.494

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `judicial_appeal`): structural=16, profile=0.730

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The process ends at Send Fine without any payment or further resolution, remaining in the residual.
- `V0012`: An unusual sequence involving payment before sending the fine; does not neatly map to standard categories.
- `V0077`: The sequence is incomplete or anomalous (ends abruptly at Send Fine after appeal steps), not fitting any clear resolution category.
- `V0193`: Variant ends prematurely with Send Fine without reaching a resolution state or category criteria.