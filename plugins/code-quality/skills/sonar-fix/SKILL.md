---
name: sonar-fix
description: >
  Use when the user wants to fix a SonarQube issue, resolve a code smell, or address a flagged violation.
  Also use when the user says "fix this issue", "resolve the ternary", or "clean up sonar findings".
  Triggers: "fix sonar", "fix issue", "resolve code smell", "fix violation", "sonar fix", "clean up issue", "address finding".
  Not for: triaging false positives (use sonar-triage), browsing issues without fixing (use sonar-issues).
---

# Sonar Fix

Guided workflow to fix a SonarQube issue — understand the rule, see the code, edit, verify locally.

**Announce at start:** "Starting SonarQube fix workflow."

## Process

### Step 1: Identify the issue and check capabilities

Get the issue from context:
- Previous `sonar-issues` output (has rule, file, line, message)
- User-provided rule/file/line
- PR findings from `search_sonar_issues_in_projects`

Also check whether `analyze_file_list` is available (IDE-connected mode).
If not, inform the user upfront: "Fixes will be applied but can only be verified after pushing — local verification requires IDE-connected mode."

### Step 2: Understand the rule

Call `show_rule` to get the full explanation with compliant/noncompliant examples:

```
show_rule { key: "<rule-key>" }
```

Present the key insight: what's wrong and what compliant code looks like.
This step is essential — never fix blindly without understanding the rule.

### Step 3: Read the code

Read the flagged file at the issue's line range.
Convert the `component` field to a relative path:

```
component.split(':')[1] → relative path
```

Show the relevant code context (±10 lines around the flagged line).

### Step 4: Apply the fix

Edit the code following the compliant pattern from the rule.
Keep changes minimal — fix only what the rule requires.
Do not refactor surrounding code or make unrelated improvements.

### Step 5: Verify locally

If IDE-connected mode is available (`analyze_file_list`):

```
analyze_file_list { file_absolute_paths: ["/absolute/path/to/fixed-file.ts"] }
```

Check two things:
1. The original issue is gone (match by file + line(±5) + message)
2. No new issues were introduced

If IDE mode is unavailable, skip verification and tell the user: "Fix applied. Push to trigger server-side validation."

### Step 6: Report

Show what changed:
- The specific edit made
- Whether the issue is verified resolved (local) or pending server verification
- Any new findings introduced (if verification ran)

If the user is fixing multiple issues in a batch, suggest running `sonar-verify` afterwards for a comprehensive RED/GREEN cross-reference.

## Bug Guardrails

- When verifying, `analyze_file_list` returns only 4 fields (no `rule` key).
  Match by file + line(±5) + message text.
- See `references/sonarqube-mcp-tools.md` for the full matching algorithm.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Fix without understanding the rule first | Call `show_rule` before editing — understand the compliant pattern |
| Make unnecessary changes beyond the flagged issue | Keep edits minimal — fix only what the rule requires |
| Assume `analyze_file_list` returns rule keys | Match by file + line(±5) + message text |
| Skip verification when IDE mode is available | Always verify locally if `analyze_file_list` is available |
| Fix and forget | Report verification results — confirmed resolved or pending server check |
