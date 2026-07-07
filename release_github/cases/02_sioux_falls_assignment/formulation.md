# Formulation — user-equilibrium traffic assignment (Beckmann)
min_v  Σ_a ∫_0^{v_a} t_a(w) dw   s.t.  Σ_p f_p = d_od (∀ o,d),  v_a = Σ_p δ_{a,p} f_p,  f ≥ 0.
BPR: t_a(v) = t0_a (1 + α (v_a/cap_a)^β), α=0.15, β=4. Convex; solved by Frank-Wolfe (all-or-nothing
direction + exact bisection line search). Relative gap = (TSTT − SPTT)/TSTT. Extensions: system-optimal,
multiclass, elastic demand, congestion pricing, dynamic (DTA).
