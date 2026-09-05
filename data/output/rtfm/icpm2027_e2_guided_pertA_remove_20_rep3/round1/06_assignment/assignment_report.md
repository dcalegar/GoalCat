# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep3` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt payment by the offender. This alternative advances the softgoal 'Maximize timely fine revenue' (Make +100) and 'Minimize administrative & enforcement cost' (Help +50), and is judged against the indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id 12. Realized in variants like V0002 where payment occurs shortly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 9/231 variants (3.9%) · micro 49635/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.69, nearest other category `delinquent_payment` at mean distance 5.23

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.301, nearest other category `delinquent_payment` at mean distance 0.316

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment occurring after penalties and enforcement notifications have been applied. This alternative advances the softgoal 'Maximize timely fine revenue' (Help +50), and is judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id 13. Realized in variants like V0004, V0006, and V0009 where payment is preceded by fine notification and penalty addition.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 59/231 variants (25.5%) · micro 17014/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.28, nearest other category `administrative_appeal` at mean distance 4.87

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.265, nearest other category `timely_payment` at mean distance 0.316

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case through an administrative appeal submitted to the Prefecture. This alternative preserves the offender's due-process rights (Help +50) while harming administrative cost (-25) and timely fine revenue (-25). It is judged against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id 14. Realized in variants like V0008, V0057, and V0135 involving the insertion and sending of appeals to the Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 80/231 variants (34.6%) · micro 604/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.52, nearest other category `delinquent_payment` at mean distance 4.87

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.398, nearest other category `judicial_appeal` at mean distance 0.412

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the fine case through a judicial appeal submitted to a Judge. This alternative strongly advances the offender's due-process rights (Make +100) while hurting administrative cost (-50) and timely fine revenue (-25). It is judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id 19. Realized in variants like V0103, V0140, and V0176 where the trace includes an appeal to the Judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 64/231 variants (27.7%) · micro 372/150370 cases (0.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.72, nearest other category `administrative_appeal` at mean distance 5.38

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.404, nearest other category `administrative_appeal` at mean distance 0.412

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

- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019
- `V0005` (`delinquent_payment`) / `V0204` (`judicial_appeal`): structural=1, profile=0.036
- `V0006` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.390
- `V0006` (`delinquent_payment`) / `V0036` (`timely_payment`): structural=1, profile=0.000
- `V0006` (`delinquent_payment`) / `V0060` (`timely_payment`): structural=1, profile=0.006
- `V0006` (`delinquent_payment`) / `V0205` (`judicial_appeal`): structural=1, profile=0.737
- `V0007` (`timely_payment`) / `V0063` (`judicial_appeal`): structural=1, profile=0.354
- `V0007` (`timely_payment`) / `V0154` (`judicial_appeal`): structural=1, profile=0.075

## Residual

19/231 variants (8.2%), 82745/150370 cases (55.0%) unassigned.

- `V0001`: The case ends with Send for Credit Collection without payment or appeal resolution, so it does not fit any of the resolution categories.
- `V0003`: The case stops at Send Fine without any payment or appeal being finalized.
- `V0008`: The process concludes at Send Appeal to Prefecture, meaning the appeal process was initiated but not yet resolved.
- `V0009`: A partial payment occurs, but the final outcome is Send for Credit Collection, which does not fit standard resolution categories.
- `V0010`: The case ultimately ends in Send for Credit Collection despite an early payment attempt.
- `V0011`: The trace ends with Send Appeal to Prefecture without a final resolution.
- `V0012`: The trace concludes with Send Fine after an initial payment, lacking a complete resolution status.
- `V0015`: The trace stops at Send Appeal to Prefecture without a concluded resolution.
- `V0017`: The case features a judicial appeal but ultimately ends in Send for Credit Collection.
- `V0019`: An administrative appeal is processed, but the final outcome is Send for Credit Collection.
- `V0020`: The case involves an administrative appeal but concludes with Send for Credit Collection.
- `V0025`: Despite undergoing an administrative appeal, the case ultimately results in Send for Credit Collection.
- `V0026`: The narrative ends with Send for Credit Collection without any payment or appeal being finalized, which does not fit any of the resolution categories.
- `V0040`: The case ends with Send for Credit Collection after an appeal to the Judge, fitting neither payment nor a successful appeal resolution category.
- `V0043`: The case ultimately results in Send for Credit Collection, making it part of the residual.
- `V0077`: The case involves an administrative appeal sequence but ends prematurely at Send Fine without resolution or payment.
- `V0083`: The sequence involves an early payment followed later by an administrative appeal process, ending inconclusively at Send Appeal to Prefecture.
- `V0086`: The case has an irregular sequence involving an intermediate payment and an administrative appeal step ending at Send Appeal to Prefecture.
- `V0182`: The case goes through administrative appeal processes but ultimately ends in credit collection ('Send for Credit Collection') rather than timely payment, delinquent payment, or a resolved appeal.