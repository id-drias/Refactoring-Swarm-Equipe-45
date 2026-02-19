"""Tests for array_utils module."""

import unittest
from array_utils import find_max, sum_array, filter_positive


class TestArrayUtils(unittest.TestCase):

    def test_find_max(self):
        self.assertEqual(find_max([1, 5, 3, 9, 2]), 9)

    def test_find_max_empty(self):
        self.assertIsNone(find_max([]))

    def test_sum_array(self):
        self.assertEqual(sum_array([1, 2, 3, 4]), 10)

    def test_sum_array_empty(self):
        self.assertEqual(sum_array([]), 0)

    def test_filter_positive(self):
        self.assertEqual(filter_positive([-1, 2, -3, 4, 0]), [2, 4])


if __name__ == "__main__":
    unittest.main()
