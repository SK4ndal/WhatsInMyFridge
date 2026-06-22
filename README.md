# WhatsInMyFridge

First implementation of the core inventory foundation.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, PostgreSQL.
- Frontend: React with TypeScript and Vite.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The default backend database URL is:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/whats_in_my_fridge
```

Override it with `WIMF_DATABASE_URL`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` by default. Override it with `VITE_API_BASE_URL`.

Run frontend linting with:

```bash
cd frontend
npm run lint
```

## Pre-commit checks

Install backend, frontend, and pre-commit dependencies once per checkout:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd ../frontend
npm install
cd ..
pip install pre-commit
pre-commit install
```

Run the hooks manually against the full repository with:

```bash
pre-commit run --all-files
```

The hooks run common file hygiene checks, Ruff linting and formatting for backend Python, and the frontend ESLint script.

## Docker Compose

Run the complete local application stack with Docker Compose:

```bash
docker compose up --build
```

Exposed local ports:

- Frontend UI: `http://localhost:8080`
- Backend API: `http://localhost:18000`
- Backend health check: `http://localhost:18000/health`
- PostgreSQL: `localhost:5433` on the host, mapped to `5432` inside Compose

The Compose stack includes:

- `postgres` using the `postgres:16-alpine` image.
- `backend` built from `backend/Dockerfile`.
- `frontend` built from `frontend/Dockerfile` and served by nginx.

PostgreSQL data is persisted in the named Docker volume `postgres_data`.

The frontend container is built with `VITE_API_BASE_URL=http://localhost:18000` so browser requests use the host-exposed backend port. The backend receives its database URL from `WIMF_DATABASE_URL` in `docker-compose.yml`.

Stop the stack with:

```bash
docker compose down
```

Remove persisted PostgreSQL data with:

```bash
docker compose down --volumes
```

## Implemented foundation

- Reusable foodstuff configuration with category and min/max estimated expiry days.
- Active inventory items with name, category, quantity amount/unit, purchase date, and estimated expiry date.
- Foodstuff suggestions and quick creation from the add-item flow.
- Inventory create, update, remove from active inventory, expiry ordering, and category grouping.
- Removal is intentionally not modeled as eaten or wasted behavior.
