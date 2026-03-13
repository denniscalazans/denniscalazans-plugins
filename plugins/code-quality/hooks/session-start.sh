#!/usr/bin/env bash
# Checks SonarQube environment readiness at session start.
# Outputs a JSON system message summarizing the detected mode.
set -euo pipefail

warnings=()
info=()

# --- Standalone mode check (remote analysis) ---
if [[ -z "${SONARQUBE_URL:-}" ]]; then
  warnings+=("SONARQUBE_URL is not set.")
fi
if [[ -z "${SONARQUBE_TOKEN:-}" ]]; then
  warnings+=("SONARQUBE_TOKEN is not set.")
fi

# If both are set, check reachability (2s timeout, silent)
if [[ -n "${SONARQUBE_URL:-}" && -n "${SONARQUBE_TOKEN:-}" ]]; then
  if curl -sf --connect-timeout 2 -o /dev/null "${SONARQUBE_URL}/api/system/status" 2>/dev/null; then
    info+=("SonarQube connected (standalone mode).")
  else
    warnings+=("Cannot reach ${SONARQUBE_URL} — check VPN or server status.")
  fi
fi

# --- IDE-connected mode check (local analysis) ---
ide_port=""
if [[ -n "${SONARQUBE_IDE_PORT:-}" ]]; then
  # Explicit port configured — verify it
  if curl -sf --connect-timeout 1 -o /dev/null "http://localhost:${SONARQUBE_IDE_PORT}" 2>/dev/null; then
    info+=("SonarQube for IDE detected on port ${SONARQUBE_IDE_PORT} (IDE-connected mode).")
  else
    warnings+=("SONARQUBE_IDE_PORT=${SONARQUBE_IDE_PORT} is set but nothing is listening — is your IDE running?")
  fi
else
  # Auto-discover: first active port only (sonar-setup skill scans all ports)
  for port in $(seq 64120 64130); do
    if curl -sf --connect-timeout 0.3 -o /dev/null "http://localhost:${port}" 2>/dev/null; then
      ide_port="$port"
      break
    fi
  done
  if [[ -n "$ide_port" ]]; then
    info+=("SonarQube for IDE detected on port ${ide_port} (auto-discovered). Set SONARQUBE_IDE_PORT=${ide_port} to enable local analysis.")
  fi
fi

# --- Build system message ---
message=""

if [[ ${#warnings[@]} -gt 0 ]]; then
  message="code-quality plugin: "
  for w in "${warnings[@]}"; do
    message+="${w} "
  done
fi

if [[ ${#info[@]} -gt 0 ]]; then
  if [[ -z "$message" ]]; then
    message="code-quality plugin: "
  fi
  for i in "${info[@]}"; do
    message+="${i} "
  done
fi

# Fallback: always announce if plugin is loaded but nothing is configured
if [[ -z "$message" && ${#warnings[@]} -eq 0 && ${#info[@]} -eq 0 ]]; then
  message="code-quality plugin: SonarQube not configured. Run /code-quality:sonar-setup to get started."
fi

# Escape for JSON and output
if [[ -n "$message" ]]; then
  message=$(echo -n "$message" | sed 's/"/\\"/g' | tr '\n' ' ')
  echo "{\"systemMessage\": \"${message}\"}"
fi
