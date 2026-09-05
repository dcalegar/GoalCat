# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep4` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through payment realization. Advances softgoal Maximize timely fine revenue and helps Minimize administrative and enforcement cost. Evaluated against indicators such as time to fine dispatch (id=112) and average time to case closure (id=114).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12, supported by frequent variants such as V0002 and V0004 where payment occurs directly.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 70/231 variants (30.3%) · micro 66620/150370 cases (44.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.82, nearest other category `administrative_appeal` at mean distance 5.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.199, nearest other category `judicial_appeal` at mean distance 0.400

## Enforced case closure (`enforced_case_closure`)

Resolution of the fine case through enforcement mechanisms and credit collection. Advances timely revenue via penalties but hurts minimization of administrative costs. Evaluated against average time to case closure (id=114).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13 (Merged 13+20), supported by variants like V0001 and V0009 ending in Send for Credit Collection.

**Goal-model linkage:** 13 (Task): Merged 13+20

**Coverage:** macro 32/231 variants (13.9%) · micro 58873/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.26, nearest other category `administrative_appeal` at mean distance 4.77

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.216, nearest other category `judicial_appeal` at mean distance 0.465

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution through an administrative appeal process to the Prefecture. Preserves offender due-process rights (id=14 contribution) while incurring enforcement costs. Judged against indicator time to appeal filing, Prefecture (id=113).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14, evidenced by variants containing Insert Date Appeal to Prefecture and Send Appeal to Prefecture such as V0008 and V0057.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 71/231 variants (30.7%) · micro 3618/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.12, nearest other category `enforced_case_closure` at mean distance 4.77

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.374, nearest other category `judicial_appeal` at mean distance 0.417

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution through a judicial appeal to the Judge. Strongly preserves due-process rights but hurts administrative cost efficiency. Evaluated using time to appeal filing, Judge (id=175).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19, substantiated by samples containing the Appeal to Judge activity such as V0103, V0176, and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 53/231 variants (22.9%) · micro 504/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.56, nearest other category `administrative_appeal` at mean distance 5.17

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.386, nearest other category `timely_payment` at mean distance 0.400

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `judicial_appeal`): structural=16, profile=0.730

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`enforced_case_closure`) / `V0004` (`timely_payment`): structural=1, profile=0.355
- `V0001` (`enforced_case_closure`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`enforced_case_closure`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0001` (`enforced_case_closure`) / `V0040` (`judicial_appeal`): structural=1, profile=0.027
- `V0004` (`timely_payment`) / `V0009` (`enforced_case_closure`): structural=1, profile=0.354
- `V0004` (`timely_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`timely_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`timely_payment`) / `V0009` (`enforced_case_closure`): structural=1, profile=0.711
- `V0005` (`timely_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387

## Residual

5/231 variants (2.2%), 20755/150370 cases (13.8%) unassigned.

- `V0003`: The case only reaches Send Fine and does not achieve final resolution through payment, appeal, or enforcement.
- `V0012`: The case ends with Send Fine without concluding via payment, appeal, or enforcement.
- `V0077`: The outcome is Send Fine, but the case does not reach a final resolution state such as payment or appeal conclusion.
- `V0093`: The case terminates with Send Fine after an initial Appeal to Judge, without a definitive closure or payment outcome.
- `V0193`: The case outcome is Send Fine after payments, representing an anomalous or incomplete sequence that does not fit standard fine resolution categories.