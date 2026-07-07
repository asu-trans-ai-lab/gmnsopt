# Formulation — shortest path
min  Σ_a c_a x_a   s.t.  Σ_out x - Σ_in x = b_i (b=+1 origin, −1 destination, 0 else), x_a ≥ 0.
c_a = free-flow travel time (min) = length_a / free_speed_a × 60. Solved by Dijkstra (integral unimodular ⇒
LP optimum). Extensions: multi-objective (time/emissions/risk), mode permission, time windows, equity weights.
