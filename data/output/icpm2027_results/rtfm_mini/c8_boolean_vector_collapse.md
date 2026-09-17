# Task C8 — boolean activity-vector collapse (`rtfm_mini`)

Source run: `data/output/rtfm_mini/20260917_192308`, round 1 — the five-way guided
categorization the paper's Table `tab:rtfm-mini` reports. An earlier version of this file named
the category `resolve_via_timely_or_delinquent_payment`, which existed only in the superseded run
`20260831_064805`'s round 2, whose merge of anchors 12 and 13 spans two Or points and is rejected
by `check_axis_partition`. The collapse argument is unaffected by the rename: the three variants
share one activity vector and one category either way.

Six of `rtfm_mini`'s eight cases are one inspectable trace each; two — `A10009` and `A10798`, **real Road-Traffic-Fine cases** (`data/logs/rtfm.xes.gz`), not synthetic — carry a payment rework loop (the fine is paid in two installments). They share their activity *set* with the single-payment case `A10000`.

## The collapse

A boolean activity-presence vector — the representation structural trace clustering uses (`baselines/structural_clustering.py`, after Amling et al.) — records only *which* activities occur, not how often or in what order. The three payment variants therefore map to **one identical vector** and are indistinguishable to any method built on it:

| variant | case | trace | activity set | boolean vector | structural cluster | guided category |
|---|---|---|---|---|---|---|
| V0003 | A10000 | `Create Fine>Send Fine>Insert Fine Notification>Add penalty>Payment` | {Add penalty, Create Fine, Insert Fine Notification, Payment, Send Fine} | *(identical)* | `None` | `delinquent_payment` |
| V0007 | A10009 | `Create Fine>Send Fine>Insert Fine Notification>Add penalty>Payment>Payment` | {Add penalty, Create Fine, Insert Fine Notification, Payment, Send Fine} | *(identical)* | `None` | `delinquent_payment` |
| V0008 | A10798 | `Create Fine>Send Fine>Insert Fine Notification>Payment>Add penalty>Payment` | {Add penalty, Create Fine, Insert Fine Notification, Payment, Send Fine} | *(identical)* | `None` | `delinquent_payment` |

All three fall in the **same structural cluster** (or the same noise bucket) — the representation cannot separate *paid once* from *paid in two installments* from *partial payment before the penalty, remainder after*.

## What the multi-view narrative keeps

The narrative preserves event count, order, and the inter-event gaps, and Step&nbsp;3 emits an explicit rework note:

- **V0003**: Create Fine Send Fine (+130d) Insert Fine Notification (+16d) Add penalty (+60d) Payment (+344d)
- **V0007**: Create Fine Send Fine (+119d) Insert Fine Notification (+6d) Add penalty (+60d) Payment (+10d) Payment (+30d) Rework observed: Payment was repeated (seen in 1 cases).
- **V0008**: Create Fine Send Fine (+130d) Insert Fine Notification (+9d) Payment (+45d) Add penalty (+15d) Payment (+10d) Rework observed: Payment was repeated (seen in 1 cases).

Guided Step&nbsp;6 assigns all three to `delinquent_payment` — correctly, since each pays only after notification and penalty — but its per-variant rationale reflects the distinction the boolean vector discards ("Payment after a penalty" vs. "Payment actions [plural] after penalties" vs. "resolved through payments [plural]").

This is architecture-executability evidence for §6, not evidence of goal-anchoring's empirical effect, and must not be cited as the latter.
