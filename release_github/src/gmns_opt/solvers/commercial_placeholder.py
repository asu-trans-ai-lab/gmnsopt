"""Tier-2 commercial solver placeholder (Gurobi/CPLEX/COPT/Mosek). Optional; never required.
TODO: add Pyomo-backed adapters that pick these up when licensed."""
from __future__ import annotations
from .base import SolverAdapter


class CommercialPlaceholder(SolverAdapter):
    name = "commercial"; tier = 2; classes = ["LP", "MILP", "QP", "NLP"]
    def available(self) -> bool:
        for mod in ("gurobipy", "cplex", "coptpy", "mosek"):
            try:
                __import__(mod); return True
            except Exception:
                continue
        return False
