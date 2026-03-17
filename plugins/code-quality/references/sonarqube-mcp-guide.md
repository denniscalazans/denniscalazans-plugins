# SonarQube MCP — Practical Guide

Curated guardrails, taxonomy reference, and operational patterns for skills and the orchestrator agent.
For installation and environment variables, see `official-docs.md`.


## Architecture

Three distinct layers — most confusion comes from conflating them:

```
AI Agent <──stdio──> SonarQube MCP Server <──HTTP──> SonarQube for IDE (localhost:641XX)
                                          <──HTTP──> SonarQube Server (remote)
```

| Layer | What it is | Where it runs |
|-------|-----------|---------------|
| **SonarQube Server** | Central analysis platform (e.g., `your-sonarqube-server.com`) | Remote |
| **SonarQube MCP Server** | Docker container (`mcp/sonarqube`) bridging AI agents to SonarQube | Local (stdio) or shared (HTTPS) |
| **SonarQube for IDE** | IDE extension/plugin (formerly SonarLint) with an embedded HTTP server | Inside VS Code / IntelliJ |

The MCP server sits in the middle.
It can talk to the remote server (standalone mode) and/or to the local IDE extension (IDE-connected mode).


## Two Modes

| Mode | What you need | What it gives you |
|------|--------------|-------------------|
| **Standalone** | `SONARQUBE_URL` + `SONARQUBE_TOKEN` | Query remote analysis results — quality gates, issues, metrics, rules, triage |
| **IDE-connected** | Standalone + SonarQube for IDE in your editor + `SONARQUBE_IDE_PORT` | All of the above + `analyze_file_list` — analyze local files before pushing |

Start with standalone — it covers 90% of daily use: checking PRs, browsing issues, looking up rules, triaging false positives.
Add IDE-connected mode when you want to catch issues before pushing.


## Three Workflows

These are the three ways you'll use the MCP server day-to-day.
Each builds on the previous.


### 1. Remote analysis — "Did my PR pass?"

**When:** After you push a branch or open a PR.
Your CI pipeline runs the Sonar scan automatically.
Use the MCP to check the result without opening the web UI.

**Check the quality gate:**

```
get_project_quality_gate_status { projectKey: "<your-project>", pullRequest: "123" }
```

For a feature branch (not yet a PR):

```
get_project_quality_gate_status { projectKey: "<your-project>", branch: "feat/my-feature" }
```

**See what issues were found:**

```
search_sonar_issues_in_projects {
  projects: ["<your-project>"],
  pullRequestId: "123",
  issueStatuses: ["OPEN"],
  ps: 50
}
```

**Get the dashboard numbers** (coverage, bugs, smells):

```
get_component_measures {
  component: "<your-project>",
  metricKeys: ["coverage", "code_smells", "bugs", "vulnerabilities", "ncloc"],
  branch: "main"
}
```

**Understand a rule** you've never seen before:

```
show_rule { key: "typescript:S3863" }
```

This returns the full rule description with noncompliant and compliant code examples.
Much faster than searching the web.


**Triage a false positive** (marks it on the server so it won't flag again):

```
change_sonar_issue_status { key: "<issue-uuid>", status: "falsepositive" }
```

You get the issue `key` (UUID) from `search_sonar_issues_in_projects`.


### 2. Fix while coding — "What's still broken in my local files?"

**When:** You've fixed some issues locally and want to verify before pushing.
Requires **IDE-connected mode** (`SONARQUBE_IDE_PORT` set).

**Analyze local files:**

```
analyze_file_list {
  file_absolute_paths: [
    "/absolute/path/to/your-component.ts",
    "/absolute/path/to/another-file.ts"
  ]
}
```

This runs SonarQube for IDE on your local files using the **same ruleset** as the server.
The file does not need to be open in the editor.

**What you get back:**

```json
{
  "findings": [
    {
      "severity": "MINOR",
      "message": "'@my-project/ui' imported multiple times.",
      "filePath": "/absolute/path/to/your-component.ts",
      "textRange": { "startLine": 4, "endLine": 4 }
    }
  ],
  "findingsCount": 1
}
```

**Important limitation:** local findings have only 4 fields — `severity`, `message`, `filePath`, `textRange`.
There is **no `rule` key** and **no issue UUID**.
You cannot triage a local finding directly — you need the server issue UUID from `search_sonar_issues_in_projects`.


### 3. RED/GREEN validation — "Which server issues did I actually fix?"

**When:** The server has N issues from the last CI scan.
You've fixed some locally.
You want to know which are resolved and which remain — before pushing.

Cross-reference server issues with local analysis:

| State | Meaning |
|-------|---------|
| 🔴 **RED** | Issue on server AND still found locally — not fixed yet |
| 🟢 **GREEN** | Issue on server but NOT found locally — your fix works, push it |
| 🆕 **NEW** | Found locally but NOT on server — you introduced something new |

**How matching works:** same file + line within ±5 + similar message text.
The ±5 tolerance accounts for local edits shifting line numbers relative to the last scan.

This workflow is most useful when you're working through a batch of issues and want confidence before pushing.
See `sonarqube-mcp-tools.md` for the full matching algorithm and token-safe collection workflow.


## IDE-Connected Mode — How It Works

### The embedded server

Every SonarQube for IDE instance (VS Code, IntelliJ, Eclipse) uses the same core library: `sonarlint-core`.
On startup, this library launches a small **embedded HTTP server** on the first available port in **64120–64130** (11 ports).
The port range is **hardcoded** in `EmbeddedServer.java` — it is **not configurable**.
There is an [open feature request](https://community.sonarsource.com/t/allow-configurable-port-range-for-the-sonarlint-embedded-server-to-support-multi-user-remote-environ/177897) for configurable ports, but it has not been implemented.

Port selection is first-come, first-served:

| Startup order | Gets port |
|---------------|-----------|
| First IDE | 64120 |
| Second IDE | 64121 |
| Third IDE | 64122 |
| ... | ...up to 64130 |

If you restart an IDE, it may grab a **different** port than before.

### What `SONARQUBE_IDE_PORT` does

This env var tells the MCP server **which port to connect TO** — it is the address of the IDE's embedded server.
The MCP server does **NOT** auto-discover IDE ports.
You must set `SONARQUBE_IDE_PORT` explicitly.

Setting it unlocks two tools:
- `analyze_file_list` — sends files to the IDE for local analysis
- `toggle_automatic_analysis` — controls auto-analysis in the IDE

Without it, the MCP server works in standalone mode only.

### How to find the port

| IDE | Method |
|-----|--------|
| **VS Code** | Quick Install button auto-configures `SONARQUBE_IDE_PORT` in MCP config. Or check OUTPUT > SonarQube for IDE for `Started embedded server on port <N>`. |
| **IntelliJ** | Check the SonarQube for IDE log tab for `Started embedded server on port <N>`. No auto-configuration. |
| **Claude Code** | Must be set manually — check which IDE port you want to connect to. |


## Multi-IDE Setup — Full Panorama

### How many ports does each IDE consume?

IntelliJ and VS Code handle SLOOP (SonarLint Out Of Process) differently:

- **IntelliJ** uses an application-level singleton (`@Service(Service.Level.APP)` in `BackendService.kt`).
  All project windows share **one SLOOP process** and **one port** — even with multiple projects open.
- **VS Code** spawns a new extension host per window.
  Each window gets its **own SLOOP process** and its **own port**.

| Scenario | SLOOP Processes | Ports consumed |
|----------|----------------|----------------|
| IntelliJ with 3 projects (3 windows) | **1** | **1** port |
| VS Code with 3 workspace windows | **3** | **3** ports |
| IntelliJ + 2 VS Code windows | **3** | **3** ports |


### Example: realistic multi-IDE developer setup

Developer has IntelliJ open with two projects (`rental-api` and `tenant-portal`) and one VS Code window for `infra-config`.
Three AI agents are running: IntelliJ GitHub Copilot, VS Code GitHub Copilot, and Claude Code.

```
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 1: SonarQube for IDE (embedded HTTP servers)                  │
│                                                                     │
│  IntelliJ (rental-api + tenant-portal)  ──→  localhost:64120        │
│  VS Code  (infra-config)                ──→  localhost:64121        │
│                                                                     │
│  Note: IntelliJ uses ONE port for BOTH projects.                    │
│  Note: If a second VS Code window opens, it grabs 64122.           │
├─────────────────────────────────────────────────────────────────────┤
│ LAYER 2: SonarQube MCP Servers (Docker containers, stdio)           │
│                                                                     │
│  IntelliJ Copilot MCP  ──→  SONARQUBE_IDE_PORT=64120               │
│  VS Code Copilot MCP   ──→  SONARQUBE_IDE_PORT=64121               │
│  Claude Code MCP       ──→  SONARQUBE_IDE_PORT=64120               │
│                                                                     │
│  Each is an independent Docker process (stdio transport).           │
│  They do NOT conflict with each other.                              │
├─────────────────────────────────────────────────────────────────────┤
│ LAYER 3: SonarQube Server (remote)                                  │
│                                                                     │
│  All three MCP servers connect to your-sonarqube-server.com             │
│  via SONARQUBE_URL + SONARQUBE_TOKEN (same for all).                │
└─────────────────────────────────────────────────────────────────────┘
```


### Can multiple MCP servers share the same IDE port?

**Yes.** The embedded server is stateless HTTP with no session tracking.

Source code evidence from `sonarlint-core`:
- `DontKeepAliveReuseStrategy` — every connection closes after each response.
  No persistent connections, no WebSockets.
- `AnalyzeFileListRequestHandler` — no `synchronized` blocks, no locks.
  Each request creates a fresh `SonarLintCancelMonitor` and dispatches analysis via `CompletableFuture`.
- No cookies, no session IDs, no client identity tracking.

In the example above, **both IntelliJ Copilot MCP and Claude Code MCP point at port 64120**.
This is fine — they both send HTTP POST requests to IntelliJ's embedded server, and both receive analysis results for `rental-api` and `tenant-portal` files.

**One caveat: shared rate limit.**
The embedded server enforces a `RateLimitFilter`: **10 requests per `Origin` header per 10-second window**.
Both MCP servers send `Origin: http://localhost`, so they share the same bucket.
For typical usage (analyzing a few files at a time) this is unlikely to be hit.
For batch operations (e.g., `sonar-verify` analyzing 50+ files), stagger requests or use one MCP server at a time.


### Key constraints

- You **cannot** assign fixed ports to specific IDEs — the port range is hardcoded and allocation is dynamic.
- Restarting any IDE can **shuffle port assignments** — your MCP config may point at the wrong IDE.
- VS Code's Quick Install button handles re-configuration automatically, but **IntelliJ and Claude Code do not**.
- Claude Code's MCP server connects to whichever IDE owns the configured port — it does not distinguish between them.
- Each MCP server runs as a separate stdio process — they do not conflict with each other.
- Multiple MCP servers can safely share the same `SONARQUBE_IDE_PORT` (shared rate limit: 10 req/10s).


### Port discovery command

To check which IDE owns which port at any time:

```bash
lsof -iTCP:64120-64130 -sTCP:LISTEN -P -n
```

Then map PIDs to IDEs:

```bash
ps -p <PID> -o command= | head -c 120
```

Look for `sonarlint-ls.jar` (VS Code) or `SonarLintServerCli` (IntelliJ) in the output.


### Practical advice

- **Single IDE workflow:** Point `SONARQUBE_IDE_PORT` at your primary IDE's port.
  Claude Code and the IDE's Copilot can safely share it.
- **Multi-IDE workflow:** Check ports after startup with `lsof`.
  Point Claude Code at whichever IDE has the project you're working on.
- **After IDE restart:** Re-check ports — they may have changed.


## Bug Guardrails

These are real bugs discovered through use.
They are not documented in the MCP server README.

| Bug | What happens | Workaround |
|-----|-------------|------------|
| `ps=500` exceeds transport limit | ~122K chars → auto-saved to temp file, not returned inline | **Use `ps=50` max.** Paginate: 5 pages of 50 for ~250 issues. |

**This guardrail is non-negotiable.**
Every skill that calls `search_sonar_issues_in_projects` must enforce it.


## Legacy vs Clean Code Taxonomy

SonarQube 10+ runs two classification systems in parallel.
The MCP API and the web UI can show different numbers for the same project — this is expected behavior, not a bug.

| Aspect | Legacy (what the UI shows) | Clean Code (what the MCP API uses) |
|--------|----------------------------|-----------------------------------|
| **Types** | Bug, Vulnerability, Code Smell | Reliability, Security, Maintainability |
| **Severities** | Blocker, Critical, Major, Minor, Info | HIGH, MEDIUM, LOW |
| **Counting** | One type + one severity per issue | Multiple impacts per issue |

**Why counts differ:** filtering `search_sonar_issues_in_projects` by impact severity can double-count issues with multiple impacts.
An issue with MEDIUM maintainability + LOW reliability impact appears in both result sets.

**The fix — use the right tool:**

| Goal | Tool | Why |
|------|------|-----|
| Dashboard numbers (always match UI) | `get_component_measures` | Returns legacy counts directly |
| Issue details (file, line, rule, message) | `search_sonar_issues_in_projects` | Full issue objects, but severity totals may differ from UI |
| Accurate severity counts | Fetch all issues, group by each issue's `severity` field | Legacy severity is included per issue |


## Token Management — Subagent Delegation

MCP tools that return issue lists (`search_sonar_issues_in_projects`, `analyze_file_list` in batch) must ALWAYS run in subagents.
The subagent writes results to disk and returns only a summary.

This applies regardless of result set size — even 10 issues produce ~120 tokens of JSON each.
The main conversation should never see raw MCP JSON responses.

1. **Paginate with `ps=50`** — never exceed 50 per page.
2. **Always write results to `.agents.tmp/code-quality/`** — e.g., `.agents.tmp/code-quality/issues/issues-p1.jsonl`.
3. **Extract with `jq`** — unique files, severity counts, rule distributions.
4. **Never read full JSONL into context** — always process with shell tools or subagents.
5. **Subagents return summaries only** — counts, severity breakdowns, formatted tables, file paths to JSONL on disk.

See `sonarqube-mcp-tools.md` for the subagent return contract and token-safe collection workflow.


## Permission-Blocked Tools

Standard user tokens (not admin) cannot access these tools.
Do not call them — they will always fail.

| Tool | Why blocked |
|------|-------------|
| `ping_system`, `get_system_health`, `get_system_info`, `get_system_logs` | Admin-only |
| `list_webhooks`, `create_webhook` | Requires Administer permission |
| `list_portfolios` | Feature not enabled (404) on non-Enterprise editions |
| `search_dependency_risks` | Requires Enterprise 2025.4+ |

Use `get_system_status` or `get_project_quality_gate_status` to verify connectivity.


## Local Findings Limitations

`analyze_file_list` returns findings with only 4 fields: `severity`, `message`, `filePath`, `textRange`.
There is **no `rule` key** and **no issue UUID**.

You cannot triage a local finding directly.
To triage: find the matching server issue via `search_sonar_issues_in_projects` (match by file + line + message), then use its `key` to call `change_sonar_issue_status`.


## Setup FAQ

These are the questions that come up most often during setup and onboarding.


### "What's the minimum config to get started?"

Two environment variables.
This gives you quality gates, issue search, rule lookup, metrics, and issue triage — everything except local file analysis.

Generate your token at `https://<your-sonarqube>/account/security/`.

```jsonc
// Minimum — standalone mode (remote analysis only)
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run",
        "--init",          // proper signal handling for clean shutdown
        "--pull=always",   // always use latest MCP server image
        "-i",              // keep stdin open (required for MCP protocol)
        "--rm",            // remove container when done (ephemeral)
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "mcp/sonarqube"
      ],
      "env": {
        "SONARQUBE_URL": "https://<your-sonarqube>",
        "SONARQUBE_TOKEN": "<your-token>"
      }
    }
  }
}
```

**What's enabled:** 10 of 15 toolsets with 17 tools (projects, analysis, issues, quality-gates, rules, measures, duplications, security-hotspots, coverage, dependency-risks).
Without `SONARQUBE_IDE_PORT`, `analysis` gives you `analyze_code_snippet` (snippet-only analysis).
No need to set `SONARQUBE_TOOLSETS`, `STORAGE_PATH`, or any other variable.


### "What's the full-power config?"

Add IDE-connected mode for local analysis, debug logging, and opt-in toolsets (`sources`, `languages`).

```jsonc
// Full power — IDE-connected mode + all useful toolsets + debug logging
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run",
        "--init",
        "--pull=always",
        "-i",
        "--rm",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "-e", "SONARQUBE_IDE_PORT",
        "-e", "SONARQUBE_TOOLSETS",
        "-e", "SONARQUBE_DEBUG_ENABLED",
        "mcp/sonarqube"
      ],
      "env": {
        "SONARQUBE_URL": "https://<your-sonarqube>",
        "SONARQUBE_TOKEN": "<your-token>",
        "SONARQUBE_IDE_PORT": "64120",
        "SONARQUBE_TOOLSETS": "analysis,issues,security-hotspots,projects,quality-gates,rules,duplications,measures,coverage,sources,languages",
        "SONARQUBE_DEBUG_ENABLED": "true"
      }
    }
  }
}
```

**What this adds over minimum:**

| Variable | What it unlocks |
|----------|----------------|
| `SONARQUBE_IDE_PORT` | `analyze_file_list` + `toggle_automatic_analysis` — local pre-push analysis via SonarQube for IDE. The port the MCP server connects TO on the IDE's embedded server (range: 64120–64130, not configurable). See "IDE-Connected Mode" section above. |
| `SONARQUBE_TOOLSETS` | `sources` (view indexed files), `languages` (list supported languages) — disabled by default to reduce context overhead |
| `SONARQUBE_DEBUG_ENABLED` | Logs to STDERR + `STORAGE_PATH/logs/mcp.log` — useful for troubleshooting MCP connection issues |

> **Linux Docker only:** add `"--network=host"` to the `args` array so the container can reach the IDE server on localhost.
> macOS doesn't need this — Docker Desktop handles it automatically.


### "Do I need to set `SONARQUBE_TOOLSETS`?"

**No.** When not set, 10 of 15 toolsets are enabled by default — covering issues, quality gates, rules, measures, security hotspots, duplications, coverage, analysis, dependency-risks, and projects (always on).
Setting it **overrides the defaults entirely** (except `projects`, which is always on).
Only set it if you specifically need `sources` or `languages`, or if you want to drop the 4 dead toolsets.
([source](https://docs.sonarsource.com/sonarqube-mcp-server/build-and-configure/environment-variables))

**IDE port effect on `analysis` toolset:** Without `SONARQUBE_IDE_PORT`, you get `analyze_code_snippet` (1 tool).
With it, the server swaps to `analyze_file_list` + `toggle_automatic_analysis` (2 tools).
They are mutually exclusive — you never get both.

See `sonarqube-mcp-tools.md` for the recommended value and the full dead-toolsets list.


### "Do I need to set `STORAGE_PATH`?"

**Not with Docker.** The container image pre-sets it to `/app/storage` internally.
Only set it if you run the JAR directly (non-Docker).
([source: Dockerfile](https://github.com/SonarSource/sonarqube-mcp-server))


### "Can I make it read-only?"

Yes. Add `SONARQUBE_READ_ONLY=true` to disable all write operations (triaging issues, creating webhooks).
Useful for shared tokens or demo environments.

```jsonc
// Add to env block:
"SONARQUBE_READ_ONLY": "true"
```


### "What you DON'T need to set"

| Variable | Why not |
|----------|---------|
| `STORAGE_PATH` | Docker image pre-sets `/app/storage` — only set for JAR mode |
| `SONARQUBE_PROJECT_KEY` | Omit to query any project; set only to lock to one project |
| `SONARQUBE_ORG` | SonarQube Cloud only — not needed for self-hosted instances |


### "Which token type should I use?"

**Always use a User Token.**

SonarQube offers three token types: User Token, Project Analysis Token, and Global Analysis Token.
Analysis tokens are designed for CI pipelines pushing scan results — they lack the Browse permission needed by many MCP tools.

With an analysis token, 4–6 tools silently fail at call time (403) — including coverage, security hotspots, and duplications.
The tools still register normally at startup, so there's no warning until you try to use them.

A User Token inherits your full user permissions and has **zero tool denials**.
Generate one at `https://<your-sonarqube>/account/security/`.

See `sonarqube-mcp-tools.md` → "Token Type Scope" for the full denial table per token type.


### "Should I set `SONARQUBE_PROJECT_KEY`?"

**Yes — in per-project configs.**

Setting `SONARQUBE_PROJECT_KEY` removes the `projectKey` parameter from 4 frequently-used tool schemas: issue search, quality gate status, PR listing, and coverage search.
This means simpler prompts and fewer chances for the AI to pass the wrong project key.

19 tools are unaffected (they use `key`, `hotspotKey`, etc.), and 5 tools keep `projectKey` as optional even when the variable is set.

Set it in your project-level `.mcp.json` (not your global config) so it's scoped to the right project.
See `sonarqube-mcp-tools.md` → "`SONARQUBE_PROJECT_KEY` Effect" for the full schema diff.


### "Can I share config with my team?"

Use a project-level `.mcp.json` file — it's committable and team-shareable.

```jsonc
// .mcp.json (project root — commit this)
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "--init", "--pull=always", "-i", "--rm",
        "-e", "SONARQUBE_TOKEN",
        "-e", "SONARQUBE_URL",
        "-e", "SONARQUBE_PROJECT_KEY",
        "-e", "SONARQUBE_IDE_PORT",
        "-e", "SONARQUBE_TOOLSETS",
        "mcp/sonarqube"
      ],
      "env": {
        "SONARQUBE_URL": "https://<your-sonarqube>",
        "SONARQUBE_PROJECT_KEY": "<your-project>",
        "SONARQUBE_TOOLSETS": "analysis,issues,security-hotspots,projects,quality-gates,rules,duplications,measures,coverage,sources,languages"
      }
    }
  }
}
```

**Critical:** The token must be per-user — **never commit tokens** to version control.
Each developer sets `SONARQUBE_TOKEN` in their personal config (e.g., `~/.claude.json` or shell env).
The `"SONARQUBE_TOKEN"` entry in `args` (without a value in `env`) tells Docker to inherit the variable from the host environment.

`SONARQUBE_IDE_PORT` is also per-user (it depends on which IDE instance owns which port).
Include it in `args` for passthrough, but let each developer set the value in their personal config.


## Troubleshooting

Common issues encountered during setup and daily use.


### "Failed to reconnect to sonarqube"

**Symptoms:** MCP server logs show reconnection failures or timeouts.

**Causes and fixes:**

| Cause | Fix |
|-------|-----|
| Docker not running | Start Docker Desktop or the Docker daemon |
| Invalid or expired token | Generate a new User Token at `https://<your-sonarqube>/account/security/` |
| Network/VPN issue | Verify you can reach `<your-sonarqube>` from your machine (`curl -s https://<your-sonarqube>/api/system/status`) |
| Wrong URL | Check `SONARQUBE_URL` — must include `https://` and no trailing slash |


### "`analyze_file_list` not available"

**Symptoms:** The tool doesn't appear in the MCP tool list, or you get `analyze_code_snippet` instead.

**Causes and fixes:**

| Cause | Fix |
|-------|-----|
| `SONARQUBE_IDE_PORT` not set | Add it to your MCP config — see "Full-power config" above |
| IDE not running | Start your IDE (VS Code / IntelliJ) with SonarQube for IDE installed |
| Port mismatch | Run `lsof -iTCP:64120-64130 -sTCP:LISTEN -P -n` to find the actual port, then update `SONARQUBE_IDE_PORT` |
| Linux Docker networking | Add `"--network=host"` to Docker args so the container can reach `localhost` |


### "IDE port keeps changing"

The embedded server port range (64120–64130) is **hardcoded** in `sonarlint-core`.
Port allocation is first-come, first-served — restarting an IDE can grab a different port.

**Mitigations:**
- Start your primary IDE first to get a consistent port (usually 64120).
- After IDE restarts, re-check with `lsof -iTCP:64120-64130 -sTCP:LISTEN -P -n`.
- VS Code's Quick Install button auto-updates the port in MCP config; IntelliJ and Claude Code require manual updates.


### "Numbers don't match the web UI exactly"

The MCP API uses the **Clean Code taxonomy** by default, while the SonarQube web UI shows the **legacy taxonomy**.
These count issues differently — an issue with multiple impact qualities (e.g., MEDIUM maintainability + LOW reliability) can appear in multiple severity buckets in the API, inflating totals.

**The fix:** Use `get_component_measures` for accurate counts that always match the web UI.
Use `search_sonar_issues_in_projects` for issue details (file, line, message, rule), but don't rely on its severity totals matching the dashboard.

See the "Legacy vs Clean Code Taxonomy" section above for the full breakdown.


## Metrics Cheat Sheet

Use with `get_component_measures` — pass as `metricKeys`:

| Key | What it measures |
|-----|-----------------|
| `coverage` | Line coverage % |
| `new_coverage` | Coverage on new code only |
| `code_smells` | Code smell count |
| `bugs` | Bug count |
| `vulnerabilities` | Security vulnerability count |
| `security_hotspots` | Security hotspot count |
| `duplicated_lines_density` | Duplication % |
| `ncloc` | Lines of code (non-comment) |
| `violations` / `new_violations` | Total / new-code rule violations |
| `blocker_violations` / `critical_violations` | Severity-specific counts |
