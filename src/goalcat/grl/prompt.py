"""Rendering a `GRLModel` into the text Step 5a sends an LLM, and validating `anchor_ids`
against it — the GRL-native replacement for what `goalcat.llm.taxonomy` used to do by slicing a
markdown document's §1-§7.

`render_excerpt()` produces the *only* goal-model content a prompt ever states for a guided run
(Step 5a's induction and revision prompts; Step 6's assignment prompt carries the induced categories
alone, and Step 8's description prompt carries only `resolve_anchor_labels()` output): no
KPI section (Step 5a never needs it, matching the markdown-era `_extract_sections()`'s own §6
exclusion), no diagram layout, no provenance prose — just actors, the decomposition tree, and
contribution links, each element shown with its native `.jucm` id so a proposed category's
`anchor_ids` can reference something real. `declared_ids()`/`resolve_anchor_labels()`/
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
3. Everything omitted is irrelevant to Step 5a's task: the `urndef` diagram layer is presentation,
   KPI
   Indicators are not an axis to subdivide, and `author`/`created`/`nextGlobalID` are file
   metadata. Dropping them also keeps the prompt's token budget on the narrative sample, which is
   what actually calibrates category granularity.
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


def declared_ids(model: GRLModel) -> set[str]:
    """Every id Step 5a's `anchor_ids` may legally reference — every intentional element
    (Goal/Task/Softgoal/Ressource), Indicators included since a category could in principle
    anchor to one, though none of this project's prompts currently invite that."""
    return set(model.elements)


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
    and Indicators are excluded even though they likewise have no parent: softgoals are rendered
    separately as contribution targets, and Indicators are KPI metadata Step 5a never needs
    (matching the markdown-era `_extract_sections()`'s own §6 exclusion — this module's docstring
    makes the same claim, so this function has to honor it)."""
    children = {link.dest for link in model.decompositions}
    return [
        element.id
        for element in model.elements.values()
        if element.id not in children and element.type not in ("Softgoal", "Indicator")
    ]


def render_excerpt(model: GRLModel) -> str:
    """The full text block Step 5a's `{goal_model_excerpt}` receives, in both the induction and
    the revision prompt.
    Deterministic (dict/list iteration order matches the `.jucm` file's own element order), so the
    same frozen goal model always renders identical prompt text — required by the freeze table's
    "Prompts: versioned" row (EXPERIMENTATION_PLAN.md §2.2) and by
    `icpm2027.goalmodel.perturb`, which hashes this text as a perturbation's provenance record.
    Changing this function's output format therefore invalidates those hashes: treat it as a
    versioned artifact, not as free-form prompt wording."""
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

    softgoals = [e for e in model.elements.values() if e.type == "Softgoal"]
    contributions = [link for link in model.contributions]
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
    if bad:
        return [f"{category_id}: anchor_ids not in goal model: {bad}"]
    return []
