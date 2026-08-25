import FormalVerification.BasicDefinitions

/-!
The same binary-mixture argument supplies the R11.1 response-time CDF and
administrative-follow-through bounds.
-/

namespace FormalVerification.SelectionBounds

open FormalVerification.UnitInterval

def mixture (coverage observed missing : ℝ) : ℝ :=
  coverage * observed + (1 - coverage) * missing

theorem sharp_binary_mixture_bounds
    {coverage observed missing : ℝ}
    (hcoverage : Holds coverage) (_hobserved : Holds observed)
    (hmissing : Holds missing) :
    coverage * observed ≤ mixture coverage observed missing ∧
    mixture coverage observed missing ≤
      coverage * observed + (1 - coverage) := by
  have hremain : 0 ≤ 1 - coverage := by linarith [hcoverage.2]
  have hleft : 0 ≤ (1 - coverage) * missing :=
    mul_nonneg hremain hmissing.1
  have hright : (1 - coverage) * missing ≤ 1 - coverage := by
    nlinarith [mul_nonneg hremain (sub_nonneg.mpr hmissing.2)]
  constructor <;> simp only [mixture] <;> linarith

theorem lower_endpoint_attainable
    (coverage observed : ℝ) :
    mixture coverage observed 0 = coverage * observed := by
  simp [mixture]

theorem upper_endpoint_attainable
    (coverage observed : ℝ) :
    mixture coverage observed 1 =
      coverage * observed + (1 - coverage) := by
  simp [mixture]

theorem every_point_attainable
    {coverage observed target : ℝ}
    (hcoverage : Holds coverage)
    (htarget : coverage * observed ≤ target ∧
      target ≤ coverage * observed + (1 - coverage)) :
    ∃ missing : ℝ, Holds missing ∧
      mixture coverage observed missing = target := by
  by_cases hone : coverage = 1
  · subst coverage
    refine ⟨0, ⟨by norm_num, by norm_num⟩, ?_⟩
    simp only [mixture]
    linarith [htarget.1, htarget.2]
  · have hremain : 0 < 1 - coverage := by
      rcases hcoverage with ⟨_, hle⟩
      exact sub_pos.mpr (lt_of_le_of_ne hle hone)
    let missing := (target - coverage * observed) / (1 - coverage)
    refine ⟨missing, ?_, ?_⟩
    · constructor
      · exact div_nonneg (sub_nonneg.mpr htarget.1) (le_of_lt hremain)
      · apply (div_le_one hremain).2
        linarith [htarget.2]
    · dsimp [missing, mixture]
      field_simp
      ring

theorem unavailable_coverage_leaves_unit_interval
    {target : ℝ} (htarget : Holds target) :
    ∃ coverage observed missing : ℝ,
      Holds coverage ∧ Holds observed ∧ Holds missing ∧
      mixture coverage observed missing = target := by
  refine ⟨0, 0, target, ⟨by norm_num, by norm_num⟩,
    ⟨by norm_num, by norm_num⟩, htarget, ?_⟩
  simp [mixture]

end FormalVerification.SelectionBounds
