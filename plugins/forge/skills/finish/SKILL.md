---
name: finish
description: >
  Use when finishing a task and cleaning up local branches whose content is already in the default branch.
  Also use when the user wants to clean up after merging PRs or remove branches that were squash-merged or rebased.
  Triggers: "finish task", "forge finish", "clean up branches", "prune branches",
  "clean branches", "delete integrated branches", "remove merged branches", "done with task".
---

# Clean Integrated Branches

Scan all local branches and identify those whose content is already in the default branch.
Only branches with zero unique content are offered for deletion — the work is already in main, so deleting the branch loses nothing.
Branches with any unique commits are reported but never offered for deletion.

**Announce at start:** "Scanning local branches for integrated content."

## Why content-based detection?

Tracking metadata (upstream refs, remote status) is fragile — users change upstreams, branches may never have been pushed, or the remote may still exist after a squash merge.
The only reliable question is: "does this branch contain anything the default branch doesn't?"

`git merge-tree` answers this by performing a three-way merge in memory.
If the result is empty, every change on the branch is already in the default branch — regardless of how it got there (merge commit, squash and merge, rebase and merge, cherry-pick, or manual re-implementation).

## The Process

### Step 1: Setup

```bash
git fetch --prune
```

Prune removes remote-tracking references for branches deleted on the remote.
This ensures the tracking status context is accurate for labeling later.

Determine the default branch (`main`, or `master` if `main` doesn't exist).
Store it as `$default_branch`.

Also note the current branch — it is excluded from scanning.

### Step 2: Collect all candidate branches

List every local branch except the default branch and the current branch:

```bash
git for-each-ref --format='%(refname:short)' refs/heads/ | grep -v "^$default_branch$"
```

Also exclude protected branch patterns: `master`, `main`, `develop`, `release/*`.

If no candidates exist, report "No branches to check." and stop.

### Step 3: Check integration with `merge-tree`

For each candidate branch:

```bash
merge_base=$(git merge-base "$default_branch" "$branch")
merge_result=$(git merge-tree "$merge_base" "$default_branch" "$branch")
```

If `merge_result` is empty → the branch is **integrated**.
Every change it introduced is already in the default branch.

If `merge_result` is non-empty → the branch has **unique work**.
It contains commits or changes not yet in the default branch.

### Step 4: Enrich with context

For each branch, gather context to help the user understand what they're looking at.
This is informational only — it does not affect the safety classification from Step 3.

**Tracking status** — what the upstream ref says:

```bash
git for-each-ref --format='%(refname:short) %(upstream:short) %(upstream:track)' refs/heads/"$branch"
```

Classify as:
- **"Remote deleted"** — upstream is set but the remote branch no longer exists. Strongest signal the PR was merged and cleaned up.
- **"Remote exists"** — upstream points to a live remote branch. Content is in main but the remote wasn't cleaned up.
- **"Local only"** — no upstream set. Branch was never pushed, or upstream was unset.
- **"Tracks main"** — upstream points to `origin/main` or `origin/master`. User workflow artifact.

**Last commit date:**

```bash
git log -1 --format='%cr' "$branch"
```

**Worktree association:**

```bash
git worktree list
```

Match each branch to a worktree path, if any.

### Step 5: Present results

Split into two clear sections.
Use `AskUserQuestion` for the deletion choice.

```
Integrated (content is already in main):
| # | Branch           | Context                | Last commit  | Worktree |
|---|------------------|------------------------|--------------|----------|
| 1 | feature/auth     | Remote deleted         | 3 days ago   | —        |
| 2 | feature/payments | Remote exists          | 1 week ago   | —        |
| 3 | fix/typo         | Local only             | 2 days ago   | —        |
| 4 | fix/header       | Remote deleted         | 5 days ago   | ~/.claude/worktrees/header (will be removed) |

Not integrated (has unique work — keeping):
| Branch                | Context        | Last commit  |
|-----------------------|----------------|--------------|
| feature/new-dashboard | Remote exists  | 2 hours ago  |
| experiment/dead-idea  | Local only     | 3 weeks ago  |

Delete the integrated branches?
```

Options:

- **Yes, delete all** — deletes every integrated branch
- **Let me pick** — user specifies branch numbers
- **Skip** — keep everything

### Step 6: Delete selected branches

For each branch the user selected:

1. If the branch has an associated worktree (and it is not the main worktree), remove the worktree first:

```bash
git worktree remove --force "$worktree"
```

2. Delete the branch.
Use `-d` first (safe flag). If it fails (squash-merged branches fail `-d` because git's ancestry check can't detect them), fall back to `-D`:

```bash
git branch -d "$branch" 2>/dev/null || git branch -D "$branch"
```

This is safe because Step 3 already verified via `merge-tree` that the content is in the default branch.
The `-d` attempt first is a defense-in-depth check — if git's own ancestry agrees, great. If not, we trust our `merge-tree` verification.

### Step 7: Report results

Show a receipt of what happened:

```bash
git branch -v
```

Example:

```
Deleted 3 branches: feature/auth, feature/payments, fix/typo
Kept 2 branches with unique work: feature/new-dashboard, experiment/dead-idea
Remaining branches:
* main                  a1b2c3d latest commit
  feature/new-dashboard e4f5g6h wip dashboard
  experiment/dead-idea  h7i8j9k experiment
```

## Common Mistakes

| Don't | Do |
|-------|-----|
| Gate on tracking metadata | Scan all branches — upstream status is fragile, content is the truth |
| Rely only on `git branch --merged` | Use `merge-tree` — it catches squash, rebase, and cherry-pick merges |
| Delete the current branch | Always exclude the current branch from candidates |
| Delete protected branches | Exclude `main`, `master`, `develop`, `release/*` |
| Delete branches with unique work | Only offer deletion for branches where `merge-tree` returns empty |
| Auto-delete without confirmation | Always present the list and let the user choose |
| Forget worktrees | Remove associated worktrees before deleting the branch |
| Use `-D` blindly | Try `-d` first, fall back to `-D` only after `merge-tree` verification |
