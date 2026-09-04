"""Actor- and model-level GRL satisfaction, computed after the fact from persisted runs.

The pipeline reports satisfaction per intentional element (`07b_indicators/goal_satisfaction.csv`,
one row per element per scope). It does not reduce a scope to a single number, because URN's
Z.151 [itu2018urn] specifies propagation but leaves aggregation to the tool. Fan, Anda and Amyot
close that gap: Eq. 10 of [fan2018arithmetic] aggregates an actor's contained intentional elements,
Eq. 11 aggregates a model's actors, and two supplementary rules cover the unweighted cases --
an actor whose top-level elements carry no positive importance weights has them "weighted equally,
with the weights summing up to 100", and a model whose actors carry no weights treats them alike.

**Nothing is re-run and nothing is re-measured.** Both equations are strictly downstream: they
consume per-element satisfactions and feed nothing back into the propagation of Eqs. 1--4. Every
number this script prints is a function of CSVs that already exist on disk, so the aggregate can be
added to, or dropped from, the analysis without touching a single LLM call or event log.

**What this script found, and why it prints two columns instead of one.** Applied faithfully to
this project's goal models, Eq. 10 is degenerate. Every model in `data/goals/` draws its softgoals
*outside* the actor boundary -- they are stakeholder concerns, not the back-office's own
intentions -- so the actor contains the goal/task tree and the indicators, and its only top-level
element is the root goal. That root sits above a decomposition subtree no indicator seeds, so it
evaluates to 0 in every scope, and the actor score is constant across every scope of every run --
0 on URN's signed range, equivalently 50 once remapped onto the paper's [0, 100], which is the
neutral midpoint rather than the floor. Either way it distinguishes nothing. The elements that do
carry signal, the softgoals fed by indicator contributions, are excluded by exactly the containment
rule Eq. 10 depends on.

So the script reports both, and labels them honestly:

* `actor_*` / `model_*` -- Eqs. 10 and 11 applied over actor-contained top-level elements, with the
  paper's equal-weight default. Structurally faithful in containment and weighting; the arithmetic
  runs on the signed satisfactions this project persists (see **Scales** below).
* `all_roots_*` -- the same weighted mean taken over *every* top-level element regardless of actor
  containment. This is **not** the paper's semantics. It is the number an analyst usually wants,
  and it is reported so that the choice between them is visible and deliberate rather than made
  silently by whichever one got implemented.

Whether the softgoals belong inside the actor is a modelling question -- "preserve the offender's
due-process rights" is arguably the offender's concern, not the Traffic Police Back-Office's --
and this script deliberately does not answer it.

**Scales, and what the `_remapped` columns are not.** Eq. 10 is stated with a clamp to [0, 100];
this project's models declare URN's [-100, 100] range, and that signed scale is what
`goal_satisfaction.csv` holds. This script aggregates the persisted signed satisfactions and then
applies URN's affine remap (`signed / 2 + 50`) to the *aggregate*. It does **not** re-run
propagation on the [0, 100] range, so a `_remapped` column is a post-hoc rescaling of a signed
result, not Eq. 10 recomputed in the paper's units. The two coincide only while no clamp binds
anywhere, which is why `clamp_bound` is reported per row: a bound clamp is exactly the case where
the order of aggregating and rescaling stops being interchangeable. No clamp binds on any run
currently in `data/output/`.

**Refusals.** Importance weights are not parsed by `goalcat.grl`, and no model in `data/goals/`
carries any. Rather than silently applying the equal-weight default to a model that does declare
weights -- which would misreport it -- the script refuses such a model, as it refuses a model with
more than one actor, whose element-to-actor mapping this project does not track beyond the single
enclosing boundary.

Run: `python scripts/aggregate_actor_satisfaction.py [--output PATH] [--root DIR]`
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from goalcat.grl.jucm_io import read_jucm  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

#: URN's signed satisfaction bounds -- the range every model in `data/goals/` declares, and the one
#: the persisted satisfactions are on. The paper's [0, 100] is reached by remapping the aggregate,
#: never by re-running the arithmetic; see this script's docstring.
SIGNED_BOUNDS = (-100.0, 100.0)

_ELEMENT_REF = re.compile(r'<nodes xsi:type="grl:IntentionalElementRef"[^>]*')
_ACTOR_REF = re.compile(r'<contRefs xsi:type="grl:ActorRef"[^>]*')
#: jUCMNav writes importance as a qualitative enum plus a quantitative int; either being present
#: and non-default means the equal-weight rule of [fan2018arithmetic] does not apply.
_IMPORTANCE = re.compile(r'\bimportance="(?!None")[^"]*"|\bimportanceQuantitative="(?!0")[^"]*"')


class Unsupported(Exception):
    """Raised when a model lies outside what the equal-weight default can honestly cover."""


def _containment(raw: str) -> dict[str, str | None]:
    """Maps each intentional element definition id to the id of the actor whose boundary encloses
    its diagram node, or None when the element is drawn outside every actor. Containment lives on
    the *reference* (the node on the graph), not on the definition, which is why this reads the
    diagram rather than the element list."""
    contained: dict[str, str | None] = {}
    for match in _ELEMENT_REF.finditer(raw):
        node = match.group(0)
        definition = re.search(r'\bdef="(\d+)"', node)
        enclosing = re.search(r'\bcontRef="(\d+)"', node)
        if definition:
            contained[definition.group(1)] = enclosing.group(1) if enclosing else None
    return contained


def _roots(model) -> list[str]:
    """Top-level intentional elements: those with no decomposition parent that contribute to
    nothing. The two link types store their endpoints in opposite senses -- a decomposition's `src`
    is the parent and its `dest` the child, while a contribution's `src` is the contributor and its
    `dest` the element contributed to -- so an element is top-level when it is neither the `dest` of
    a decomposition nor the `src` of a contribution."""
    has_parent = {link.dest for link in model.decompositions}
    contributes = {link.src for link in model.contributions}
    return [element_id for element_id in model.elements
            if element_id not in has_parent and element_id not in contributes]


def _weighted_mean(values: list[float], bounds: tuple[float, float]) -> tuple[float, bool]:
    """Eq. 10 under the equal-weight default: n top-level elements each weigh 100/n, so the weights
    sum to exactly 100, `Max(100, sum)` is 100, and the weighted sum reduces to the arithmetic mean.
    Returns the clamped score and whether the clamp actually bound."""
    if not values:
        return float("nan"), False
    raw = sum(values) / len(values)
    low, high = bounds
    clamped = max(low, min(high, raw))
    return clamped, clamped != raw


def _to_paper_scale(signed: float) -> float:
    """The remap URN's `StrategyEvaluationRangeHelper` applies between the two ranges."""
    return signed / 2 + 50


def aggregate_run(csv_path: Path) -> list[dict]:
    """Reduces one `goal_satisfaction.csv` to one row per scope."""
    model_files = sorted(csv_path.parent.glob("*_measured.jucm"))
    if not model_files:
        raise Unsupported(f"no *_measured.jucm beside {csv_path}")
    model_path = model_files[0]
    raw = model_path.read_text()

    actors = _ACTOR_REF.findall(raw)
    if len(actors) > 1:
        raise Unsupported(f"{model_path.name}: {len(actors)} actors; element-to-actor mapping "
                          "beyond a single boundary is not tracked")
    if _IMPORTANCE.search(raw):
        raise Unsupported(f"{model_path.name}: declares importance weights, which goalcat.grl does "
                          "not parse; the equal-weight default would misreport it")

    model = read_jucm(model_path)
    contained = _containment(raw)
    roots = _roots(model)
    actor_roots = [element_id for element_id in roots if contained.get(element_id) is not None]
    excluded = [model.elements[e].name for e in roots if contained.get(e) is None]

    satisfaction = pd.read_csv(csv_path)
    satisfaction["element_id"] = satisfaction["element_id"].astype(str)

    rows = []
    for scope, group in satisfaction.groupby("scope", sort=True):
        by_id = dict(zip(group.element_id, group.satisfaction.astype(float)))
        actor_values = [by_id[e] for e in actor_roots if e in by_id]
        all_values = [by_id[e] for e in roots if e in by_id]

        actor_signed, actor_clamped = _weighted_mean(actor_values, SIGNED_BOUNDS)
        all_signed, all_clamped = _weighted_mean(all_values, SIGNED_BOUNDS)
        # Remap the aggregate, rather than aggregating remapped values: the arithmetic happens once,
        # on the scale the inputs are actually on, and the rescaling is visibly downstream of it.
        actor_remapped = _to_paper_scale(actor_signed)
        all_remapped = _to_paper_scale(all_signed)

        scope_kind = group.scope_kind.iloc[0]
        category = group.category_name.iloc[0]
        rows.append({
            "dataset": csv_path.parts[csv_path.parts.index("output") + 1],
            "run": csv_path.parents[2].name,
            "round": csv_path.parents[1].name,
            "model": model_path.name,
            "scope": scope,
            "scope_kind": scope_kind,
            "category_name": "" if pd.isna(category) else category,
            # Eqs. 10 and 11 as written. With a single unweighted actor Eq. 11 reduces to Eq. 10,
            # so the model score is the actor score; the column is kept to make that explicit.
            "n_actor_roots": len(actor_values),
            "actor_signed": round(actor_signed, 4),
            "actor_remapped": round(actor_remapped, 4),
            "model_signed": round(actor_signed, 4),
            "model_remapped": round(actor_remapped, 4),
            # Not the paper's semantics -- see this script's docstring.
            "n_all_roots": len(all_values),
            "all_roots_signed": round(all_signed, 4),
            "all_roots_remapped": round(all_remapped, 4),
            "clamp_bound": bool(actor_clamped or all_clamped),
            "roots_excluded_by_containment": "; ".join(excluded),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=REPO_ROOT / "data" / "output",
                        help="directory to search for goal_satisfaction.csv (default: data/output)")
    parser.add_argument("--output", type=Path,
                        default=REPO_ROOT / "data" / "output" / "actor_satisfaction.csv",
                        help="where to write the aggregated table")
    args = parser.parse_args()

    csv_paths = sorted(args.root.rglob("07b_indicators/goal_satisfaction.csv"))
    if not csv_paths:
        print(f"No goal_satisfaction.csv found under {args.root}.")
        return 1

    rows: list[dict] = []
    refused: list[str] = []
    for csv_path in csv_paths:
        try:
            rows.extend(aggregate_run(csv_path))
        except Unsupported as reason:
            refused.append(str(reason))

    if not rows:
        print("Every run was refused:")
        for reason in refused:
            print(f"  - {reason}")
        return 1

    table = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output, index=False)

    run_rounds = len(table[["dataset", "run", "round"]].drop_duplicates())
    runs = len(table[["dataset", "run"]].drop_duplicates())
    try:  # a --output anywhere outside the repository is legitimate; just show it whole
        destination = args.output.relative_to(REPO_ROOT)
    except ValueError:
        destination = args.output
    print(f"Aggregated {run_rounds} run-rounds across {runs} runs from {len(csv_paths)} files "
          f"-> {destination} ({len(table)} scope rows)")
    if refused:
        print(f"Refused {len(refused)}:")
        for reason in refused:
            print(f"  - {reason}")

    degenerate = table.groupby("dataset").actor_signed.nunique()
    for dataset, distinct in degenerate.items():
        subset = table[table.dataset == dataset]
        excluded = subset.roots_excluded_by_containment.iloc[0]
        if distinct <= 1:
            note = (f"constant at {subset.actor_signed.iloc[0]:.2f} signed "
                    f"({subset.actor_remapped.iloc[0]:.2f} remapped) — carries no signal")
        else:
            note = f"{distinct} distinct values"
        print(f"\n[{dataset}] Eq. 10 over {subset.n_actor_roots.iloc[0]} actor-contained root(s): {note}")
        if excluded:
            print(f"  excluded by actor containment: {excluded}")
        print(f"  all-roots variant (not the paper's semantics) spans "
              f"[{subset.all_roots_signed.min():.2f}, {subset.all_roots_signed.max():.2f}] signed, "
              f"[{subset.all_roots_remapped.min():.2f}, {subset.all_roots_remapped.max():.2f}] remapped")
    if table.clamp_bound.any():
        print(f"\n{int(table.clamp_bound.sum())} scope rows had a clamp bind; on those the two "
              "scales are not related by the affine remap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
