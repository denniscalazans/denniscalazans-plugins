#!/bin/bash
set -uo pipefail
# Note: -e omitted intentionally — we track per-role exit codes individually.

# Run Flow Across Multiple Roles
# Executes a .flow.ts file once per role, printing an informational summary.
#
# Usage:
#   <path>/run-flow-roles.sh <flow-file> <app> <role1> [role2] [role3] ...
#
# Examples:
#   run-flow-roles.sh .agents.tmp/scratch/playwright/create-record/create-record.flow.ts myapp manager partner
#
# Prerequisites:
#   - storageState exported for each role at .agents.tmp/.auth/<app>-<role>.json
#     (use: npx tsx plugins/dc/skills/browser-login/scripts/export-auth.ts <app> <role>)
#   - @playwright/test installed in the consuming project
#
# Results are INFORMATIONAL — a "failed" flow means broken selectors or timeouts,
# not incorrect business behavior. The developer interprets the results.

# Ensure nvm-managed node (and npx) is on PATH
if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then
  source "${NVM_DIR:-$HOME/.nvm}/nvm.sh" --no-use
  nvm use default > /dev/null 2>&1
fi

FLOW_FILE="${1:?Usage: run-flow-roles.sh <flow-file> <app> <role1> [role2] ...}"
APP="${2:?Usage: run-flow-roles.sh <flow-file> <app> <role1> [role2] ...}"
shift 2
ROLES=("$@")

if [[ ${#ROLES[@]} -eq 0 ]]; then
  echo "Error: At least one role is required."
  echo "Usage: run-flow-roles.sh <flow-file> <app> <role1> [role2] ..."
  exit 1
fi

# --- Input validation (path traversal prevention) ---

if [[ ! -f "$FLOW_FILE" ]]; then
  echo "Error: Flow file not found: ${FLOW_FILE}"
  exit 1
fi

if [[ ! "$APP" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Invalid app name: ${APP}"
  echo "Only alphanumeric, hyphens, and underscores are allowed."
  exit 1
fi

for ROLE in "${ROLES[@]}"; do
  if [[ ! "$ROLE" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: Invalid role name: ${ROLE}"
    echo "Only alphanumeric, hyphens, and underscores are allowed."
    exit 1
  fi
done

# --- Auth check ---
# In the unified browser plugin, auth is live in agent-browser's Chrome session.
# No storageState files to validate — the flow connects via connectOverCDP.
echo "Note: Flows connect to agent-browser's Chrome. Ensure sessions are authenticated."
echo "  Use: /browser:login as <role> on <app>"

echo "Running flow: ${FLOW_FILE}"
echo "App: ${APP} | Roles: ${ROLES[*]}"
echo ""

# --- Run flow per role (sequential — Playwright tests compete for browser) ---
# Indexed arrays for bash 3.2 compatibility (no associative arrays).
EXIT_CODES=()
DURATIONS=()

for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  echo "[${ROLE}] Running..."

  START=$(date +%s)
  FLOW_ROLE="$ROLE" FLOW_APP="$APP" npx playwright test "$FLOW_FILE" 2>&1
  EXIT_CODES+=($?)
  END=$(date +%s)
  DURATIONS+=($((END - START)))
done

# --- Print summary table ---

echo ""
echo "--- Results ------------------------------------"
for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  CODE="${EXIT_CODES[$i]}"
  DURATION="${DURATIONS[$i]}"
  if [[ "$CODE" -eq 0 ]]; then
    STATUS="PASS"
  else
    STATUS="FAIL"
  fi
  printf "  [%-12s]  %-4s  %ds\n" "$ROLE" "$STATUS" "$DURATION"
done
echo "------------------------------------------------"
echo ""
echo "Results are informational — interpret whether observed behavior matches expectations."

# Exit 0 always — results are informational, not assertions.
exit 0
