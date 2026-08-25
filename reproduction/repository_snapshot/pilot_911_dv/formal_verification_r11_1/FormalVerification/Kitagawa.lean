import FormalVerification.BasicDefinitions

namespace FormalVerification.Kitagawa

theorem symmetric_identity (mE mR qE qR : ℝ) :
    mE * qE - mR * qR =
      ((qE + qR) / 2) * (mE - mR) +
      ((mE + mR) / 2) * (qE - qR) := by
  ring

theorem finite_symmetric_identity
    {Disposition : Type*} [Fintype Disposition]
    (piE piR qE qR : Disposition → ℝ) :
    (∑ r, piE r * qE r) - (∑ r, piR r * qR r) =
      (∑ r, ((qE r + qR r) / 2) * (piE r - piR r)) +
      (∑ r, ((piE r + piR r) / 2) * (qE r - qR r)) := by
  rw [← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  ring

end FormalVerification.Kitagawa
