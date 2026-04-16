"""
Evaluation package for the Eco-Formulation Copilot.

This package contains the agent evaluation framework — a systematic
way to test whether the AI agent gives correct answers.

WHAT IT DOES:
    Runs 20 pre-defined questions against the agent, computes the
    correct answer from the real DataFrame using Pandas, then checks
    if the agent's response matches the correct answer.

WHY IT EXISTS:
    Without evaluation, the agent might give wrong answers and
    nobody would know. This package catches accuracy problems
    before they reach the user.

MODULES:
    questions.py — 20 evaluation questions with compute functions
    matcher.py  — hybrid matching logic (numeric + keyword)
    run_eval.py — standalone script that prints an accuracy report
"""
