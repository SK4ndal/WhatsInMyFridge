# Meal Planning Calendar

## Type

feature

## Context

Meal planning connects recipes, inventory, and shopping-list suggestions. Planned meals should help users understand which ingredients are reserved for future meals and what still needs to be bought.

## Functional Requirements

- Users can plan meals on a calendar.
- Users can mark planned meals as eaten.
- Inventory items used in planned meals display a planned indicator.
- Planned indicators link back to the related meal or recipe.
- Users can select a date and see which inventory items are planned or reserved for that date, plus any food defaults or recipe ingredients that still need to be bought.
- Inventory items can be visually greyed out when reserved for planned meals.
- Missing ingredients from planned meals can feed shopping-list suggestions.

## Technical Requirements

- Decision: Meal planning should be built after inventory and recipes because it links both domains.
- Decision: Planned inventory indicators should remain navigable so users can understand why an item is reserved.
- Decision: Marking a meal as eaten should be considered an inventory-impacting event, but exact deduction behavior needs confirmation before implementation.
- Rejected alternative: Calendar-only planning without inventory linkage; rejected because it would not support the waste-reduction and shopping-list goals.
- Constraint: Calendar interactions should remain simple and avoid cluttering the inventory view.

## Acceptance Criteria

- A user can add a meal to a calendar date.
- A user can mark a planned meal as eaten.
- Inventory items tied to planned meals show a planned indicator.
- Planned indicators link to the relevant meal or recipe.
- Date selection can show planned or reserved inventory items and missing ingredients derived from recipes or food defaults.
- Planned-meal missing ingredients can be suggested for the shopping list.
