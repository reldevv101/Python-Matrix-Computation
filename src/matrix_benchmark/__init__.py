"""Tools for benchmarking matrix computation."""

from .sequential import multiply, timed_multiply

__all__ = ["multiply", "timed_multiply"]
