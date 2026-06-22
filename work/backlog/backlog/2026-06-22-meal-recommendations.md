# Meal Recommendations

## Type

feature

## Context

Meal recommendations should help users consume inventory before it is wasted. Recommendations should prioritize food already available, especially items close to estimated expiry, while allowing users to filter based on practical constraints such as portion size and allergies.

## Functional Requirements

- Users can view meal recommendations based on current inventory.
- Recommendations prioritize ingredients close to estimated expiry.
- Users can filter recommendations by allergy constraints.
- Users can specify or view portion size.
- Users can favorite recipes.
- Users can create their own recipes.
- Recipes can be grouped by breakfast, lunch, and dinner.
- Recipes can be grouped or filtered by cuisine or country of origin.

## Technical Requirements

- Decision: Meal recommendations should consume inventory and expiry data rather than operate as a standalone recipe catalog.
- Decision: Allergy filtering should be explicit in the recommendation flow because it affects whether a suggested meal is usable.
- Decision: User-created recipes should be supported so recommendations can improve around household-specific meals.
- Rejected alternative: Build only a static recipe list; rejected because the product goal is waste reduction through inventory-aware recommendations.
- Constraint: Recommendation ranking should favor soon-to-expire inventory, but should not hide other usable meals entirely unless filters require it.

## Acceptance Criteria

- Recommended meals are derived from current inventory.
- Meals using soon-to-expire ingredients are prioritized.
- Allergy filters affect visible recommendations.
- Users can mark recipes as favorites.
- Users can create recipes.
- Recipes support meal-type grouping.
- Recipes support cuisine or country-of-origin grouping.
