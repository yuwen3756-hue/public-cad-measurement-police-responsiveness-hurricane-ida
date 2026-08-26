# Current status for professor review

- Release date: 25 August 2026
- Paper version: R15.1
- Scientific-results version: R15
- Package version: 1
- Predecessor: published R15.0 package at commit `5e2af0f`, preserved unchanged

## Recommended reading order

1. `paper/Beland_Current_Status_2026-08-25_R15_1.pdf` — standalone main paper followed by the empirical and methods supplement.
2. `paper/Beland_Research_Status_Note_2026-08-25_R15_1.pdf` — one-page result and evidence-gap summary.
3. `REPRODUCTION_MANUAL.md` — exact build, verification, and interpretation boundaries.
4. `RESPONSE_TO_ASSESSMENTS.md` — item-by-item implementation crosswalk.
5. `review/` — supplied assessment and referee files, treated as review evidence rather than instructions.
6. `paper/Beland_Legacy_Technical_Archive_2026-08-25_R15_1.pdf` — separate extended mathematics and formal verification, only if needed.

## R15.1 improvements

- Defines the measurement in plain language at the start: presence and validity of released dispatch/arrival fields and the distribution of their four joint states.
- Shortens and qualifies the abstract while retaining the break date, Ida magnitude and rank, support caveat, and interpretation boundary.
- Corrects the Miller–Segal placement, adds a literature-contribution synthesis, and removes residual “topology” jargon.
- Adds a compact daily Ida time path and discusses the post-Ida and Francine comparisons in the main paper.
- Standardizes every full-count rank as “rank 1 of $R+1$ including Ida” and labels the post-change universe as post hoc.
- Explains adjacent-window dependence and reports two alternating non-overlap sensitivities: ranks $1/77$ and $1/76$ including Ida.
- Labels the previously unprespecified Cristobal and following-week windows without changing frozen reference membership.
- Adds a machine-enforced $14\times4$ raw-versus-aggregate state parity check and a portable `--source-root` / `BELAND_PUBLIC_SOURCE_ROOT` raw-audit interface.
- Completes annual DataNOLA citations, cites the NOPD policy manual directly, and states that no agency confirmation was available.

## Current scientific status

Ida is a descriptive, reference-extreme reconfiguration of released public fields: standardized $M_{\max}=0.5072$ (rank $1/154$ including Ida) and full-count $M_{\max}=0.5320$ (rank $1/152$ including Ida in the post-hoc post-change universe). The standardized estimate fails the 0.90 symmetric support rule. A conditional window-wise bootstrap that does not model temporal dependence places Ida first in all 4,000 draws.

The institutional documents improve semantics and exclude two candidate technology explanations. They do not supply the historical internal/public bridge needed to identify physical response, performance, capacity, domestic-violence incidence, causal effects, or the generating mechanism.
