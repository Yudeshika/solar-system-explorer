"""

Handles interpretation of user input.

This module analyses user input, determines the intent behind the input, and extracts relevant information to perform actions or provide responses. 
Converts free text input into structured commands that the application can process.
"""

from dataclasses import dataclass
from validators import clean_text, normalize_planet_name

@dataclass
class Intent:
    # Represents what the user is asking for.
    kind: str
    planet_name: str
class QueryParser:
    def __init__(self):
        # Keep a small set of known planet names for better extraction.
        self.known_planets = {
            "mercury", "venus", "earth", "mars",
            "jupiter", "saturn", "uranus", "neptune",
            "pluto",  # included so "Is Pluto in the list?" works nicely
        }

    def parse(self, question: str) -> Intent:
        if question is None:
            return Intent(kind="UNKNOWN", planet_name="")
        
        cleaned = clean_text(question)
        words = cleaned.split()

        if not words:
            return Intent(kind="UNKNOWN", planet_name="")

        planet_name = self._extract_planet_name(words)

        # Intent detection (order matters: more specific checks first)
        if "everything" in words or ("tell" in words and "about" in words):
            return Intent(kind="EVERYTHING", planet_name=planet_name)

        if "mass" in words or "massive" in words:
            return Intent(kind="MASS", planet_name=planet_name)

        if "moon" in words or "moons" in words:
            # handles "How many moons does Earth have?"
            return Intent(kind="MOONS", planet_name=planet_name)

        if "list" in words and ("planet" in words or "planets" in words):
            # handles "Is Pluto in the list of planets?"
            return Intent(kind="EXISTS", planet_name=planet_name)

        if cleaned.startswith("is ") and planet_name:
            # a fallback for questions like "Is Pluto a planet?"
            return Intent(kind="EXISTS", planet_name=planet_name)

        return Intent(kind="UNKNOWN", planet_name=planet_name)

    def _extract_planet_name(self, words: list[str]) -> str:
        """
        Try to extract a planet name from the words.

        1) If any word matches a known planet, use that.
        2) Otherwise, use the last word as a best guess.
        """
        for w in words:
            if w in self.known_planets:
                # Return with capital first letter so output looks nice
                return w.capitalize()

        # Fallback: last word as guess (e.g., "saturn")
        last = words[-1]
        return last.capitalize()
    