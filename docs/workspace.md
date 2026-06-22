# Workspace

## The role of `work/`

`work/` is the repo-local workspace for planning, project context, delivery state, and decisions.

Its role is not just organizational. It makes the repository self-describing enough that AI can work more like a well-contextualized engineer.

Without something like `work/`, the missing context tends to be scattered across issue trackers, tribal knowledge, old chats, and one-off prompts. Humans can often recover from that. AI is much less reliable when forced to do so.

By moving that context into durable repo artifacts, the workflow becomes:

- inspectable in git
- reviewable by humans
- reusable across sessions
- easier to automate safely
- easier to open source because the process is visible

## Typical `work/` structure

```text
work/
|- project-config.md
|- README.md
|- backlog/
|  |- backlog/
|  |- planned/
|  |- in-progress/
|  `- done/
|- guidelines/
|- adr/
|- ideas/
`- releases/
```

## What the main areas are for

- `work/project-config.md` is the main operating context for agents
- `work/backlog/backlog/` holds backlog stories
- `work/backlog/planned/` is an optional staging area for likely next work
- `work/backlog/in-progress/` holds stories currently in delivery
- `work/backlog/done/` holds completed story history
- `work/guidelines/` holds compact repo-specific engineering rules
- `work/adr/` holds Architecture Decision Records
- `work/ideas/` holds rough concepts that are not ready to become stories
- `work/releases/` holds release artifacts and grouped completed work

## Why `work/project-config.md` matters

`work/project-config.md` is the AI's operating map of the repository.

This information is intentionally not kept in `AGENTS.md`.

- `AGENTS.md` gives the stable, high-level workflow overview (what this project is and general repo structure).
- `work/project-config.md` holds execution-critical, repo-specific operating detail used during implementation and validation.

Keeping them separate avoids sending heavy, fast-changing operational rules to every agent invocation.

- `AGENTS.md` stays small and durable as the general contract.
- `work/project-config.md` can evolve with engineering process details without bloating the global agent prompt.
- Agents load `work/project-config.md` when they need to perform software-delivery work, so they follow current local rules instead of guessing.

Instead of forcing the model to infer structure and rules each time, the workflow gives it one file that answers questions like:

- how the repo is organized
- which guideline files apply to which kinds of work
- which review triggers matter
- which validation commands are canonical
- which generated artifacts need special handling

In practice, this file often contains:

- repo structure
- domain rules that map keywords and file patterns to guidelines
- technology rules
- review rules for higher-risk topics
- loading rules for analysis, implementation, and validation
- command rules for verification and code generation

## Why `work/guidelines/` exists

`work/guidelines/` encodes local engineering judgment in a form that is small enough to load selectively and concrete enough to change execution.

These files should act like senior-team pointers, not long tutorials.

- Keep guidance compact and directive.
- Nudge the AI on what to do and what to avoid.
- Focus on expectations, constraints, and decision rules.
- Avoid dumping many examples unless they are truly needed to prevent repeat mistakes.

The model already knows general coding patterns; guidelines are for repo-local ways of working.

- Think of this as onboarding notes for an experienced developer joining the team.
- Provide enough context to align behavior quickly.
- Let the AI adapt its execution from those pointers.

This is where a repository captures the local rules that a long-time contributor already knows, such as:

- expected directory structure
- preferred or forbidden abstractions
- generated code handling
- test expectations for different changes
- mistakes that have already caused trouble before

For how these artifacts are used across phases, see `docs/flows.md`. For the agent roles that read and update them, see `docs/agents.md`.
