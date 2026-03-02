This document outlines the planned testing strategy for the Solar System Application.

# Test Plan — Solar System Explorer

# 1. Purpose
This test plan describes how the Solar System Explorer application will be tested to ensure it is correct, robust, and user-friendly.
The application allows users to query information about planets in the Solar System using:
- A command-line interface menu (`src/main.py`)
- A GUI (`src/gui.py`)

Tests cover:
- Loading planet data from a JSON file
- Planet model
- Query parsing (understanding user questions)
- Input validation and error handling
- CLI and GUI user flows

# 2. Scope

# 2.1 Within the Scope
- Planet data loading from `data/planets.json`
- Planet lookups (case-insensitive)
- Supported query types:
  - Tell me everything about "planet"
  - How massive is "planet"
  - How many moons does the "planet" have
  - Is "name" (pluto) in the list of planets
- Input validation (empty input, unknown planet names, unknown question formats)
- Display/output formatting (readable responses)
- Unit tests using Python’s "unittest"

# 2.2 Out of Scope
- Web scraping or live data retrieval from Wikipedia
- Relational databases
- Web application deployment
- Advanced natural language processing

# 3. Test Approach

# 3.1 Testing Types
- Unit testing - Verifies individual components (validators, parser, models, repository).
- Integration testing - Verifies components work together (CLI/GUI + repository + parser).
- Manual testing - Confirms user experience and interface behaviour (especially GUI).

# 3.2 Pass/Fail Criteria
A test case passes if the actual result matches the expected result.
A test case fails if
- The result is incorrect
- The program crashes or behaves unexpectedly
- Input is not validated correctly
- The user cannot complete a basic query flow

# 4. Test Environment

# 4.1 Hardware / OS
- macOS (local development machine)

# 4.2 Software
- Python 3.x (Homebrew)
- Tkinter available for GUI tests (`python3 -m tkinter` should open a window)
- Project structure:
  - `src/` for code
  - `data/planets.json` for data
  - `tests/` for unit tests

# 4.3 How to Run
CLI:
```bash
python3 src/main.py
    or
python3 src/gui.py

