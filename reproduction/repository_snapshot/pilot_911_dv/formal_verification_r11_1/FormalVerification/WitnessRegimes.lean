import FormalVerification.BasicDefinitions

/-! Exact finite count for the R11.1 witness-availability phase diagram. -/

namespace FormalVerification.WitnessRegimes

abbrev Availability := Fin 3

def LegalQueuePriorityPair :=
  {pair : Availability × Availability // pair.2.val ≤ pair.1.val}

instance : Fintype LegalQueuePriorityPair :=
  Fintype.subtype
    (Finset.univ.filter fun pair : Availability × Availability =>
      pair.2.val ≤ pair.1.val)
    (by simp)

abbrev WitnessRegime :=
  Availability × Availability × LegalQueuePriorityPair

theorem legal_queue_priority_pair_count :
    Fintype.card LegalQueuePriorityPair = 6 := by
  decide

theorem witness_regime_count : Fintype.card WitnessRegime = 54 := by
  decide

end FormalVerification.WitnessRegimes
