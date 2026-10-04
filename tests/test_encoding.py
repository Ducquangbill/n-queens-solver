"""Tests for N-Queens SAT encoding."""

import pytest
from n_queens_solver.encoding import (
    NQueensCNF,
    ENCODING_MAP,
    solve_nqueens_sat,
    model_to_board,
    validate_board,
)


ENCODINGS = ["binary", "commander", "product", "seqcounter"]


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_nqueens_cnf_creation(encoding):
    """Test CNF creation for all encoding types."""
    cnf = NQueensCNF.create(8, ENCODING_MAP[encoding])
    assert cnf.n == 8
    assert cnf.variables >= 64  # At least original variables, more for encodings with aux vars
    assert len(cnf.clauses) > 0


@pytest.mark.parametrize("encoding", ENCODINGS)
def test_nqueens_sat_solve(encoding):
    """Test SAT solving for N=8 with all encoding types."""
    sat, model, stats = solve_nqueens_sat(8, encoding, "cadical195")
    assert sat is True
    assert model is not None
    board = model_to_board(model, 8)
    assert validate_board(board)


def test_nqueens_unsat():
    """Test N=2,3 are UNSAT."""
    for n in [2, 3]:
        sat, model, _ = solve_nqueens_sat(n, "binary", "cadical195")
        assert sat is False
        assert model is None


def test_model_to_board():
    """Test model conversion to board."""
    # Mock model with queens at (0,0), (1,2)...
    # var = row * n + col + 1
    # row 0, col 0 -> var 1
    # row 1, col 2 -> var 1*4 + 2 + 1 = 7
    model = [1, -2, -3, -4, -5, -6, 7, -8, -9, -10, -11, -12, -13, -14, -15, -16]
    board = model_to_board(model, 4)
    assert board[0][0] == 1
    assert board[1][2] == 1


def test_validate_board():
    """Test board validation."""
    # Valid 4-queens solution
    valid = [
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
    ]
    assert validate_board(valid)

    # Invalid: two queens in row
    invalid_row = [
        [1, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
    ]
    assert not validate_board(invalid_row)

    # Invalid: two queens in column
    invalid_col = [
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
    ]
    assert not validate_board(invalid_col)

    # Invalid: diagonal conflict
    invalid_diag = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
    assert not validate_board(invalid_diag)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])