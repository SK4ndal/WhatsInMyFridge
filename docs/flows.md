# Flows

## Main story flow

The normal story-driven workflow looks like this:

1. `brainstorm`
2. `record-story`
3. optional `story-reviewer`
4. `story-start`
5. `story-analyzer`
6. `story-implementer`
7. `story-validator`
8. `story-done`
9. `story-pr`

The role details for these phases live in `docs/agents.md`. This page focuses only on sequence and handoff shape.

Important properties of this flow:

- `brainstorm` is the normal starting point
- brainstorming can produce large stories; the operator is responsible for applying software engineering judgment to keep stories appropriately bounded for reliable AI implementation
- recording the story creates the durable handoff artifact
- story review is optional but useful for risky or ambiguous work
- analysis happens before implementation
- validation is a gate, not a courtesy step
- the core loop is implement -> validate -> feedback -> implement
- closeout and PR phases happen only after validation passes

## Delivery loop

The central control loop of AiFact is the implementation and validation cycle:

1. `story-analyzer`
2. `story-implementer`
3. `story-validator`
4. if validation fails, append implementation feedback to the story
5. retry implementation against that feedback
6. close out only after validation passes

This loop matters because failure becomes part of the durable artifact rather than disappearing into chat history.

## Orchestrated flows

### Execute through validation

Use `story-execute-orchestrator` when you want AI to run the normal delivery phases but not automatically close the story or continue into PR handling.

### Ship through PR

Use `story-ship-orchestrator` when you want the full lifecycle handled from active story through PR and CI follow-through.

## Artifact flow

There are two main artifact paths:

- rough idea -> discussion, `record-idea`, or `record-story`
- story artifact -> in-progress -> validated -> done -> release

Repo-wide context artifacts follow a parallel path through:

- `refresh-project-config` for repo structure and command context
- `record-guideline` for engineering rules
- `record-adr` for architecture decisions

For the artifact locations themselves, see `docs/workspace.md`.
