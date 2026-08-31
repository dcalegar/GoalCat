"""In-memory GRL model — the subset of `grl.ecore`/`urncore.ecore` these goal models use.

Every field name and enum literal here matches the real metamodel (fetched from jUCMNavPlus:
`seg.jUCMNav/src/seg/jUCMNav/emf/{grl,urncore}.ecore`), not an invented shorthand:

- `IntentionalElementType` = grl.ecore's `IntentionalElementType` EEnum (`Softgoal`, `Goal`,
  `Task`, `Ressource` — that spelling, not "Resource", is the metamodel's own; `Indicator`).
- `DecompositionType` = grl.ecore's `DecompositionType` EEnum (`And`, `Or`, `Xor`).
- `ContributionType` = grl.ecore's `ContributionType` EEnum (`Make`, `Help`, `SomePositive`,
  `Unknown`, `SomeNegative`, `Hurt`, `Break`).
- `IntentionalElement.id` = `URNmodelElement.id` (EString) — the model's only stable identifier.
  These goal models use plain ascending integers ("2", "3", ...), *not* the short mnemonic codes
  (`TP`, `TB`, `G0`, ...) a reader sees in prose — those mnemonics are prose-only convenience, not
  part of the GRL model. `anchor_ids` (Step 5a's `Category.anchor_ids`) therefore reference these
  numeric ids directly; `prompt.py`'s rendered excerpt shows each element's id next to its name so
  an LLM has both.

This module holds structure only — no XMI parsing (`jucm_io.py`) and no LLM-prompt rendering
(`prompt.py`), so a caller that already has a `GRLModel` in hand (e.g. after a perturbation) never
needs to round-trip through text to use it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

IntentionalElementType = Literal["Softgoal", "Goal", "Task", "Ressource", "Indicator"]
DecompositionType = Literal["And", "Or", "Xor"]
ContributionType = Literal["Make", "Help", "SomePositive", "Unknown", "SomeNegative", "Hurt", "Break"]

#: grl.ecore's ContributionType EEnum literal -> its standard qualitative weight (Amyot et al.,
#: 2022 IMS example convention, also documented in prose form in every goal model's own §5).
CONTRIBUTION_WEIGHT: dict[str, int] = {
    "Make": 100,
    "Help": 50,
    "SomePositive": 25,
    "Unknown": 0,
    "SomeNegative": -25,
    "Hurt": -50,
    "Break": -100,
}


class AxisError(ValueError):
    """A goal model does not declare a single categorization axis.

    Raised by `GRLModel.axis_frontier()` when a subtree contains several independent Or/Xor
    frontiers joined by an And decomposition. Its own type (rather than a bare `ValueError`) so
    the experimentation harness can distinguish "this model cannot be used this way" from an
    ordinary bad argument and report it as a modeling problem.
    """


@dataclass
class ActorDef:
    """grl.ecore's `Actor` (the `URNmodelElement.id`/`name` pair only — this project's goal
    models never populate `Actor.importance`/`count`, and layout-only `ActorRef` fields live in
    the XMI's `urndef` diagram layer, not here)."""

    id: str
    name: str


@dataclass
class IntentionalElement:
    """grl.ecore's `IntentionalElement` (a `Goal`/`Task`/`Softgoal`/`Ressource`, or `Indicator`
    for the `grl.ecore`'s `Indicator` subtype, kept separately as `KPIIndicator`).

    `decomposition_type` is set only when this element has children (via an outgoing
    `Decomposition` link) — a leaf task carries `None`, matching the metamodel's own optional
    `decompositionType` attribute rather than defaulting it to a value that would assert a
    decomposition the element doesn't have.
    """

    id: str
    name: str
    type: IntentionalElementType
    decomposition_type: DecompositionType | None = None
    description: str | None = None
    #: `urncore.ecore`'s `URNmodelElement.metadata` — a containment list of `Metadata` (name/value)
    #: pairs every URN tool may annotate an element with; jUCMNav stamps `_numEval`/`_qualEval`
    #: there itself after running a strategy. Flattened to a dict because every key this project
    #: reads or writes is single-valued (`goalcat.grl.measures`' `goalcat:*` measurement binding);
    #: a model that repeated a name would keep only its last occurrence.
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class DecompositionLink:
    """grl.ecore's `Decomposition` (an `ElementLink` subtype), oriented **parent -> child**: `src`
    is the decomposed element, `dest` one of its parts. `id` is the link's own XMI id, distinct
    from either endpoint's.

    That is this dataclass's convention, not the wire format's. GRL itself orients a decomposition
    link the other way — the part is `src` and the whole is `dest`, which is what makes
    jUCMNav's own propagation work (`QuantitativeGRLStrategyAlgorithm.getEvaluation()` walks an
    element's `linksDest` and reads each `link.src`'s satisfaction, so an And-decomposed parent can
    only take the minimum over its children if the children are the sources). `jucm_io.py`
    translates on both read and write; nothing above it needs to think about the flip, and
    `children_of()`/`parent_of()` read naturally as a result.
    """

    id: str
    src: str
    dest: str


@dataclass
class ContributionLink:
    """grl.ecore's `Contribution` (an `ElementLink` subtype): `src` contributes to `dest`'s
    satisfaction at the given qualitative/quantitative strength."""

    id: str
    src: str
    dest: str
    contribution: ContributionType
    quantitative: int | None = None


@dataclass
class KPIEvalPoint:
    """grl.ecore's `KPIEvalValueSet`, attached to one `Evaluation` of one `Indicator` inside an
    `EvaluationStrategy` — this project's goal models use exactly one strategy/evaluation per
    indicator (a single frozen baseline), so this is kept flat rather than modeling the full
    strategies/groups hierarchy `grl.ecore` allows."""

    target: float | None
    threshold: float | None
    worst: float | None
    unit: str | None
    qualitative_evaluation_value: str | None


@dataclass
class KPIIndicator:
    """grl.ecore's `Indicator` (an `IntentionalElement` subtype) plus its `KPIEvalValueSet`,
    joined here since every caller that wants one wants both."""

    id: str
    name: str
    group_id: str | None
    group_name: str | None
    eval_point: KPIEvalPoint | None


@dataclass
class GRLModel:
    """One parsed `.jucm` file's GRL content — `grlspec` only, never the `urndef` diagram layer
    (pure layout, irrelevant to what Step 5a/6 need or to what a perturbation changes semantically;
    `jucm_io.write_jucm()` regenerates a fresh, schema-valid diagram layer on write rather than
    ever reading one back in).
    """

    source_path: str
    name: str
    author: str | None
    urn_version: str | None
    spec_version: str | None
    next_global_id: int
    elements: dict[str, IntentionalElement] = field(default_factory=dict)
    actors: dict[str, ActorDef] = field(default_factory=dict)
    decompositions: list[DecompositionLink] = field(default_factory=list)
    contributions: list[ContributionLink] = field(default_factory=list)
    indicators: dict[str, KPIIndicator] = field(default_factory=dict)
    #: Verbatim XML of grlspec's KPI-related children (indicatorGroup/groups/strategies/
    #: impactModel/featureModel), for round-tripping on write — see jucm_io.py's module
    #: docstring for why this content is passed through rather than reconstructed from
    #: `indicators`.
    kpi_raw_xml: str | None = None

    def element(self, element_id: str) -> IntentionalElement:
        if element_id not in self.elements:
            raise KeyError(
                f"No intentional element with id={element_id!r} in {self.source_path} "
                f"(declared ids: {sorted(self.elements, key=_int_sort_key)})"
            )
        return self.elements[element_id]

    def children_of(self, parent_id: str) -> list[str]:
        """Child element ids for `parent_id`'s outgoing `Decomposition` links, in link order
        (this project's `.jucm` files always write them in document/id order, which is what a
        reader sees as the decomposition's declared order)."""
        return [link.dest for link in self.decompositions if link.src == parent_id]

    def parent_of(self, child_id: str) -> str | None:
        for link in self.decompositions:
            if link.dest == child_id:
                return link.src
        return None

    def declared_alternatives(self) -> dict[str, list[str]]:
        """{parent_id: [alternative ids...]} for every Or/Xor-decomposed element — the same
        concept `experimentation/icpm2027/goalmodel/parse.py`'s markdown-based predecessor
        computed from §4's OR/XOR rows, now read from the model's own `decomposition_type`
        rather than inferred from table text."""
        out: dict[str, list[str]] = {}
        for element in self.elements.values():
            if element.decomposition_type in ("Or", "Xor"):
                children = self.children_of(element.id)
                if children:
                    out[element.id] = children
        return out

    def or_points_below(self, element_id: str) -> list[str]:
        """The *topmost* Or/Xor-decomposed elements at or below `element_id`, in document order.

        "Topmost" means the recursion stops at the first Or/Xor point on each branch rather than
        collecting every one: `axis_frontier()` needs to know how many independent decision
        frontiers a subtree contains, and a frontier nested *inside* another one (RTFM's Xor 7
        inside Or 6 inside Or 4) is part of that same frontier, not a second one.

        Returns `[element_id]` itself when `element_id` is Or/Xor-decomposed.
        """
        element = self.elements.get(element_id)
        if element is None:
            return []
        if element.decomposition_type in ("Or", "Xor") and self.children_of(element_id):
            return [element_id]
        found: list[str] = []
        for child_id in self.children_of(element_id):
            found.extend(self.or_points_below(child_id))
        return found

    def axis_frontier(self, axis_root: str | None = None) -> list[str]:
        """The categorization axis a goal model declares: the alternatives reachable from
        `axis_root` through Or/Xor decompositions, in document order.

        This is the set `Category.anchor_ids` may legally name — narrower than `declared_ids()`
        (`prompt.py`), which is only the set of ids that *resolve*. Descent rules:

        - An Or/Xor point contributes its children.
        - A child that contains exactly one Or/Xor point below it is not itself a frontier element;
          the recursion descends into that point instead. This is what puts RTFM's `13/14/19/20`
          rather than the And-decomposed `5` on the frontier.
        - A child with no Or/Xor point below it is a frontier element, whether it is a leaf task
          (RTFM `12`) or itself And-decomposed into mandatory sub-steps (BPIC `5`, `6`, `7`).

        Raises `AxisError` when the subtree contains several *independent* Or/Xor frontiers joined
        by an And decomposition. That is not a partition: a case realizes one alternative from each
        frontier, so no single label can describe it. Sepsis is exactly this shape — its root And
        joins `5` (admission) and `6` (discharge) — and each frontier must be declared as its own
        axis. See ITU-T Z.151: `Xor` is "one and only one", `Or` is inclusive, and neither operator
        makes the union of two frontiers exclusive.

        With `axis_root` omitted, the model must declare exactly one topmost Or/Xor point, which is
        used as the root; a model with several (Sepsis) raises rather than guessing.
        """
        if axis_root is None:
            child_ids = {link.dest for link in self.decompositions}
            roots = [
                element.id
                for element in self.elements.values()
                if element.id not in child_ids and element.type not in ("Softgoal", "Indicator")
            ]
            tops: list[str] = []
            for root_id in roots:
                tops.extend(self.or_points_below(root_id))
            if not tops:
                raise AxisError(
                    f"{self.source_path} declares no Or/Xor decomposition, so it declares no "
                    "categorization axis. An unset GRL decompositionType defaults to And."
                )
            if len(tops) > 1:
                raise AxisError(
                    f"{self.source_path} declares {len(tops)} independent Or/Xor frontiers "
                    f"({', '.join(f'{i} ({self.element(i).name!r})' for i in tops)}) joined by an "
                    "And decomposition, so it has no single axis. Pass axis_root to choose one; "
                    "each frontier is its own axis and must be run separately."
                )
            axis_root = tops[0]

        root_element = self.element(axis_root)
        if root_element.decomposition_type not in ("Or", "Xor"):
            tops = self.or_points_below(axis_root)
            if len(tops) != 1:
                raise AxisError(
                    f"axis_root={axis_root!r} ({root_element.name!r}) is "
                    f"{root_element.decomposition_type or 'un'}-decomposed and contains "
                    f"{len(tops)} Or/Xor frontiers ({', '.join(tops) or 'none'}); an axis root must "
                    "resolve to exactly one."
                )
            axis_root = tops[0]

        frontier: list[str] = []
        self._collect_frontier(axis_root, frontier, set())
        return frontier

    def _collect_frontier(self, or_point_id: str, out: list[str], visited: set[str]) -> None:
        if or_point_id in visited:
            return
        visited = visited | {or_point_id}
        for child_id in self.children_of(or_point_id):
            nested = self.or_points_below(child_id)
            if not nested:
                out.append(child_id)
            elif len(nested) == 1:
                self._collect_frontier(nested[0], out, visited)
            else:
                raise AxisError(
                    f"alternative {child_id!r} ({self.element(child_id).name!r}) of Or/Xor point "
                    f"{or_point_id!r} contains {len(nested)} independent Or/Xor frontiers "
                    f"({', '.join(nested)}); it joins several axes and cannot sit on one."
                )

    def contributions_from(self, source_id: str) -> list[ContributionLink]:
        return [link for link in self.contributions if link.src == source_id]

    def new_id(self) -> str:
        """Allocates and reserves the next free XMI id (mirrors `nextGlobalID`'s own role in the
        format: every element/link in a `.jucm` file needs a unique id, and jUCMNav itself keeps
        a running counter for exactly this reason)."""
        allocated = str(self.next_global_id)
        self.next_global_id += 1
        return allocated


def _int_sort_key(element_id: str) -> tuple[int, str]:
    """Sorts numeric-looking ids numerically (so id "9" sorts before "10"), falling back to
    lexicographic for anything else — used only in error messages, never in written output."""
    try:
        return (0, f"{int(element_id):020d}")
    except ValueError:
        return (1, element_id)
