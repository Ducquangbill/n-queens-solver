# N-Queens SAT Solver — Domain Context

## Ubiquitous Language

| Term | Definition |
|------|------------|
| **N-Queens** | Place N queens on N×N board, no two attack each other |
| **SAT** | Boolean Satisfiability Problem — find assignment satisfying all clauses |
| **CNF** | Conjunctive Normal Form — AND of ORs (clauses) |
| **Clause** | Disjunction of literals (e.g., `x₁ ∨ ¬x₂ ∨ x₃`) |
| **Literal** | Variable or its negation |
| **Encoding** | Mapping N-Queens constraints → CNF clauses |
| **AMO** | At-Most-One — ≤1 queen per row/col/diag |
| **ALO** | At-Least-One — ≥1 queen per row (exactly-one = AMO + ALO) |
| **Solver** | SAT solver backend (CaDiCaL, Glucose, Kissat, CryptoMiniSAT) |
| **PySAT** | Python library wrapping multiple SAT solvers + encodings |
| **Encoding method** | How AMO/ALO translated to clauses: binary, commander, product, sequential counter |
| **Metrics** | Time (s), memory (MB), clauses, variables, decisions, conflicts |

## Core Entities

### Problem Instance
- `n: int` — board size (4..100+)
- `encoding: EncodingMethod` — AMO/ALO translation strategy
- `solver: SolverBackend` — SAT engine

### EncodingMethod (enum)
- `binary` — pairwise ¬xᵢ ∨ ¬xⱼ
- `commander` — hierarchical grouping with commander variables
- `product` — 2D product encoding
- `sequential_counter` — Sinz sequential counter

### SolverBackend (enum)
- `cadical` — CaDiCaL (CDCL, inprocessing)
- `glucose` — Glucose (parallel, clause sharing)
- `kissat` — Kissat (simplified CaDiCaL)
- `cryptominisat` — CryptoMiniSAT (XOR handling)
- `cp_sat` — OR-Tools CP-SAT (CP, not pure SAT)
- `cplex_mip` — CPLEX MIP (ILP)
- `gurobi` — Gurobi (ILP)

### Result
- `sat: bool` — satisfiable?
- `model: List[int]` — variable assignment (if SAT)
- `time_sec: float`
- `memory_mb: float`
- `clauses: int`
- `variables: int`
- `decisions: int`
- `conflicts: int`

## Key Business Rules

1. **Exactly one queen per row** — ALO + AMO on row variables
2. **Exactly one queen per column** — ALO + AMO on col variables
3. **At most one queen per diagonal** — AMO on each diagonal (↘ and ↙)
4. **Variables** — `x_{r,c}` = queen at row r, col c (1-indexed)
5. **Total variables** = N²
6. **Symmetry breaking** — optional: fix queen in first row to reduce search space

## Metrics to Compare

| Metric | Unit | Purpose |
|--------|------|---------|
| `wall_time` | seconds | Primary performance |
| `cpu_time` | seconds | Solver effort |
| `peak_memory` | MB | Resource usage |
| `clauses` | count | Encoding size |
| `variables` | count | Problem size |
| `decisions` | count | Search effort |
| `conflicts` | count | CDCL activity |
| `propagations` | count | Unit propagation work |

## Bounded Context

**In scope:** N-Queens → SAT encoding → solver → metrics → comparison report
**Out of scope:** General SAT solving, other puzzles (Sudoku separate), solver implementation internals