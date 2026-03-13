---
name: sonar-triage
description: >
  Use when the user wants to mark a SonarQube issue as false positive, accept it, or reopen a previously triaged issue.
  Also use when the user says "this is a false positive", "accept this issue", or "triage sonar findings".
  Triggers: "false positive", "triage", "accept issue", "sonar triage", "mark as false positive", "reopen issue", "not a real issue".
  Not for: fixing issues (use sonar-fix), browsing issues (use sonar-issues).
---

# Sonar Triage

Mark SonarQube issues as false positive, accepted, or reopen previously triaged issues.

**Announce at start:** "Triaging SonarQube issue."

## Process

### Step 1: Get the issue key

The `key` field (UUID) is required for triage operations.

Get it from:
- Previous `sonar-issues` output (the `key` field on each issue)
- Search with `search_sonar_issues_in_projects` by file + message

**Important:** `analyze_file_list` (local) findings do NOT have issue keys.
If the user has only a local finding, search for the matching server issue first using file path and message text.

### Step 2: Confirm action

Ask the user which status to set:

| Status | Meaning | When to use |
|--------|---------|-------------|
| `falsepositive` | This is not a real issue | Code is correct but the rule doesn't understand the context |
| `accept` | This is a real issue but we accept the risk | Known tech debt, intentional trade-off |
| `reopen` | Re-open a previously triaged issue | Conditions changed, issue is real again |

Before triaging, suggest looking up the rule first (`show_rule`) to make an informed decision.

### Step 3: Execute

Call `change_sonar_issue_status` with the issue key and chosen status:

```
change_sonar_issue_status { key: "<issue-uuid>", status: "falsepositive" }
```

### Step 4: Confirm

Report the result.
The issue will no longer appear in open issue counts on the dashboard.

## Security Hotspots

Security hotspots use a different tool with different parameters:

```
change_security_hotspot_status {
  hotspotKey: "<hotspot-uuid>",
  status: "REVIEWED",
  resolution: "SAFE",
  comment: "Reviewed — safe because..."
}
```

Resolution options: `FIXED`, `SAFE`, `ACKNOWLEDGED`.
Do not use `change_sonar_issue_status` for security hotspots — it will fail.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Try to triage from local findings directly | Find the server issue key first via `search_sonar_issues_in_projects` |
| Triage without understanding the issue | Show the rule explanation first — suggest `sonar-rule` |
| Use `change_sonar_issue_status` for security hotspots | Use `change_security_hotspot_status` with `resolution` param |
| Triage without user confirmation | Always ask which status before executing — triage is a server mutation |
