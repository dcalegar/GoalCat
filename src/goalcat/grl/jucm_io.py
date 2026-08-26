"""Reading and writing `.jucm` (jUCMNav's URN/GRL XMI serialization) via pyecore.

Schema-driven, not hand-derived: the real metamodel — `grl.ecore`, `urncore.ecore`, `urn.ecore`
(plus their own dependencies `ucm.ecore`, `ucmscenarios.ecore`, `asd.ecore`) — is vendored under
`third_party/jucmnav/` (fetched from jUCMNavPlus, EPL-1.0; see that directory's README) and loaded
through `pyecore` (a Python EMF implementation), so parsing/serialization go through the same
metaclass machinery a real EMF tool would use, rather than a bespoke re-derivation of the schema
into ad hoc dataclasses and string-templated XML. The first version of this module did the latter;
it round-tripped the four real goal models correctly but had already shipped one bug (an
`xsi:type` prefix mismatch that silently dropped every decomposition/contribution link) purely
from hand-transcribing the schema — the class of error a real metamodel loader rejects by
construction, which is the entire reason for this rewrite.

**`grlspec` only, still.** `urndef/specDiagrams` (the `GRLGraph` visual layer) remains outside
what this module reads or schema-validates on write — verified against every `data/goals/*.jucm`
file, it carries no content beyond an (x, y) position and a `def`/`link` pointer back to the real
`grlspec` element. `read_jucm()` strips it (and the `links/@refs` attribute, its only forward
pointer from `grlspec`) before parsing; `write_jucm()` regenerates a fresh one via the same
lightweight template the hand-rolled version used — pyecore's own generic writer produces
non-canonical output for it (its diagram classes carry more structural constraints than a
from-scratch construction here is worth satisfying for content with no semantic weight).

**KPI content (`indicatorGroup`/`groups`/`strategies`/`evaluations`/`impactModel`/`featureModel`)
is still parsed informationally and round-tripped as raw XML**, not modeled through pyecore either
— Step 5a/6 never read it (excluded from the LLM prompt for the same reason the markdown-era code
excluded its own §6), and no perturbation in this project touches a KPI.
"""

from __future__ import annotations

import functools
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from goalcat.atomic_io import atomic_write_text
from goalcat.config import REPO_ROOT

from .model import (
    ActorDef,
    ContributionLink,
    DecompositionLink,
    GRLModel,
    IntentionalElement,
    KPIEvalPoint,
    KPIIndicator,
)

_JUCMNAV_EMF = (
    REPO_ROOT / "third_party" / "jucmnav" / "seg.jUCMNav" / "src" / "seg" / "jUCMNav" / "emf"
)

# Load order matters: each file's cross-package references must already be registered in
# rset.metamodel_registry before the file that uses them loads. ucm.ecore/ucmscenarios.ecore/
# asd.ecore are dependencies of urn.ecore (URN combines GRL with UCM/ASD) that this project never
# otherwise touches — loaded only to let urn.ecore itself resolve, never used beyond that.
_METAMODEL_LOAD_ORDER = (
    "urncore.ecore",
    "ucmscenarios.ecore",
    "ucm.ecore",
    "asd.ecore",
    "urn.ecore",
    "grl.ecore",
)


@functools.lru_cache(maxsize=1)
def _metamodels():
    """Loads the real GRL/URN metamodel once per process and caches it — the `.ecore` files never
    change at runtime, and reloading them per call would repeat non-trivial XMI parsing for no
    benefit. Returns (resource_set, grl_package, urn_package)."""
    from pyecore.resources import ResourceSet

    rset = ResourceSet()

    def load(filename: str):
        resource = rset.get_resource(str(_JUCMNAV_EMF / filename))
        package = resource.contents[0]
        rset.metamodel_registry[package.nsURI] = package
        for sub in package.eSubpackages:
            rset.metamodel_registry[sub.nsURI] = sub
        return package

    packages = {name: load(name) for name in _METAMODEL_LOAD_ORDER}
    return rset, packages["grl.ecore"], packages["urn.ecore"], packages["urncore.ecore"]


class _StringURI:
    """A pyecore URI backed by an in-memory string, for parsing/serializing `.jucm` text without
    a real file — `PipelineConfig.goal_model_path.read_text()` already hands this module text,
    and a perturbation builds a `GRLModel` entirely in memory before ever touching disk."""

    def __init__(self, content: bytes = b"", uri: str = "memory://model.jucm"):
        import io

        from pyecore.resources.resource import URI as PyEcoreURI

        self._impl = PyEcoreURI(uri)
        self._instream = io.BytesIO(content)
        self._outstream = io.BytesIO()

    def __getattr__(self, name):
        return getattr(self._impl, name)

    def create_instream(self):
        return self._instream

    def create_outstream(self):
        return self._outstream


# ------------------------------------------------------------------------------------------
# Reading
# ------------------------------------------------------------------------------------------

_URNDEF_RE = re.compile(r"<urndef>.*</urndef>\s*", re.S)
_REFS_ATTR_RE = re.compile(r'\s+refs="[^"]*"')


def parse_jucm(xml_text: str, source_path: str = "<memory>") -> GRLModel:
    """Parses `.jucm` XMI text into a `GRLModel`, through pyecore against the real metamodel.

    `urndef` and every `links/@refs` attribute are stripped before parsing — both are pure
    forward-pointers into the diagram layer this module never reads (see this module's
    docstring); stripping them avoids pulling the diagram classes' own EMF plumbing into a parse
    that only wants `grlspec`. Raises `ValueError` (wrapping pyecore's own error) on anything that
    fails to validate against the real schema — this project's goal models are frozen artifacts
    that must parse completely and correctly, or not at all.
    """
    from pyecore.resources.xmi import XMIResource

    rset, _grl_pkg, _urn_pkg, _urncore_pkg = _metamodels()

    stripped = _URNDEF_RE.sub("", xml_text)
    stripped = _REFS_ATTR_RE.sub("", stripped)

    resource = XMIResource(_StringURI(stripped.encode("utf-8")))
    resource.resource_set = rset
    try:
        resource.load()
    except Exception as exc:  # pyecore raises plain Exception/ValueError/KeyError variants
        raise ValueError(f"{source_path}: failed to parse as GRL/URN XMI against grl.ecore: {exc}") from exc

    if not resource.contents:
        raise ValueError(f"{source_path}: document produced no root element")
    urnspec = resource.contents[0]
    if urnspec.eClass.name != "URNspec":
        raise ValueError(f"{source_path}: root element is {urnspec.eClass.name!r}, expected 'URNspec'")
    grlspec = urnspec.grlspec
    if grlspec is None:
        raise ValueError(f"{source_path}: document has no <grlspec> element")

    model = GRLModel(
        source_path=source_path,
        name=urnspec.name or "",
        author=getattr(urnspec, "author", None) or None,
        urn_version=getattr(urnspec, "urnVersion", None) or None,
        spec_version=getattr(urnspec, "specVersion", None) or None,
        next_global_id=int(urnspec.nextGlobalID or "1"),
    )

    for el in grlspec.intElements:
        model.elements[el.id] = IntentionalElement(
            id=el.id,
            name=el.name or "",
            type=el.type.name,
            # el.decompositionType (a plain getattr) always returns the EEnum's class-level
            # default ("And") even for a leaf that never had the attribute in the source XML —
            # EMF attribute access can't distinguish "explicitly set to the default" from "never
            # set" without eIsSet(), so that's what gates this rather than a truthiness check.
            decomposition_type=el.decompositionType.name if el.eIsSet("decompositionType") else None,
            metadata={entry.name: entry.value for entry in el.metadata if entry.name is not None},
        )

    for actor in grlspec.actors:
        model.actors[actor.id] = ActorDef(id=actor.id, name=actor.name or "")

    for link in grlspec.links:
        kind = link.eClass.name
        if kind == "Decomposition":
            # GRL orients a decomposition part -> whole; GRLModel orients it parent -> child. See
            # DecompositionLink's own docstring for why the wire format is the way it is.
            model.decompositions.append(DecompositionLink(id=link.id, src=link.dest.id, dest=link.src.id))
        elif kind == "Contribution":
            model.contributions.append(
                ContributionLink(
                    id=link.id,
                    src=link.src.id,
                    dest=link.dest.id,
                    contribution=link.contribution.name,
                    quantitative=link.quantitativeContribution,
                )
            )
        # Other ElementLink subtypes (Dependency, ...) are unused by this project's goal models.

    _parse_kpis_raw(xml_text, model)
    return model


def _parse_kpis_raw(xml_text: str, model: GRLModel) -> None:
    """Builds the read-only `GRLModel.indicators` view and captures the KPI subtree's raw XML for
    verbatim round-tripping, via plain `ElementTree` against the *original* text (not the
    pyecore-parsed object graph) — see this module's docstring for why KPI content stays outside
    the schema-validated path. Best-effort: an unrecognized/absent KPI structure leaves
    `indicators` empty rather than raising, since KPIs are documentary and never gate Step 5a/6 or
    a perturbation."""
    root = ET.fromstring(xml_text)
    grlspec = root.find("grlspec")
    if grlspec is None:
        return

    group_name_by_id: dict[str, str] = {}
    indicator_group_by_indicator_id: dict[str, str] = {}
    for group_el in grlspec.findall("indicatorGroup"):
        group_id = group_el.get("id")
        if group_id is None:
            continue
        group_name_by_id[group_id] = group_el.get("name", "")
        for indicator_id in (group_el.get("indicators") or "").split():
            indicator_group_by_indicator_id[indicator_id] = group_id

    eval_point_by_indicator_id: dict[str, KPIEvalPoint] = {}
    for evaluation_el in grlspec.iter("evaluations"):
        indicator_id = evaluation_el.get("intElement")
        if indicator_id is None:
            continue
        eval_set = evaluation_el.find("kpiEvalValueSet")
        if eval_set is None:
            continue

        def _float_or_none(value: str | None) -> float | None:
            return float(value) if value is not None else None

        eval_point_by_indicator_id[indicator_id] = KPIEvalPoint(
            target=_float_or_none(eval_set.get("targetValue")),
            threshold=_float_or_none(eval_set.get("thresholdValue")),
            worst=_float_or_none(eval_set.get("worstValue")),
            unit=eval_set.get("unit"),
            qualitative_evaluation_value=eval_set.get("qualitativeEvaluationValue"),
        )

    for element in model.elements.values():
        if element.type != "Indicator":
            continue
        group_id = indicator_group_by_indicator_id.get(element.id)
        model.indicators[element.id] = KPIIndicator(
            id=element.id,
            name=element.name,
            group_id=group_id,
            group_name=group_name_by_id.get(group_id) if group_id else None,
            eval_point=eval_point_by_indicator_id.get(element.id),
        )

    kpi_fragments = [
        ET.tostring(el, encoding="unicode")
        for el in list(grlspec.findall("indicatorGroup"))
        + list(grlspec.findall("groups"))
        + list(grlspec.findall("strategies"))
        + list(grlspec.findall("impactModel"))
        + list(grlspec.findall("featureModel"))
    ]
    model.kpi_raw_xml = "\n    ".join(kpi_fragments) if kpi_fragments else None


def read_jucm(path: str | Path) -> GRLModel:
    # Resolved (not just read) so source_path is always absolute regardless of what the caller
    # passed — perturb.py's provenance records call .relative_to(REPO_ROOT) on it.
    path = Path(path).resolve()
    return parse_jucm(path.read_text(encoding="utf-8"), source_path=str(path))


# ------------------------------------------------------------------------------------------
# Writing
# ------------------------------------------------------------------------------------------

_LINKS_OPPOSITE_ATTR_RE = re.compile(r'\s+links(?:Src|Dest)="[^"]*"')


def _build_grlspec_eobject(model: GRLModel):
    """Constructs a real, schema-validated pyecore object graph for `grlspec`'s content from a
    `GRLModel` — the same metaclasses `parse_jucm()` reads back, so a value pyecore's own
    constructors reject (e.g. an invalid `ContributionType` literal) fails here, at construction,
    rather than silently serializing something jUCMNav would refuse to open."""
    _rset, grl_pkg, urn_pkg, urncore_pkg = _metamodels()
    URNspec = urn_pkg.getEClassifier("URNspec")
    GRLspec = grl_pkg.getEClassifier("GRLspec")
    IntentionalElementCls = grl_pkg.getEClassifier("IntentionalElement")
    # Indicator lives in grl.ecore's nested "kpimodel" eSubpackage, not in grl_pkg's own
    # eClassifiers — getEClassifier() doesn't search subpackages, so it's looked up explicitly.
    kpimodel_pkg = next(sub for sub in grl_pkg.eSubpackages if sub.name == "kpimodel")
    IndicatorCls = kpimodel_pkg.getEClassifier("Indicator")
    ActorCls = grl_pkg.getEClassifier("Actor")
    MetadataCls = urncore_pkg.getEClassifier("Metadata")
    DecompositionCls = grl_pkg.getEClassifier("Decomposition")
    ContributionCls = grl_pkg.getEClassifier("Contribution")
    IntentionalElementType = grl_pkg.getEClassifier("IntentionalElementType")
    DecompositionType = grl_pkg.getEClassifier("DecompositionType")
    ContributionType = grl_pkg.getEClassifier("ContributionType")

    urnspec = URNspec()
    urnspec.name = model.name
    if model.author:
        urnspec.author = model.author
    urnspec.specVersion = model.spec_version or "1.0"
    urnspec.urnVersion = model.urn_version or "1.27"
    urnspec.nextGlobalID = str(model.next_global_id)

    grlspec = GRLspec()
    urnspec.grlspec = grlspec

    eobject_by_element_id = {}
    for element in model.elements.values():
        cls = IndicatorCls if element.type == "Indicator" else IntentionalElementCls
        eobject = cls()
        eobject.id = element.id
        eobject.name = element.name
        eobject.type = getattr(IntentionalElementType, element.type)
        if element.decomposition_type:
            eobject.decompositionType = getattr(DecompositionType, element.decomposition_type)
        for name, value in element.metadata.items():
            entry = MetadataCls()
            entry.name = name
            entry.value = value
            eobject.metadata.append(entry)
        grlspec.intElements.append(eobject)
        eobject_by_element_id[element.id] = eobject

    for actor in model.actors.values():
        eactor = ActorCls()
        eactor.id = actor.id
        eactor.name = actor.name
        grlspec.actors.append(eactor)

    for link in model.decompositions:
        elink = DecompositionCls()
        elink.id = link.id
        # Back to GRL's part -> whole orientation (see parse_jucm's mirror-image comment).
        elink.src = eobject_by_element_id[link.dest]
        elink.dest = eobject_by_element_id[link.src]
        grlspec.links.append(elink)

    for link in model.contributions:
        elink = ContributionCls()
        elink.id = link.id
        elink.src = eobject_by_element_id[link.src]
        elink.dest = eobject_by_element_id[link.dest]
        elink.contribution = getattr(ContributionType, link.contribution)
        if link.quantitative is not None:
            elink.quantitativeContribution = link.quantitative
        grlspec.links.append(elink)

    return urnspec


def _reinstate_decomposition_type(grlspec_xml: str, model: GRLModel) -> str:
    """Adds back `decompositionType="And"` on exactly the elements whose `GRLModel` value is
    `"And"` — pyecore's default writer drops it everywhere (elision applies uniformly to every
    element carrying the schema default, leaf or not), and forcing it back on with
    `SERIALIZE_DEFAULT_VALUES=True` overcorrects the other way (it then appears on genuine leaves
    too, which never had any decomposition at all in every real `data/goals/*.jucm` file). Neither
    of pyecore's two serialization modes matches real jUCMNav output here, so the attribute is
    reinstated by id from the model itself — the one source that actually knows which elements are
    real And-decompositions rather than bare leaves.
    """
    from xml.sax.saxutils import quoteattr as _q

    for element in model.elements.values():
        if element.decomposition_type != "And":
            continue
        tag_re = re.compile(rf'(<intElements\b[^>]*\bid={_q(element.id)}[^>]*?)(/>)')
        match = tag_re.search(grlspec_xml)
        if match and "decompositionType" not in match.group(1):
            grlspec_xml = grlspec_xml[: match.start()] + match.group(1) + ' decompositionType="And"' + "/>" + grlspec_xml[match.end() :]
    return grlspec_xml


def _render_grlspec_via_pyecore(model: GRLModel) -> str:
    """Serializes `grlspec`'s content through pyecore's own XMI writer against the real
    metamodel, then corrects the two conventions it doesn't share with real jUCMNav output:
    `decompositionType="And"` is reinstated only on genuine And-decompositions (see
    `_reinstate_decomposition_type`), and the `linksSrc`/`linksDest` back-references are dropped
    (EMF-computed opposites of `links/@src,@dest`; real jUCMNav output omits them as redundant,
    and `parse_jucm()` never reads them either way).
    """
    from pyecore.resources.xmi import XMIResource

    urnspec = _build_grlspec_eobject(model)
    resource = XMIResource(_StringURI())
    resource.append(urnspec)
    resource.save()
    xml_text = resource.uri._outstream.getvalue().decode("utf-8")

    grlspec_start = xml_text.index("<grlspec")
    grlspec_end = xml_text.index("</grlspec>") + len("</grlspec>")
    grlspec_xml = xml_text[grlspec_start:grlspec_end]
    grlspec_xml = _LINKS_OPPOSITE_ATTR_RE.sub("", grlspec_xml)
    grlspec_xml = _reinstate_decomposition_type(grlspec_xml, model)

    if model.kpi_raw_xml:
        grlspec_xml = grlspec_xml[: -len("</grlspec>")] + f"\n    {model.kpi_raw_xml}\n  </grlspec>"
    else:
        grlspec_xml = grlspec_xml[: -len("</grlspec>")] + "\n    <impactModel/>\n    <featureModel/>\n  </grlspec>"
    return "  " + grlspec_xml if not grlspec_xml.startswith("  ") else grlspec_xml


def _attr(name: str, value: str | int | None) -> str:
    from xml.sax.saxutils import quoteattr

    return "" if value is None else f" {name}={quoteattr(str(value))}"


def _layout_positions(model: GRLModel) -> dict[str, tuple[int, int]]:
    """A simple BFS-depth grid layout: column = order-of-appearance within its depth row, row =
    distance from the nearest root (an element with no incoming Decomposition link), softgoals
    pinned to their own row below everything else. Good enough to open and read in jUCMNav — not
    a claim of matching a hand-tuned original (see this module's docstring)."""
    parent_of: dict[str, str] = {link.dest: link.src for link in model.decompositions}
    depth: dict[str, int] = {}
    for element_id, element in model.elements.items():
        if element.type == "Softgoal":
            continue
        d, current, seen = 0, element_id, {element_id}
        while current in parent_of and parent_of[current] not in seen:
            current = parent_of[current]
            seen.add(current)
            d += 1
        depth[element_id] = d

    positions: dict[str, tuple[int, int]] = {}
    by_depth: dict[int, list[str]] = {}
    for element_id, d in sorted(depth.items(), key=lambda item: (item[1], item[0])):
        by_depth.setdefault(d, []).append(element_id)
    for d, ids in by_depth.items():
        for column, element_id in enumerate(ids):
            positions[element_id] = (200 + column * 220, 80 + d * 100)

    softgoal_ids = [e.id for e in model.elements.values() if e.type == "Softgoal"]
    softgoal_row = 80 + (max(by_depth) + 1) * 100 if by_depth else 80
    for column, element_id in enumerate(softgoal_ids):
        positions[element_id] = (200 + column * 220, softgoal_row)
    return positions


def _render_urndef(model: GRLModel) -> str:
    """Regenerates `urndef/specDiagrams` from scratch as a lightweight template (see this
    module's docstring for why this layer stays outside the pyecore-validated path). Node/link
    ids are freshly allocated via `model.new_id()`, which also advances `next_global_id` so the
    written file's own `nextGlobalID` stays a true upper bound.

    Single-actor simplification: with exactly one actor, every non-softgoal/non-indicator element
    is placed inside that actor's box (matching every existing `data/goals/*.jucm` file, where
    `grlspec` itself carries no element-to-actor ownership at all — only this diagram layer does);
    with zero or more than one actor, no element is placed inside any actor's box.
    """
    from xml.sax.saxutils import quoteattr as _q

    positions = _layout_positions(model)
    graph_id = model.new_id()

    single_actor = next(iter(model.actors.values())) if len(model.actors) == 1 else None
    node_id_by_element: dict[str, str] = {}
    node_lines: list[str] = []
    actor_child_ids: list[str] = []

    for element in model.elements.values():
        node_id = model.new_id()
        node_id_by_element[element.id] = node_id
        x, y = positions.get(element.id, (200, 80))
        cont_ref_attr = ""
        if single_actor is not None and element.type != "Softgoal":
            cont_ref_attr = "__ACTOR_REF__"
            actor_child_ids.append(node_id)
        node_lines.append(
            f'      <nodes xsi:type="grl:IntentionalElementRef" id={_q(node_id)} '
            f'name={_q(element.name)} x={_q(str(x))} y={_q(str(y))} '
            f'def={_q(element.id)}{cont_ref_attr}>\n        <label/>\n      </nodes>'
        )

    actor_ref_id = model.new_id() if single_actor is not None else None
    if single_actor is not None:
        node_lines = [line.replace("__ACTOR_REF__", f" contRef={_q(actor_ref_id)}") for line in node_lines]

    connection_lines: list[str] = []
    for link in list(model.decompositions) + list(model.contributions):
        conn_id = model.new_id()
        # A LinkRef's source/target mirror its link's own endpoints, so decompositions are drawn
        # part -> whole here too, matching what _build_grlspec_eobject() serializes.
        from_id, to_id = (
            (link.dest, link.src) if isinstance(link, DecompositionLink) else (link.src, link.dest)
        )
        source_node = node_id_by_element.get(from_id)
        target_node = node_id_by_element.get(to_id)
        if source_node is None or target_node is None:
            continue
        connection_lines.append(
            f'      <connections xsi:type="grl:LinkRef" id={_q(conn_id)} '
            f'source={_q(source_node)} target={_q(target_node)} link={_q(link.id)}/>'
        )

    lines = [
        "  <urndef>",
        f'    <specDiagrams xsi:type="grl:GRLGraph" name={_q(model.name)} id={_q(graph_id)}>',
    ]
    if single_actor is not None and actor_ref_id is not None:
        nodes_attr = f' nodes={_q(" ".join(actor_child_ids))}' if actor_child_ids else ""
        width = max((x for x, _ in positions.values()), default=400) + 400
        height = max((y for _, y in positions.values()), default=200) + 200
        lines.append(
            f'      <contRefs xsi:type="grl:ActorRef" id={_q(actor_ref_id)} '
            f'name={_q(single_actor.name)} x="180" y="40" width={_q(str(width))} '
            f'height={_q(str(height))} contDef={_q(single_actor.id)}'
            f'{nodes_attr}>\n        <label/>\n      </contRefs>'
        )
    lines.extend(node_lines)
    lines.extend(connection_lines)
    lines.append("    </specDiagrams>")
    lines.append("  </urndef>")
    return "\n".join(lines)


def render_jucm(model: GRLModel) -> str:
    """Serializes a `GRLModel` back to `.jucm` XMI text: `grlspec` through pyecore against the
    real metamodel, `urndef` as a lightweight regenerated template (see module docstring), joined
    in `pm4py_ucm`'s own documented child order (`ucmspec -> grlspec -> urndef`, minus the empty
    `ucmspec` this project's goal models never populate — see
    `pm4py_ucm.objects.ucm.exporter.variants.jucm`'s module docstring, which states that ordering
    as a jUCMNav-import requirement).
    """
    from xml.sax.saxutils import quoteattr

    # Order matters: _render_urndef() allocates fresh ids via model.new_id(), advancing
    # model.next_global_id — the grlspec render (which embeds nextGlobalID in the header) must
    # happen only after that allocation, or it would understate the bound.
    urndef_xml = _render_urndef(model)
    grlspec_xml = _render_grlspec_via_pyecore(model)

    header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urn:URNspec xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:grl="http:///grl.ecore" '
        'xmlns:grl.kpimodel="http:///grl/kpimodel.ecore" xmlns:urn="http:///urn.ecore" '
        f'name={quoteattr(model.name)}{_attr("author", model.author)} '
        f'specVersion={quoteattr(model.spec_version or "1.0")} '
        f'urnVersion={quoteattr(model.urn_version or "1.27")} '
        f'nextGlobalID={quoteattr(str(model.next_global_id))}>'
    )
    return "\n".join([header, grlspec_xml, urndef_xml, "</urn:URNspec>"]) + "\n"


def write_jucm(model: GRLModel, path: str | Path) -> Path:
    path = Path(path)
    atomic_write_text(path, render_jucm(model))
    return path
