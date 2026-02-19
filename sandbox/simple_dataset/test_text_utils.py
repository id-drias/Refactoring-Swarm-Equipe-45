"""Tests for text_utils module."""

import unittest
from text_utils import reverse_string, count_vowels, capitalize_words


class TestTextUtils(unittest.TestCase):

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_reverse_empty(self):
        self.assertEqual(reverse_string(""), "")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)

    def test_count_vowels_uppercase(self):
        self.assertEqual(count_vowels("HELLO"), 2)

    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")


if __name__ == "__main__":
    unittest.main()
