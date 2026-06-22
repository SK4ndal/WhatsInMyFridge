# Use FastAPI, SQLAlchemy, and PostgreSQL for the Backend

Date: 2026-06-22
Status: Accepted

## Context

The core inventory foundation story introduced the first backend implementation for WhatsInMyFridge. The implemented backend needs to expose inventory APIs and foodstuff APIs. In product terms, foodstuff records are reusable food default settings that can exist without adding anything to inventory. These defaults can provide category, expected expiry range, amount, or similar starter values when a user later adds an owned inventory item. They must remain separate from actual inventory items and support later stories such as expiry awareness, waste tracking, shopping-list intelligence, meal recommendations, and meal planning.

`work/project-config.md` already defines the backend stack as Python, FastAPI, SQLAlchemy, and PostgreSQL. The implemented containerization story also confirms PostgreSQL as the Compose database service and validates backend connectivity through `WIMF_DATABASE_URL`.

## Decision

Use Python with FastAPI for the backend HTTP API, SQLAlchemy for persistence models and database access, and PostgreSQL as the primary application database.

Backend configuration that differs by environment, including the database URL, must come from environment variables rather than hard-coded runtime values. Local full-stack execution uses Docker Compose to run PostgreSQL and the backend together.

## Consequences

- Backend API behavior should remain aligned with product stories in `work/backlog/`.
- SQLAlchemy models are the source for persisted boundaries between owned inventory items and reusable food default settings currently represented by foodstuff records.
- PostgreSQL-specific behavior is acceptable for application persistence decisions.
- Later schema changes for expiry, waste events, shopping suggestions, and meal planning should be treated as cross-story data-model decisions.
- Validation should use the Docker-based backend command defined in `work/project-config.md` so agents do not depend on host Python tooling.
