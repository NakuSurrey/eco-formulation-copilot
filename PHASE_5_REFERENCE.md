# PHASE 5 REFERENCE — Containerisation & CI/CD

## Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Tells Docker how to package the entire app into a portable container. Uses `python:3.10-slim` as the base, installs dependencies from `requirements.txt`, copies project files, and runs `streamlit run app.py` on port 8501. Includes a health check. |
| `.dockerignore` | Tells Docker which files to SKIP when building the image. Excludes `.env` (secrets), `venv/` (container installs its own), `tests/` (not needed at runtime), `.git/`, cache files, and documentation. Keeps the image small and secure. |
| `.github/workflows/ci.yml` | GitHub Actions CI/CD pipeline. Runs 3 jobs on every push: (1) `lint` — flake8 code style check, (2) `test` — pytest unit tests, (3) `docker` — verifies the Docker image builds. A green badge = all passing. |

## Files Modified

| File | Change |
|------|--------|
| `tests/test_agent.py` | Removed unused `import pandas as pd` (line 17). Was causing flake8 F401 failure. See Error 003 in ERRORS.md. |
| `.gitignore` | Added `pytest-cache-files-*/` and `.pytest_cache/` rules. Removed `*.md` rule that was blocking all Markdown files from being pushed. |

## Key Decisions

1. **`python:3.10-slim`** as the Docker base image — matches the Python version used in development. The `slim` variant is ~150MB instead of ~900MB, keeping the container small.
2. **Layer caching strategy** — `COPY requirements.txt` happens BEFORE `COPY . .` in the Dockerfile. Docker caches each step. If dependencies don't change, the slow `pip install` step is skipped entirely on rebuilds. Only changed source code gets re-copied.
3. **3 separate CI jobs (lint, test, docker)** instead of 1 combined job — if linting fails, you see "lint: failed" immediately without waiting for tests to finish. Each job runs in parallel on GitHub's servers, so total CI time is the duration of the slowest job, not the sum of all jobs.
4. **`--server.address=0.0.0.0`** in the Docker CMD — without this, Streamlit listens only on `127.0.0.1` (localhost), which means it only accepts connections from inside the container itself. `0.0.0.0` means "accept connections from any IP address", which is required for the `-p 8501:8501` port mapping to work.
5. **Tests excluded from Docker image** — the `.dockerignore` skips the `tests/` folder because tests are for development, not production. They run in CI (GitHub Actions), not inside the container.
6. **Health check** — Docker periodically curls `/_stcore/health` (Streamlit's built-in health endpoint) to verify the app is responding. If 3 checks fail in a row, Docker marks the container as unhealthy.

## Connection to Previous Phases

- Uses `requirements.txt` from Phase 1 to install dependencies inside the container
- Uses `data/formulations.csv` from Phase 2 — gets copied into the container
- Uses `tests/test_agent.py` and `tests/test_data_loader.py` from Phases 2–3 — run by the CI pipeline
- Uses `app.py` from Phase 4 as the container's entry point command

## Connection to Next Phases

- **Phase 6 (Deployment & Documentation)** will reference the Docker build capability in the README. Streamlit Community Cloud will use `requirements.txt` directly (not Docker) for deployment. The CI green badge will be displayed in the README.

## Errors Encountered

- **Error 003:** `flake8 F401` — unused `import pandas as pd` in `tests/test_agent.py`. Removed the import. See ERRORS.md for full details.
