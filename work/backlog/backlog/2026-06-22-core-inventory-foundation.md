# Core Inventory Foundation

## Type

feature

## Context

The app goal is to minimize food waste by helping users understand what food they have, when it may expire, and what needs attention. The inventory is the foundation for later expiry awareness, meal recommendations, shopping-list suggestions, and waste-behavior insights.

## Functional Requirements

- Users can add food items to inventory.
- Users can edit existing inventory items.
- Users can remove inventory items.
- Inventory items capture at least name, category, quantity, purchase date, and estimated expiry date.
- Users can view inventory sorted by expiry date.
- Users can view or group inventory by product category.
- Users can select from configured foodstuff suggestions while adding an item.
- Users can quickly create a new foodstuff when no suitable suggestion exists.

## Technical Requirements

- Decision: Build inventory before recommendations, shopping intelligence, or meal planning because those features depend on reliable item data.
- Decision: Treat expiry date as an estimate, not a guarantee, matching the brainstormed product concept.
- Decision: Include category and quantity in the core item model so later overview, low-stock, and meal-planning features have usable data.
- Rejected alternative: Start with recipes or meal planning first; rejected because those features need inventory data to be useful.
- Constraint: UX should remain clean, uncluttered, and suitable for dark mode.

## Acceptance Criteria

- A user can create an inventory item with required inventory fields.
- A user can update an inventory item after creation.
- A user can remove an inventory item.
- Inventory can be ordered by estimated expiry date.
- Inventory can be viewed or grouped by category.
- Foodstuff suggestions are available while adding inventory.
- If no matching foodstuff exists, the user can start creating one from the add flow.
