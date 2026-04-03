# PHASE 4 REFERENCE — Dashboard & Front-End

## Files Created

| File | Purpose |
|------|---------|
| `src/charts.py` | Contains 3 functions that each take the DataFrame and return a Plotly figure: `build_scatter_chart()` (Cost vs Biodegradability), `build_bar_chart()` (Top 10 by Cleaning Efficacy), `build_surfactant_pie_chart()` (Surfactant distribution). |
| `app.py` | The Streamlit entry point. Builds the entire single-page web app: title, 4 key metrics, 3 interactive charts, 3 example question buttons, and a chat interface connected to the LangChain agent. Run with `streamlit run app.py`. |

## Key Decisions

1. **Plotly over Matplotlib** — Plotly charts are interactive (hover, zoom, filter). Matplotlib produces static images. Interactive charts mimic Power BI, which is what P&G uses.
2. **`@st.cache_data` for the DataFrame** — Loads the CSV once and reuses it across every page refresh. Without caching, the CSV would re-read on every chat message.
3. **`@st.cache_resource` for the Agent** — Creates the LLM connection once and reuses it. Without caching, a new Gemini connection would be established on every interaction.
4. **3 example question buttons** (Trait #182 Intuitive) — The recruiter does not have to think of what to type. They click a button and the app demonstrates itself instantly.
5. **`st.spinner()` wrapper** (Trait #191 Loading-state handled) — Shows "Querying formulation database..." while the LLM processes. Without this, the app appears frozen for 2-3 seconds.
6. **`st.session_state["messages"]`** for chat history — Streamlit re-runs the entire script on every interaction. Session state preserves the chat history across re-runs so previous messages do not disappear.
7. **3 charts, not 1** — The scatter plot shows cost-vs-sustainability tradeoff. The bar chart shows top performers. The pie chart shows dataset balance. Together they give a complete picture without being overwhelming.

## Connection to Previous Phases

- Imports `APP_TITLE` from `src/config.py` (Phase 1)
- Imports `load_data()` from `src/data_loader.py` (Phase 2) — provides the DataFrame
- Imports `create_agent()` and `query_agent()` from `src/agent.py` (Phase 3) — powers the chat

## Connection to Next Phases

- **Phase 5 (Docker)** will containerise this app so it runs identically anywhere.
- **Phase 6 (Deploy)** will put this on Streamlit Community Cloud so the recruiter has a live URL.

## Errors Encountered

None in this phase.
