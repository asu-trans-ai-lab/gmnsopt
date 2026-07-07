"""gmns4optimization — a GMNS-native transportation optimization testbed.

Turns standardized GMNS networks + demand + operations data into reproducible optimization cases:
    GMNS network + demand -> optimization model -> solver -> (simulation check) -> report.

Public API:
    read_gmns, build_graph, validate_gmns        (io)
    shortest_path, min_cost_flow, traffic_assignment   (models)
    run_case                                     (benchmark case runner)
"""
from .io import read_gmns, build_graph, validate_gmns
from .models import shortest_path, min_cost_flow, traffic_assignment
from .benchmark import run_case

__version__ = "0.2.0"
__all__ = ["read_gmns", "build_graph", "validate_gmns",
           "shortest_path", "min_cost_flow", "traffic_assignment", "run_case"]
