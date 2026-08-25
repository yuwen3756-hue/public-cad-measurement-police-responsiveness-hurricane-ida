# Current Status for Review

**Release date:** 24 August 2026  
**Paper version:** R12.2  
**Scientific-results version:** R12  
**Package version:** 1

This package is the professor-review release of *From Police Workload to Auditable Performance Measures: Hurricane Ida, Public CAD, and the Measurement Frontier for Reported DV-Related Calls*.

## Recommended reading order

1. `paper/Beland_Current_Status_2026-08-24_R12_2.pdf` - main paper followed by the mathematical and reproducibility appendix.
2. `REPRODUCTION_MANUAL.md` - what was done, what can be reproduced from this package, and the exact commands.
3. `source/` and `reproduction/repository_snapshot/` - LaTeX, empirical replay code, locked aggregate artifacts, and formal-verification source.

## Current scientific status

- The empirical estimates remain system-level. The paper does not estimate a DV performance effect or a DV call-volume trend.
- Ida's public dispatch-arrival field path ranks first among 217 qualified reference windows, with the same rank in the two narrower prespecified comparison sets.
- The within-disposition decomposition shows that the public-record change is not explained only by a change in the disposition mix.
- The released record cannot by itself distinguish operational service paths from recording, retention, and export paths. Candidate DV measures are therefore classified as directly supportable, bounded, selected, or unavailable according to their required evidence.
- Current public data add descriptive and semantic detail, but they do not supply queue stock, effective capacity, complete priority histories, realized continuity states, or a stable internal-to-public lineage bridge.
- Numerical LP results remain `TESTED_ONLY`. Lean verifies stated mathematical theorems under their assumptions; institutional and source-field bindings still require human review.

## What changed for this release

The R12.2 scientific text and R12 numerical results were retained. The title pages were cleaned so that the metadata block contains only the release date and version identifiers. A reproducibility manual, package-native verification scripts, exact paper sources, the aggregate-only M7B replay, the M7D-E and M8P replay code, and the Lean source package were added.

No empirical result was recomputed or promoted merely to make this review package.
