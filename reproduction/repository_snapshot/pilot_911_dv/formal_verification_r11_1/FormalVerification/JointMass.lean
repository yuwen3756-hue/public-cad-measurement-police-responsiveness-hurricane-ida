import FormalVerification.Kitagawa

/-! Joint-mass/conditional-share identities linking the paper's two tables. -/

namespace FormalVerification.JointMass

def h11 (recordedMass conditionalShare : ℝ) : ℝ :=
  recordedMass * conditionalShare

def h01 (recordedMass conditionalShare : ℝ) : ℝ :=
  recordedMass * (1 - conditionalShare)

theorem joint_masses_recover_recorded_mass
    (recordedMass conditionalShare : ℝ) :
    h11 recordedMass conditionalShare +
      h01 recordedMass conditionalShare = recordedMass := by
  simp [h11, h01]
  ring

theorem conditional_share_recovered_from_joint_mass
    {recordedMass conditionalShare : ℝ} (hmass : recordedMass ≠ 0) :
    h11 recordedMass conditionalShare / recordedMass = conditionalShare := by
  simp [h11, hmass]

theorem joint_mass_change_equals_kitagawa_terms
    (mEvent mReference qEvent qReference : ℝ) :
    h11 mEvent qEvent - h11 mReference qReference =
      ((mEvent + mReference) / 2) * (qEvent - qReference) +
      ((qEvent + qReference) / 2) * (mEvent - mReference) := by
  simp only [h11]
  ring

end FormalVerification.JointMass
