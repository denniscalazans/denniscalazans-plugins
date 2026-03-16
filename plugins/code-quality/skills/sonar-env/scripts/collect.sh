#!/usr/bin/env bash
# Collects SonarQube infrastructure data from the local machine.
# Outputs structured sections that the skill interprets and presents.
# Read-only — no containers are stopped, no config is changed.
set -euo pipefail

echo "=== EMBEDDED_SERVERS ==="
# Find SonarQube for IDE instances listening on port range 64120-64130.
# Each line: PID COMMAND PORT
if command -v lsof &>/dev/null; then
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    pid=$(echo "$line" | awk '{print $2}')
    # NAME field is e.g. "127.0.0.1:64120" — extract port after the colon.
    port=$(echo "$line" | awk '{print $(NF-1)}' | sed 's/.*://')
    cmd=$(ps -p "$pid" -o command= 2>/dev/null | head -c 300 || echo "unknown")
    echo "PID=${pid} PORT=${port} CMD=${cmd}"
  done < <(lsof -iTCP:64120-64130 -sTCP:LISTEN -P -n 2>/dev/null | grep -v "^COMMAND" || true)
else
  echo "SKIP: lsof not available"
fi

echo ""
echo "=== MCP_CONTAINERS ==="
# Find running mcp/sonarqube Docker containers and their env vars.
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
  container_ids=$(docker ps --filter "ancestor=mcp/sonarqube" --format "{{.ID}}" 2>/dev/null || true)
  if [[ -z "$container_ids" ]]; then
    # Try broader filter in case image name differs (e.g., docker.io/mcp/sonarqube)
    container_ids=$(docker ps --format "{{.ID}} {{.Image}}" 2>/dev/null | grep -i "mcp/sonarqube" | awk '{print $1}' || true)
  fi
  if [[ -n "$container_ids" ]]; then
    while IFS= read -r cid; do
      [[ -z "$cid" ]] && continue
      name=$(docker inspect --format '{{.Name}}' "$cid" 2>/dev/null | sed 's/^\///')
      status=$(docker inspect --format '{{.State.Status}}' "$cid" 2>/dev/null)
      created=$(docker inspect --format '{{.Created}}' "$cid" 2>/dev/null | cut -c1-19)
      ide_port=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$cid" 2>/dev/null | grep "^SONARQUBE_IDE_PORT=" | cut -d= -f2 || echo "not set")
      sq_url=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$cid" 2>/dev/null | grep "^SONARQUBE_URL=" | cut -d= -f2- || echo "not set")
      echo "ID=${cid} NAME=${name} STATUS=${status} CREATED=${created} IDE_PORT=${ide_port} URL=${sq_url}"
    done <<< "$container_ids"
  else
    echo "NONE: No mcp/sonarqube containers running"
  fi
else
  echo "SKIP: Docker not available or not running"
fi
