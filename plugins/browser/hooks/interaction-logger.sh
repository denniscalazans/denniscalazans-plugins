#!/bin/bash
set -uo pipefail

# Interaction Logger Hook
# Automatically logs agent-browser commands with rich element metadata.
# Runs as a PostToolUse hook on Bash — fires after every Bash command.
#
# Only processes commands containing "agent-browser".
# Appends JSONL entries to .agents.tmp/.browser-log/session.jsonl.
#
# Credential safety: fill values are always redacted.

# Read hook input from stdin
INPUT=$(cat)

# Extract the Bash command that was executed
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only process Bash calls containing agent-browser (not inside op run)
if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

if [[ "$COMMAND" != *"agent-browser"* ]]; then
  exit 0
fi

# Skip op run wrappers (login credentials — not part of replayable flows)
if [[ "$COMMAND" == *"op run"* ]]; then
  exit 0
fi

# Determine the agent-browser subcommand
AB_CMD=""
if [[ "$COMMAND" == *"agent-browser open"* ]]; then
  AB_CMD="open"
elif [[ "$COMMAND" == *"agent-browser snapshot"* ]]; then
  AB_CMD="snapshot"
elif [[ "$COMMAND" == *"agent-browser click"* ]]; then
  AB_CMD="click"
elif [[ "$COMMAND" == *"agent-browser fill"* ]]; then
  AB_CMD="fill"
elif [[ "$COMMAND" == *"agent-browser check"* ]]; then
  AB_CMD="check"
elif [[ "$COMMAND" == *"agent-browser select"* ]]; then
  AB_CMD="select"
elif [[ "$COMMAND" == *"agent-browser scroll"* ]]; then
  AB_CMD="scroll"
elif [[ "$COMMAND" == *"agent-browser close"* ]]; then
  AB_CMD="close"
else
  # Not an interaction we track
  exit 0
fi

# Ensure log directory exists
LOG_DIR=".agents.tmp/.browser-log"
LOG_FILE="${LOG_DIR}/session.jsonl"
mkdir -p "$LOG_DIR"

# If this is an "open" command and a log already exists, start a new session
if [[ "$AB_CMD" == "open" && -f "$LOG_FILE" ]]; then
  ARCHIVE="${LOG_DIR}/session-$(date +%Y%m%d-%H%M%S).jsonl"
  mv "$LOG_FILE" "$ARCHIVE"
fi

# Build the log entry
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_result // empty')

case "$AB_CMD" in
  open)
    URL=$(echo "$COMMAND" | grep -oE 'open\s+\S+' | awk '{print $2}')
    echo "{\"ts\":\"${TS}\",\"cmd\":\"open\",\"url\":\"${URL}\"}" >> "$LOG_FILE"
    ;;
  snapshot)
    ELEMENT_COUNT=$(echo "$TOOL_RESULT" | grep -c '\[ref=' 2>/dev/null || echo "0")
    CURRENT_URL=$(agent-browser get url 2>/dev/null || echo "unknown")
    echo "{\"ts\":\"${TS}\",\"cmd\":\"snapshot\",\"elements\":${ELEMENT_COUNT},\"url\":\"${CURRENT_URL}\"}" >> "$LOG_FILE"
    ;;
  click|fill|check|select)
    REF=$(echo "$COMMAND" | grep -oE '@e[0-9]+' | head -1)

    # Capture rich element metadata via agent-browser eval
    ELEMENT_JSON=$(agent-browser eval --stdin <<'EVALEOF' 2>/dev/null || echo "{}"
(() => {
  const snapshot = document.querySelectorAll('*');
  // Find the focused/last-interacted element
  const el = document.activeElement || document.body;
  if (!el || el === document.body) return JSON.stringify({});
  return JSON.stringify({
    tag: el.tagName,
    id: el.id || '',
    testId: el.getAttribute('data-test-id') || el.getAttribute('data-testid') || '',
    name: el.getAttribute('name') || '',
    formControl: el.getAttribute('formcontrolname') || '',
    role: el.getAttribute('role') || el.tagName.toLowerCase(),
    text: (el.textContent || '').trim().substring(0, 30),
    selector: el.id ? '#' + el.id
      : el.getAttribute('data-test-id') ? '[data-test-id="' + el.getAttribute('data-test-id') + '"]'
      : el.getAttribute('data-testid') ? '[data-testid="' + el.getAttribute('data-testid') + '"]'
      : el.getAttribute('name') ? el.tagName.toLowerCase() + '[name="' + el.getAttribute('name') + '"]'
      : el.getAttribute('formcontrolname') ? '[formcontrolname="' + el.getAttribute('formcontrolname') + '"]'
      : ''
  });
})()
EVALEOF
    )

    # Redact fill values
    VALUE=""
    if [[ "$AB_CMD" == "fill" ]]; then
      VALUE=",\"value\":\"<redacted>\""
    fi

    echo "{\"ts\":\"${TS}\",\"cmd\":\"${AB_CMD}\",\"ref\":\"${REF}\",\"element\":${ELEMENT_JSON}${VALUE}}" >> "$LOG_FILE"
    ;;
  scroll)
    echo "{\"ts\":\"${TS}\",\"cmd\":\"scroll\"}" >> "$LOG_FILE"
    ;;
  close)
    echo "{\"ts\":\"${TS}\",\"cmd\":\"close\"}" >> "$LOG_FILE"
    ;;
esac

exit 0
