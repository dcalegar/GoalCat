# RTFM (mini fixture) Goal Model (Step G) — Road Traffic Fine Management

**Status:** version 1.2, 2026-08-25 — created at v1.2, as a byte-for-byte copy of
`rtfm_goal_model.jucm` except for the `author` attribute, which names this file instead.
**Target log:** `data/logs/rtfm_mini.xes.gz` — the six-case functional-test fixture described in
`experimentation/examples/rtfm_mini/config_mini.yaml`, not the full 150,370-case log.
**Authoritative content:** `rtfmGM_description.md`. This document does **not** restate the goal
model; it records why a second file exists and what must stay true of it.

## 1. Why a separate file

`rtfm_mini` is a development fixture, and a fixture's goal model gets edited for fixture reasons —
to exercise a code path, to force a residual, to make a value set discriminate over six cases rather
than 150,370. Sharing one `.jucm` between the fixture and the full log means every such edit silently
changes the artifact the real results are produced against. Splitting them makes that impossible:
`config_mini.yaml` points here, `config_rtfm.yaml` and `experimentation/icpm2027/configs/rtfm.yaml`
point at `rtfm_goal_model.jucm`.

## 2. The invariant

**The GRL structure must stay identical between the two files.** Same element ids, names and types;
same decomposition tree and operators; same actor; same contribution links. Only the KPI layer may
diverge, and only deliberately.

The reason is that `rtfm_mini` exists to exercise the pipeline that the full log then runs for real.
A fixture whose goal model has drifted structurally stops testing anything: Step 5a would induce a
taxonomy against one axis and the full run against another, and a Step 6 assignment validated on the
fixture would prove nothing about the log. Concretely, the two files currently render an identical
Step 5a prompt excerpt — including the `Goal model:` name line, which is why both carry the name
`RTFM Goal Model` rather than distinguishing themselves there.

Check it, rather than trusting it:

```bash
python - <<'PY'
from goalcat.grl import read_jucm, render_excerpt
a = render_excerpt(read_jucm("data/goals/rtfm_goal_model.jucm"))
b = render_excerpt(read_jucm("data/goals/rtfm_mini_goal_model.jucm"))
print("identical" if a == b else "DIVERGED")
PY
```

That check covers the decomposition tree, the contribution links, the actor list and — since
`render_excerpt()` started rendering indicators on 2026-08-25 — §6's indicator value sets
(name, unit, target/threshold/worst, provenance) and the contribution links originating at them. It
still does not cover the indicators' `goalcat:from`/`goalcat:to` measurement bindings, which the
excerpt deliberately omits per §7's prohibition on lexical pre-matching; compare `§6` of the two
descriptions for those.

## 3. Current divergence

None. The two models are identical apart from `author`. Any future divergence belongs in this
section, with its reason, before it is introduced.

## 4. What this fixture demonstrates about the KPI layer

Worth recording because it is the reason the fixture is useful for Step 7b specifically: its six
hand-picked cases exercise all three ways a measurement can legitimately fail to produce a number,
one case each, which no larger sample makes as easy to inspect.

| Case | Path | What it exercises |
|---|---|---|
| `A10005` | paid the day after issuance | `Time to fine dispatch` is **undefined** — the case never reaches `Send Fine`, because the outcome was *good*. Scoring it as a bad value would invert the measurement. |
| `A31588` | judicial appeal, no ruling in the log | `Average time to case closure` is **right-censored**: no resolving task occurred. |
| four cases | no appeal filed | Both appeal-filing indicators are **not applicable**, which is not the same as unsatisfied and is excluded from the aggregate rather than scored zero. |

`goalcat.indicators` reports these three states separately (`n_no_start`, `n_no_end`,
`n_not_applicable`) alongside a `coverage` figure, so an aggregate over two of six cases never reads
like one over six of six.

## 5. Limitations

Everything §8 of `rtfmGM_description.md` records applies here unchanged — no domain-expert review,
authored contribution weights, an illustrative `worst` bound on the closure KPI. One limitation is
specific to this file: with one case per resolution path, every per-category measurement is a single
observation, not an aggregate. The fixture demonstrates the mechanism; it measures nothing.
