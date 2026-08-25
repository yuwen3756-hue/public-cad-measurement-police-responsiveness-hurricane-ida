# Reproduction Manual

## 1. Purpose

This package supports three different checks that should not be conflated:

1. **Document reproduction:** rebuild the main paper, appendix, and combined PDF from LaTeX.
2. **Numerical and artifact verification:** verify the frozen results and independent-replication outputs included in the package.
3. **Formal verification:** rebuild the Lean theorem package and run the exact-certificate fixture and witness-regime enumeration.

The package also includes the full empirical replay programs. Public call-level source files are not duplicated into this release. A full raw-data replay therefore requires the exact public source caches listed in Section 6.

## 2. What we did

The work proceeded in five layers:

1. Defined four public CAD field-presence states from dispatch and arrival fields and standardized event-reference contrasts within ten frozen 12-hour bins.
2. Applied the same restricted-support discrepancy estimator to Ida and 217 qualified reference windows. Two narrower comparison sets were retained as prespecified sensitivity designs.
3. Decomposed the dispatch-field change among arrival-field records into disposition-composition and within-disposition components.
4. Mapped candidate reported-DV performance measures to measure-specific identified sets and the minimum privacy-safe witnesses needed to contract them.
5. Replayed the 2025-2026 public-data architecture to determine whether newer public fields close the structural measurement gaps. They improve description but do not establish a strict mechanism-relevant identified-set contraction.

R12.2 refined the identification and literature framing while retaining R12 mathematics and numerical results. This release changes title-page presentation and packaging only.

## 3. Package layout

```text
paper/                         final main, appendix, and combined PDFs
source/                        self-contained LaTeX and bibliography
scripts/                       verification, replay, and PDF-build entry points
reproduction/repository_snapshot/
  pilot_911_dv/experiments/    empirical code and locked aggregate artifacts
  pilot_911_dv/formal_verification_r11_1/
                                Lean, certificate, and enumeration sources
  pilot_911_dv/source_data/     metadata only; public call-level CSVs excluded
```

`PACKAGE_MANIFEST.sha256` binds the distributed files. The manifest excludes itself.

## 4. Environment

The recorded computational environment was:

- Python 3.12.4
- NumPy 1.26.4
- SciPy 1.13.1 with HiGHS dual simplex for the M7B LP replay
- Lean 4 and Mathlib 4.33.0, pinned by `lean-toolchain` and `lake-manifest.json`
- pdfLaTeX and BibTeX through MiKTeX, with Latin Modern fonts
- pypdf 6.10.0 for joining the two PDFs in this release

Install the Python requirements from the package root:

```powershell
python -m pip install -r requirements.txt
```

## 5. Fast verification from included artifacts

From the package root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
```

This is read-only. It verifies the package manifest and checks the declared M7B, M7D-E, and M8P invariants. It also runs the exact-certificate fixture and the 54-regime enumeration. Expected terminal status: `RELEASE_VERIFICATION_PASS`.

Expected empirical invariants include:

- M7B: 217 full qualified reference windows; Ida rank 1 in the full, stage-era, and same-season-stage sets; maximum Ida matrix parity error no larger than $10^{-10}$; no Ida-reference interval overlap.
- M7D-E: independent parent parity and Kitagawa identity residuals below $10^{-12}$; independent replication `PASS`.
- M8P: 20 focused validation checks pass; decision `M8P_PUBLIC_OBSERVABILITY_PARTIALLY_IMPROVED`; strict-contraction list empty; all four M8D structural witness statuses `CLOSED`.

## 6. Empirical replay

### 6.1 Self-contained aggregate-only M7B replay

The M7B independent replay is self-contained in the package. It reconstructs the paired event-minus-seven-day, within-bin common-support estimator from the included aggregate tally and independently resolves the frozen score geometry.

Run it in a disposable copy created automatically by:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\replay_m7b.ps1
```

Expected final JSON status: `PASS`.

### 6.2 M7D-E full replay

The code, disposition sidecar, source registry, aggregate outputs, and independent-replication result are included. The public 2021 call-level cache is not duplicated. To run the full replay, place the exact public files at:

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

Then, from `reproduction/repository_snapshot`:

```powershell
python pilot_911_dv/experiments/nola_2020-01-01_2024-12-31_beland_plus_wave4r/candidate/m7d_e_within_disposition_dispatch_observability/replicate_m7d_e.py
```

This program writes beside its inputs. Run it only in a disposable copy.

### 6.3 M8P current-public-data replay

The official dataset bindings are:

| Year | Socrata dataset | Rows | SHA-256 |
|---|---:|---:|---|
| 2025 | `4xwx-sfte` | 329,770 | `be8416343d253e2518a16ae007568a1561ee8b511dbdef3d5465956a198ae875` |
| 2026 | `es9j-6y5d` | 209,829 | `c151ca38199aa53921ad1fe048ee7108f6165e8700ae459070f4c014ce614e17` |

Place the matching public CSVs at:

```text
reproduction/repository_snapshot/pilot_911_dv/source_data/socrata/
  nola_4xwx-sfte/2025/m8p_public_snapshot_2026-08-11/calls_for_service_2025.csv
  nola_es9j-6y5d/2026/m8p_public_snapshot_2026-08-11/calls_for_service_2026.csv
```

Metadata, column definitions, official current-architecture extracts, and the frozen source manifest are included. From `reproduction/repository_snapshot`, run:

```powershell
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/audit_current_public_data.py
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/build_m8p_outputs.py
python pilot_911_dv/experiments/nola_2025-01-01_2026-08-11_m8p_public_observability_replay/notebooks/validate_m8p.py
```

Expected validation status: `PASS` with 20 checks and no failed checks.

## 7. Formal verification

From the package root:

```powershell
Set-Location .\reproduction\repository_snapshot\pilot_911_dv\formal_verification_r11_1
lake -Kjobs=1 build
python certificates\verify_certificates.py
python enumeration\verify_witness_regimes.py
```

The Lean build verifies 65 named theorem declarations with no `sorry`, `admit`, or project-defined axioms. The numerical paper LP remains `TESTED_ONLY`; the included exact-rational certificate is a checker fixture, not an exact certificate for the paper LP. Field meanings, institutional stages, denominators, and source authority remain semantic review questions.

## 8. Rebuild the PDFs

With MiKTeX, Python, and pypdf available:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_pdfs.ps1
```

The script compiles the main paper and appendix, runs BibTeX, performs the required LaTeX passes, and writes the three PDFs to `paper/`.

## 9. Interpretation boundary

The package measures a descriptive, reference-extreme change in the released public record under system stress. It does not identify police performance, effective capacity, physical response, a causal mechanism, true DV incidence, or a DV-specific treatment effect. Reported DV-related calls remain administrative reporting measures conditional on the declared CAD denominator and labeling rule.
