"""k-replicate aggregation for the paper's setup and divergence tables.

`report.py` is a *two*-replicate instrument by construction: its driver
(`run_experiment.py`, `replicates = protocol.replicates.get("unperturbed", 2)`) computes coverage
and contingency on replicate 1 and divergence on the rep1/rep2 pair, which is what the frozen
protocol prescribed. The guided arm was subsequently extended to five replicates on RTFM and on
both Sepsis axes (§4), and the paper reports means with min--max ranges over every completed
replicate and over all $\\binom{5}{2}$ guided pairs. Nothing emitted those aggregates, so the two
headline tables could not be regenerated from the package (review item R1); the `guided_no_sample`
ablation likewise appeared in no committed artifact (item R2).

This module closes both. It recomputes, from the frozen run directories alone and with no LLM call:

* the **setup table** --- $|T^G|$, $n$, and residual variant/case percentages as mean [min--max]
  over the $n$ guided replicates of each axis, plus the same rows for the open and
  `guided_no_sample` arms;
* the **divergence table** --- AMI over every unordered within-arm replicate pair and every
  cross-arm pair, under both weightings, with the residual as its own block.

Replicate discovery is by run directory: a condition counts when `ConditionSpec.run_dir` holds a
taxonomy and an `assignments.csv`, so the emitted $n$ is what was executed, never a configured
expectation. The pairs within an arm are not independent (they share replicates), so a range over
them is descriptive, exactly as §4 states; note also that a min--max range widens with the number
of draws, so ranges over unequal $n$ are not directly comparable (review item M15).

Usage::

    python -m experimentation.icpm2027.analysis.aggregate_tables [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Iterator

import pandas as pd

from goalcat.config import REPO_ROOT, TAXONOMY_DIRNAME, VARIANTS_DIRNAME

from ..protocol import ConditionSpec, DatasetSpec
from .coverage import CoverageReport, compute_coverage
from .divergence import compute_divergence

#: Dataset ids in the order the paper's tables list them, and the display names it uses.
DATASETS: tuple[str, ...] = ("rtfm", "sepsis", "bpic2019")
LOG_LABELS = {"rtfm": "RTFM", "sepsis": "Sepsis", "bpic2019": "BPIC 2019"}
AXIS_LABELS = {"resolution": "resolution", "admission": "admission", "discharge": "discharge",
               "matching_regime": "matching regime"}

#: The arms the tables cover, in reporting order. `guided_no_sample` is the Task C11a ablation.
ARMS: tuple[str, ...] = ("guided", "open", "guided_no_sample")

#: Task D1's pre-registered convention. Both weightings are reported (the paper prints both
#: blocks); the residual is its own cluster in each.
RESIDUAL_HANDLING = "own_cluster"
WEIGHTINGS: tuple[str, ...] = ("variant", "case")

#: Discovery ceiling. Nothing in the design runs more than five replicates of a condition; the
#: cap only bounds the probe loop.
MAX_REPLICATES = 10

RESULTS_DIR = REPO_ROOT / "data" / "output" / "icpm2027_results"


@dataclass(frozen=True)
class Run:
    """One executed condition, with the three frames every metric below is computed from."""

    condition: ConditionSpec
    assignments: pd.DataFrame
    variants: pd.DataFrame
    category_count: int

    @property
    def label(self) -> str:
        return f"{self.condition.arm} rep{self.condition.replicate}"

    @property
    def coverage(self) -> CoverageReport:
        return compute_coverage(self.assignments, self.variants, self.label)


@dataclass
class AxisRuns:
    """Every executed run of one (dataset, axis) cell, grouped by arm."""

    dataset: DatasetSpec
    axis: str
    by_arm: dict[str, list[Run]] = field(default_factory=dict)

    @property
    def log_label(self) -> str:
        return LOG_LABELS.get(self.dataset.dataset_id, self.dataset.dataset_id)

    @property
    def axis_label(self) -> str:
        return AXIS_LABELS.get(self.axis, self.axis)


def _load_run(condition: ConditionSpec) -> Run | None:
    """The run if it is on disk and complete enough to measure, else None.

    Deliberately independent of `conditions.already_complete()`: that predicate exists to decide
    whether a *driver* should re-bill a condition, and it reads the full variant population to do
    it. Here the question is only whether frozen artifacts exist to aggregate.
    """
    round_dir = condition.run_dir / "round1"
    assignments_path = round_dir / "06_assignment" / "assignments.csv"
    taxonomy_path = round_dir / TAXONOMY_DIRNAME / "taxonomy.json"
    variants_path = condition.run_dir / VARIANTS_DIRNAME / "variants.csv"
    if not (assignments_path.exists() and taxonomy_path.exists() and variants_path.exists()):
        return None

    assignments = pd.read_csv(assignments_path, usecols=["variant_id", "category_id"], dtype=str)
    variants = pd.read_csv(variants_path, usecols=["variant_id", "frequency"])
    taxonomy = json.loads(taxonomy_path.read_text())
    return Run(
        condition=condition,
        assignments=assignments,
        variants=variants,
        category_count=len(taxonomy.get("categories", [])),
    )


def discover(dataset_ids: tuple[str, ...] = DATASETS) -> Iterator[AxisRuns]:
    """Every (dataset, axis) cell with the runs that actually executed, in reporting order.

    The open arm carries no axis (`ConditionSpec.effective_axis` normalizes it away), so one open
    run is the comparator for every axis of a multi-axis dataset --- Sepsis's two axes therefore
    both cite the same pair of open replicates, which is precisely how the paper reports them.
    """
    for dataset_id in dataset_ids:
        dataset = DatasetSpec.load(dataset_id)
        for axis in dataset.axes:
            cell = AxisRuns(dataset=dataset, axis=axis)
            for arm in ARMS:
                runs = []
                for replicate in range(1, MAX_REPLICATES + 1):
                    condition = ConditionSpec(
                        dataset=dataset, arm=arm, replicate=replicate, experiment="e1", axis=axis
                    )
                    run = _load_run(condition)
                    if run is None:
                        break
                    runs.append(run)
                if runs:
                    cell.by_arm[arm] = runs
            yield cell


# --------------------------------------------------------------------------------------------
# Aggregation


def _spread(values: list[float]) -> dict[str, float | int]:
    return {
        "n": len(values),
        "mean": sum(values) / len(values) if values else float("nan"),
        "min": min(values) if values else float("nan"),
        "max": max(values) if values else float("nan"),
    }


def coverage_spread(runs: list[Run]) -> dict[str, object]:
    """Residual percentages over an arm's replicates, plus the invariants the table asserts.

    `category_counts` and the variant/case totals are returned as the *set* of observed values:
    the paper reports $|T^G|$ without a range on the strength of its being invariant across
    replicates, and that has to be re-derived here rather than assumed.
    """
    reports = [run.coverage for run in runs]
    return {
        "n": len(runs),
        "category_counts": sorted({run.category_count for run in runs}),
        "total_variants": sorted({r.total_variants for r in reports}),
        "total_cases": sorted({r.total_cases for r in reports}),
        "residual_variants_pct": _spread([r.residual_variant_count / r.total_variants * 100 for r in reports]),
        "residual_cases_pct": _spread([r.residual_case_count / r.total_cases * 100 for r in reports]),
        "per_replicate": [
            {
                "replicate": run.condition.replicate,
                "categories": run.category_count,
                "residual_variants_pct": r.residual_variant_count / r.total_variants * 100,
                "residual_cases_pct": r.residual_case_count / r.total_cases * 100,
            }
            for run, r in zip(runs, reports)
        ],
    }


def _ami(left: Run, right: Run, weighting: str) -> float:
    """AMI of two runs' partitions under one weighting, residual as its own block.

    `compute_divergence` returns all four (residual_handling, weighting) combinations; the one
    selected here is Task D1's residual convention at the requested weighting. The variant
    population is the left run's --- both runs of any pair drew Steps 1--4 from the same shared
    base, so the two frames agree.
    """
    result = compute_divergence(
        left.assignments, right.assignments, left.variants, left.label, right.label,
        primary_residual_handling=RESIDUAL_HANDLING, primary_weighting=weighting,
    )
    score = result.primary
    return score.ami


def pair_spread(left_runs: list[Run], right_runs: list[Run], weighting: str, *, within: bool) -> dict[str, object]:
    """AMI over every pair: the $\\binom{n}{2}$ unordered ones within an arm, or the $n\\times m$
    cross-arm ones. Pairs sharing a replicate are not independent, so the range is descriptive."""
    pairs: list[tuple[Run, Run]]
    if within:
        pairs = list(combinations(left_runs, 2))
    else:
        pairs = [(left, right) for left in left_runs for right in right_runs]
    observations = [
        {
            "pair": [left.condition.replicate, right.condition.replicate],
            "ami": _ami(left, right, weighting),
        }
        for left, right in pairs
    ]
    return {**_spread([o["ami"] for o in observations]), "pairs": observations}


def aggregate(cells: list[AxisRuns]) -> dict[str, object]:
    """The full recomputation: one record per (dataset, axis), with every arm and every pairing."""
    axes = []
    for cell in cells:
        guided = cell.by_arm.get("guided", [])
        open_arm = cell.by_arm.get("open", [])
        no_sample = cell.by_arm.get("guided_no_sample", [])

        divergence: dict[str, dict[str, object]] = {}
        for weighting in WEIGHTINGS:
            entry: dict[str, object] = {}
            if len(guided) >= 2:
                entry["guided_guided"] = pair_spread(guided, guided, weighting, within=True)
            if len(open_arm) >= 2:
                entry["open_open"] = pair_spread(open_arm, open_arm, weighting, within=True)
            if guided and open_arm:
                entry["guided_vs_open"] = pair_spread(guided, open_arm, weighting, within=False)
            if guided and no_sample:
                entry["guided_vs_no_sample"] = pair_spread(guided, no_sample, weighting, within=False)
            if len(no_sample) >= 2:
                entry["no_sample_no_sample"] = pair_spread(no_sample, no_sample, weighting, within=True)
            divergence[weighting] = entry

        axes.append({
            "dataset": cell.dataset.dataset_id,
            "log": cell.log_label,
            "axis": cell.axis,
            "axis_label": cell.axis_label,
            "coverage": {arm: coverage_spread(runs) for arm, runs in cell.by_arm.items()},
            "divergence": divergence,
        })

    return {
        "conventions": {
            "residual_handling": RESIDUAL_HANDLING,
            "weightings": list(WEIGHTINGS),
            "note": (
                "Recomputed from the frozen run directories. Within-arm pairs share replicates and "
                "are not independent; a min-max range also widens with the number of pairs, so "
                "ranges over unequal n are descriptive and not directly comparable."
            ),
        },
        "axes": axes,
    }


# --------------------------------------------------------------------------------------------
# Rendering


def _fmt(spread: dict[str, object], decimals: int, suffix: str = "") -> str:
    """`mean [min--max]`, collapsed to a bare value when the range vanishes at this precision ---
    the same convention the paper's captions declare."""
    mean, low, high = float(spread["mean"]), float(spread["min"]), float(spread["max"])
    body = f"{mean:.{decimals}f}{suffix}"
    if f"{low:.{decimals}f}" == f"{high:.{decimals}f}":
        return body
    return f"{body} [{low:.{decimals}f}--{high:.{decimals}f}]"


def _one(values: list, what: str, where: str) -> object:
    """The single observed value, or a loud marker when the invariant the table asserts fails."""
    if len(values) == 1:
        return values[0]
    return f"NOT INVARIANT ({what} in {where}: {values})"


def render_markdown(data: dict) -> str:
    lines = [
        "# Aggregated multi-replicate tables (setup and divergence)",
        "",
        "Recomputed from the frozen run directories by "
        "`experimentation/icpm2027/analysis/aggregate_tables.py`; no LLM call is made. Ranges are "
        "min--max over the replicates (or replicate pairs) that executed and are descriptive: "
        "within-arm pairs share replicates and are not independent, and a min--max range widens "
        "with the number of draws, so ranges over unequal $n$ are not directly comparable.",
        "",
        "## Setup — categories and residual, per arm",
        "",
        "| Log | Axis | Arm | Variants | Cases | \\|T\\| | n | Residual (var.) | Residual (cases) |",
        "|---|---|---|---:|---:|---:|---:|---|---|",
    ]
    for axis in data["axes"]:
        for arm in ARMS:
            cov = axis["coverage"].get(arm)
            if cov is None:
                continue
            where = f"{axis['log']}/{axis['axis_label']}/{arm}"
            lines.append(
                f"| {axis['log']} | {axis['axis_label']} | `{arm}` | "
                f"{_one(cov['total_variants'], 'variants', where)} | "
                f"{_one(cov['total_cases'], 'cases', where)} | "
                f"{_one(cov['category_counts'], '|T|', where)} | {cov['n']} | "
                f"{_fmt(cov['residual_variants_pct'], 1, '%')} | "
                f"{_fmt(cov['residual_cases_pct'], 1, '%')} |"
            )

    pairings = [
        ("guided_guided", "guided--guided"),
        ("open_open", "open--open"),
        ("guided_vs_open", "guided vs. open"),
        ("guided_vs_no_sample", "guided vs. no-sample"),
        ("no_sample_no_sample", "no-sample--no-sample"),
    ]
    lines += ["", "## Divergence — AMI, residual as its own block", ""]
    for weighting in WEIGHTINGS:
        lines += [
            f"### {weighting.capitalize()}-weighted",
            "",
            "| Log | Axis | " + " | ".join(label for _, label in pairings) + " |",
            "|---|---|" + "---|" * len(pairings),
        ]
        for axis in data["axes"]:
            entry = axis["divergence"][weighting]
            cells = []
            for key, _ in pairings:
                spread = entry.get(key)
                cells.append(f"{_fmt(spread, 2)} (n={spread['n']})" if spread else "—")
            lines.append(f"| {axis['log']} | {axis['axis_label']} | " + " | ".join(cells) + " |")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_latex(data: dict) -> str:
    """The two tables in the manuscript's own shape: guided-only setup rows, and the divergence
    table's three columns split into a variant-weighted and a case-weighted block."""
    out = [
        "% Regenerated by experimentation/icpm2027/analysis/aggregate_tables.py — do not hand-edit.",
        "% Table: evaluation logs and the intent-guided partition (guided arm only).",
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Log & Axis & Variants & Cases & $|T^G|$ & $n$ & Residual (var.) & Residual (cases) \\\\",
        "\\midrule",
    ]
    for axis in data["axes"]:
        cov = axis["coverage"].get("guided")
        if cov is None:
            continue
        where = f"{axis['log']}/{axis['axis_label']}/guided"
        variants = _one(cov["total_variants"], "variants", where)
        cases = _one(cov["total_cases"], "cases", where)
        cases_tex = f"{cases:,}".replace(",", "{,}") if isinstance(cases, int) else cases
        variants_tex = f"{variants:,}".replace(",", "{,}") if isinstance(variants, int) else variants
        out.append(
            f"{axis['log']} & {axis['axis_label']} & {variants_tex} & {cases_tex} & "
            f"{_one(cov['category_counts'], '|T^G|', where)} & {cov['n']} & "
            f"{_fmt(cov['residual_variants_pct'], 1)}\\% & {_fmt(cov['residual_cases_pct'], 1)}\\% \\\\"
        )
    out += ["\\bottomrule", "\\end{tabular}", "", "% Table: partition divergence (AMI).",
            "\\begin{tabular}{llccc}", "\\toprule",
            "Log & Axis & Guided--guided & Open--open & Guided vs.\\ open \\\\", "\\midrule"]
    for index, weighting in enumerate(WEIGHTINGS):
        if index:
            out.append("\\addlinespace")
        out.append(f"\\multicolumn{{5}}{{l}}{{\\emph{{{weighting.capitalize()}-weighted}}}} \\\\")
        for axis in data["axes"]:
            entry = axis["divergence"][weighting]
            cells = [
                _fmt(entry[key], 2) if key in entry else "---"
                for key in ("guided_guided", "open_open", "guided_vs_open")
            ]
            out.append(f"{axis['log']} & {axis['axis_label']} & " + " & ".join(cells) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=RESULTS_DIR,
                        help="Directory for aggregate_tables.{json,md,tex} (default: the frozen results dir).")
    parser.add_argument("--dataset", action="append", choices=list(DATASETS),
                        help="Restrict to one dataset (repeatable). Default: all three.")
    args = parser.parse_args(argv)

    dataset_ids = tuple(args.dataset) if args.dataset else DATASETS
    cells = [cell for cell in discover(dataset_ids) if cell.by_arm]
    if not cells:
        print("No executed conditions found under data/output/ — nothing to aggregate.", file=sys.stderr)
        return 1

    data = aggregate(cells)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "aggregate_tables.json").write_text(json.dumps(data, indent=2) + "\n")
    (args.out / "aggregate_tables.md").write_text(render_markdown(data))
    (args.out / "aggregate_tables.tex").write_text(render_latex(data))
    print(render_markdown(data))
    print(f"Wrote aggregate_tables.{{json,md,tex}} to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
