---
name: sonar-status
description: >
  Use when checking code quality health, quality gate status, or dashboard metrics for a project or PR.
  Also use when the user asks "did my PR pass?", "how's code quality?", or wants a quick health check.
  Triggers: "quality gate", "sonar status", "code quality", "dashboard metrics", "did my PR pass", "quality check", "sonar health".
---

# Sonar Status

Check quality gate and key metrics without opening the web UI.

**Announce at start:** "Checking code quality status."

## Process

### Step 1: Identify target

Determine the project key, branch, or PR number.
If the project key is not in context (e.g., from a `sonar-project.properties` file or previous conversation), ask the user.

Use `branch` for feature branches, `pullRequest` for PR numbers.
If neither is specified, default to the main branch.

### Step 2: Check quality gate

Call `get_project_quality_gate_status` with the appropriate target:

```
get_project_quality_gate_status { projectKey: "<your-project>", branch: "main" }
```

Or for a PR:

```
get_project_quality_gate_status { projectKey: "<your-project>", pullRequest: "123" }
```

The response includes `status` (OK or ERROR) and an array of `conditions` with their thresholds and actual values.

### Step 3: Fetch metrics

Call `get_component_measures` for the dashboard numbers:

```
get_component_measures {
  component: "<your-project>",
  metricKeys: ["coverage", "bugs", "vulnerabilities", "code_smells", "duplicated_lines_density", "ncloc", "security_hotspots"],
  branch: "main"
}
```

Pass `pullRequest` instead of `branch` for PR-specific metrics.

### Step 4: Present summary

Format the results as a readable table matching the web UI layout:

```
Quality Gate: ✅ OK (or ❌ FAILED)

| Metric              | Value  |
|---------------------|--------|
| Coverage            | 62.7%  |
| Bugs                | 0      |
| Vulnerabilities     | 0      |
| Code Smells         | 238    |
| Duplications        | 2.0%   |
| Security Hotspots   | 0      |
| Lines of Code       | 17,482 |
```

If any quality gate condition failed, highlight it and show the threshold vs actual value.

## Bug Guardrails

- **Use `get_component_measures` for accurate counts** — `search_sonar_issues_in_projects` severity counts may not match the dashboard due to Clean Code taxonomy double-counting.
  See `references/sonarqube-mcp-guide.md` for taxonomy details if the user asks about number discrepancies.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Use `search_sonar_issues_in_projects` for issue counts | Use `get_component_measures` — always matches the web UI |
| Forget the `branch` or `pullRequest` param | Always specify the target — omitting it queries the default branch |
| Show raw JSON to the user | Format as a readable table matching the web UI layout |
