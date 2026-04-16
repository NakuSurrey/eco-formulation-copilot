"""
Standalone evaluation script for the Eco-Formulation Copilot agent.

This script runs all 20 evaluation questions against the live agent
and prints a full accuracy report to the terminal.

HOW TO RUN:
    cd eco-formulation-copilot
    python -m eval.run_eval

WHAT IT DOES — step by step:
    Step 1 → Load the formulations CSV into a DataFrame
    Step 2 → Create the LangChain agent (needs GOOGLE_API_KEY in .env)
    Step 3 → For each of the 20 questions:
             a) Compute the correct answer from the DataFrame
             b) Send the question to the agent
             c) Check if the agent's response matches the correct answer
             d) Log PASS or FAIL
    Step 4 → Print a summary report with total accuracy percentage

OUTPUT FORMAT:
    ============================================
    ECO-FORMULATION COPILOT — AGENT EVALUATION
    ============================================

    [1/20] PASS — count_bio_above_90 (counting)
    [2/20] FAIL — avg_cost (aggregation)
           Expected: 2.53
           Got: "The average cost is approximately £2.50"
    ...

    ============================================
    RESULTS: 17/20 PASSED (85.0%)
    ============================================

    CATEGORY BREAKDOWN:
    counting:    4/4 (100.0%)
    aggregation: 3/4 (75.0%)
    ...

REQUIRES:
    - GOOGLE_API_KEY set in .env (or environment variable)
    - data/formulations.csv to exist
    - All dependencies from requirements.txt installed
"""

import sys
import time

from src.data_loader import load_data
from src.agent import create_agent, query_agent
from eval.questions import EVAL_QUESTIONS
from eval.matcher import check_match
from eval.cache import save_result_json


def run_evaluation() -> dict:
    """
    Runs the full 20-question evaluation and returns results.

    Returns a dict with:
        - "results": list of per-question result dicts
        - "total": total number of questions
        - "passed": number that passed
        - "failed": number that failed
        - "accuracy": percentage as a float (e.g., 85.0)
        - "by_category": dict of category → {passed, total}
        - "duration": total time in seconds
    """
    print("=" * 52)
    print("ECO-FORMULATION COPILOT — AGENT EVALUATION")
    print("=" * 52)
    print()

    # Step 1: Load the data
    print("Loading formulations data...")
    df = load_data()
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns.")
    print()

    # Step 2: Create the agent
    print("Creating LangChain agent...")
    agent = create_agent(df)
    print("  Agent ready.")
    print()

    # Step 3: Run each question
    results = []
    category_stats: dict[str, dict[str, int]] = {}
    start_time = time.time()

    total = len(EVAL_QUESTIONS)

    for i, q in enumerate(EVAL_QUESTIONS, start=1):
        q_id = q["id"]
        category = q["category"]
        question = q["question"]
        match_type = q["match_type"]
        tolerance = q.get("tolerance", 0.05)

        # compute the correct answer from the DataFrame
        expected = q["compute_answer"](df)

        # send the question to the agent
        print(f"[{i}/{total}] Asking: {q_id} ({category})")
        agent_response = query_agent(agent, question)

        # check if the response matches
        passed = check_match(
            response=agent_response,
            expected=expected,
            match_type=match_type,
            tolerance=tolerance,
        )

        # record the result
        result = {
            "id": q_id,
            "category": category,
            "question": question,
            "expected": expected,
            "response": agent_response,
            "match_type": match_type,
            "passed": passed,
        }
        results.append(result)

        # update category stats
        if category not in category_stats:
            category_stats[category] = {"passed": 0, "total": 0}
        category_stats[category]["total"] += 1
        if passed:
            category_stats[category]["passed"] += 1

        # print the result
        status = "PASS" if passed else "FAIL"
        print(f"         {status} — {q_id}")
        if not passed:
            print(f"         Expected: {expected}")
            # truncate long responses for readability
            short_response = agent_response[:200]
            if len(agent_response) > 200:
                short_response += "..."
            print(f"         Got: \"{short_response}\"")
        print()

    # Step 4: Print the summary
    end_time = time.time()
    duration = round(end_time - start_time, 1)

    passed_count = sum(1 for r in results if r["passed"])
    failed_count = total - passed_count
    accuracy = round((passed_count / total) * 100, 1)

    print("=" * 52)
    print(f"RESULTS: {passed_count}/{total} PASSED ({accuracy}%)")
    print(f"TIME: {duration} seconds")
    print("=" * 52)
    print()

    print("CATEGORY BREAKDOWN:")
    # keep the order: counting, aggregation, filtering,
    # ranking, grouping, lookup
    category_order = [
        "counting", "aggregation", "filtering",
        "ranking", "grouping", "lookup",
    ]
    for cat in category_order:
        if cat in category_stats:
            stats = category_stats[cat]
            cat_acc = round(
                (stats["passed"] / stats["total"]) * 100, 1
            )
            print(
                f"  {cat:14s}: "
                f"{stats['passed']}/{stats['total']} "
                f"({cat_acc}%)"
            )
    print()

    # print failed questions for quick debugging
    failed = [r for r in results if not r["passed"]]
    if failed:
        print("FAILED QUESTIONS:")
        for r in failed:
            print(f"  - {r['id']}: expected {r['expected']}")
        print()

    return {
        "results": results,
        "total": total,
        "passed": passed_count,
        "failed": failed_count,
        "accuracy": accuracy,
        "by_category": category_stats,
        "duration": duration,
    }


if __name__ == "__main__":
    try:
        summary = run_evaluation()

        # write the result to eval/last_run.json — this is what the
        # Streamlit Evaluation tab reads on page-load
        cache_path = save_result_json(summary)
        print(f"CACHE: wrote {cache_path}")
        print()

        # exit with code 1 if accuracy is below 70%
        # this lets CI/CD treat low accuracy as a failure
        if summary["accuracy"] < 70.0:
            print(
                f"WARN: Accuracy {summary['accuracy']}% "
                f"is below the 70% threshold."
            )
            sys.exit(1)
        sys.exit(0)
    except ValueError as e:
        print(f"ERROR: {e}")
        print("Make sure GOOGLE_API_KEY is set in your .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {type(e).__name__}: {e}")
        sys.exit(1)
