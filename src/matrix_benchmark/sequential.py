"""Pure-Python sequential matrix multiplication and timing helpers."""

from __future__ import annotations

from time import perf_counter

Matrix = list[list[float]]


def _validate_matrices(left: Matrix, right: Matrix) -> None:
    if not left or not right:
        raise ValueError("Matriks tidak boleh kosong.")

    left_width = len(left[0])
    right_width = len(right[0])
    if any(len(row) != left_width for row in left):
        raise ValueError("Matriks kiri harus berbentuk persegi panjang.")
    if any(len(row) != right_width for row in right):
        raise ValueError("Matriks kanan harus berbentuk persegi panjang.")
    if left_width != len(right):
        raise ValueError("Jumlah kolom matriks kiri harus sama dengan jumlah baris matriks kanan.")


def multiply(left: Matrix, right: Matrix) -> Matrix:
    """Return `left x right` using one sequential process."""
    _validate_matrices(left, right)
    right_columns = list(zip(*right))
    return [
        [sum(a * b for a, b in zip(left_row, right_column)) for right_column in right_columns]
        for left_row in left
    ]


def timed_multiply(left: Matrix, right: Matrix) -> tuple[Matrix, float]:
    """Multiply two matrices and return the result with elapsed seconds."""
    started_at = perf_counter()
    result = multiply(left, right)
    return result, perf_counter() - started_at


def matrix_checksum(matrix: Matrix) -> float:
    """Return a simple deterministic value for comparing computed results."""
    return sum(sum(row) for row in matrix)
