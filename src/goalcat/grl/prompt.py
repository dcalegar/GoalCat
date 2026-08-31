"""Rendering a `GRLModel` into the text Step 5a sends an LLM, and validating `anchor_ids`
against it — the GRL-native replacement for what `goalcat.llm.taxonomy` used to do by slicing a
markdown document's §1-§7.

`render_excerpt()` produces the *only* goal-model content a prompt ever states for a guided run
(Step 5a's induction and revision prompts; Step 6's assignment prompt carries the induced categories
alone, and Step 8's description prompt carries only `resolve_anchor_labels()` output): actors, the
decomposition tree, the indicator value sets, and contribution links, each element shown with its
native `.jucm` id so a proposed category's `anchor_ids` can reference something real. No diagram
layout and no provenance prose — those are presentation and file metadata, not declared intent.

**Everything the model declares is rendered, with one deliberate carve-out.** The indicator section
states each indicator's name, unit, target/threshold/worst and provenance, but *never* its
`goalcat:from`/`goalcat:to` measurement binding. Those values are activity labels, and every goal
model's §7 forbids the activity-label table from reaching Steps 5a/6, because categorization there
must be semantic rather than a lexical pre-match (`goalcat.grl.measures`' module docstring states
the same boundary from the measuring side). Rendering the binding would leak exactly that table into
the categorization prompt. The conversion arithmetic is declared intent and belongs here; the
label binding is a measurement mechanism and stays in Step 7b. `declared_ids()`/`resolve_anchor_labels()`/
`grounding_problems()` replace `_extract_declared_ids()`/`_resolve_anchor_labels()`/
`check_taxonomy_grounding()`'s markdown-table lookups with the equivalent lookups against
`GRLModel.elements` directly — no parsing involved, since the model is already structured.

Why a projection instead of the `.jucm` file itself (README, "What the LLM actually sees of the
goal model", carries this same rationale for readers who never open this module):

1. The prompts' decision rules depend on structure the XMI does not present directly.
   `prompt_taxonomy_intent_guided.txt` tells the model to "check the AND/OR/XOR operators shown in
   the decomposition — never combine alternatives the goal model marks XOR". In XMI that means
   joining `intElements[@decompositionType]` against a flat `<links xsi:type="grl:Decomposition">`
   edge list and reconstructing parenthood transitively; `_render_tree()` does that join
   deterministically here rather than leaving the intent-guided condition's central constraint to
   an LLM's graph traversal.
2. Identifier grounding stays mechanically checkable. Each element is printed with its native id,
   so `Category.anchor_ids` can name one and `grounding_problems()` can validate it against
   `declared_ids()`. The mnemonic codes a reader sees in the goal models' prose descriptions
   (`G0`, `TP`, ...) are prose-only (see `model.py`'s `IntentionalElement.id` note), so rendering
   that prose instead would invite anchors that resolve to nothing.
3. Everything omitted is irrelevant to Step 5a's task: the `urndef` diagram layer is presentation
   and `author`/`created`/`nextGlobalID` are file metadata. Indicators used to be omitted on the
   grounds that they are "not an axis to subdivide" — true, but that conflated *anchoring to*
   something with *reasoning from* it. They now render as context, with the prompts stating that an
   indicator is never a valid `anchor_ids` target.
4. Determinism — see `render_excerpt()`'s own docstring.

Two model properties are deliberately *not* carried into the excerpt. Neither affects the goal
models in `data/goals/`, but both would need revisiting before that changes:

- Element-to-actor membership: actors are listed, but no element is attributed to one. Every
  current goal model declares exactly one actor and carries no element-level `actor` attribute in
  `grlspec` at all (ownership lives only in the diagram layer — see `jucm_io.py`'s single-actor
  note), so nothing is lost today; a multi-actor model would need this rendered.
- Softgoals with no incoming Contribution link: the softgoal block is emitted only when both
  softgoals and contributions exist, and it iterates the links, so an unconnected softgoal never
  appears.
"""

from __future__ import annotations

from .model import GRLModel, IntentionalElement

# Re-exported so a caller only needs `from goalcat.grl import declared_alternatives` and never
# has to know this is a GRLModel method versus a module-level function.
def declared_alternatives(model: GRLModel) -> dict[str, list[str]]:
    return model.declared_alternatives()


def axis_frontier(model: GRLModel, axis_root: str | None = None) -> list[str]:
    """The ids `Category.anchor_ids` may legally name for this axis — see
    `GRLModel.axis_frontier()`. Re-exported here beside `declared_ids()` because the two are the
    anchoring rule and the resolution rule respectively, and callers reach for them together."""
    return model.axis_frontier(axis_root)


def declared_ids(model: GRLModel) -> set[str]:
    """Every id Step 5a's `anchor_ids` may legally reference — every intentional element
    (Goal/Task/Softgoal/Ressource), Indicators excluded. Indicators became visible to Step 5a when
    `render_excerpt()` started rendering them, and both intent-guided prompts state the rule this
    enforces: an indicator measures whether a goal is achieved, so a category anchors to that goal,
    never to the measurement. Softgoals stay legal here — no prompt invites anchoring to one and
    none ever has, but a category naming the softgoal it realizes is a defensible reading of the
    axis in a way that one naming a KPI is not."""
    return {element_id for element_id, element in model.elements.items() if element.type != "Indicator"}


def _decomposition_operator(model: GRLModel, element: IntentionalElement) -> str:
    if element.decomposition_type:
        return element.decomposition_type.upper()
    return "leaf" if not model.children_of(element.id) else "AND"  # grl.ecore default is And


def _render_tree(model: GRLModel, element_id: str, depth: int, lines: list[str], visited: set[str]) -> None:
    if element_id in visited:
        lines.append("  " * depth + f"- [cycle back to id={element_id}]")
        return
    visited = visited | {element_id}
    element = model.element(element_id)
    children = model.children_of(element_id)
    operator = _decomposition_operator(model, element) if children else "leaf"
    lines.append("  " * depth + f"- id={element.id} [{element.type}] {element.name} ({operator})")
    for child_id in children:
        _render_tree(model, child_id, depth + 1, lines, visited)


def _roots(model: GRLModel) -> list[str]:
    """Elements with no incoming Decomposition link — where the tree rendering starts. Softgoals
    and Indicators are excluded from the *tree* even though they likewise have no parent, because
    neither is a decomposition root: softgoals render separately as contribution targets, and
    indicators render in their own section as contribution sources. Excluded from this rendering,
    not from the excerpt."""
    children = {link.dest for link in model.decompositions}
    return [
        element.id
        for element in model.elements.values()
        if element.id not in children and element.type not in ("Softgoal", "Indicator")
    ]


def render_excerpt(model: GRLModel, axis_root: str | None = None) -> str:
    """The full text block Step 5a's `{goal_model_excerpt}` receives, in both the induction and
    the revision prompt.
    Deterministic (dict/list iteration order matches the `.jucm` file's own element order), so the
    same frozen goal model always renders identical prompt text — required by the freeze table's
    "Prompts: versioned" row (`experimentation/icpm2027/configs/protocol.yaml`) and by
    `icpm2027.goalmodel.perturb`, which hashes this text as a perturbation's provenance record.
    Changing this function's output format therefore invalidates those hashes: treat it as a
    versioned artifact, not as free-form prompt wording.

    `axis_root` names the Or/Xor point whose alternatives are the categorization axis. When given,
    a closing block states that frontier explicitly, so an anchor above it (`taxonomy.py`'s
    `check_axis_partition`, which rejects exactly that) is a rule the prompt states rather than one
    the model has to infer from the indented operators. Omitting it reproduces the pre-axis output
    byte for byte, which is what keeps a run whose manifest predates this parameter comparable."""
    lines = [f"Goal model: {model.name}", ""]

    if model.actors:
        lines.append("Actors:")
        for actor in model.actors.values():
            lines.append(f"  - id={actor.id}: {actor.name}")
        lines.append("")

    lines.append("Goal-task decomposition (id, type, name, decomposition operator; indentation = parent/child):")
    for root_id in _roots(model):
        _render_tree(model, root_id, 0, lines, visited=set())
    lines.append("")

    if model.indicators:
        lines.append(
            "Indicators (how the organization measures whether a goal is met; id, name, unit, and the "
            "value set converting a measurement to satisfaction):"
        )
        for indicator in model.indicators.values():
            point = indicator.eval_point
            detail = ""
            if point is not None:
                bounds = ", ".join(
                    f"{label} {value:g}"
                    for label, value in (("target", point.target), ("threshold", point.threshold), ("worst", point.worst))
                    if value is not None
                )
                unit = f" {point.unit}" if point.unit else ""
                detail = f" ({bounds}{unit})" if bounds else ""
            provenance = model.elements[indicator.id].metadata.get("goalcat:provenance") if indicator.id in model.elements else None
            provenance_note = f" [provenance: {provenance}]" if provenance else ""
            lines.append(f"  - id={indicator.id} [Indicator] {indicator.name}{detail}{provenance_note}")
        lines.append("")

    softgoals = [e for e in model.elements.values() if e.type == "Softgoal"]
    contributions = list(model.contributions)
    if softgoals and contributions:
        lines.append("Softgoals and contribution links (source -> effect on softgoal):")
        softgoal_names = {s.id: s.name for s in softgoals}
        for link in contributions:
            source = model.element(link.src)
            target_name = softgoal_names.get(link.dest, model.element(link.dest).name)
            quantitative = f" ({link.quantitative:+d})" if link.quantitative is not None else ""
            lines.append(
                f"  - id={source.id} {source.name} --[{link.contribution}{quantitative}]--> {target_name}"
            )
        lines.append("")

    if axis_root is not None:
        frontier = model.axis_frontier(axis_root)
        root = model.element(axis_root)
        lines.append(
            f"Categorization axis: the alternatives of id={root.id} ({root.name}), decomposed "
            f"{(root.decomposition_type or 'And').upper()}."
        )
        for element_id in frontier:
            element = model.element(element_id)
            lines.append(f"  - id={element.id} [{element.type}] {element.name}")
        lines.append(
            "These ids, and only these, are valid anchor_ids. Do not anchor to a parent or "
            "ancestor of one of them: a coarser element is a different, broader goal, not the "
            "alternative it contains. Do not anchor to an alternative of any other decomposition "
            "point in the tree above — those belong to a different axis and a case may realize one "
            "of them in addition to, not instead of, one of these."
        )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def resolve_anchor_labels(model: GRLModel, anchor_ids: list[str]) -> str:
    """Resolves `anchor_ids` to real `id (type): name` labels, deterministic lookup against the
    frozen model — the GRL-native replacement for `taxonomy._resolve_anchor_labels()`. Empty
    `anchor_ids` (Step 5b/open induction, or Task C5's label-list control) still renders the fixed
    placeholder, matching the markdown-era behaviour exactly."""
    if not anchor_ids:
        return "(open induction — no goal model)"
    resolved = []
    for anchor_id in anchor_ids:
        if anchor_id in model.elements:
            element = model.elements[anchor_id]
            resolved.append(f"{element.id} ({element.type}): {element.name}")
        else:
            resolved.append(f"{anchor_id} (not found in goal model)")
    return "; ".join(resolved)


def grounding_problems(model: GRLModel, anchor_ids: list[str], category_id: str) -> list[str]:
    """Same check `taxonomy.check_taxonomy_grounding()` runs per category, factored out so it can
    be unit-tested against a `GRLModel` directly. Warn-only by design — Step 9's human review
    remains the actual correctness gate, matching every other grounding check in this project."""
    valid = declared_ids(model)
    bad = sorted(set(anchor_ids) - valid)
    if not bad:
        return []
    # An indicator id is in the model but not anchorable, which is a different reviewer-facing
    # problem from an id that resolves to nothing at all -- reporting both as "not in goal model"
    # would send a reviewer looking for a typo that isn't there.
    indicators = [anchor_id for anchor_id in bad if anchor_id in model.indicators]
    unknown = [anchor_id for anchor_id in bad if anchor_id not in model.indicators]
    problems = []
    if unknown:
        problems.append(f"{category_id}: anchor_ids not in goal model: {unknown}")
    if indicators:
        problems.append(
            f"{category_id}: anchor_ids name Indicators, which measure a goal rather than declare "
            f"one and are not anchorable: {indicators}"
        )
    return problems
