import FormalVerification.BasicDefinitions

namespace FormalVerification.CompositionOnly

theorem sign_nonnegative
    {q deltaMass deltaH11 deltaH01 : ℝ}
    (hq : FormalVerification.UnitInterval.Holds q)
    (h11 : deltaH11 = q * deltaMass)
    (h01 : deltaH01 = (1 - q) * deltaMass) :
    0 ≤ deltaH11 * deltaH01 := by
  rw [h11, h01]
  have hqcomp : 0 ≤ q * (1 - q) :=
    mul_nonneg hq.1 (sub_nonneg.mpr hq.2)
  nlinarith [sq_nonneg deltaMass]

theorem negative_sign_rejects_composition_only
    {q deltaMass deltaH11 deltaH01 : ℝ}
    (hq : FormalVerification.UnitInterval.Holds q)
    (h11 : deltaH11 = q * deltaMass)
    (h01 : deltaH01 = (1 - q) * deltaMass)
    (hnegative : deltaH11 * deltaH01 < 0) : False := by
  have hnonnegative := sign_nonnegative hq h11 h01
  linarith

theorem boundary_q_zero (deltaMass : ℝ) :
    (0 : ℝ) * deltaMass = 0 ∧ (1 - (0 : ℝ)) * deltaMass = deltaMass := by
  constructor <;> ring

theorem boundary_q_one (deltaMass : ℝ) :
    (1 : ℝ) * deltaMass = deltaMass ∧ (1 - (1 : ℝ)) * deltaMass = 0 := by
  constructor <;> ring

theorem dropped_unit_interval_counterexample :
    let q : ℝ := -1
    let deltaMass : ℝ := 1
    (q * deltaMass) * ((1 - q) * deltaMass) < 0 := by
  norm_num

end FormalVerification.CompositionOnly
