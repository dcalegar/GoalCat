# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertC_distractor_6_187_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing the softgoal to maximize timely fine revenue and helping minimize administrative and enforcement costs, judged against time to fine dispatch and case closure indicators.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=12 as supported by frequent variants such as V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49629/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.18, nearest other category `administrative_appeal` at mean distance 5.39

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.312, nearest other category `delinquent_payment` at mean distance 0.255

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved through late payment after reminders and penalties have been applied, helping maximize timely fine revenue while balancing due-process rights, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=13, evidenced by variants like V0004, V0005, and V0006 where payment occurs after penalty insertion.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 40/231 variants (17.3%) · micro 16900/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.76, nearest other category `administrative_appeal` at mean distance 5.07

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.165, nearest other category `timely_payment` at mean distance 0.255

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal submitted to the Prefecture, preserving offender due-process rights at the cost of administrative expense and revenue delay, judged against time to appeal filing.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=14, evidenced by workflow variants featuring appeal insertion, sending, and result notification steps such as V0008, V0057, and V00137.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 80/231 variants (34.6%) · micro 3900/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.83, nearest other category `coercive_credit_collection` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.367, nearest other category `judicial_appeal` at mean distance 0.403

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases where the offender pursues a judicial appeal before a judge, strongly making due-process softgoals while hurting enforcement cost efficiency.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=19, evidenced by narrative traces containing explicit judicial appeal steps such as V0103, V0176, and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 64/231 variants (27.7%) · micro 507/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.70, nearest other category `administrative_appeal` at mean distance 5.15

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.386, nearest other category `delinquent_payment` at mean distance 0.376

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases escalated to coercive collection due to non-payment, helping revenue recovery while increasing enforcement costs and negatively impacting due-process preservation.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=20, supported by frequent high-duration variants ending in credit collection dispatch like V0001.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 36/231 variants (15.6%) · micro 58683/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.19, nearest other category `administrative_appeal` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.191, nearest other category `administrative_appeal` at mean distance 0.487

## Resolve via fine annulment (`fine_annulment`)

Cases resulting in the formal cancellation and annulment of the issued fine.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative id=187 as declared in the goal model decomposition.

**Goal-model linkage:** 187 (Task): Resolve via fine annulment

**Coverage:** macro 0/231 variants (0.0%) · micro 0/150370 cases (0.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a, nearest other category `None` at mean distance n/a

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
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062

## Residual

3/231 variants (1.3%), 20751/150370 cases (13.8%) unassigned.

- `V0003`: The narrative ends at Send Fine without payment, appeal, or credit collection closure.
- `V0012`: Payment happens before sending the fine, forming an unusual sequence not neatly fitting standard completion categories.
- `V0077`: The narrative ends abruptly at Send Fine after an appeal was initiated, without a final resolution like payment or collection.