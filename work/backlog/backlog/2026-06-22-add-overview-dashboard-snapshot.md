# Add Overview Dashboard Snapshot

## Priority

P3 - Implement after the shell exists so Overview has a destination, and after inventory model decisions so metrics use stable fields.

## Type

feature

## Context

The reference project makes the product feel like a waste-minimization dashboard by opening on an Overview page with metrics, expiry queue, low-stock queue, and concise links into deeper pages. The current project already has inventory data and existing backlog stories for expiry/waste, shopping, and meal planning, but it does not yet have a dashboard snapshot contract.

## Functional Requirements

- Users can open an Overview page that summarizes current inventory status.
- The Overview shows total active item count.
- The Overview shows an estimated expiry queue using existing inventory expiry dates.
- The Overview shows category distribution or grouping summary from existing inventory categories.
- The Overview reserves space for future waste, budget, shopping, and calendar metrics without showing fake data.

## Technical Requirements

- Approach: Add a backend dashboard endpoint or compose existing endpoints only after choosing the API contract during analysis.
- Approach: Use `foodmaxd/backend/app/routers/dashboard.py` and `foodmaxd/frontend/src/components/Overview.tsx` as references for snapshot shape, metric cards, and queues.
- Decision: Start with metrics supported by the current inventory model; defer money, low-stock percentage, waste rate, and calendar preview until their data exists.
- Decision: Keep dashboard response read-only and derived from persisted inventory state.
- Constraint: Do not invent budget, waste-event, recipe, or calendar records as placeholders.
- Constraint: Expiry copy must keep the current “estimated expiry” product language.

## Acceptance Criteria

- Overview displays active inventory count from real application data.
- Overview displays an estimated expiry queue sorted by soonest estimated expiry.
- Overview displays a category summary or category queue from real application data.
- Empty states are shown when inventory data is missing.
- Any future-only metric area is hidden, disabled, or labeled as not available rather than populated with mock data.
- Backend tests cover any new dashboard API contract if a backend endpoint is added.
- `npm run build` succeeds from `frontend/`.
- `python -m pytest backend/tests` succeeds from the repo root if backend code changes.
