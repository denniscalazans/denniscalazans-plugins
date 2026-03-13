---
name: sonar-verify
description: >
  Use when the user wants to verify which SonarQube issues are fixed locally before pushing.
  Also use when cross-referencing server issues with local analysis results (RED/GREEN validation).
  Triggers: "verify fixes", "red green", "which issues did I fix", "sonar verify", "check local fixes", "pre-push check", "validate fixes".
---

# Sonar Verify

RED/GREEN validation — cross-reference server issues with local analysis to see which are fixed before pushing.

**Announce at start:** "Running RED/GREEN verification."

## Prerequisite Check

This skill requires IDE-connected mode (`analyze_file_list` available via `SONARQUBE_IDE_PORT`).
If unavailable, inform the user and stop: "RED/GREEN verification requires IDE-connected mode with SonarQube for IDE running. See `references/sonarqube-mcp-guide.md` for setup."

## Issue States

| State | Meaning |
|-------|---------|
| 🔴 RED | Issue on server AND still found locally — not fixed yet |
| 🟢 GREEN | Issue on server but NOT found locally — fix works, push it |
| 🆕 NEW | Found locally but NOT on server — newly introduced |

## Process

### Step 1: Collect server issues

Fetch issues with `search_sonar_issues_in_projects`:

```
search_sonar_issues_in_projects {
  projects: ["<your-project>"],
  issueStatuses: ["OPEN"],
  p: 1,
  ps: 50
}
```

**Never pass `severities`** — it crashes the MCP server.

If `total > 50`, paginate and write each page to `.agents.tmp/sonar-verify/server-issues.jsonl`.
For small result sets (≤ 50), keep in context.

### Step 2: Extract unique files

Get unique file paths from server issues.
Convert `component` field to absolute paths using the workspace root:

```
component.split(':')[1] → relative path
workspace root + relative path → absolute path
```

### Step 3: Analyze locally

Call `analyze_file_list` for each unique file:

```
analyze_file_list { file_absolute_paths: ["/absolute/path/to/file.ts"] }
```

Collect all findings.

### Step 4: Cross-reference

Apply the matching algorithm from `references/sonarqube-mcp-tools.md`:

```
same_file   = local_finding.filePath ends with server_issue.component.split(':')[1]
line_near   = abs(local_finding.textRange.startLine - server_issue.textRange.startLine) <= 5
msg_overlap = normalize(local_finding.message) contains normalize(server_issue.message)
              OR vice versa
```

**Message normalization:** lowercase, strip backticks, strip trailing punctuation.

- If all three match → 🔴 RED (still broken)
- Server issue with no local match → 🟢 GREEN (fixed locally)
- Local finding with no server match → 🆕 NEW (newly introduced)

### Step 5: Present report

Format as a table grouped by status — GREEN first (wins), then RED (still broken), then NEW (watch out):

```
RED/GREEN Verification Report

| Status | Rule   | File                  | Line | Message                        |
|--------|--------|-----------------------|------|--------------------------------|
| 🟢     | S3358  | store/site.store.ts   | 62   | Ternary operators not nested   |
| 🟢     | S3863  | tabs/details-tab.ts   | 4    | Imported multiple times         |
| 🔴     | S2004  | containers/details.ts | 42   | Refactor to reduce nesting     |
| 🆕     | —      | utils/helpers.ts      | 15   | Unused import detected          |

Summary: 2 fixed (🟢), 1 remaining (🔴), 1 new (🆕)
```

## Bug Guardrails

- **Never pass `severities`** when fetching server issues.
- Local findings have no `rule` field — match by message text.
- Line tolerance ±5 accounts for local edits shifting lines.
- For large projects (> 100 issues), use subagents and `.agents.tmp/` to stay within token budget.
  See `references/sonarqube-mcp-tools.md` for the full token-safe collection workflow.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Match by exact line number | Use ±5 tolerance — local edits shift lines |
| Expect `rule` field in local findings | Match by message text — local findings have no rule key |
| Load all issues into context | Paginate and write to disk for large result sets |
| Run without IDE-connected mode | Check if `analyze_file_list` is available first — stop if not |
| Show RED issues first | Show GREEN first — the user wants to see their wins |
