# ADR 003: Comparison Baselines — CPLEX, Gurobi, CP-SAT

## Status
Accepted

## Context
Assignment requires comparing SAT solving with "exact methods: ILP, CP" specifically naming "Cplex CP, Cplex MIP, Gurobi, CP-SAT".

## Decision
Include these four baseline solvers in experimental comparison:

| Solver | Type | Access Method |
|--------|------|---------------|
| **CPLEX CP** | Constraint Programming | `docplex.cp` (IBM Decision Optimization) |
| **CPLEX MIP** | Mixed Integer Programming | `docplex.mp` or `cplex` Python API |
| **Gurobi** | MIP (ILP) | `gurobipy` Python API |
| **OR-Tools CP-SAT** | Constraint Programming | `ortools.sat.python.cp_model` |

All formulate N-Queens as exact optimization/feasibility (not SAT encoding).

## Consequences

### Positive
- Meets assignment requirement directly
- Covers both CP and MIP paradigms
- Industry-standard baselines

### Negative
- CPLEX/Gurobi require licenses (academic free, but setup needed)
- Different modeling APIs — more implementation effort
- CP-SAT is CP, not SAT — different paradigm, fair comparison needs care

## References
- Assignment: "so sánh với Cpelx CP, Cplex MIP, Gurobi, CP-SAT"
- IBM docplex: https://ibmdecisionoptimization.github.io/docplex-doc/
- Gurobi Python: https://www.gurobi.com/documentation/
- OR-Tools CP-SAT: https://developers.google.com/optimization/cp/sat