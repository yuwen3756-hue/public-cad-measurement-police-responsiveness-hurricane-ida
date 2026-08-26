# Current status for reviewer reading

- Project: **Public CAD Is Not Operational Ground Truth: A Hurricane Ida Stress Test of Public Dispatch Data**
- Release date: 26 August 2026
- Paper version: R16.1
- Scientific-results version: R15.1
- Package version: 1
- Predecessor: R16.0 commit `3b8fbac`, preserved unchanged

## Recommended reading order

1. `paper/Public_CAD_2026-08-26_R16_1.pdf` — main paper followed by the empirical supplement.
2. `paper/Public_CAD_Research_Status_Note_2026-08-26_R16_1.pdf` — one-page result and evidence-gap summary.
3. `REPRODUCTION_MANUAL.md` — exact build, verification, and interpretation boundaries.
4. `RESPONSE_TO_ASSESSMENTS.md` — implementation crosswalk for the readability review.
5. `review/` — supplied review materials, preserved as evidence rather than instructions.
6. `paper/Public_CAD_Legacy_Technical_Archive_2026-08-26_R16_1.pdf` — separate extended mathematics and formal verification, only if needed.

## The R16.1 reading sequence

1. The public-data convention changes abruptly on 28 July 2021.
2. Ida produces a second, temporary change inside the new convention.
3. Ida's largest change is 53.2 percentage points, larger than all 151 post-change ordinary-week comparisons.
4. The public record does not identify physical response or the institutional mechanism.

## What changed from R16.0

- Corrects the daily narrative to report the 29 August arrival-field dip and the separate 10 September excursion visible in Figure 2.
- Defines the **public missing-dispatch share** and uses it consistently in the abstract, text, status note, and figure legends.
- Removes a duplicated standardized-estimator paragraph and corrects the claim that three field configurations are independent.
- Adds author, affiliation, discussion-draft status, and a public data-and-code availability statement.
- Adds the alternating non-overlap result, the Cristobal comparison, and the concrete OPCD records-request next step without changing any estimate.
- Preserves all R15.1 numerical objects, raw/aggregate parity, source lineage, and scientific boundaries.
