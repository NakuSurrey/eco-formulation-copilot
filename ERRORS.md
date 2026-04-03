# ERRORS.md — Eco-Formulation Copilot

> Running log of every error encountered during the build.
> Each entry records: what broke, why it broke, how it was fixed, and the prevention rule.

---

## Error 001 — Pandas converts "None" string to NaN (Phase 2)

**What broke:** The `Enzyme_Type` column showed `NaN` (missing data) for rows where the enzyme value was the string `"None"`.

**Why it broke:** Pandas has a built-in list of strings it automatically converts to `NaN` when reading a CSV. The word `"None"` is on that list. So `pd.read_csv()` saw `None` in the CSV and treated it as missing data instead of a category label.

**How it was fixed:** Changed the string `"None"` to `"No Enzyme"` in `generate_data.py`. This is a descriptive label that Pandas does not auto-convert.

**Prevention rule:** Never use the exact strings `"None"`, `"NA"`, `"null"`, or `"NaN"` as category values in CSV data. Use descriptive labels instead. Alternatively, pass `keep_default_na=False` to `pd.read_csv()`.

---

## Error 002 — AgentType import path moved in LangChain v1.2.14 (Phase 3)

**What broke:** `from langchain.agents.agent_types import AgentType` raised `ModuleNotFoundError`. The test suite could not even collect tests because the import in `agent.py` failed at load time.

**Why it broke:** LangChain v1.2.14 reorganised its internal modules. The `AgentType` enum class was moved from `langchain.agents.agent_types` to `langchain_classic.agents.agent_types`. The old path no longer exists.

**How it was fixed:** Removed the `AgentType` import entirely. Passed the plain string `"zero-shot-react-description"` directly to `create_pandas_dataframe_agent()` instead of using `AgentType.ZERO_SHOT_REACT_DESCRIPTION`. The function accepts both — strings are immune to internal module reshuffling.

**Prevention rule:** When a LangChain function accepts both an enum and a plain string for the same parameter, always use the plain string. Strings do not break when internal modules are reorganised between library versions.

---

## Error 003 — Unused import causes flake8 F401 failure (Phase 5)

**What broke:** Running `flake8` on the codebase returned `F401 'pandas as pd' imported but unused` in `tests/test_agent.py` line 17. This would cause the CI pipeline to fail with a red X on every push.

**Why it broke:** During Phase 3, `import pandas as pd` was added to the test file but was never actually used in any test. The tests reference `SYSTEM_PROMPT` and `query_agent` (imported from `src.agent`), but no test ever calls `pd.DataFrame()` or any other Pandas function directly.

**How it was fixed:** Removed `import pandas as pd` from line 17 of `tests/test_agent.py`. No test depends on it, so nothing else changed.

**Prevention rule:** Always run `flake8` locally before committing. The CI pipeline (`.github/workflows/ci.yml`) now catches this automatically on every push, but catching it locally is faster and avoids a red X on the repo.
