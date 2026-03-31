#!/bin/bash
set -uo pipefail

# Parallel Browser Login via agent-browser
# Opens multiple role sessions for the same app simultaneously.
#
# Usage:
#   <path>/parallel-login.sh <app> <url> <role1> [role2] [role3] ...
#
# Examples:
#   parallel-login.sh ffa http://localhost:4488 manager partner auditor
#
# Prerequisites:
#   - Each role needs a profile at .agents.local/login/<app>-<role>.env
#   - 1Password CLI (op) installed and configured
#   - agent-browser installed (npm i -g agent-browser)
#
# Note: 1Password serializes biometric prompts — one biometric prompt per role,
#       appearing sequentially even though logins run in parallel.

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
PIDS=()

for i in "${!ROLES[@]}"; do
  ROLE="${ROLES[$i]}"
  SESSION="${APP}-${ROLE}"
  PROFILE="${PROFILES_DIR}/${APP}-${ROLE}.env"
  LOG_FILE="${LOG_DIR}/${ROLE}.log"

  echo "[${ROLE}] Starting login (session: ${SESSION})..."

  (
    # Open browser session
    agent-browser --session "$SESSION" open "$URL" > /dev/null 2>&1
    sleep 3

    # Snapshot and find login form
    SNAPSHOT=$(agent-browser --session "$SESSION" snapshot -i 2>/dev/null)
    EMAIL_REF=$(echo "$SNAPSHOT" | grep -iE 'textbox.*(email|username|user).*ref=' | head -1 | grep -oE '@e[0-9]+' | head -1)
    PASS_REF=$(echo "$SNAPSHOT" | grep -iE 'textbox.*(password).*ref=' | head -1 | grep -oE '@e[0-9]+' | head -1)
    SUBMIT_REF=$(echo "$SNAPSHOT" | grep -iE 'button.*(continue|submit|log|sign).*ref=' | head -1 | grep -oE '@e[0-9]+' | head -1)

    if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
      # Check if already authenticated
      CURRENT_URL=$(agent-browser --session "$SESSION" get url 2>/dev/null)
      if echo "$CURRENT_URL" | grep -qvE '(login|authorize|oauth|signin|sso)'; then
        echo "Already authenticated as ${ROLE} on ${APP}."
        exit 0
      fi
      echo "Error: Could not find login form for ${ROLE}."
      exit 1
    fi

    # Fill credentials via op run
    op run --env-file="$PROFILE" -- sh -c "
      agent-browser --session '$SESSION' fill '$EMAIL_REF' \"\$AUTH0_USER\" > /dev/null 2>&1 && \
      agent-browser --session '$SESSION' fill '$PASS_REF' \"\$AUTH0_PASS\" > /dev/null 2>&1 && \
      agent-browser --session '$SESSION' click '${SUBMIT_REF:-}' > /dev/null 2>&1
    "

    sleep 4
    echo "Logged in as ${ROLE} on ${APP}."
    echo "Session: ${SESSION}"
  ) > "$LOG_FILE" 2>&1 &
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
    LAST_LINE=$(tail -1 "${LOG_DIR}/${ROLE}.log")
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
