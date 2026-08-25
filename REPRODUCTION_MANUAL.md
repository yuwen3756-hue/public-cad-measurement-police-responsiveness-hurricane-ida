# Reproduction manual

## 1. Scope

This package supports five checks:

1. Rebuild the aggregate regime-break, support, ranking, uncertainty, initiation-stream, and current-denominator diagnostics.
2. Reproduce the first-hand public-source lineage and July 2021 audit when the canonical official cache is available.
3. Build the main paper, empirical supplement, one-page status note, separate legacy archive, and professor-facing combined PDF.
4. Verify exact numerical, textual, PDF, snapshot-parity, and manifest invariants.
5. Rebuild the inherited numerical and formal-verification artifacts when their specialized runtimes are available.

The package contains no call narratives, exact addresses, personal identifiers, or private records. Public call-level source files are not duplicated.

## 2. Package layout

```text
paper/                         five final PDFs
source/                        LaTeX, bibliography, aggregate tables, audits
scripts/                       builders, verifier, manifest, ZIP, parity tools
reproduction/repository_snapshot/
  pilot_911_dv/experiments/    locked aggregate and empirical artifacts
  pilot_911_dv/formal_verification_r11_1/
                                Lean and exact-checker sources
  pilot_911_dv/source_data/     metadata only; public row files excluded
```

The professor-facing combined PDF contains only the main paper and empirical supplement. The mathematical/formal archive is a separate file.

`PACKAGE_MANIFEST.sha256` binds every curated file, including `README.md`, `.gitattributes`, the parity receipt, PDFs, sources, scripts, and reproduction snapshot. It excludes itself, `tmp/`, Python caches, and the generated ZIP. `.gitattributes` uses `* -text`; the snapshot parity receipt compares every copied snapshot file byte-for-byte with the published predecessor.

## 3. Environment

- Python 3.12+
- NumPy 1.26.4
- SciPy 1.13.1 for inherited constrained-optimization replay
- pypdf 6.10.0 for PDF combination and verification
- MiKTeX pdfLaTeX and BibTeX with Latin Modern fonts
- Lean 4 / Mathlib 4.33.0 only for the separate formal archive

Install:

```powershell
python -m pip install -r requirements.txt
```

The R15 evidence builder uses Python's standard library and NumPy. It does not use pandas. The four mutually exclusive public states are $J_{00}$, $J_{10}$, $J_{01}$, and $J_{11}$.

## 4. Fast verification

From the package root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
```

Expected terminal status:

```text
RELEASE_VERIFICATION_PASS
```

The verifier checks the manifest, exact five-PDF set, page relationships, embedded scientific text, forbidden revision-history language in the main source, source-audit invariants, 2025/2026 denominator arithmetic, 4,000-draw bootstrap outputs, support/rank/threshold results, snapshot parity, inherited empirical invariants, and exact-checker fixtures.

## 5. Rebuild aggregate evidence

```powershell
python .\scripts\build_r15_evidence.py
```

Expected status:

```text
R15_EVIDENCE_BUILD_PASS
```

The builder reads the packaged aggregate `w2_period_tally.csv.gz`, locked reference registries/matrices/thresholds/intervals/statistics, and packaged 2025–2026 aggregate validity audit. It writes:

- `r15_aggregate_diagnostics.json`
- weekly, monthly, and annual initiation-stream completeness tables
- daily Ida and period summaries
- standardized and raw reference scores
- all secondary-statistic ranks
- cell-level Ida bootstrap output
- Ida/top-five standardized and full-count bootstrap intervals
- the full 151-reference post-change bootstrap rank distribution
- 2025/2026 denominator audit

The bootstrap is conditional on observed public categories, stratum totals, fixed bins, and the chosen reference design. It does not model time-series dependence or uncertainty in the July regime boundary.

## 6. Reproduce the raw public-source audit

This optional step requires the canonical official monthly DataNOLA cache at:

```text
pilot_911_dv/source_data/socrata/
  nola_hp7u-i9hf/2020/cad_operational/*.csv.gz
  nola_3pha-hum9/2021/cad_operational/*.csv.gz
  nola_nci8-thrr/2022/cad_operational/*.csv.gz
  nola_pc5d-tvaw/2023/cad_operational/*.csv.gz
  nola_2zcj-b6ts/2024/cad_operational/*.csv.gz
```

Run from this package inside the project:

```powershell
python .\scripts\audit_public_source_lineage.py
```

Expected status:

```text
R15_PUBLIC_SOURCE_AUDIT_PASS
```

The audit records official dataset IDs and URLs, observed date limits, raw row counts, monthly hashes, deterministic annual bundle hashes, local cache mtimes, verification date, parsing rules, and aggregate July 25–31 state counts. It explicitly reports that retrieval dates were not recorded in the monthly cache. No row-level value is persisted.

## 7. Build the PDFs

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_pdfs.ps1
```

To rebuild the public-source audit in the same run when the canonical cache exists:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_pdfs.ps1 -RunRawSourceAudit
```

The build recompiles every LaTeX document, rejects undefined references/citations and overfull boxes, combines only the main paper and empirical supplement, and writes exactly five PDFs to `paper/`.

## 8. Key invariants

- First positive non-officer $J_{01}$ day: 28 July 2021.
- Raw 27–29 July officer dispatch presence: 479/479, 230/575, 5/504.
- Standardized $M_{\max}=0.5071816170$, rank $1/154$.
- Full-count $M_{\max}=0.5319863704$, post-change rank $1/152$.
- Ida support: 86.1% event and 77.0% baseline, failing the 0.90 symmetric rule.
- Threshold exceedance counts: 9/8/9 across full/stage/same-season reference sets.
- 4,000 bootstrap draws; full-count Ida rank is 1 in every draw against 151 post-change references.
- 2025 non-officer: 136,712/207,050 = 66.03%; officer: 1,117/122,720 = 0.91%; all rows: 137,829/329,770 = 41.80%.
- 2026 snapshot non-officer dispatch share: 66.84%.
- No causal-effect, mechanism, physical-response, capacity, performance, or DV-incidence claim.

## 9. Inherited empirical and formal replay

The self-contained aggregate reference replay is:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\replay_m7b.ps1
```

The full call-level disposition replay requires the exact official 2021 cache and should run in a disposable copy. The 2025/2026 replay requires the exact official annual files identified in the snapshot metadata.

For the formal archive:

```powershell
Set-Location .\reproduction\repository_snapshot\pilot_911_dv\formal_verification_r11_1
lake -Kjobs=1 build
python certificates\verify_certificates.py
python enumeration\verify_witness_regimes.py
```

Lean verifies mathematical statements under stated assumptions. The empirical LP remains `TESTED_ONLY`; field meanings, source authority, and institutional bindings are not proved by the kernel.

## 10. Manifest and ZIP

After a clean PDF build and verification:

```powershell
python .\scripts\build_snapshot_parity_receipt.py
python .\scripts\build_manifest.py
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
python .\scripts\build_release_zip.py
```

The ZIP is written beside the package directory and is excluded from the internal manifest.

## 11. Interpretation boundary

The package identifies a public-record regime change before Ida and a reference-extreme public-field reconfiguration during Ida. Institutional documents improve semantics and eliminate two candidate technology explanations. They do not supply the historical bridge from internal events and entry histories to released fields. Public counts remain reporting measures, and public timestamps remain administrative-field measures unless separately validated as stable operational clocks.
