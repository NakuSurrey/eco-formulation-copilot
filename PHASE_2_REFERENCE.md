# PHASE 2 REFERENCE — Data Generation & Loading

## Files Created

| File | Purpose |
|------|---------|
| `data/generate_data.py` | Script that generates 500 rows of synthetic chemical formulation data with realistic column names, value ranges, and correlations (e.g., high biodegradability costs more). Uses `random.seed(42)` for reproducibility. |
| `data/formulations.csv` | The generated dataset. 500 rows, 9 columns: Formula_ID, Surfactant_Type, Polymer_Type, Enzyme_Type, Concentration_Pct, Biodegradability_Score, Cleaning_Efficacy_Score, Toxicity_Level, Cost_Per_Litre_GBP. |
| `src/data_loader.py` | Single function `load_data()` that reads the CSV into a Pandas DataFrame and validates it (checks for missing columns, empty data, NaN values). Every other file that needs the data imports from here. |
| `tests/test_data_loader.py` | 13 tests covering: successful load, correct row/column count, all columns present, no NaN values, realistic numeric ranges, and proper error handling for bad inputs. |

## Key Decisions

1. **500 rows** — Large enough to look realistic in charts and agent queries. Small enough to load instantly in memory.
2. **`random.seed(42)`** — Makes the data deterministic. Running the script twice produces the same CSV. This is Trait #26 (Reproducible).
3. **"No Enzyme" instead of "None"** — Fixed a bug where Pandas auto-converted the string "None" to NaN. See ERRORS.md Error 001.
4. **Validation inside `load_data()`** — Fails fast with a clear error message if the CSV is missing, empty, or has wrong columns. Prevents cryptic crashes later in the agent.
5. **Separate `data_loader.py` module** — Both the agent (Phase 3) and the dashboard (Phase 4) need the same DataFrame. Loading it in one place avoids duplicated code (Trait #29 DRY).

## Connection to Previous Phases

- Imports `DATA_FILEPATH` from `src/config.py` (Phase 1) to know where the CSV lives.

## Connection to Next Phases

- **Phase 3 (Agent)** will call `load_data()` to get the DataFrame that the LLM queries against.
- **Phase 4 (Dashboard)** will call `load_data()` to get the DataFrame for Plotly charts.

## Errors Encountered

- **Error 001:** Pandas converted the string "None" to NaN in the Enzyme_Type column. Fixed by changing "None" to "No Enzyme". See ERRORS.md for full details.
