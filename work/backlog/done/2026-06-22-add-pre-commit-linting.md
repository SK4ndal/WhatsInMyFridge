# Add Pre-commit Linting

## Type

chore

## Context

The application now has a Python FastAPI backend and a React TypeScript frontend. The repo needs consistent automated checks before commits so formatting, linting, and common quality issues are caught early across both stacks.

This story adds a pre-commit setup with Ruff for Python backend checks and relevant frontend checks for TypeScript/React code.

## Functional Requirements

- Developers can install one pre-commit configuration for the repository.
- Pre-commit runs Python backend formatting and linting checks.
- Pre-commit runs frontend formatting, linting, or type-related checks appropriate for React TypeScript code.
- Pre-commit catches common file hygiene issues such as trailing whitespace, invalid YAML/JSON, and missing final newlines.
- The repository documents how to install and run the hooks manually.

## Technical Requirements

- Approach: Add a root-level `.pre-commit-config.yaml`.
- Approach: Add Ruff configuration for backend Python formatting and linting, preferably in `backend/pyproject.toml` unless a root configuration is more appropriate.
- Approach: Add frontend linting configuration for React TypeScript, such as ESLint with TypeScript and React rules.
- Approach: Keep frontend type checking available through the existing `npm run build` flow or add a dedicated type-check script if useful.
- Decision: Use Ruff as the primary backend formatter/linter to keep Python checks fast and simple.
- Decision: Use pre-commit for local guardrails, while keeping backend tests and frontend build as explicit validation commands.
- Constraint: Hooks should not require Docker to run.
- Constraint: Hooks should avoid unexpectedly modifying unrelated files outside the backend/frontend/workflow scope.
- Constraint: Hook commands should work from a fresh checkout after documented dependency installation.
- Constraint: Update `work/project-config.md` command rules if linting/static-check commands become canonical.
- Rejected alternative: Rely only on manual code review for formatting and linting; rejected because cross-stack consistency should be automated.

## Acceptance Criteria

- A root-level `.pre-commit-config.yaml` exists.
- Backend Python files are checked by Ruff through pre-commit.
- Backend Python formatting is enforced or fixable through Ruff.
- Frontend TypeScript/React linting is configured and can be run through npm scripts.
- Common file hygiene hooks are included for whitespace, final newlines, and structured config files.
- `README.md` documents how to install and run pre-commit hooks.
- `work/project-config.md` lists canonical lint/static-check commands after they are defined.
- Running the documented hook command succeeds after dependencies are installed.

## Analysis

### Likely Impact

- Primary implementation lane: root developer-tooling config -> backend Ruff config/dependencies -> frontend lint script/config -> README and project-config command documentation.
- `.pre-commit-config.yaml` - new root entry point required by the story; should wire generic hygiene hooks plus scoped backend/frontend checks.
- `backend/pyproject.toml` - existing backend project metadata and dev extras live here; add Ruff dev dependency/config close to current pytest config.
- `frontend/package.json` - current scripts only include `dev`, `build`, and `preview`; add lint/static-check script(s) and ESLint-related dev dependencies here.
- Frontend lint config file, likely `frontend/eslint.config.js` or equivalent - no existing ESLint config was found, so implementation needs a new TypeScript/React lint configuration.
- `README.md` and `work/project-config.md` - acceptance criteria require documented pre-commit installation/manual run instructions and canonical lint/static-check command rules.

### Possible Adjacent Touchpoints

- `frontend/tsconfig.json` - already has strict TypeScript settings and `noEmit`; only touch if ESLint/parser configuration needs an explicit project reference.
- `frontend/src/**/*.{ts,tsx}` and `backend/**/*.py` - avoid broad formatting churn, but small fixes may be needed if newly configured Ruff/ESLint rules reveal existing violations.
- `.gitignore` - only touch if the chosen toolchain creates new local cache/output paths not already ignored.

### Existing Patterns / Prior Art

- `backend/pyproject.toml` - existing pattern for Python tool config is co-locating pytest settings and dev dependencies in the backend package file.
- `frontend/package.json` - existing npm script pattern is simple project-local commands (`npm run build` already performs `tsc -b && vite build`).
- `README.md` - existing docs are split by backend/frontend/Docker sections with copyable shell snippets; add pre-commit usage in the same concise style.
- No existing pre-commit or ESLint configuration was found, so implementation should use standard tool defaults rather than trying to match repo-local prior art.

### Layer Boundaries

- Touch first: root workflow/tooling config, backend Python packaging/tool config, frontend package/lint config, repo docs, and command metadata in `work/project-config.md`.
- Avoid unless evidence emerges: FastAPI routers/models/schemas, React component behavior, database/Alembic setup, Docker/Compose runtime wiring, and product backlog requirements outside this story.
- Inference: If lint fixes are required, keep them mechanical and limited to files flagged by the new checks rather than using this story for refactors.

### Verification Plan

**Integration Tests**:

- Verify the documented manual pre-commit command runs against all files after installing documented dependencies.
- Verify backend Ruff formatting/lint hooks and frontend lint hook can run from a fresh checkout workflow without Docker.

**E2E / Manual Validation**:

- Confirm README instructions cover installing pre-commit, installing backend/frontend dependencies, installing hooks, and manually running hooks.

**Additional Checks (as applicable)**:

- Confirm `work/project-config.md` is updated only after canonical lint/static-check commands exist, and that command rules distinguish pre-commit/local linting from existing Docker-based validation commands.

## Implementation notes (2026-06-22 00:00)

- Added root pre-commit configuration with file hygiene hooks, Ruff backend checks, and frontend ESLint hook.
- Added backend Ruff dev dependency/config and frontend ESLint script/config/dependencies.
- Updated README installation/manual hook instructions and project command rules.
- Ran validation: backend tests, backend Ruff checks, frontend Docker build, frontend lint in Node Docker, and pre-commit hooks in Node Docker.
- Note: direct host `npm --prefix frontend run lint` could not run because `npm` is not installed in this environment; Docker-based equivalent passed.

## Validation update (2026-06-22 14:46)

* Validation passed with no regressions found.
* Gate result: PASS.
* Baseline checks passed or had no unrelated failures observed: backend pytest, backend Ruff, frontend lint via Node Docker, frontend Docker build, and pre-commit hooks via Node Docker passed.
* Touched-scope coverage: no material regression; no coverage command is defined for this tooling-only change.
* Security review: completed; no secrets, privileged workflow, auth, external-call, file-access, or input-handling risks introduced beyond pinned pre-commit hook sources and local tooling commands.
* Retained exploratory artifacts: none.
* Validated checklist items: root pre-commit config exists; Ruff backend lint/format configured and hooked; frontend ESLint script/config exists and runs; hygiene hooks cover whitespace, final newline, YAML, JSON, and TOML; README install/manual hook instructions exist; project-config canonical lint/static-check commands exist; documented hook flow passes after dependencies are installed.
* Providers covered: not applicable.
