# Use React, TypeScript, and Vite for the Frontend

Date: 2026-06-22
Status: Accepted

## Context

The core inventory foundation story introduced the first frontend implementation for inventory creation, editing, removal, expiry sorting, category grouping, foodstuff suggestions, and quick foodstuff creation. The UI needs to remain suitable for continued iteration across upcoming dashboard, receipt import, expiry awareness, shopping-list, recipe, and meal-planning stories.

`work/project-config.md` defines the frontend stack as React with TypeScript. The implemented containerization story builds the frontend with Vite and serves the production bundle from the frontend Docker image. Compose validation confirms the browser can load the frontend and call the backend API through a host-accessible URL.

## Decision

Use React with TypeScript for frontend UI implementation and Vite for frontend development/build tooling.

Frontend API access should use typed DTOs and a small API boundary rather than scattering raw fetch calls throughout components. Browser-facing API URLs must remain host-accessible in Docker Compose unless a frontend reverse proxy is explicitly added.

## Consequences

- Frontend changes should follow `work/guidelines/frontend.md` for component boundaries, API access, DTO types, and reference-app adaptation.
- The frontend build path is the Vite production build executed by `docker compose build frontend`.
- Shared product concepts such as inventory items, foodstuffs, expiry dates, categories, and quantities should stay aligned with backend contracts and backlog stories.
- Compose builds must provide a browser-accessible `VITE_API_BASE_URL`, currently `http://localhost:18000`.
- Validation should use the Docker-based frontend command defined in `work/project-config.md` so agents do not depend on host npm tooling.
