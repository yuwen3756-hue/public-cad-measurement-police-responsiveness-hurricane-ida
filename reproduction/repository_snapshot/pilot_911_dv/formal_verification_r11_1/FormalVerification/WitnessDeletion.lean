import FormalVerification.PriorityHistory

/-!
Finite counterexamples behind the R11.1 witness-deletion statements.  They
show why separate marginal aggregates do not preserve call-level pairing.
-/

namespace FormalVerification.WitnessDeletion

def durations (origins endpoints : List ℤ) : List ℤ :=
  List.zipWith (· - ·) endpoints origins

theorem clock_marginals_do_not_identify_duration_distribution :
    let origins : List ℤ := [0, 10]
    let endpointsAligned : List ℤ := [10, 20]
    let endpointsCrossed : List ℤ := [20, 10]
    endpointsAligned.Perm endpointsCrossed ∧
      ¬ (durations origins endpointsAligned).Perm
        (durations origins endpointsCrossed) := by
  dsimp [durations]
  constructor
  · exact (List.Perm.swap (10 : ℤ) 20 []).symm
  · intro hperm
    have hcount := hperm.count 10
    norm_num at hcount

def eligibleCompletionCount (rows : List (Bool × Bool)) : ℕ :=
  (rows.filter fun row => row.1 && row.2).length

def eligibilityMarginal (rows : List (Bool × Bool)) : List Bool :=
  rows.map Prod.fst

def completionMarginal (rows : List (Bool × Bool)) : List Bool :=
  rows.map Prod.snd

theorem lineage_marginals_do_not_identify_eligible_completion :
    let linked : List (Bool × Bool) := [(true, true), (false, false)]
    let reassigned : List (Bool × Bool) := [(true, false), (false, true)]
    (eligibilityMarginal linked).Perm (eligibilityMarginal reassigned) ∧
      (completionMarginal linked).Perm (completionMarginal reassigned) ∧
      eligibleCompletionCount linked ≠ eligibleCompletionCount reassigned := by
  dsimp [eligibilityMarginal, completionMarginal, eligibleCompletionCount]
  refine ⟨List.Perm.refl _, (List.Perm.swap true false []).symm, ?_⟩
  decide

end FormalVerification.WitnessDeletion
