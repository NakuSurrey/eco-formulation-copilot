# PHASE 1 REFERENCE — Project Skeleton & Configuration

## Files Created

| File | Purpose |
|------|---------|
| `requirements.txt` | Lists all Python dependencies with pinned versions. Anyone can run `pip install -r requirements.txt` to get the exact same environment. |
| `.env.example` | Template showing what environment variables are needed. Contains placeholder values, not real keys. Safe to commit to GitHub. |
| `.gitignore` | Tells Git to ignore secrets (.env), cache files (__pycache__), IDE configs, and OS junk. Prevents accidental exposure. |
| `src/__init__.py` | Makes `src/` a Python package. Without this file, Python cannot import modules from the `src` folder. |
| `src/config.py` | The single source of truth for all app settings. Loads `GOOGLE_API_KEY` from `.env`, defines paths, and provides a `validate_config()` function that stops the app early with a clear error if the key is missing. |
| `tests/__init__.py` | Makes `tests/` a Python package. Without this file, pytest cannot discover test files. |
| `ERRORS.md` | Running error log (empty so far). Will track every error, its cause, fix, and prevention rule. |

## Key Decisions

1. **Google Gemini 1.5 Flash** chosen as the LLM — free tier, no credit card, 1,500 requests/day.
2. **python-dotenv** for secret management — loads `.env` into environment variables. `.env` is in `.gitignore` so it never reaches GitHub.
3. **Pinned dependency versions** in `requirements.txt` — ensures reproducibility. If someone installs this in 6 months, they get the exact same library versions.
4. **`validate_config()` function** — fails fast with a human-readable error if the API key is missing. Prevents cryptic crashes later in the agent.

## Connection to Next Phases

- **Phase 2 (Data)** will import `DATA_FILEPATH` from `config.py` to know where to find the CSV file.
- **Phase 3 (Agent)** will import `GOOGLE_API_KEY` and `GEMINI_MODEL` from `config.py` to initialize the LLM.
- **Phase 4 (Frontend)** will import `APP_TITLE` from `config.py` to set the page title.
- **Phase 5 (Docker)** will use `requirements.txt` to install dependencies inside the container.

## Errors Encountered

None in this phase.
