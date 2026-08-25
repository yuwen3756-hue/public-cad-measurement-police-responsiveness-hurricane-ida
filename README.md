# Public CAD Is Not Operational Ground Truth

- **Release:** 24 August 2026
- **Paper:** R14.0
- **Scientific results:** R14

This repository contains the professor-review package for *Public CAD Is Not Operational Ground Truth: Regime Change, Hurricane Ida, and the Measurement of Police Responsiveness*.

## Read

- [Combined paper and online supplement](paper/Beland_Current_Status_2026-08-24_R14_0.pdf)
- [10-page main paper](paper/Beland_Current_Status_Main_2026-08-24_R14_0.pdf)
- [30-page online supplement](paper/Beland_Current_Status_Appendix_2026-08-24_R14_0.pdf)
- [Release overview](START_HERE.md)
- [Reproduction manual](REPRODUCTION_MANUAL.md)

## R14.0 in brief

R14.0 is a major referee-response revision. It makes the 28 July 2021 public-file regime break the first result, corrects the estimator denominator to non-officer-initiated records, uses the transparent maximum-cell contrast as the headline statistic, makes the stage-era comparison primary, discloses Ida's failure of the 0.90 symmetric support rule, and adds conditional bootstrap intervals, full-count robustness, every secondary-statistic rank, threshold sensitivity, and excluded-emergency comparisons.

The result is descriptive: Ida is an extreme reconfiguration of the released public record relative to retained ordinary weeks. The analysis does not identify police performance, a causal effect, an institutional mechanism, physical response, effective capacity, true domestic-violence incidence, or a DV-specific effect.

## Reproduce

From the repository root:

```powershell
python .\scripts\build_r14_evidence.py
powershell -ExecutionPolicy Bypass -File .\scripts\verify_release.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\replay_m7b.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_pdfs.ps1
```

See the reproduction manual for environment details, source-cache bindings, and the formal-verification commands.
