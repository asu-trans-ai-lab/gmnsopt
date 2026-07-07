# Formulation — min-cost flow
min  Σ_a c_a x_a   s.t.  node conservation with supply b_i (Σ b = 0),  0 ≤ x_a ≤ u_a (capacity).
LP; solved with networkx min-cost-flow. This is the building block for multicommodity flow, assignment, and
network design. Extensions: multiple commodities, side constraints, integer design variables.
