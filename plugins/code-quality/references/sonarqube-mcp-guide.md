# SonarQube MCP — Practical Guide

Curated guardrails, taxonomy reference, and operational patterns for skills and the orchestrator agent.
For installation and environment variables, see `official-docs.md`.


## Two Modes

| Mode | What you need | What it gives you |
|------|--------------|-------------------|
| **Standalone** | `SONARQUBE_URL` + `SONARQUBE_TOKEN` | Query remote analysis results — quality gates, issues, metrics, rules, triage |
| **IDE-connected** | Standalone + SonarQube for IDE in your editor | All of the above + `analyze_file_list` — analyze local files before pushing |

Start with standalone — it covers 90% of daily use: checking PRs, browsing issues, looking up rules, triaging false positives.
Add IDE-connected mode when you want to catch issues before pushing.


## Bug Guardrails

These are real bugs discovered through use.
They are not documented in the MCP server README.

| Bug | What happens | Workaround |
|-----|-------------|------------|
| `severities` param crashes the server | Type-cast failure (string → List) kills the MCP process | **Never pass `severities`.** Fetch all, filter client-side. |
| `ps=500` exceeds transport limit | ~122K chars → auto-saved to temp file, not returned inline | **Use `ps=50` max.** Paginate: 5 pages of 50 for ~250 issues. |

**These guardrails are non-negotiable.**
Every skill that calls `search_sonar_issues_in_projects` must enforce them.


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


## Token Management

Large result sets can exceed the MCP transport limit or blow up the conversation context.
Follow these patterns to stay safe.

1. **Paginate with `ps=50`** — never exceed 50 per page.
2. **Write large results to `.agents.tmp/`** — e.g., `.agents.tmp/sonar-issues/issues-p1.jsonl`.
3. **Extract with `jq`** — unique files, severity counts, rule distributions.
4. **Never read full JSONL into context** — always process with shell tools or subagents.

For projects with > 100 issues, use the token-safe collection workflow described in `sonarqube-mcp-tools.md`.


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


## Setup Minimum

Two environment variables give you quality gates, issue search, rule lookup, metrics, and triage — everything except local file analysis.

Generate your token at `https://<your-sonarqube>/account/security/`.

```jsonc
// Minimum — standalone mode (remote analysis only)
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "--init", "--pull=always", "-i", "--rm",
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

**Full-power config** (adds local analysis, debug logging, optional toolsets):

```jsonc
{
  "mcpServers": {
    "sonarqube": {
      "command": "docker",
      "args": [
        "run", "--init", "--pull=always", "-i", "--rm",
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

| Variable | What it unlocks |
|----------|----------------|
| `SONARQUBE_IDE_PORT` | `analyze_file_list` — local pre-push analysis via SonarQube for IDE (port range: 64120–64130) |
| `SONARQUBE_TOOLSETS` | `sources`, `coverage`, `languages` — disabled by default to reduce context overhead |
| `SONARQUBE_DEBUG_ENABLED` | Logs to STDERR + file — useful for troubleshooting MCP connection issues |
| `SONARQUBE_READ_ONLY` | Set to `true` to disable all write operations (triaging, webhooks) |


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
