"""
Pytest integration for agent evaluation.

This file turns each of the 20 evaluation questions into a
separate pytest test case. Each test:
    1. Loads the DataFrame
    2. Creates the agent
    3. Sends one question to the agent
    4. Computes the correct answer from the DataFrame
    5. Checks if the agent's response matches

WHY PYTEST (not just run_eval.py):
    - pytest gives per-test PASS/FAIL in CI output
    - pytest integrates with GitHub Actions CI badge
    - pytest can be filtered: run only counting tests, only
      aggregation tests, etc., using -k flag
    - pytest shows clear failure messages with expected vs actual

HOW TO RUN:
    cd eco-formulation-copilot

    # run all 20 evaluation tests
    pytest tests/test_agent_eval.py -v

    # run only counting tests
    pytest tests/test_agent_eval.py -v -k "counting"

    # run only one specific test
    pytest tests/test_agent_eval.py -v -k "count_bio_above_90"

NOTE: All 20 tests require GOOGLE_API_KEY to be set.
When the key is not present (e.g., in GitHub Actions CI),
all 20 tests are automatically skipped.
"""

import os
import pytest
import pandas as pd

from src.data_loader import load_data
from src.agent import create_agent, query_agent
from eval.questions import EVAL_QUESTIONS
from eval.matcher import check_match


# ============================================================
# Skip all tests if GOOGLE_API_KEY is not available
# ============================================================
# These tests call the real Gemini API, so they cannot run
# in CI/CD without exposing secrets. The skip decorator
# makes pytest show "SKIPPED" instead of "FAILED".
# ============================================================
HAS_API_KEY = bool(os.getenv("GOOGLE_API_KEY", ""))
skip_no_key = pytest.mark.skipif(
    not HAS_API_KEY,
    reason="GOOGLE_API_KEY not set — skipping live agent eval tests"
)


# ============================================================
# Shared fixtures — load data and create agent ONCE
# ============================================================
# Using module-scoped fixtures means the DataFrame is loaded
# once and the agent is created once for all 20 tests.
# Without this, each test would create a new agent — wasting
# time and API quota.
# ============================================================

@pytest.fixture(scope="module")
def eval_df() -> pd.DataFrame:
    """Loads the formulations DataFrame once for all eval tests."""
    return load_data()


@pytest.fixture(scope="module")
def eval_agent(eval_df: pd.DataFrame) -> object:
    """Creates the LangChain agent once for all eval tests."""
    return create_agent(eval_df)


# ============================================================
# Helper: Build test IDs from question IDs
# ============================================================
# This gives pytest nice test names like:
#   test_agent_eval[count_bio_above_90]
#   test_agent_eval[avg_cost]
# instead of generic test_agent_eval[0], test_agent_eval[1]
# ============================================================
question_ids = [q["id"] for q in EVAL_QUESTIONS]


@skip_no_key
@pytest.mark.parametrize(
    "question_data",
    EVAL_QUESTIONS,
    ids=question_ids,
)
def test_agent_eval(
    question_data: dict,
    eval_df: pd.DataFrame,
    eval_agent: object,
) -> None:
    """
    Sends one evaluation question to the agent and checks
    if the response matches the expected answer.

    Each of the 20 questions runs as a separate test case.
    If the agent gives a wrong answer, the test fails with
    a clear message showing what was expected vs what was received.
    """
    q_id = question_data["id"]
    category = question_data["category"]
    question = question_data["question"]
    match_type = question_data["match_type"]
    tolerance = question_data.get("tolerance", 0.05)

    # compute the correct answer from the real DataFrame
    expected = question_data["compute_answer"](eval_df)

    # send the question to the agent
    response = query_agent(eval_agent, question)

    # check if the response matches the expected answer
    is_correct = check_match(
        response=response,
        expected=expected,
        match_type=match_type,
        tolerance=tolerance,
    )

    # build a clear failure message
    # truncate long responses so the pytest output stays readable
    short_response = response[:300]
    if len(response) > 300:
        short_response += "..."

    assert is_correct, (
        f"\n"
        f"EVALUATION FAILED: {q_id} ({category})\n"
        f"Question:  {question}\n"
        f"Expected:  {expected}\n"
        f"Response:  {short_response}\n"
        f"Match type: {match_type}\n"
    )
