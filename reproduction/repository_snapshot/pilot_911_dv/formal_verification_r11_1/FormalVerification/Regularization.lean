import FormalVerification.BasicDefinitions

/-! A unique regularized selector can coexist with a nonsingleton feasible set. -/

namespace FormalVerification.Regularization

def feasibleTheta : Set ℤ := {theta | theta = 0 ∨ theta = 1}

def quadraticRegularizer (theta : ℤ) : ℤ := theta ^ 2

theorem feasible_set_not_singleton :
    (0 : ℤ) ∈ feasibleTheta ∧ (1 : ℤ) ∈ feasibleTheta ∧
      (0 : ℤ) ≠ 1 := by
  norm_num [feasibleTheta]

theorem zero_is_unique_regularized_selector :
    ∃! theta : ℤ, theta ∈ feasibleTheta ∧
      ∀ other ∈ feasibleTheta,
        quadraticRegularizer theta ≤ quadraticRegularizer other := by
  refine ⟨0, ?_, ?_⟩
  · constructor
    · simp [feasibleTheta]
    · intro other hother
      rcases hother with (rfl | rfl) <;>
        norm_num [quadraticRegularizer]
  · intro theta htheta
    rcases htheta.1 with (rfl | rfl)
    · rfl
    · have h := htheta.2 0 (by simp [feasibleTheta])
      norm_num [quadraticRegularizer] at h

end FormalVerification.Regularization
