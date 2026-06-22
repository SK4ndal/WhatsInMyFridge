# Overview

## What AiFact is

AiFact is a repo-local framework for running software delivery with AI in a way that stays explicit, reviewable, and durable.

It does not try to replace software engineering with something new. It encodes the parts of good engineering that experienced developers already do, especially the context that usually lives in their heads:

- clarifying what should be built before coding starts
- understanding how the repository is organized
- applying local conventions and quality rules
- choosing safe implementation boundaries
- handing work off between phases without losing context
- validating whether work is actually done

## Why it exists

Experienced engineers rarely start from zero. They already know the project history, the architecture, the local conventions, and the common failure modes.

AI usually does not.

The core problem AiFact addresses is not how to make a model generate code faster. It is how to give the model the durable context and working structure that a strong engineer already has.

That is why AiFact is artifact-based:

- project context lives in repo files
- work state lives in repo files
- reviews and decisions live in repo files
- handoffs happen through repo files

## How it works

The workflow is centered on one idea: the AI should not rely on hidden state as the source of truth.

Instead, the source of truth is a repo artifact, usually a story under `work/backlog/`. Each phase reads the current artifact, updates the section it owns, and leaves a durable handoff for the next phase.

In practice:

- `brainstorm` clarifies what should be built
- `record-story` turns the result into a durable work artifact
- `story-reviewer` pressure-tests the story when needed
- `story-analyzer` maps the story onto the repo and writes implementation analysis
- `story-implementer` executes the change against that analysis
- `story-validator` decides whether the work passes, fails, or is blocked
- `story-done` and `story-pr` close the loop after validation passes

For the shape of `work/`, see `docs/workspace.md`. For the phase order and delivery loops, see `docs/flows.md`.

## Why this differs from many AI coding setups

There are a few common ways people work with AI today.

One is plain ad hoc prompting, sometimes called vibe coding: describe a change, see what the model does, tweak the prompt, and keep iterating in chat. That can feel fast, especially for prototypes and small isolated tasks.

The weakness is that the model often starts each turn with limited durable context. The user has to keep re-explaining the local rules, preferred style, constraints, and boundaries. Over time that can lead to drift in structure, inconsistent implementation choices, and a lot of repeated prompting.

Another pattern is the long-running general-purpose coding session: one agent, one long conversation, and a large amount of context accumulated in chat. That can work well for a while, but it becomes fragile when the work needs:

- durable handoffs
- repeatable validation
- project-specific rules
- auditability
- onboarding for new humans or new models

There are also more structured frameworks that push the work through specs, plans, tasks, or multiple agent roles. For example, Spec Kit presents itself as a toolkit for Spec-Driven Development with stages such as specify, plan, tasks, and implement, and it supports many different AI agents. BMAD presents itself as an AI-driven agile framework with structured workflows and specialized agents across the lifecycle.

AiFact is not different because it is the only workflow with phases or the only workflow with multiple agents. The difference is in the tradeoffs it makes.

AiFact is intentionally narrower and more opinionated:

- it is tuned for fixed OpenAI GPT model families for consistency in prompt behavior
- it treats repo artifacts as the durable source of truth instead of the chat transcript
- it models work as the same explicit steps a senior developer normally follows: clarify, record, review when needed, analyze, implement, validate, and close
- it uses `work/project-config.md` to tell agents what repo context and rules they should load
- it uses compact guideline files that are loaded selectively based on the task, so the workflow can inject local policy without restating everything on every run

That selective loading matters. The goal is not to repeat generic advice the model already knows. The goal is to add the small amount of repo-specific guidance that materially changes outcomes: local rules, preferred abstractions, generated-code handling, validation commands, and known pitfalls.

So the core distinction is not that AiFact is more complex. It is that AiFact tries to make AI work more like a disciplined senior engineer working inside a real repository, with explicit context, explicit handoffs, and explicit validation.

For onboarding, see `docs/getting-started.md`. For model-targeting and prompt reference notes, see `docs/prompting.md`.
