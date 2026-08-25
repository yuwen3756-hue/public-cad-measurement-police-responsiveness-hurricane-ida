import FormalVerification.BasicDefinitions

namespace FormalVerification.Frechet

/-!
The four cells are a normalized nonnegative 2x2 table. The overlap is `n11`;
the two marginals are `n10 + n11` and `n01 + n11`.
-/

theorem overlap_bounds
    {n00 n01 n10 n11 : ℝ}
    (h00 : 0 ≤ n00) (h01 : 0 ≤ n01) (h10 : 0 ≤ n10) (h11 : 0 ≤ n11)
    (hnorm : n00 + n01 + n10 + n11 = 1) :
    max 0 ((n10 + n11) + (n01 + n11) - 1) ≤ n11 ∧
    n11 ≤ min (n10 + n11) (n01 + n11) := by
  constructor
  · rw [max_le_iff]
    constructor <;> nlinarith
  · rw [le_min_iff]
    constructor <;> nlinarith

theorem conditional_overlap_bounds
    {n00 n01 n10 n11 : ℝ}
    (h00 : 0 ≤ n00) (h01 : 0 ≤ n01) (h10 : 0 ≤ n10) (h11 : 0 ≤ n11)
    (hnorm : n00 + n01 + n10 + n11 = 1)
    (hu : 0 < n01 + n11) :
    max 0 ((n10 + n11) + (n01 + n11) - 1) / (n01 + n11) ≤
        n11 / (n01 + n11) ∧
    n11 / (n01 + n11) ≤
        min (n10 + n11) (n01 + n11) / (n01 + n11) := by
  have hoverlap := overlap_bounds h00 h01 h10 h11 hnorm
  constructor
  · exact (div_le_div_iff_of_pos_right hu).2 hoverlap.1
  · exact (div_le_div_iff_of_pos_right hu).2 hoverlap.2

theorem marginals_normalized
    {n00 n01 n10 n11 : ℝ}
    (h00 : 0 ≤ n00) (h01 : 0 ≤ n01) (h10 : 0 ≤ n10) (h11 : 0 ≤ n11)
    (hnorm : n00 + n01 + n10 + n11 = 1) :
    FormalVerification.UnitInterval.Holds (n10 + n11) ∧
    FormalVerification.UnitInterval.Holds (n01 + n11) := by
  constructor <;> constructor <;> nlinarith

theorem lower_endpoint_attainable
    {d u : ℝ}
    (hd : FormalVerification.UnitInterval.Holds d)
    (hu : FormalVerification.UnitInterval.Holds u)
    (huPos : 0 < u) :
    let z := max 0 (d + u - 1)
    let n11 := z
    let n10 := d - z
    let n01 := u - z
    let n00 := 1 - d - u + z
    0 ≤ n00 ∧
    0 ≤ n01 ∧
    0 ≤ n10 ∧
    0 ≤ n11 ∧
    n00 + n01 + n10 + n11 = 1 ∧
    n10 + n11 = d ∧
    n01 + n11 = u ∧
    0 < n01 + n11 ∧
    n11 / u = max 0 (d + u - 1) / u := by
  dsimp
  have hzNonneg : 0 ≤ max 0 (d + u - 1) := le_max_left _ _
  have hzLeD : max 0 (d + u - 1) ≤ d := by
    apply max_le hd.1
    linarith [hu.2]
  have hzLeU : max 0 (d + u - 1) ≤ u := by
    apply max_le hu.1
    linarith [hd.2]
  have hsumLeZ : d + u - 1 ≤ max 0 (d + u - 1) := le_max_right _ _
  refine ⟨by linarith, by linarith, by linarith, hzNonneg, ?_, ?_, ?_, ?_, rfl⟩
  · ring
  · ring
  · ring
  · linarith

theorem upper_endpoint_attainable
    {d u : ℝ}
    (hd : FormalVerification.UnitInterval.Holds d)
    (hu : FormalVerification.UnitInterval.Holds u)
    (huPos : 0 < u) :
    let z := min d u
    let n11 := z
    let n10 := d - z
    let n01 := u - z
    let n00 := 1 - d - u + z
    0 ≤ n00 ∧
    0 ≤ n01 ∧
    0 ≤ n10 ∧
    0 ≤ n11 ∧
    n00 + n01 + n10 + n11 = 1 ∧
    n10 + n11 = d ∧
    n01 + n11 = u ∧
    0 < n01 + n11 ∧
    n11 / u = min d u / u := by
  dsimp
  have hzNonneg : 0 ≤ min d u := le_min hd.1 hu.1
  have hzLeD : min d u ≤ d := min_le_left _ _
  have hzLeU : min d u ≤ u := min_le_right _ _
  have hsumLeZ : d + u - 1 ≤ min d u := by
    apply le_min
    · linarith [hu.2]
    · linarith [hd.2]
  refine ⟨by linarith, by linarith, by linarith, hzNonneg, ?_, ?_, ?_, ?_, rfl⟩
  · ring
  · ring
  · ring
  · linarith

end FormalVerification.Frechet
