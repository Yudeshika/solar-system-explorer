"""
Mainen entry point for the application. 
This file initializes the application, display the menu, and handles user interactions. 
It serves as the central hub that connects the various components of the application, such as the repository, parser, and validators.
"""

from __future__ import annotations

from pathlib import Path
import sys


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "planets.json"


def print_header() -> None:
    print("\nSolar System Explorer")
    print("-" * 22)


def print_menu() -> None:
    print("\nChoose an option:")
    print("1) Ask a question")
    print("2) List planets")
    print("3) Exit")


def read_non_empty_input(prompt: str) -> str:
    """Read input from the user and reject empty/whitespace-only input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter something (input cannot be empty).")


def read_menu_choice() -> str:
    """Read a menu choice and validate it is one of the allowed options."""
    allowed = {"1", "2", "3"}
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in allowed:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def safe_load_system():
    """
    Attempt to load repository and parser.

    This lets main.py run even if you haven't finished the other modules yet.
    When you implement them, this function will start using them automatically.
    """
    try:
        from repository import PlanetRepository
        repo = PlanetRepository(DATA_PATH)
    except Exception as e:
        repo = None
        print("\n[Warning] Could not load planet data yet.")
        print(f"Reason: {e}")

    try:
        from parser import QueryParser
        parser = QueryParser()
    except Exception as e:
        parser = None
        print("\n[Warning] Query parser not available yet.")
        print(f"Reason: {e}")

    return repo, parser


def handle_list_planets(repo) -> None:
    if repo is None:
        print("Planet data is not available yet. Implement repository.py next.")
        return

    planets = repo.list_planets()
    print("\nPlanets in this system:")
    print(", ".join(planets))


def handle_question(repo, parser) -> None:
    question = read_non_empty_input("\nAsk your question: ")

    if repo is None or parser is None:
        print("\nI can't answer questions yet because:")
        if repo is None:
            print("- Planet data/repository is not implemented or failed to load.")
        if parser is None:
            print("- Query parser is not implemented or failed to load.")
        print("\nNext steps: implement repository.py and parser.py.")
        return

    intent = parser.parse(question)

    # Simple “dispatcher” pattern: handle each intent type cleanly.
    if intent.kind == "EVERYTHING":
        planet = repo.get_planet(intent.planet_name)
        if planet is None:
            print(f"'{intent.planet_name}' is not in the list of planets.")
        else:
            print("\n" + planet.summary())

    elif intent.kind == "MASS":
        planet = repo.get_planet(intent.planet_name)
        if planet is None:
            print(f"'{intent.planet_name}' is not in the list of planets.")
        else:
            print(f"{planet.name} has a mass of {planet.mass_kg:.3e} kg.")

    elif intent.kind == "EXISTS":
        exists = repo.has_planet(intent.planet_name)
        if exists:
            print(f"Yes. {intent.planet_name} is in the list of planets.")
        else:
            print(f"No. {intent.planet_name} is not in the list of planets.")

    elif intent.kind == "MOONS":
        planet = repo.get_planet(intent.planet_name)
        if planet is None:
            print(f"'{intent.planet_name}' is not in the list of planets.")
        else:
            print(f"{planet.name} has {planet.moon_count()} moon(s).")

    else:
        print("Sorry, I didn’t understand that question. Try asking about mass, moons, or a planet name.")


def main() -> None:
    print_header()

    # This will warn gracefully until repository/parser is built.
    repo, parser = safe_load_system()

    while True:
        print_menu()
        choice = read_menu_choice()

        if choice == "1":
            handle_question(repo, parser)
        elif choice == "2":
            handle_list_planets(repo)
        elif choice == "3":
            print("\nGoodbye!")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
        