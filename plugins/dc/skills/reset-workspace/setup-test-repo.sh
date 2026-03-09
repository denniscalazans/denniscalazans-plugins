#!/bin/bash
# Creates a test repo at /tmp/reset-skill-test with realistic branch states.
# Usage: bash setup-test-repo.sh [scenario]
# Scenarios:
#   clean       - clean working directory, on a squash-merged branch, stale branches exist
#   dirty-integrated - dirty working directory, current branch is integrated into main
#   dirty-wip   - dirty working directory, current branch has unmerged work

set -e
SCENARIO="${1:-clean}"
REPO="/tmp/reset-skill-test-${SCENARIO}"
REMOTE="/tmp/reset-skill-test-${SCENARIO}-remote"

rm -rf "$REPO" "$REMOTE"
mkdir -p "$REPO" && cd "$REPO" && git init

# Initial commit on main
echo "# Project" > README.md && git add README.md && git commit -m "initial commit"

# Create a remote (bare) to simulate upstream
git clone --bare "$REPO" "$REMOTE"
git remote add origin "$REMOTE"

# --- Create branches that will become [gone] ---

# 1. A branch that was squash-merged into main
git checkout -b feature/auth
echo "auth code" > auth.ts && git add auth.ts && git commit -m "add auth"
git push -u origin feature/auth
git checkout main
git merge --squash feature/auth && git commit -m "feat: add auth (#1)"
git push origin main
# Delete remote branch (simulates PR merge + branch delete)
git push origin --delete feature/auth

# 2. A branch that was regular-merged into main
git checkout -b fix/typo
echo "fixed" > typo.txt && git add typo.txt && git commit -m "fix typo"
git push -u origin fix/typo
git checkout main
git merge fix/typo -m "Merge pull request #2 from fix/typo"
git push origin main
git push origin --delete fix/typo

# 3. A branch that was NOT merged (abandoned)
git checkout -b experiment/new-api
echo "experimental" > experiment.ts && git add experiment.ts && git commit -m "wip experiment"
git push -u origin experiment/new-api
git checkout main
git push origin --delete experiment/new-api

# Prune to mark remote refs as gone
git fetch --prune

# --- Set up the scenario ---

case "$SCENARIO" in
  clean)
    # Stay on the squash-merged branch, clean worktree
    git checkout feature/auth
    ;;
  dirty-integrated)
    # On the squash-merged branch with dirty files
    git checkout feature/auth
    echo "staged change" > staged.txt && git add staged.txt
    echo "unstaged change" >> auth.ts
    echo "scratch notes" > notes.txt
    ;;
  dirty-wip)
    # On a new branch with unmerged work + dirty files
    git checkout -b feature/new-dashboard
    echo "dashboard wip" > dashboard.ts && git add dashboard.ts && git commit -m "wip dashboard"
    echo "more wip" >> dashboard.ts
    echo "todo" > TODO.txt
    ;;
esac

echo "Test repo ready at $REPO (scenario: $SCENARIO)"
echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"
git status --short
