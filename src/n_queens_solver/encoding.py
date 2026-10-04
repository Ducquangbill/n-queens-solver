"""N-Queens SAT encoding module.

Generates CNF clauses for N-Queens problem with configurable AMO/ALO encoding methods.
"""

from dataclasses import dataclass
from typing import List
from pysat.card import CardEnc
from pysat.card import EncType as _EncType
from pysat.formula import CNF, IDPool

# Valid encoding types for cardinality constraints
EncType = _EncType
# Map friendly names to PySAT EncType attributes
# Note: commander encoding not available in this PySAT version; using sortnetwrk (sorting network) as closest alternative
ENCODING_MAP = {
    "binary": EncType.pairwise,
    "commander": EncType.sortnetwrk,  # sorting network - tree-based like commander
    "product": EncType.cardnetwrk,    # cardinality network
    "seqcounter": EncType.seqcounter, # sequential counter
}


@dataclass
class NQueensCNF:
    """CNF representation of N-Queens problem."""
    n: int
    encoding_type: EncType
    clauses: List[List[int]]
    variables: int

    @classmethod
    def create(cls, n: int, encoding_type: EncType) -> "NQueensCNF":
        """Create CNF for N-Queens with given encoding."""
        builder = _NQueensCNFBuilder(n, encoding_type)
        return builder.build()


class _NQueensCNFBuilder:
    """Builds N-Queens CNF incrementally with shared variable pool."""

    def __init__(self, n: int, encoding_type: EncType):
        self.n = n
        self.encoding_type = encoding_type
        self.cnf = CNF()
        self.vpool = IDPool()
        # Reserve original variables (1..n*n)
        for r in range(n):
            for c in range(n):
                self.vpool.id(f"q_{r}_{c}")  # Creates IDs 1..n*n

    def _var(self, row: int, col: int) -> int:
        """Map (row, col) to variable ID (1-indexed)."""
        return row * self.n + col + 1

    def _row_vars(self, row: int) -> List[int]:
        """All variables in a row."""
        return [self._var(row, c) for c in range(self.n)]

    def _col_vars(self, col: int) -> List[int]:
        """All variables in a column."""
        return [self._var(r, col) for r in range(self.n)]

    def _diag_vars(self, diff: int) -> List[int]:
        """Variables on diagonal (row - col = diff)."""
        vars_ = []
        for r in range(self.n):
            c = r - diff
            if 0 <= c < self.n:
                vars_.append(self._var(r, c))
        return vars_

    def _anti_diag_vars(self, sum_: int) -> List[int]:
        """Variables on anti-diagonal (row + col = sum)."""
        vars_ = []
        for r in range(self.n):
            c = sum_ - r
            if 0 <= c < self.n:
                vars_.append(self._var(r, c))
        return vars_

    def _add_exactly_one(self, lits: List[int]) -> None:
        """Add exactly-one constraint (ALO + AMO) using CardEnc."""
        # Use CardEnc.equals which gives exactly-one (ALO + AMO)
        self.cnf.extend(CardEnc.equals(lits=lits, bound=1, encoding=self.encoding_type, vpool=self.vpool))

    def _add_at_most_one(self, lits: List[int]) -> None:
        """Add at-most-one constraint using CardEnc."""
        if len(lits) <= 1:
            return
        self.cnf.extend(CardEnc.atmost(lits=lits, bound=1, encoding=self.encoding_type, vpool=self.vpool))

    def build(self) -> NQueensCNF:
        """Build complete CNF."""
        # Exactly one queen per row
        for r in range(self.n):
            self._add_exactly_one(self._row_vars(r))

        # Exactly one queen per column
        for c in range(self.n):
            self._add_exactly_one(self._col_vars(c))

        # At most one queen per diagonal (↘)
        for diff in range(-self.n + 1, self.n):
            self._add_at_most_one(self._diag_vars(diff))

        # At most one queen per anti-diagonal (↙)
        for sum_ in range(0, 2 * self.n - 1):
            self._add_at_most_one(self._anti_diag_vars(sum_))

        return NQueensCNF(
            n=self.n,
            encoding_type=self.encoding_type,
            clauses=self.cnf.clauses,
            variables=self.vpool.top,
        )


def solve_nqueens_sat(n: int, encoding: str, solver_name: str = "cadical195", time_limit: int = 300):
    """Solve N-Queens via SAT and return (sat, model, stats).

    Args:
        n: Board size
        encoding: Encoding name ("binary", "commander", "product", "seqcounter")
        solver_name: SAT solver name
        time_limit: Time limit in seconds (not enforced by all solvers)
    """
    from pysat.solvers import Solver

    encoding_type = ENCODING_MAP[encoding]
    cnf_obj = NQueensCNF.create(n, encoding_type)

    with Solver(name=solver_name, bootstrap_with=cnf_obj.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        stats = solver.accum_stats()

    return sat, model, stats


def model_to_board(model: List[int], n: int) -> List[List[int]]:
    """Convert SAT model to board representation (1=queen, 0=empty).

    Only considers original variables (1..n*n), ignores auxiliary variables.
    """
    board = [[0] * n for _ in range(n)]
    for var in model:
        if 0 < var <= n * n:  # Only original variables
            var_idx = var - 1
            r = var_idx // n
            c = var_idx % n
            board[r][c] = 1
    return board


def validate_board(board: List[List[int]]) -> bool:
    """Validate N-Queens board satisfies all constraints."""
    n = len(board)

    # Check rows
    for r in range(n):
        if sum(board[r]) != 1:
            return False

    # Check columns
    for c in range(n):
        if sum(board[r][c] for r in range(n)) != 1:
            return False

    # Check diagonals
    for r in range(n):
        for c in range(n):
            if board[r][c] == 1:
                # Check ↘ diagonal
                for dr in range(1, n):
                    nr, nc = r + dr, c + dr
                    if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == 1:
                        return False
                # Check ↙ diagonal
                for dr in range(1, n):
                    nr, nc = r + dr, c - dr
                    if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == 1:
                        return False
    return True