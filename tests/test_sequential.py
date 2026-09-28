import unittest

from matrix_benchmark.sequential import matrix_checksum, multiply, timed_multiply


class SequentialMultiplyTests(unittest.TestCase):
    def test_multiply_known_matrices(self) -> None:
        left = [[1.0, 2.0], [3.0, 4.0]]
        right = [[5.0, 6.0], [7.0, 8.0]]
        self.assertEqual(multiply(left, right), [[19.0, 22.0], [43.0, 50.0]])

    def test_timed_multiply_returns_non_negative_time(self) -> None:
        result, elapsed = timed_multiply([[2.0]], [[4.0]])
        self.assertEqual(result, [[8.0]])
        self.assertGreaterEqual(elapsed, 0.0)

    def test_checksum(self) -> None:
        self.assertEqual(matrix_checksum([[1.5, 2.5], [3.0, -1.0]]), 6.0)

    def test_rejects_incompatible_matrices(self) -> None:
        with self.assertRaises(ValueError):
            multiply([[1.0, 2.0]], [[1.0, 2.0]])


if __name__ == "__main__":
    unittest.main()
