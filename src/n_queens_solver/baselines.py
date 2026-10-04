"""Baseline solvers for N-Queens: CP-SAT (OR-Tools), CPLEX CP/MIP, Gurobi."""

import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class SolverResult:
    """Result from a baseline solver."""
    sat: bool
    board: Optional[List[List[int]]]
    time_sec: float
    stats: dict


def solve_nqueens_cp_sat(n: int, time_limit: int = 300) -> SolverResult:
    """Solve N-Queens using OR-Tools CP-SAT."""
    from ortools.sat.python import cp_model

    model = cp_model.CpModel()

    # Variables: x[r][c] = 1 if queen at (r,c)
    x = [[model.NewBoolVar(f"x_{r}_{c}") for c in range(n)] for r in range(n)]

    # Exactly one per row
    for r in range(n):
        model.Add(sum(x[r][c] for c in range(n)) == 1)

    # Exactly one per column
    for c in range(n):
        model.Add(sum(x[r][c] for r in range(n)) == 1)

    # At most one per diagonal (↘)
    for diff in range(-n + 1, n):
        diag_vars = [x[r][r - diff] for r in range(n) if 0 <= r - diff < n]
        if len(diag_vars) > 1:
            model.Add(sum(diag_vars) <= 1)

    # At most one per anti-diagonal (↙)
    for sum_ in range(0, 2 * n - 1):
        diag_vars = [x[r][sum_ - r] for r in range(n) if 0 <= sum_ - r < n]
        if len(diag_vars) > 1:
            model.Add(sum(diag_vars) <= 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8

    start = time.perf_counter()
    status = solver.Solve(model)
    elapsed = time.perf_counter() - start

    sat = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    board = None
    if sat:
        board = [[int(solver.Value(x[r][c])) for c in range(n)] for r in range(n)]

    stats = {
        "wall_time_sec": elapsed,
        "status": solver.StatusName(status),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
        "wall_time": solver.WallTime(),
    }

    return SolverResult(sat=sat, board=board, time_sec=elapsed, stats=stats)


def solve_nqueens_cplex_cp(n: int, time_limit: int = 300) -> SolverResult:
    """Solve N-Queens using CPLEX CP (docplex.cp). Requires CPLEX runtime."""
    try:
        from docplex.cp.model import CpoModel
    except ImportError:
        return SolverResult(False, None, 0, {"error": "docplex.cp not available"})

    model = CpoModel()
    x = [[model.binary_var(name=f"x_{r}_{c}") for c in range(n)] for r in range(n)]

    # Exactly one per row
    for r in range(n):
        model.add(model.sum(x[r][c] for c in range(n)) == 1)

    # Exactly one per column
    for c in range(n):
        model.add(model.sum(x[r][c] for r in range(n)) == 1)

    # At most one per diagonal
    for diff in range(-n + 1, n):
        diag_vars = [x[r][r - diff] for r in range(n) if 0 <= r - diff < n]
        if len(diag_vars) > 1:
            model.add(model.sum(diag_vars) <= 1)

    for sum_ in range(0, 2 * n - 1):
        diag_vars = [x[r][sum_ - r] for r in range(n) if 0 <= sum_ - r < n]
        if len(diag_vars) > 1:
            model.add(model.sum(diag_vars) <= 1)

    start = time.perf_counter()
    try:
        sol = model.solve(TimeLimit=time_limit)
        elapsed = time.perf_counter() - start

        if sol:
            board = [[int(sol[x[r][c]]) for c in range(n)] for r in range(n)]
            return SolverResult(True, board, elapsed, {"status": "solved"})
        else:
            return SolverResult(False, None, elapsed, {"status": "no_solution"})
    except Exception as e:
        return SolverResult(False, None, time.perf_counter() - start, {"error": str(e)})


def solve_nqueens_cplex_mip(n: int, time_limit: int = 300) -> SolverResult:
    """Solve N-Queens using CPLEX MIP (docplex.mp). Requires CPLEX runtime."""
    try:
        from docplex.mp.model import Model
    except ImportError:
        return SolverResult(False, None, 0, {"error": "docplex.mp not available"})

    model = Model(name="nqueens")
    x = [[model.binary_var(name=f"x_{r}_{c}") for c in range(n)] for r in range(n)]

    # Exactly one per row
    for r in range(n):
        model.add_constraint(model.sum(x[r][c] for c in range(n)) == 1)

    # Exactly one per column
    for c in range(n):
        model.add_constraint(model.sum(x[r][c] for r in range(n)) == 1)

    # At most one per diagonal
    for diff in range(-n + 1, n):
        diag_vars = [x[r][r - diff] for r in range(n) if 0 <= r - diff < n]
        if len(diag_vars) > 1:
            model.add_constraint(model.sum(diag_vars) <= 1)

    for sum_ in range(0, 2 * n - 1):
        diag_vars = [x[r][sum_ - r] for r in range(n) if 0 <= sum_ - r < n]
        if len(diag_vars) > 1:
            model.add_constraint(model.sum(diag_vars) <= 1)

    model.parameters.timelimit = time_limit
    model.parameters.threads = 8

    start = time.perf_counter()
    try:
        sol = model.solve()
        elapsed = time.perf_counter() - start

        if sol:
            board = [[int(sol[x[r][c]]) for c in range(n)] for r in range(n)]
            stats = {
                "wall_time_sec": elapsed,
                "nodes": sol.solve_details.nb_nodes_processed if sol.solve_details else 0,
                "gap": sol.solve_details.gap if sol.solve_details else None,
                "status": "optimal" if sol.is_optimal() else "feasible",
            }
            return SolverResult(True, board, elapsed, stats)
        else:
            return SolverResult(False, None, elapsed, {"status": "no_solution"})
    except Exception as e:
        return SolverResult(False, None, time.perf_counter() - start, {"error": str(e)})


def solve_nqueens_gurobi(n: int, time_limit: int = 300) -> SolverResult:
    """Solve N-Queens using Gurobi. Requires Gurobi license."""
    try:
        import gurobipy as gp
    except ImportError:
        return SolverResult(False, None, 0, {"error": "gurobipy not available"})

    model = gp.Model("nqueens")
    model.Params.TimeLimit = time_limit
    model.Params.Threads = 8
    model.Params.OutputFlag = 0

    x = model.addVars(n, n, vtype=gp.GRB.BINARY, name="x")

    # Exactly one per row
    for r in range(n):
        model.addConstr(gp.quicksum(x[r, c] for c in range(n)) == 1)

    # Exactly one per column
    for c in range(n):
        model.addConstr(gp.quicksum(x[r, c] for r in range(n)) == 1)

    # At most one per diagonal
    for diff in range(-n + 1, n):
        diag_vars = [x[r, r - diff] for r in range(n) if 0 <= r - diff < n]
        if len(diag_vars) > 1:
            model.addConstr(gp.quicksum(diag_vars) <= 1)

    for sum_ in range(0, 2 * n - 1):
        diag_vars = [x[r, sum_ - r] for r in range(n) if 0 <= sum_ - r < n]
        if len(diag_vars) > 1:
            model.addConstr(gp.quicksum(diag_vars) <= 1)

    start = time.perf_counter()
    try:
        model.optimize()
        elapsed = time.perf_counter() - start

        if model.Status in (gp.GRB.OPTIMAL, gp.GRB.FEASIBLE):
            board = [[int(x[r, c].X + 0.5) for c in range(n)] for r in range(n)]
            stats = {
                "wall_time_sec": elapsed,
                "nodes": model.NodeCount,
                "gap": model.MIPGap,
                "status": "optimal" if model.Status == gp.GRB.OPTIMAL else "feasible",
            }
            return SolverResult(True, board, elapsed, stats)
        else:
            return SolverResult(False, None, elapsed, {"status": model.Status})
    except Exception as e:
        return SolverResult(False, None, time.perf_counter() - start, {"error": str(e)})


def solve_nqueens_baseline(n: int, solver: str, time_limit: int = 300) -> SolverResult:
    """Dispatch to appropriate baseline solver."""
    dispatch = {
        "cp-sat": solve_nqueens_cp_sat,
        "cplex-cp": solve_nqueens_cplex_cp,
        "cplex-mip": solve_nqueens_cplex_mip,
        "gurobi": solve_nqueens_gurobi,
    }
    if solver not in dispatch:
        raise ValueError(f"Unknown baseline solver: {solver}")
    return dispatch[solver](n, time_limit)