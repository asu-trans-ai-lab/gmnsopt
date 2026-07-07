"""GMNS-native optimization model templates. Each returns a result dict with a common shape:
    {objective, solution (per-link/per-path), objective_trace, constraint_status, meta}.

Implemented (working, dependency-light): shortest_path, min_cost_flow, traffic_assignment (UE Frank-Wolfe).
Planned templates (see docs/BENCHMARK_SPEC.md): system_optimal_assignment, odme_inverse, signal_timing_milp,
network_design_mip, pricing_bilevel, resilience_robust, freight_vrp, ev_charging, transit_frequency.
"""
from .shortest_path import shortest_path
from .min_cost_flow import min_cost_flow
from .traffic_assignment import traffic_assignment

__all__ = ["shortest_path", "min_cost_flow", "traffic_assignment"]
