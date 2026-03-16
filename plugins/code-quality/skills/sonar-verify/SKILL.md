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

### Step 1: Collect server issues (subagent)

Delegate issue collection to a subagent:

1. Subagent calls `search_sonar_issues_in_projects` with `ps=50`, paginating all pages.
   **Never pass `severities`** — it crashes the MCP server.
2. Subagent writes issues to `.agents.tmp/code-quality/verify/server-issues.jsonl` (one JSON object per line).
3. Subagent extracts unique files: `jq -r '.component' | sort -u` → `.agents.tmp/code-quality/verify/unique-files.txt`.
4. Subagent converts `component` fields to absolute paths using the workspace root:
   `component.split(':')[1]` → relative path → workspace root + relative path → absolute path.
5. Subagent returns **ONLY** a summary: total count, severity breakdown, unique file count.

The main context NEVER sees the raw issue JSON.

### Step 2: Analyze locally (subagent)

Delegate local analysis to a subagent:

1. Subagent reads `unique-files.txt`.
2. Subagent calls `analyze_file_list` for each file.
3. Subagent writes findings to `.agents.tmp/code-quality/verify/local-findings.jsonl` (one JSON object per line).
4. Subagent returns **ONLY**: finding count, files with findings.

### Step 3: Cross-reference (subagent)

Delegate cross-referencing to a subagent:

1. Subagent reads both JSONL files (`server-issues.jsonl` and `local-findings.jsonl`).
2. Subagent applies the matching algorithm from `references/sonarqube-mcp-tools.md`:

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

3. Subagent writes the full report to `.agents.tmp/code-quality/verify/report.md`.
4. Subagent returns the report content — this IS the final output shown to the user.

### Step 4: Present report

Format as a table grouped by status — GREEN first (wins), then RED (still broken), then NEW (watch out):

```
RED/GREEN Verification Report

| Status | Rule   | File                     | Line | Message                        |
|--------|--------|--------------------------|------|--------------------------------|
| 🟢     | S3358  | services/auth.service.ts | 62   | Ternary operators not nested   |
| 🟢     | S3863  | utils/helpers.ts         | 4    | Imported multiple times         |
| 🔴     | S2004  | components/dashboard.ts  | 42   | Refactor to reduce nesting     |
| 🆕     | —      | models/user.ts           | 15   | Unused import detected          |

Rule column shows the server rule key for RED/GREEN rows.
NEW rows have no rule — local findings lack this field.

Summary: 2 fixed (🟢), 1 remaining (🔴), 1 new (🆕)
```

## Bug Guardrails

- **Never pass `severities`** when fetching server issues.
- Local findings have no `rule` field — match by message text.
- Line tolerance ±5 accounts for local edits shifting lines.
- Always use subagents for issue collection and local analysis — the main context must never see raw MCP JSON.
  See `references/sonarqube-mcp-tools.md` for the subagent return contract.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Match by exact line number | Use ±5 tolerance — local edits shift lines |
| Expect `rule` field in local findings | Match by message text — local findings have no rule key |
| Load issues into main context | Always delegate to subagents — write to disk, return summaries only |
| Run without IDE-connected mode | Check if `analyze_file_list` is available first — stop if not |
| Show RED issues first | Show GREEN first — the user wants to see their wins |
