"""Main entry point for N-Queens SAT Solver experiments."""

import argparse
import sys
from pathlib import Path

# Add src to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent))

from .experiment import (
    run_all_experiments,
    SAT_SOLVERS,
    BASELINE_SOLVERS,
    ENCODINGS,
    N_VALUES,
)


def main():
    parser = argparse.ArgumentParser(description="N-Queens SAT Solver Experiments")
    parser.add_argument("--n", type=int, nargs="+", default=N_VALUES, help="Board sizes")
    parser.add_argument("--sat-solvers", nargs="+", default=SAT_SOLVERS, help="SAT solvers")
    parser.add_argument("--baselines", nargs="+", default=BASELINE_SOLVERS, help="Baseline solvers")
    parser.add_argument("--encodings", nargs="+", default=ENCODINGS, help="Encoding methods")
    parser.add_argument("--time-limit", type=int, default=300, help="Time limit per run (seconds)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--output", type=str, default="results", help="Output directory")

    args = parser.parse_args()

    print("N-Queens SAT Solver Experiment Runner")
    print(f"N values: {args.n}")
    print(f"SAT solvers: {args.sat_solvers}")
    print(f"Baselines: {args.baselines}")
    print(f"Encodings: {args.encodings}")
    print(f"Time limit: {args.time_limit}s")
    print(f"Workers: {args.workers}")
    print(f"Output: {args.output}")
    print()

    run_all_experiments(
        n_values=args.n,
        sat_solvers=args.sat_solvers,
        baseline_solvers=args.baselines,
        encodings=args.encodings,
        time_limit=args.time_limit,
        max_workers=args.workers,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()