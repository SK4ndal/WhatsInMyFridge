# Frontend Guidelines

## Principles
- Keep page-level state in `App.tsx` only until a story justifies a narrower state module.
- Split durable UI areas into focused components under `frontend/src/components/`.
- Keep shared DTOs in `frontend/src/types.ts` aligned with FastAPI response shapes.
- Keep API access behind `frontend/src/api.ts`; avoid raw fetch calls in components.
- Prefer dashboard cards, queues, filters, and modals that mirror the reference app without copying unscoped features.
- Preserve expiry language as estimated guidance, not food-safety certainty.
- Run `npm run build` for frontend changes.

## Pitfalls
- Do not add meal, shopping, calendar, receipt, or waste behavior inside unrelated UI polish stories.
- Do not grow `App.tsx` with large page markup when a named component boundary is clear.
- Do not introduce browser-only persisted state without a story-level reason.

## Decisions
- Use `foodmaxd/frontend/src/` as visual and interaction reference, not as source to copy verbatim.
- Keep frontend implementation dependency-light unless a story explicitly accepts a new package.
