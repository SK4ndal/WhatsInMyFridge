# Extend Inventory Item Details for Dashboard UX

## Priority

P1 - Implement before dashboard, inventory browsing polish, and receipt import because those stories depend on the accepted inventory fields.

## Type

feature

## Context

The reference project models inventory with fields that support richer dashboard and shopping experiences: location, quantity remaining, total quantity, unit, item value, opened state, and notes. The current project captures name, category, quantity amount/unit, purchase date, estimated expiry date, and optional foodstuff linkage. In product terms, that foodstuff linkage points to reusable food default settings that can prefill inventory-item fields without being inventory themselves. This story decides which additional item details should become part of this product’s durable inventory model and which of those details should also be supported as reusable defaults.

## Functional Requirements

- Users can capture where an inventory item is stored, such as fridge, freezer, pantry, or counter.
- Users can distinguish current quantity from original quantity when that distinction is needed for low-stock behavior.
- Users can optionally capture item cost or estimated value for future waste-value metrics.
- Users can optionally capture whether an item has been opened.
- Users can optionally capture notes for an inventory item.

## Technical Requirements

- Approach: Review `foodmaxd/frontend/src/types.ts` and `foodmaxd/backend/app/models/food.py` as references for richer inventory fields.
- Approach: Update backend schemas, persistence model, API tests, frontend types, and inventory forms together so the contract remains aligned.
- Decision: Keep existing foodstuff/default settings separate from actual owned inventory items.
- Decision: Treat value, location, opened state, and notes as optional product enhancers unless the implementation analysis finds they are required for a linked story.
- Constraint: Do not implement low-stock recommendations, waste value dashboards, or receipt import in this story; only unblock them with data model support.
- Constraint: Confirm migration strategy before changing persisted schema, because database migration commands are not yet defined in `work/project-config.md`.

## Acceptance Criteria

- Inventory items can store a location value if the field is accepted during analysis.
- Inventory items can store current and original quantity if the field split is accepted during analysis.
- Inventory items can store optional value, opened state, and notes if accepted during analysis.
- Frontend inventory add/edit forms expose accepted fields without cluttering the primary add flow.
- Backend request/response schemas and frontend TypeScript types remain aligned.
- Existing inventory CRUD tests are updated for the accepted model changes.
- `python -m pytest backend/tests` succeeds from the repo root.
- `npm run build` succeeds from `frontend/`.
