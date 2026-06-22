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
- `README.md` exists but is currently empty.
- Application runtime code layout is not yet present in the repository.
- Until runtime folders are created, treat backend and frontend as separate logical domains selected by technology and file patterns rather than fixed directories.

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
- Relevant keywords: inventory, foodstuff, expiry, waste, meals, shopping list, planning, backlog, idea, ADR.
- Backend application domain:
- Planned stack: Python, FastAPI, SQLAlchemy, PostgreSQL.
- Matching file patterns when present: `**/*.py`, `**/requirements*.txt`, `**/pyproject.toml`, `**/alembic.ini`, `**/alembic/**/*.py`.
- Relevant keywords: FastAPI, router, endpoint, SQLAlchemy, session, model, schema, repository, service, PostgreSQL, Postgres, migration, Alembic.
- Frontend application domain:
- Planned stack: React with TypeScript.
- Matching file patterns when present: `**/*.{ts,tsx}`, `**/package.json`, `**/tsconfig.json`.
- Relevant keywords: React, TypeScript, component, hook, page, form, state, props, inventory view, sorting, grouping.
- Cross-domain product model domain:
- Applies when work touches concepts shared across backlog, backend, and frontend.
- Relevant keywords: inventory item, foodstuff, category, quantity, purchase date, estimated expiry, waste event, meal plan, shopping suggestion.

## Technology Rules

- Python:
- Use for backend application logic.
- Prioritize clear separation between API, domain logic, and persistence concerns.
- FastAPI:
- Use for HTTP API endpoints and request/response contracts.
- Keep endpoint behavior aligned with product stories in `work/backlog/`.
- SQLAlchemy:
- Use for persistence models and database access.
- Keep reusable foodstuff configuration distinct from actual inventory items.
- PostgreSQL:
- Use as the primary application database.
- Treat schema decisions around inventory, foodstuff defaults, and later waste events as cross-story decisions.
- React with TypeScript:
- Use for frontend UI and stateful user flows.
- Keep UI behavior aligned with backlog requirements such as inventory CRUD, expiry sorting, and category grouping.
- No technology-specific guideline files are defined yet.
- Until dedicated guideline files exist, this file is the governing technology guidance.

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
- Trigger keywords: inventory item, foodstuff, expiry, quantity, category, waste, meal planning, shopping list.
- Focus: shared concept definitions and dependency impact across stories.
- No separate review guideline files are defined yet.

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
- For changes that affect shared concepts such as inventory item or foodstuff, inspect both product artifacts and all touched technology domains.
- If dedicated guideline files are added later, update this file to reference them explicitly.

### Validation

- Validate against the acceptance criteria in the relevant backlog story.
- Validate shared model changes against adjacent dependent stories when the same concepts appear there.
- Run domain-appropriate checks for any touched backend or frontend code once project commands are defined.
- If no repo command exists yet for a validation step, say so explicitly rather than inventing one.

## Command Rules

- Backend validation commands are not yet defined in the repo.
- Frontend validation commands are not yet defined in the repo.
- Database migration commands are not yet defined in the repo.
- Once the runtime project is scaffolded, add the canonical commands for:
- backend tests
- backend linting or static checks
- frontend tests
- frontend linting and type-checking
- database migrations
- Until then, agents must not invent repo-standard commands.

## Agent Usage Rule

- Read this file first when you need repo structure, guideline loading rules, review triggers, or repo-level command rules.
- Load only the guideline files that match the current task.
- Do not invent rules outside this file, `AGENTS.md`, and the loaded guideline files.
