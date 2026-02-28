"""
Repository module for managing data access and storage for Planet objects.

This module reads raw planet data from a json file, creates planet objects, and provides methods to retrieve and query planet information.

"""

import json
from pathlib import Path

from models import Planet


class PlanetRepository:
    # Loads planets from the JSON file and provides lookup/query methods.

    def __init__(self, json_path: Path):
        self.json_path = json_path
        self._planets_by_name: dict[str, Planet] = {}
        self._load()

    def _load(self) -> None:
        # Load planet data from JSON and build Planet objects.
        if not self.json_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if not isinstance(raw, list):
            raise ValueError("Invalid data format: expected a list of planets.")

        for item in raw:
            planet = self._planet_from_dict(item)
            key = planet.name.lower()

            # Prevent duplicates
            if key in self._planets_by_name:
                raise ValueError(f"Duplicate planet name found in data: {planet.name}")

            self._planets_by_name[key] = planet

    def _planet_from_dict(self, item: dict) -> Planet:
        # Convert the JSON dictionary into a Planet object (with basic validation).
        required = ["name", "mass_kg", "distance_from_sun_km", "moons"]
        for field in required:
            if field not in item:
                raise ValueError(f"Missing field '{field}' in planet data: {item}")

        name = item["name"]
        mass_kg = item["mass_kg"]
        distance_km = item["distance_from_sun_km"]
        moons = item["moons"]

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Invalid planet name: {name}")

        if not isinstance(mass_kg, (int, float)) or mass_kg <= 0:
            raise ValueError(f"Invalid mass_kg for {name}: {mass_kg}")

        if not isinstance(distance_km, int) or distance_km <= 0:
            raise ValueError(f"Invalid distance_from_sun_km for {name}: {distance_km}")

        if not isinstance(moons, list) or not all(isinstance(m, str) for m in moons):
            raise ValueError(f"Invalid moons list for {name}: {moons}")

        return Planet(name=name.strip(), mass_kg=float(mass_kg), distance_from_sun_km=distance_km, moons=moons)

    def list_planets(self) -> list[str]:
        # Return planet names sorted alphabetically.
        names = [p.name for p in self._planets_by_name.values()]
        return sorted(names)

    def get_planet(self, name: str) -> Planet | None:
        # Return a Planet by name (case-insensitive).
        if not name:
            return None
        return self._planets_by_name.get(name.strip().lower())

    def has_planet(self, name: str) -> bool:
        # True if the planet exists in the repository.
        return self.get_planet(name) is not None
    