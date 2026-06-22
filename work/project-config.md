# Project Config

This file is the canonical, human-readable source of truth for repo structure, guideline loading, review triggers, and repo-level command rules.

If another repo document conflicts with this file, follow this file.

## Purpose

- Use this file as rule, not background reading.
- Humans read it to understand expected agent behavior.
- Agents read it to decide which guidelines, reviews, and commands apply.

## Repo Structure

- Verified current workflow folders:
- `work/` is the durable source of truth for backlog, ideas, ADRs, and project operating context.
- `.opencode/` contains workflow implementation such as agents, commands, and skills.
- `AGENTS.md` defines agent behavior for this repository.
- `README.md` documents local and Docker Compose run commands.
- Runtime code layout:
- `backend/` contains the Python FastAPI, SQLAlchemy, and PostgreSQL backend.
- `frontend/` contains the React TypeScript frontend.
- `docker-compose.yml` defines the local full-stack runtime with PostgreSQL, backend, and frontend services.

## Output Rules

- Keep responses concise, structured, and grounded in repo artifacts.
- Distinguish verified facts from proposals and inferences.
- Prefer flat bullet lists over long prose unless the user requests another format.
- When repo context is needed, cite the relevant file path.
- Do not invent architecture, workflow, or domain rules that are not defined in this file, `AGENTS.md`, or the referenced repo artifacts.

## Domain Rules

- Product backlog and planning domain:
- Source of truth: `work/backlog/`, `work/ideas/`, `work/adr/`.
- Matching file patterns: `work/**/*.md`.
- Relevant keywords: inventory, foodstuff, food default, expiry, waste, meals, shopping list, planning, backlog, idea, ADR.
- Backend application domain:
- Planned stack: Python, FastAPI, SQLAlchemy, PostgreSQL.
- Matching file patterns: `backend/**/*.py`, `backend/pyproject.toml`, `backend/alembic.ini`, `backend/alembic/**/*.py`.
- Relevant keywords: FastAPI, router, endpoint, SQLAlchemy, session, model, schema, repository, service, PostgreSQL, Postgres, migration, Alembic.
- Frontend application domain:
- Planned stack: React with TypeScript.
- Matching file patterns: `frontend/**/*.{ts,tsx}`, `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`.
- Relevant keywords: React, TypeScript, component, hook, page, form, state, props, inventory view, sorting, grouping.
- Cross-domain product model domain:
- Applies when work touches concepts shared across backlog, backend, and frontend.
- Relevant keywords: inventory item, foodstuff, food default, category, quantity, purchase date, estimated expiry, waste event, meal plan, shopping suggestion.
- Containerization domain:
- Matching file patterns: `Dockerfile`, `**/Dockerfile`, `**/.dockerignore`, `docker-compose.yml`, `docker-compose.*.yml`.
- Relevant keywords: Docker, Compose, container, image, service, healthcheck, volume, port, environment variable, build arg, nginx.

## Technology Rules

- Python:
- Use for backend application logic.
- Prioritize clear separation between API, domain logic, and persistence concerns.
- FastAPI:
- Use for HTTP API endpoints and request/response contracts.
- Keep endpoint behavior aligned with product stories in `work/backlog/`.
- SQLAlchemy:
- Use for persistence models and database access.
- Treat foodstuff records as reusable food default settings, not actual inventory items; keep them distinct from owned inventory items.
- PostgreSQL:
- Use as the primary application database.
- Treat schema decisions around inventory, reusable food defaults, and later waste events as cross-story decisions.
- React with TypeScript:
- Use for frontend UI and stateful user flows.
- Keep UI behavior aligned with backlog requirements such as inventory CRUD, expiry sorting, and category grouping.
- Follow `work/guidelines/frontend.md` for frontend component boundaries, API access, DTO types, and reference-app adaptation.
- Docker and Docker Compose:
- Use for local full-stack runtime orchestration.
- Keep Compose service names, ports, environment variables, and build args documented in `README.md`.
- Keep browser-facing frontend API URLs host-accessible unless a frontend reverse proxy is explicitly added.
- Keep Docker build contexts free of local virtual environments, `node_modules`, build output, git data, and secrets.
- Frontend guideline file: `work/guidelines/frontend.md`.
- Until other dedicated guideline files exist, this file remains the governing technology guidance for non-frontend domains.

## Review Rules

- Story clarification review:
- Trigger keywords: story, backlog, acceptance criteria, scope, uncertainty, edge case.
- Primary sources: `work/backlog/`, `work/ideas/`, `work/adr/`, `brainstom.md`.
- Backend/API review:
- Trigger keywords: FastAPI, endpoint, route, request, response, SQLAlchemy, model, database, Postgres, migration.
- Focus: API contract clarity, model boundaries, persistence implications, story alignment.
- Frontend/UI review:
- Trigger keywords: React, TypeScript, component, form, sorting, grouping, dark mode, UX.
- Focus: user flow clarity, state boundaries, acceptance-criteria alignment, clean UI scope.
- Cross-domain data model review:
- Trigger keywords: inventory item, foodstuff, food default, expiry, quantity, category, waste, meal planning, shopping list.
- Focus: shared concept definitions and dependency impact across stories.
- Containerization review:
- Trigger keywords: Dockerfile, docker-compose, container, service, volume, healthcheck, build arg, environment variable.
- Focus: runtime wiring, service health, exposed ports, persistent data, secret avoidance, and README/project-config alignment.
- Frontend reviews should also consult `work/guidelines/frontend.md`.
- No other separate review guideline files are defined yet.

## Loading Rules

### Always Load

- Read `work/project-config.md` first for repo-level operating context.
- Use `AGENTS.md` as the repository workflow instruction source.
- Prefer `work/` artifacts over chat memory when they exist.

### Analysis

- Start with the smallest repo lookup needed to ground the question.
- When discussing product behavior, consult the relevant story in `work/backlog/` first.
- When discussing shared decisions or sequencing, also inspect adjacent backlog stories that depend on the same concepts.
- When discussing architecture or standards, inspect `work/adr/` if ADRs exist.
- If runtime code exists later, inspect only the files needed for the current question.

### Implementation

- Choose guidance based on affected domain files.
- For backend changes, load the backend technology rules in this file and inspect relevant backlog stories.
- For frontend changes, load the frontend technology rules in this file and inspect relevant backlog stories.
- For changes that affect shared concepts such as inventory item or foodstuff/food defaults, inspect both product artifacts and all touched technology domains.
- If dedicated guideline files are added later, update this file to reference them explicitly.

### Validation

- Validate against the acceptance criteria in the relevant backlog story.
- Validate shared model changes against adjacent dependent stories when the same concepts appear there.
- Run domain-appropriate checks for any touched backend or frontend code once project commands are defined.
- If no repo command exists yet for a validation step, say so explicitly rather than inventing one.

## Command Rules

- Backend validation commands:
- `docker run --rm -v "$PWD/backend:/app" -w /app python:3.13-slim sh -c 'python -m pip install -e ".[dev]" && python -m pytest tests'` from the repo root. Always run for backend changes.
- `docker run --rm -v "$PWD/backend:/app" -w /app python:3.13-slim sh -c 'python -m pip install -e ".[dev]" && ruff check . && ruff format --check .'` from the repo root. Always run for backend lint/static-check changes and backend Python changes.
- Frontend validation commands:
- `npm --prefix frontend run lint` from the repo root. Always run for frontend TypeScript/React changes and frontend lint/static-check changes after frontend dependencies are installed.
- `docker compose build frontend` from the repo root. Always run for frontend changes.
- Repo hygiene validation commands:
- `pre-commit run --all-files` from the repo root. Always run for pre-commit configuration changes after backend, frontend, and pre-commit dependencies are installed.
- Docker/Compose validation commands:
- `docker compose config` from the repo root. Always run for Compose changes.
- `docker compose build` from the repo root. Always run for Dockerfile or Compose build changes when Docker is available.
- Database migration commands are not yet defined in the repo.
- Backend linting/static-check commands are defined above.
- Frontend linting/static-check commands are defined above.
- Frontend unit-test commands are not yet defined in the repo.
- If a required command cannot run because Docker is unavailable, report the environment blocker explicitly.

## Agent Usage Rule

- Read this file first when you need repo structure, guideline loading rules, review triggers, or repo-level command rules.
- Load only the guideline files that match the current task.
- Do not invent rules outside this file, `AGENTS.md`, and the loaded guideline files.
