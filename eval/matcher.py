"""
Hybrid matcher for agent evaluation responses.

This module checks whether the agent's text response contains
the correct answer. It supports three matching strategies:

MATCHING STRATEGIES:
    1. numeric  — extract numbers from the agent's text, compare
                  the closest one against the expected value with
                  a tolerance (e.g., ±0.05)
    2. keyword  — check if a specific string appears somewhere
                  in the agent's response (case-insensitive)
    3. keyword_all — check if ALL strings in a list appear in
                     the response (case-insensitive)
    4. count    — same as numeric, but expects an exact integer
                  match (tolerance of 0.5 to handle "83" vs 83)

WHY HYBRID:
    The agent returns free-text answers like:
        "The average cost per litre is £2.53"
        "There are 87 formulas with biodegradability above 90"

    Some answers are numbers (need numeric extraction).
    Some answers are text strings (need keyword matching).
    Some answers are lists of IDs (need keyword_all).
    Using one strategy for everything would miss half the cases.

FLOW:
    agent_response (str) + expected_answer (computed from DataFrame)
        ↓
    check_match() — picks the right strategy based on match_type
        ↓
    True/False — did the agent get it right?
"""

import re
from typing import Any


def extract_numbers(text: str) -> list[float]:
    """
    Pulls all numbers out of a text string.

    Handles integers, decimals, and numbers with commas.
    Examples:
        "The average is £2.53"  → [2.53]
        "There are 87 formulas" → [87.0]
        "Cost: 1,234.56"       → [1234.56]

    Returns a list of floats, in the order they appear in the text.
    Returns an empty list if no numbers are found.
    """
    # pattern explanation:
    #   -?        optional negative sign
    #   \d{1,3}   1-3 digits (handles comma-separated thousands)
    #   (,\d{3})* optional groups of comma + 3 digits
    #   (\.\d+)?  optional decimal point + digits
    pattern = r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?"
    matches = re.findall(pattern, text)

    numbers = []
    for match in matches:
        # remove commas before converting to float
        clean = match.replace(",", "")
        try:
            numbers.append(float(clean))
        except ValueError:
            # skip if conversion fails for any reason
            continue

    return numbers


def _match_numeric(
    response: str, expected: float, tolerance: float = 0.05
) -> bool:
    """
    Checks if any number in the response is close enough
    to the expected value.

    HOW IT WORKS:
    Step 1 → Extract all numbers from the agent's text
    Step 2 → For each number, compute the absolute difference
             from the expected value
    Step 3 → If any number is within the tolerance, return True

    Parameters:
        response:  the agent's text answer
        expected:  the correct numeric value (from Pandas)
        tolerance: how far off the agent can be and still pass

    Returns:
        True if any extracted number is within tolerance of expected.
    """
    numbers = extract_numbers(response)
    if not numbers:
        return False

    for num in numbers:
        if abs(num - expected) <= tolerance:
            return True

    return False


def _match_keyword(response: str, expected: str) -> bool:
    """
    Checks if the expected string appears in the response.

    Both strings are compared in lowercase to handle variations
    like "Alcohol Ethoxylate" vs "alcohol ethoxylate".

    Parameters:
        response: the agent's text answer
        expected: the string that must appear in the response

    Returns:
        True if the expected string is found (case-insensitive).
    """
    return expected.lower() in response.lower()


def _match_keyword_all(
    response: str, expected: list | dict
) -> bool:
    """
    Checks if ALL expected strings appear in the response.

    Accepts either:
    - A list of strings (e.g., ["ECO-F-0007", "ECO-F-0012"])
    - A dict where keys are the strings to find (e.g., surfactant
      type names from a groupby result)

    For dict values, also checks if the dict's values (as strings)
    appear in the response. This handles groupby results where
    both the group name and the computed value should be present.

    Parameters:
        response: the agent's text answer
        expected: list of strings or dict of key-value pairs

    Returns:
        True if ALL expected strings are found (case-insensitive).
        For dicts: True if all KEYS are found. Values are checked
        as a bonus but do not cause failure if missing (the LLM
        may round differently).
    """
    response_lower = response.lower()

    if isinstance(expected, dict):
        # for groupby results, check that all group names appear
        keys = list(expected.keys())
        all_keys_found = all(
            str(k).lower() in response_lower for k in keys
        )
        return all_keys_found

    if isinstance(expected, list):
        if not expected:
            # empty list means no results expected — the agent
            # should say something like "no formulas found"
            no_result_keywords = ["no ", "none", "0 formula", "zero"]
            return any(kw in response_lower for kw in no_result_keywords)

        return all(
            str(item).lower() in response_lower for item in expected
        )

    # fallback: treat as single keyword
    return str(expected).lower() in response_lower


def _match_ranking(response: str, expected: dict) -> bool:
    """
    Checks if the response contains enough valid IDs from a
    ranking query where ties are possible.

    WHY THIS EXISTS:
    When you ask "top 3 by biodegradability", there might be
    8 formulas all tied at score 99. Pandas nlargest(3) picks
    3 of them, but the agent might pick a different 3. Both
    answers are correct. This matcher handles that by checking
    if the response contains at least N IDs from the full set
    of tied candidates.

    Parameters:
        response: the agent's text answer
        expected: a dict with two keys:
            "valid_ids" — list of ALL formula IDs that would be
                          correct at the tied ranks
            "min_count" — how many of those IDs must appear in
                          the response (e.g., 3 for "top 3")

    Returns:
        True if at least min_count valid IDs appear in the response.
    """
    response_lower = response.lower()
    valid_ids = expected["valid_ids"]
    min_count = expected["min_count"]

    found_count = sum(
        1 for vid in valid_ids
        if str(vid).lower() in response_lower
    )

    return found_count >= min_count


def check_match(
    response: str,
    expected: Any,
    match_type: str,
    tolerance: float = 0.05,
) -> bool:
    """
    Main entry point — checks if the agent's response matches
    the expected answer using the specified strategy.

    This is the ONLY function the rest of the evaluation code
    calls. It picks the right matching strategy based on
    match_type and delegates to the correct internal function.

    Parameters:
        response:   the agent's text answer (string)
        expected:   the correct answer (from compute_answer function)
        match_type: one of "numeric", "keyword", "keyword_all",
                    "ranking", or "count"
        tolerance:  for numeric matches, how close is close enough

    Returns:
        True if the agent's answer matches the expected answer.
        False if it does not match, or if the response is empty.

    FLOW:
        response + expected + match_type
            ↓
        match_type == "numeric"     → _match_numeric()
        match_type == "count"       → _match_numeric(tolerance=0.5)
        match_type == "keyword"     → _match_keyword()
        match_type == "keyword_all" → _match_keyword_all()
        match_type == "ranking"     → _match_ranking()
            ↓
        True / False
    """
    if not response or not response.strip():
        return False

    if match_type == "numeric":
        return _match_numeric(response, float(expected), tolerance)

    elif match_type == "count":
        # counts are integers — tolerance of 0.5 handles "83" vs 83
        return _match_numeric(response, float(expected), tolerance=0.5)

    elif match_type == "keyword":
        return _match_keyword(response, str(expected))

    elif match_type == "keyword_all":
        return _match_keyword_all(response, expected)

    elif match_type == "ranking":
        return _match_ranking(response, expected)

    else:
        raise ValueError(
            f"Unknown match_type: '{match_type}'. "
            f"Expected: numeric, keyword, keyword_all, "
            f"ranking, or count."
        )
