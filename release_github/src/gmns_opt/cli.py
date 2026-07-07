"""Command-line entry point:  gmns-opt run <case_dir>   |   gmns-opt validate <case_dir>."""
from __future__ import annotations
import argparse
import os
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gmns-opt", description="GMNS-native transportation optimization testbed")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run a benchmark case folder (problem.yml + input/)")
    r.add_argument("case_dir")
    v = sub.add_parser("validate", help="validate a GMNS case against the data contract")
    v.add_argument("case_dir")
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
        print(f"[{os.path.basename(args.case_dir)}] objective = {res.get('objective')} | "
              f"{res.get('meta', {})}")
        print(f"outputs -> {res.get('output_dir')}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
