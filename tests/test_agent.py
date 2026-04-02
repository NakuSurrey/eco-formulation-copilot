"""
Tests for the agent module.

These tests verify that:
1. The agent module imports correctly
2. The system prompt contains critical safety instructions
3. The query_agent function handles empty input gracefully
4. The query_agent function handles LLM errors gracefully

NOTE: Tests that require a real Google API key are skipped
automatically when the key is not present. This lets the tests
run in CI/CD (GitHub Actions) without exposing secrets.
"""

import os
import pytest
import pandas as pd

from src.agent import SYSTEM_PROMPT, query_agent


# ============================================================
# Helper: Check if the Google API key is available
# ============================================================
# If the key is not set, tests that need a live LLM connection
# are skipped with a clear message.
# ============================================================
HAS_API_KEY = bool(os.getenv("GOOGLE_API_KEY", ""))
skip_no_key = pytest.mark.skipif(
    not HAS_API_KEY,
    reason="GOOGLE_API_KEY not set — skipping live agent tests"
)


class TestSystemPrompt:
    """Tests that the system prompt contains critical instructions."""

    def test_prompt_contains_role(self) -> None:
        """The prompt tells the LLM it is an R&D Assistant."""
        assert "Research & Development Assistant" in SYSTEM_PROMPT

    def test_prompt_contains_anti_hallucination(self) -> None:
        """The prompt includes an anti-hallucination rule."""
        assert "Data not available" in SYSTEM_PROMPT

    def test_prompt_contains_column_descriptions(self) -> None:
        """The prompt describes the dataset columns so the LLM knows what it has."""
        assert "Formula_ID" in SYSTEM_PROMPT
        assert "Biodegradability_Score" in SYSTEM_PROMPT
        assert "Cost_Per_Litre_GBP" in SYSTEM_PROMPT

    def test_prompt_forbids_invention(self) -> None:
        """The prompt explicitly forbids the LLM from inventing data."""
        assert "Do NOT invent" in SYSTEM_PROMPT


class TestQueryAgentErrorHandling:
    """Tests that query_agent handles bad input without crashing."""

    def test_empty_string_returns_message(self) -> None:
        """An empty question returns a polite prompt, not a crash."""
        # We pass None as the agent because the guard should
        # catch the empty string BEFORE touching the agent
        result = query_agent(agent=None, user_question="")
        assert "Please enter a question" in result

    def test_whitespace_only_returns_message(self) -> None:
        """A whitespace-only question returns a polite prompt."""
        result = query_agent(agent=None, user_question="   ")
        assert "Please enter a question" in result

    def test_none_agent_with_valid_question_returns_error(self) -> None:
        """If the agent is None but the question is valid,
        the function catches the error instead of crashing."""
        result = query_agent(agent=None, user_question="Show top 5 formulas")
        # Should return an error message string, not raise an exception
        assert isinstance(result, str)
        assert "error" in result.lower() or "Error" in result
