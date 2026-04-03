# PHASE 3 REFERENCE — The Agentic AI Brain

## Files Created

| File | Purpose |
|------|---------|
| `src/agent.py` | Creates the LangChain DataFrame Agent powered by Google Gemini. Contains two functions: `create_agent()` initialises the LLM and connects it to the DataFrame. `query_agent()` sends a user question, gets back an answer string. All errors are caught gracefully. |
| `tests/test_agent.py` | 7 tests covering: system prompt content validation (role, anti-hallucination, column descriptions), empty input handling, and error handling when the agent is None. Tests run without a real API key. |

## Key Decisions

1. **`"zero-shot-react-description"` as a string** instead of `AgentType.ZERO_SHOT_REACT_DESCRIPTION` enum — the enum import path broke in LangChain v1.2.14 (see Error 002). Using the plain string is immune to internal module reorganisation.
2. **`temperature=0`** on the Gemini LLM — for data queries we want deterministic, exact answers. Temperature 0 means the LLM picks the most likely response every time instead of being creative.
3. **Strict system prompt (SYSTEM_PROMPT)** — implements Trait #202 (Prompt-engineered) and Trait #203 (Anti-hallucinatory). The LLM is told to only answer from the dataset and to explicitly say "Data not available" if it cannot find the answer.
4. **`allow_dangerous_code=True`** — LangChain requires this flag because the agent executes Python code. The risk is mitigated by the strict system prompt which limits what the agent can do.
5. **Tests skip live API calls** — the `skip_no_key` marker skips tests that need a real Google API key. This means GitHub Actions CI/CD can run all tests without exposing secrets.

## Connection to Previous Phases

- Imports `GOOGLE_API_KEY`, `GEMINI_MODEL`, `validate_config` from `src/config.py` (Phase 1)
- Uses the DataFrame from `data_loader.py` (Phase 2) — passed into `create_agent(df)`

## Connection to Next Phases

- **Phase 4 (Dashboard)** will import `create_agent()` and `query_agent()` to process chat messages from the Streamlit UI.

## Errors Encountered

- **Error 002:** `AgentType` import path moved in LangChain v1.2.14. Fixed by using the plain string `"zero-shot-react-description"` instead. See ERRORS.md for full details.
