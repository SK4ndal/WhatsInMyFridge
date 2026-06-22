# Upgrade Inventory Browsing Experience

## Priority

P4 - Implement after the shell and accepted inventory fields, because browsing controls should reflect the final near-term item model.

## Type

feature

## Context

The current inventory UI supports add/edit/remove plus expiry and category views. The `foodmaxd` reference inventory page adds a more dashboard-like browsing experience with search, category/location filters, sort controls, grid/list modes, and compact item cards. This story adapts the browsing experience while staying within the current inventory domain.

## Functional Requirements

- Users can search active inventory by item name.
- Users can filter active inventory by category.
- Users can sort active inventory by estimated expiry and name.
- Users can switch between compact card/grid and list-style inventory views.
- Inventory cards or rows show the item’s quantity, category, and estimated expiry clearly.

## Technical Requirements

- Approach: Use `foodmaxd/frontend/src/components/Inventory.tsx`, `FoodTile.tsx`, and `FoodRow.tsx` as references for controls and component boundaries.
- Approach: Prefer client-side filtering and sorting initially if the active inventory list remains small; add backend query support only when needed for acceptance criteria or performance.
- Decision: Keep this story focused on browsing and presentation; do not add consume/waste actions.
- Decision: Reuse current API fields unless the separate inventory-details story expands the model.
- Constraint: Do not add receipt import, food catalog management, location filters, value sorting, or low-stock behavior unless their prerequisite stories are implemented.
- Constraint: Preserve existing foodstuff suggestion and quick-create flows.

## Acceptance Criteria

- A user can search active inventory by name.
- A user can filter active inventory by category.
- A user can sort active inventory by estimated expiry and name.
- A user can switch between at least two inventory presentation modes.
- Existing create, edit, remove, foodstuff suggestion, and quick-create behavior still works.
- `npm run build` succeeds from `frontend/`.
