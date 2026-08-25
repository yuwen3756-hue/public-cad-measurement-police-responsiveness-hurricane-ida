import FormalVerification.BasicDefinitions

/-!
Kernel-checked core of the R11.1 measurement-admissibility framework.

The paper's compatibility set is represented by an arbitrary predicate over a
witness bundle, a latent state, and a recording/export state.  No empirical or
institutional semantics are built into these definitions.
-/

namespace FormalVerification.IdentifiedSets

open Set

universe uW uS uR uTheta

def IdentifiedSet
    {Witness : Type uW} {State : Type uS} {Recording : Type uR}
    {Target : Type uTheta}
    (compatible : Witness → State → Recording → Prop)
    (target : State → Target) (witness : Witness) : Set Target :=
  {theta | ∃ state recording,
    compatible witness state recording ∧ target state = theta}

def WitnessStronger
    {Witness : Type uW} {State : Type uS} {Recording : Type uR}
    (compatible : Witness → State → Recording → Prop)
    (strong weak : Witness) : Prop :=
  ∀ state recording, compatible strong state recording →
    compatible weak state recording

theorem witness_contraction
    {Witness : Type uW} {State : Type uS} {Recording : Type uR}
    {Target : Type uTheta}
    (compatible : Witness → State → Recording → Prop)
    (target : State → Target) {strong weak : Witness}
    (hstrong : WitnessStronger compatible strong weak) :
    IdentifiedSet compatible target strong ⊆
      IdentifiedSet compatible target weak := by
  intro theta htheta
  rcases htheta with ⟨state, recording, hcompatible, rfl⟩
  exact ⟨state, recording, hstrong state recording hcompatible, rfl⟩

/-!
For a fixed tolerance, `DiameterAtMost` is the pairwise form of the paper's
condition `diam(I) ≤ delta`.  It avoids adding compactness assumptions that are
irrelevant to the deletion logic.
-/
def DiameterAtMost {Target : Type uTheta}
    (rho : Target → Target → ℝ) (identified : Set Target)
    (delta : ℝ) : Prop :=
  ∀ ⦃left⦄, left ∈ identified → ∀ ⦃right⦄, right ∈ identified →
    rho left right ≤ delta

theorem diameter_at_most_mono
    {Target : Type uTheta} (rho : Target → Target → ℝ)
    {small large : Set Target} {delta : ℝ}
    (hsubset : small ⊆ large)
    (hlarge : DiameterAtMost rho large delta) :
    DiameterAtMost rho small delta := by
  intro left hleft right hright
  exact hlarge (hsubset hleft) (hsubset hright)

def Sufficient
    {WitnessAtom : Type uW} {Target : Type uTheta}
    (defined : Set WitnessAtom → Prop)
    (identified : Set WitnessAtom → Set Target)
    (rho : Target → Target → ℝ) (delta : ℝ)
    (bundle : Set WitnessAtom) : Prop :=
  defined bundle ∧ DiameterAtMost rho (identified bundle) delta

def InclusionMinimal
    {WitnessAtom : Type uW}
    (sufficient : Set WitnessAtom → Prop)
    (bundle : Set WitnessAtom) : Prop :=
  sufficient bundle ∧
    ∀ witness ∈ bundle, ¬ sufficient (bundle \ {witness})

theorem inclusion_minimal_of_deletion_tests
    {WitnessAtom : Type uW}
    (sufficient : Set WitnessAtom → Prop)
    (bundle : Set WitnessAtom)
    (hbundle : sufficient bundle)
    (hdelete : ∀ witness ∈ bundle,
      ¬ sufficient (bundle \ {witness})) :
    InclusionMinimal sufficient bundle :=
  ⟨hbundle, hdelete⟩

def BundleCost
    {WitnessAtom : Type uW} [DecidableEq WitnessAtom]
    (cost : WitnessAtom → ℝ) (bundle : Finset WitnessAtom) : ℝ :=
  ∑ witness ∈ bundle, cost witness

def IsMinimumCost
    {WitnessAtom : Type uW} [DecidableEq WitnessAtom]
    (admissible sufficient : Finset WitnessAtom → Prop)
    (cost : WitnessAtom → ℝ) (bundle : Finset WitnessAtom) : Prop :=
  admissible bundle ∧ sufficient bundle ∧
    ∀ other, admissible other → sufficient other →
      BundleCost cost bundle ≤ BundleCost cost other

end FormalVerification.IdentifiedSets
