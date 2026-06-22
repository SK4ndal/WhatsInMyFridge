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
