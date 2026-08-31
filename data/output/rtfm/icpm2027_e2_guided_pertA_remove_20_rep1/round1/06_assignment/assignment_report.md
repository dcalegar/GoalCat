# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`resolve_timely_payment`)

Represents the prompt settlement of fines by offenders. This pathway advances the softgoal 'Maximize timely fine revenue' (via Make contribution) and 'Minimize administrative & enforcement cost' (via Help contribution), measured against indicator 'Average time to case closure' and 'Time to fine dispatch'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=12. Supported by frequent narrative samples such as variant V0002 and V0007 where payment resolves the case quickly.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49970/150370 cases (33.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.86, nearest other category `resolve_delinquent_payment` at mean distance 5.25

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.322, nearest other category `resolve_delinquent_payment` at mean distance 0.310

## Resolve via delinquent payment (`resolve_delinquent_payment`)

Represents the resolution of cases where payment occurs after penalties or notifications. Advances 'Maximize timely fine revenue' via Help contribution, measured against indicator 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=13. Supported by variants like V0001, V0004, V0009, and V0010 where payments occur after notification and penalty additions or culminate in credit collection.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 42/231 variants (18.2%) · micro 16929/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.45, nearest other category `resolve_administrative_appeal` at mean distance 4.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.232, nearest other category `resolve_timely_payment` at mean distance 0.310

## Resolve via administrative appeal to the Prefecture (`resolve_administrative_appeal`)

Represents the resolution pathway through an administrative appeal lodged with the Prefecture. Advances 'Preserve offender's due-process rights' (Help contribution) while negatively impacting enforcement costs and revenue, judged against 'Time to appeal filing, Prefecture' and 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=14. Supported by sample variants such as V0008, V0057, V0135, and V0137 containing administrative appeal actions.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 88/231 variants (38.1%) · micro 666/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.32, nearest other category `resolve_delinquent_payment` at mean distance 4.91

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.390, nearest other category `resolve_judicial_appeal` at mean distance 0.406

## Resolve via judicial appeal to the Judge (`resolve_judicial_appeal`)

Represents the path where the offender escalates the appeal to a judicial judge. Strongly advances 'Preserve offender's due-process rights' (Make contribution) and incurs cost impacts, evaluated via 'Time to appeal filing, Judge'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative id=19. Supported by variants such as V0103, V0140, V0176, and V0177 where judicial appeals are logged.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 68/231 variants (29.4%) · micro 420/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.64, nearest other category `resolve_administrative_appeal` at mean distance 5.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.396, nearest other category `resolve_administrative_appeal` at mean distance 0.406

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `resolve_judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `resolve_judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.716
- `V0082` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.698
- `V0097` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `resolve_judicial_appeal`): structural=17, profile=0.358

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`resolve_delinquent_payment`) / `V0014` (`resolve_judicial_appeal`): structural=1, profile=0.022
- `V0004` (`resolve_delinquent_payment`) / `V0029` (`resolve_judicial_appeal`): structural=1, profile=0.374
- `V0004` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal`): structural=1, profile=0.030
- `V0004` (`resolve_delinquent_payment`) / `V0116` (`resolve_administrative_appeal`): structural=1, profile=0.025
- `V0005` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal`): structural=1, profile=0.387
- `V0005` (`resolve_delinquent_payment`) / `V0037` (`resolve_judicial_appeal`): structural=1, profile=0.062
- `V0005` (`resolve_delinquent_payment`) / `V0116` (`resolve_administrative_appeal`): structural=1, profile=0.382
- `V0005` (`resolve_delinquent_payment`) / `V0184` (`resolve_judicial_appeal`): structural=1, profile=0.060
- `V0006` (`resolve_delinquent_payment`) / `V0014` (`resolve_judicial_appeal`): structural=1, profile=0.390
- `V0006` (`resolve_delinquent_payment`) / `V0205` (`resolve_judicial_appeal`): structural=1, profile=0.737

## Residual

25/231 variants (10.8%), 82385/150370 cases (54.8%) unassigned.

- `V0001`: This narrative results in sending the fine for credit collection without payment or appeal resolution, falling outside the defined taxonomy categories.
- `V0003`: The process ends at sending the fine with no subsequent resolution, payment, or appeal.
- `V0008`: The process concludes at sending an appeal to the Prefecture without reaching a final resolution or payment.
- `V0009`: Despite an initial payment attempt, the case ultimately ends up sent for credit collection.
- `V0010`: The case ends with credit collection despite intermediate payment and penalties.
- `V0011`: The process stops after sending an appeal to the Prefecture, leaving the case unresolved.
- `V0015`: The narrative terminates at sending an appeal to the Prefecture with no final resolution.
- `V0017`: The case includes a judicial appeal to the Judge but ultimately results in credit collection.
- `V0019`: The administrative appeal process concludes, but the case ultimately goes to credit collection.
- `V0020`: An administrative appeal is processed, but the case ultimately ends in credit collection.
- `V0025`: An administrative appeal takes place, but the final outcome is credit collection.
- `V0026`: Despite early payment, penalties and notifications lead to credit collection.
- `V0040`: Includes a judicial appeal to the Judge, but ends in credit collection.
- `V0043`: The process involves notifications and payments, but ultimately results in credit collection.
- `V0077`: Incomplete or anomalous sequence without a clear resolution outcome like payment or appeal completion.
- `V0160`: The case does not resolve successfully through payment or appeals, ending instead in credit collection.
- `V0161`: The process concludes with credit collection rather than a resolution category like payment or a completed appeal.
- `V0163`: The case terminates in credit collection without achieving a successful resolution through payment or appeal conclusion.
- `V0165`: The process ends in credit collection, failing to resolve via payment or a completed appeal.
- `V0169`: The case is sent for credit collection, not fulfilling any standard resolution category.
- `V0170`: Ends in credit collection despite partial payments and a judicial appeal.
- `V0173`: Terminates in credit collection.
- `V0177`: Ends with credit collection after multiple convoluted appeal paths.
- `V0182`: Ends in credit collection despite undergoing an administrative appeal.
- `V0193`: The process terminates prematurely at 'Send Fine' without reaching a resolution.