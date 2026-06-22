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

## Implemented foundation

- Reusable foodstuff configuration with category and min/max estimated expiry days.
- Active inventory items with name, category, quantity amount/unit, purchase date, and estimated expiry date.
- Foodstuff suggestions and quick creation from the add-item flow.
- Inventory create, update, remove from active inventory, expiry ordering, and category grouping.
- Removal is intentionally not modeled as eaten or wasted behavior.
