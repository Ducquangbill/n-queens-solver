# ADR 001: Use PySAT as Primary SAT Interface

## Status
Accepted

## Context
Need to call multiple SAT solvers (CaDiCaL, Glucose, Kissat, CryptoMiniSAT) and use built-in encodings (AMO/ALO: binary, commander, product, sequential counter). Options:
1. Direct solver calls via CLI/subprocess
2. PySAT library (Python bindings + encoding helpers)
3. python-sat (alternative wrapper)

## Decision
Use **PySAT** (`pip install python-sat`).

## Consequences

### Positive
- Unified API across solvers: `Solver(name='cadical')`, `Solver(name='glucose4')`, etc.
- Built-in encodings: `CardEnc.atmost()`, `CardEnc.equals()`, `CardEnc.atleast()` with `encoding=EncType.*`
- Incremental solving support (`solve(assumptions=...)`)
- Model extraction: `get_model()`
- Pure Python, no subprocess parsing
- Active maintenance, used in SAT competitions

### Negative
- Extra dependency (but lightweight)
- Solver versions tied to PySAT release (may lag latest CaDiCaL/Kissat)
- Less control over solver-specific parameters vs direct CLI

## References
- PySAT docs: https://pysathq.github.io/
- EncType enum: `EncType.binary`, `EncType.commander`, `EncType.product`, `EncType.seqcounter`