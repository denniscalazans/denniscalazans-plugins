---
name: sonar-issues
description: >
  Use when browsing, searching, or listing SonarQube issues for a project or PR.
  Also use when the user asks "what issues are there?", "show me the code smells", or wants to see issues by severity.
  Triggers: "sonar issues", "code smells", "show issues", "list issues", "what issues", "browse issues", "sonar findings".
---

# Sonar Issues

Browse SonarQube issues with safe pagination and severity filtering.

**Announce at start:** "Fetching SonarQube issues."

## Process

### Step 1: Identify target

Determine the project key, branch or PR, and any optional filters (severity, file path, rule).
If the project key is not in context, ask the user.

### Step 2: Fetch issues (subagent)

Delegate issue fetching to a subagent:

1. Subagent calls `search_sonar_issues_in_projects` with `ps=50`, `p=1`.
   For PR-specific issues, adds `pullRequestId: "123"`.
   To filter by severity, pass `severities: ["CRITICAL"]` (legacy values: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`).
2. Subagent writes issues to `.agents.tmp/code-quality/issues/page-1.jsonl` (one JSON object per line).
3. Subagent formats a markdown table grouped by severity (CRITICAL → MAJOR → MINOR → INFO):
   - Columns: Severity, Rule, File (short path — last 2-3 segments), Line, Message.
   - Strip the project prefix from `component.split(':')[1]`.
4. Subagent returns **ONLY**: the formatted table + paging metadata (total, pages remaining).

The main context receives the pre-formatted table, not raw JSON.

### Step 3: Present issues

Show the table returned by the subagent:

```
Found 238 open issues (showing page 1 of 5)

| Severity | Rule   | File                    | Line | Message                           |
|----------|--------|-------------------------|------|-----------------------------------|
| CRITICAL | S2004  | components/dashboard.ts | 42   | Refactor to reduce deep nesting   |
| MAJOR    | S3358  | services/auth.service.ts| 62   | Ternary operators not nested      |
| MINOR    | S3863  | utils/helpers.ts        | 4    | Imported multiple times            |
```

### Step 4: Offer pagination

If `total > 50`, tell the user how many pages remain and offer to fetch the next page.
Each additional page follows the same subagent pattern — fetch, write to disk, return formatted table.

```
Showing 50 of 238 issues (page 1 of 5). Want me to fetch the next page?
```

## Bug Guardrails

- **Use `ps=50` max** — `ps=500` exceeds the transport limit (~122K chars).
- Severity counts from this tool may not match the dashboard due to Clean Code taxonomy multi-impact double-counting.
  See `references/sonarqube-mcp-guide.md` for explanation.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Use `ps` greater than 50 | Paginate with `ps=50` — 5 pages for ~250 issues |
| Fetch issues inline in main context | Always delegate to subagents — write to disk, return formatted tables only |
| Show full component paths | Show short paths — last 2-3 segments only |
