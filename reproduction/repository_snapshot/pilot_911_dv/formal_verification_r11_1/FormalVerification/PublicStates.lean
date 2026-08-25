import FormalVerification.BasicDefinitions

namespace FormalVerification.PublicStates

inductive PublicState where
  | j00
  | j01
  | j10
  | j11
  deriving DecidableEq, Repr

def realizedState (dispatch arrival : Bool) : PublicState :=
  match dispatch, arrival with
  | false, false => .j00
  | false, true => .j01
  | true, false => .j10
  | true, true => .j11

def indicator (dispatch arrival : Bool) (state : PublicState) : ℕ :=
  if realizedState dispatch arrival = state then 1 else 0

theorem indicator_sum_one (dispatch arrival : Bool) :
    indicator dispatch arrival .j00 +
      indicator dispatch arrival .j01 +
      indicator dispatch arrival .j10 +
      indicator dispatch arrival .j11 = 1 := by
  cases dispatch <;> cases arrival <;>
    decide

theorem indicators_mutually_exclusive
    (dispatch arrival : Bool) {left right : PublicState} (h : left ≠ right) :
    indicator dispatch arrival left * indicator dispatch arrival right = 0 := by
  by_cases hl : realizedState dispatch arrival = left
  · have hr : realizedState dispatch arrival ≠ right := by
      intro hright
      apply h
      exact hl.symm.trans hright
    rw [indicator, indicator, if_pos hl, if_neg hr]
  · simp [indicator, hl]

theorem realized_state_unique (dispatch arrival : Bool) :
    ∃! state : PublicState, state = realizedState dispatch arrival := by
  refine ⟨realizedState dispatch arrival, rfl, ?_⟩
  intro state hstate
  exact hstate

end FormalVerification.PublicStates
