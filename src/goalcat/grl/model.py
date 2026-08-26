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
