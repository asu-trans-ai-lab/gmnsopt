"""Learning-to-branch dataset scaffold (see docs/ml_for_optimization.md).

Collects (state, candidate, label) records from MILP solves for imitation of strong branching. This scaffold
defines the record schema and a writer; wiring it to scipy.milp / commercial callbacks is a TODO."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List
import csv


@dataclass
class BranchRecord:
    instance_id: str
    node_id: int
    variable_index: int
    fractionality: float
    pseudo_cost: float
    strong_branch_score: float      # imitation label
    chosen: int                     # 1 if selected by expert


def write_branching_dataset(records: List[BranchRecord], path: str) -> str:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(BranchRecord.__annotations__))
        w.writeheader()
        for r in records:
            w.writerow(asdict(r))
    return path
# TODO: collect records from MILP callbacks; train imitation model; evaluate with train/val/test CITY split.
