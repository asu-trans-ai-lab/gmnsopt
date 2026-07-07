"""ML-for-optimization readiness: feature extraction, warm-start interface, learning-to-branch dataset.
ML SUPPORTS solvers and repeated scenarios; it does not replace rigorous optimization. See
docs/ml_for_optimization.md."""
from .features import extract_features
from .warm_start import WarmStarter
from .branching_dataset import BranchRecord, write_branching_dataset

__all__ = ["extract_features", "WarmStarter", "BranchRecord", "write_branching_dataset"]
