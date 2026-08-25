# Reproduction Manual

## 1. Purpose

This release supports four distinct checks:

1. **R14 aggregate reconstruction:** rebuild the regime-break, support, ranking, uncertainty, and robustness diagnostics from the packaged aggregate tally and locked reference artifacts.
2. **Document reproduction:** rebuild the main paper, online supplement, and combined PDF from LaTeX.
3. **Numerical and artifact verification:** verify the package manifest and the declared M7B, M7D-E, M8P, and R14 invariants.
4. **Formal verification:** rebuild the Lean theorem package and run the exact-certificate fixture and witness-regime enumeration.

The release contains no raw narratives, addresses, personal identifiers, or private records. Public call-level files are not duplicated. Full call-level replays require the official source caches listed below.

## 2. What we did

The analysis proceeds in six layers:

1. Define five mutually exclusive field-presence states from public dispatch and arrival fields, separately for non-officer-initiated and officer-initiated records.
2. Diagnose the public-file time series. For non-officer-initiated records, $J_{01}$ is exactly zero before 28 July 2021 and positive thereafter. This is treated as an empirical data-regime break; the institutional cause is not identified.
3. Standardize Ida's event-minus-seven-day field-state contrasts within ten fixed 12-hour bins and compare the maximum absolute cell change with ordinary reference windows. The prespecified stage-era set is primary; the full and same-season sets are sensitivities.
4. Add post-review diagnostics: per-bin support, a 4,000-replicate within-stratum categorical bootstrap, all secondary-statistic ranks, threshold sensitivity, an unstandardized full-count comparison, post-change sensitivity, and excluded-event comparisons.
5. Retain the within-disposition Kitagawa decomposition as an accounting localization exercise and the linear-program score as robustness material. Neither supplies an institutional mechanism.
6. Audit the 2025--2026 public architecture and state what additional operational evidence would be needed for a police-performance or DV-specific study.

R14.0 is a major version because it changes both the scientific framing and the reported evidence. It corrects the denominator, brings the public-file regime break and support failure into the main text, adds sampling uncertainty and robustness outputs, demotes mathematical machinery that does not drive the empirical conclusion, and compresses the unestimated DV application.

## 3. Package layout

```text
paper/                         final main, supplement, and combined PDFs
source/                        R14 LaTeX, bibliography, and aggregate diagnostics
scripts/                       R14 builder, verification, replay, and PDF tools
reproduction/repository_snapshot/
  pilot_911_dv/experiments/    empirical code and locked aggregate artifacts
  pilot_911_dv/formal_verification_r11_1/
                                Lean, certificate, and enumeration sources
  pilot_911_dv/source_data/     metadata only; public call-level CSVs excluded
```

`PACKAGE_MANIFEST.sha256` binds every distributed file except itself. Generated temporary files and the release ZIP are excluded.

The R14 evidence files are:

- `source/r14_aggregate_diagnostics.json`: machine-readable headline findings and boundaries.
- `source/r14_weekly_field_completeness.csv` and `source/r14_monthly_field_completeness.csv`: public-field completeness series.
- `source/r14_daily_ida_field_completeness.csv` and `source/r14_period_summary.csv`: break/Ida summaries.
- `source/r14_stage_era_reference_scores.csv` and `source/r14_raw_window_scores.csv`: standardized and unstandardized comparisons.
- `source/r14_secondary_statistic_ranks.csv`: every prespecified secondary-statistic rank in all three reference universes.
- `source/r14_bootstrap_cells.csv`: cell estimates and conditional bootstrap intervals.

## 4. Environment

The recorded environment is:

- Python 3.12.4
- NumPy 1.26.4
- SciPy 1.13.1 with HiGHS dual simplex for the M7B replay
- pandas 2.2.2 for the aggregate R14 builder
- Lean 4 and Mathlib 4.33.0, pinned by `lean-toolchain` and `lake-manifest.json`
- pdfLaTeX and BibTeX through MiKTeX, with embedded Latin Modern fonts
- pypdf 6.10.0 for joining the PDFs

Install the Python requirements from the package root:

```powershell
python -m pip install -r requirements.txt
```

## 5. Fast release verification

From the package root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
```

This read-only check verifies the package manifest; the exact R14 PDF set; the regime-break, support, rank, uncertainty, and boundary invariants; the included M7B, M7D-E, and M8P results; the exact-certificate fixture; and the 54-regime enumeration. Expected terminal status:

```text
RELEASE_VERIFICATION_PASS
```

Important R14 invariants include:

- first positive non-officer $J_{01}$ day: 28 July 2021;
- 66 of 217 full-set reference windows occur entirely before that date and 64 start before the 1 July stage cutoff;
- Ida fails the 0.90 symmetric common-support screen;
- standardized maximum-cell discrepancy 0.5071816170, rank 1/154 including Ida in the stage-era comparison;
- unstandardized maximum-cell discrepancy 0.5319863704, ranked first in both complete stage-era and post-change comparisons;
- 4,000 fixed-seed bootstrap replicates and exact parity with the locked Ida matrix;
- no causal-effect, mechanism, physical-response, or DV-incidence claim.

## 6. Rebuild the R14 aggregate evidence

Run:

```powershell
python .\scripts\build_r14_evidence.py
```

Expected first line:

```text
R14_EVIDENCE_BUILD_PASS
```

The program reads only:

- the packaged aggregate `w2_period_tally.csv.gz`; and
- locked M7B registries, matrices, thresholds, intervals, and statistics.

It does not read raw narratives or row-level private data. The bootstrap resamples the five observed categorical states within each fixed event/reference stratum using a multinomial draw. This is equivalent to resampling categorical records within those observed strata. Its interval is conditional on the public categories, fixed bins, and chosen event/reference pairing; it does not account for reference-set selection, time-series dependence beyond the strata, or the July 2021 regime break.

## 7. Empirical replay

### 7.1 Self-contained aggregate M7B replay

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\replay_m7b.ps1
```

The script creates a disposable copy, reconstructs the paired event-minus-seven-day common-support estimator from the included aggregate tally, and independently resolves the frozen score geometry. Expected final JSON status: `PASS`.

### 7.2 M7D-E call-level replay

The code, disposition sidecar, source registry, aggregate outputs, and independent-replication result are included. The official 2021 call-level cache is not duplicated. Place the exact public files at:

```text
reproduction/repository_snapshot/pilot_911_dv/source_data/
  socrata/nola_3pha-hum9/2021/cad_operational/*.csv.gz
```

The source digest and year binding are in:

```text
reproduction/repository_snapshot/pilot_911_dv/experiments/
  nola_2020-01-01_2024-12-31_beland_plus_wave4r/candidate/
  m7d_d_public_disposition_schema_completion/M7D_D_PUBLIC_SOURCE_REGISTRY.json
```

From `reproduction/repository_snapshot`, run the replay only in a disposable copy:

```powershell
python pilot_911_dv/experiments/nola_2020-01-01_2024-12-31_beland_plus_wave4r/candidate/m7d_e_within_disposition_dispatch_observability/replicate_m7d_e.py
```

### 7.3 M8P current-public-data replay

The official dataset bindings are:

| Year | Socrata dataset | Rows | SHA-256 |
|---|---:|---:|---|
| 2025 | `4xwx-sfte` | 329,770 | `be8416343d253e2518a16ae007568a1561ee8b511dbdef3d5465956a198ae875` |
| 2026 through 11 August | `es9j-6y5d` | 209,829 | `c151ca38199aa53921ad1fe048ee7108f6165e8700ae459070f4c014ce614e17` |

Place the matching public CSVs at:

```text
reproduction/repository_snapshot/pilot_911_dv/source_data/socrata/
  nola_4xwx-sfte/2025/m8p_public_snapshot_2026-08-11/calls_for_service_2025.csv
  nola_es9j-6y5d/2026/m8p_public_snapshot_2026-08-11/calls_for_service_2026.csv
```

From `reproduction/repository_snapshot`, run:

```powershell
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/audit_current_public_data.py
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/build_m8p_outputs.py
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/validate_m8p.py
```

Expected validation status: `PASS` with 20 checks and no failed checks.

## 8. Formal verification

From the package root:

```powershell
Set-Location .\reproduction\repository_snapshot\pilot_911_dv\formal_verification_r11_1
lake -Kjobs=1 build
python certificates\verify_certificates.py
python enumeration\verify_witness_regimes.py
```

The Lean build verifies 65 named declarations with no `sorry`, `admit`, or project-defined axioms. The numerical paper LP remains `TESTED_ONLY`; the exact-rational certificate is a checker fixture, not an exact certificate for the empirical LP. Institutional stages, field meanings, denominators, and source authority remain semantic review questions.

## 9. Rebuild the PDFs

With MiKTeX, Python, and pypdf available:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_pdfs.ps1
```

The script first rebuilds the R14 aggregate evidence, compiles the main paper and supplement, runs BibTeX and the required LaTeX passes, and writes exactly three PDFs to `paper/`.

## 10. Interpretation boundary

The package establishes a descriptive, reference-extreme reconfiguration in the released public record during Ida and documents a preceding public-file regime break. It does not identify police performance, a causal effect, an institutional mechanism, effective capacity, physical response, true DV incidence, or a DV-specific effect. Released call counts are reporting measures conditional on the declared CAD denominator and labeling rule.

The unfavorable timing-shift placebo, incomplete symmetric support, public-file regime change, restricted denominator, and omitted internal provenance all limit interpretation. The 2025--2026 audit documents current public observability but does not turn administrative timestamps into verified operational clocks.

## 11. Literature placement

The main paper cites Brent and Beland (2020) as the closest economics antecedent: it demonstrates the value of valid first-responder response clocks using linked operational incident and traffic data. Four disaster--IPV studies establish substantive motivation but use different outcomes and designs; they do not validate public CAD fields or identify an Ida effect on reported DV calls. R14 therefore keeps the DV discussion short and prospective.

Unpublished or inaccessible items flagged in review were removed from the manuscript bibliography: the project talk, the project self-citation, and the unverified working-paper citation. Reproduction artifacts retain their historical filenames and labels only where changing them would alter predecessor evidence.

## 12. Version and predecessor

- Paper: R14.0
- Scientific results: R14
- Package: 1
- Untouched predecessor: `beland_plus_current_status_professor_2026-08-24_r13_0_v1`
- Public repository: `https://github.com/yuwen3756-hue/beland-plus-current-status-2026-08-24-r12-2`
