"""
Eco-Formulation Copilot — Streamlit Application

This is the ENTRY POINT of the entire application.
Run it with: streamlit run app.py

WHAT THIS FILE DOES:
It builds a single-page web application with two sections:
1. DASHBOARD (top)  — Interactive Plotly charts showing cost, biodegradability,
                       cleaning efficacy, and surfactant distribution
2. CHAT (bottom)    — A chat interface where the scientist types plain English
                       questions and the AI agent returns data-driven answers

HOW ALL THE PIECES CONNECT:
    app.py (this file)
        ↓ imports
    config.py      → APP_TITLE, validate_config()
    data_loader.py → load_data() → returns the DataFrame
    agent.py       → create_agent(df), query_agent(agent, question)
    charts.py      → build_scatter_chart(df), build_bar_chart(df), build_surfactant_pie_chart(df)
        ↓ renders
    Streamlit UI   → Charts + Chat displayed in the browser
"""

import streamlit as st
from datetime import datetime, timezone

from src.config import APP_TITLE
from src.data_loader import load_data
from src.charts import (
    build_scatter_chart,
    build_bar_chart,
    build_surfactant_pie_chart,
)
from eval.cache import load_result_json


# ============================================================
# Page Configuration
# ============================================================
# This MUST be the first Streamlit command in the script.
# It sets the browser tab title, the page icon, and the layout.
# "wide" layout uses the full browser width instead of a narrow column.
#
# IMPORTANT: the agent import is placed AFTER this line because
# langchain-google-genai v4+ triggers a Streamlit command during
# its import chain. If imported before set_page_config(), Streamlit
# crashes. Moving it here fixes that.
# ============================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧪",
    layout="wide",
)

# --- Lazy import: agent module loaded AFTER set_page_config ---
from src.agent import create_agent, query_agent  # noqa: E402


# ============================================================
# Data Loading (cached)
# ============================================================
# @st.cache_data tells Streamlit: "Run this function once, store
# the result in memory, and reuse it on every page refresh."
# Without this, the CSV would be re-read every time the user
# sends a chat message — wasting time and memory.
# ============================================================
@st.cache_data
def get_data():
    """Load and cache the formulations DataFrame."""
    return load_data()


# ============================================================
# Agent Initialisation (cached)
# ============================================================
# @st.cache_resource is similar to @st.cache_data but for objects
# that should NOT be serialised (like database connections or
# AI agents). The agent is created once and reused across all
# chat interactions in the same session.
# ============================================================
@st.cache_resource
def get_agent(_df):
    """Create and cache the LangChain DataFrame Agent."""
    return create_agent(_df)


# ============================================================
# Evaluation Tab Helpers
# ============================================================
# These functions build the "Evaluation" tab. Split out of main()
# to keep the dashboard code readable and to allow the modal
# dialog to be defined at module level (Streamlit requirement).
# ============================================================

def _friendly_time(iso_timestamp: str) -> str:
    """
    Converts an ISO 8601 timestamp into "N hours ago" / "N days ago"
    so the recruiter sees when the last evaluation ran, not a raw date.
    """
    try:
        # parse the ISO string — keep timezone aware
        ts = datetime.fromisoformat(iso_timestamp)
        now = datetime.now(timezone.utc)
        delta = now - ts
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return "just now"
        if seconds < 3600:
            return f"{seconds // 60} min ago"
        if seconds < 86400:
            return f"{seconds // 3600} h ago"
        return f"{seconds // 86400} d ago"
    except (ValueError, TypeError):
        # falls back to the raw string if parsing breaks
        return iso_timestamp


def _category_colour(accuracy_pct: float) -> str:
    """Returns a hex colour for a category accuracy row."""
    if accuracy_pct >= 90:
        return "#3fb950"        # green — passing well
    if accuracy_pct >= 70:
        return "#d29922"        # amber — partial
    return "#f85149"            # red — failing


def _run_live_eval() -> None:
    """
    Runs the 20-question evaluation live against the agent, saves the
    result to eval/last_run.json, then triggers a rerun so the tab
    picks up the new numbers.

    Isolated here so both the confirm modal and a fallback button
    can call it without duplicating code.
    """
    # imports are local — these are heavy modules, only load on click
    from eval.run_eval import run_evaluation
    from eval.cache import save_result_json

    try:
        with st.spinner("Running 20 real agent queries... ~30-60 seconds"):
            summary = run_evaluation()
            save_result_json(summary)
        st.success(
            f"Evaluation complete — {summary['accuracy']}% accuracy "
            f"({summary['passed']}/{summary['total']} passed)"
        )
        st.rerun()
    except ValueError as e:
        st.error(f"Evaluation failed: {e}")
        st.info(
            "Check GOOGLE_API_KEY is set in .env and the quota is not "
            "exhausted."
        )
    except Exception as e:  # noqa: BLE001 — UI must not crash on any error
        st.error(f"Unexpected error: {type(e).__name__}: {e}")


@st.dialog("Run live evaluation?")
def _confirm_live_eval_dialog() -> None:
    """
    Confirmation modal shown when the user clicks 'Run evaluation now'.

    Streamlit requires dialog functions to live at module level, not
    inside another function — otherwise the dialog re-registers on
    every rerun and breaks.
    """
    st.markdown(
        "This runs **20 real Gemini API calls** against the live agent "
        "and takes around 30-60 seconds."
    )
    st.markdown(
        "It uses the free-tier quota attached to the `GOOGLE_API_KEY` "
        "in the server's `.env`. No billing is incurred."
    )
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button(
            "Run evaluation",
            type="primary",
            use_container_width=True,
        ):
            _run_live_eval()


def _render_category_table(by_category: dict) -> None:
    """
    Renders the 6-row category breakdown as a styled table.
    Uses the fixed order: counting, aggregation, filtering,
    ranking, grouping, lookup — matching the run_eval output.
    """
    category_order = [
        "counting", "aggregation", "filtering",
        "ranking", "grouping", "lookup",
    ]

    # build plain-Python rows for display — no pandas import needed
    rows = []
    for cat in category_order:
        stats = by_category.get(cat)
        if not stats:
            continue
        passed = stats.get("passed", 0)
        total = stats.get("total", 0)
        acc = round((passed / total) * 100, 1) if total else 0.0
        rows.append({
            "Category": cat,
            "Passed / Total": f"{passed} / {total}",
            "Accuracy": f"{acc:.1f}%",
            "_pct": acc,   # hidden — used for colour only
        })

    # render as a coloured unordered list — cleaner than st.dataframe
    # for a 6-row summary
    for row in rows:
        colour = _category_colour(row["_pct"])
        st.markdown(
            f"""
            <div style='
                display: flex;
                justify-content: space-between;
                padding: 8px 14px;
                margin-bottom: 6px;
                background-color: rgba(48, 54, 61, 0.4);
                border-left: 4px solid {colour};
                border-radius: 4px;
                font-family: monospace;
            '>
                <span style='min-width: 140px;'>{row['Category']}</span>
                <span style='min-width: 100px;'>{row['Passed / Total']}</span>
                <span style='color: {colour}; font-weight: bold;'>
                    {row['Accuracy']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_per_question_table(results: list[dict]) -> None:
    """
    Renders every question from the cached run with expandable rows
    so the recruiter can drill into any specific question.
    """
    for r in results:
        status = "✅" if r.get("passed") else "❌"
        label = (
            f"{status}  [{r.get('category')}]  "
            f"{r.get('id')}  —  {r.get('question')}"
        )
        with st.expander(label):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Expected (ground truth)**")
                st.code(str(r.get("expected")), language="text")
            with col_b:
                st.markdown("**Agent response**")
                st.code(str(r.get("response"))[:600], language="text")
            st.caption(
                f"Match type: `{r.get('match_type')}` — "
                f"{'passed' if r.get('passed') else 'failed'}"
            )


def render_evaluation_tab(df) -> None:
    """
    Builds the full Evaluation tab.

    Layout:
        1. subheader + intro
        2. 4-metric row (accuracy, passed, failed, last-run-ago)
        3. category breakdown (6 coloured rows)
        4. "Run evaluation now" button (opens confirm dialog)
        5. expandable per-question breakdown
        6. footer — link to eval/ source files on GitHub
    """
    st.subheader("✅ Agent Accuracy Evaluation")
    st.caption(
        "The agent is not just tested for code-level behaviour — it is "
        "also measured against 20 real questions with ground-truth "
        "answers computed from the dataset. This tab shows the last "
        "evaluation run."
    )

    cached = load_result_json()

    if cached is None:
        # fallback — no cached JSON yet (first deploy, or file deleted)
        st.warning(
            "No cached evaluation found yet. Click below to run one now."
        )
        if st.button(
            "▶ Run evaluation now",
            type="primary",
            use_container_width=True,
        ):
            _confirm_live_eval_dialog()
        return

    # --- 4-metric row ---
    acc_col, pass_col, fail_col, time_col = st.columns(4)
    acc_col.metric("Accuracy", f"{cached['accuracy']:.1f}%")
    pass_col.metric(
        "Passed",
        f"{cached['passed']} / {cached['total']}",
    )
    fail_col.metric("Failed", cached["failed"])
    time_col.metric(
        "Last run",
        _friendly_time(cached.get("timestamp", "")),
    )

    # --- small meta row under the metrics ---
    st.caption(
        f"model: `{cached.get('model', '?')}` ┃ "
        f"commit: `{cached.get('commit') or '—'}` ┃ "
        f"duration: {cached.get('duration', 0)} s"
    )

    st.divider()

    # --- category breakdown ---
    st.markdown("### Category breakdown")
    _render_category_table(cached.get("by_category", {}))

    st.divider()

    # --- run live button ---
    st.markdown("### Run a fresh evaluation")
    st.caption(
        "Re-runs the 20 questions against the live agent and updates "
        "this tab. Uses Gemini free-tier API quota. Takes 30-60 seconds."
    )
    if st.button(
        "▶ Run evaluation now",
        type="primary",
        use_container_width=False,
    ):
        _confirm_live_eval_dialog()

    st.divider()

    # --- per-question breakdown ---
    st.markdown("### Per-question breakdown")
    st.caption(
        "Click any row to see the expected answer (computed from the "
        "DataFrame) and the agent's response."
    )
    _render_per_question_table(cached.get("results", []))


# ============================================================
# Main Application
# ============================================================
def main() -> None:
    """
    Builds and renders the entire Streamlit application.

    Top-level layout:
        ┌──────────────────────────────────────────┐
        │  Title + Subtitle (always visible)       │
        ├──────────────────────────────────────────┤
        │  [📊 Dashboard]  [✅ Evaluation]          │  <- st.tabs
        ├──────────────────────────────────────────┤
        │  active tab content                      │
        └──────────────────────────────────────────┘

    Dashboard tab = original UI (metrics, charts, chat).
    Evaluation tab = render_evaluation_tab() — cached eval result + live re-run.
    """

    # --- Header stays OUTSIDE the tabs so both tabs share it ---
    st.title(f"🧪 {APP_TITLE}")
    st.markdown(
        "An **Agentic AI** proof-of-concept for P&G Newcastle R&D. "
        "Ask questions about chemical formulations in plain English."
    )
    st.divider()

    # --- Load Data ONCE — shared by both tabs ---
    try:
        df = get_data()
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

    # --- Build the two-tab strip ---
    tab_dash, tab_eval = st.tabs(["📊 Dashboard", "✅ Evaluation"])

    # ============================================================
    # TAB 1 — Dashboard (charts + chat)
    # ============================================================
    with tab_dash:

        # --- Key Metrics Row ---
        # these 4 numbers give the scientist an instant snapshot
        # of the dataset before they look at any charts
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Formulas", len(df))
        col2.metric(
            "Avg Biodegradability",
            f"{df['Biodegradability_Score'].mean():.1f}/100"
        )
        col3.metric(
            "Avg Cleaning Efficacy",
            f"{df['Cleaning_Efficacy_Score'].mean():.1f}/100"
        )
        col4.metric(
            "Avg Cost/Litre",
            f"£{df['Cost_Per_Litre_GBP'].mean():.2f}"
        )

        st.divider()

        # --- Dashboard Charts ---
        # two charts side by side, then one centred below
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                build_scatter_chart(df),
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                build_bar_chart(df),
                use_container_width=True,
            )

        # pie chart centred below
        pie_col1, pie_col2, pie_col3 = st.columns([1, 2, 1])
        with pie_col2:
            st.plotly_chart(
                build_surfactant_pie_chart(df),
                use_container_width=True,
            )

        st.divider()

        # --- AI Chat Section ---
        st.subheader("💬 Ask the R&D Assistant")
        st.caption(
            "Type a question in plain English. The AI agent will write "
            "Pandas code behind the scenes, query the dataset, and return "
            "the answer."
        )

        # --- Example Questions (Trait #182 — Intuitive) ---
        # pre-written buttons let the recruiter test the app
        # instantly without thinking of what to type
        example_col1, example_col2, example_col3 = st.columns(3)

        with example_col1:
            if st.button(
                "🔬 Top 5 biodegradable formulas under £2",
                use_container_width=True,
            ):
                st.session_state["prefill"] = (
                    "Show me the top 5 formulas with the highest "
                    "biodegradability score that cost less than £2 per litre"
                )

        with example_col2:
            if st.button(
                "📊 Average cost by surfactant type",
                use_container_width=True,
            ):
                st.session_state["prefill"] = (
                    "What is the average cost per litre for each surfactant type?"
                )

        with example_col3:
            if st.button(
                "🧬 Lowest toxicity formulas",
                use_container_width=True,
            ):
                st.session_state["prefill"] = (
                    "Show me the 5 formulas with the lowest toxicity level, "
                    "including their biodegradability and cleaning scores"
                )

        # --- Initialise Chat History ---
        # st.session_state persists data across page refreshes
        # without it, chat history would reset on every message
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # --- Initialise the Agent ---
        try:
            agent = get_agent(df)
        except ValueError as e:
            st.error(f"Agent setup failed: {e}")
            st.info(
                "Make sure your GOOGLE_API_KEY is set in the .env file. "
                "Get a free key at: https://aistudio.google.com/apikey"
            )
            st.stop()

        # --- Display Chat History ---
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # --- Handle Pre-filled Questions from Example Buttons ---
        prefill = st.session_state.pop("prefill", None)

        # --- Chat Input ---
        user_input = st.chat_input(
            "Ask about formulations (e.g., 'Which polymers have the best cleaning score?')"
        )

        # use prefill if an example button was clicked
        if prefill:
            user_input = prefill

        # --- Process the Question ---
        if user_input:
            # show the user's message
            st.session_state["messages"].append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)

            # get the agent's answer (Trait #191 — Loading-state handled)
            with st.chat_message("assistant"):
                with st.spinner("🔍 Querying formulation database..."):
                    answer = query_agent(agent, user_input)
                st.markdown(answer)

            # save the answer to chat history
            st.session_state["messages"].append(
                {"role": "assistant", "content": answer}
            )

    # ============================================================
    # TAB 2 — Evaluation (cached JSON + live re-run button)
    # ============================================================
    with tab_eval:
        render_evaluation_tab(df)


if __name__ == "__main__":
    main()
