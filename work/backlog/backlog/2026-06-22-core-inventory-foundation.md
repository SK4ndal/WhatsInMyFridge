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
