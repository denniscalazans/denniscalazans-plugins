#!/bin/bash
set -uo pipefail
# Note: -e omitted intentionally — we track per-role exit codes individually.

# Parallel Browser Login
# Opens multiple role sessions for the same app simultaneously.
#
# Usage:
#   <path>/parallel-login.sh <app> <url> <role1> [role2] [role3] ...
#
# Examples:
#   parallel-login.sh my-app http://localhost:4200 admin editor
#   parallel-login.sh my-app http://localhost:4200 admin editor viewer
#
# Prerequisites:
#   - Each role needs a profile at .agents.local/login/<app>-<role>.env (cwd-relative)
#   - 1Password CLI (op) installed and configured
#   - playwright-cli installed globally (@playwright/cli)
#
# Note: 1Password serializes biometric prompts — you'll get one biometric
#       prompt per role, appearing sequentially even though logins run in parallel.

APP="${1:?Usage: parallel-login.sh <app> <url> <role1> [role2] ...}"
URL="${2:?Usage: parallel-login.sh <app> <url> <role1> [role2] ...}"
shift 2
ROLES=("$@")

if [[ ${#ROLES[@]} -eq 0 ]]; then
  echo "Error: At least one role is required."
  echo "Usage: parallel-login.sh <app> <url> <role1> [role2] ..."
  exit 1
fi

PROFILES_DIR=".agents.local/login"
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGIN_SCRIPT="${SCRIPTS_DIR}/login.sh"
LOG_DIR=".agents.tmp/.parallel-login/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$LOG_DIR"

# --- Validate all profiles exist (fail fast) ---
MISSING=0
for ROLE in "${ROLES[@]}"; do
  PROFILE="${PROFILES_DIR}/${APP}-${ROLE}.env"
  if [[ ! -f "$PROFILE" ]]; then
    echo "Error: Profile not found: ${PROFILE}"
    MISSING=1
  fi
done

if [[ "$MISSING" -eq 1 ]]; then
  echo ""
  echo "Available profiles:"
  ls "$PROFILES_DIR"/*.env 2>/dev/null | xargs -I{} basename {} .env | sed 's/^/  /'
  exit 1
fi

echo "Logging in to ${APP} (${URL}) as: ${ROLES[*]}"
echo "1Password will prompt for biometric auth once per role (sequential prompts)."
echo ""

# --- Launch logins in parallel ---
# Indexed arrays for bash 3.2 compatibility (no associative arrays).
# PIDS[i] and ROLES[i] are correlated by index.
PIDS=()

for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  PROFILE="${PROFILES_DIR}/${APP}-${ROLE}.env"
  LOG_FILE="${LOG_DIR}/${ROLE}.log"

  echo "[${ROLE}] Starting login..."
  op run --env-file="$PROFILE" -- "$LOGIN_SCRIPT" "$APP" "$ROLE" "$URL" > "$LOG_FILE" 2>&1 &
  PIDS+=($!)
done

# --- Wait for all and collect exit codes ---
EXIT_CODES=()
for i in "${!PIDS[@]}"; do
  wait "${PIDS[$i]}" 2>/dev/null
  EXIT_CODES+=($?)
done

# --- Print summary ---
echo ""
echo "--- Summary ------------------------------------"
HAS_FAILURE=0
for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  CODE="${EXIT_CODES[$i]}"
  if [[ "$CODE" -eq 0 ]]; then
    LAST_LINE=$(tail -2 "${LOG_DIR}/${ROLE}.log" | head -1)
    echo "  [${ROLE}] OK — ${LAST_LINE}"
  else
    echo "  [${ROLE}] FAILED (exit ${CODE}) — see ${LOG_DIR}/${ROLE}.log"
    HAS_FAILURE=1
  fi
done
echo "------------------------------------------------"

# --- Cleanup ---
if [[ "$HAS_FAILURE" -eq 0 ]]; then
  rm -r "$LOG_DIR"
  echo "All roles authenticated successfully."
  exit 0
else
  echo ""
  echo "Some logins failed. Logs preserved at: ${LOG_DIR}/"
  exit 1
fi
