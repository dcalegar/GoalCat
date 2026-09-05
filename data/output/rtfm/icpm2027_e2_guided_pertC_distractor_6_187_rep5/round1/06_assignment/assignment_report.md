# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertC_distractor_6_187_rep5` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment of the fine, advancing the softgoal to maximize timely fine revenue and helping to minimize administrative and enforcement cost, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12 as supported by frequent variants such as V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49696/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.95, nearest other category `delinquent_payment` at mean distance 5.33

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.321, nearest other category `delinquent_payment` at mean distance 0.277

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after penalties or notifications have been processed, helping to maximize timely fine revenue, judged against time to fine dispatch and average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13, evidenced by variants like V0004 and V0006 where payments occur following penalty additions.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 39/231 variants (16.9%) · micro 16828/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.24, nearest other category `administrative_appeal` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.178, nearest other category `timely_payment` at mean distance 0.277

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases resolved through an administrative appeal process directed to the Prefecture, preserving offender's due-process rights while potentially impacting enforcement costs and revenue, measured against time to appeal filing.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14, supported by variants such as V0008 and V0057 containing appeal steps.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 80/231 variants (34.6%) · micro 3906/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.24, nearest other category `delinquent_payment` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.373, nearest other category `delinquent_payment` at mean distance 0.390

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases resolved through a judicial appeal brought before a judge, strongly making the softgoal to preserve offender's due-process rights while hurting minimization of administrative costs, judged against time to appeal filing.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19, evidenced in variants like V0103, V0140, and V0176 involving judicial appeals.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 65/231 variants (28.1%) · micro 510/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.68, nearest other category `administrative_appeal` at mean distance 5.25

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.398, nearest other category `delinquent_payment` at mean distance 0.396

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases resolved by sending the fine for coercive credit collection after enforcement steps, helping revenue but hurting cost minimization, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=20, supported by frequent variants ending in credit collection such as V0001 and V0009.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 37/231 variants (16.0%) · micro 58679/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.20, nearest other category `administrative_appeal` at mean distance 4.87

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.205, nearest other category `judicial_appeal` at mean distance 0.484

## Resolve via fine annulment (`fine_annulment`)

Cases resolved through the formal annulment of the issued fine.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=187 as default from the goal model decomposition.

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
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0018` (`timely_payment`): structural=1, profile=0.367
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387

## Residual

3/231 variants (1.3%), 20751/150370 cases (13.8%) unassigned.

- `V0003`: The case stops at Send Fine without payment, appeal, or collection, falling into the residual.
- `V0012`: The narrative sequence involves payment followed by sending the fine, which does not fit standard trajectories.
- `V0077`: The narrative ends with Send Fine following an appeal process and does not fit any clear resolution category like payment or final appeal closure.