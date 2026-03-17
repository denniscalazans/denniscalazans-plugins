# SonarQube MCP — Tool Catalogue & Schemas

Complete tool reference with response schemas, matching algorithm, and call examples.
Skills read specific sections on demand via progressive disclosure.


## Tool Discovery

SonarQube MCP tools are registered under the name the user chose for their MCP server configuration.
The full tool name follows the pattern `mcp__<server-name>__<base-tool-name>`.

For example, `search_sonar_issues_in_projects` might be registered as:
- `mcp__sonarqube__search_sonar_issues_in_projects`
- `mcp__sonar__search_sonar_issues_in_projects`
- `mcp__sq__search_sonar_issues_in_projects`

**Always discover tools by their base name suffix.**
Never hardcode a prefix — look for a tool whose name ends with the base name listed in this catalogue.
If no matching tool is found, the SonarQube MCP server is not configured.


## Tool Catalogue

### Default Toolsets (enabled without `SONARQUBE_TOOLSETS`)

#### `projects` (always on) — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_my_sonarqube_projects` | `q`, `page`, `pageSize` | Search projects by name fragment |
| `list_pull_requests` | `projectKey` | List all PRs for a project |

#### `analysis` — 1 tool (no IDE) / 2 tools (with IDE)

The `analysis` toolset registers **different tools** depending on whether `SONARQUBE_IDE_PORT` is set.
`analyze_code_snippet` and `analyze_file_list` are **mutually exclusive** — the server swaps one for the other based on IDE connectivity.

| Tool | Without IDE port | With IDE port | Notes |
|------|:---:|:---:|-------|
| `analyze_code_snippet` | ✅ Registered | ❌ Not registered | Snippet-only analysis — no file context |
| `analyze_file_list` | ❌ Not registered | ✅ Registered | Local analysis via SonarQube for IDE — the MCP server delegates to the IDE's embedded HTTP server on `localhost:<SONARQUBE_IDE_PORT>` |
| `toggle_automatic_analysis` | ❌ Not registered | ✅ Registered | Enable/disable auto-analysis as files change |

#### `issues` — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_sonar_issues_in_projects` | `projects[]`, `pullRequestId`, `issueStatuses[]`, `impactSoftwareQualities[]`, `severities[]`, `p`, `ps` | Use `ps=50` max. `severities` accepts legacy values: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`. |
| `change_sonar_issue_status` | `key`, `status` (`accept` / `falsepositive` / `reopen`) | Triage server issues |

#### `quality-gates` — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_project_quality_gate_status` | `projectKey`, `branch`, `pullRequest` | Returns OK/ERROR + condition details |
| `list_quality_gates` | — | List all available quality gates |

#### `rules` — 1 tool

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `show_rule` | `key` (e.g., `typescript:S3358`) | Full rule detail with noncompliant/compliant examples |

#### `measures` — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_component_measures` | `component`, `metricKeys[]`, `branch`, `pullRequest` | Dashboard metrics — always matches the web UI |
| `search_metrics` | `p`, `ps` | List all available metric keys |

#### `duplications` — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_duplications` | `key` (file key), `pullRequest` | Duplication blocks for a specific file |
| `search_duplicated_files` | `projectKey`, `pageIndex`, `pageSize`, `pullRequest` | Project-wide duplication report |

#### `security-hotspots` — 3 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_security_hotspots` | `projectKey`, `status[]`, `resolution[]`, `pullRequest`, `ps` | Filter by `TO_REVIEW` / `REVIEWED` |
| `show_security_hotspot` | `hotspotKey` | Rule details, code context, flows, comments |
| `change_security_hotspot_status` | `hotspotKey`, `status`, `resolution` (`FIXED`/`SAFE`/`ACKNOWLEDGED`), `comment` | Review hotspots |

#### `coverage` (default since MCP 1.10) — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_files_by_coverage` | `projectKey`, `maxCoverage`, `pageSize`, `pullRequest` | Sorted worst-first |
| `get_file_coverage_details` | `key` (file key), `pullRequest` | Line-by-line coverage detail |

### Optional Toolsets (must add to `SONARQUBE_TOOLSETS`)

#### `sources` — 2 tools

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_raw_source` | `key` (file key), `pullRequest` | File source as SonarQube indexed it |
| `get_scm_info` | `key`, `from`, `to`, `commits_by_line` | Per-line datetime (author/revision may be empty) |

#### `languages` — 1 tool

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `list_languages` | `q` (optional filter) | All languages the instance can analyze |


### Dead Toolsets (do NOT enable)

These toolsets register tools that always fail or register nothing.
Enabling them wastes context tokens without adding functionality.

| Toolset | Tools registered | Why dead |
|---------|:---:|----------|
| `dependency-risks` | **0** | Registers zero tools — requires Enterprise edition 2025.4+ |
| `portfolios` | 1 (`list_portfolios`) | Always returns 404 — endpoint doesn't exist on non-Enterprise editions |
| `webhooks` | 2 (`list_webhooks`, `create_webhook`) | Always returns 403 — requires `Administer` permission on the project |
| `system` | 5 (but 4 are 403) | Only `get_system_status` works without admin token — not worth the context overhead |


### Tool Count Summary

Probe-verified counts (2026-03-16) via MCP `tools/list` JSON-RPC request to isolated Docker containers.

| Configuration | Tools registered |
|---------------|:---:|
| Bare minimum (`SONARQUBE_URL` + `SONARQUBE_TOKEN`) | **17** |
| With `SONARQUBE_IDE_PORT` | **18** (swap `analyze_code_snippet` → `analyze_file_list`, add `toggle_automatic_analysis`) |
| All 15 toolsets, no IDE | **28** |
| All 15 toolsets + IDE | **29** |


### Per-Toolset Isolation Probe

Each toolset tested in isolation (2026-03-16) — `SONARQUBE_TOOLSETS` set to that single toolset plus `projects` (always on).
Shows exact tools registered and whether the IDE toggles any.

| Toolset | Tools (no IDE) | Tools (with IDE) | Tool names |
|---------|:-:|:-:|------------|
| `projects` | 2 | 2 | `search_my_sonarqube_projects`, `list_pull_requests` |
| `analysis` | 1 | 2 | Without IDE: `analyze_code_snippet`. With IDE: `analyze_file_list`, `toggle_automatic_analysis` |
| `issues` | 2 | 2 | `search_sonar_issues_in_projects`, `change_sonar_issue_status` |
| `quality-gates` | 2 | 2 | `get_project_quality_gate_status`, `list_quality_gates` |
| `rules` | 1 | 1 | `show_rule` |
| `measures` | 2 | 2 | `get_component_measures`, `search_metrics` |
| `duplications` | 2 | 2 | `get_duplications`, `search_duplicated_files` |
| `security-hotspots` | 3 | 3 | `search_security_hotspots`, `show_security_hotspot`, `change_security_hotspot_status` |
| `coverage` | 2 | 2 | `search_files_by_coverage`, `get_file_coverage_details` |
| `dependency-risks` | 0 | 0 | Nothing registered — requires Enterprise 2025.4+ |
| `sources` | 2 | 2 | `get_raw_source`, `get_scm_info` |
| `languages` | 1 | 1 | `list_languages` |
| `portfolios` | 1 | 1 | `list_portfolios` (always 404 on non-Enterprise) |
| `webhooks` | 2 | 2 | `list_webhooks`, `create_webhook` (always 403) |
| `system` | 5 | 5 | `get_system_status`, `ping_system`, `get_system_health`, `get_system_info`, `get_system_logs` (4 of 5 are 403) |

**Key observations:**
- Only `analysis` changes tool registration based on IDE connectivity.
- `projects` toolset is always on — it appears even when not listed in `SONARQUBE_TOOLSETS`.
- `dependency-risks` registers zero tools — the endpoint doesn't exist on non-Enterprise editions.


### Recommended `SONARQUBE_TOOLSETS` Value

Drop the 4 dead toolsets to avoid registering tools that always fail:

```
SONARQUBE_TOOLSETS=analysis,issues,security-hotspots,projects,quality-gates,rules,duplications,measures,coverage,sources,languages
```

**Important:** setting `SONARQUBE_TOOLSETS` **overrides the defaults entirely** (except `projects`, which is always on).
If you only set `SONARQUBE_TOOLSETS=sources`, you lose all default tools.
Always include the full set you want.


### Write / Mutate Tools

These tools modify state on the SonarQube server.
Set `SONARQUBE_READ_ONLY=true` to disable all of them.

| Tool | Toolset | What it does | Status |
|------|---------|-------------|--------|
| `change_sonar_issue_status` | `issues` | Triage issues: `accept`, `falsepositive`, `reopen` | Works with standard tokens |
| `change_security_hotspot_status` | `security-hotspots` | Review hotspots: `FIXED`, `SAFE`, `ACKNOWLEDGED` | Works with standard tokens |
| `create_webhook` | `webhooks` | Create project webhooks | Always 403 — requires `Administer` permission |

**`SONARQUBE_READ_ONLY=true` effect:**
Reduces registered tools from 17 → 15 by removing `change_sonar_issue_status` and `change_security_hotspot_status`.
`show_security_hotspot` (viewing) is kept — only status-change tools are blocked.
`create_webhook` is unaffected (it belongs to the `webhooks` toolset, which is not default-enabled).


### Token Type Scope

The SonarQube token type determines which tools succeed at runtime.
Probe-verified (2026-03-16) against isolated Docker containers with each token type.

| Token type | Tools denied at runtime | Notes |
|-----------|------------------------|-------|
| **User Token** | **0** | Full access to all tools the user's permissions allow |
| **Project Analysis Token** | 4–6 (varies by toolset config) | Denied: `search_files_by_coverage`, `get_file_coverage_details`, `search_security_hotspots`, `show_security_hotspot`, `get_duplications`, `search_duplicated_files` |
| **Global Analysis Token** | 4–6 (varies by toolset config) | Same denials as Project Analysis Token — analysis tokens lack Browse permission on project data |

**Why analysis tokens lose tools:** Analysis tokens are scoped to push analysis results only.
They lack the Browse permission required by coverage, security hotspot, and duplication endpoints.
The tools register normally but return 403 at call time — no error at startup.

**Recommendation:** Always use a **User Token** — it is the only type with zero denials.
Generate one at `https://<your-sonarqube>/account/security/`.


### `SONARQUBE_PROJECT_KEY` Effect

Setting `SONARQUBE_PROJECT_KEY` as an environment variable changes tool schemas at registration time.
Probe-verified (2026-03-16) via `tools/list` JSON-RPC diff between containers with and without the variable.

**Tools where `projectKey` is REMOVED from the schema (4 tools):**

| Tool | Toolset | Effect |
|------|---------|--------|
| `search_sonar_issues_in_projects` | `issues` | `projects` param removed — locked to the configured project |
| `get_project_quality_gate_status` | `quality-gates` | `projectKey` param removed |
| `list_pull_requests` | `projects` | `projectKey` param removed |
| `search_files_by_coverage` | `coverage` | `projectKey` param removed |

**Tools where `projectKey` stays optional (5 tools):**

| Tool | Toolset | Why kept |
|------|---------|----------|
| `search_security_hotspots` | `security-hotspots` | Also accepts `files`, `resolution` — needs explicit project when combining filters |
| `search_duplicated_files` | `duplications` | Supports `pageIndex`, `pageSize` — project key is part of a larger query |
| `get_component_measures` | `measures` | Uses `component` (not `projectKey`) — accepts any component key |
| `get_duplications` | `duplications` | Uses `key` (file key, not project key) |
| `search_dependency_risks` | `dependency-risks` | Uses `projectKey` but also `branchKey`, `pullRequestKey` |

19 tools are unaffected — they use `key`, `hotspotKey`, `file_absolute_paths`, or no project identifier at all.

**Recommendation:** Set `SONARQUBE_PROJECT_KEY` in per-project MCP configs.
It simplifies prompts by removing `projectKey` from 4 frequently-used tools.


## Response Schemas

### `search_sonar_issues_in_projects` — issue object

```json
{
  "key": "uuid-string",
  "rule": "typescript:S3358",
  "project": "<your-project>",
  "component": "<your-project>:path/to/file.ts",
  "severity": "MAJOR",
  "status": "OPEN",
  "message": "Human-readable issue description.",
  "cleanCodeAttribute": "CLEAR",
  "cleanCodeAttributeCategory": "INTENTIONAL",
  "author": "user@example.com",
  "creationDate": "2026-03-05T16:44:11+0000",
  "textRange": { "startLine": 62, "endLine": 62 }
}
```

12 fields per issue.
Severity values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO` (legacy taxonomy).

### `search_sonar_issues_in_projects` — paging object

```json
{ "pageIndex": 1, "pageSize": 50, "total": 142 }
```

### `analyze_file_list` — response object

```json
{
  "findings": [
    {
      "severity": "MINOR",
      "message": "Human-readable issue description.",
      "filePath": "/absolute/path/to/file.ts",
      "textRange": { "startLine": 4, "endLine": 4 }
    }
  ],
  "findingsCount": 1
}
```

**Only 4 fields per finding.**
No `rule` key, no issue UUID.
This is the critical constraint for the RED/GREEN matching algorithm.


## Component → Path Conversion

The `component` field in server issues uses the format `<project-key>:relative/path/to/file.ts`.

```
component = "<your-project>:modules/path/to/file.ts"
relative  = component.split(':')[1]           // "modules/path/to/file.ts"
absolute  = "<workspace-root>/" + relative    // "/path/to/project/modules/..."
```


## RED/GREEN Matching Algorithm

Cross-reference server issues with local findings to determine fix status.

### Issue States

| State | Meaning |
|-------|---------|
| 🔴 RED | Issue on server AND still found locally — not fixed yet |
| 🟢 GREEN | Issue on server but NOT found locally — fix works, push it |
| 🆕 NEW | Found locally, NOT on server, AND in code you changed — newly introduced |
| 📋 PRE-EXISTING | Found locally, NOT on server, but in code you did NOT change — existed before your work |

### Why PRE-EXISTING exists

The server (in PR mode) only analyzes **changed lines** — it intentionally ignores pre-existing issues outside the diff.
The IDE's local analyzer (`analyze_file_list`) scans the **entire file**, including untouched code.
Without the git-diff check, every pre-existing issue in an unchanged line would be mislabeled as 🆕 NEW — confusing users into thinking they introduced it.

### Algorithm

```
Step 1 — Get changed line ranges:
  git diff <base-branch>...HEAD --unified=0 -- <file>
  Parse hunk headers (@@ -a,b +c,d @@) to build a set of changed line ranges per file.

Step 2 — Match server issues to local findings:
  For each server_issue in search_sonar_issues_in_projects:
    server_file = server_issue.component.split(':')[1]
    server_line = server_issue.textRange.startLine

    For each local_finding in analyze_file_list(absolute_path):
      same_file   = local_finding.filePath ends with server_file
      line_near   = abs(local_finding.textRange.startLine - server_line) <= 5
      msg_overlap = normalize(local_finding.message) contains normalize(server_issue.message)
                    OR vice versa

      If same_file AND line_near AND msg_overlap → MATCH (🔴 RED)

    If no match found → 🟢 GREEN (fixed locally)

Step 3 — Classify unmatched local findings:
  For each local finding with no server match:
    If finding.startLine falls within a changed hunk → 🆕 NEW
    Else → 📋 PRE-EXISTING
```

**Message normalization:** lowercase, strip backticks, strip trailing punctuation.
**Line tolerance ±5** accounts for local edits shifting line numbers relative to the last scan.


## Token-Safe Collection Workflow

All issue-fetching MCP calls must run in subagents, regardless of result set size.
Even 10 issues produce ~120 tokens of JSON each — this adds up fast.

```
Step 1 — Collect (subagent, write to disk):
  For p in range(1, ceil(total/50) + 1):
    page = search_sonar_issues_in_projects(ps=50, p=p)
    append page.issues to .agents.tmp/code-quality/verify/issues.jsonl

Step 2 — Extract unique files (shell):
  jq -r '.component' .agents.tmp/code-quality/verify/issues.jsonl | sort -u
    → .agents.tmp/code-quality/verify/unique-files.txt

Step 3 — Local analysis (subagent, per-file):
  For each file in unique-files.txt:
    findings = analyze_file_list([absolute_path])
    append findings to .agents.tmp/code-quality/verify/local-findings.jsonl

Step 4 — Cross-reference (subagent):
  Match issues.jsonl × local-findings.jsonl using algorithm above
    → .agents.tmp/code-quality/verify/red-green-report.md
```

**Never read the full JSONL into conversation context — always process with `jq` in subagents.**


## Subagent Return Contract

When a subagent collects issues or findings, it returns ONLY:

- Total count
- Severity breakdown (e.g., "3 CRITICAL, 12 MAJOR, 35 MINOR")
- Unique file count
- File path to the JSONL on disk
- Pre-formatted markdown table (if the skill needs to show results to the user)

The subagent NEVER returns raw JSON issue objects to the parent context.


## Quick Call Examples

Copy-paste ready tool calls for common operations.
Replace `<your-project>` with your actual project key.

```
// Check quality gate on main
get_project_quality_gate_status { projectKey: "<your-project>", branch: "main" }

// Check quality gate on a PR
get_project_quality_gate_status { projectKey: "<your-project>", pullRequest: "123" }

// Fetch issues — safe page size
search_sonar_issues_in_projects {
  projects: ["<your-project>"],
  issueStatuses: ["OPEN"],
  p: 1,
  ps: 50
}

// Fetch issues on a specific PR
search_sonar_issues_in_projects {
  projects: ["<your-project>"],
  pullRequestId: "123",
  issueStatuses: ["OPEN"],
  ps: 50
}

// Analyze local files (requires IDE-connected mode)
analyze_file_list {
  file_absolute_paths: ["/absolute/path/to/your-file.ts"]
}

// Look up a rule
show_rule { key: "typescript:S3358" }

// Fetch dashboard metrics
get_component_measures {
  component: "<your-project>",
  metricKeys: ["coverage", "code_smells", "bugs", "vulnerabilities", "ncloc"],
  branch: "main"
}

// Mark a false positive
change_sonar_issue_status { key: "<issue-uuid>", status: "falsepositive" }
```
