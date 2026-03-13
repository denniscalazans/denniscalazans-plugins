---
name: sonar-rule
description: >
  Use when the user asks about a SonarQube rule, wants to understand why code was flagged, or needs compliant/noncompliant examples.
  Also use when seeing rule IDs like "S3358" or "typescript:S1135".
  Triggers: "explain rule", "what is S3358", "sonar rule", "why was this flagged", "show rule", "rule details", "noncompliant example".
---

# Sonar Rule

Look up any SonarQube rule and get the full explanation with code examples.

**Announce at start:** "Looking up SonarQube rule."

## Process

### Step 1: Identify rule key

Accept any of these formats:
- Full key: `typescript:S3358`
- Short number: `S3358`
- From issue context: extract the `rule` field from a previous `search_sonar_issues_in_projects` result

If only the number is given (e.g., `S3358`), determine the language prefix from context:
- Check the file extension of the flagged file (`.ts` → `typescript`, `.java` → `java`, `.py` → `python`)
- If no file context, ask the user which language

### Step 2: Fetch rule

Call `show_rule` with the full key:

```
show_rule { key: "typescript:S3358" }
```

The response includes the rule name, description, severity, tags, and code examples.

### Step 3: Present

Show the key information concisely — the rule response can be verbose:

1. **Rule name** — what the rule checks
2. **Why it matters** — the rationale behind the rule
3. **Noncompliant example** — code that triggers the violation
4. **Compliant example** — how to fix it
5. **Clean Code attribute** — e.g., CLEAR (Intentional), FOCUSED (Adaptable)

Keep the presentation focused — don't dump the entire raw response.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Show the entire raw rule response | Extract key sections: why, noncompliant, compliant |
| Guess the language prefix blindly | Check the file extension or ask the user |
| Skip the compliant example | Always show both noncompliant and compliant code |
