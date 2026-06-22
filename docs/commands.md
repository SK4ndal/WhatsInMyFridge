# Commands

Commands are support entry points for common workflows. They are useful, but they are not the conceptual center of the system.

Most commands either run a narrow fixed sequence or hand control to a specific agent for a structured workflow.

## Main commands

### `init`

Initializes the workflow scaffold.

- Runs `.opencode/custom/init/init.sh`
- Creates the initial `work/` structure and bootstrap files

### `refresh-project-config`

Refreshes `work/project-config.md` from current repo state while preserving existing valid policy.

- Runs through `brainstorm`
- Updates only what can be verified from the repository
- Avoids inventing new policy

### `change`

Takes one finished non-feature change from the current worktree, records it as a done story, and commits it.

- Uses `ad-hoc-implementer`
- Works only for one coherent non-feature change
- Excludes `.opencode/` files from the inferred change set

### `commit`

Creates a guarded Conventional Commit from the current worktree.

- Uses `lightweight-command-runner`
- Refuses detached HEAD or `main`/`master`
- Stages all changes, checks for likely secrets, and enforces a simple Conventional Commit format

### `create-guideline`

Runs a short brainstorm around a guideline topic and then records the result.

- Reuses or updates an existing guideline when topics overlap
- Records the result through `record-guideline`

### `release`

Turns completed stories into a versioned release artifact.

- Moves stories from `work/backlog/done/` into a versioned release folder
- Creates `release.md` and updates `work/releases/releases.md`
- Requires the user to choose the final version when one is not provided

## Bootstrap path

Before the workflow can help in a repository, the scaffold needs to exist.

The bootstrap path is:

1. Run `init`.
2. Brainstorm and implement your bootstraping of the project
3. Run `refresh-project-config`.
4. Align `work/project-config.md` to repository reality.

For first-run onboarding, see `docs/getting-started.md`. For how command-driven work fits into the larger delivery lifecycle, see `docs/flows.md`.
