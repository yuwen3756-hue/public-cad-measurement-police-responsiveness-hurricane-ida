# Research status note — R15.1 — 25 August 2026

The paper measures whether released public dispatch and arrival fields are present and valid, and how their four joint states change across windows. New Orleans public CAD changes before Hurricane Ida and changes again during Ida. The supported object is a public-field configuration, not physical dispatch, arrival, capacity, response quality, domestic-violence incidence, or a mechanism.

What is now established:

- The official July 2021 CSV confirms the first non-officer $J_{01}$ records on 28 July and a simultaneous officer-stream dispatch-field collapse; nonblank timestamps remain parseable.
- Ida's standardized maximum-cell contrast is 0.5072, rank $1/154$ including Ida. The post-hoc post-change full-count contrast is 0.5320, rank $1/152$ including Ida. A conditional window-wise bootstrap that does not model temporal dependence places Ida first in all 4,000 draws; alternating non-overlapping phases give ranks $1/77$ and $1/76$.
- The standardized comparison covers 86.1 percent of event and 77.0 percent of baseline records and fails the 0.90 reference eligibility rule.
- The comparable non-officer dispatch-field series is 65.4 percent (2024), 66.0 percent (2025), and 66.8 percent (2026 snapshot). The 2025 all-row rate is 41.8 percent because officer-initiated records follow a different public-field convention.
- Public institutional documents define labels and exclude two technology explanations, but do not identify the July mechanism.

Remaining evidence need: a versioned 2021 changelog or privacy-safe internal/public reconciliation binding operational events, entry history, retention, and exported fields.
