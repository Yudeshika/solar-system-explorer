"""
Tests for the repository module.

This file contains unit tests for the functions and classes in repository.py.
Verifies correct loading of planet data, planet lookup behaviour, and other edge cases.
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from repository import PlanetRepository

# It is best to have temp or mock data for testing, but for simplicity I will use the actual data file here.
class TestRepository(unittest.TestCase):

    def setUp(self):
        data_path = Path(__file__).resolve().parents[1] / "data" / "planets.json"
        self.repo = PlanetRepository(data_path)

    def test_has_planet(self):
        self.assertTrue(self.repo.has_planet("Earth"))
        self.assertTrue(self.repo.has_planet("earth"))
        self.assertFalse(self.repo.has_planet("Pluto"))

    def test_get_planet(self):
        earth = self.repo.get_planet("Earth")
        self.assertIsNotNone(earth)
        self.assertEqual(earth.name, "Earth")

    def test_list_planets(self):
        planets = self.repo.list_planets()
        self.assertIn("Earth", planets)
        self.assertIn("Mars", planets)


if __name__ == "__main__":
    unittest.main()
    