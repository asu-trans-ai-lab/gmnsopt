"""Solver tiers (see docs/solver_tiers.md). Core models use Tier-0 (networkx/scipy HiGHS) by default; higher
tiers (Pyomo+open, commercial, GPU/neural/RL) are OPTIONAL and never required."""
from .base import SolverAdapter, SolverInfo
from .scipy_highs import ScipyHiGHS
from .networkx_solver import NetworkXSolver
from .ortools_adapter import ORToolsAdapter
from .commercial_placeholder import CommercialPlaceholder
from .neural_placeholder import NeuralPlaceholder

ADAPTERS = [NetworkXSolver(), ScipyHiGHS(), ORToolsAdapter(), CommercialPlaceholder(), NeuralPlaceholder()]


def solver_status():
    """List each adapter's availability + tier (for `gmns-opt` diagnostics / docs)."""
    return [a.describe().__dict__ for a in ADAPTERS]


__all__ = ["SolverAdapter", "SolverInfo", "ScipyHiGHS", "NetworkXSolver", "ORToolsAdapter",
           "CommercialPlaceholder", "NeuralPlaceholder", "ADAPTERS", "solver_status"]
