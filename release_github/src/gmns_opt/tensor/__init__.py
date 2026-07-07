"""High-dimensional transportation tensors: x[o,d,m,p,tau,s,a] and companions D/F/Q/U/C/R/V.

See docs/tensor_framework.md. Provides dataclass schemas + validation + GMNS-table -> tensor conversion +
simple scenario expansion + CSV/JSON export. Does not yet solve tensor problems (that is the roadmap)."""
from .schema import SparseTensor, TensorAxes, validate_tensor, AXES_DECISION
from .demand_tensor import demand_to_tensor, read_demand_table, export_tensor
from .scenario_tensor import expand_demand_scenarios, capacity_scenario
from .control_tensor import control_tensor

__all__ = ["SparseTensor", "TensorAxes", "validate_tensor", "AXES_DECISION",
           "demand_to_tensor", "read_demand_table", "export_tensor",
           "expand_demand_scenarios", "capacity_scenario", "control_tensor"]
