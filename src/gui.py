"""
GUI module for the Solar System Explorer application.
This module provides a simple command-line interface for users to interact with the application.

"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from repository import PlanetRepository
from parser import QueryParser

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "planets.json"

class SolarSystemExplorerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Solar System Explorer")
        self.root.geometry("720x450")

        # Load core logic components (repository and parser).
        try:
            self.repo = PlanetRepository(DATA_PATH)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data file:\n{e}")
            self.root.destroy()
            return

        self.parser = QueryParser()

        self._build_ui()

    def _build_ui(self) -> None:
        # Title
        title = tk.Label(self.root, text="Solar System Explorer", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Question entry row
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=12)

        tk.Label(frame, text="Ask a question:").pack(anchor="w")

        self.entry = tk.Entry(frame, font=("Arial", 12))
        self.entry.pack(fill="x", pady=6)
        self.entry.bind("<Return>", lambda _event: self.ask_question())

        # Buttons row
        btns = tk.Frame(self.root)
        btns.pack(fill="x", padx=12, pady=6)

        tk.Button(btns, text="Ask", command=self.ask_question, width=12).pack(side="left")
        tk.Button(btns, text="List planets", command=self.list_planets, width=12).pack(side="left", padx=6)
        tk.Button(btns, text="Clear Output", command=self.clear_output, width=12).pack(side="left")

        # Output text area
        out_frame = tk.Frame(self.root)
        out_frame.pack(fill="both", expand=True, padx=12, pady=10)

        tk.Label(out_frame, text="Output:").pack(anchor="w")

        self.output = tk.Text(out_frame, wrap="word", font=("Consolas", 11), state="disabled")
        self.output.pack(fill="both", expand=True)

    def _write_output(self, text: str) -> None:
        """Append text to the output area."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def clear_output(self) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def list_planets(self) -> None:
        planets = self.repo.list_planets()
        self._write_output("Planets in this system:")
        self._write_output(", ".join(planets))
        self._write_output("")

    def _get_planet_or_show_error(self, planet_name: str):
        # Get a planet from the repository or show an error message if not found.
        planet = self.repo.get_planet(planet_name)
        if planet is None:
            self._write_output(f"'{planet_name}' is not in the list of planets.\n")
        return planet

    def ask_question(self) -> None:
        question = self.entry.get().strip()

        # Input validation
        if not question:
            messagebox.showwarning("Input needed", "Please type a question first.")
            return

        intent = self.parser.parse(question)

        if intent.kind == "EVERYTHING":
            planet = self._get_planet_or_show_error(intent.planet_name)
            if planet:
                self._write_output(planet.summary())
                self._write_output("")

        elif intent.kind == "MASS":
            planet = self._get_planet_or_show_error(intent.planet_name)
            if planet:
                self._write_output(f"{planet.name} has a mass of {planet.mass_kg:.3e} kg.\n")

        elif intent.kind == "MOONS":
            planet = self._get_planet_or_show_error(intent.planet_name)
            if planet:
                self._write_output(f"{planet.name} has {planet.moon_count()} moon(s).\n")

        elif intent.kind == "EXISTS":
            exists = self.repo.has_planet(intent.planet_name)
            if exists:
                self._write_output(f"Yes. {intent.planet_name} is in the list of planets.\n")
            else:
                self._write_output(f"No. {intent.planet_name} is not in the list of planets.\n")

        else:
            self._write_output("Sorry, I didn't understand that question.")
            self._write_output("Try examples like:")
            self._write_output("- Tell me everything about Saturn?")
            self._write_output("- How massive is Neptune?")
            self._write_output("- How many moons does Earth have?")
            self._write_output("- Is Pluto in the list of planets?\n")

        self.entry.delete(0, "end")

def main() -> None:
    root = tk.Tk()
    SolarSystemExplorerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()