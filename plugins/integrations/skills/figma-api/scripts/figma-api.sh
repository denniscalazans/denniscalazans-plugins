#!/usr/bin/env bash
# Figma REST API wrapper — resolves the API token via 1Password CLI (op run).
# The token never appears in command arguments or shell history.
#
# Usage:
#   ./figma-api.sh GET /v1/me
#   ./figma-api.sh GET "/v1/files/ABC123?depth=1"
#   ./figma-api.sh POST /v1/files/ABC123/comments '{"message":"Hello"}'
#
# Environment:
#   FIGMA_API_KEY is resolved at runtime by op run from op://Development/Figma/credential
#   You can override the 1Password reference by setting FIGMA_OP_REF before calling.

set -euo pipefail

FIGMA_OP_REF="${FIGMA_OP_REF:-op://Development/Figma/credential}"
BASE_URL="https://api.figma.com"

METHOD="${1:?Usage: figma-api.sh METHOD PATH [BODY]}"
API_PATH="${2:?Usage: figma-api.sh METHOD PATH [BODY]}"
BODY="${3:-}"

# Build the full URL (handle paths that already include query params)
FULL_URL="${BASE_URL}${API_PATH}"

# Build the curl command string with proper quoting for bash -c.
# Array expansion inside bash -c loses quoting, so we build the string directly.
CURL_CMD="curl -s -w '"'\n%{http_code}'"' -H 'X-Figma-Token: '\"'\$FIGMA_API_KEY'\""

if [[ "$METHOD" != "GET" ]]; then
  CURL_CMD="$CURL_CMD -X $METHOD"
  if [[ -n "$BODY" ]]; then
    ESCAPED_BODY=$(printf '%s' "$BODY" | sed "s/'/'\\\\''/g")
    CURL_CMD="$CURL_CMD -H 'Content-Type: application/json' -d '$ESCAPED_BODY'"
  fi
fi

CURL_CMD="$CURL_CMD '$FULL_URL'"

# Execute via op run — token is injected as env var, never exposed to stdout
RESPONSE=$(op run --env "FIGMA_API_KEY=$FIGMA_OP_REF" -- \
  bash -c "$CURL_CMD")

# Extract HTTP status code (last line) and body (everything else)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY_RESPONSE=$(echo "$RESPONSE" | sed '$d')

# Handle rate limiting
if [[ "$HTTP_CODE" == "429" ]]; then
  echo '{"error": "rate_limited", "status": 429, "message": "Rate limited by Figma API. Wait and retry."}' >&2
  exit 1
fi

# Handle auth errors
if [[ "$HTTP_CODE" == "403" || "$HTTP_CODE" == "401" ]]; then
  echo "{\"error\": \"auth_failed\", \"status\": $HTTP_CODE, \"message\": \"Authentication failed. Check your Figma API token in 1Password.\"}" >&2
  exit 1
fi

# Output the response body
echo "$BODY_RESPONSE"
