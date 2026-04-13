"""
Configuration module for the Eco-Formulation Copilot.

This file is the SINGLE source of truth for all application settings.
It loads secret values (like the Google API key) from EITHER:
  1. Streamlit Cloud Secrets (st.secrets) — used in production
  2. A local .env file — used in local development

Every other file in the project imports from here instead of
reading environment variables directly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# Step 1: Load the .env file (local development only)
# ============================================================
# load_dotenv() searches for a file called .env in the project root.
# It reads each line (e.g., GOOGLE_API_KEY=abc123) and loads them
# into the operating system's environment variables, so os.getenv()
# can find them.
#
# On Streamlit Community Cloud, there is no .env file.
# Instead, secrets are stored in Streamlit's Secrets Manager.
# We try st.secrets FIRST, then fall back to os.getenv().
# ============================================================
load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """
    Tries to read a secret from the .env file first (via os.getenv).
    If not found, falls back to Streamlit Cloud Secrets (st.secrets).

    WHY THIS ORDER MATTERS:
    - Checking os.getenv() FIRST avoids touching st.secrets at module
      load time. Streamlit treats st.secrets access as a "command",
      and if any command runs before st.set_page_config(), Streamlit
      crashes. By checking the environment variable first, st.secrets
      is only touched if the .env value is missing — which only
      happens on Streamlit Cloud where set_page_config timing is
      handled differently.
    - On your local machine / VPS: secrets come from .env → os.getenv
      finds them → st.secrets is never touched → no crash.
    - On Streamlit Cloud: no .env file exists → os.getenv returns ""
      → falls through to st.secrets → works because Streamlit Cloud
      manages the timing internally.
    """
    # Check environment variable first (loaded from .env by dotenv)
    env_value = os.getenv(key, "")
    if env_value:
        return env_value

    # Fall back to Streamlit Cloud Secrets (only reached if .env is missing)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return default


# ============================================================
# Step 2: Define all configuration values
# ============================================================

# --- Google Gemini Settings ---
GOOGLE_API_KEY: str = _get_secret("GOOGLE_API_KEY", "")
GEMINI_MODEL: str = _get_secret("GEMINI_MODEL", "gemini-2.5-flash")

# --- Application Settings ---
APP_TITLE: str = _get_secret("APP_TITLE", "Eco-Formulation Copilot")
DATA_PATH: str = _get_secret("DATA_PATH", "data/formulations.csv")

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
