"""Probe: how much does concurrency-aware variant reduction actually compress GoalCat's Step 1
partition, and would collapsing those classes before Step 6 destroy anything Step 2 measures?

Motivation. Step 1 (extraction/variants.py) partitions traces by *exact* activity sequence, so two
traces that differ only in the interleaving order of genuinely concurrent activities become two
variants — each getting its own LUPIN narrative (Step 3) and its own slot in an LLM assignment
batch (Step 6). If those interleavings can be detected, one delegate per class could be sent to the
LLM and the rest assigned deterministically. This script measures whether that premise holds on our
logs, before any pipeline surgery is attempted. It writes nothing into the pipeline's own run
directories and imports nothing from goalcat: it is a measurement, not a pipeline step.

Method. Interleaving-equivalence is Mazurkiewicz trace equivalence: fix an *independence relation*
over activity labels, and two sequences are equivalent iff one can be rewritten into the other by
repeatedly swapping adjacent independent activities. Equivalence is decided here by canonical form
— the lexicographically smallest linearization of the sequence's dependence graph — so classes are
found by grouping on that form, in one pass, rather than by comparing variant pairs.

Two independence oracles feed that one engine:

  alpha  a || b iff both a>b and b>a hold in the log's directly-follows relation (the classic
         alpha-algorithm concurrency test). Derived from the log alone — no process model, so
         nothing to overfit or degenerate.
  tree   a || b iff the lowest common ancestor of a and b in an Inductive Miner process tree is a
         PARALLEL operator. Model-derived, and the same notion of concurrency that pm4py-ucm's
         choice signatures encode (github.com/ProcessMining-uOttawa/pm4py-ucm), but read off the
         tree's structure instead of replaying every trace through it. That trade matters here:
         full choice-signature replay is that package's dominant cost (~23 min for 4,366 sequences
         on BPI Challenge 2012), and its extra precision is about *which branch a trace took*,
         which is not what a merge decision needs. It also fails gracefully where replay does not:
         on a flower-model fallback there is no PARALLEL node at all, so this oracle reports zero
         independence (no compression) rather than collapsing every trace into one class.

The alpha oracle's known defect is the length-two loop: an "a b a" pattern puts both (a,b) and
(b,a) in the directly-follows relation without a and b being concurrent. --keep-length-two-loops
disables the refinement that excludes those pairs, to show what it costs.

Guard metrics. Compression alone does not justify the merge. Step 2 profiles each variant on
duration, rework, resource and outcome, and outcome is defined as the *last* activity
(extraction/profiling.py) — which is not invariant under interleaving. So for every class with more
than one member the report also counts classes whose members disagree on outcome, and the spread of
their median case durations. Those are the members a propagation guard would have to hold back;
merging them blind would erase exactly the profile-divergent distinctions Step 6's report is built
to surface.

Usage:
    python scripts/concurrency_variant_reduction.py                     # default log set
    python scripts/concurrency_variant_reduction.py --logs rtfm sepsis
    python scripts/concurrency_variant_reduction.py --logs all          # adds bpic2019 (slow)
    python scripts/concurrency_variant_reduction.py --oracle alpha
    python scripts/concurrency_variant_reduction.py --out-dir /tmp/probe   # per-variant CSVs
"""

from __future__ import annotations

import argparse
import heapq
import statistics
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

import pandas as pd
import pm4py
from pm4py.objects.process_tree.obj import Operator

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = REPO_ROOT / "data" / "logs"

# Mirrors src/goalcat/config.yaml's keys — this probe reads logs directly rather than through
# PipelineConfig, so that it can run against a log that has no config or goal model yet.
CASE_ID_KEY = "case:concept:name"
ACTIVITY_KEY = "concept:name"
TIMESTAMP_KEY = "time:timestamp"

# Ordered cheapest-first so an interrupted run has still reported something useful. bpic2019 is
# excluded by default: ~1.6M events, and it is the one log where the tree oracle's mining step is
# itself a multi-minute cost.
DEFAULT_LOGS = ("rtfm_mini", "sepsis", "bpic2020_permit", "rtfm")
ALL_LOGS = DEFAULT_LOGS + ("bpic2019",)

# config.yaml's llm.assignment_batch_size — used only to translate a variant count into the Step 6
# call count it would imply, which is the number the reduction is ultimately trying to move.
ASSIGNMENT_BATCH_SIZE = 50

_EMPTY: frozenset[str] = frozenset()


# ---------------------------------------------------------------------------
# Log loading and variant extraction
# ---------------------------------------------------------------------------

@dataclass
class VariantTable:
    """Step 1's partition, plus the per-variant duration/outcome facts the guard metrics need.

    Produced by a direct groupby rather than by calling goalcat's extract_variants(), which needs a
    full PipelineConfig; the partition is the same one (traces grouped by exact activity sequence,
    events ordered by timestamp), and this probe never needs Step 1's V#### numbering.
    """

    sequences: list[tuple[str, ...]]
    frequencies: list[int]
    #: Median end-to-end case duration in seconds, per variant. NaN when a variant's cases all have
    #: a single event (zero duration is real, so this stays 0.0 rather than NaN in that case).
    median_durations: list[float]
    total_cases: int

    def __len__(self) -> int:
        return len(self.sequences)


def load_variants(log_path: Path) -> VariantTable:
    df = pm4py.read_xes(str(log_path))
    df = df[[CASE_ID_KEY, ACTIVITY_KEY, TIMESTAMP_KEY]].copy()
    # kind="stable" so cases whose events share a timestamp keep their file order, matching what
    # pm4py.split_by_process_variant does in Step 1 — otherwise the variant a case lands in could
    # differ between this probe and the pipeline for no reason but sort instability.
    df = df.sort_values([CASE_ID_KEY, TIMESTAMP_KEY], kind="stable")

    grouped = df.groupby(CASE_ID_KEY, sort=False)
    sequence_by_case = grouped[ACTIVITY_KEY].agg(tuple)
    bounds = grouped[TIMESTAMP_KEY].agg(["min", "max"])
    duration_by_case = (bounds["max"] - bounds["min"]).dt.total_seconds()

    durations_by_sequence: dict[tuple[str, ...], list[float]] = defaultdict(list)
    for case_id, sequence in sequence_by_case.items():
        durations_by_sequence[sequence].append(float(duration_by_case[case_id]))

    sequences = list(durations_by_sequence)
    return VariantTable(
        sequences=sequences,
        frequencies=[len(durations_by_sequence[s]) for s in sequences],
        median_durations=[statistics.median(durations_by_sequence[s]) for s in sequences],
        total_cases=len(sequence_by_case),
    )


# ---------------------------------------------------------------------------
# Independence oracles
# ---------------------------------------------------------------------------

def alpha_independence(
    sequences: list[tuple[str, ...]], exclude_length_two_loops: bool = True
) -> dict[str, frozenset[str]]:
    """a || b iff a is directly followed by b somewhere and b by a somewhere.

    Computed over distinct sequences, not over cases: the directly-follows relation is a set, so a
    pair either occurs or it does not and repeating a sequence cannot add to it.

    exclude_length_two_loops implements the alpha+ refinement. Without it, a genuine "a b a" cycle
    is indistinguishable from concurrency — both put (a,b) and (b,a) in the relation — and every
    such pair becomes a licence to reorder activities that are strictly ordered in reality, which
    would over-merge variants that a business reviewer must keep apart.
    """
    follows: set[tuple[str, str]] = set()
    length_two_loops: set[frozenset[str]] = set()
    for sequence in sequences:
        for i in range(len(sequence) - 1):
            follows.add((sequence[i], sequence[i + 1]))
            if i + 2 < len(sequence) and sequence[i] == sequence[i + 2] and sequence[i] != sequence[i + 1]:
                length_two_loops.add(frozenset((sequence[i], sequence[i + 1])))

    independent: dict[str, set[str]] = defaultdict(set)
    for a, b in follows:
        if a == b or (b, a) not in follows:
            continue
        if exclude_length_two_loops and frozenset((a, b)) in length_two_loops:
            continue
        independent[a].add(b)
        independent[b].add(a)
    return {a: frozenset(bs) for a, bs in independent.items()}


def tree_independence(tree) -> dict[str, frozenset[str]]:
    """a || b iff a and b sit under different children of the same PARALLEL node.

    Equivalent to "the lowest common ancestor of a and b is a PARALLEL operator", but computed
    bottom-up in one post-order walk: each node returns its own label alphabet, and every PARALLEL
    node emits the cross product over each pair of its children's alphabets.

    Labels repeated in two sibling subtrees would be reported as independent with themselves, which
    is never true; the a != b filter below covers that. Inductive Miner partitions the activity
    alphabet at every cut, so this should not arise, but the tree is an input here, not an
    invariant this script controls.
    """
    independent: dict[str, set[str]] = defaultdict(set)

    def walk(node) -> set[str]:
        if not node.children:
            return set() if node.label is None else {node.label}  # label is None for tau
        child_alphabets = [walk(child) for child in node.children]
        if node.operator == Operator.PARALLEL:
            for left, right in combinations(child_alphabets, 2):
                for a in left:
                    for b in right:
                        if a != b:
                            independent[a].add(b)
                            independent[b].add(a)
        return set().union(*child_alphabets)

    walk(tree)
    return {a: frozenset(bs) for a, bs in independent.items()}


# ---------------------------------------------------------------------------
# Mazurkiewicz canonical form
# ---------------------------------------------------------------------------

def canonical_form(
    sequence: tuple[str, ...], independent: dict[str, frozenset[str]]
) -> tuple[str, ...]:
    """The lexicographically smallest sequence reachable by swapping adjacent independent
    activities — a canonical representative of the sequence's interleaving-equivalence class.

    Two sequences are Mazurkiewicz-equivalent exactly when the linearizations of their dependence
    graphs coincide, so the lex-least linearization identifies the class: group variants on this
    value and each group is one class. Computed as a greedy topological sort over the dependence
    graph that always takes the smallest available label. Positions carrying the same label are
    always dependent, so at most one of them is ever available and the tie-break never has to
    choose between two identical labels at different positions.
    """
    alphabet = set(sequence)
    # Fast path: a sequence whose own activities are pairwise dependent admits no reordering at
    # all, so it is its own canonical form. This covers the large majority of variants on a log
    # with little concurrency, and skips the O(len^2) graph build entirely.
    if not any(independent.get(a, _EMPTY) & alphabet for a in alphabet):
        return sequence

    n = len(sequence)
    successors: list[list[int]] = [[] for _ in range(n)]
    in_degree = [0] * n
    for i in range(n):
        independent_with_i = independent.get(sequence[i], _EMPTY)
        for j in range(i + 1, n):
            if sequence[j] not in independent_with_i:  # dependent => i must precede j
                successors[i].append(j)
                in_degree[j] += 1

    available = [(sequence[i], i) for i in range(n) if in_degree[i] == 0]
    heapq.heapify(available)
    ordered: list[str] = []
    while available:
        label, i = heapq.heappop(available)
        ordered.append(label)
        for j in successors[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                heapq.heappush(available, (sequence[j], j))
    return tuple(ordered)


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

@dataclass
class OracleResult:
    oracle: str
    independent_pairs: int
    class_count: int
    #: Canonical form -> member variant indices, for classes with more than one member.
    multi_member_classes: dict[tuple[str, ...], list[int]] = field(default_factory=dict)
    outcome_divergent_classes: int = 0
    duration_divergent_classes: int = 0
    largest_class: int = 1
    cases_in_multi_member_classes: int = 0
    seconds: float = 0.0
    note: str = ""


def _batches(n: int) -> int:
    return -(-n // ASSIGNMENT_BATCH_SIZE)  # ceil


def evaluate_oracle(
    oracle: str,
    independent: dict[str, frozenset[str]],
    variants: VariantTable,
    duration_ratio_threshold: float,
) -> OracleResult:
    started = time.perf_counter()
    classes: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for i, sequence in enumerate(variants.sequences):
        classes[canonical_form(sequence, independent)].append(i)

    multi = {form: members for form, members in classes.items() if len(members) > 1}

    outcome_divergent = 0
    duration_divergent = 0
    for members in multi.values():
        if len({variants.sequences[i][-1] for i in members}) > 1:
            outcome_divergent += 1
        medians = [variants.median_durations[i] for i in members]
        low, high = min(medians), max(medians)
        # A zero low bound would make every ratio infinite; treat "one member is instantaneous and
        # another is not" as divergent directly rather than reporting inf.
        if (low <= 0.0 < high) or (low > 0.0 and high / low >= duration_ratio_threshold):
            duration_divergent += 1

    return OracleResult(
        oracle=oracle,
        independent_pairs=sum(len(bs) for bs in independent.values()) // 2,
        class_count=len(classes),
        multi_member_classes=multi,
        outcome_divergent_classes=outcome_divergent,
        duration_divergent_classes=duration_divergent,
        largest_class=max((len(m) for m in classes.values()), default=0),
        cases_in_multi_member_classes=sum(
            variants.frequencies[i] for members in multi.values() for i in members
        ),
        seconds=time.perf_counter() - started,
    )


def run_log(
    log_stem: str,
    oracles: tuple[str, ...],
    noise_threshold: float,
    exclude_length_two_loops: bool,
    duration_ratio_threshold: float,
    out_dir: Path | None,
) -> tuple[VariantTable, list[OracleResult]] | None:
    log_path = LOGS_DIR / f"{log_stem}.xes.gz"
    if not log_path.exists():
        print(f"  ! {log_path} not found — skipped", file=sys.stderr)
        return None

    started = time.perf_counter()
    variants = load_variants(log_path)
    print(
        f"  loaded {variants.total_cases} cases / {len(variants)} variants "
        f"in {time.perf_counter() - started:.1f}s"
    )

    results: list[OracleResult] = []
    for oracle in oracles:
        if oracle == "alpha":
            independent = alpha_independence(variants.sequences, exclude_length_two_loops)
            note = ""
        else:
            mine_started = time.perf_counter()
            df = pm4py.read_xes(str(log_path))
            tree = pm4py.discover_process_tree_inductive(
                df,
                noise_threshold=noise_threshold,
                activity_key=ACTIVITY_KEY,
                timestamp_key=TIMESTAMP_KEY,
                case_id_key=CASE_ID_KEY,
            )
            independent = tree_independence(tree)
            note = f"IM noise_threshold={noise_threshold}, mined in {time.perf_counter() - mine_started:.1f}s"
            if not independent:
                note += " — no PARALLEL operator in the tree, so no reordering is licensed"
        result = evaluate_oracle(oracle, independent, variants, duration_ratio_threshold)
        result.note = note
        results.append(result)

    if out_dir is not None:
        _write_class_csv(log_stem, variants, results, out_dir)
    return variants, results


def _write_class_csv(
    log_stem: str, variants: VariantTable, results: list[OracleResult], out_dir: Path
) -> None:
    """One row per variant, with the class id each oracle assigned it — enough to inspect which
    variants a merge would actually fold together, and to join back onto a run's variants.csv by
    activity_sequence."""
    out_dir.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(
        {
            "activity_sequence": [">".join(s) for s in variants.sequences],
            "frequency": variants.frequencies,
            "trace_length": [len(s) for s in variants.sequences],
            "outcome": [s[-1] for s in variants.sequences],
            "duration_seconds_median": variants.median_durations,
        }
    )
    for result in results:
        class_of: dict[int, str] = {}
        for class_index, members in enumerate(sorted(result.multi_member_classes.values())):
            for i in members:
                class_of[i] = f"C{class_index + 1:04d}"
        frame[f"{result.oracle}_class_id"] = [class_of.get(i, "") for i in range(len(variants))]
    path = out_dir / f"{log_stem}_concurrency_classes.csv"
    frame.to_csv(path, index=False)
    print(f"  wrote {path}")


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def report(log_stem: str, variants: VariantTable, results: list[OracleResult]) -> None:
    n = len(variants)
    print(f"\n  {log_stem}: {variants.total_cases} cases, {n} variants, "
          f"{_batches(n)} Step 6 calls at batch size {ASSIGNMENT_BATCH_SIZE}")
    header = (
        f"    {'oracle':<7} {'|| pairs':>8} {'classes':>8} {'ratio':>7} {'merged':>7} "
        f"{'largest':>8} {'calls':>6} {'outcome!=':>10} {'dur!=':>7} {'sec':>6}"
    )
    print(header)
    print("    " + "-" * (len(header) - 4))
    for r in results:
        ratio = r.class_count / n if n else 1.0
        merged = n - r.class_count
        print(
            f"    {r.oracle:<7} {r.independent_pairs:>8} {r.class_count:>8} {ratio:>7.3f} "
            f"{merged:>7} {r.largest_class:>8} {_batches(r.class_count):>6} "
            f"{r.outcome_divergent_classes:>10} {r.duration_divergent_classes:>7} {r.seconds:>6.1f}"
        )
    for r in results:
        if r.note:
            print(f"    {r.oracle}: {r.note}")
        if r.multi_member_classes:
            divergent = r.outcome_divergent_classes + r.duration_divergent_classes
            print(
                f"    {r.oracle}: {len(r.multi_member_classes)} multi-member classes covering "
                f"{r.cases_in_multi_member_classes} cases; {divergent} of them would be held back "
                f"by an outcome/duration propagation guard"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--logs", nargs="+", default=list(DEFAULT_LOGS),
                        help=f"log stems under data/logs/, or 'all' for {' '.join(ALL_LOGS)}")
    parser.add_argument("--oracle", nargs="+", choices=["alpha", "tree"], default=["alpha", "tree"])
    parser.add_argument("--noise-threshold", type=float, default=0.0,
                        help="Inductive Miner noise threshold for the tree oracle (default 0.0, "
                             "matching config.yaml's discovery_noise_threshold)")
    parser.add_argument("--keep-length-two-loops", action="store_true",
                        help="disable the alpha+ refinement, letting 'a b a' patterns count as "
                             "concurrency (shows what the refinement is worth)")
    parser.add_argument("--duration-ratio-threshold", type=float, default=10.0,
                        help="a multi-member class counts as duration-divergent when its members' "
                             "median durations differ by at least this factor (default 10x)")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="optional directory for per-variant class-assignment CSVs; nothing "
                             "is written without it")
    args = parser.parse_args()

    log_stems = list(ALL_LOGS) if args.logs == ["all"] else args.logs
    oracles = tuple(args.oracle)

    for log_stem in log_stems:
        print(f"\n=== {log_stem} ===")
        outcome = run_log(
            log_stem,
            oracles,
            args.noise_threshold,
            not args.keep_length_two_loops,
            args.duration_ratio_threshold,
            args.out_dir,
        )
        if outcome is not None:
            report(log_stem, *outcome)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
