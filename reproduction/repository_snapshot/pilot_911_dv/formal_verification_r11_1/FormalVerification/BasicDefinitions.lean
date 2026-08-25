import Mathlib

/-!
Typed measurement universes implement the denominator firewall. A quantity
from the public-record universe cannot be used as an operational-queue
quantity unless an explicit `UniverseMap` is supplied.
-/

namespace FormalVerification

inductive MeasurementUniverse where
  | publicRecord
  | operationalQueue
  deriving DecidableEq, Repr

structure Quantity (u : MeasurementUniverse) where
  value : ℝ

abbrev PublicQuantity := Quantity .publicRecord
abbrev OperationalQuantity := Quantity .operationalQueue

structure UniverseMap (source target : MeasurementUniverse) where
  toFun : Quantity source → Quantity target

namespace UnitInterval

def Holds (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

theorem nonneg {x : ℝ} (hx : Holds x) : 0 ≤ x := hx.1

theorem le_one {x : ℝ} (hx : Holds x) : x ≤ 1 := hx.2

end UnitInterval

end FormalVerification
