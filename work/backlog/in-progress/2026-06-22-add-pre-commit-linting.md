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
