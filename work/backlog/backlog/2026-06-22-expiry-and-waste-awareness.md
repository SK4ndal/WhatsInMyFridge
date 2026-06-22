# Expiry and Waste Awareness

## Type

feature

## Context

The product should reduce food waste by surfacing items that are close to expiry and by helping users understand waste behavior over time. Expiry dates are estimates, so the app should communicate uncertainty rather than presenting expiry as an absolute safety guarantee.

## Functional Requirements

- Users can see which items are expiring soon.
- Users can see which items are expired or past their estimated expiry date.
- Users can mark inventory items as eaten.
- Users can mark inventory items as wasted or discarded.
- The overview screen shows 30-day waste behavior.
- The overview screen shows most wasted items.
- The overview screen shows estimated expired value when item value data is available.
- Expiry status uses a visual gradient or warning treatment as the estimated expiry date approaches.
- The app displays “look, smell, taste” style warning language near expiry guidance.

## Technical Requirements

- Decision: Track item outcomes separately from deletion so eaten and wasted behavior can be measured.
- Decision: Present expiry as estimated, using warning copy to avoid implying food safety certainty.
- Decision: Capture waste events early because future shopping suggestions depend on previous waste behavior.
- Rejected alternative: Only delete items when they leave inventory; rejected because it loses waste-behavior data.
- Constraint: Waste metrics should be understandable without cluttering the overview screen.

## Acceptance Criteria

- Items approaching estimated expiry are visually distinguishable.
- Expired or past-estimate items are visible to the user.
- A user can mark an item as eaten.
- A user can mark an item as wasted or discarded.
- Waste actions contribute to 30-day waste behavior metrics.
- Most wasted items can be surfaced from recorded waste behavior.
- Expiry-related UI makes clear that dates are estimates.
