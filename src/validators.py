"""
Contains input validation functions for the application. 

These functions ensure that user input is clean, safe, and correctly formatted before it is processed by the application. 
Prevents system crshes or errors out due to invalid or malicious input.
"""

from __future__ import annotations

PUNCTUATION = ["?", "!", ".", ",", ":", ";", "'", "\""]  # Set of punctuation characters to remove

def clean_text(text: str) -> str:
    # Lowercase and remove common punctuation from the input text.
    if text is None:
        return ""
    cleaned = text.strip().lower()
    for ch in PUNCTUATION:
        cleaned = cleaned.replace(ch, "")
    return cleaned

def is_non_empty(text: str) -> bool:
    # True if text is not None and contains at least one non-space character.
    return text is not None and text.strip() != ""

def normalize_planet_name(name: str) -> str:
    # Normalize planet names by stripping whitespace and lowercasing.
    cleaned = clean_text(name)
