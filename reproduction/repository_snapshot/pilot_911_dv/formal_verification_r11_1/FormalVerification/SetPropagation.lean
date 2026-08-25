import FormalVerification.IdentifiedSets

/-! Tagged model unions and identified-set propagation of moment regions. -/

namespace FormalVerification.SetPropagation

def TaggedUnion {Model Theta : Type*}
    (admitted : Set Model) (identified : Model → Set Theta) :
    Set (Model × Theta) :=
  {tagged | tagged.1 ∈ admitted ∧ tagged.2 ∈ identified tagged.1}

theorem tagged_union_membership
    {Model Theta : Type*}
    (admitted : Set Model) (identified : Model → Set Theta)
    (model : Model) (theta : Theta) :
    (model, theta) ∈ TaggedUnion admitted identified ↔
      model ∈ admitted ∧ theta ∈ identified model := by
  rfl

def PropagatedRegion {Moment Theta : Type*}
    (momentRegion : Set Moment) (identified : Moment → Set Theta) :
    Set Theta :=
  {theta | ∃ moment ∈ momentRegion, theta ∈ identified moment}

theorem true_pair_belongs_to_propagated_region
    {Moment Theta : Type*}
    (momentRegion : Set Moment) (identified : Moment → Set Theta)
    {trueMoment : Moment} {trueTheta : Theta}
    (hmoment : trueMoment ∈ momentRegion)
    (htheta : trueTheta ∈ identified trueMoment) :
    trueTheta ∈ PropagatedRegion momentRegion identified :=
  ⟨trueMoment, hmoment, htheta⟩

def NextReachable {State Action : Type*}
    (current : Set State) (actions : Set Action)
    (transition : State → Action → State → Prop) : Set State :=
  {next | ∃ state ∈ current, ∃ action ∈ actions,
    transition state action next}

theorem next_reachable_membership
    {State Action : Type*}
    (current : Set State) (actions : Set Action)
    (transition : State → Action → State → Prop) (next : State) :
    next ∈ NextReachable current actions transition ↔
      ∃ state ∈ current, ∃ action ∈ actions,
        transition state action next := by
  rfl

end FormalVerification.SetPropagation
