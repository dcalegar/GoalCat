# Final output — accepted taxonomy (round 2)

This is the accepted, final deliverable of the GoalCat pipeline for `rtfm_mini` (run `20260825_215313`).

- `taxonomy.json` — the accepted category taxonomy.
- `assignments.csv` — the full per-variant assignment (`variant_id` -> `category_id`, plus distances and rationale) that produced `sublogs/`. A copy of `round2/06_assignment/assignments.csv`, kept here so this taxonomy can be re-filtered or re-partitioned by other tools without depending on the round directory still existing.
- `sublogs/` — one `<category_id>.xes.gz` per category, the raw event log partitioned per category:
- `sublogs/payment_resolution.xes.gz`
- `sublogs/administrative_appeal_to_prefecture.xes.gz`
- `sublogs/judicial_appeal_to_the_judge.xes.gz`
- `sublogs/coercive_credit_collection.xes.gz`
- `sublogs/residual.xes.gz` — cases that fit no category.

Process-model visualizations (Petri net + DFG renders) were not kept as part of this deliverable to save disk space — re-run Step 7 against `assignments.csv` and this taxonomy to regenerate them if needed.

For per-category coverage/cohesion, see [`../round2/06_assignment/assignment_report.md`](../round2/06_assignment/assignment_report.md).
For conformance metrics, see [`../round2/07_discovery/discovery_report.md`](../round2/07_discovery/discovery_report.md).
For prose descriptions and goal alignment, see [`../round2/08_description/description_report.md`](../round2/08_description/description_report.md).

Full revision history: [`../review_index.md`](../review_index.md).
