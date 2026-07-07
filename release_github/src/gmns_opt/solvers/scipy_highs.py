"""Tier-0 LP/MILP via scipy.optimize.linprog/milp (HiGHS back end). Used by signal_timing, network_design,
facility_location. No license required."""
from __future__ import annotations
from .base import SolverAdapter


class ScipyHiGHS(SolverAdapter):
    name = "scipy_highs"; tier = 0; classes = ["LP", "MILP", "QP"]
    def available(self) -> bool:
        try:
            from scipy.optimize import milp, linprog  # noqa: F401
            return True
        except Exception:
            return False
