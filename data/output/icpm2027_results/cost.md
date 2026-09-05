# Hosted-LLM spend — ICPM 2027 study (Task C15)

Single reproducible aggregation (`analysis/cost.py`). Sums `estimated_cost_usd` (single-call steps) **and** `total_estimated_cost_usd` (batched assignment) over the run set defined in that module. Indicative, not a benchmark.

| Dataset | Phase | Cost (USD) | Calls | Input tok | Output tok |
|---|---|--:|--:|--:|--:|
| bpic2019 | C12 stability | 0.11 | 5 | 352,530 | 3,491 |
| bpic2019 | E1 | 37.03 | 5760 | 53,577,418 | 8,382,537 |
| rtfm | C12 stability | 0.02 | 5 | 31,650 | 5,055 |
| rtfm | E1 | 0.71 | 172 | 561,170 | 216,414 |
| rtfm | E2 | 0.69 | 165 | 568,980 | 206,091 |
| rtfm_mini | case study | 0.01 | 6 | 9,168 | 2,389 |
| sepsis | C12 stability | 0.04 | 10 | 88,510 | 6,267 |
| sepsis | E1 | 3.83 | 801 | 3,624,012 | 1,095,810 |
| sepsis | E2 | 4.08 | 875 | 3,985,705 | 1,151,996 |
| **all** | **all** | **46.51** | **7799** | **62,799,143** | **11,070,050** |

## Headline

- **Whole study: ~7799 calls, ~USD 46.51** (62.8 M input + 11.1 M output tokens).
- **Experiment 1 (51 conditions): ~USD 41.57** (6733 calls) — bpic2019 USD 37.03, rtfm USD 0.71, sepsis USD 3.83.
- BPIC 2019 dominates because its assignment runs at `batch_size = 25` over 11,973 variants (~480 calls per condition).
