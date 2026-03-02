"""
Tests for the parser module.

This file contains unit tests for the QueryParser in parser.py.
Verifies correct intent detection and planet name extraction from user questions.
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from parser import QueryParser, Intent


class TestQueryParser(unittest.TestCase):

    def setUp(self):
        self.parser = QueryParser()

    def test_intent_everything(self):
        # Test "everything" intent
        intent = self.parser.parse("Tell me everything about Mars")
        self.assertEqual(intent.kind, "EVERYTHING")
        self.assertEqual(intent.planet_name, "Mars")

        intent = self.parser.parse("everything about Jupiter")
        self.assertEqual(intent.kind, "EVERYTHING")

    def test_intent_mass(self):
        # Test "mass" intent
        intent = self.parser.parse("How massive is Earth?")
        self.assertEqual(intent.kind, "MASS")
        self.assertEqual(intent.planet_name, "Earth")

        intent = self.parser.parse("What is the mass of Venus")
        self.assertEqual(intent.kind, "MASS")
        self.assertEqual(intent.planet_name, "Venus")

    def test_intent_moons(self):
        # Test "moons" intent
        intent = self.parser.parse("How many moons does Jupiter have?")
        self.assertEqual(intent.kind, "MOONS")
        self.assertEqual(intent.planet_name, "Jupiter")

        intent = self.parser.parse("Does Mars have moons")
        self.assertEqual(intent.kind, "MOONS")
        self.assertEqual(intent.planet_name, "Mars")

    def test_intent_exists(self):
        # Test "exists" intent
        intent = self.parser.parse("Is Pluto in the list of planets?")
        self.assertEqual(intent.kind, "EXISTS")
        self.assertEqual(intent.planet_name, "Pluto")

        intent = self.parser.parse("Is Neptune a planet")
        self.assertEqual(intent.kind, "EXISTS")
        self.assertEqual(intent.planet_name, "Neptune")

    def test_intent_unknown(self):
        # Test unknown/unrecognized questions
        intent = self.parser.parse("What color is Mars?")
        self.assertEqual(intent.kind, "UNKNOWN")

        intent = self.parser.parse("")
        self.assertEqual(intent.kind, "UNKNOWN")

    def test_planet_name_extraction(self):
        # Test planet name extraction from known planets
        intent = self.parser.parse("Tell me about Earth")
        self.assertEqual(intent.planet_name, "Earth")

        intent = self.parser.parse("What about Saturn and its rings")
        self.assertEqual(intent.planet_name, "Saturn")

    def test_edge_cases(self):
        # Test edge cases
        intent = self.parser.parse(None)
        self.assertEqual(intent.kind, "UNKNOWN")
        self.assertEqual(intent.planet_name, "")

        intent = self.parser.parse("")
        self.assertEqual(intent.kind, "UNKNOWN")

        intent = self.parser.parse("   ")
        self.assertEqual(intent.kind, "UNKNOWN")

    def test_case_insensitive(self):
        # Parser should handle different cases
        intent = self.parser.parse("TELL ME ABOUT MARS")
        self.assertEqual(intent.kind, "EVERYTHING")
        self.assertEqual(intent.planet_name, "Mars")


if __name__ == "__main__":
    unittest.main()
