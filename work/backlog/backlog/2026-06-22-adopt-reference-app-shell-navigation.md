# Adopt Reference App Shell Navigation

## Priority

P2 - Implement after inventory model decisions and before adding multiple dashboard-style pages.

## Type

feature

## Context

The current app has a single-page inventory-focused layout in `frontend/src/App.tsx`. The `foodmaxd` reference project presents the product as a kitchen dashboard with a persistent sidebar, topbar actions, tabbed sections, collapsed navigation affordances, and modal-driven add flows. This story adapts the reference shell pattern without pulling in unimplemented product domains.

## Functional Requirements

- Users can navigate between available product areas through a persistent app shell.
- The app shell supports at least Overview and Inventory destinations immediately.
- Destinations for future areas may be shown only if they are clearly disabled, hidden, or treated as future scope.
- Users can access primary actions such as adding inventory from the shell.
- The shell remains usable in desktop and narrower browser widths.

## Technical Requirements

- Approach: Introduce focused frontend components for the shell/navigation rather than expanding the current monolithic `App.tsx` markup.
- Approach: Use `foodmaxd/frontend/src/components/Sidebar.tsx` and `foodmaxd/frontend/src/App.tsx` as interaction references for sidebar, topbar, active tab, and primary action placement.
- Decision: Build the shell as a frontend-only UX restructure first; do not add backend behavior solely for navigation.
- Decision: Keep future sections out of scope unless the linked feature story is ready to implement.
- Constraint: Do not add meal recommendations, shopping list intelligence, calendar planning, receipt import, or waste tracking behavior in this story.
- Constraint: Follow `work/guidelines/frontend.md` once recorded.

## Acceptance Criteria

- The frontend has a persistent app shell with clear navigation between Overview and Inventory.
- Inventory add/edit flows remain available and functional after the shell restructure.
- Future navigation entries are absent or clearly non-interactive unless backed by implemented routes/pages.
- Shell and navigation components live under `frontend/src/components/` or another clearly named frontend component boundary.
- `npm run build` succeeds from `frontend/`.
