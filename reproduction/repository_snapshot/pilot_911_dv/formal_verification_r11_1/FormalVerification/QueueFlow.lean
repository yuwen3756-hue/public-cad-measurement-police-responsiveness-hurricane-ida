import FormalVerification.BasicDefinitions

namespace FormalVerification.QueueFlow

def totalExit (currentStock inflow nextStock : ℝ) : ℝ :=
  currentStock + inflow - nextStock

theorem total_exits_identified
    {currentStock inflow nextStock exits : ℝ}
    (hflow : nextStock = currentStock + inflow - exits) :
    exits = totalExit currentStock inflow nextStock := by
  unfold totalExit
  linarith

structure ExitSplit (total : ℝ) where
  assignment : ℝ
  cancellation : ℝ
  alternateResponse : ℝ
  assignment_nonneg : 0 ≤ assignment
  cancellation_nonneg : 0 ≤ cancellation
  alternate_nonneg : 0 ≤ alternateResponse
  sums_to_total : assignment + cancellation + alternateResponse = total

def allAssignment {total : ℝ} (htotal : 0 ≤ total) : ExitSplit total where
  assignment := total
  cancellation := 0
  alternateResponse := 0
  assignment_nonneg := htotal
  cancellation_nonneg := by norm_num
  alternate_nonneg := by norm_num
  sums_to_total := by ring

def allCancellation {total : ℝ} (htotal : 0 ≤ total) : ExitSplit total where
  assignment := 0
  cancellation := total
  alternateResponse := 0
  assignment_nonneg := by norm_num
  cancellation_nonneg := htotal
  alternate_nonneg := by norm_num
  sums_to_total := by ring

theorem positive_total_has_distinct_splits {total : ℝ} (htotal : 0 < total) :
    (allAssignment (le_of_lt htotal)).assignment ≠
      (allCancellation (le_of_lt htotal)).assignment := by
  simp [allAssignment, allCancellation]
  exact ne_of_gt htotal

theorem zero_total_split_unique {split : ExitSplit 0} :
    split.assignment = 0 ∧ split.cancellation = 0 ∧ split.alternateResponse = 0 := by
  constructor
  · nlinarith [split.assignment_nonneg, split.cancellation_nonneg,
      split.alternate_nonneg, split.sums_to_total]
  constructor <;>
    nlinarith [split.assignment_nonneg, split.cancellation_nonneg,
      split.alternate_nonneg, split.sums_to_total]

structure QueuePath where
  currentStock : ℝ
  inflow : ℝ
  assignment : ℝ
  cancellation : ℝ
  alternateResponse : ℝ
  nextStock : ℝ

def QueuePath.Feasible (path : QueuePath) : Prop :=
  0 ≤ path.currentStock ∧
  0 ≤ path.inflow ∧
  0 ≤ path.assignment ∧
  0 ≤ path.cancellation ∧
  0 ≤ path.alternateResponse ∧
  0 ≤ path.nextStock ∧
  path.nextStock = path.currentStock + path.inflow -
    path.assignment - path.cancellation - path.alternateResponse

def zeroStockPath (a : ℝ) : QueuePath where
  currentStock := 0
  inflow := a
  assignment := a
  cancellation := 0
  alternateResponse := 0
  nextStock := 0

def shiftedStockPath (a b : ℝ) : QueuePath where
  currentStock := b
  inflow := a
  assignment := a
  cancellation := 0
  alternateResponse := 0
  nextStock := b

structure BridgeQueueWitness where
  bridgePrevalence : ℝ
  queuePath : QueuePath

theorem bridge_does_not_identify_queue_state
    (u a b : ℝ) (hu : FormalVerification.UnitInterval.Holds u)
    (ha : 0 < a) (hb : 0 < b) :
    ∃ left right : BridgeQueueWitness,
      left.bridgePrevalence = u ∧
      right.bridgePrevalence = u ∧
      FormalVerification.UnitInterval.Holds left.bridgePrevalence ∧
      FormalVerification.UnitInterval.Holds right.bridgePrevalence ∧
      left.queuePath.Feasible ∧
      right.queuePath.Feasible ∧
      left.queuePath.currentStock ≠ right.queuePath.currentStock ∧
      left.queuePath.inflow = right.queuePath.inflow ∧
      left.queuePath.assignment = right.queuePath.assignment ∧
      left.queuePath.cancellation = right.queuePath.cancellation ∧
      left.queuePath.alternateResponse = right.queuePath.alternateResponse := by
  refine ⟨
    { bridgePrevalence := u, queuePath := zeroStockPath a },
    { bridgePrevalence := u, queuePath := shiftedStockPath a b },
    rfl, rfl, hu, hu, ?_, ?_, ?_, rfl, rfl, rfl, rfl⟩
  · simp [QueuePath.Feasible, zeroStockPath, le_of_lt ha]
  · simp [QueuePath.Feasible, shiftedStockPath, le_of_lt ha, le_of_lt hb]
  · simp [zeroStockPath, shiftedStockPath, (ne_of_gt hb).symm]

theorem empty_stock_flow_set
    {QL QU IL IU QnextL QnextU Q I Qnext E : ℝ}
    (hQ : QL ≤ Q ∧ Q ≤ QU)
    (hI : IL ≤ I ∧ I ≤ IU)
    (hQnext : QnextL ≤ Qnext ∧ Qnext ≤ QnextU)
    (hExit : E = Q + I - Qnext)
    (hExitNonneg : 0 ≤ E)
    (hempty : QU + IU < QnextL) :
    False := by
  linarith [hQ.2, hI.2, hQnext.1]

theorem total_exit_outer_bounds
    {QL QU IL IU QnextL QnextU Q I Qnext E : ℝ}
    (hQ : QL ≤ Q ∧ Q ≤ QU)
    (hI : IL ≤ I ∧ I ≤ IU)
    (hQnext : QnextL ≤ Qnext ∧ Qnext ≤ QnextU)
    (hExit : E = Q + I - Qnext)
    (hExitNonneg : 0 ≤ E) :
    max 0 (QL + IL - QnextU) ≤ E ∧
    E ≤ QU + IU - QnextL := by
  constructor
  · rw [max_le_iff]
    constructor
    · exact hExitNonneg
    · linarith [hQ.1, hI.1, hQnext.2]
  · linarith [hQ.2, hI.2, hQnext.1]

end FormalVerification.QueueFlow
