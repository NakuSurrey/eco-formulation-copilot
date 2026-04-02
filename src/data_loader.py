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
# This dictionary maps each column name to the Pandas dtype
# it MUST have after loading. If a column is missing or has
# the wrong type, the validation will catch it immediately.
# ============================================================

EXPECTED_COLUMNS: dict[str, str] = {
    "Formula_ID": "object",                # Text (e.g., "ECO-F-0001")
    "Surfactant_Type": "object",           # Text category
    "Polymer_Type": "object",              # Text category
    "Enzyme_Type": "object",               # Text category
    "Concentration_Pct": "float64",        # Decimal number
    "Biodegradability_Score": "int64",     # Whole number 0-100
    "Cleaning_Efficacy_Score": "int64",    # Whole number 0-100
    "Toxicity_Level": "float64",           # Decimal number
    "Cost_Per_Litre_GBP": "float64",       # Decimal number (price)
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
    # Check 1: Is the DataFrame empty?
    if df.empty:
        raise ValueError(
            "Dataset is empty. Run 'python data/generate_data.py' "
            "to create the formulations CSV."
        )

    # Check 2: Are all expected columns present?
    missing_cols = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing columns in dataset: {missing_cols}. "
            f"Expected columns: {list(EXPECTED_COLUMNS.keys())}"
        )

    # Check 3: Are there any missing values?
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

    Parameters:
        filepath: Path to the CSV file. Defaults to DATA_FILEPATH from config.py.

    Returns:
        A validated Pandas DataFrame with 500 rows and 9 columns.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the DataFrame is empty, missing columns, or has NaN values.
    """
    # Step 1: Check the file exists
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"Data file not found at: {filepath}\n"
            f"Run 'python data/generate_data.py' to create it."
        )

    # Step 2: Read the CSV
    df = pd.read_csv(filepath)

    # Step 3: Validate the schema
    validate_dataframe(df)

    # Step 4: Return the clean DataFrame
    return df
