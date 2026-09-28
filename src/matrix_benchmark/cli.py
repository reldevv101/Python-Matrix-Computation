"""Command-line entry point for the sequential benchmark."""

from __future__ import annotations

import argparse
import os
import random

from .parallel import timed_parallel_multiply
from .sequential import matrix_checksum, timed_multiply


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark perkalian matriks sequential dan parallel."
    )
    parser.add_argument(
        "--size", type=int, default=100,
        help="Ukuran matriks persegi N x N (default: 100).",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Seed untuk data acak yang dapat diulang (default: 42).",
    )
    parser.add_argument(
        "--mode", choices=("sequential", "parallel", "both"), default="sequential",
        help="Metode yang diuji (default: sequential).",
    )
    parser.add_argument(
        "--workers", type=int, default=os.cpu_count() or 1,
        help="Jumlah proses untuk mode parallel (default: jumlah CPU).",
    )
    return parser


def make_matrix(size: int, rng: random.Random) -> list[list[float]]:
    return [[rng.uniform(-10.0, 10.0) for _ in range(size)] for _ in range(size)]


def main() -> None:
    args = build_parser().parse_args()
    if args.size <= 0:
        raise SystemExit("--size harus berupa bilangan bulat positif.")
    if args.workers <= 0:
        raise SystemExit("--workers harus berupa bilangan bulat positif.")

    rng = random.Random(args.seed)
    matrix_a = make_matrix(args.size, rng)
    matrix_b = make_matrix(args.size, rng)
    print("Matrix Computation Benchmark")
    print(f"Ukuran matriks : {args.size} x {args.size}")
    print(f"Seed           : {args.seed}")

    sequential_result: list[list[float]] | None = None
    sequential_elapsed: float | None = None
    if args.mode in ("sequential", "both"):
        sequential_result, sequential_elapsed = timed_multiply(matrix_a, matrix_b)
        print(f"Sequential     : {sequential_elapsed:.6f} detik")
        print(f"Checksum       : {matrix_checksum(sequential_result):.6f}")

    if args.mode in ("parallel", "both"):
        parallel_result, parallel_elapsed = timed_parallel_multiply(
            matrix_a, matrix_b, args.workers
        )
        print(f"Parallel ({args.workers} proses): {parallel_elapsed:.6f} detik")
        print(f"Checksum       : {matrix_checksum(parallel_result):.6f}")
        if sequential_result is not None and sequential_elapsed is not None:
            if parallel_result != sequential_result:
                raise RuntimeError("Hasil parallel tidak sama dengan hasil sequential.")
            print(f"Speedup        : {sequential_elapsed / parallel_elapsed:.2f}x")


if __name__ == "__main__":
    main()
