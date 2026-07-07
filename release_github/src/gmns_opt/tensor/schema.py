"""Schemas for the high-dimensional transportation decision tensor and its companions.

Decision tensor:  x[o, d, m, p, tau, s, a]
    o=origin, d=destination, m=mode, p=path/policy, tau=time-stage, s=scenario, a=action/control.

Companion tensors (see docs/tensor_framework.md):
    D[o,d,m,tau,s]   demand      F[link,m,tau,s]  flow      Q[link,tau,s]  queue
    U[action,tau,s]  control     C[link,tau,s]    capacity  R[state,action] reward   V[state] value

The tensors are stored SPARSELY as dict{index_tuple: value} plus a `TensorAxes` describing the axis labels,
so cases stay small and CSV/JSON-exportable. This module intentionally does not solve tensor problems yet — it
provides the data contract used by demand_tensor / scenario_tensor / control_tensor.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

AXES_DECISION = ["o", "d", "m", "p", "tau", "s", "a"]


@dataclass
class TensorAxes:
    """Ordered axis names and, optionally, the label list per axis (for CSV export headers)."""
    names: List[str]
    labels: Dict[str, List] = field(default_factory=dict)

    def validate_index(self, idx: Tuple) -> bool:
        return len(idx) == len(self.names)


@dataclass
class SparseTensor:
    """A sparse tensor: axes + {index_tuple -> value}. Keeps benchmark cases compact."""
    name: str
    axes: TensorAxes
    data: Dict[Tuple, float] = field(default_factory=dict)

    def set(self, index: Tuple, value: float) -> None:
        if not self.axes.validate_index(index):
            raise ValueError(f"{self.name}: index {index} does not match axes {self.axes.names}")
        self.data[tuple(index)] = float(value)

    def get(self, index: Tuple, default: float = 0.0) -> float:
        return self.data.get(tuple(index), default)

    @property
    def nnz(self) -> int:
        return len(self.data)

    def total(self) -> float:
        return float(sum(self.data.values()))

    def to_rows(self) -> List[dict]:
        rows = []
        for idx, v in self.data.items():
            row = {ax: idx[i] for i, ax in enumerate(self.axes.names)}
            row["value"] = v
            rows.append(row)
        return rows


def validate_tensor(t: SparseTensor) -> dict:
    """Return {ok, errors, stats} for a sparse tensor."""
    errors = []
    for idx in t.data:
        if not t.axes.validate_index(idx):
            errors.append(f"bad index {idx}")
    neg = sum(1 for v in t.data.values() if v < 0)
    return {"ok": not errors, "errors": errors[:20],
            "stats": {"name": t.name, "axes": t.axes.names, "nnz": t.nnz,
                      "total": t.total(), "negative_entries": neg}}
