# Containerize Application

## Type

chore

## Context

The first application implementation now has a FastAPI/SQLAlchemy backend in `backend/`, a React TypeScript frontend in `frontend/`, and PostgreSQL as the intended database. Developers need a repeatable way to build and run the whole application locally without manually starting each runtime dependency.

This story adds Docker support for the backend, frontend, and database, plus a Docker Compose setup that runs the complete application stack.

## Functional Requirements

- Developers can build a backend container image for the FastAPI application.
- Developers can build a frontend container image for the React TypeScript application.
- Developers can run the backend, frontend, and PostgreSQL database together with Docker Compose.
- The backend service can connect to the PostgreSQL service through Compose networking.
- The frontend service can communicate with the backend API when the Compose stack is running.
- The Compose setup exposes the frontend and backend on documented local ports.
- The Compose setup persists PostgreSQL data across container restarts using a named volume.

## Technical Requirements

- Approach: Add a `backend/Dockerfile` for the FastAPI app and a `frontend/Dockerfile` for the React TypeScript app.
- Approach: Add a root-level `docker-compose.yml` that defines `backend`, `frontend`, and `postgres` services.
- Decision: Use PostgreSQL as the Compose database service to match `work/project-config.md` and the backend stack decision.
- Decision: Configure the backend database URL through environment variables rather than hard-coding container-specific values in application code.
- Decision: Keep local Docker configuration focused on development/demo usage first; production hardening can be handled separately.
- Decision: Include service health checks or dependency ordering where useful so startup behavior is understandable.
- Constraint: Do not add eaten/wasted, recommendations, shopping-list, or meal-planning behavior as part of containerization.
- Constraint: Docker files should not copy local virtual environments, `node_modules`, build artifacts, or secrets into images.
- Constraint: Document required commands and ports in `README.md` and update `work/project-config.md` command rules if Docker becomes a canonical validation/run path.
- Rejected alternative: Run only PostgreSQL in Docker and keep backend/frontend host-based; rejected because the goal is to run the whole application stack consistently.

## Acceptance Criteria

- `backend/Dockerfile` exists and can build the FastAPI backend image.
- `frontend/Dockerfile` exists and can build the React TypeScript frontend image.
- A root-level `docker-compose.yml` exists with backend, frontend, and PostgreSQL services.
- Running the Compose stack starts PostgreSQL, the backend API, and the frontend UI.
- The backend receives its PostgreSQL connection settings from Compose environment configuration.
- PostgreSQL data is stored in a named Docker volume.
- The frontend can call the backend API from the Compose-run UI.
- `README.md` documents how to build and run the Compose stack.
- `work/project-config.md` is updated if Docker commands become canonical repo commands.

## Analysis

### Likely Impact

- Primary implementation lane: root Compose file -> backend Dockerfile/runtime command -> frontend Dockerfile/runtime strategy -> README/project-config command updates.
- `backend/pyproject.toml` - backend image should install the Python package and runtime dependencies from the existing project metadata.
- `backend/app/main.py` - backend container should run `uvicorn app.main:app`; the existing `/health` endpoint can support Compose health checks.
- `backend/app/config.py` - backend database and CORS configuration already come from `WIMF_` environment variables, so Compose should set `WIMF_DATABASE_URL` for the `postgres` service and likely `WIMF_ALLOWED_ORIGINS` for the frontend origin.
- `frontend/package.json` - frontend image should use existing npm scripts; `npm run build` is the configured validation/build path.
- `frontend/src/api.ts` - frontend API URL is controlled by `VITE_API_BASE_URL`, which is a build-time Vite value and must be set carefully for a browser-accessible backend URL.

### Possible Adjacent Touchpoints

- `.dockerignore` files or root ignore rules - needed to prevent `.venv`, `node_modules`, build output, git data, and local secrets from entering Docker build contexts.
- `frontend/package.json` - may need script or dependency adjustments if the container runs Vite dev server with `--host`, or if a production static server such as nginx is chosen.
- `backend/app/config.py` - may need CORS-origin parsing confirmation for Compose-provided values, because the current setting is a `list[str]` loaded through Pydantic settings.
- `README.md` - should document exposed ports, environment overrides, and `docker compose up --build` usage.
- `work/project-config.md` - should add Docker/Compose commands only if they become canonical repo run or validation commands.

### Existing Patterns / Prior Art

- `README.md` - existing local run docs identify backend and frontend startup commands and default ports; Docker docs should extend this rather than create a parallel story of how the app runs.
- `work/project-config.md` - current source of truth for backend/frontend layout and validation commands.
- `backend/app/main.py` health route - closest existing health-check hook for a backend Compose health check.
- No existing Dockerfile, Compose file, or containerization pattern was found in the repo.

### Layer Boundaries

- Touch first: `backend/Dockerfile`, `frontend/Dockerfile`, root `docker-compose.yml`, Docker ignore files, `README.md`, and possibly `work/project-config.md` command rules.
- Touch first: environment wiring for `WIMF_DATABASE_URL`, frontend `VITE_API_BASE_URL`, service ports, and PostgreSQL named volume.
- Avoid unless evidence emerges: inventory API behavior, SQLAlchemy models, React inventory UI logic, eaten/wasted semantics, recommendations, shopping-list features, meal planning, and database migrations beyond what is required to boot the existing app.
- Avoid unless evidence emerges: production deployment hardening such as TLS, image registry publishing, secrets management, horizontal scaling, or reverse-proxy architecture.

### Verification Plan

**Integration Tests**:

- Build backend and frontend images successfully through Docker or Compose.
- Start the full Compose stack and verify PostgreSQL, backend, and frontend services become healthy or reachable.
- Verify backend `/health` responds through the exposed host port while running in Compose.
- Verify backend can connect to the Compose PostgreSQL service using `WIMF_DATABASE_URL`.

**E2E / Manual Validation**:

- Open the Compose-run frontend in a browser and confirm it can reach the backend API.
- Create a foodstuff and inventory item through the Compose-run UI to prove frontend -> backend -> PostgreSQL wiring.
- Restart the Compose stack and confirm PostgreSQL data persists through the named volume.

**Additional Checks (as applicable)**:

- Confirm the browser-facing API URL is host-accessible, not the internal Compose service name, unless a frontend reverse proxy is added.
- Confirm Docker build contexts exclude `.venv`, `node_modules`, build artifacts, and secrets.
- Confirm any new Docker commands added to `work/project-config.md` match the actual Compose workflow.
