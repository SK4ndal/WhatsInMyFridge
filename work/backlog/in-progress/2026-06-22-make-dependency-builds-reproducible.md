# Make Dependency Builds Reproducible

## Type

chore

## Context

Security review found that dependency builds are not currently reproducible. The frontend uses `latest` dependency ranges without a committed lockfile, the frontend Docker build uses `npm install`, and the backend dependency metadata uses lower-bound-only Python requirements. This allows local installs and container builds to resolve different dependency versions over time, increasing supply-chain, compatibility, and incident-response risk.

## Functional Requirements

- Developers can install frontend dependencies from a committed lockfile.
- Frontend container builds use the committed lockfile rather than resolving fresh dependency versions.
- Backend dependencies are constrained enough to make expected dependency resolution reviewable and repeatable.
- Dependency source-of-truth files are committed and documented for local development and container builds.
- Existing backend and frontend validation commands still pass after dependency locking changes.

## Technical Requirements

- Approach: Replace frontend `latest` dependency declarations with explicit version ranges or pinned versions appropriate for the currently working React/Vite/TypeScript stack.
- Approach: Generate and commit `frontend/package-lock.json` from the updated `frontend/package.json`.
- Approach: Change `frontend/Dockerfile` from `npm install` to `npm ci` so Docker builds consume the committed lockfile.
- For the backend use venvs and use astral uv. 
- Approach: Review `backend/pyproject.toml` dependency specifiers and add upper bounds or compatible-release constraints for runtime and dev dependencies where practical.
- Decision: Treat lockfiles and constrained dependency metadata as the source of truth for reproducible development and Docker builds.
- Constraint: Do not add unrelated feature work, auth, UI behavior changes, or API contract changes.
- Constraint: Do not suppress or ignore dependency installation errors; fix incompatible constraints explicitly.
- Validation: Run `npm run build` from `frontend/` after lockfile changes.Use the container infrastructure for this. 
- Validation: Run `python -m pytest backend/tests` from the repo root with backend dependencies installed after backend constraint changes. Use container infrastructure for this. 
- Validation: Run `docker compose build` from the repo root if Docker is available, because `frontend/Dockerfile` behavior changes.

## Acceptance Criteria

- `frontend/package.json` no longer uses `latest` dependency declarations.
- `frontend/package-lock.json` exists and is committed.
- `frontend/Dockerfile` uses `npm ci` for dependency installation.
- Backend dependency constraints in `backend/pyproject.toml` are reviewed and updated to avoid unconstrained lower-bound-only resolution where appropriate.
- `npm run build` succeeds from `frontend/`.
- `python -m pytest backend/tests` succeeds from the repo root when backend dependencies are installed.
- `docker compose build` succeeds when Docker is available.
- Any intentionally unpinned or broadly ranged dependency is documented with rationale in the story closeout or README.

## Analysis

### Likely Impact

- Primary implementation lane: dependency source files -> container install behavior -> local-development documentation.
- `frontend/package.json` - direct acceptance target; current dependencies and dev dependencies all use `"latest"`, so this is the first frontend source-of-truth change.
- `frontend/package-lock.json` - currently absent; generate from the updated frontend dependency metadata so local installs and Docker builds share a lockfile.
- `frontend/Dockerfile` - current build copies `package*.json` then runs `npm install`; switch that install step to lockfile-consuming behavior (`npm ci`).
- `backend/pyproject.toml` - current runtime and dev dependencies are lower-bound-only (`>=...`); review and constrain ranges there before widening to backend runtime code.
- Inference: README documentation likely needs a small update because current frontend local setup says `npm install`, and backend setup currently uses `pip install -e ".[dev]"` rather than uv.

### Possible Adjacent Touchpoints

- `README.md` - may need to document lockfile-based frontend install and the intended backend dependency workflow/source of truth for local development.
- `backend/Dockerfile` - current container install path is pip-based and copies only `pyproject.toml`; touch only if the uv requirement is interpreted as applying to backend container builds, not just local venv workflow.
- `backend/uv.lock` or another uv-managed lock artifact - currently absent; story says “use astral uv,” but acceptance criteria only require constrained `pyproject.toml`, so confirm implementation intent before adding backend lockfile scope.

### Existing Patterns / Prior Art

- `frontend/Dockerfile` - already has the standard package metadata copy before install, so the closest pattern is a narrow `npm install` -> `npm ci` substitution after creating `package-lock.json`.
- `docker-compose.yml` frontend build service - existing Compose wiring builds `./frontend` with `VITE_API_BASE_URL`; reuse this path to validate the Dockerfile change rather than adding new build flows.
- No close repo prior art found for uv-based backend dependency locking; current backend local and container paths use pip from `pyproject.toml`.

### Layer Boundaries

- Touch first: package/dependency metadata, lockfiles, Docker install commands, and minimal README dependency workflow text.
- Avoid unless evidence emerges: FastAPI routes, SQLAlchemy models, frontend React components, API contracts, auth, database migrations, Compose service topology, nginx config, and feature behavior.
- Repo-grounded ambiguity: the story names uv for backend dependency management, but current repo evidence uses pip in `README.md` and `backend/Dockerfile`, with no `uv.lock`; treat uv adoption breadth as an implementation risk to clarify without expanding into unrelated backend changes.

### Verification Plan

**Unit Tests**:

- Verify backend tests run after dependency constraint changes using the repo-configured backend validation path.

**Integration Tests**:

- Verify the frontend Docker build consumes `package-lock.json` through the lockfile install path.
- Verify generated frontend lockfile is in sync with `frontend/package.json` and no frontend dependency declaration remains `latest`.

**E2E / Manual Validation**:

- If README dependency instructions change, follow the documented local install steps in a clean environment or container to confirm they are accurate.

**Additional Checks**:

- Security-officer story-scope review: no blocker found; confirmed story reduces supply-chain reproducibility risk. Main caution is to avoid unreviewed broad uv/container workflow expansion beyond the dependency-locking scope.
