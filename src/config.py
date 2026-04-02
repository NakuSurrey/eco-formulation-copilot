"""
Configuration module for the Eco-Formulation Copilot.

This file is the SINGLE source of truth for all application settings.
It loads secret values (like the Google API key) from a .env file
and provides default values for non-secret settings.

Every other file in the project imports from here instead of
reading environment variables directly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# Step 1: Load the .env file
# ============================================================
# load_dotenv() searches for a file called .env in the project root.
# It reads each line (e.g., GOOGLE_API_KEY=abc123) and loads them
# into the operating system's environment variables, so os.getenv()
# can find them.
# ============================================================
load_dotenv()


# ============================================================
# Step 2: Define all configuration values
# ============================================================

# --- Google Gemini Settings ---
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# --- Application Settings ---
APP_TITLE: str = os.getenv("APP_TITLE", "Eco-Formulation Copilot")
DATA_PATH: str = os.getenv("DATA_PATH", "data/formulations.csv")

# --- Project Root Path ---
# This calculates the absolute path to the project root folder.
# Path(__file__) = the path to THIS config.py file
# .resolve()    = turns it into an absolute path
# .parent       = goes up one folder (from src/ to project root)
# .parent       = goes up again (covers the src/ folder)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# --- Absolute Data Path ---
# Joins the project root with the relative data path.
# This means the app can find formulations.csv no matter
# where you run the app from (project root, src/, etc.)
DATA_FILEPATH: Path = PROJECT_ROOT / DATA_PATH


def validate_config() -> bool:
    """
    Checks that all required configuration values are present.

    Returns True if everything is set correctly.
    Raises a ValueError with a clear message if something is missing.

    This function is called once when the app starts. If the API key
    is missing, the app stops immediately with a helpful error instead
    of crashing later with a cryptic message.
    """
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        raise ValueError(
            "\n"
            "========================================\n"
            "MISSING: GOOGLE_API_KEY\n"
            "========================================\n"
            "1. Copy .env.example to .env\n"
            "2. Get your free key at: https://aistudio.google.com/apikey\n"
            "3. Paste it into .env as: GOOGLE_API_KEY=your_key\n"
            "========================================"
        )
    return True
