# BELAND-PLUS R11.1 Lean verification

This additive package checks the mathematical claims in the R11.1 main paper and appendix. It preserves `pilot_911_dv/formal_verification`, the earlier accepted package, and does not modify the paper, frozen data, or empirical results.

## Source boundary

The checked sources are:

- `notebooks (For human users)/Final Writings/BELAND_PLUS_M8P_R11_1_LATEX_SOURCES/main_paper_r11_1.tex`
- `notebooks (For human users)/Final Writings/BELAND_PLUS_M8P_R11_1_LATEX_SOURCES/math_appendix_r11_1.tex`

`CLAIM_MAP.md` inventories the equation families and assigns each to kernel proof, finite enumeration, computational testing, or semantic review. Pure definitions are checked for type correctness but do not become empirical facts merely because Lean accepts them.

## Result

- Lean 4.33.0 and Mathlib v4.33.0 are pinned.
- 65 named theorem declarations build successfully.
- The source contains no `sorry`, `admit`, or project-defined axioms.
- The original 29-theorem tranche is preserved.
- The R11.1 additions cover identified-set contraction, target-specific sufficiency and deletion logic, reference standardization, joint-mass identities, sharp `1/0/U` bounds, response/follow-through mixture bounds, priority-history ambiguity, marginal-pairing counterexamples, regularization, tagged unions, set propagation, and the 54-regime count.

## Important finding

The appendix's deterministic-transform argument is valid within a regime:

`raw endpoints + deterministic transform` and `raw endpoints alone` generate the same identified set.

The displayed equality between the 2021 and 2026 identified sets additionally requires the two regimes to induce the same feasible-world restrictions for the target. `DeterministicTransform.lean` proves the within-regime result, proves cross-regime equality under an explicit equal-base assumption, and gives a counterexample showing that determinism alone is insufficient. The R11.1 equation `eq:deterministic_no_gain` therefore remains `NOT_YET_VERIFIED_AS_STATED`.

## Run

From this directory:

```powershell
lake -Kjobs=1 build
python certificates/verify_certificates.py
python enumeration/verify_witness_regimes.py
```

The exact-rational checker fixture is a checker test, not the paper LP. The Ida LP interval remains `TESTED_ONLY` because no canonical rational paper instance and exact primal-dual certificate are supplied.

## Boundary

A successful build proves the formal statements in this package. Source-variable meanings, denominator bindings, institutional interpretations, empirical inputs, and the mapping from prose to formal assumptions still require direct source and human review.
