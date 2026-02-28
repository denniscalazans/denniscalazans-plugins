---
name: reset
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

### Step 4: Clean up stale branches

Run the `clean_gone` logic — delete local branches whose remote is `[gone]`:

```bash
git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
  worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
  if [ -n "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
    echo "Removing worktree: $worktree"
    git worktree remove --force "$worktree"
  fi
  echo "Deleting branch: $branch"
  git branch -D "$branch"
done
```

If no `[gone]` branches exist, report "No stale branches to clean up."

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
| Assume `main` exists | Fall back to `master` |
