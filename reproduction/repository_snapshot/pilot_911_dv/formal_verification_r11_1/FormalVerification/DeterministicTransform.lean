import FormalVerification.BasicDefinitions

/-!
The kernel distinguishes within-regime redundancy of a deterministic transform
from cross-regime equality.  The latter needs equality of the underlying
feasible-world restrictions; determinism alone is insufficient.
-/

namespace FormalVerification.DeterministicTransform

def RawIdentifiedSet {Theta : Type*} (base : Theta → Prop) : Set Theta :=
  {theta | base theta}

def WithDerivedTransform {Theta Raw Derived : Type*}
    (base : Theta → Prop) (raw : Raw) (transform : Raw → Derived)
    (derived : Derived) : Set Theta :=
  {theta | base theta ∧ transform raw = derived}

theorem deterministic_transform_is_redundant
    {Theta Raw Derived : Type*}
    (base : Theta → Prop) (raw : Raw) (transform : Raw → Derived)
    (derived : Derived) (hderived : derived = transform raw) :
    WithDerivedTransform base raw transform derived = RawIdentifiedSet base := by
  ext theta
  simp [WithDerivedTransform, RawIdentifiedSet, hderived]

theorem cross_regime_equality_of_equal_base
    {Theta Raw Derived : Type*}
    (base2021 base2026 : Theta → Prop)
    (raw : Raw) (transform : Raw → Derived) (derived : Derived)
    (hderived : derived = transform raw)
    (hbase : ∀ theta, base2021 theta ↔ base2026 theta) :
    RawIdentifiedSet base2021 =
      WithDerivedTransform base2026 raw transform derived := by
  ext theta
  simp [RawIdentifiedSet, WithDerivedTransform, hderived, hbase]

theorem determinism_alone_does_not_imply_cross_regime_equality :
    let base2021 : Bool → Prop := fun theta => theta = false
    let base2026 : Bool → Prop := fun theta => theta = true
    RawIdentifiedSet base2021 ≠
      WithDerivedTransform base2026 () id () := by
  dsimp
  intro hsets
  have hmembership := congrArg (fun set : Set Bool => false ∈ set) hsets
  simp [RawIdentifiedSet, WithDerivedTransform] at hmembership

end FormalVerification.DeterministicTransform
