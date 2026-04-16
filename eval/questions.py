"""
Evaluation questions for the Eco-Formulation Copilot agent.

This file defines 20 test questions, spread across 6 categories:
    - COUNTING (4)    — "How many formulas have X?"
    - AGGREGATION (4) — "What is the average/max/min of X?"
    - FILTERING (3)   — "Show me formulas where X"
    - RANKING (3)     — "What are the top/bottom N by X?"
    - GROUPING (3)    — "What is X grouped by Y?"
    - LOOKUP (3)      — "What is the value of X for formula Y?"

HOW IT WORKS:
    Each question is a dictionary with these keys:
    - id:             unique short name (e.g., "count_bio_above_90")
    - category:       which of the 6 categories it belongs to
    - question:       the plain English question to send to the agent
    - compute_answer: a function that takes a DataFrame and returns
                      the correct answer (computed with Pandas)
    - match_type:     how to check the agent's response:
        "numeric"     — extract a number from the response, compare
                        with tolerance
        "keyword"     — check if a specific string appears in the
                        response
        "keyword_all" — check if ALL strings in a list appear in
                        the response
        "count"       — extract a number from the response, compare
                        against a count value (exact integer match
                        with small tolerance)
        "ranking"     — for top-N / bottom-N queries where ties
                        exist at the boundary. Checks that at least
                        N valid IDs from the tied set appear

WHY COMPUTE AT RUNTIME:
    The correct answers are NOT hardcoded. They are computed fresh
    from the DataFrame every time the evaluation runs. This means:
    1. If the dataset changes, the evaluation still works
    2. No risk of human calculation errors in the expected values
    3. The ground truth is always the real data
"""

import pandas as pd
from typing import Any


def _count_bio_above_90(df: pd.DataFrame) -> int:
    """How many formulas have biodegradability score above 90."""
    return int(len(df[df["Biodegradability_Score"] > 90]))


def _count_no_enzyme(df: pd.DataFrame) -> int:
    """How many formulas use No Enzyme."""
    return int(len(df[df["Enzyme_Type"] == "No Enzyme"]))


def _count_cost_below_1(df: pd.DataFrame) -> int:
    """How many formulas cost less than £1.00 per litre."""
    return int(len(df[df["Cost_Per_Litre_GBP"] < 1.0]))


def _count_cleaning_above_90(df: pd.DataFrame) -> int:
    """How many formulas have cleaning efficacy above 90."""
    return int(len(df[df["Cleaning_Efficacy_Score"] > 90]))


def _avg_cost(df: pd.DataFrame) -> float:
    """Average cost per litre across all formulas."""
    return round(float(df["Cost_Per_Litre_GBP"].mean()), 2)


def _max_biodegradability(df: pd.DataFrame) -> int:
    """Maximum biodegradability score in the dataset."""
    return int(df["Biodegradability_Score"].max())


def _min_toxicity(df: pd.DataFrame) -> float:
    """Minimum toxicity level in the dataset."""
    return round(float(df["Toxicity_Level"].min()), 2)


def _unique_surfactant_count(df: pd.DataFrame) -> int:
    """Number of unique surfactant types."""
    return int(df["Surfactant_Type"].nunique())


def _filter_low_toxicity_ids(df: pd.DataFrame) -> list[str]:
    """Formula IDs where toxicity is below 0.5."""
    filtered = df[df["Toxicity_Level"] < 0.5]
    return sorted(filtered["Formula_ID"].tolist())


def _filter_bio_and_cleaning_above_90(df: pd.DataFrame) -> list[str]:
    """Formula IDs with both biodegradability and cleaning above 90."""
    filtered = df[
        (df["Biodegradability_Score"] > 90)
        & (df["Cleaning_Efficacy_Score"] > 90)
    ]
    return sorted(filtered["Formula_ID"].tolist())


def _filter_apg_cheap(df: pd.DataFrame) -> int:
    """Count of Alkyl Polyglucoside formulas costing less than £2."""
    filtered = df[
        (df["Surfactant_Type"] == "Alkyl Polyglucoside")
        & (df["Cost_Per_Litre_GBP"] < 2.0)
    ]
    return int(len(filtered))


def _top3_biodegradability_ids(df: pd.DataFrame) -> dict:
    """
    All formula IDs that could correctly appear in a "top 3
    by biodegradability" answer, including ties.

    Returns a dict with:
        valid_ids  — all IDs tied at the boundary score or above
        min_count  — how many the response must contain (3)
    """
    top3 = df.nlargest(3, "Biodegradability_Score")
    boundary_score = top3["Biodegradability_Score"].min()
    all_valid = df[
        df["Biodegradability_Score"] >= boundary_score
    ]
    return {
        "valid_ids": all_valid["Formula_ID"].tolist(),
        "min_count": 3,
    }


def _cheapest3_ids(df: pd.DataFrame) -> dict:
    """
    All formula IDs that could correctly appear in a "3 cheapest"
    answer, including ties at the boundary cost.

    Returns a dict with:
        valid_ids  — all IDs tied at the boundary cost or below
        min_count  — how many the response must contain (3)
    """
    cheapest3 = df.nsmallest(3, "Cost_Per_Litre_GBP")
    boundary_cost = cheapest3["Cost_Per_Litre_GBP"].max()
    all_valid = df[
        df["Cost_Per_Litre_GBP"] <= boundary_cost
    ]
    return {
        "valid_ids": all_valid["Formula_ID"].tolist(),
        "min_count": 3,
    }


def _top5_cleaning_ids(df: pd.DataFrame) -> dict:
    """
    All formula IDs that could correctly appear in a "top 5
    by cleaning efficacy" answer, including ties.

    Returns a dict with:
        valid_ids  — all IDs tied at the boundary score or above
        min_count  — how many the response must contain (5)
    """
    top5 = df.nlargest(5, "Cleaning_Efficacy_Score")
    boundary_score = top5["Cleaning_Efficacy_Score"].min()
    all_valid = df[
        df["Cleaning_Efficacy_Score"] >= boundary_score
    ]
    return {
        "valid_ids": all_valid["Formula_ID"].tolist(),
        "min_count": 5,
    }


def _avg_bio_by_surfactant(df: pd.DataFrame) -> dict[str, float]:
    """Average biodegradability score per surfactant type."""
    grouped = df.groupby("Surfactant_Type")["Biodegradability_Score"]
    return grouped.mean().round(2).to_dict()


def _count_by_enzyme(df: pd.DataFrame) -> dict[str, int]:
    """Count of formulas per enzyme type."""
    return df["Enzyme_Type"].value_counts().to_dict()


def _avg_cost_by_polymer(df: pd.DataFrame) -> dict[str, float]:
    """Average cost per litre per polymer type."""
    grouped = df.groupby("Polymer_Type")["Cost_Per_Litre_GBP"]
    return grouped.mean().round(2).to_dict()


def _lookup_cost_eco_f_0012(df: pd.DataFrame) -> float:
    """Cost per litre of ECO-F-0012."""
    row = df[df["Formula_ID"] == "ECO-F-0012"]
    return float(row["Cost_Per_Litre_GBP"].values[0])


def _lookup_surfactant_eco_f_0001(df: pd.DataFrame) -> str:
    """Surfactant type of ECO-F-0001."""
    row = df[df["Formula_ID"] == "ECO-F-0001"]
    return str(row["Surfactant_Type"].values[0])


def _lookup_bio_eco_f_0100(df: pd.DataFrame) -> int:
    """Biodegradability score of ECO-F-0100."""
    row = df[df["Formula_ID"] == "ECO-F-0100"]
    return int(row["Biodegradability_Score"].values[0])


# ============================================================
# The 20 Evaluation Questions
# ============================================================
# Each dict has: id, category, question, compute_answer, match_type
#
# match_type controls how matcher.py checks the agent's response:
#   "numeric"     — pull a number from text, compare ± tolerance
#   "keyword"     — check if a string is in the response
#   "keyword_all" — check if ALL strings in a list are present
#   "count"       — same as numeric but expects exact integer
#   "ranking"     — for top-N with ties, check N valid IDs appear
# ============================================================

EVAL_QUESTIONS: list[dict[str, Any]] = [
    # ---- COUNTING (4) ----
    {
        "id": "count_bio_above_90",
        "category": "counting",
        "question": (
            "How many formulas have a biodegradability score "
            "above 90?"
        ),
        "compute_answer": _count_bio_above_90,
        "match_type": "count",
    },
    {
        "id": "count_no_enzyme",
        "category": "counting",
        "question": (
            "How many formulas use No Enzyme as the enzyme type?"
        ),
        "compute_answer": _count_no_enzyme,
        "match_type": "count",
    },
    {
        "id": "count_cost_below_1",
        "category": "counting",
        "question": (
            "How many formulas cost less than £1.00 per litre?"
        ),
        "compute_answer": _count_cost_below_1,
        "match_type": "count",
    },
    {
        "id": "count_cleaning_above_90",
        "category": "counting",
        "question": (
            "How many formulas have a cleaning efficacy score "
            "above 90?"
        ),
        "compute_answer": _count_cleaning_above_90,
        "match_type": "count",
    },

    # ---- AGGREGATION (4) ----
    {
        "id": "avg_cost",
        "category": "aggregation",
        "question": (
            "What is the average cost per litre across all "
            "formulas in the dataset?"
        ),
        "compute_answer": _avg_cost,
        "match_type": "numeric",
        "tolerance": 0.05,
    },
    {
        "id": "max_biodegradability",
        "category": "aggregation",
        "question": (
            "What is the maximum biodegradability score in "
            "the dataset?"
        ),
        "compute_answer": _max_biodegradability,
        "match_type": "numeric",
        "tolerance": 0.5,
    },
    {
        "id": "min_toxicity",
        "category": "aggregation",
        "question": (
            "What is the minimum toxicity level in the dataset?"
        ),
        "compute_answer": _min_toxicity,
        "match_type": "numeric",
        "tolerance": 0.02,
    },
    {
        "id": "unique_surfactant_count",
        "category": "aggregation",
        "question": (
            "How many unique surfactant types are in the dataset?"
        ),
        "compute_answer": _unique_surfactant_count,
        "match_type": "count",
    },

    # ---- FILTERING (3) ----
    {
        "id": "filter_low_toxicity",
        "category": "filtering",
        "question": (
            "Which formulas have a toxicity level below 0.5? "
            "List their Formula IDs."
        ),
        "compute_answer": _filter_low_toxicity_ids,
        "match_type": "keyword_all",
    },
    {
        "id": "filter_bio_and_cleaning_90",
        "category": "filtering",
        "question": (
            "Which formulas have both a biodegradability score "
            "above 90 AND a cleaning efficacy score above 90? "
            "List their Formula IDs."
        ),
        "compute_answer": _filter_bio_and_cleaning_above_90,
        "match_type": "keyword_all",
    },
    {
        "id": "filter_apg_cheap",
        "category": "filtering",
        "question": (
            "How many formulas use Alkyl Polyglucoside as the "
            "surfactant type and cost less than £2 per litre?"
        ),
        "compute_answer": _filter_apg_cheap,
        "match_type": "count",
    },

    # ---- RANKING (3) ----
    {
        "id": "top3_biodegradability",
        "category": "ranking",
        "question": (
            "What are the top 3 formulas with the highest "
            "biodegradability score? Show their Formula IDs."
        ),
        "compute_answer": _top3_biodegradability_ids,
        "match_type": "ranking",
    },
    {
        "id": "cheapest3",
        "category": "ranking",
        "question": (
            "What are the 3 cheapest formulas by cost per "
            "litre? Show their Formula IDs."
        ),
        "compute_answer": _cheapest3_ids,
        "match_type": "ranking",
    },
    {
        "id": "top5_cleaning",
        "category": "ranking",
        "question": (
            "What are the top 5 formulas with the highest "
            "cleaning efficacy score? Show their Formula IDs."
        ),
        "compute_answer": _top5_cleaning_ids,
        "match_type": "ranking",
    },

    # ---- GROUPING (3) ----
    {
        "id": "avg_bio_by_surfactant",
        "category": "grouping",
        "question": (
            "What is the average biodegradability score for "
            "each surfactant type?"
        ),
        "compute_answer": _avg_bio_by_surfactant,
        "match_type": "keyword_all",
    },
    {
        "id": "count_by_enzyme",
        "category": "grouping",
        "question": (
            "How many formulas are there for each enzyme type?"
        ),
        "compute_answer": _count_by_enzyme,
        "match_type": "keyword_all",
    },
    {
        "id": "avg_cost_by_polymer",
        "category": "grouping",
        "question": (
            "What is the average cost per litre for each "
            "polymer type?"
        ),
        "compute_answer": _avg_cost_by_polymer,
        "match_type": "keyword_all",
    },

    # ---- SPECIFIC LOOKUP (3) ----
    {
        "id": "lookup_cost_0012",
        "category": "lookup",
        "question": (
            "What is the cost per litre of formula ECO-F-0012?"
        ),
        "compute_answer": _lookup_cost_eco_f_0012,
        "match_type": "numeric",
        "tolerance": 0.01,
    },
    {
        "id": "lookup_surfactant_0001",
        "category": "lookup",
        "question": (
            "What surfactant type does formula ECO-F-0001 use?"
        ),
        "compute_answer": _lookup_surfactant_eco_f_0001,
        "match_type": "keyword",
    },
    {
        "id": "lookup_bio_0100",
        "category": "lookup",
        "question": (
            "What is the biodegradability score of formula "
            "ECO-F-0100?"
        ),
        "compute_answer": _lookup_bio_eco_f_0100,
        "match_type": "numeric",
        "tolerance": 0.5,
    },
]
