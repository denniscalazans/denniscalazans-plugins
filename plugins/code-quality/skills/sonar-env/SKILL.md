---
name: sonar-env
description: >
  Use when inspecting the local SonarQube infrastructure: which IDE embedded servers are running, which ports they own, and which MCP Docker containers are active.
  Also use when the user asks "what's listening on the sonar ports?", "which IDE is my MCP connected to?", or wants to check for port mismatches or orphaned containers.
  Triggers: "sonar environment", "sonar ports", "sonar-env", "sonar containers", "mcp containers", "port mismatch", "what's running", "check sonar infra", "sonar docker".
---

# Sonar Env

Diagnose the local SonarQube infrastructure — embedded IDE servers, MCP containers, and port wiring.

**Announce at start:** "Scanning SonarQube infrastructure."


## Process

### Step 1: Collect data

Run the bundled collection script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/sonar-env/scripts/collect.sh"
```

The script outputs two sections: `EMBEDDED_SERVERS` and `MCP_CONTAINERS`.
It is read-only — it never stops containers or changes configuration.


### Step 2: Parse embedded servers

From the `EMBEDDED_SERVERS` section, identify each IDE by its command string:

| Pattern in CMD | IDE |
|----------------|-----|
| `sonarlint-ls.jar` | VS Code |
| `SonarLintServerCli` | IntelliJ |
| `sonarlint` (other) | Eclipse or other |

Each line has `PID`, `PORT`, and `CMD`.
If the section says `SKIP`, `lsof` is not available — inform the user.


### Step 3: Parse MCP containers

From the `MCP_CONTAINERS` section, extract:
- `NAME` — container name
- `IDE_PORT` — the `SONARQUBE_IDE_PORT` env var (the port the MCP connects TO)
- `URL` — the `SONARQUBE_URL` env var
- `CREATED` — when the container was spawned

If the section says `SKIP`, Docker is not available.
If it says `NONE`, no `mcp/sonarqube` containers are running.


### Step 4: Cross-reference and detect mismatches

Compare the MCP containers' `IDE_PORT` values against the actual listening ports from Step 2.

Flag these issues:

**Port mismatch:** An MCP container's `IDE_PORT` points to a port where no IDE is listening.
This means `analyze_file_list` will fail silently — the MCP server cannot reach the IDE.

**Orphaned containers:** Multiple MCP containers running with the same configuration.
This wastes resources and can happen when Claude Code sessions don't clean up.

**Unconnected IDE:** An IDE embedded server is listening but no MCP container points to its port.
The IDE's local analysis is available but no AI agent is wired to it.


### Step 5: Present results

Format the output as two tables plus a diagnostics section.

**Example output:**

```
## SonarQube for IDE — Embedded Servers

| IDE      | Port  | PID   |
|----------|-------|-------|
| VS Code  | 64120 | 15851 |
| IntelliJ | 64121 | 40780 |


## SonarQube MCP Containers

| Container       | IDE Port | URL                          | Created             |
|-----------------|----------|------------------------------|---------------------|
| sweet_wing      | 64120    | https://sonarqube.example.com | 2026-03-16 09:31:10 |
| vibrant_mcnulty | 64120    | https://sonarqube.example.com | 2026-03-16 09:31:42 |


## Diagnostics

⚠️ Orphaned container: `vibrant_mcnulty` has the same config as `sweet_wing` — consider stopping it:
   docker stop vibrant_mcnulty

✅ VS Code (port 64120) ← connected via `sweet_wing`
⚠️ IntelliJ (port 64121) ← no MCP container wired to this port
```

If mismatches are found, output the corrective command but **never execute it**.
The user decides what to stop or reconfigure.


### Step 6: Suggest corrections

If a port mismatch is detected, suggest the fix:

> MCP container `<name>` is configured with `SONARQUBE_IDE_PORT=<wrong>` but that port has no listener.
> Active IDE ports: `<list>`.
> To reconnect, update your MCP config to use one of the active ports, then restart Claude Code.

If orphaned containers are found:

> Duplicate containers detected. To clean up:
> ```bash
> docker stop <container-name>
> ```


## References

For background on port allocation, multi-IDE setup, and the embedded server architecture:
- `references/sonarqube-mcp-guide.md` — "Multi-IDE Setup — Full Panorama" section
- `references/official-docs.md` — "SonarQube for IDE" and "Source Code References" sections


## Common Mistakes

| Don't | Do |
|-------|-----|
| Stop containers automatically | Output the `docker stop` command and let the user decide |
| Assume port 64120 is always VS Code | Parse the CMD string to identify the IDE |
| Show raw `lsof` or `docker inspect` output | Parse and present as clean tables |
| Ignore the case where Docker is not running | Handle gracefully — show embedded servers only |
| Print `SONARQUBE_TOKEN` values from containers | Only show `SONARQUBE_URL` and `SONARQUBE_IDE_PORT` |
| Run the script without `${CLAUDE_PLUGIN_ROOT}` | The script path is relative to the plugin root |
