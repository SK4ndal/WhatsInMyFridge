# Shopping List Intelligence

## Type

feature

## Context

The shopping list should help users buy what they need while avoiding repeated overbuying and waste. Suggestions should be based on low stock, planned meals, and previous expiration or waste behavior.

## Functional Requirements

- Users can maintain a shopping list.
- Users can add low-stock items to the shopping list.
- Users can add items needed for planned meals to the shopping list.
- The shopping list can show suggested items based on low stock.
- The shopping list can show suggested items based on planned meals.
- The shopping list can suggest behavior improvements based on previous waste or expiration patterns.
- Users can decide whether to accept suggested shopping-list items.

## Technical Requirements

- Decision: Suggestions should be user-confirmed rather than silently added, to keep user control over buying behavior.
- Decision: Low-stock and planned-meal suggestions should be separate suggestion reasons so users understand why an item appears.
- Decision: Waste-pattern suggestions depend on recorded waste events from the expiry and waste awareness story.
- Rejected alternative: Fully automatic shopping-list generation; rejected because it may create unwanted purchases and undermine waste reduction.
- Constraint: Shopping suggestions should not require advanced meal planning to be useful; low-stock suggestions should work independently.

## Acceptance Criteria

- A user can add and manage shopping-list items.
- Low-stock inventory items can be suggested for the shopping list.
- Planned-meal ingredients can be suggested for the shopping list when meal planning data exists.
- Waste-related suggestions explain the behavior pattern that caused the suggestion.
- Suggested items require user confirmation before becoming active shopping-list items.
