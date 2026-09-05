# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertC_distractor_6_187_rep3` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', evaluated against 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12, supported by frequent variants such as V0002 and V0007 where payment resolves the fine case quickly without requiring coercive enforcement.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 16/231 variants (6.9%) · micro 49600/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.87, nearest other category `delinquent_payment` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.294, nearest other category `delinquent_payment` at mean distance 0.235

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment made after notification or penalties have been applied, contributing to 'Maximize timely fine revenue', measured against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13, evidenced by variants like V0004, V0005, and V0006 where payments occur after fine notifications and added penalties.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 34/231 variants (14.7%) · micro 16978/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.09, nearest other category `timely_payment` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.180, nearest other category `timely_payment` at mean distance 0.235

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving an administrative appeal submitted to the Prefecture, helping preserve the offender's due-process rights while potentially impacting enforcement costs and revenue, measured against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14, supported by variants such as V0008, V0057, and V0135 containing appeal submission and result notification steps.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 78/231 variants (33.8%) · micro 3642/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.34, nearest other category `delinquent_payment` at mean distance 4.80

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.384, nearest other category `delinquent_payment` at mean distance 0.391

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases where an appeal is brought before a judge, strongly advancing due-process rights but incurring costs and delaying fine revenue, measured against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19, evidenced by variants like V0103, V0176, and V0140 containing judicial appeal activities.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 61/231 variants (26.4%) · micro 521/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.76, nearest other category `administrative_appeal` at mean distance 5.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.390, nearest other category `delinquent_payment` at mean distance 0.389

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases escalated to credit collection due to non-payment, contributing to fine revenue while increasing enforcement costs and negatively affecting due-process softgoals, measured against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20, backed by high-frequency and long-duration variants like V0001 and V0009 ending in credit collection dispatch.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 40/231 variants (17.3%) · micro 58882/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.14, nearest other category `administrative_appeal` at mean distance 4.93

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.195, nearest other category `judicial_appeal` at mean distance 0.479

## Resolve via fine annulment (`fine_annulment`)

Cases concluded through the formal annulment of the issued fine, stopping enforcement procedures.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=187 as specified by the goal model decomposition for case resolution alternatives.

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
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0001` (`coercive_credit_collection`) / `V0040` (`judicial_appeal`): structural=1, profile=0.027
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`timely_payment`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: The case ends simply at 'Send Fine' without payment, appeal, or credit collection, falling into the residual.
- `V0012`: The sequence involves an early payment followed by sending the fine later, which does not cleanly fit any single standard category lifecycle.