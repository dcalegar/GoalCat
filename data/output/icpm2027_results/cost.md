# Hosted-LLM spend — ICPM 2027 study (Task C15)

Single reproducible aggregation (`analysis/cost.py`). Sums `estimated_cost_usd` (single-call steps) **and** `total_estimated_cost_usd` (batched assignment) over the run set defined in that module. Indicative, not a benchmark.

| Dataset | Phase | Cost (USD) | Calls | Input tok | Output tok |
|---|---|--:|--:|--:|--:|
| bpic2019 | C12 stability | 0.11 | 5 | 352,530 | 3,491 |
| bpic2019 | E1 | 18.81 | 2882 | 26,927,285 | 4,294,482 |
| rtfm | C12 stability | 0.02 | 5 | 31,650 | 5,055 |
| rtfm | E1 | 0.38 | 54 | 294,538 | 118,431 |
| rtfm | E2 | 0.09 | 12 | 67,588 | 25,968 |
| rtfm_mini | case study | 0.01 | 6 | 9,168 | 2,389 |
| sepsis | C12 stability | 0.04 | 10 | 88,510 | 6,267 |
| sepsis | E1 | 2.53 | 288 | 2,336,275 | 731,888 |
| sepsis | E2 | 0.46 | 54 | 441,645 | 131,135 |
| **all** | **all** | **22.46** | **3316** | **30,549,189** | **5,319,106** |

## Headline

- **Whole study: ~3316 calls, ~USD 22.46** (30.5 M input + 5.3 M output tokens).
- **Experiment 1 (22 conditions): ~USD 21.73** (3224 calls) — bpic2019 USD 18.81, rtfm USD 0.38, sepsis USD 2.53.
- BPIC 2019 dominates because its assignment runs at `batch_size = 25` over 11,973 variants (~480 calls per condition).
