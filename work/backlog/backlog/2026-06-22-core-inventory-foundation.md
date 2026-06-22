# Core Inventory Foundation

## Type

feature

## Context

The app goal is to minimize food waste by helping users understand what food they have, when it may expire, and what needs attention. The inventory is the foundation for later expiry awareness, meal recommendations, shopping-list suggestions, and waste-behavior insights.

Inventory items represent actual food currently owned by the user. Foodstuffs represent reusable food configuration used for suggestions and defaults, such as category and the expected expiry range for that type of food.

## Functional Requirements

- Users can add food items to inventory.
- Users can edit existing inventory items.
- Users can remove inventory items.
- Inventory items capture at least name, category, quantity, purchase date, and estimated expiry date.
- Users can view inventory sorted by expiry date.
- Users can view or group inventory by product category.
- Users can select from configured foodstuff suggestions while adding an item.
- Users can quickly create a new foodstuff when no suitable suggestion exists.
- Foodstuff configuration captures a default estimated expiry range using minimum and maximum days.
- Selecting a configured foodstuff can provide defaults for the inventory item, while still allowing item-specific values to be adjusted.

## Technical Requirements

- Decision: Build inventory before recommendations, shopping intelligence, or meal planning because those features depend on reliable item data.
- Decision: Treat expiry date as an estimate, not a guarantee, matching the brainstormed product concept.
- Decision: Include category and quantity in the core item model so later overview, low-stock, and meal-planning features have usable data.
- Decision: Treat foodstuffs as general reusable configuration about a type of food, not as the actual owned inventory item.
- Decision: Model foodstuff expiry guidance as an estimated range with minimum and maximum days, rather than a single fixed duration.
- Decision: Inventory items may use foodstuff defaults, but item-specific details such as purchase date, quantity, category, and estimated expiry date remain editable for the actual owned item.
- Decision: Removing an item removes it from active inventory and does not record eaten or wasted behavior; eaten and wasted outcomes belong to the expiry and waste awareness story.
- Rejected alternative: Start with recipes or meal planning first; rejected because those features need inventory data to be useful.
- Rejected alternative: Treat foodstuff suggestions as labels only; rejected because later expiry defaults and category grouping need reusable food configuration.
- Constraint: UX should remain clean, uncluttered, and suitable for dark mode.
- Constraint: Expiry-related copy and UI should avoid presenting estimated dates as food-safety guarantees.
- Constraint: Full foodstuff configuration management beyond quick creation and reusable defaults may be deferred unless explicitly included in implementation scope.

## Acceptance Criteria

- A user can create an inventory item with required inventory fields.
- A user can update an inventory item after creation.
- A user can remove an inventory item.
- Inventory can be ordered by estimated expiry date.
- Inventory can be viewed or grouped by category.
- Foodstuff suggestions are available while adding inventory.
- If no matching foodstuff exists, the user can start creating one from the add flow.
- Foodstuff suggestions can carry default category and estimated expiry range values.
- A foodstuff expiry range stores both minimum and maximum day values.
- Inventory items created from a foodstuff suggestion can still have item-specific values adjusted.
- Removing an inventory item does not count as marking it eaten or wasted.

## Analysis

### Likely Impact

- Primary implementation lane: new runtime scaffold -> FastAPI inventory/foodstuff API -> SQLAlchemy/PostgreSQL persistence models -> React TypeScript inventory UI.
- `work/project-config.md` - confirms the planned backend stack is Python, FastAPI, SQLAlchemy, and PostgreSQL, and the frontend stack is React with TypeScript.
- `work/project-config.md` - confirms application runtime code layout is not yet present, so implementation will likely need to create the first backend and frontend project structure before feature code can land.
- Backend data model/API - likely first layer to define `Foodstuff` reusable configuration separately from `InventoryItem`, preserving the story decision that foodstuffs are not owned inventory.
- Frontend inventory flow - likely needed to satisfy add/edit/remove, expiry sorting, category grouping, suggestion selection, and quick foodstuff creation from the add flow.

### Possible Adjacent Touchpoints

- Database migration setup - likely needed if the backend scaffold includes persistent PostgreSQL schema management; repo command rules do not yet define migration commands.
- API contract types/schemas - likely needed for inventory item create/update/list/delete and foodstuff suggestion/quick-create flows.
- Frontend API client/state layer - may be needed so the React UI can call the FastAPI endpoints consistently.
- `work/backlog/backlog/2026-06-22-expiry-and-waste-awareness.md` - adjacent dependency because later eaten/wasted outcomes must remain separate from simple inventory removal.
- `work/backlog/backlog/2026-06-22-shopping-list-intelligence.md` - adjacent dependency because low-stock suggestions depend on the quantity model chosen here.

### Existing Patterns / Prior Art

- `work/project-config.md` - closest implementation guidance; it defines logical backend, frontend, and cross-domain model domains plus stack expectations.
- `brainstom.md` - product prior art for inventory ordering, foodstuff suggestions, quick foodstuff creation, and per-foodstuff expiry configuration.
- No close runtime code prior art was found; there are no existing Python, TypeScript, FastAPI, SQLAlchemy, or React files in the repo yet.

### Layer Boundaries

- Touch first: runtime scaffolding, backend persistence models, backend API endpoints/schemas, frontend inventory UI, and frontend add/edit form flows.
- Touch first: shared model definitions around `InventoryItem`, `Foodstuff`, `category`, `quantity`, `purchaseDate`, and `estimatedExpiryDate` because later stories depend on these concepts.
- Avoid unless evidence emerges: meal recommendations, meal planning calendar, shopping-list intelligence, waste metrics, eaten/wasted event tracking, photo-based expiry extraction, and a full standalone foodstuff configuration page beyond quick creation/default reuse.
- Avoid unless evidence emerges: marking items eaten or wasted during removal; the story explicitly keeps removal separate from those later outcomes.

### Verification Plan

**Unit Tests**:

- Verify foodstuff expiry ranges require both minimum and maximum day values and reject invalid ranges such as maximum below minimum.
- Verify inventory item create/update behavior keeps item-specific values editable even when created from a foodstuff suggestion.
- Verify removal removes the item from active inventory without creating eaten or wasted semantics.

**Integration Tests**:

- Verify inventory CRUD through the API, including create, update, list, and remove behavior.
- Verify list ordering by estimated expiry date and category grouping/filtering behavior.
- Verify add-item flow can retrieve foodstuff suggestions and quick-create a new foodstuff for future selection.

**E2E / Manual Validation**:

- Add an inventory item from an existing foodstuff suggestion and confirm defaults are applied but editable.
- Add an inventory item by quick-creating a new foodstuff when no suitable suggestion exists.
- Confirm inventory can be viewed sorted by expiry date and grouped or viewed by category in a clean, dark-mode-suitable UI.

**Additional Checks (as applicable)**:

- Confirm the chosen quantity representation is sufficient for later low-stock and shopping-list behavior before broadening implementation into those features.
- Confirm the database schema preserves the boundary between reusable foodstuff configuration and actual owned inventory items.

## Implementation feedback (2026-06-22 13:12)

* Gate result: FAIL.
* Quick-created foodstuff defaults are not reliably applied to the in-progress inventory form. In `frontend/src/App.tsx`, `submitFoodstuff` awaits `refresh()` and then calls `applySelectedFoodstuff(String(foodstuff.id))`, but `applySelectedFoodstuff` reads from the stale `foodstuffs` state captured before the refresh. The new foodstuff id is selected, but name, category, and estimated expiry can remain empty until the user manually changes the selection again. This leaves the acceptance criteria for quick-create/add-flow defaults insufficiently implemented for newly created suggestions.
* Required validation commands could not be completed in this environment: `python -m pytest backend/tests` failed with `python: command not found`, and `npm run build` from `frontend/` failed with `npm: command not found`. Re-run both commands after installing the required local tooling/dependencies.
