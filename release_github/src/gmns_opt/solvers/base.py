"""Solver-tier interface. A solver adapter exposes `available()` and `describe()`; models call solvers
directly today (networkx/scipy), and these adapters document the tier ladder and optional back ends."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SolverInfo:
    name: str
    tier: int          # 0 open/default, 1 pyomo+open, 2 commercial, 3 GPU/neural/RL
    classes: list      # formulation classes supported
    available: bool
    note: str = ""


class SolverAdapter:
    name = "base"; tier = 0; classes = []
    def available(self) -> bool: return False
    def describe(self) -> SolverInfo:
        return SolverInfo(self.name, self.tier, self.classes, self.available())
