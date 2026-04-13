# Eco-Formulation Copilot

[![CI](https://github.com/NakuSurrey/eco-formulation-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/NakuSurrey/eco-formulation-copilot/actions/workflows/ci.yml)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Executive Summary

A proof-of-concept **Agentic AI** application built to accelerate high-throughput R&D data querying for sustainable chemical products. Scientists ask questions about chemical formulations in plain English. The AI agent translates the question into Pandas code, executes it against a structured dataset, and returns the answer — no coding required.

Built specifically to demonstrate the technical skills required for the **P&G Newcastle Innovation Centre — Software Development Industrial Placement 2026**.

---

## Live Demo

**[http://46.225.208.197](http://46.225.208.197)** — deployed on a Hetzner Cloud VPS (Ubuntu, Nginx reverse proxy, systemd service).

---

## How It Works

```
Scientist types a plain English question
        |
        v
Streamlit Front-End (app.py) captures the question
        |
        v
LangChain DataFrame Agent (agent.py) receives the question
        |
        v
Google Gemini LLM reads the question and writes Pandas code
        |
        v
The agent executes that Pandas code against the DataFrame
        |
        v
The result (number, table, list) is returned as a string
        |
        v
Streamlit displays the answer in the chat interface
```

The scientist never writes or sees any code. The LLM handles the translation from English to Pandas to Answer.

---

## Features

**Interactive Dashboard** — Three Plotly charts provide an instant visual overview of the dataset: Cost vs Biodegradability scatter plot, Top 10 by Cleaning Efficacy bar chart, and Surfactant Type distribution pie chart. All charts support hover, zoom, and filter interactions.

**AI Chat Interface** — A conversational chat where the user types questions like "Show me the top 5 formulas with the highest biodegradability score under £2 per litre" and the AI returns a data-driven answer.

**Example Question Buttons** — Three pre-written questions let anyone test the app instantly without thinking of what to type.

**Anti-Hallucination Safeguards** — The AI agent is prompt-engineered to only answer from the dataset. If the data does not contain the answer, it responds with "Data not available" instead of inventing information.

**Key Metrics Row** — Four summary statistics (Total Formulas, Avg Biodegradability, Avg Cleaning Efficacy, Avg Cost/Litre) appear at the top of the dashboard for an instant snapshot.

---

## How This Maps to the P&G Job Description

| P&G Requirement | Implementation in This Project |
|---|---|
| Databricks (data pipelines & transformation) | Pandas DataFrame + CSV data loading with validation |
| Power BI (interactive dashboards & analytics) | Streamlit + Plotly (interactive, hoverable charts) |
| Microsoft Copilot Studio & Agentic AI | LangChain DataFrame Agent + Google Gemini LLM |
| Data engineering, analytics & AI development | `data_loader.py` + `generate_data.py` + `agent.py` |
| Testing, troubleshooting & optimisation | pytest (20 automated tests) + flake8 linting |
| CI/CD & DevOps workflows | GitHub Actions (lint + test + Docker build on every push) |

---

## Tech Stack

| Tool | Role | Why This Over Alternatives |
|---|---|---|
| **Python 3.10** | Core language | Entire stack is Python-native |
| **Streamlit** | Web framework | Full dashboard + chat UI in under 100 lines. No HTML/CSS/JS needed |
| **LangChain** | Agent orchestration | Pre-built `create_pandas_dataframe_agent` for structured data querying |
| **Google Gemini 2.0 Flash** | LLM | Free tier (30 req/min), no credit card, fast response times |
| **Pandas** | Data manipulation | Lightweight Databricks substitute. Agent writes Pandas code to query data |
| **Plotly** | Data visualisation | Interactive charts (hover, zoom, filter). Lightweight Power BI substitute |
| **Docker** | Containerisation | Packages entire app into a portable image. Runs identically on any machine |
| **GitHub Actions** | CI/CD | Automated lint + test + Docker build on every push |
| **pytest** | Testing | 20 automated tests covering data loading, agent behaviour, and error handling |
| **flake8** | Code quality | Enforces consistent code style across the project |

---

## Dataset

500 rows of synthetic chemical formulation data with 9 columns:

| Column | Description | Range |
|---|---|---|
| `Formula_ID` | Unique identifier | F-0001 to F-0500 |
| `Surfactant_Type` | Chemical surfactant category | 5 categories |
| `Polymer_Type` | Polymer used in the formula | 5 categories |
| `Enzyme_Type` | Enzyme used (or "No Enzyme") | 4 categories |
| `Concentration_Pct` | Active ingredient concentration | 5.0 – 40.0% |
| `Biodegradability_Score` | Environmental friendliness score | 30 – 98 out of 100 |
| `Cleaning_Efficacy_Score` | How well it cleans | 40 – 99 out of 100 |
| `Toxicity_Level` | Toxicity measurement | 0.5 – 8.0 |
| `Cost_Per_Litre_GBP` | Manufacturing cost | £0.45 – £4.80 |

Data is generated with `random.seed(42)` for full reproducibility.

---

## Project Structure

```
eco-formulation-copilot/
├── src/
│   ├── __init__.py           — Makes src/ a Python package
│   ├── config.py             — Single source of truth for all settings
│   ├── data_loader.py        — Loads and validates the CSV into a DataFrame
│   ├── agent.py              — LangChain DataFrame Agent powered by Gemini
│   └── charts.py             — Builds Plotly charts (scatter, bar, pie)
├── tests/
│   ├── __init__.py           — Makes tests/ a Python package
│   ├── test_data_loader.py   — 13 tests for data loading and validation
│   └── test_agent.py         — 7 tests for agent prompt and error handling
├── data/
│   ├── generate_data.py      — Script to generate the synthetic dataset
│   └── formulations.csv      — The 500-row dataset
├── .github/
│   └── workflows/
│       └── ci.yml            — GitHub Actions CI/CD pipeline
├── app.py                    — Streamlit entry point (run this)
├── Dockerfile                — Container definition
├── .dockerignore             — Files excluded from Docker image
├── requirements.txt          — Pinned Python dependencies
├── .env.example              — Template for environment variables
├── .gitignore                — Files excluded from Git
└── ERRORS.md                 — Running log of every error and its fix
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- A free Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Option 1: Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/NakuSurrey/eco-formulation-copilot.git
cd eco-formulation-copilot

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Open .env and replace "your_google_api_key_here" with your real key

# 5. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Option 2: Run with Docker

```bash
# 1. Build the container
docker build -t eco-formulation-copilot .

# 2. Run the container (pass your API key via .env file)
docker run -p 8501:8501 --env-file .env eco-formulation-copilot
```

The app opens at `http://localhost:8501`.

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only data loader tests
pytest tests/test_data_loader.py -v

# Run only agent tests
pytest tests/test_agent.py -v

# Run linting
flake8 src/ tests/ app.py --max-line-length=120
```

Tests that require a live Google API key are automatically skipped when the key is not present. This allows CI/CD to run the full test suite without exposing secrets.

---

## CI/CD Pipeline

Every push to `main` triggers three parallel jobs on GitHub Actions:

1. **Lint** — Runs `flake8` to check code style (max line length: 120 chars)
2. **Test** — Runs `pytest` to execute all 20 unit tests
3. **Docker** — Verifies the Docker image builds successfully

The badge at the top of this README shows the current status.

---

## License

This project is available for educational and portfolio purposes.
