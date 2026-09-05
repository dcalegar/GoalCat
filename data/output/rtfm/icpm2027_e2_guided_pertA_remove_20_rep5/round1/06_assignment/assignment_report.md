# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep5` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early or timely payment made by the offender. This contributes to maximizing timely fine revenue and minimizing administrative and enforcement costs, and is measured by indicators such as the average time to case closure and time to fine dispatch.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12. Supported by frequent narrative samples such as V0002, V0004, and V0007 where payment occurs directly or after initial dispatch.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 9/231 variants (3.9%) · micro 49629/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.81, nearest other category `delinquent_payment` at mean distance 5.45

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.304, nearest other category `delinquent_payment` at mean distance 0.312

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment occurring after enforcement steps such as penalty addition have been executed. This advances timely fine revenue while interacting with penalty imposition, and performance is evaluated against the average time to case closure indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13. Supported by narratives like V0001, V0009, and V0010 where payments or collections occur after penalty notifications and additions.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 66/231 variants (28.6%) · micro 16972/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.42, nearest other category `administrative_appeal_prefecture` at mean distance 4.95

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.251, nearest other category `timely_payment` at mean distance 0.312

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

Resolution through an administrative appeal submitted to the Prefecture. This preserves the offender's due-process rights while potentially impacting enforcement costs and revenue, measured by statutory indicators such as time to appeal filing in the Prefecture.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14. Supported by variants involving appeal tracking steps directed to the Prefecture, such as V0008, V0057, and V0137.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 91/231 variants (39.4%) · micro 3746/150370 cases (2.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.26, nearest other category `delinquent_payment` at mean distance 4.95

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.374, nearest other category `judicial_appeal_judge` at mean distance 0.407

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

Resolution through a judicial appeal brought before a Judge. Strongly preserves offender due-process rights while incurring costs and affecting revenue, monitored through the judicial appeal filing time indicator.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19. Supported by variants containing judicial appeal activities, such as V0103, V0140, V0151, and V0176.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 53/231 variants (22.9%) · micro 356/150370 cases (0.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.93, nearest other category `administrative_appeal_prefecture` at mean distance 5.43

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.389, nearest other category `administrative_appeal_prefecture` at mean distance 0.407

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.698
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal_judge`): structural=17, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal_prefecture`): structural=1, profile=0.019
- `V0006` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.390
- `V0006` (`delinquent_payment`) / `V0036` (`timely_payment`): structural=1, profile=0.000
- `V0006` (`delinquent_payment`) / `V0205` (`judicial_appeal_judge`): structural=1, profile=0.737
- `V0007` (`timely_payment`) / `V0063` (`judicial_appeal_judge`): structural=1, profile=0.354
- `V0007` (`timely_payment`) / `V0154` (`judicial_appeal_judge`): structural=1, profile=0.075
- `V0008` (`administrative_appeal_prefecture`) / `V0054` (`delinquent_payment`): structural=1, profile=0.361
- `V0011` (`administrative_appeal_prefecture`) / `V0116` (`delinquent_payment`): structural=1, profile=0.392

## Residual

12/231 variants (5.2%), 79667/150370 cases (53.0%) unassigned.

- `V0001`: The narrative ends with Send for Credit Collection, which does not result in payment or an appeal, so it does not fit any of the resolution categories.
- `V0003`: The case ends after Send Fine without a payment or appeal recorded.
- `V0009`: Despite an intermediate payment, the case ultimately ends with Send for Credit Collection, failing to fully resolve through payment or appeal.
- `V0010`: The case ends with Send for Credit Collection after penalty imposition.
- `V0012`: The case concludes with Send Fine after a preliminary payment, representing an incomplete or atypical flow.
- `V0017`: The case includes an appeal to the Judge but ultimately concludes with Send for Credit Collection rather than resolution.
- `V0019`: Although an administrative appeal to the Prefecture takes place, the final outcome is Send for Credit Collection.
- `V0020`: Includes an administrative appeal to the Prefecture but ends with Send for Credit Collection.
- `V0025`: Involves an administrative appeal to the Prefecture but ultimately ends in Send for Credit Collection.
- `V0026`: The case results in sending for credit collection after a penalty was added, which does not fit timely payment, delinquent payment, or any appeal category.
- `V0040`: The case ends with sending for credit collection after a judicial appeal, which does not resolve via payment or appeals.
- `V0043`: The case results in credit collection after a penalty was added, fitting none of the target categories.