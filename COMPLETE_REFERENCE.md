# COMPLETE PROJECT REFERENCE — Eco-Formulation Copilot

> This document is a comprehensive reference of the entire build process.
> Every decision, every code file, every error, every discussion — captured in full.
> Use this as study notes, interview preparation, or to rebuild the project from scratch.

---

## TABLE OF CONTENTS

1. [Project Context & Origin](#1-project-context--origin)
2. [The Concept — What This Project Is](#2-the-concept--what-this-project-is)
3. [Tech Stack Assessment — Every Tool and Why](#3-tech-stack-assessment--every-tool-and-why)
4. [LLM Decision — Why Google Gemini](#4-llm-decision--why-google-gemini)
5. [Full Project Blueprint](#5-full-project-blueprint)
6. [Phase 1 — Project Skeleton & Configuration](#6-phase-1--project-skeleton--configuration)
7. [Phase 2 — Data Generation & Loading](#7-phase-2--data-generation--loading)
8. [Phase 3 — The Agentic AI Brain](#8-phase-3--the-agentic-ai-brain)
9. [Phase 4 — Dashboard & Front-End](#9-phase-4--dashboard--front-end)
10. [Error Log — Full Debugging Protocol](#10-error-log--full-debugging-protocol)
11. [Trait Checklist — What Was Included & What Was Skipped](#11-trait-checklist--what-was-included--what-was-skipped)
12. [Package Installation & Testing — How It Works](#12-package-installation--testing--how-it-works)
13. [Git Workflow — Every Push](#13-git-workflow--every-push)
14. [Remaining Phases — What Comes Next](#14-remaining-phases--what-comes-next)

---

## 1. PROJECT CONTEXT & ORIGIN

### The Job

- **Company:** Procter & Gamble (P&G)
- **Role:** Software Development Industrial Placement 2026
- **Location:** Newcastle Innovation Centre, Newcastle upon Tyne, UK
- **Salary:** £26,000/year
- **Duration:** 1st July 2026 to 12th June 2027
- **Application Deadline:** 1pm GMT, 3rd April 2026
- **Job ID:** R000147514

### What the Job Asks For

The job description specifically mentions these technologies:

- **Databricks** — building and maintaining data pipelines
- **Power BI** — interactive dashboards, reports, and analytics
- **Microsoft Copilot Studio & Agentic AI** — AI-driven solutions
- **Data engineering, analytics, and AI development**

### The Newcastle Innovation Centre (NIC)

P&G's NIC is their global centre for Fabric and Home Care research (brands like Ariel, Fairy, Lenor). Their current work involves running high-throughput testing on new sustainable and biodegradable polymers to make detergents more eco-friendly.

### Your Existing Portfolio (Before This Project)

1. **Computer Vision "Safety-First" Inventory Auditor** — YOLOv8-nano, PostgreSQL, FastAPI
2. **UK Legal RAG Pipeline** — Python, FastAPI, Docker, LangChain, Streamlit, DigitalOcean
3. **Explainable Fraud Detection System** — XGBoost, SHAP, FastAPI, Docker, 182 automated tests, GitHub Actions CI/CD

### Why This Project Was Built

To stand out from other applicants by building a proof-of-concept (PoC) that directly demonstrates the exact skills P&G is asking for. Instead of sending a generic CV, this project shows the recruiter a working application that mirrors their tech stack.

---

## 2. THE CONCEPT — WHAT THIS PROJECT IS

### Name: Eco-Formulation Copilot

### One-Sentence Description

An AI assistant that lets a scientist query a chemical formulations database using plain English instead of writing code.

### The Problem It Solves

Scientists at P&G's Newcastle lab run thousands of high-throughput chemical tests. They have massive datasets with columns like biodegradability scores, cleaning efficacy, cost per litre, etc. To get answers from this data, they currently need to know Pandas or SQL. This is a barrier. Our app removes that barrier.

### How It Works — The Flow

```
Scientist types plain English question
        ↓
Streamlit Front-End (app.py) captures the question
        ↓
LangChain DataFrame Agent (agent.py) receives the question
        ↓
Google Gemini LLM reads the question and writes Pandas code
        ↓
The agent executes that Pandas code against the DataFrame
        ↓
The result (number, table, list) is returned as a string
        ↓
Streamlit displays the answer in the chat interface
```

The scientist never sees or touches any code. The LLM does the translation from English → Pandas → Answer.

### How It Maps to the P&G Job Description

| P&G Requirement | Our Implementation |
|---|---|
| Databricks (data pipelines) | Pandas + CSV (lightweight substitute) |
| Power BI (dashboards) | Streamlit + Plotly (interactive charts) |
| Copilot Studio (Agentic AI) | LangChain + Google Gemini |
| Data engineering & analytics | data_loader.py + generate_data.py |
| Testing & troubleshooting | pytest (20 automated tests) |

---

## 3. TECH STACK ASSESSMENT — EVERY TOOL AND WHY

### Python 3.11+

- **What it does:** The programming language everything runs in.
- **Why we need it:** Every tool in our stack (Streamlit, LangChain, FastAPI) is a Python library.
- **Alternative:** JavaScript/Node.js
- **Why we picked this:** Three existing Python projects in portfolio. No time to learn a new ecosystem.

### Streamlit

- **What it does:** Turns a Python script into a live web application with zero HTML/CSS/JS.
- **Why we need it:** The job asks for "interactive dashboards and analytics solutions." Streamlit gives charts + chat UI in one tool.
- **Alternative:** Power BI (what P&G actually uses) or React + Flask.
- **Why we picked this:** Power BI requires a Microsoft license. React would take 20+ hours. Streamlit gives a full dashboard in under 100 lines of Python.

### LangChain + Google Gemini

- **What it does:** LangChain is a framework that connects an LLM to external data sources. The LLM reads the user's question, writes Python/SQL code, executes it against the dataset, and returns the answer.
- **Why we need it:** The job explicitly asks for "AI-driven solutions using Agentic AI frameworks." This IS the Agentic AI.
- **Alternative:** Build a custom agent from scratch using raw API calls.
- **Why we picked this:** LangChain has a pre-built `create_pandas_dataframe_agent` that does exactly what we need.

### Pandas

- **What it does:** A Python library that loads, cleans, filters, and analyzes tabular data (rows and columns).
- **Why we need it:** Acts as our lightweight substitute for Databricks. The LangChain agent writes Pandas code to query the data.
- **Alternative:** SQLite (a file-based database).
- **Why we picked this:** Pandas loads a CSV directly into memory. No database setup. The LangChain DataFrame Agent is built specifically for Pandas.

### Plotly

- **What it does:** Creates interactive, zoomable, hoverable charts inside Streamlit.
- **Why we need it:** The job asks for data visualization (the Power BI requirement). Plotly charts look professional and are interactive.
- **Alternative:** Matplotlib or Streamlit's built-in `st.chart`.
- **Why we picked this:** Plotly charts are interactive (hover, zoom, filter). Matplotlib charts are static images.

### python-dotenv

- **What it does:** Loads secret values (like API keys) from a hidden `.env` file into Python code.
- **Why we need it:** Trait #62 (Secret-managed). We must never commit the Google API key to GitHub.
- **Alternative:** Hardcoding the key in the script.
- **Why we picked this:** Hardcoding secrets is an instant rejection at any enterprise company.

### Docker

- **What it does:** Packages the entire application (code + libraries + settings) into a single portable container that runs identically on any machine.
- **Why we need it:** Trait #71 (Containerised). Proves modern deployment knowledge.
- **Alternative:** Deploy without a container.
- **Why we picked this:** Docker proves the skill. Streamlit Cloud provides the live demo link.

### GitHub Actions (CI/CD)

- **What it does:** Automatically runs checks (linting, tests) every time you push code to GitHub.
- **Why we need it:** Trait #77 (CI/CD-automated). A green checkmark badge on the repo shows enterprise workflow knowledge.
- **Alternative:** No CI/CD.
- **Why we picked this:** Already built in the Fraud Detection project. Copy the YAML and adapt.

---

## 4. LLM DECISION — WHY GOOGLE GEMINI

Three options were evaluated:

### Option A: Google Gemini API (Free Tier) ← CHOSEN

- Free tier: 15 requests per minute, 1,500 requests per day
- No credit card required
- Model used: `gemini-1.5-flash`
- LangChain class: `ChatGoogleGenerativeAI`
- Package: `langchain-google-genai`

### Option B: Groq API (Free Tier)

- Free tier: 30 requests per minute, 14,400 requests per day
- Runs open-source models (Llama 3 70B, Mixtral)
- Very fast response times
- Risk: Groq sometimes changes rate limits

### Option C: OpenAI API (Pay-as-you-go)

- No free tier. Requires credit card.
- GPT-4o-mini costs about $0.01 per 20 queries
- Best quality for code generation
- Rejected because it costs real money

### Decision

Google Gemini was chosen because: completely free, no credit card needed, good enough for writing Pandas code, and LangChain integrates with it in 2 lines of code.

### What Changed When Gemini Was Chosen (The Swap Table)

```
BEFORE (if we had chosen OpenAI)         →  AFTER (Google Gemini — chosen)
─────────────────────────────────            ──────────────────────────────
langchain-openai (package)               →  langchain-google-genai (package)
ChatOpenAI (class in code)               →  ChatGoogleGenerativeAI (class in code)
OPENAI_API_KEY (env variable)            →  GOOGLE_API_KEY (env variable)
GPT-4o-mini (model name)                →  gemini-1.5-flash (model name)
```

Everything else — file structure, phases, architecture — stayed exactly the same. Only the "brain" changed.

### How to Get the API Key

```
Step 1 → Go to https://aistudio.google.com/apikey
Step 2 → Sign in with your Google account
Step 3 → Click "Create API Key"
Step 4 → Copy the key and paste into .env file
```

---

## 5. FULL PROJECT BLUEPRINT

### File/Folder Structure

```
eco-formulation-copilot/
├── .github/
│   └── workflows/
│       └── ci.yml                — GitHub Actions pipeline: runs linting and tests on every push
├── data/
│   ├── generate_data.py          — Script that creates the synthetic chemical formulation CSV
│   └── formulations.csv          — The generated dataset (500 rows, 9 columns)
├── src/
│   ├── __init__.py               — Makes src a Python package
│   ├── config.py                 — Loads environment variables and app settings
│   ├── data_loader.py            — Loads and validates the CSV into a Pandas DataFrame
│   ├── agent.py                  — Creates and configures the LangChain DataFrame Agent
│   └── charts.py                 — Builds the Plotly dashboard charts (scatter, bar, pie)
├── tests/
│   ├── __init__.py               — Makes tests a Python package
│   ├── test_data_loader.py       — Tests CSV loading, schema validation, data ranges
│   └── test_agent.py             — Tests agent initialisation, prompt content, error handling
├── app.py                        — Streamlit front-end: dashboard + chat interface (entry point)
├── Dockerfile                    — Container definition to package the entire app
├── .dockerignore                 — Tells Docker which files to skip
├── requirements.txt              — All Python dependencies with pinned versions
├── .env.example                  — Template showing what environment variables are needed
├── .gitignore                    — Prevents .env, __pycache__, and caches from being committed
├── README.md                     — Executive summary, live demo link, architecture diagram
└── ERRORS.md                     — Running log of every error encountered during the build
```

### Phase Breakdown

```
Phase 1 — Project Skeleton & Configuration
  └── Files: .gitignore, requirements.txt, .env.example, config.py, __init__.py files
  └── What works after: Project exists, dependencies defined, secrets managed

Phase 2 — Data Generation & Loading
  └── Files: generate_data.py, formulations.csv, data_loader.py, test_data_loader.py
  └── What works after: 500-row dataset exists and loads cleanly into a DataFrame

Phase 3 — The Agentic AI Brain
  └── Files: agent.py, test_agent.py
  └── What works after: Natural language → Pandas code → data answer pipeline works

Phase 4 — The Dashboard & Front-End
  └── Files: charts.py, app.py
  └── What works after: Complete Streamlit app with charts + AI chat, runs locally

Phase 5 — Containerisation & CI/CD
  └── Files: Dockerfile, .dockerignore, .github/workflows/ci.yml
  └── What works after: App runs in Docker. GitHub Actions runs on every push

Phase 6 — Deployment & Documentation
  └── Files: README.md (polished), Streamlit Cloud deployment
  └── What works after: Live public URL exists. README maps features to P&G job description
```

### System Architecture

```
[Scientist types a question]
        ↓
[Streamlit Front-End (app.py)]
  — Captures the user's natural language query
  — Displays interactive Plotly charts
        ↓
[LangChain DataFrame Agent (agent.py)]
  — Receives the question as a string
  — The LLM (Google Gemini) reads the question and writes Pandas code
  — The agent executes that Pandas code against the DataFrame
  — Returns the result
        ↓
[Data Layer (data_loader.py → formulations.csv)]
  — CSV loaded into a Pandas DataFrame at app startup
  — Agent queries this DataFrame directly in memory
        ↓
[Streamlit Front-End (app.py)]
  — Receives the agent's answer
  — Displays it in the chat interface below the dashboard
```

---

## 6. PHASE 1 — PROJECT SKELETON & CONFIGURATION

### What Was Built

The project folder structure, all dependency definitions, secret management, and the configuration module.

### Files Created

---

### File: `requirements.txt`

**Purpose:** Lists every Python package the project needs, with pinned versions. Anyone can run `pip install -r requirements.txt` to get the exact same environment.

```txt
# ============================================================
# Eco-Formulation Copilot - Python Dependencies
# ============================================================
# Install with: pip install -r requirements.txt
# ============================================================

# --- Core Framework ---
streamlit==1.41.1                  # Web app framework (dashboard + chat UI)

# --- AI / Agent ---
langchain==0.3.14                  # Agent orchestration framework
langchain-google-genai==2.0.8      # Google Gemini LLM integration for LangChain
langchain-experimental==0.3.4      # Contains create_pandas_dataframe_agent

# --- Data & Visualisation ---
pandas==2.2.3                      # Tabular data manipulation (our mini-Databricks)
plotly==5.24.1                     # Interactive charts (our mini-Power BI)

# --- Configuration ---
python-dotenv==1.0.1               # Loads secrets from .env file

# --- Code Quality (development only) ---
flake8==7.1.1                      # Linter - checks code style automatically
pytest==8.3.4                      # Test runner
```

---

### File: `.env.example`

**Purpose:** Template showing what environment variables are needed. Contains placeholder values, NOT real keys. Safe to commit to GitHub.

```txt
# ============================================================
# Eco-Formulation Copilot - Environment Variables
# ============================================================
# INSTRUCTIONS:
# 1. Copy this file and rename it to .env
# 2. Replace the placeholder values with your real keys
# 3. NEVER commit the .env file to GitHub
# ============================================================

# Google Gemini API Key
# Get yours free at: https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_google_api_key_here

# Gemini Model Name
# gemini-1.5-flash is free tier, fast, and good for code generation
GEMINI_MODEL=gemini-1.5-flash

# Application Settings
APP_TITLE=Eco-Formulation Copilot
DATA_PATH=data/formulations.csv
```

---

### File: `.gitignore`

**Purpose:** Prevents secrets, cache files, and junk from being committed to GitHub.

```txt
# --- Secrets (CRITICAL - never commit these) ---
.env

# --- Python cache files ---
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
dist/
build/

# --- Virtual environment ---
venv/
.venv/
env/

# --- IDE files ---
.vscode/
.idea/
*.swp
*.swo

# --- OS files ---
.DS_Store
Thumbs.db

# --- Docker ---
*.log

# --- Streamlit ---
.streamlit/secrets.toml
```

---

### File: `src/__init__.py`

**Purpose:** Makes the `src` folder a Python package. Without this file, Python cannot import modules from the `src` folder.

```python
# ============================================================
# src package
# ============================================================
# This file makes the 'src' folder a Python package.
# Without it, Python cannot import files from this folder.
# ============================================================
```

---

### File: `tests/__init__.py`

**Purpose:** Makes the `tests` folder a Python package. Without this file, pytest cannot discover test files.

```python
# ============================================================
# tests package
# ============================================================
# This file makes the 'tests' folder a Python package.
# Without it, pytest cannot discover test files in this folder.
# ============================================================
```

---

### File: `src/config.py`

**Purpose:** The SINGLE source of truth for all application settings. Loads the Google API key from `.env`, defines file paths, and provides a `validate_config()` function that stops the app early with a clear error if the key is missing.

```python
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
```

### Phase 1 Key Decisions

1. **Google Gemini 1.5 Flash** — free tier, no credit card, 1,500 requests/day.
2. **python-dotenv** for secret management — `.env` is in `.gitignore` so it never reaches GitHub.
3. **Pinned dependency versions** — ensures reproducibility.
4. **`validate_config()` function** — fails fast with human-readable error if API key is missing.

### Phase 1 Git Push

```bash
git init
git add .
git commit -m "Phase 1: Project skeleton and configuration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/eco-formulation-copilot.git
git push -u origin main
```

---

## 7. PHASE 2 — DATA GENERATION & LOADING

### What Was Built

A script to generate 500 rows of synthetic chemical data, the CSV file itself, a loader module with validation, and 13 tests.

### Files Created

---

### File: `data/generate_data.py`

**Purpose:** Creates a realistic CSV file containing 500 rows of fake chemical formulation data. Each row represents one detergent formula that a P&G scientist might test in the lab.

```python
"""
Synthetic Data Generator for the Eco-Formulation Copilot.

This script creates a realistic CSV file containing 500 rows of
fake chemical formulation data. Each row represents one detergent
formula that a P&G scientist might test in the lab.

WHY SYNTHETIC DATA:
We do not have access to real P&G lab results. Instead, we generate
data that mimics the structure and value ranges of real high-throughput
chemical testing. This lets us build and demo the full AI pipeline
without needing proprietary data.

USAGE:
    python data/generate_data.py

OUTPUT:
    data/formulations.csv (500 rows, 9 columns)
"""

import random
import csv
import os

# ============================================================
# Step 1: Define the realistic value ranges
# ============================================================
# Each constant below defines the possible values or ranges
# for one column in the dataset. These are based on what
# real detergent R&D metrics look like.
# ============================================================

NUM_ROWS: int = 500

SURFACTANT_TYPES: list[str] = [
    "Linear Alkylbenzene Sulfonate",   # Most common in laundry detergent
    "Alcohol Ethoxylate",              # Non-ionic, good for cold water
    "Methyl Ester Sulfonate",          # Bio-based, palm oil derived
    "Alkyl Polyglucoside",             # Plant-derived, highly biodegradable
    "Sodium Lauryl Sulfate",           # Strong cleaning, common in dish soap
    "Cocamidopropyl Betaine",          # Mild, used in sensitive formulas
]

POLYMER_TYPES: list[str] = [
    "Polyethylene Glycol",             # Standard anti-redeposition agent
    "Carboxymethyl Cellulose",         # Bio-based, prevents soil redeposit
    "Polyvinylpyrrolidone",            # Dye transfer inhibitor
    "Polyacrylic Acid",               # Scale inhibitor
    "Modified Starch",                 # Fully biodegradable alternative
    "Chitosan Derivative",             # Marine-sourced, experimental
]

ENZYME_TYPES: list[str] = [
    "Protease",                        # Breaks down protein stains (blood, grass)
    "Amylase",                         # Breaks down starch stains (pasta, rice)
    "Lipase",                          # Breaks down fat/grease stains
    "Cellulase",                       # Fabric care, removes fuzz
    "Mannanase",                       # Breaks down food thickener stains
    "No Enzyme",                        # Some formulas skip enzymes
]

# Score ranges (min, max) — all scores are 0-100
BIODEGRADABILITY_RANGE: tuple[int, int] = (15, 99)
CLEANING_EFFICACY_RANGE: tuple[int, int] = (30, 98)
TOXICITY_RANGE: tuple[float, float] = (0.1, 8.5)

# Cost range in GBP per litre
COST_RANGE: tuple[float, float] = (0.35, 4.80)

# Concentration percentage of active ingredients
CONCENTRATION_RANGE: tuple[float, float] = (5.0, 45.0)


def generate_formulation_id(index: int) -> str:
    """
    Creates a unique formula ID like 'ECO-F-0001'.

    The prefix 'ECO-F' stands for Eco-Formulation.
    The number is zero-padded to 4 digits for consistent sorting.
    """
    return f"ECO-F-{index:04d}"


def generate_single_row(index: int) -> dict:
    """
    Generates one row of synthetic formulation data.

    Returns a dictionary where each key is a column name
    and each value is a randomly generated realistic value.
    """
    biodegradability = random.randint(*BIODEGRADABILITY_RANGE)
    cleaning_efficacy = random.randint(*CLEANING_EFFICACY_RANGE)

    # Formulas with higher biodegradability tend to cost more
    # This adds a realistic correlation to the data
    cost_base = random.uniform(*COST_RANGE)
    if biodegradability > 80:
        cost_base *= random.uniform(1.1, 1.4)

    return {
        "Formula_ID": generate_formulation_id(index),
        "Surfactant_Type": random.choice(SURFACTANT_TYPES),
        "Polymer_Type": random.choice(POLYMER_TYPES),
        "Enzyme_Type": random.choice(ENZYME_TYPES),
        "Concentration_Pct": round(random.uniform(*CONCENTRATION_RANGE), 1),
        "Biodegradability_Score": biodegradability,
        "Cleaning_Efficacy_Score": cleaning_efficacy,
        "Toxicity_Level": round(random.uniform(*TOXICITY_RANGE), 2),
        "Cost_Per_Litre_GBP": round(cost_base, 2),
    }


def generate_dataset() -> list[dict]:
    """
    Generates the full dataset of 500 formulation rows.

    Uses a fixed random seed so the same CSV is produced every time.
    This makes the data reproducible — if you run this script twice,
    you get the exact same dataset.
    """
    random.seed(42)
    return [generate_single_row(i + 1) for i in range(NUM_ROWS)]


def save_to_csv(data: list[dict], filepath: str) -> None:
    """
    Writes the generated data to a CSV file.

    Uses the keys of the first dictionary as column headers.
    """
    if not data:
        raise ValueError("Cannot save empty dataset.")

    fieldnames = list(data[0].keys())

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    """
    Entry point: generates the dataset and saves it to CSV.
    """
    # Calculate the output path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "formulations.csv")

    data = generate_dataset()
    save_to_csv(data, output_path)

    print(f"Generated {len(data)} formulations → {output_path}")
    print(f"Columns: {list(data[0].keys())}")


if __name__ == "__main__":
    main()
```

---

### File: `data/formulations.csv` (first 5 rows sample)

**Purpose:** The generated dataset. 500 rows, 9 columns.

```
Formula_ID,Surfactant_Type,Polymer_Type,Enzyme_Type,Concentration_Pct,Biodegradability_Score,Cleaning_Efficacy_Score,Toxicity_Level,Cost_Per_Litre_GBP
ECO-F-0001,Alcohol Ethoxylate,Carboxymethyl Cellulose,No Enzyme,9.1,96,44,6.32,0.55
ECO-F-0002,Linear Alkylbenzene Sulfonate,Carboxymethyl Cellulose,Amylase,25.2,84,41,0.32,3.30
ECO-F-0003,Sodium Lauryl Sulfate,Polyvinylpyrrolidone,Protease,35.4,40,83,1.44,1.33
ECO-F-0004,Alcohol Ethoxylate,Polyvinylpyrrolidone,Protease,8.7,69,73,0.91,1.59
ECO-F-0005,Cocamidopropyl Betaine,Polyacrylic Acid,Mannanase,10.0,59,63,7.85,3.94
```

### Dataset Statistics

```
                Concentration_Pct  Biodegradability_Score  Cleaning_Efficacy_Score  Toxicity_Level  Cost_Per_Litre_GBP
count              500.00                  500.00                   500.00          500.00              500.00
mean                25.13                   58.60                    62.53            4.34                2.68
std                 11.72                   24.12                    20.17            2.43                1.37
min                  5.00                   15.00                    30.00            0.14                0.36
max                 45.00                   99.00                    98.00            8.50                6.36
```

---

### File: `src/data_loader.py`

**Purpose:** Loads the formulations CSV into a clean, validated Pandas DataFrame. Both the AI agent and the dashboard import from here — Single Source of Truth for the data.

```python
"""
Data Loader for the Eco-Formulation Copilot.

This module is responsible for ONE thing: loading the chemical
formulations CSV file into a clean, validated Pandas DataFrame.

WHY THIS EXISTS AS A SEPARATE FILE:
Both the AI agent (agent.py) and the dashboard (charts.py) need
access to the same DataFrame. Instead of loading the CSV in two
places (which would be duplicated code), both files import from
here. This is the "Single Source of Truth" for the data.

FLOW:
    formulations.csv → load_data() → validated DataFrame → used by agent.py and charts.py
"""

import pandas as pd
from pathlib import Path

from src.config import DATA_FILEPATH

# ============================================================
# Define the expected schema
# ============================================================
EXPECTED_COLUMNS: dict[str, str] = {
    "Formula_ID": "object",
    "Surfactant_Type": "object",
    "Polymer_Type": "object",
    "Enzyme_Type": "object",
    "Concentration_Pct": "float64",
    "Biodegradability_Score": "int64",
    "Cleaning_Efficacy_Score": "int64",
    "Toxicity_Level": "float64",
    "Cost_Per_Litre_GBP": "float64",
}


def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Checks that the loaded DataFrame matches the expected schema.

    Validates three things:
    1. The DataFrame is not empty (has at least one row)
    2. Every expected column exists in the DataFrame
    3. No column contains missing values (NaN)

    Returns True if all checks pass.
    Raises ValueError with a clear message if any check fails.
    """
    if df.empty:
        raise ValueError(
            "Dataset is empty. Run 'python data/generate_data.py' "
            "to create the formulations CSV."
        )

    missing_cols = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing columns in dataset: {missing_cols}. "
            f"Expected columns: {list(EXPECTED_COLUMNS.keys())}"
        )

    null_counts = df[list(EXPECTED_COLUMNS.keys())].isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if not cols_with_nulls.empty:
        raise ValueError(
            f"Columns with missing values: "
            f"{dict(cols_with_nulls)}. "
            f"Clean the data or regenerate with generate_data.py."
        )

    return True


def load_data(filepath: Path = DATA_FILEPATH) -> pd.DataFrame:
    """
    Loads the formulations CSV into a validated Pandas DataFrame.

    Steps:
    1. Checks that the CSV file exists on disk
    2. Reads it into a Pandas DataFrame
    3. Runs validation to confirm the schema is correct
    4. Returns the clean DataFrame
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"Data file not found at: {filepath}\n"
            f"Run 'python data/generate_data.py' to create it."
        )

    df = pd.read_csv(filepath)
    validate_dataframe(df)
    return df
```

---

### File: `tests/test_data_loader.py`

**Purpose:** 13 tests covering: successful load, correct row/column count, all columns present, no NaN values, realistic numeric ranges, and proper error handling for bad inputs.

```python
"""
Tests for the data loader module.

These tests verify that:
1. The CSV file loads successfully into a DataFrame
2. The DataFrame has the correct number of rows and columns
3. All expected columns are present
4. No columns contain missing values (NaN)
5. Numeric columns are within realistic ranges
6. The loader raises clear errors when given bad input
"""

import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import load_data, validate_dataframe, EXPECTED_COLUMNS


class TestLoadData:
    """Tests for the load_data() function."""

    def test_loads_successfully(self) -> None:
        """The CSV loads without any errors."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)

    def test_correct_row_count(self) -> None:
        """The dataset contains exactly 500 rows."""
        df = load_data()
        assert len(df) == 500

    def test_correct_column_count(self) -> None:
        """The dataset contains exactly 9 columns."""
        df = load_data()
        assert len(df.columns) == 9

    def test_all_expected_columns_present(self) -> None:
        """Every column defined in EXPECTED_COLUMNS exists in the DataFrame."""
        df = load_data()
        for col in EXPECTED_COLUMNS:
            assert col in df.columns, f"Missing column: {col}"

    def test_no_missing_values(self) -> None:
        """No column contains NaN (missing) values."""
        df = load_data()
        for col in EXPECTED_COLUMNS:
            assert df[col].isnull().sum() == 0, (
                f"Column '{col}' has {df[col].isnull().sum()} missing values"
            )

    def test_file_not_found_raises_error(self) -> None:
        """Loading a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_data(filepath=Path("data/nonexistent.csv"))


class TestDataRanges:
    """Tests that numeric values are within realistic ranges."""

    def setup_method(self) -> None:
        """Load the DataFrame once before each test in this class."""
        self.df = load_data()

    def test_biodegradability_range(self) -> None:
        assert self.df["Biodegradability_Score"].min() >= 0
        assert self.df["Biodegradability_Score"].max() <= 100

    def test_cleaning_efficacy_range(self) -> None:
        assert self.df["Cleaning_Efficacy_Score"].min() >= 0
        assert self.df["Cleaning_Efficacy_Score"].max() <= 100

    def test_toxicity_range(self) -> None:
        assert self.df["Toxicity_Level"].min() >= 0

    def test_cost_is_positive(self) -> None:
        assert self.df["Cost_Per_Litre_GBP"].min() > 0

    def test_concentration_range(self) -> None:
        assert self.df["Concentration_Pct"].min() >= 0
        assert self.df["Concentration_Pct"].max() <= 100


class TestValidateDataframe:
    """Tests for the validate_dataframe() function."""

    def test_empty_dataframe_raises_error(self) -> None:
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="empty"):
            validate_dataframe(empty_df)

    def test_missing_column_raises_error(self) -> None:
        incomplete_df = pd.DataFrame({
            "Formula_ID": ["ECO-F-0001"],
            "Surfactant_Type": ["Test"],
        })
        with pytest.raises(ValueError, match="Missing columns"):
            validate_dataframe(incomplete_df)
```

### Phase 2 Key Decisions

1. **500 rows** — Large enough to look realistic. Small enough to load instantly.
2. **`random.seed(42)`** — Deterministic. Running the script twice produces the same CSV. Trait #26 (Reproducible).
3. **"No Enzyme" instead of "None"** — Fixed a bug where Pandas converted "None" to NaN. See Error 001.
4. **Separate `data_loader.py`** — Agent and dashboard both need the DataFrame. Loading in one place avoids duplicate code. Trait #29 (DRY).

### Phase 2 Git Push

```bash
git add .
git commit -m "Phase 2: Data generation and loading layer with 13 passing tests"
git push
```

---

## 8. PHASE 3 — THE AGENTIC AI BRAIN

### What Was Built

The LangChain DataFrame Agent powered by Google Gemini. This is the core of the entire project — the "brain" that translates English questions into Pandas code and executes them.

### Files Created

---

### File: `src/agent.py`

**Purpose:** Creates the LangChain DataFrame Agent connected to Google Gemini. Two functions: `create_agent()` builds the connection, `query_agent()` sends questions and returns answers.

```python
"""
Agentic AI module for the Eco-Formulation Copilot.

This file creates the "brain" of the application. It connects
Google Gemini (the LLM) to the chemical formulations DataFrame
using LangChain's DataFrame Agent.

HOW IT WORKS — step by step:
1. The user types a plain English question
2. This module sends that question to the Gemini LLM
3. Gemini reads the question and writes Pandas code to answer it
4. The agent executes that Pandas code against the real DataFrame
5. The result (a number, a table, a list) is returned as a string

FLOW:
    User question (str)
        ↓
    create_agent() — builds the LLM + DataFrame connection
        ↓
    query_agent() — sends the question, gets the answer
        ↓
    Answer (str) — returned to the Streamlit front-end
"""

import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)

from src.config import GOOGLE_API_KEY, GEMINI_MODEL, validate_config

SYSTEM_PROMPT: str = """
You are an AI Research & Development Assistant for the Eco-Formulation
Copilot at a consumer goods company. You help scientists analyze
chemical formulation data for sustainable detergent products.

RULES YOU MUST FOLLOW:
1. You can ONLY answer questions using the provided DataFrame.
2. If the data does not contain the answer, reply exactly with:
   "Data not available in current testing batch."
3. Do NOT invent, estimate, or hallucinate chemical properties.
4. When returning tabular data, format it as a clean markdown table.
5. When asked for "top" or "best" formulas, always state which
   metric you are sorting by.
6. Always include units where applicable (e.g., £ for cost, % for scores).
7. Be concise. Scientists want data, not essays.

THE DATASET COLUMNS:
- Formula_ID: Unique identifier for each formulation (e.g., ECO-F-0001)
- Surfactant_Type: The cleaning agent used (6 types)
- Polymer_Type: The anti-redeposition polymer used (6 types)
- Enzyme_Type: The stain-breaking enzyme used (6 types, or "No Enzyme")
- Concentration_Pct: Active ingredient concentration (5-45%)
- Biodegradability_Score: How eco-friendly the formula is (0-100, higher = better)
- Cleaning_Efficacy_Score: How well it cleans (0-100, higher = better)
- Toxicity_Level: How toxic the formula is (0-10, lower = better)
- Cost_Per_Litre_GBP: Production cost in British Pounds per litre
"""


def create_agent(df: pd.DataFrame) -> object:
    """
    Creates a LangChain DataFrame Agent connected to Google Gemini.
    """
    validate_config()

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type="zero-shot-react-description",
        verbose=False,
        prefix=SYSTEM_PROMPT,
        allow_dangerous_code=True,
    )

    return agent


def query_agent(agent: object, user_question: str) -> str:
    """
    Sends a user's question to the agent and returns the answer.
    Wraps the call in error handling so the app never crashes.
    """
    if not user_question or not user_question.strip():
        return "Please enter a question about the formulation data."

    try:
        result = agent.invoke({"input": user_question})
        return result.get("output", "No output returned from the agent.")

    except ValueError as e:
        return (
            "I couldn't process that query. "
            "Please try rephrasing your chemical parameters. "
            f"(Detail: {str(e)[:200]})"
        )

    except Exception as e:
        error_name = type(e).__name__
        return (
            f"An error occurred while querying the data: {error_name}. "
            "Please check your API key and internet connection, "
            "or try a simpler question."
        )
```

---

### File: `tests/test_agent.py`

**Purpose:** 7 tests covering: system prompt content, empty input handling, error handling. Tests run WITHOUT a real API key (safe for CI/CD).

```python
"""
Tests for the agent module.
"""

import os
import pytest
import pandas as pd

from src.agent import SYSTEM_PROMPT, query_agent

HAS_API_KEY = bool(os.getenv("GOOGLE_API_KEY", ""))
skip_no_key = pytest.mark.skipif(
    not HAS_API_KEY,
    reason="GOOGLE_API_KEY not set — skipping live agent tests"
)


class TestSystemPrompt:
    def test_prompt_contains_role(self) -> None:
        assert "Research & Development Assistant" in SYSTEM_PROMPT

    def test_prompt_contains_anti_hallucination(self) -> None:
        assert "Data not available" in SYSTEM_PROMPT

    def test_prompt_contains_column_descriptions(self) -> None:
        assert "Formula_ID" in SYSTEM_PROMPT
        assert "Biodegradability_Score" in SYSTEM_PROMPT
        assert "Cost_Per_Litre_GBP" in SYSTEM_PROMPT

    def test_prompt_forbids_invention(self) -> None:
        assert "Do NOT invent" in SYSTEM_PROMPT


class TestQueryAgentErrorHandling:
    def test_empty_string_returns_message(self) -> None:
        result = query_agent(agent=None, user_question="")
        assert "Please enter a question" in result

    def test_whitespace_only_returns_message(self) -> None:
        result = query_agent(agent=None, user_question="   ")
        assert "Please enter a question" in result

    def test_none_agent_with_valid_question_returns_error(self) -> None:
        result = query_agent(agent=None, user_question="Show top 5 formulas")
        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result
```

### Phase 3 Key Decisions

1. **String `"zero-shot-react-description"` instead of `AgentType` enum** — the enum import broke in LangChain v1.2.14. See Error 002.
2. **`temperature=0`** — deterministic answers. No creativity for data queries.
3. **Strict system prompt** — Trait #202 (Prompt-engineered) and #203 (Anti-hallucinatory). LLM told to only answer from the dataset.
4. **`allow_dangerous_code=True`** — required by LangChain. Risk mitigated by the strict prompt.
5. **Tests skip live API calls** — CI/CD runs without exposing secrets.

### Phase 3 Git Push

```bash
git add .
git commit -m "Phase 3: Agentic AI brain — LangChain DataFrame Agent with Google Gemini"
git push
```

---

## 9. PHASE 4 — DASHBOARD & FRONT-END

### What Was Built

The Streamlit web application that ties everything together: interactive charts on top, AI chat on the bottom.

### Files Created

---

### File: `src/charts.py`

**Purpose:** Contains 3 functions that each take the DataFrame and return a Plotly figure. Scatter plot (Cost vs Biodegradability), Bar chart (Top 10 by Cleaning Efficacy), Pie chart (Surfactant distribution).

```python
"""
Chart builder module for the Eco-Formulation Copilot.

Each function takes the formulations DataFrame and returns
a Plotly figure object.

WHY PLOTLY (not Matplotlib):
Plotly charts are interactive — hover, zoom, filter.
This mimics Power BI functionality.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_scatter_chart(df: pd.DataFrame) -> go.Figure:
    """
    Interactive scatter plot: Cost vs Biodegradability.
    Colour = Cleaning Efficacy.
    """
    fig = px.scatter(
        df,
        x="Cost_Per_Litre_GBP",
        y="Biodegradability_Score",
        color="Cleaning_Efficacy_Score",
        hover_data=["Formula_ID", "Surfactant_Type", "Toxicity_Level"],
        title="Cost vs Biodegradability (colour = Cleaning Efficacy)",
        labels={
            "Cost_Per_Litre_GBP": "Cost per Litre (£)",
            "Biodegradability_Score": "Biodegradability Score (0-100)",
            "Cleaning_Efficacy_Score": "Cleaning Efficacy (0-100)",
        },
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=40, t=50, b=40),
    )
    return fig


def build_bar_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Horizontal bar chart: Top N formulas by Cleaning Efficacy.
    Colour = Biodegradability.
    """
    top_df = df.nlargest(top_n, "Cleaning_Efficacy_Score")
    fig = px.bar(
        top_df,
        x="Cleaning_Efficacy_Score",
        y="Formula_ID",
        orientation="h",
        color="Biodegradability_Score",
        hover_data=["Surfactant_Type", "Cost_Per_Litre_GBP", "Toxicity_Level"],
        title=f"Top {top_n} Formulas by Cleaning Efficacy (colour = Biodegradability)",
        labels={
            "Cleaning_Efficacy_Score": "Cleaning Efficacy Score (0-100)",
            "Formula_ID": "Formula",
            "Biodegradability_Score": "Biodegradability (0-100)",
        },
        color_continuous_scale="Greens",
    )
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(categoryorder="total ascending"),
    )
    return fig


def build_surfactant_pie_chart(df: pd.DataFrame) -> go.Figure:
    """
    Donut pie chart: Distribution of surfactant types.
    """
    surfactant_counts = df["Surfactant_Type"].value_counts().reset_index()
    surfactant_counts.columns = ["Surfactant_Type", "Count"]
    fig = px.pie(
        surfactant_counts,
        names="Surfactant_Type",
        values="Count",
        title="Surfactant Type Distribution",
        hole=0.3,
    )
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
    )
    return fig
```

---

### File: `app.py`

**Purpose:** The ENTRY POINT of the entire application. Run with `streamlit run app.py`. Builds a single-page web app with dashboard charts + AI chat interface.

```python
"""
Eco-Formulation Copilot — Streamlit Application

This is the ENTRY POINT of the entire application.
Run it with: streamlit run app.py

Layout:
┌─────────────────────────────────────────────┐
│  Title + Subtitle                           │
├─────────────────────────────────────────────┤
│  Key Metrics (4 columns)                    │
├──────────────────────┬──────────────────────┤
│  Scatter Chart       │  Bar Chart           │
├──────────────────────┴──────────────────────┤
│  Pie Chart (centred)                        │
├─────────────────────────────────────────────┤
│  Example Questions (3 buttons)              │
├─────────────────────────────────────────────┤
│  Chat History + Chat Input Box              │
└─────────────────────────────────────────────┘
"""

import streamlit as st

from src.config import APP_TITLE
from src.data_loader import load_data
from src.agent import create_agent, query_agent
from src.charts import (
    build_scatter_chart,
    build_bar_chart,
    build_surfactant_pie_chart,
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧪",
    layout="wide",
)


@st.cache_data
def get_data():
    """Load and cache the formulations DataFrame."""
    return load_data()


@st.cache_resource
def get_agent(_df):
    """Create and cache the LangChain DataFrame Agent."""
    return create_agent(_df)


def main() -> None:
    # --- Header ---
    st.title(f"🧪 {APP_TITLE}")
    st.markdown(
        "An **Agentic AI** proof-of-concept for P&G Newcastle R&D. "
        "Ask questions about chemical formulations in plain English."
    )
    st.divider()

    # --- Load Data ---
    try:
        df = get_data()
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

    # --- Key Metrics Row ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Formulas", len(df))
    col2.metric("Avg Biodegradability", f"{df['Biodegradability_Score'].mean():.1f}/100")
    col3.metric("Avg Cleaning Efficacy", f"{df['Cleaning_Efficacy_Score'].mean():.1f}/100")
    col4.metric("Avg Cost/Litre", f"£{df['Cost_Per_Litre_GBP'].mean():.2f}")
    st.divider()

    # --- Dashboard Charts ---
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(build_scatter_chart(df), use_container_width=True)
    with chart_col2:
        st.plotly_chart(build_bar_chart(df), use_container_width=True)

    pie_col1, pie_col2, pie_col3 = st.columns([1, 2, 1])
    with pie_col2:
        st.plotly_chart(build_surfactant_pie_chart(df), use_container_width=True)
    st.divider()

    # --- AI Chat Section ---
    st.subheader("💬 Ask the R&D Assistant")
    st.caption(
        "Type a question in plain English. The AI agent will write "
        "Pandas code behind the scenes, query the dataset, and return the answer."
    )

    # --- Example Questions (Trait #182 — Intuitive) ---
    example_col1, example_col2, example_col3 = st.columns(3)
    with example_col1:
        if st.button("🔬 Top 5 biodegradable formulas under £2", use_container_width=True):
            st.session_state["prefill"] = (
                "Show me the top 5 formulas with the highest "
                "biodegradability score that cost less than £2 per litre"
            )
    with example_col2:
        if st.button("📊 Average cost by surfactant type", use_container_width=True):
            st.session_state["prefill"] = (
                "What is the average cost per litre for each surfactant type?"
            )
    with example_col3:
        if st.button("🧬 Lowest toxicity formulas", use_container_width=True):
            st.session_state["prefill"] = (
                "Show me the 5 formulas with the lowest toxicity level, "
                "including their biodegradability and cleaning scores"
            )

    # --- Chat State ---
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # --- Agent ---
    try:
        agent = get_agent(df)
    except ValueError as e:
        st.error(f"Agent setup failed: {e}")
        st.info("Make sure your GOOGLE_API_KEY is set in the .env file.")
        st.stop()

    # --- Display Chat History ---
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Handle Prefill ---
    prefill = st.session_state.pop("prefill", None)

    # --- Chat Input ---
    user_input = st.chat_input("Ask about formulations...")
    if prefill:
        user_input = prefill

    # --- Process ---
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Querying formulation database..."):
                answer = query_agent(agent, user_input)
            st.markdown(answer)

        st.session_state["messages"].append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
```

### Phase 4 Key Decisions

1. **Plotly over Matplotlib** — interactive charts mimic Power BI.
2. **`@st.cache_data`** — loads CSV once, reuses on every refresh.
3. **`@st.cache_resource`** — creates agent once, reuses across chat interactions.
4. **3 example question buttons** (Trait #182) — recruiter tests app instantly.
5. **`st.spinner()`** (Trait #191) — shows loading state while LLM processes.
6. **`st.session_state`** — preserves chat history across Streamlit re-runs.

### Phase 4 Git Push

```bash
git add .
git commit -m "Phase 4: Streamlit dashboard with interactive charts and AI chat interface"
git push
```

---

## 10. ERROR LOG — FULL DEBUGGING PROTOCOL

### Error 001 — Pandas Converts "None" String to NaN (Phase 2)

**ERROR TRANSLATION:**

```
ERROR: Enzyme_Type column shows NaN for rows where the enzyme is "None"
└── means → Pandas reads the string "None" from CSV and interprets it as missing value (NaN)
└── expected → Text value "None" to appear as the string "None"
└── received → Pandas converted it to NaN (Not a Number = missing data)
```

**WHERE IT BROKE:**

```
[Step 1 — generate_data.py creates rows with Enzyme_Type = "None"]  ← string written to CSV
    ↓
[Step 2 — CSV file contains the word None]  ← looks fine in the file
    ↓
[Step 3 — Pandas reads the CSV with pd.read_csv()]  ← THIS IS WHERE IT BROKE
    ↓
    Pandas has a built-in rule: if it sees "None" in a CSV,
    it assumes data is MISSING and converts to NaN
    ↓
[Step 4 — DataFrame shows NaN instead of a useful label]  ← broken output
```

**THE FIX:** Changed the string `"None"` to `"No Enzyme"` in `generate_data.py`. Pandas does not auto-convert "No Enzyme" to NaN.

**PREVENTION RULE:** Never use the exact strings `"None"`, `"NA"`, `"null"`, or `"NaN"` as category values in CSV data. Use descriptive labels instead.

---

### Error 002 — AgentType Import Path Moved in LangChain v1.2.14 (Phase 3)

**ERROR TRANSLATION:**

```
ERROR: ModuleNotFoundError: No module named 'langchain.agents.agent_types'
└── means → Python tried to import AgentType from a path that no longer exists
└── expected → langchain.agents.agent_types to contain AgentType class
└── received → The module path does not exist in LangChain v1.2.14
```

**WHERE IT BROKE:**

```
[Step 1 — Python starts importing src/agent.py]
    ↓
[Step 2 — Hits: from langchain.agents.agent_types import AgentType]  ← THIS BROKE
    ↓
    Python searched inside langchain package for agents/agent_types.py
    but that file was moved to langchain_classic in this version
    ↓
[Step 3 — ModuleNotFoundError raised, test collection stops]
```

**THE INVESTIGATION:**

```
Check 1: What version of langchain is installed? → 1.2.14
Check 2: Where does AgentType actually live? → langchain_classic.agents.agent_types
Check 3: Does the function accept a string instead? → YES, "zero-shot-react-description"
```

**THE FIX:** Removed the `AgentType` import entirely. Passed the plain string `"zero-shot-react-description"` directly to `create_pandas_dataframe_agent()`.

**PREVENTION RULE:** When a LangChain function accepts both an enum AND a plain string, always use the plain string. Strings do not break when LangChain reorganises its internal modules between versions.

---

## 11. TRAIT CHECKLIST — WHAT WAS INCLUDED & WHAT WAS SKIPPED

### Background — The 290 Traits

The PLAN.md file contained a massive checklist of 290 software engineering traits, organized into 20 categories:

1. Architecture (20 traits) — Modular, Decoupled, API-driven, Microserviced, etc.
2. Code Quality (16 traits) — Maintainable, Testable, Type-hinted, DRY, etc.
3. Testing & QA (14 traits) — Unit-tested, Integration-tested, Fuzz-tested, etc.
4. Security (20 traits) — Secure, Encrypted, Rate-limited, CORS-configured, etc.
5. Infrastructure & DevOps (23 traits) — Containerised, Cloud-deployed, CI/CD-automated, etc.
6. Reliability & Resilience (15 traits) — Fault-tolerant, Auto-restarting, Circuit-breaker, etc.
7. Scalability & Flexibility (15 traits) — Scalable, Extensible, Feature-flagged, etc.
8. Performance & Optimisation (16 traits) — Lightweight, Low-latency, Cached, etc.
9. API Design (14 traits) — RESTful, Swagger-documented, Paginated, etc.
10. Data Management (15 traits) — Data-validated, Migration-safe, ACID-compliant, etc.
11. Logging & Observability (12 traits) — Logged, Traceable, Metrics-emitting, etc.
12. User Experience (14 traits) — Responsive, Intuitive, Loading-state handled, etc.
13. AI & Intelligence (16 traits) — Prompt-engineered, Anti-hallucinatory, RAG-architected, etc.
14. Documentation (14 traits) — README-complete, API-spec'd, Changelog-maintained, etc.
15. Compliance & Governance (12 traits) — GDPR-aware, Licensed, Auditable, etc.
16. Collaboration & Process (12 traits) — PR-workflow driven, Issue-tracked, etc.
17. Portability & Compatibility (12 traits) — Cross-platform, Cloud-agnostic, etc.
18. Internationalisation (8 traits) — Multi-language, Timezone-aware, etc.
19. Networking & Communication (10 traits) — HTTPS-secured, WebSocket-enabled, etc.
20. Professional & Career Readiness (12 traits) — Production-grade, Demo-ready, etc.

### The YAGNI Principle — Why We Cut 278 Traits

YAGNI stands for "You Aren't Gonna Need It." It is a software engineering principle that says: do not build something unless you actually need it right now.

For a 48-hour proof-of-concept with a hard deadline, attempting to hit all 290 traits guarantees you finish nothing. We ruthlessly cut anything that did not immediately prove the P&G core stack (Data, Agentic AI, Dashboards) or delayed getting a live link in front of the recruiter.

The final selection: 12 must-have traits out of 290.

### INCLUDED (12 traits — high impact, low effort)

| # | Trait | How It Was Implemented |
|---|---|---|
| 25 | Error-handled | `try/except` in `query_agent()` — app never crashes on bad LLM output |
| 27 | Readable | Clean docstrings on every major function |
| 32 | Type-hinted | Python type hints everywhere (e.g., `def query_agent(agent: object, user_question: str) -> str:`) |
| 35 | Well-commented | Docstrings explaining purpose inside the data pipeline |
| 62 | Secret-managed | `.env` file + `python-dotenv` + `.gitignore` blocks `.env` |
| 71 | Containerised | Dockerfile (Phase 5) |
| 77 | CI/CD-automated | GitHub Actions YAML (Phase 5) |
| 182 | Intuitive | 3 example question buttons in the UI |
| 191 | Loading-state handled | `st.spinner()` during LLM processing |
| 202 | Prompt-engineered | Custom SYSTEM_PROMPT with strict rules |
| 203 | Anti-hallucinatory | "Data not available" fallback in prompt |
| 216 | README-complete | Executive summary + P&G alignment (Phase 6) |
| 285 | Commercially-aware | README maps features to job description (Phase 6) |
| 288 | Demo-ready | Live URL via Streamlit Cloud (Phase 6) |

### SKIPPED (time traps for a 48-hour sprint)

| # | Trait | Why Skipped |
|---|---|---|
| 10 | Microserviced | Single Docker container is sufficient for a PoC |
| 79 | Orchestrated (Kubernetes) | Would take 10+ hours to configure |
| 140 | RESTful (full CRUD) | Only need a single chat endpoint |
| 147 | GraphQL-ready | Irrelevant for this project |
| 156 | Migration-safe | No database — just CSV in memory |
| 164 | ACID-compliant | No database transactions |
| 261 | Multi-language (i18n) | English-only demo |
| 39 | End-to-end tested | Time-consuming Selenium tests |
| 69 | Token-authenticated (JWT) | No user login needed for a demo |

---

## 12. PACKAGE INSTALLATION & TESTING — HOW IT WORKS

### How Packages Are Downloaded

```
pip install -r requirements.txt
```

**What happens under the hood:**

```
pip reads requirements.txt line by line
    ↓
For each package (e.g., "pandas==2.2.3"):
    pip connects to PyPI (https://pypi.org)
    ↓
    Finds "pandas" version 2.2.3
    ↓
    Downloads it plus all its dependencies
    ↓
    Installs the files into the Python library folder
    ↓
    Now any script can do: import pandas
```

### How Tests Are Run

```
python -m pytest tests/ -v
```

**What happens under the hood:**

```
Step 1 → pytest scans the tests/ folder
    ↓
Step 2 → Finds every file starting with "test_"
    ↓
Step 3 → Inside each file, finds every function starting with "test_"
    ↓
Step 4 → Runs each test function one by one
    ↓
Step 5 → For each test:
           If no error raised → PASSED
           If assert fails    → FAILED
           If import breaks   → ERROR
    ↓
Step 6 → Prints final count: "20 passed, 0 failed"
```

### Virtual Environment Setup (on your machine)

```bash
cd eco-formulation-copilot
python -m venv venv              # Create isolated environment
venv\Scripts\activate            # Activate it (Windows)
pip install -r requirements.txt  # Install all packages
python -m pytest tests/ -v       # Run all tests
```

### VS Code Integration

Press `Ctrl+Shift+P` → "Python: Select Interpreter" → choose the `venv` path. This removes the wavy underlines on imports.

---

## 13. GIT WORKFLOW — EVERY PUSH

### Initial Setup (one time)

```bash
git init
git add .
git commit -m "Phase 1: Project skeleton and configuration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/eco-formulation-copilot.git
git push -u origin main
```

### After Every Phase (3 commands)

```bash
git add .
git commit -m "Phase N: description"
git push
```

### Commit History

```
Phase 1: Project skeleton and configuration
Phase 2: Data generation and loading layer with 13 passing tests
Phase 3: Agentic AI brain — LangChain DataFrame Agent with Google Gemini
Phase 4: Streamlit dashboard with interactive charts and AI chat interface
Phase 5: (pending) Containerisation and CI/CD
Phase 6: (pending) Deployment and documentation
```

---

## 14. REMAINING PHASES — WHAT COMES NEXT

### Phase 5 — Containerisation & CI/CD

**Files to create:**
- `Dockerfile` — packages the app into a Docker container
- `.dockerignore` — tells Docker to skip `.env`, `__pycache__`, `venv/`
- `.github/workflows/ci.yml` — GitHub Actions pipeline for lint + tests

### Phase 6 — Deployment & Documentation

**Files to create:**
- `README.md` — executive summary, live demo link, architecture diagram, P&G job alignment
- Streamlit Community Cloud deployment — live public URL

### After All Phases — Project Closeout

- Full file/folder structure recap
- Key concepts learned summary
- Three follow-up challenges

---

## TEST RESULTS SUMMARY

```
Total tests: 20
Passed:      20
Failed:       0

test_data_loader.py (13 tests):
  ✓ test_loads_successfully
  ✓ test_correct_row_count
  ✓ test_correct_column_count
  ✓ test_all_expected_columns_present
  ✓ test_no_missing_values
  ✓ test_file_not_found_raises_error
  ✓ test_biodegradability_range
  ✓ test_cleaning_efficacy_range
  ✓ test_toxicity_range
  ✓ test_cost_is_positive
  ✓ test_concentration_range
  ✓ test_empty_dataframe_raises_error
  ✓ test_missing_column_raises_error

test_agent.py (7 tests):
  ✓ test_prompt_contains_role
  ✓ test_prompt_contains_anti_hallucination
  ✓ test_prompt_contains_column_descriptions
  ✓ test_prompt_forbids_invention
  ✓ test_empty_string_returns_message
  ✓ test_whitespace_only_returns_message
  ✓ test_none_agent_with_valid_question_returns_error
```

---

> **This document will be updated as Phase 5 and Phase 6 are completed.**
