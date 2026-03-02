"""
Tests for the validators module.

This file contains unit tests for the validation functions in validators.py.
Verifies correct text cleaning, empty input detection, and planet name normalization.
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from validators import clean_text, is_non_empty, normalize_planet_name


class TestValidators(unittest.TestCase):

    def test_clean_text_basic(self):
        # Test basic cleaning: lowercase and remove punctuation
        self.assertEqual(clean_text("Hello World!"), "hello world")
        self.assertEqual(clean_text("What is Mars?"), "what is mars")
        self.assertEqual(clean_text("Earth's moon"), "earths moon")

    def test_clean_text_edge_cases(self):
        # Test edge cases
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text("   "), "")
        self.assertEqual(clean_text(None), "")

    def test_clean_text_punctuation(self):
        # Test all punctuation removal
        self.assertEqual(clean_text("Hello, World!?"), "hello world")
        self.assertEqual(clean_text("Test: semi-colon; quotes\""), "test semi-colon quotes")

    def test_is_non_empty(self):
        # Test empty detection
        self.assertTrue(is_non_empty("Hello"))
        self.assertTrue(is_non_empty("  text  "))
        self.assertFalse(is_non_empty(""))
        self.assertFalse(is_non_empty("   "))
        self.assertFalse(is_non_empty(None))

    def test_normalize_planet_name(self):
        # Test planet name normalization
        self.assertEqual(normalize_planet_name("Mars"), "mars")
        self.assertEqual(normalize_planet_name("  EARTH  "), "earth")
        self.assertEqual(normalize_planet_name("Jupiter!"), "jupiter")


if __name__ == "__main__":
    unittest.main()
