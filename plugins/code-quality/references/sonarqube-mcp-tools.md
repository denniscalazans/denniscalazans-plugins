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

#### `projects` (always on)

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_my_sonarqube_projects` | `q`, `page`, `pageSize` | Search projects by name fragment |
| `list_pull_requests` | `projectKey` | List all PRs for a project |

#### `analysis`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `analyze_file_list` | `file_absolute_paths[]` | Local analysis via SonarQube for IDE — requires `SONARQUBE_IDE_PORT` |
| `toggle_automatic_analysis` | `enabled` (bool) | Enable/disable auto-analysis as files change |

#### `issues`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_sonar_issues_in_projects` | `projects[]`, `pullRequestId`, `issueStatuses[]`, `impactSoftwareQualities[]`, `p`, `ps` | **Never pass `severities`** — crashes the MCP server. Use `ps=50` max. |
| `change_sonar_issue_status` | `key`, `status` (`accept` / `falsepositive` / `reopen`) | Triage server issues |

#### `quality-gates`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_project_quality_gate_status` | `projectKey`, `branch`, `pullRequest` | Returns OK/ERROR + condition details |
| `list_quality_gates` | — | List all available quality gates |

#### `rules`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `show_rule` | `key` (e.g., `typescript:S3358`) | Full rule detail with noncompliant/compliant examples |

#### `measures`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_component_measures` | `component`, `metricKeys[]`, `branch`, `pullRequest` | Dashboard metrics — always matches the web UI |
| `search_metrics` | `p`, `ps` | List all available metric keys |

#### `duplications`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_duplications` | `key` (file key), `pullRequest` | Duplication blocks for a specific file |
| `search_duplicated_files` | `projectKey`, `pageIndex`, `pageSize`, `pullRequest` | Project-wide duplication report |

#### `security-hotspots`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_security_hotspots` | `projectKey`, `status[]`, `resolution[]`, `pullRequest`, `ps` | Filter by `TO_REVIEW` / `REVIEWED` |
| `show_security_hotspot` | `hotspotKey` | Rule details, code context, flows, comments |
| `change_security_hotspot_status` | `hotspotKey`, `status`, `resolution` (`FIXED`/`SAFE`/`ACKNOWLEDGED`), `comment` | Review hotspots |

#### `coverage` (default since MCP 1.10)

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `search_files_by_coverage` | `projectKey`, `maxCoverage`, `pageSize`, `pullRequest` | Sorted worst-first |
| `get_file_coverage_details` | `key` (file key), `pullRequest` | Line-by-line coverage detail |

### Optional Toolsets (must add to `SONARQUBE_TOOLSETS`)

#### `sources`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `get_raw_source` | `key` (file key), `pullRequest` | File source as SonarQube indexed it |
| `get_scm_info` | `key`, `from`, `to`, `commits_by_line` | Per-line datetime (author/revision may be empty) |

#### `languages`

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `list_languages` | `q` (optional filter) | All languages the instance can analyze |


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
{ "pageIndex": 1, "pageSize": 50, "total": 238 }
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
| 🆕 NEW | Found locally but NOT on server — newly introduced |

### Algorithm

```
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

Remaining local findings with no server match → 🆕 NEW
```

**Message normalization:** lowercase, strip backticks, strip trailing punctuation.
**Line tolerance ±5** accounts for local edits shifting line numbers relative to the last scan.


## Token-Safe Collection Workflow

For projects with > 100 issues, use this 4-step process to stay within token budget.

```
Step 1 — Collect (subagent, write to disk):
  For p in range(1, ceil(total/50) + 1):
    page = search_sonar_issues_in_projects(ps=50, p=p)
    append page.issues to .agents.tmp/code-quality/verify/issues.jsonl

Step 2 — Extract unique files (shell):
  jq -r '.component' .agents.tmp/code-quality/verify/issues.jsonl | sort -u
    → .agents.tmp/code-quality/verify/unique-files.txt

Step 3 — Local analysis (per-file):
  For each file in unique-files.txt:
    findings = analyze_file_list([absolute_path])
    append findings to .agents.tmp/code-quality/verify/local-findings.jsonl

Step 4 — Cross-reference (shell + jq):
  Match issues.jsonl × local-findings.jsonl using algorithm above
    → .agents.tmp/code-quality/verify/red-green-report.md
```

**Never read the full JSONL into conversation context — always process with `jq` in subagents.**


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
