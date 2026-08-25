import FormalVerification.BasicDefinitions

/-! Sharp `1/0/U` completion bounds for the declared administrative rule. -/

namespace FormalVerification.DVClassification

def completedCount (knownDV : ℕ) (unresolved : List Bool) : ℕ :=
  knownDV + unresolved.count true

theorem declared_rule_lower_bound (knownDV : ℕ) (unresolved : List Bool) :
    knownDV ≤ completedCount knownDV unresolved := by
  simp [completedCount]

theorem declared_rule_upper_bound (knownDV : ℕ) (unresolved : List Bool) :
    completedCount knownDV unresolved ≤ knownDV + unresolved.length := by
  simp only [completedCount, Nat.add_le_add_iff_left]
  exact List.count_le_length

theorem lower_endpoint_attainable (knownDV unresolvedCount : ℕ) :
    completedCount knownDV (List.replicate unresolvedCount false) = knownDV := by
  simp [completedCount, List.count_replicate]

theorem upper_endpoint_attainable (knownDV unresolvedCount : ℕ) :
    completedCount knownDV (List.replicate unresolvedCount true) =
      knownDV + unresolvedCount := by
  simp [completedCount]

theorem every_integer_attainable
    (knownDV unresolvedCount selected : ℕ)
    (hselected : selected ≤ unresolvedCount) :
    ∃ completion : List Bool,
      completion.length = unresolvedCount ∧
      completedCount knownDV completion = knownDV + selected := by
  refine ⟨List.replicate selected true ++
      List.replicate (unresolvedCount - selected) false, ?_, ?_⟩
  · simp
    omega
  · simp [completedCount, List.count_replicate]

end FormalVerification.DVClassification
