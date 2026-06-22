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
