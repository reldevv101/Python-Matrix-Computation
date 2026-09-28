"""Command-line entry point for the sequential benchmark."""

from __future__ import annotations

import argparse
import random

from .sequential import matrix_checksum, timed_multiply


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark sequential matrix multiplication."
    )
    parser.add_argument(
        "--size", type=int, default=100,
        help="Ukuran matriks persegi N x N (default: 100).",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Seed untuk data acak yang dapat diulang (default: 42).",
    )
    return parser


def make_matrix(size: int, rng: random.Random) -> list[list[float]]:
    return [[rng.uniform(-10.0, 10.0) for _ in range(size)] for _ in range(size)]


def main() -> None:
    args = build_parser().parse_args()
    if args.size <= 0:
        raise SystemExit("--size harus berupa bilangan bulat positif.")

    rng = random.Random(args.seed)
    matrix_a = make_matrix(args.size, rng)
    matrix_b = make_matrix(args.size, rng)
    result, elapsed_seconds = timed_multiply(matrix_a, matrix_b)

    print("Matrix Computation Benchmark (Sequential)")
    print(f"Ukuran matriks : {args.size} x {args.size}")
    print(f"Seed           : {args.seed}")
    print(f"Waktu komputasi: {elapsed_seconds:.6f} detik")
    print(f"Checksum hasil : {matrix_checksum(result):.6f}")


if __name__ == "__main__":
    main()
