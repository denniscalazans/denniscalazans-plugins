#!/bin/bash
set -euo pipefail

# Browser Login Script
# Securely logs into a web app using playwright-cli.
# Credentials are injected via op run (1Password CLI) — never visible in output.
#
# Usage:
#   op run --env-file=".agents.local/login/<app>-<role>.env" -- <path>/login.sh <app> <role> <url>
#
# Examples:
#   op run --env-file=".agents.local/login/my-app-admin.env" -- scripts/login.sh my-app admin http://localhost:4200

# Ensure nvm-managed node (and playwright-cli) is on PATH
if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then
  source "${NVM_DIR:-$HOME/.nvm}/nvm.sh" --no-use
  nvm use default > /dev/null 2>&1
fi

APP="${1:?Usage: login.sh <app> <role> <url>}"
ROLE="${2:?Usage: login.sh <app> <role> <url>}"
URL="${3:?Usage: login.sh <app> <role> <url>}"
SESSION="${APP}-${ROLE}"
SNAPSHOT="/tmp/login-snapshot-${SESSION}.yaml"

# Validate required env vars (set by op run)
if [[ -z "${LOGIN_USER:-}" || -z "${LOGIN_PASS:-}" ]]; then
  echo "Error: LOGIN_USER and LOGIN_PASS must be set."
  echo "Run with: op run --env-file=\".agents.local/login/${SESSION}.env\" -- $0 $*"
  exit 1
fi

echo "Opening ${APP} as ${ROLE} (${URL})..."

# Open browser with named persistent session
playwright-cli -s="$SESSION" open --headed --persistent "$URL" > /dev/null 2>&1
sleep 3

# --- Detect login form (with auto-discovery fallback) ---

find_login_form() {
  playwright-cli -s="$SESSION" snapshot --filename="$SNAPSHOT" 2>/dev/null
  # Snapshot format: - textbox "Email address" [ref=e42]:
  EMAIL_REF=$(grep -iE '(input|textbox).*(email|username|user).*\[ref=e[0-9]+\]' "$SNAPSHOT" 2>/dev/null | head -1 | grep -oE 'e[0-9]+' | head -1 || true)
  PASS_REF=$(grep -iE '(input|textbox).*(password).*\[ref=e[0-9]+\]' "$SNAPSHOT" 2>/dev/null | head -1 | grep -oE 'e[0-9]+' | head -1 || true)
}

find_login_form

# --- Check if already authenticated ---
if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
  # playwright-cli eval wraps output in markdown — extract the quoted URL from the "### Result" section
  EVAL_OUTPUT=$(playwright-cli -s="$SESSION" eval "() => window.location.href" 2>/dev/null || true)
  CURRENT_URL=$(echo "$EVAL_OUTPUT" | grep -oE 'https?://[^"]+' | head -1 || true)
  APP_HOST=$(echo "$URL" | sed -E 's|https?://([^/:]+).*|\1|')

  if [[ -n "$CURRENT_URL" ]]; then
    CURRENT_HOST=$(echo "$CURRENT_URL" | sed -E 's|https?://([^/:]+).*|\1|')
    CURRENT_PATH=$(echo "$CURRENT_URL" | sed -E 's|https?://[^/]+(/.*)|\1|' | sed 's|[?#].*||')

    IS_AUTH_URL=false
    if echo "$CURRENT_URL" | grep -qiE '(login|authorize|oauth|signin|sso|saml)'; then
      IS_AUTH_URL=true
    fi

    IS_LANDING=false
    if [[ "$CURRENT_PATH" == "/" || "$CURRENT_PATH" == "/welcome" || "$CURRENT_PATH" == "/home" ]]; then
      IS_LANDING=true
    fi

    if [[ "$CURRENT_HOST" == "$APP_HOST" && "$IS_AUTH_URL" == "false" && "$IS_LANDING" == "false" ]]; then
      rm -f "$SNAPSHOT"
      echo "Already authenticated as ${ROLE} on ${APP}."
      echo "Session: ${SESSION}"
      exit 0
    fi
  fi
fi

if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
  echo "No login form detected on the current page."

  # Try to find a login/sign-in link or button on the page
  LOGIN_LINK=$(grep -iE '(button|a|link).*"[^"]*(log\s*in|sign\s*in|login|signin|authenticate|enter|access)[^"]*".*\[ref=e[0-9]+\]' "$SNAPSHOT" 2>/dev/null | head -1 | grep -oE 'e[0-9]+' | head -1 || true)

  if [[ -n "$LOGIN_LINK" ]]; then
    echo "Found a login link/button — clicking it..."
    playwright-cli -s="$SESSION" click "$LOGIN_LINK" > /dev/null 2>&1
    sleep 3
    find_login_form
  fi

  # If still no form, ask the user
  if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
    echo ""
    echo "Could not find the login form automatically."
    echo ""
    echo "Options:"
    echo "  [w] Wait — navigate to the login page manually in the browser, then press Enter"
    echo "  [r] Retry — re-scan the current page for a login form"
    echo "  [a] Abort — exit without logging in"
    echo ""

    while true; do
      read -rp "Choose [w/r/a]: " choice
      case "${choice,,}" in
        w)
          echo "Waiting... navigate to the login page in the browser, then press Enter."
          read -r
          find_login_form
          if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
            echo "Still no login form found."
            continue
          fi
          break
          ;;
        r)
          find_login_form
          if [[ -z "$EMAIL_REF" || -z "$PASS_REF" ]]; then
            echo "Still no login form found."
            continue
          fi
          break
          ;;
        a)
          rm -f "$SNAPSHOT"
          echo "Aborted. Session '${SESSION}' is open but not authenticated."
          echo "  playwright-cli -s=${SESSION} snapshot"
          exit 0
          ;;
        *)
          echo "Invalid choice. Enter w, r, or a."
          ;;
      esac
    done
  fi
fi

# Find submit button
SUBMIT_REF=$(grep -iE '(button|a).*"[^"]*(submit|continue|log|sign)[^"]*".*\[ref=e[0-9]+\]' "$SNAPSHOT" 2>/dev/null | head -1 | grep -oE 'e[0-9]+' | head -1 || true)

# Fill credentials — ALL OUTPUT SUPPRESSED to prevent leaking values
playwright-cli -s="$SESSION" fill "$EMAIL_REF" "$LOGIN_USER" > /dev/null 2>&1
playwright-cli -s="$SESSION" fill "$PASS_REF" "$LOGIN_PASS" > /dev/null 2>&1

if [[ -n "$SUBMIT_REF" ]]; then
  playwright-cli -s="$SESSION" click "$SUBMIT_REF" > /dev/null 2>&1
else
  # Fallback: press Enter if no button found
  playwright-cli -s="$SESSION" press Enter > /dev/null 2>&1
fi

# Cleanup snapshot (may contain form field hints)
rm -f "$SNAPSHOT"

# Wait for redirect after login
sleep 4

echo "Logged in as ${ROLE} on ${APP}."
echo "Session: ${SESSION}"
echo ""
echo "To reuse this session later:"
echo "  playwright-cli -s=${SESSION} open --headed --persistent ${URL}"
