import FormalVerification.BasicDefinitions

/-! Algebra of reference-standardized state shares and contrasts. -/

namespace FormalVerification.Standardization

open scoped BigOperators

def standardizedShare
    {Stratum State : Type*} [Fintype Stratum]
    (weights : Stratum → ℝ) (shares : Stratum → State → ℝ)
    (state : State) : ℝ :=
  ∑ stratum, weights stratum * shares stratum state

def standardizedContrast
    {Stratum State : Type*} [Fintype Stratum]
    (weights : Stratum → ℝ)
    (eventShares referenceShares : Stratum → State → ℝ)
    (state : State) : ℝ :=
  standardizedShare weights eventShares state -
    standardizedShare weights referenceShares state

theorem standardized_simplex
    {Stratum State : Type*} [Fintype Stratum] [Fintype State]
    (weights : Stratum → ℝ) (shares : Stratum → State → ℝ)
    (hweights : ∑ stratum, weights stratum = 1)
    (hshares : ∀ stratum, ∑ state, shares stratum state = 1) :
    ∑ state, standardizedShare weights shares state = 1 := by
  rw [show (∑ state, standardizedShare weights shares state) =
      ∑ stratum, weights stratum * (∑ state, shares stratum state) by
    simp only [standardizedShare, Finset.mul_sum]
    rw [Finset.sum_comm]]
  simp [hshares, hweights]

theorem standardized_contrast_sums_to_zero
    {Stratum State : Type*} [Fintype Stratum] [Fintype State]
    (weights : Stratum → ℝ)
    (eventShares referenceShares : Stratum → State → ℝ)
    (hweights : ∑ stratum, weights stratum = 1)
    (hevent : ∀ stratum, ∑ state, eventShares stratum state = 1)
    (href : ∀ stratum, ∑ state, referenceShares stratum state = 1) :
    ∑ state, standardizedContrast weights eventShares referenceShares state = 0 := by
  simp only [standardizedContrast, Finset.sum_sub_distrib]
  rw [standardized_simplex weights eventShares hweights hevent]
  rw [standardized_simplex weights referenceShares hweights href]
  norm_num

theorem omitted_state_determined
    {j00 j01 j10 j11 : ℝ}
    (hsimplex : j00 + j01 + j10 + j11 = 0) :
    j00 = -(j01 + j10 + j11) := by
  linarith

end FormalVerification.Standardization
