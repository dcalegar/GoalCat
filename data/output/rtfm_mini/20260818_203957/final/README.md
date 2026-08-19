# Final output — accepted taxonomy (round 2)

This is the accepted, final deliverable of the GoalCat pipeline for `rtfm_mini` (run `20260818_203957`).

- `taxonomy.json` — the accepted category taxonomy.
- One `<category_id>.xes.gz` per category — the raw event log, partitioned per category:
- `payment.xes.gz`
- `administrative_appeal.xes.gz`
- `judicial_appeal.xes.gz`
- `coercive_collection.xes.gz`
- `residual.xes.gz` — cases that fit no category.

Process-model visualizations (Petri net + DFG renders) were not kept as part of this deliverable to save disk space — re-run Step 7 against `round2/06_assignment/assignments.csv` and this taxonomy to regenerate them if needed.

For per-category coverage/cohesion, see [`../round2/06_assignment/assignment_report.md`](../round2/06_assignment/assignment_report.md).
For conformance metrics, see [`../round2/07_discovery/discovery_report.md`](../round2/07_discovery/discovery_report.md).
For prose descriptions and goal alignment, see [`../round2/08_description/description_report.md`](../round2/08_description/description_report.md).

Full revision history: [`../review_index.md`](../review_index.md).
