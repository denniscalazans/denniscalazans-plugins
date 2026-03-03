---
name: reset-to-main
description: Use when finishing a task and wanting to return to main branch with a clean working directory, switching context between tasks, or starting fresh after a PR
---

# Reset to Main

## Overview

Return to the main branch with a clean working directory and pruned stale branches.

**Announce at start:** "Resetting workspace to main."

## The Process

### Step 1: Check for uncommitted work

```bash
git status --short
```

**If working directory is dirty**, present options:

```
Uncommitted changes detected:

1. Stash changes (git stash push -m "auto-stash before reset")
2. Abort — I'll handle it manually

Which option?
```

**Do NOT discard changes without explicit confirmation.**

### Step 2: Switch to main

```bash
git checkout main
```

If `main` doesn't exist, try `master`.

### Step 3: Pull latest

```bash
git pull --prune
```

The `--prune` flag removes remote-tracking references for branches deleted on the remote.

### Step 4: Review and clean up stale branches

This step is interactive — the user chooses which branches to delete.

#### 4a. Detect candidates

Find branches whose remote tracking ref was pruned:

```bash
git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}'
```

If no `[gone]` branches exist, report "No stale branches to clean up." and skip to Step 5.

#### 4b. Enrich with merge status

Determine which default branch exists (`main` or `master`), then get the list of merged branches:

```bash
git branch --merged main
```

For each `[gone]` branch, mark it as **merged** (appears in the list) or **unmerged** (does not).

#### 4c. Check for associated worktrees

```bash
git worktree list
```

Match each `[gone]` branch to a worktree path, if any.

#### 4d. Present summary and let the user choose

Use `AskUserQuestion` with `multiSelect: false` to present the candidates and let the user decide.

Show a table first, then present options:

```
These local branches have been deleted on the remote:

| # | Branch | Status | Worktree | Recommendation |
|---|--------|--------|----------|----------------|
| 1 | feature/login | Merged to main | — | Safe to delete |
| 2 | fix/header-bug | Merged to main | ~/.claude/worktrees/header | Safe to delete (worktree will be removed) |
| 3 | experiment/new-api | NOT merged to main | — | Has unmerged commits — review before deleting |

Which branches should I delete?
```

Options:

- **Delete all safe (merged) branches** — deletes only branches marked "Merged to main"
- **Delete all branches** — deletes everything in the list
- **Let me pick** — user specifies branch numbers or names in the "Other" free-text input
- **Skip** — keep all branches, delete nothing

#### 4e. Delete selected branches

For each branch the user selected:

1. If the branch has an associated worktree (and it is not the main worktree), remove the worktree first:

```bash
git worktree remove --force "$worktree"
```

2. Delete the branch:

```bash
git branch -D "$branch"
```

#### 4f. Report results

Report what was deleted and what was kept.

Example: "Deleted 2 branches (feature/login, fix/header-bug). Kept 1 branch (experiment/new-api)."

### Step 5: Confirm

```bash
git branch -v
```

Report final state: current branch, number of branches cleaned, any remaining local branches.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Delete uncommitted changes silently | Always warn and offer stash |
| Skip `--prune` on pull | Always prune to detect `[gone]` branches |
| Force-delete branches without checking worktrees | Remove worktrees first |
| Delete all `[gone]` branches without asking | Present summary and let the user choose |
| Delete unmerged branches without warning | Mark unmerged branches clearly and recommend review |
| Assume `main` exists | Fall back to `master` |
