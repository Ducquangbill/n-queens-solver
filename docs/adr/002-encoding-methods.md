# ADR 002: AMO/ALO Encoding Methods to Evaluate

## Status
Accepted

## Context
N-Queens requires exactly-one constraints per row/column and at-most-one per diagonal. Four encoding methods available in PySAT for cardinality constraints. Need to compare all as required by assignment.

## Decision
Evaluate all four encoding methods for AMO/ALO constraints:

| Method | PySAT `EncType` | Characteristics |
|--------|-----------------|-----------------|
| **Binary** | `EncType.binary` | Pairwise clauses `¬xᵢ ∨ ¬xⱼ` — O(n²) clauses, simple |
| **Commander** | `EncType.commander` | Hierarchical grouping with commander vars — O(n log n) clauses |
| **Product** | `EncType.product` | 2D product construction — O(n√n) clauses |
| **Sequential Counter** | `EncType.seqcounter` | Sinz sequential counter — O(n) clauses, auxiliary vars |

Apply to:
- **ALO (exactly-one)**: rows, columns → `CardEnc.equals(lits, bound=1, encoding=...)`
- **AMO (at-most-one)**: diagonals → `CardEnc.atmost(lits, bound=1, encoding=...)`

## Consequences

### Positive
- Meets assignment requirement to compare encoding methods
- Covers clause-size vs auxiliary-variable trade-off spectrum
- PySAT handles all uniformly

### Negative
- 4 encodings × 4 solvers × multiple N = large experiment matrix
- Sequential counter introduces many auxiliary variables
- Binary encoding blows up clause count for large N

## References
- PySAT `CardEnc` docs
- Sinz, C. (2005). "Towards an Optimal CNF Encoding of Boolean Cardinality Constraints"
- Assignment requirement: "binary, commander, Product, Sequential counter"