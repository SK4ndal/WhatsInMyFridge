# Project Config

This file is the canonical, human-readable source of truth for repo structure, guideline loading, review triggers, and repo-level command rules.

If another repo document conflicts with this file, follow this file.

## Purpose

- Use this file as rule, not background reading.
- Humans read it to understand expected agent behavior.
- Agents read it to decide which guidelines, reviews, and commands apply.

## Repo Structure

- Top-level layout is minimal: `.opencode/` holds the workflow implementation, `work/` holds durable project artifacts, and `README.md` describes the framework.
- `.opencode/agent/` contains the primary agent definitions for the workflow.
- `.opencode/commands/` contains command entry points such as `init`, `refresh-project-config`, `change`, `commit`, `create-guideline`, and `release`.
- `.opencode/skills/` contains reusable skills such as `record-story`, `record-idea`, `record-guideline`, `record-adr`, and `agent-browser`.
- `.opencode/custom/init/` contains the repo bootstrap assets, including `init.sh`, prompt reference files, and the project README source.
- `.opencode/scripts/` contains support scripts used by workflow automation.
- `work/project-config.md` is the main repo-local operating context file.
- `work/backlog/backlog/`, `work/backlog/planned/`, `work/backlog/in-progress/`, and `work/backlog/done/` hold story state.
- `work/ideas/ideas/` and `work/ideas/Inbox.md` hold early-stage ideas.
- `work/guidelines/`, `work/adr/`, and `work/releases/` exist but currently contain only scaffold files.

## Output Rules

- Be concise.
- Start with action, not explanation.
- Use bullets instead of long paragraphs.
- No filler.
- Use structured output when possible.
- Keep sections short unless technical detail is required.

## Domain Rules

### Workflow Definition

- Guideline: none currently present under `work/guidelines/`
- Patterns: `.opencode/agent/**/*`, `.opencode/commands/**/*`, `.opencode/skills/**/*`, `.opencode/scripts/**/*`
- Keywords: `agent`, `command`, `skill`, `workflow`, `orchestrator`, `validator`

### Work Artifacts

- Guideline: none currently present under `work/guidelines/`
- Patterns: `work/project-config.md`, `work/backlog/**/*`, `work/ideas/**/*`, `work/adr/**/*`, `work/releases/**/*`
- Keywords: `story`, `backlog`, `idea`, `adr`, `release`, `project config`

### Bootstrap and Prompt Assets

- Guideline: none currently present under `work/guidelines/`
- Patterns: `.opencode/custom/init/**/*`, `README.md`
- Keywords: `init`, `bootstrap`, `readme`, `prompt`, `guideline`

## Technology Rules

- Markdown is the primary artifact format for agent definitions, commands, skills, and human-readable documentation.
- Shell scripting is used for bootstrap and support automation in `.opencode/custom/init/init.sh` and `.opencode/scripts/`.
- No language-specific build, test, or application runtime stack is verified outside the workflow assets above.

## Review Rules

- No dedicated review guideline files are currently present under `work/guidelines/`.
- Use repo-grounded review when changes affect agent instructions, command behavior, workflow bootstrap assets, or durable story state.
- If future review-specific guidelines are added under `work/guidelines/`, reference them here instead of inventing new review policy in prompts.

## Loading Rules

### Always Load

- Always load `work/project-config.md`.
- Load additional guideline files only when they exist and match the current task.

### Analysis

- Start from the affected area: `.opencode/` for workflow behavior.
- When `work/guidelines/` gains task-relevant files, load only the files that match the affected area.

### Implementation

- Use the affected file paths to choose the matching domain above.
- Treat `work/` artifacts as durable handoff material and `.opencode/` files as workflow implementation assets.
- Do not assume application runtime conventions that are not present in this repository.

### Validation

- If no guideline exists for the changed area, prefer repo structure and adjacent artifacts over invented policy.

## Command Rules

- No command rules.

## Agent Usage Rule

- Read this file first when you need repo structure, guideline loading rules, review triggers, or repo-level command rules.
- Load only the guideline files that match the current task.
- Do not invent rules outside this file and the loaded guideline files.
