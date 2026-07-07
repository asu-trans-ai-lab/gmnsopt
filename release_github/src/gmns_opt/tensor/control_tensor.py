"""Control tensor U[action, tau, s] schema helper (signals, tolls, speed advisories, dispatch, ...)."""
from __future__ import annotations
from typing import Dict
from .schema import SparseTensor, TensorAxes


def control_tensor(actions: Dict[tuple, float], scenario: str = "normal") -> SparseTensor:
    """Build U[action, tau, s] from {(action_id, tau): value}. TODO: link to solver decision variables."""
    U = SparseTensor(name="control", axes=TensorAxes(names=["action", "tau", "s"]))
    for (action_id, tau), val in actions.items():
        U.set((action_id, tau, scenario), val)
    return U
