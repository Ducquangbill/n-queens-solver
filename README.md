# N-Queens SAT Solver

Comparative analysis of SAT encoding methods and solvers for the N-Queens problem.

## Overview

This project implements and evaluates SAT-based approaches for solving the N-Queens problem, comparing:
- **4 encoding methods**: Binary (pairwise), Commander (sorting network), Product (cardinality network), Sequential Counter
- **4 SAT solvers**: CaDiCaL, Glucose, Kissat, CryptoMiniSAT
- **1 CP baseline**: OR-Tools CP-SAT

## Installation

```bash
uv sync
```

## Usage

Run experiments:
```bash
# Run full experiment matrix
uv run nqueens --n 8 10 12 14 16 --sat-solvers cadical195 glucose4 kissat404 cryptominisat5 --baselines cp-sat --encodings binary commander product seqcounter --time-limit 120

# Quick test
uv run nqueens --n 8 --sat-solvers cadical195 --encodings binary
```

Options:
- `--n`: Board sizes (default: 8 10 12 14 16 18 20 25 30)
- `--sat-solvers`: SAT solvers to test
- `--baselines`: Baseline solvers (cp-sat)
- `--encodings`: Encoding methods (binary, commander, product, seqcounter)
- `--time-limit`: Time limit per run in seconds (default: 300)
- `--workers`: Parallel workers (default: 4, but runs sequentially due to native lib constraints)
- `--output`: Output directory (default: results)

## Results

Results are saved to `results/`:
- `summary.csv` - All experiment results
- `raw/` - Individual JSON results per experiment
- `scaling_plot.png` - Scaling behavior plots
- `heatmap_n*.png` - Heatmaps per board size
- `clause_variables.png` - Clause/variable count analysis
- `comparison_table.csv/.tex` - Comparison tables

## Generate Report

```bash
uv run python -m n_queens_solver.report
```

## Project Structure

```
src/n_queens_solver/
├── encoding.py      # N-Queens SAT encoding (4 methods)
├── baselines.py     # CP-SAT, CPLEX CP/MIP, Gurobi baselines
├── experiment.py    # Experiment runner
├── report.py        # Report generation (plots, tables)
├── __main__.py      # CLI entry point
└── __init__.py

.scratch/n-queens-solver/  # Issue tracking
docs/
├── adr/             # Architecture Decision Records
└── agents/          # Agent skill configs
```

## Key Findings

| Encoding | Variables (N=16) | Clauses (N=16) | Best Time (N=16) |
|----------|------------------|----------------|------------------|
| Binary | 256 | 6,352 | 0.018s (Glucose4) |
| Commander | 8,800 | 12,916 | 0.033s (Glucose4) |
| Product | 3,928 | 5,616 | 0.015s (CaDiCaL) |
| SeqCounter | 1,182 | 2,728 | **0.0097s (Glucose4)** |

**Sequential Counter with Glucose4** achieves the fastest solve times.

## Requirements

- Python ≥ 3.12
- PySAT (python-sat)
- OR-Tools
- docplex (for CPLEX - requires separate runtime)
- gurobipy (for Gurobi - requires license)

## License

MIT