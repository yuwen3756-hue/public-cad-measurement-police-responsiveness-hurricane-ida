# Current Status for Review

- **Release date:** 24 August 2026
- **Paper version:** R14.0
- **Scientific-results version:** R14
- **Package version:** 1

This is the professor-review release of *Public CAD Is Not Operational Ground Truth: Regime Change, Hurricane Ida, and the Measurement of Police Responsiveness*.

## Recommended reading order

1. `paper/Beland_Current_Status_2026-08-24_R14_0.pdf` - the 10-page main paper followed by the 30-page online supplement.
2. `REPRODUCTION_MANUAL.md` - what was done, the review-driven changes, the interpretation limits, and exact reproduction commands.
3. `source/` and `reproduction/repository_snapshot/` - LaTeX, aggregate diagnostics, empirical replay code, locked artifacts, and formal-verification source.

## What changed in R14.0

- The paper now leads with the public-file regime break: non-officer-initiated $J_{01}$ records are absent before 28 July 2021 and appear thereafter. The cause is not identified; no agency contact or internal-system audit was undertaken.
- The denominator is corrected from “all calls” to non-officer-initiated public CAD records. Officer-initiated records are analyzed separately as a candidate pathway, not a mechanism finding.
- The transparent maximum-cell discrepancy is the headline statistic. The optimization score is retained as a robustness calculation in the supplement.
- The main comparison is the prespecified 153-window stage-era set. The full 217-window and 86-window same-season sets are sensitivities, and the paper states that 66 full-set reference windows occur entirely before the public-file break.
- Ida does not satisfy the proposed 0.90 symmetric common-support screen. The paper reports all ten bin coverages and labels the result as a restricted-support diagnostic.
- R14 adds a fixed-seed 4,000-replicate conditional bootstrap, all secondary-statistic ranks, threshold sensitivity, full-count/post-change robustness, excluded-event comparisons, and the unfavorable timing-shift placebo.
- The within-disposition result is described as an accounting decomposition with repeated sign checks, not an independent theorem test. The DV material is compressed to a short illustration; no DV outcome is estimated.
- Unpublished project branding, an inaccessible talk citation, a self-citation, and an unverified working-paper citation were removed from the manuscript.

## Current scientific status

- The standardized maximum-cell discrepancy is 0.5072 and ranks 1/154 in the stage-era comparison, including Ida. The analogous unstandardized full-count statistic is 0.5320 and ranks first in the complete stage-era and post-change comparisons.
- The conditional bootstrap 95% interval for the maximum-cell discrepancy is [0.4597, 0.5656]. It represents record-sampling variation conditional on the observed public categories and fixed event/reference design; it does not address reference-window selection or the public-file regime change.
- Ida remains a descriptive, reference-extreme public-record reconfiguration. The package does not identify police performance, a causal effect, an institutional mechanism, physical response, effective capacity, true DV incidence, or a DV-specific effect.
- The 2025--2026 public audit remains descriptive: it identifies substantial missingness and endpoint disagreement but does not close the queue, capacity, lineage, or continuity gaps needed for a performance estimate.
- Numerical optimization results remain `TESTED_ONLY`. Lean verifies mathematical statements under their assumptions; source-field and institutional bindings remain human-review questions.

R13.0 and earlier release packages remain untouched predecessors. The public repository is `https://github.com/yuwen3756-hue/beland-plus-current-status-2026-08-24-r12-2`.
