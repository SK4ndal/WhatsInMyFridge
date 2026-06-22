# Add Receipt Import Flow

## Priority

P5 - Implement after inventory item details and browsing are stable, because imported receipt items need the accepted item fields and a place to review results.

## Type

feature

## Context

The `foodmaxd` reference project includes a receipt upload flow that previews parsed receipt items before adding them to inventory. This can make the app feel closer to the reference project and reduce manual inventory entry, but it depends on a richer and stable inventory model plus clear user review before data is persisted.

## Functional Requirements

- Users can upload a receipt file from the inventory area.
- Users can preview parsed receipt items before they are added to inventory.
- Users can confirm or cancel the import.
- Imported items populate accepted inventory fields where possible.
- Users can see which receipt lines were skipped or could not be parsed.

## Technical Requirements

- Approach: Use `foodmaxd/backend/app/routers/items.py` receipt preview/import flow and `foodmaxd/frontend/src/components/Inventory.tsx` receipt modal as references.
- Approach: Start with text or structured receipt parsing unless OCR is explicitly accepted during implementation analysis.
- Decision: Require a preview/confirmation step before creating inventory items.
- Decision: Treat OCR as optional follow-up because it adds runtime dependencies and container implications.
- Constraint: Do not add receipt import before accepted inventory fields are finalized.
- Constraint: Do not silently add parsed items without user review.
- Constraint: Validate file size and accepted file types before parsing.

## Acceptance Criteria

- A user can select an accepted receipt file from the inventory UI.
- The app shows a parsed preview with item names and any mapped inventory fields before persistence.
- The user can cancel without creating inventory items.
- The user can confirm and create inventory items from the preview.
- Skipped or unparsed receipt lines are shown to the user.
- Backend tests cover receipt parsing, file-size validation, preview behavior, and confirmed import behavior if backend endpoints are added.
- `python -m pytest backend/tests` succeeds from the repo root if backend code changes.
- `npm run build` succeeds from `frontend/`.
