---
name: sonar-setup
description: >
  Use when setting up SonarQube MCP integration, diagnosing connectivity issues, or checking which code-quality skills are functional.
  Also use when the user asks "is SonarQube working?", "set up sonar", or wants to enable IDE-connected mode.
  Triggers: "sonar setup", "configure sonarqube", "sonar not working", "mcp connection", "ide mode", "analyze_file_list", "sonar connectivity".
---

# Sonar Setup

Diagnose SonarQube MCP connectivity and guide the user through configuration.

**Announce at start:** "Checking SonarQube setup."


## Process

### Step 1: Check environment variables

Run a shell command to check which env vars are set (never print token values):

```bash
echo "SONARQUBE_URL: ${SONARQUBE_URL:-(not set)}"
echo "SONARQUBE_TOKEN: ${SONARQUBE_TOKEN:+set (hidden)}${SONARQUBE_TOKEN:-(not set)}"
echo "SONARQUBE_IDE_PORT: ${SONARQUBE_IDE_PORT:-(not set)}"
```

If `SONARQUBE_URL` or `SONARQUBE_TOKEN` are missing, guide the user:

> Set these environment variables to connect:
>
> ```bash
> export SONARQUBE_URL="https://your-sonarqube-instance"
> export SONARQUBE_TOKEN="your-token"
> ```
>
> Generate a token at `<your-sonarqube>/account/security/`.


### Step 2: Check server reachability

If both URL and token are set, test connectivity:

```bash
curl -sf --connect-timeout 5 "${SONARQUBE_URL}/api/system/status" 2>/dev/null || echo "UNREACHABLE"
```

If unreachable, suggest common causes:
- VPN not connected (common for corporate SonarQube instances)
- Server URL is wrong
- Token expired or revoked


### Step 3: Check MCP tool availability

Search for SonarQube MCP tools using ToolSearch.
Look for `search_sonar_issues_in_projects` (standalone) and `analyze_file_list` (IDE-connected).

Report findings as a table:

| Tool | Status | What it enables |
|------|--------|-----------------|
| `search_sonar_issues_in_projects` | Found / Not found | Issue browsing, fix, triage |
| `get_project_quality_gate_status` | Found / Not found | Quality gate checks |
| `get_component_measures` | Found / Not found | Dashboard metrics |
| `analyze_file_list` | Found / Not found | Local pre-push analysis |


### Step 4: Discover IDE ports

Scan the SonarQube for IDE port range to find **all** active instances:

```bash
for port in $(seq 64120 64130); do
  if curl -sf --connect-timeout 0.5 -o /dev/null "http://localhost:${port}" 2>/dev/null; then
    echo "SonarQube for IDE found on port ${port}"
  fi
done
```

Report all active ports — each one corresponds to a different IDE instance.

If a port is found but `SONARQUBE_IDE_PORT` is not set, guide the user:

> SonarQube for IDE detected on port `<port>`.
> To enable local analysis, set the env var before starting Claude Code:
>
> ```bash
> export SONARQUBE_IDE_PORT=<port>
> ```
>
> The port may change when you restart your IDE.
> Re-run `/code-quality:sonar-setup` to find the new port.

If multiple ports are active, explain:

> Multiple SonarQube for IDE instances detected (ports: `<list>`).
> Each corresponds to a different IDE.
> Set `SONARQUBE_IDE_PORT` to the one you want Claude Code to analyze with.
> You cannot switch mid-session — changing requires restarting Claude Code.


### Step 5: Report detected mode

Summarize the overall setup status:

**Full setup (IDE-connected):**
> SonarQube is fully configured.
> All code-quality skills are functional, including local pre-push analysis via `sonar-verify`.

**Standalone mode:**
> SonarQube is connected in standalone mode.
> Remote skills work: `sonar-status`, `sonar-issues`, `sonar-fix`, `sonar-triage`, `sonar-rule`.
> Local analysis (`sonar-verify`) requires IDE-connected mode — see Step 4.

**Not configured:**
> SonarQube MCP is not available.
> Code-quality skills will not work until the MCP server is configured.

If MCP tools are not found, show the config snippet:

```jsonc
// Add to your MCP configuration
// Standalone mode (remote analysis only):
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "mcp/sonarqube"
      ]
    }
  }
}
```

```jsonc
// Full-power mode (adds local analysis):
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "-e", "SONARQUBE_IDE_PORT",
        "mcp/sonarqube"
      ]
    }
  }
}
```

On **Linux**, add `"--network=host"` to the args array (before `"mcp/sonarqube"`) so the Docker container can reach SonarQube for IDE on localhost.


## Common Mistakes

| Don't | Do |
|-------|-----|
| Print or log the `SONARQUBE_TOKEN` value | Only confirm it is set — never reveal |
| Assume the IDE port is always 64120 | Scan the full range 64120-64130 |
| Hardcode a SonarQube URL in the config snippet | Use env var pass-through so the config is project-agnostic |
| Skip the reachability check | Always verify — VPN/firewall issues are the most common problem |
| Tell the user to restart Claude Code for every port change | Suggest re-running `/code-quality:sonar-setup` to detect the new port, then restart only if needed |
| Forget the Linux `--network=host` flag | Docker on Linux cannot reach localhost without it — macOS/Windows work without it |
