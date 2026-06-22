# Agents

Agents are the primary workflow roles. They are the conceptual center of AiFact.

Each agent has a narrow job, reads repo context before acting, and leaves a durable artifact or state change for the next phase instead of relying on chat memory.

## Core delivery agents

### `brainstorm`

The normal entry point for delivery work. It clarifies what should be built before implementation planning begins.

In traditional software development terms, this is where the product owner and tech lead (or team) align functional intent with technical context to decide what should be built.

- Reads repo context first, especially `work/project-config.md`
- Stays in concept-refinement mode rather than implementing
- Can record docs and work artifacts under `work/`, `docs/`, and `.opencode/` when asked

### `story-reviewer`

Pressure-tests an existing story for hidden complexity, risky assumptions, unclear wording, and likely failure modes.

In traditional software delivery, this step is often skipped or deferred until implementation starts, which is one reason stories can expand unexpectedly when missed details surface. It may also happen during sprint planning or planning poker, but usually with less focused depth.

- Used after a story exists, not for first-pass ideation
- Challenges the draft rather than rewriting broad product intent

### `story-start`

Moves drafted work into active delivery and establishes the starting point for the rest of the flow.

In traditional software development, this is typically just moving a Jira ticket from planned to doing.

- Accepts stories from `work/backlog/backlog/` or `work/backlog/planned/`
- Moves the story to `work/backlog/in-progress/`
- Creates or reuses the working branch and records the kickoff in git

### `story-analyzer`

Identifies where in the repo the story should be implemented and writes repo-grounded analysis into the story.

In traditional delivery, this often happens informally in a developer's head; for larger stories, developers may sketch or inspect code first to identify likely changes. Sometimes it is skipped and implementation begins from an initial touchpoint, then evolves during coding.

- Finds the primary implementation lane and likely adjacent touchpoints
- Adds or updates the `## Analysis` section in the story
- Optimizes for scoping implementation, not redesigning the feature

### `story-implementer`

Executes story-driven changes against the recorded analysis and repo-local rules.

In traditional software development, this corresponds to the developer implementing the story.

- Requires `## Analysis` to exist before implementation starts
- Treats repo-configured commands as the verification source of truth
- Can use `story-builder` only for rare, clearly bounded execution slices

### `story-validator`

Acts as the release gate. It gathers proof and decides whether the story passes, fails, or is blocked.

In traditional software delivery, this is where multiple checks happen: linting, automated tests, and technical/security checks (for example SAST). It is also where the delivered behavior is validated manually by a developer, QA, or tester to confirm the implementation actually works.

- Turns the story into an explicit validation checklist
- Prefers the narrowest credible proof surface first
- Appends either `## Implementation feedback` or `## Validation update` to the story

### `story-done`

Closes validated work by moving the story into done state and preparing final closure.

In many real-world teams, "done" is tied to deployment status. For this workflow, it is intentionally scoped to coding completion and successful checks.

- Requires a successful validation update before closeout
- Moves the story to `work/backlog/done/`
- Commits the completed story work when the staged scope is clean

### `story-pr`

Owns the pull request and CI follow-through phase.

In traditional software workflows, PR handling can vary. Often, most technical checks already happened during validation, so PR stage checks are lighter and focused on integration/review flow rather than first-pass verification.

- Creates or reuses the GitHub PR for the current branch
- Waits for checks through the repo-local wait script
- Allows limited recovery for CI-owned failures, but not broad product-code rework

## Supporting agents

### `story-builder`

A bounded helper that `story-implementer` can use for a rare separable slice. It is not a normal workflow phase.

- Used only when a slice has clear file boundaries and limited dependency edges
- Returns control to `story-implementer`, which still owns the story

### `browser-validator`

Handles browser-specific validation evidence when a story needs visible UI proof or focused E2E debugging.

- Covers only the browser-specific subset of validation
- Works alongside `story-validator`, not instead of it

### Orchestrators

Because OpenCode does not provide another native mechanism for workflow loops and multi-phase flow control, using orchestrator agents is the most practical way to run these sequences reliably.

- `story-execute-orchestrator` runs the story flow through validation
- `story-ship-orchestrator` runs the full story flow through closure and PR follow-through

These orchestrators re-read the story between phases and use the recorded artifact as the authority.

### Additional specialized agents

- `ad-hoc-implementer` for bounded changes that do not need a story
- `external-ideas-reviewer` for repo improvement review with vendor-neutral wording (an intentional exception to strict role-specific agents, used to gather technical or functional feedback from other models for inspiration)
- `lightweight-command-runner` for narrow fixed command flows

For the order these agents appear in delivery, see `docs/flows.md`.
