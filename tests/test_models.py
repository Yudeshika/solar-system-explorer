import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from models import Planet

class TestPlanetModel(unittest.TestCase):
    def test_moon_count(self):
        earth = Planet(
            name="Earth",
            mass_kg=5.972e24,
            distance_from_sun_km=149597871,
            moons=["Moon"]
        )
        self.assertEqual(earth.moon_count(), 1)

        mercury = Planet(
            name="Mercury",
            mass_kg=3.301e23,
            distance_from_sun_km=57894376,
            moons=[]
        )
        self.assertEqual(mercury.moon_count(), 0)

    def test_summary_contains_key_information(self):
        mars = Planet(
            name="Mars",
            mass_kg=6.417e23,
            distance_from_sun_km=227987155,
            moons=["Phobos", "Deimos"]
        )

        summary = mars.summary()

        # I won't check the whole string exactly.
        # Just check important parts exist.
        self.assertIn("Name: Mars", summary)
        self.assertIn("Mass (kg):", summary)
        self.assertIn("Distance from Sun (km):", summary)
        self.assertIn("Moons (2): Phobos, Deimos", summary)


if __name__ == "__main__":
    unittest.main()