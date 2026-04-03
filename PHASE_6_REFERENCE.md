# PHASE 6 REFERENCE — Deployment & Documentation

## Files Created

| File | Purpose |
|------|---------|
| `README.md` | The project's front page on GitHub. Contains: Executive Summary, architecture diagram (text-based flow), feature list, P&G job mapping table, tech stack table with rationale, dataset schema, full project structure, Quick Start (local + Docker), test commands, CI/CD explanation, and author section. This is the first thing a recruiter sees. |

## Key Decisions

1. **CI badge at the very top** — the green checkmark badge is the first visual element a recruiter sees. It immediately signals "this person runs automated tests." Badges are standard practice on enterprise open-source projects.
2. **P&G Job Mapping table** — explicitly maps every bullet point from the job description to a specific file or feature in the project. The recruiter does not have to guess which requirement each feature addresses.
3. **Two Quick Start options (local + Docker)** — the recruiter can choose whichever method they prefer. Local is simpler for developers. Docker is a single command for non-developers.
4. **Dataset table with ranges** — shows the recruiter exactly what data the app works with, without them having to open the CSV. This demonstrates data documentation skills.
5. **"Coming soon" for Live Demo** — placeholder until Streamlit Community Cloud deployment is configured. Honest about the current state rather than linking to a dead URL.
6. **Text-based architecture diagram** — uses plain ASCII characters instead of an image. This renders everywhere (GitHub, terminal, email) without needing an external image host or Mermaid support.

## Connection to Previous Phases

- References `requirements.txt` from Phase 1 in Quick Start instructions
- Documents the dataset from Phase 2 (all 9 columns with ranges)
- Explains the agent architecture from Phase 3 in the "How It Works" section
- Lists all dashboard features from Phase 4 in the "Features" section
- Displays the CI badge from Phase 5 at the top of the file
- References Docker commands from Phase 5 in Quick Start

## Connection to Next Steps

- When Streamlit Community Cloud is deployed, replace the "Coming soon" placeholder with the live URL
- The CI badge will automatically update to show green/red based on the pipeline status after the first push

## Errors Encountered

None in this phase.
