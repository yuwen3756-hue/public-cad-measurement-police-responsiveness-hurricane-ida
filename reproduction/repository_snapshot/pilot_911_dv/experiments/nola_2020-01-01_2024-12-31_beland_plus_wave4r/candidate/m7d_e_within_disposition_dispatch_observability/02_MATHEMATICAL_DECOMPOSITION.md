# Mathematical decomposition

For disposition $r$, define $m_{r,e}=H01_{r,e}+H11_{r,e}$ and, where $m_{r,e}>0$,

$$
q_{r,e}=\frac{H11_{r,e}}{m_{r,e}}.
$$

This is the public dispatch-field share among arrival-observed records. It is not a dispatch or response probability.

The symmetric Kitagawa identity for $H11$ is

$$
\Delta H11_r=\frac{q_E+q_R}{2}(m_E-m_R)+\frac{m_E+m_R}{2}(q_E-q_R),
$$

with the analogous complementary identity for $H01$. The maximum primary identity residual is $1.67\times10^{-16}$, below the $10^{-12}$ tolerance.

Zero-mass cell shares remain `NOT_DEFINED_IN_CELL`. A zero value is used only as an algebraically inert convention inside the all-category aggregate identity when the corresponding composition share is zero.
