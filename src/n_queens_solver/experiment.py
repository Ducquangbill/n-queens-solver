"""Experiment runner for N-Queens SAT solver comparison."""

import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from .encoding import ENCODING_MAP, NQueensCNF, solve_nqueens_sat
from .baselines import solve_nqueens_baseline


@dataclass
class ExperimentResult:
    """Single experiment result."""
    n: int
    solver_type: str  # "sat" or "baseline"
    solver: str       # solver name
    encoding: Optional[str]  # encoding for SAT, None for baseline
    sat: bool
    time_sec: float
    variables: int
    clauses: int
    decisions: int
    conflicts: int
    propagations: int
    memory_mb: float
    error: Optional[str] = None


SAT_SOLVERS = ["cadical195", "glucose4", "kissat404", "cryptominisat5"]
BASELINE_SOLVERS = ["cp-sat"]  # Only CP-SAT available
ENCODINGS = ["binary", "commander", "product", "seqcounter"]
N_VALUES = [8, 10, 12, 14, 16, 18, 20, 25, 30]


def run_sat_experiment(n: int, encoding: str, solver: str, time_limit: int = 300) -> ExperimentResult:
    """Run a single SAT experiment."""
    encoding_type = ENCODING_MAP[encoding]
    cnf_obj = NQueensCNF.create(n, encoding_type)

    start = time.perf_counter()
    try:
        sat, model, stats = solve_nqueens_sat(n, encoding, solver, time_limit)
        elapsed = time.perf_counter() - start

        # Extract stats from PySAT
        decisions = stats.get("decisions", 0)
        conflicts = stats.get("conflicts", 0)
        propagations = stats.get("propagations", 0)
        # Memory not directly available from PySAT
        memory_mb = 0.0

        return ExperimentResult(
            n=n,
            solver_type="sat",
            solver=solver,
            encoding=encoding,
            sat=sat,
            time_sec=elapsed,
            variables=cnf_obj.variables,
            clauses=len(cnf_obj.clauses),
            decisions=decisions,
            conflicts=conflicts,
            propagations=propagations,
            memory_mb=memory_mb,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        return ExperimentResult(
            n=n,
            solver_type="sat",
            solver=solver,
            encoding=encoding,
            sat=False,
            time_sec=elapsed,
            variables=0,
            clauses=0,
            decisions=0,
            conflicts=0,
            propagations=0,
            memory_mb=0.0,
            error=str(e),
        )


def run_baseline_experiment(n: int, solver: str, time_limit: int = 300) -> ExperimentResult:
    """Run a single baseline experiment."""
    start = time.perf_counter()
    try:
        result = solve_nqueens_baseline(n, solver, time_limit)
        elapsed = time.perf_counter() - start

        if "error" in result.stats:
            return ExperimentResult(
                n=n,
                solver_type="baseline",
                solver=solver,
                encoding=None,
                sat=False,
                time_sec=elapsed,
                variables=0,
                clauses=0,
                decisions=0,
                conflicts=0,
                propagations=0,
                memory_mb=0.0,
                error=result.stats["error"],
            )

        return ExperimentResult(
            n=n,
            solver_type="baseline",
            solver=solver,
            encoding=None,
            sat=result.sat,
            time_sec=elapsed,
            variables=n * n,
            clauses=0,  # Not applicable
            decisions=result.stats.get("branches", 0),
            conflicts=result.stats.get("conflicts", 0),
            propagations=0,
            memory_mb=0.0,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        return ExperimentResult(
            n=n,
            solver_type="baseline",
            solver=solver,
            encoding=None,
            sat=False,
            time_sec=elapsed,
            variables=0,
            clauses=0,
            decisions=0,
            conflicts=0,
            propagations=0,
            memory_mb=0.0,
            error=str(e),
        )


def run_all_experiments(
    n_values: List[int] = None,
    sat_solvers: List[str] = None,
    baseline_solvers: List[str] = None,
    encodings: List[str] = None,
    time_limit: int = 300,
    max_workers: int = 4,
    output_dir: str = "results",
) -> List[ExperimentResult]:
    """Run all experiments and save results."""
    n_values = n_values or N_VALUES
    sat_solvers = sat_solvers or SAT_SOLVERS
    baseline_solvers = baseline_solvers or BASELINE_SOLVERS
    encodings = encodings or ENCODINGS

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    raw_dir = output_path / "raw"
    raw_dir.mkdir(exist_ok=True)

    results = []

    # Build task list
    tasks = []

    # SAT experiments
    for n in n_values:
        for encoding in encodings:
            for solver in sat_solvers:
                tasks.append(("sat", n, encoding, solver))

    # Baseline experiments
    for n in n_values:
        for solver in baseline_solvers:
            tasks.append(("baseline", n, None, solver))

    print(f"Running {len(tasks)} experiments sequentially...")

    for task_type, n, encoding, solver in tasks:
        if task_type == "sat":
            result = run_sat_experiment(n, encoding, solver, time_limit)
        else:
            result = run_baseline_experiment(n, solver, time_limit)
        results.append(result)
        status = "SAT" if result.sat else "UNSAT"
        if result.error:
            status = f"ERROR: {result.error}"
        enc_str = f" ({encoding})" if encoding else ""
        print(f"  n={n:2d} {solver}{enc_str:12s} {result.time_sec:6.2f}s {status}")

        # Save raw result immediately
        filename = f"n{result.n}_{result.solver_type}_{result.solver}"
        if result.encoding:
            filename += f"_{result.encoding}"
        filename += ".json"
        with open(raw_dir / filename, "w") as f:
            json.dump(asdict(result), f, indent=2)

    # Save summary CSV
    csv_path = output_path / "summary.csv"
    with open(csv_path, "w", newline="") as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].__dataclass_fields__.keys())
            writer.writeheader()
            for r in results:
                writer.writerow(asdict(r))

    print(f"Results saved to {output_path}")
    return results


if __name__ == "__main__":
    run_all_experiments()