"""Command-line entry point.

  gmns-opt run <case_dir>                     run a benchmark case (problem.yml + input/)
  gmns-opt validate <case_dir>                validate a GMNS case against the data contract
  gmns-opt list-families                      list the problem-family taxonomy
  gmns-opt describe-family <family_id>        describe one problem family
  gmns-opt generate-scenarios --case ...      write a scenario.csv perturbation
  gmns-opt solver-status                      report available solver tiers
"""
from __future__ import annotations
import argparse
import os
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gmns-opt", description="GMNS-native transportation optimization testbed")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="run a benchmark case folder").add_argument("case_dir")
    sub.add_parser("validate", help="validate a GMNS case").add_argument("case_dir")
    sub.add_parser("list-families", help="list the problem-family taxonomy")
    sub.add_parser("describe-family", help="describe one problem family").add_argument("family_id")
    sub.add_parser("solver-status", help="report available solver tiers")
    g = sub.add_parser("generate-scenarios", help="write a scenario.csv perturbation for a case")
    g.add_argument("--case", required=True)
    g.add_argument("--type", default="capacity_drop")
    g.add_argument("--links", default="", help="comma-separated link ids")
    g.add_argument("--drop", type=float, default=0.5)
    g.add_argument("--factor", type=float, default=1.3)
    g.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args(argv)

    if args.cmd == "validate":
        from .io import read_gmns, validate_gmns
        rep = validate_gmns(read_gmns(args.case_dir))
        print("OK" if rep["ok"] else "ERRORS", "|", rep["stats"])
        for e in rep["errors"][:10]:
            print("  error:", e)
        return 0 if rep["ok"] else 1

    if args.cmd == "run":
        from .benchmark import run_case
        res = run_case(args.case_dir)
        print(f"[{os.path.basename(os.path.normpath(args.case_dir))}] objective = {res.get('objective')} | "
              f"{res.get('meta', {})}")
        print(f"outputs -> {res.get('output_dir')}")
        return 0

    if args.cmd == "list-families":
        from .benchmark.registry import list_families
        print(f"{'family_id':38s}{'maturity':10s}{'classes'}")
        for f in list_families():
            print(f"{f.id:38s}{f.maturity:10s}{','.join(f.formulation_classes)}")
        return 0

    if args.cmd == "describe-family":
        from .benchmark.registry import get_family
        f = get_family(args.family_id)
        print(f"# {f.name}  ({f.id})  [maturity: {f.maturity}]")
        print(f"formulation_classes : {', '.join(f.formulation_classes)}")
        print(f"required_files      : {', '.join(f.required_files)}")
        print(f"optional_files      : {', '.join(f.optional_files)}")
        print(f"outputs             : {', '.join(f.outputs)}")
        print(f"default_solver_tier : {f.default_solver_tier}")
        print(f"visualization       : {f.visualization}")
        print(f"runnable_models     : {', '.join(f.runnable_models) or '(none yet)'}")
        print(f"subtypes            : {', '.join(f.subtypes)}")
        return 0

    if args.cmd == "solver-status":
        from .solvers import solver_status
        for s in solver_status():
            print(f"tier {s['tier']}  {s['name']:14s} available={s['available']}  {','.join(s['classes'])}")
        return 0

    if args.cmd == "generate-scenarios":
        from .scenarios import generate_scenarios
        links = [int(x) for x in args.links.split(",") if x.strip()] or None
        path = generate_scenarios(args.case, scenario_type=args.type, links=links, drop=args.drop,
                                  factor=args.factor, seed=args.seed)
        print(f"wrote {path}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
