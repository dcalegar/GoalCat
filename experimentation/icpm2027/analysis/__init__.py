"""Cross-condition analysis: coverage/residual, contingency matrices, and partition divergence
(EXPERIMENTATION_PLAN.md §3's "Evidence reported per dataset" and §7's metrics reference).

Every function here takes plain `assignments_df`-shaped input (`variant_id`, `category_id`, with
`category_id` possibly missing/NaN for a residual) and a `variants_df` for case-weighting
(`variant_id`, `frequency`) — the same two-column shape `goalcat`'s own Step 6 writes, and the
same shape `baselines.structural_clustering.StructuralClusteringResult.as_assignments_df()`
produces. Nothing here is specific to which condition (guided, open, or the structural baseline)
produced its input, so §3's "guided-vs-structural-baseline contingency as a secondary comparison"
reuses exactly the same `contingency_matrix()` call as the primary guided-vs-open one.
"""
