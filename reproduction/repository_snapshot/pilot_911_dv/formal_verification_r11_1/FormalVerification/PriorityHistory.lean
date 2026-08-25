import FormalVerification.BasicDefinitions

/-! Endpoint disagreement and the unobserved priority-history completion. -/

namespace FormalVerification.PriorityHistory

def ChangedThreeStep {Priority : Type*} [DecidableEq Priority]
    (initial intermediate recorded : Priority) : Prop :=
  initial ≠ intermediate ∨ intermediate ≠ recorded

theorem endpoint_disagreement_implies_change
    {Priority : Type*} [DecidableEq Priority]
    {initial intermediate recorded : Priority}
    (hendpoints : initial ≠ recorded) :
    ChangedThreeStep initial intermediate recorded := by
  by_cases hfirst : initial = intermediate
  · right
    intro hsecond
    exact hendpoints (hfirst.trans hsecond)
  · exact Or.inl hfirst

theorem stable_equal_endpoint_completion :
    ¬ ChangedThreeStep false false false := by
  simp [ChangedThreeStep]

theorem offsetting_equal_endpoint_completion :
    ChangedThreeStep false true false ∧ false = false := by
  simp [ChangedThreeStep]

theorem endpoint_event_subset_history_event
    {Record Priority : Type*} [DecidableEq Priority]
    (initial intermediate recorded : Record → Priority) :
    {row | initial row ≠ recorded row} ⊆
      {row | ChangedThreeStep (initial row) (intermediate row) (recorded row)} := by
  intro row hrow
  exact endpoint_disagreement_implies_change hrow

theorem endpoint_probability_le_history_probability
    {Record Priority : Type*} [MeasurableSpace Record] [DecidableEq Priority]
    (measure : MeasureTheory.Measure Record)
    (initial intermediate recorded : Record → Priority) :
    measure {row | initial row ≠ recorded row} ≤
      measure {row |
        ChangedThreeStep (initial row) (intermediate row) (recorded row)} :=
  MeasureTheory.measure_mono
    (endpoint_event_subset_history_event initial intermediate recorded)

end FormalVerification.PriorityHistory
