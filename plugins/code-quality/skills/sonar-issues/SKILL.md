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

### Step 2: Fetch first page

Call `search_sonar_issues_in_projects` with safe parameters:

```
search_sonar_issues_in_projects {
  projects: ["<your-project>"],
  issueStatuses: ["OPEN"],
  p: 1,
  ps: 50
}
```

For PR-specific issues, add `pullRequestId: "123"`.

**CRITICAL: Never pass the `severities` parameter.**
It crashes the MCP server due to a type-cast bug (string → List).
Filter by severity client-side after fetching.

### Step 3: Present issues

Format as a table grouped by severity (CRITICAL → MAJOR → MINOR → INFO):

```
Found 238 open issues (showing page 1 of 5)

| Severity | Rule   | File                    | Line | Message                           |
|----------|--------|-------------------------|------|-----------------------------------|
| CRITICAL | S2004  | containers/details.ts   | 42   | Refactor to reduce deep nesting   |
| MAJOR    | S3358  | store/site.store.ts     | 62   | Ternary operators not nested      |
| MINOR    | S3863  | tabs/details-tab.ts     | 4    | Imported multiple times            |
```

Use short file paths — strip the project prefix from `component.split(':')[1]` and show only the last 2-3 path segments.

### Step 4: Offer pagination

If `total > 50`, tell the user how many pages remain and offer to fetch the next page:

```
Showing 50 of 238 issues (page 1 of 5). Want me to fetch the next page?
```

### Step 5: Large result sets

If `total > 100`, write results to `.agents.tmp/sonar-issues/` as JSONL and use `jq` for queries:

```bash
jq -r 'select(.severity == "CRITICAL") | [.rule, .component, .textRange.startLine, .message] | @tsv' \
  .agents.tmp/sonar-issues/issues.jsonl
```

Never read full JSONL files into the conversation context.

## Bug Guardrails

- **Never pass `severities`** — crashes the MCP server (string → List type cast failure).
- **Use `ps=50` max** — `ps=500` exceeds the transport limit (~122K chars).
- Severity counts from this tool may not match the dashboard due to Clean Code taxonomy multi-impact double-counting.
  See `references/sonarqube-mcp-guide.md` for explanation.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Pass `severities` param to `search_sonar_issues_in_projects` | Filter by severity client-side after fetching |
| Use `ps` greater than 50 | Paginate with `ps=50` — 5 pages for ~250 issues |
| Read full JSONL into conversation context | Use `jq` in subagents for large result sets |
| Show full component paths | Show short paths — last 2-3 segments only |
