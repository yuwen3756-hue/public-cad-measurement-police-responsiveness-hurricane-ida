# BELAND-PLUS R11.1 mathematical verification report

## Verdict

The R11.1 mathematical core is coherent. The Lean kernel accepts 65 named theorems covering the public-state algebra, standardization identities, decomposition, partial-identification boundaries, queue logic, DV classification bounds, selection bounds, witness deletion, and finite regime count.

One appendix theorem needs revision before the paper can claim complete mathematical closure: `eq:deterministic_no_gain` equates a 2026 identified set with a 2021 identified set. A deterministic dashboard transform proves redundancy relative to its own raw vector. Equality across regimes additionally requires equality of the underlying feasible-world restrictions. The current prose mentions a common semantic map but does not state that stronger premise.

## Source authority

| Read-only R11.1 source | Bytes | SHA-256 |
|---|---:|---|
| `main_paper_r11_1.tex` | 50,010 | `cc97ed125276c5d1cb6a580401f5d3b9549ddd7379ce1b8e5e193f41c59db390` |
| `math_appendix_r11_1.tex` | 66,240 | `d0f4e0071b3047670a0f3942ccc5591b233019cea606d4a22d7bca90556fb7d4` |
| `01_MAIN_SUMMER_PAPER_M8P_R11_1.pdf` | 467,520 | `0ca5b0cc48a1ea0340f698a8809cfbc7a24b9c77a8ed9f84855ac312674c1b60` |
| `07_MATHEMATICAL_AND_REPRODUCIBILITY_APPENDIX_M8P_R11_1.pdf` | 636,718 | `49b82b5464ec02de2b15e604df278bdfbbc650bdf7728d580fd445ae86a6bf9b` |
| `BELAND_PLUS_SUMMER_PAPER_WITH_APPENDIX_M8P_R11_1.pdf` | 1,073,069 | `006723fd306bf42863ed31ec0f21c0a93c35b36ac77300f22a7db980feeea11a` |

The paper and frozen scientific artifacts were not modified.

## Kernel and computational checks

| Check | Result |
|---|---|
| Lean toolchain | `leanprover/lean4:v4.33.0` |
| Mathlib | `v4.33.0` |
| `lake -Kjobs=1 build` | `PASS`, 8,725 jobs |
| Named theorem declarations | 65 |
| `sorry`, `admit`, project `axiom` scan | `PASS`, zero hits |
| Axiom printout | Standard Lean foundations only |
| Exact-rational checker fixture | `CERTIFICATE_VERIFIED`; primal = dual = `7/3`; forged certificate rejected |
| Witness-regime enumeration | `EXHAUSTIVELY_ENUMERATED`; 54 legal, 47 multi-module, unique, dependency forgery rejected |
| Paper LP exact rational certificate | `NOT_YET_VERIFIED` |
| Paper LP numerical interval | `TESTED_ONLY`; preserved predecessor classification |

## R11.1 additions verified

- Stronger witness restrictions contract the measure-specific identified set.
- Pairwise identified-set tolerance is monotone under set contraction.
- Inclusion-minimality follows from sufficiency plus every-member deletion failure.
- Reference-standardized shares preserve the simplex, and event-reference contrasts sum to zero.
- Joint masses recover recorded mass; positive recorded mass recovers the conditional share; the joint-mass change equals the symmetric Kitagawa decomposition.
- The declared `1/0/U` count bound is sharp at both endpoints and attains every intermediate integer.
- Binary selection mixtures yield the sharp response-CDF and follow-through bounds, including every intermediate point.
- Endpoint disagreement implies a priority change and therefore its event probability cannot exceed the probability of any history change; equal endpoints admit both stable and offsetting completions.
- Separate clock marginals admit different duration distributions; separate eligibility and completion marginals admit different eligible-completion totals.
- A unique regularized minimizer can coexist with a nonsingleton data-consistent set.
- Tagged model unions retain model tags; moment-region propagation contains the true target whenever its premises hold.
- The six legal ordered queue-priority levels and two independent three-level modules yield exactly 54 regimes.

## Material finding: deterministic-transform theorem

The kernel verifies:

1. If `derived = g(raw)`, then adding `derived` to the same raw endpoint information leaves the identified set unchanged.
2. If the 2021 and 2026 base compatibility predicates are pointwise equivalent, the two identified sets are equal.
3. Determinism alone does not imply the cross-regime equality; an explicit Boolean counterexample compiles.

The safest paper repair is to replace the displayed equation with the within-2026 equality

`I_2026(theta | Y_Ida, Y_26_raw, g(Y_26_raw), h) = I_2026(theta | Y_Ida, Y_26_raw, h)`.

If the cross-regime equality is substantively intended, add a premise that the normalized shared endpoints and every restriction defining the target-compatible worlds coincide across the two regimes. A common semantic map alone does not supply that equality.

This clarification does not change the frozen Ida estimates or the paper's central DV measurement-admissibility result.

## Boundaries

- The support-library construction, source weights, strata, chronology windows, and public-field semantics require direct artifact review.
- The Ida minimax score and ranks are floating-point scientific results. They remain `TESTED_ONLY` until a canonical rational LP instance and exact primal-dual certificate exist.
- The witness-minimality application assumes the named variables define the intended denominator, clock, history, and follow-through duty. Lean verifies the logic and counterexamples, not those bindings.
- No DV-specific estimator or police-performance change is proved or computed.
- Kernel acceptance does not establish mechanism, causal effects, physical service, true DV incidence, or victim safety.
