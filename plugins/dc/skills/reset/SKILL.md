---
name: reset-to-main
description: >
  Use when finishing a task and wanting to return to main branch with a clean working directory, switching context between tasks, or starting fresh after a PR.
  Triggers: "reset", "switch to main", "start fresh", "back to main", "done with this task", "clean up workspace", "done with branch", "close this task".
---

# Reset to Main

Return to the default branch with a clean working directory and pruned integrated branches.

**Announce at start:** "Resetting workspace to main."

## The Process

### Step 1: Gather context

Collect the full picture before showing anything to the user:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git stash list
```

Determine the default branch (`main`, or `master` if `main` doesn't exist).
Store it as `$default_branch` for all later steps.

Also check if the current branch is already integrated into the default branch:

```bash
merge_base=$(git merge-base "$default_branch" HEAD)
merge_result=$(git merge-tree "$merge_base" "$default_branch" HEAD)
```

If `merge_result` is empty, the current branch's content is already in the default branch.
Store this as `$branch_integrated=true`.

This covers all GitHub merge strategies:
- **Merge commit** — detected by ancestry
- **Squash and merge** — detected by `merge-tree` (different SHAs, same content)
- **Rebase and merge** — detected by both (cherry-picked commits preserve content)

### Step 2: Present working directory state

Show a categorized summary so the user can see exactly what's in their working directory.
Parse `git status --short` output: first column = staged, second column = unstaged, `??` = untracked.

```
Current branch: feature/login (integrated into main ✓)

Staged (ready to commit):
  M  src/auth.ts
  A  src/new-file.ts

Unstaged (modified but not staged):
  M  src/utils.ts

Untracked (not in git, not ignored):
     notes.txt
     scratch/debug.log

Stash: 2 entries
```

Omit empty categories — only show sections that have files.
Show the integration status next to the branch name — this tells the user whether their work is safe.

#### If clean working directory

Say "Working directory is clean." and skip to Step 3.

#### If dirty but branch is integrated

The branch's committed work is already in the default branch, so only the uncommitted changes need handling.
Present a simplified flow:

```
Your branch content is already in main. Only uncommitted changes remain:

1. Stash changes — save for later with `git stash pop`
2. Discard changes — these aren't committed anywhere, this cannot be undone
3. Abort — I'll handle it myself
```

Omit the worktree option here — there's no in-progress branch work to preserve.

#### If dirty and branch is NOT integrated

The user has uncommitted changes AND branch commits not yet in the default branch.
Present the full set of options:

```
What should I do with these changes?

1. Stash everything — saves all changes, you can restore later with `git stash pop`
2. Move to a worktree — keeps your branch and changes in a separate directory (best for "I'll come back to this")
3. Discard all changes — throws away everything (staged, unstaged, untracked). Cannot be undone.
4. Abort — I'll handle it myself
```

Use `AskUserQuestion` to let the user choose.

#### Execute the chosen option

**Option: Stash everything**

```bash
git stash push --include-untracked -m "auto-stash: <branch-name> (<date>)"
```

The `--include-untracked` flag captures untracked files too, so nothing is left behind.
Confirm: "Stashed all changes. Restore later with `git stash pop`."

**Option: Move to a worktree** (only offered when branch is not integrated)

Create a worktree for the current branch so the user can return to it later:

```bash
git stash push --include-untracked -m "worktree-stash: <branch-name> (<date>)"
worktree_path="$HOME/.claude/worktrees/<branch-name>"
git worktree add "$worktree_path" "<branch-name>"
cd "$worktree_path" && git stash pop
```

The stash-then-pop dance is necessary because `git worktree add` requires a clean working directory.
Confirm: "Moved branch `<branch-name>` and its changes to `<worktree_path>`. Resume work there anytime."

**Option: Discard all changes**

This is destructive and cannot be undone.
Before executing, ask for explicit confirmation:

```
This will permanently delete:
- <N> staged changes
- <N> unstaged changes
- <N> untracked files

Type "yes" to confirm.
```

Only proceed if the user types "yes". Then:

```bash
git reset HEAD .
git checkout -- .
git clean -fd
```

**Option: Abort**

Stop the skill. Say "Aborted. Working directory unchanged."

### Step 3: Switch to the default branch and pull

```bash
git checkout "$default_branch"
git pull --prune
```

The `--prune` flag removes remote-tracking references for branches deleted on the remote.

### Step 4: Clean up integrated branches

Follow the `/dc:clean-branches` skill process (Steps 2–7).
The `git fetch --prune` in that skill's Step 1 was already done by `git pull --prune` in Step 3 above, so skip it.

### Step 5: Confirm final state

```bash
git branch -v
git stash list
```

Report:
- Current branch
- Number of branches cleaned
- Any remaining local branches
- Stash count reminder if any exist, e.g. "You have 3 stashes. Use `git stash list` to inspect."

The stash reminder matters because stashes are easy to forget after context-switching.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Delete uncommitted changes silently | Show categorized working directory state and let the user choose |
| Offer worktree when branch is already integrated | Only offer worktree when branch has unmerged work worth preserving |
| Skip `--prune` on pull | Always prune to get accurate remote tracking status |
| Assume `main` exists | Fall back to `master`, store as `$default_branch` |
| Forget about stashes after reset | Always check `git stash list` and remind the user |
| Stash without `--include-untracked` | Include untracked files so nothing is left behind |
