import FormalVerification.BasicDefinitions

namespace FormalVerification.BridgeProduct

def CaptureDefined (internalPrevalence : ℝ) : Prop := 0 < internalPrevalence

theorem admissible_factorization
    {q u : ℝ} (hq0 : 0 < q) (hqu : q ≤ u) (hu1 : u ≤ 1) :
    FormalVerification.UnitInterval.Holds u ∧
    FormalVerification.UnitInterval.Holds (q / u) ∧
    u * (q / u) = q := by
  have hu0 : 0 < u := lt_of_lt_of_le hq0 hqu
  constructor
  · exact ⟨le_of_lt hu0, hu1⟩
  constructor
  · constructor
    · exact div_nonneg (le_of_lt hq0) (le_of_lt hu0)
    · exact (div_le_iff₀ hu0).2 (by simpa using hqu)
  · field_simp

theorem distinct_endpoint_factorizations
    {q : ℝ} (hq0 : 0 < q) (hq1 : q < 1) :
    FormalVerification.UnitInterval.Holds q ∧
    FormalVerification.UnitInterval.Holds (1 : ℝ) ∧
    q * 1 = q ∧ 1 * q = q ∧ (q, (1 : ℝ)) ≠ ((1 : ℝ), q) := by
  refine ⟨⟨le_of_lt hq0, le_of_lt hq1⟩, ⟨by norm_num, by norm_num⟩, by ring, by ring, ?_⟩
  intro hpairs
  have : q = 1 := congrArg Prod.fst hpairs
  linarith

theorem one_product_forces_factors_one
    {u chi : ℝ}
    (hu : FormalVerification.UnitInterval.Holds u)
    (hchi : FormalVerification.UnitInterval.Holds chi)
    (hproduct : u * chi = 1) :
    u = 1 ∧ chi = 1 := by
  constructor <;> nlinarith [hu.1, hu.2, hchi.1, hchi.2]

theorem positive_internal_zero_product
    {u chi : ℝ} (hu : 0 < u) (hproduct : u * chi = 0) : chi = 0 := by
  rcases mul_eq_zero.mp hproduct with hu0 | hchi
  · exact False.elim ((ne_of_gt hu) hu0)
  · exact hchi

theorem zero_internal_gives_zero_product (chi : ℝ) : (0 : ℝ) * chi = 0 := by
  ring

theorem zero_internal_conditioning_cell_undefined : ¬ CaptureDefined 0 := by
  simp [CaptureDefined]

end FormalVerification.BridgeProduct
