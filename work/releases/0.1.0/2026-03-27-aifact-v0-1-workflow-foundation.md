# AiFact v0.1 Workflow Foundation

## Type

feature

## Context

AiFact currently implements the core repo-local workflow scaffold for artifact-based AI delivery. This story captures the implemented v0.1 baseline as a single high-level epic for release planning, focused on the workflow foundation that already exists rather than future expansion.

## Functional Requirements

- Provide bootstrap support for initializing the repo-local workflow scaffold.
- Provide durable artifact recording for stories, ideas, guidelines, and ADRs.
- Define a documented story lifecycle from brainstorming through validation, closeout, and PR handling.
- Provide command entry points for workflow bootstrap, project-config refresh, guarded commits, ad-hoc change capture, and release preparation.
- Provide workflow-level support for browser validation and PR/CI follow-through.

## Technical Requirements

- Treat `work/` as the durable source of truth for project context, backlog state, and release artifacts.
- Treat `.opencode/` as the workflow implementation surface for agents, commands, skills, scripts, and bootstrap assets.
- Keep the workflow artifact-first, with narrow agent roles and explicit handoffs instead of hidden chat state.
- Keep validation as a gate in the defined delivery flow.
- Scope v0.1 to the implemented workflow scaffold and supporting docs, not to populated backlog history, completed release history, or application-runtime integration.
- Keep this epic intentionally high level; detailed behavior remains in the workflow docs and implementation artifacts.

## Acceptance Criteria

- The repository can bootstrap a `work/` workspace with initial workflow artifacts and docs.
- The repository defines a documented story-driven workflow from `brainstorm` through `story-pr`.
- The repository includes recording support for story, idea, guideline, and ADR artifacts.
- The repository includes command support for initialization, project-config refresh, guarded commit flow, ad-hoc non-feature change capture, and release preparation.
- The repository includes workflow support for browser-based validation and PR/CI follow-through.
- v0.1 is understood as the implemented workflow foundation, not as proof of populated project history or application feature delivery.
