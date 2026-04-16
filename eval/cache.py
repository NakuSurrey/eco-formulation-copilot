"""
JSON cache helpers for the evaluation framework.

Keeps a single source of truth — eval/last_run.json — that stores the
latest evaluation result. The Streamlit Evaluation tab reads this file
on page-load so the recruiter sees the 90% result without burning API
quota.

WHAT THIS MODULE DOES
    save_result_json  → writes a summary dict (from run_evaluation)
                        to disk as a pretty-printed JSON file.
    load_result_json  → reads the JSON back as a dict.
                        returns None if the file does not exist.

WHY IT EXISTS
    Streamlit runs the app on every page-load. Without a cache, the
    Evaluation tab would either be empty (if the API is not called)
    or burn quota on every refresh (if it is). A JSON cache solves
    both — read-only by default, explicit "Run now" button for live
    updates.

HOW TO USE
    from eval.cache import save_result_json, load_result_json

    # after a live run
    save_result_json(summary_dict)

    # on page load in Streamlit
    cached = load_result_json()
    if cached is None:
        st.warning("No cached evaluation result found.")
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

# file lives next to this module, inside eval/
DEFAULT_CACHE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "last_run.json",
)


def save_result_json(
    summary: dict[str, Any],
    path: Optional[str] = None,
    model: Optional[str] = None,
    commit: Optional[str] = None,
) -> str:
    """
    Saves an evaluation summary dict to disk as JSON.

    Args:
        summary: the dict returned by run_evaluation() in run_eval.py
        path:    override path (default: eval/last_run.json)
        model:   model name to record (default: reads MODEL_NAME from env)
        commit:  git commit hash (default: tries GITHUB_SHA then leaves blank)

    Returns:
        absolute path of the file that was written.

    The saved JSON always includes a `timestamp` (ISO 8601 UTC) so the
    Streamlit tab can show "last run: N hours ago".
    """
    if path is None:
        path = DEFAULT_CACHE_PATH

    # default model name — same var the rest of the app reads
    if model is None:
        model = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

    # default commit — CI sets GITHUB_SHA, local runs leave it blank
    if commit is None:
        commit = os.environ.get("GITHUB_SHA", "")

    # trim the per-question response to keep the JSON file small
    # full text lives in CI logs; the tab only needs a short preview
    results_trimmed = []
    for r in summary.get("results", []):
        response_text = str(r.get("response", ""))
        if len(response_text) > 500:
            response_text = response_text[:500] + "..."
        results_trimmed.append({
            "id": r.get("id"),
            "category": r.get("category"),
            "question": r.get("question"),
            "expected": _json_safe(r.get("expected")),
            "response": response_text,
            "match_type": r.get("match_type"),
            "passed": bool(r.get("passed")),
        })

    out = {
        "timestamp": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "model": model,
        "commit": commit,
        "total": int(summary.get("total", 0)),
        "passed": int(summary.get("passed", 0)),
        "failed": int(summary.get("failed", 0)),
        "accuracy": float(summary.get("accuracy", 0.0)),
        "duration": float(summary.get("duration", 0.0)),
        "by_category": summary.get("by_category", {}),
        "results": results_trimmed,
    }

    # create parent dir if missing — safety for custom paths
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)

    return os.path.abspath(path)


def load_result_json(
    path: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """
    Loads the cached evaluation summary from disk.

    Returns None if the file does not exist yet — caller must handle
    this case in the UI (e.g., show "Run evaluation now" prompt).
    """
    if path is None:
        path = DEFAULT_CACHE_PATH

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _json_safe(value: Any) -> Any:
    """
    Converts non-JSON types (int64, float64, DataFrame, Series) into
    plain Python types so json.dump does not crash.
    """
    # pandas types — check duck-typed to avoid importing pandas here
    if hasattr(value, "to_dict"):
        # DataFrame / Series — reduce to a list of rows / list of values
        try:
            return value.to_dict(orient="records")
        except TypeError:
            return value.to_dict()

    if hasattr(value, "tolist"):
        # numpy array / numpy scalar
        return value.tolist()

    if hasattr(value, "item"):
        # numpy int64 / float64 scalar
        try:
            return value.item()
        except (ValueError, AttributeError):
            pass

    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]

    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}

    # plain Python types — pass through
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    # fall back to string representation
    return str(value)
