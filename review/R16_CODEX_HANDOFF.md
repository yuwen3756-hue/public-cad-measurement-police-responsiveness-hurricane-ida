# Codex task: rebuild the R15.1 package around the readability rewrite

## Objective

Treat `main_paper_readability_rewrite.tex` as the authoritative replacement for the current main manuscript. Preserve the validated empirical results from R15.1, but rebuild the professor-facing package so that every supporting document follows the new narrative:

**July 28 public-file regime change → Ida-era spike → comparison with later-regime ordinary weeks → interpretation boundary → measurement implications.**

Do not add new scientific claims. Do not change any locked or predecessor reproduction artifact.

## Inputs

- Authoritative replacement manuscript: `main_paper_readability_rewrite.tex`
- Current repository: `yuwen3756-hue/public-cad-measurement-police-responsiveness-hurricane-ida`
- Current published commit: `872127a4912cfb2a1aa606e4ee9831e3f3496a18`
- Existing empirical data objects:
  - `source/r15_monthly_field_completeness.csv`
  - `source/r15_1_ida_time_path.csv`
  - `source/r15_raw_july_25_31_audit.csv`
  - `source/r15_current_denominator_audit.csv`
  - `source/r15_raw_window_scores.csv`
  - `source/r15_bootstrap_window_maxima.csv`
  - `source/r15_secondary_statistic_ranks.csv`
  - `source/r15_aggregate_diagnostics.json`
  - `source/r15_1_refinement_diagnostics.json`

## Versioning

Use a new paper version because this is a full narrative rewrite, but do not promote the scientific result version unless a numerical result changes.

Recommended:
- Paper version: `R16.0`
- Scientific-results version: `R15.1`

Keep version identifiers out of the manuscript body. They may appear in `VERSION.txt`, filenames, README, and release notes.

## Main-paper requirements

1. Replace the existing main source with the supplied readability rewrite.
2. Preserve the current title unless a neutral filename change is required.
3. Keep only two principal figures:
   - the 2020–2024 non-officer field-completeness series;
   - the daily Ida path.
4. Keep only the following main tables:
   - four public field configurations;
   - the July 27–29 transition;
   - later-regime denominator comparison;
   - primary versus secondary comparison designs;
   - measurement implications.
5. Do not restore the eight-statistic table, LP details, threshold counts, full support table, or full bootstrap construction to the main paper.
6. Use plain-language labels in the prose:
   - “arrival only,” not `J01`;
   - “largest percentage-point change,” not `M_max`, except at the formal definition;
   - “post-change ordinary weeks,” not “support-independent universe” except in a methods note.
7. Keep the main paper between 10 and 14 pages.
8. Reject undefined citations/references, overfull boxes, or unreadable tables.

## Empirical-supplement changes

Reorganize the supplement to mirror the new paper, but retain full technical transparency.

Order:

1. Source lineage and parsing rules.
2. Complete July 25–31 raw audit and raw/aggregate parity.
3. Monthly and annual initiation-stream series.
4. Ida daily and half-day field states.
5. Exact construction of the full-count maximum-change statistic.
6. Post-change reference-set construction and exclusions.
7. Full-count bootstrap and dependence caveats.
8. Standardized estimator and support audit.
9. All secondary statistics, LP, threshold variants, and timing placebo.
10. Excluded episodes, including Francine and post-Ida recovery.
11. Disposition accounting.
12. Institutional-source audit.
13. DV measurement bounds.
14. Reproduction claim index.

The supplement may use formal notation. The main paper should not depend on reading it.

## Supporting-document changes

Update:

- `README.md`
- `START_HERE.md`
- `RESEARCH_STATUS_NOTE.md`
- `RESPONSE_TO_ASSESSMENTS.md`
- `REPRODUCTION_MANUAL.md`
- `VERSION.txt`
- `source/research_status_note_*.tex`
- `source/empirical_supplement_*.tex`
- bibliography filename/references if versioned
- PDF build and combine scripts
- manifest builder and manifest
- release ZIP builder if filenames change
- release verifier

The one-page research-status note should use the same four-sentence hierarchy as the new abstract.

## Verification changes

Add automated checks that:

1. The main source contains none of:
   - `U_{\mathrm{direct}}`
   - `U_{\mathrm{full}}`
   - `Q upper`
   - `D upper`
   - `threshold-sensitive`
   - `alternating_phase`
   - `rank 1/152`
   - `J_{01}` outside the definition table or a parenthetical notation note.
2. The main source contains:
   - `53.2 percentage points`
   - `larger than all 151`
   - `43.4 percent on 31 August`
   - `49.3 percent on 1 September`
   - `65.4 percent in 2024`
   - `66.0 percent in 2025`
   - `66.8 percent in the 2026 snapshot`
3. The professor-facing combined PDF contains the main paper and empirical supplement only.
4. The legacy archive remains separate and byte-identical where no intentional cover-page version update is made.
5. Every headline number matches the machine-readable diagnostics.
6. The main paper is 10–14 pages and the abstract is under 190 words.
7. All five public PDFs build cleanly.

## Scientific boundaries

Preserve exactly:

- no causal effect of Ida;
- no identification of physical dispatch or arrival;
- no police-performance estimate;
- no effective-capacity estimate;
- no unique mechanism;
- no DV-incidence or DV-specific treatment effect;
- no claim that `SelfInitiated=N` means 911-only;
- no claim that the bootstrap provides valid time-series rank inference.

## Deliverables

1. New main-paper source and PDF.
2. Updated empirical supplement and PDF.
3. Updated one-page status note.
4. Separate legacy archive.
5. Combined professor-facing PDF.
6. Updated supporting documentation and scripts.
7. A concise change log explaining that the scientific results are unchanged and the release is a narrative/readability overhaul.
8. `RELEASE_VERIFICATION_PASS`.
