"""
models.py

Defines the data models for the application. In this case, it Defines the Planet class and related behaviour.
This filefocuses on data representation and business logic, while the repository.py file focuses on data access and storage.
"""

class Planet:
    # A simple model representing a planet in our solar system.

    def __init__(self, name: str, mass_kg: float, distance_from_sun_km: int, moons: list[str]):
        self.name = name
        self.mass_kg = mass_kg
        self.distance_from_sun_km = distance_from_sun_km
        self.moons = moons

    def moon_count(self) -> int:
        return len(self.moons)

    def summary(self) -> str:
        # Return a user-friendly multi-line summary of the planet.
        lines = [
            f"Name: {self.name}",
            f"Mass (kg): {self.mass_kg:.3e}",
            f"Distance from Sun (km): {self.distance_from_sun_km:,}",
            f"Moons ({self.moon_count()}): {', '.join(self.moons) if self.moons else 'None'}",
        ]
        return "\n".join(lines)
    