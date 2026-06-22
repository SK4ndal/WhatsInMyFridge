# Clarify workflow docs for context loading and guideline intent

## Type

docs

## Context

Core documentation was updated to make workflow expectations easier to interpret during AI-assisted delivery. The changes clarify how project-level context should be split between `AGENTS.md` and `work/project-config.md`, how `work/guidelines/` should be authored as concise behavior nudges, and how several agent/flow descriptions map to common software-delivery practice.

## Functional Requirements

- Document why `work/project-config.md` carries execution-critical operating rules instead of `AGENTS.md`.
- Document that `work/guidelines/` should provide compact, expectation-focused pointers rather than long general tutorials.
- Improve workflow docs with clearer framing across agent roles, flow boundaries, and skill-authoring intent.

## Technical Requirements

- Restrict changes to documentation artifacts under `docs/` and a done-story record under `work/backlog/done/`.
- Keep guidance aligned with repository-local workflow behavior and avoid introducing product feature requirements.
- Preserve existing document structure while inserting concise clarifications in relevant sections.

## Acceptance Criteria

- `docs/workspace.md` explicitly explains the separation between `AGENTS.md` and `work/project-config.md` responsibilities.
- `docs/workspace.md` explicitly frames `work/guidelines/` as compact, team-style implementation guidance.
- Updated docs read as one coherent documentation clarification change rather than feature work.
