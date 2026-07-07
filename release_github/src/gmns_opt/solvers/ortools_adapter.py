"""Tier-0/1 OR-Tools adapter (routing/CP-SAT). Optional dependency. TODO: wire VRP/CP models."""
from __future__ import annotations
from .base import SolverAdapter


class ORToolsAdapter(SolverAdapter):
    name = "ortools"; tier = 1; classes = ["MILP", "CP", "routing"]
    def available(self) -> bool:
        try:
            import ortools  # noqa: F401
            return True
        except Exception:
            return False
