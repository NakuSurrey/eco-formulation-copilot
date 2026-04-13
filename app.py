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

from src.config import APP_TITLE
from src.data_loader import load_data
from src.charts import (
    build_scatter_chart,
    build_bar_chart,
    build_surfactant_pie_chart,
)


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
# Main Application
# ============================================================
def main() -> None:
    """
    Builds and renders the entire Streamlit application.

    Layout:
    ┌─────────────────────────────────────────────┐
    │  Title + Subtitle                           │
    ├─────────────────────────────────────────────┤
    │  Key Metrics (4 columns)                    │
    ├──────────────────────┬──────────────────────┤
    │  Scatter Chart       │  Bar Chart           │
    ├──────────────────────┴──────────────────────┤
    │  Pie Chart (centred)                        │
    ├─────────────────────────────────────────────┤
    │  Example Questions (3 buttons)              │
    ├─────────────────────────────────────────────┤
    │  Chat History                               │
    ├─────────────────────────────────────────────┤
    │  Chat Input Box                             │
    └─────────────────────────────────────────────┘
    """

    # --- Header ---
    st.title(f"🧪 {APP_TITLE}")
    st.markdown(
        "An **Agentic AI** proof-of-concept for P&G Newcastle R&D. "
        "Ask questions about chemical formulations in plain English."
    )
    st.divider()

    # --- Load Data ---
    try:
        df = get_data()
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

    # --- Key Metrics Row ---
    # These 4 numbers give the scientist an instant snapshot
    # of the dataset before they look at any charts.
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
    # Two charts side by side, then one below
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

    # Pie chart centred below
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
    # These pre-written buttons let the recruiter test the app
    # instantly without thinking of what to type.
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
    # st.session_state is Streamlit's way of storing data that
    # persists across page refreshes. Without it, the chat history
    # would disappear every time the user sends a message.
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

    # Use prefill if an example button was clicked
    if prefill:
        user_input = prefill

    # --- Process the Question ---
    if user_input:
        # Show the user's message
        st.session_state["messages"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get the agent's answer (Trait #191 — Loading-state handled)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Querying formulation database..."):
                answer = query_agent(agent, user_input)
            st.markdown(answer)

        # Save the answer to chat history
        st.session_state["messages"].append(
            {"role": "assistant", "content": answer}
        )


if __name__ == "__main__":
    main()
