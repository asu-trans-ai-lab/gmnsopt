# Tensor framework (the intellectual center)

Do not flatten transportation to `min cᵀx`. Preserve the structured decision tensor

```
x[o, d, m, p, τ, s, a]
```

o=origin, d=destination, m=mode, p=path/policy, τ=time stage, s=scenario, a=action/control.

Companion tensors:

```
D[o,d,m,τ,s]     demand      F[link,m,τ,s]  flow        Q[link,τ,s]  queue
U[action,τ,s]    control     C[link,τ,s]    capacity    R[state,action] reward   V[state] value
```

This connects dynamic programming, stochastic/robust programming, reinforcement learning, tensor
compression / low-rank approximation, learning-to-branch, and simulation-based optimization on ONE data
contract. The `gmns_opt.tensor` module provides sparse schemas (`SparseTensor`, `TensorAxes`), validation,
GMNS-table → demand-tensor conversion (`demand_to_tensor`, `read_demand_table`), scenario expansion
(`expand_demand_scenarios`, `capacity_scenario`), a control-tensor helper, and CSV/JSON export. It stores
tensors sparsely (`{index_tuple: value}`) so benchmark cases stay small.

Example:
```python
from gmns_opt import read_gmns
from gmns_opt.tensor import demand_to_tensor, expand_demand_scenarios, export_tensor
D = demand_to_tensor(read_gmns("cases/02_sioux_falls_assignment"))   # D[o,d,m,τ,s]
Ds = expand_demand_scenarios(D, {"normal": 1.0, "demand_surge": 1.3})
export_tensor(Ds, "demand_tensor.csv")
```
TODO: flow/queue/value tensors wired to dynamic and RL models.
