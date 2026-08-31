# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep3` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', measured against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=12 as evidenced by variants such as V0002 and V0007 ending directly in payment.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49617/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.57, nearest other category `delinquent_payment` at mean distance 5.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.226, nearest other category `delinquent_payment` at mean distance 0.210

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after a notification and penalty have been applied, helping maximize timely fine revenue and judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=13 as supported by variants like V0004, V0005, and V0006 where payment occurs after penalties and notifications.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 31/231 variants (13.4%) · micro 16912/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.47, nearest other category `administrative_appeal` at mean distance 5.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.151, nearest other category `timely_payment` at mean distance 0.210

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal to the Prefecture, preserving due-process rights while impacting enforcement costs and revenue, measured against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=14 as evidenced by traces like V0008 and V0057 containing administrative appeal steps.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 78/231 variants (33.8%) · micro 3692/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.90, nearest other category `coercive_credit_collection` at mean distance 4.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.345, nearest other category `delinquent_payment` at mean distance 0.374

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases where the offender pursues a judicial appeal to the Judge, maximizing due-process rights while hurting administrative costs, evaluated against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=19, observed in samples such as V0103 and V0144 featuring judicial appeal activities.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 69/231 variants (29.9%) · micro 386/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.60, nearest other category `administrative_appeal` at mean distance 5.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.404, nearest other category `administrative_appeal` at mean distance 0.389

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases that reach an enforced closure through coercive credit collection, helping revenue while hurting cost, judged against average case closure time.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to the declared alternative id=20 as frequently seen in variants like V0001, V0009, and V0010 ending with credit collection.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 42/231 variants (18.2%) · micro 59011/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.06, nearest other category `administrative_appeal` at mean distance 4.68

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.173, nearest other category `judicial_appeal` at mean distance 0.496

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
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019
- `V0005` (`delinquent_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The case ends after sending the fine without any payment, appeal, or credit collection conclusion.
- `V0012`: The case ends with Send Fine following a prior payment step, leaving the outcome unresolved.
- `V0077`: Incomplete case variant ending prematurely at Send Fine.
- `V0193`: Does not fit any category cleanly as it ends in Send Fine with premature payments.