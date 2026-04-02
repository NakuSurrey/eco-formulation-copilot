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
