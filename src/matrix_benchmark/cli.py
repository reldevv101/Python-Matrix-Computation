"""Command-line entry point for the sequential benchmark."""

from __future__ import annotations

import argparse
from datetime import datetime
import os
import random
from pathlib import Path

from .parallel import timed_parallel_multiply
from .reporting import append_benchmark_result
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
    parser.add_argument(
        "--save-csv",
        type=Path,
        help="Simpan hasil percobaan sebagai satu baris CSV pada path ini.",
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
    parallel_result: list[list[float]] | None = None
    parallel_elapsed: float | None = None
    speedup: float | None = None
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
            speedup = sequential_elapsed / parallel_elapsed
            print(f"Speedup        : {speedup:.2f}x")

    if args.save_csv is not None:
        result = sequential_result if sequential_result is not None else parallel_result
        checksum = matrix_checksum(result) if result is not None else ""
        append_benchmark_result(
            args.save_csv,
            {
                "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
                "size": args.size,
                "seed": args.seed,
                "mode": args.mode,
                "workers": args.workers if args.mode != "sequential" else 1,
                "sequential_seconds": (
                    f"{sequential_elapsed:.6f}" if sequential_elapsed is not None else ""
                ),
                "parallel_seconds": (
                    f"{parallel_elapsed:.6f}" if parallel_elapsed is not None else ""
                ),
                "speedup": f"{speedup:.6f}" if speedup is not None else "",
                "checksum": f"{checksum:.6f}" if isinstance(checksum, float) else checksum,
                "result_match": (
                    "yes" if args.mode == "both" else "not_checked"
                ),
            },
        )
        print(f"Hasil disimpan : {args.save_csv}")


if __name__ == "__main__":
    main()
