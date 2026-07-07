"""GMNS-native optimization model templates. Each returns a result dict with a common shape:
    {objective, solution (per-link/-path/-decision), objective_trace, constraint_status, meta}.

Implemented (working, dependency-light):
  A routing/access : shortest_path, accessibility
  B assignment     : traffic_assignment (UE), system_optimal (+ marginal-cost pricing)
  flow             : min_cost_flow, max_flow (min-cut / evacuation throughput)
  C inverse        : odme (NNLS OD estimation)
  D operations     : signal_timing (green-split LP)
  E design         : network_design (fixed-charge MILP)
  G siting         : facility_location (p-median MILP; EV charging / hub siting)

Planned (see docs/BENCHMARK_SPEC.md): dynamic assignment, pricing bilevel, resilience/robust, freight VRP,
transit frequency, CAV/UAM control.
"""
from .shortest_path import shortest_path
from .accessibility import accessibility
from .min_cost_flow import min_cost_flow
from .max_flow import max_flow
from .traffic_assignment import traffic_assignment
from .system_optimal import system_optimal
from .odme import odme
from .signal_timing import signal_timing
from .network_design import network_design
from .facility_location import facility_location

__all__ = ["shortest_path", "accessibility", "min_cost_flow", "max_flow", "traffic_assignment",
           "system_optimal", "odme", "signal_timing", "network_design", "facility_location"]
