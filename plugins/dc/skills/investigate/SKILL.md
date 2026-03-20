---
name: investigate
description: >
  Use when the user has a clear goal but implementation hasn't started yet.
  Also use when Claude needs to understand existing codebase patterns, conventions,
  and constraints before proposing changes.
  Produces a "TODAY IS / EXPECTED IS" investigation report, then stops.
  Does NOT write code or propose implementations.
  Triggers: "investigate first", "explore the codebase", "what exists",
  "map the patterns", "today is expected is", "before we implement",
  "what are the conventions", "understand before changing".
---

# Investigate — Codebase-First Discovery

Explore the codebase systematically to understand what exists before proposing any changes.
Produce a "TODAY IS / EXPECTED IS" investigation report grounded in file-path evidence, then stop.

**Do not write code, propose implementations, or suggest solutions.**
The report maps the terrain so that the next step (planning, grilling, or implementing) starts from reality, not assumptions.


## Core Principle: File Paths or Nothing

Every finding must reference at least one concrete file path.
"The project uses Redux" is not a finding.
"`src/store/index.ts:14` initializes a Redux Toolkit store with `configureStore`" is a finding.

If a claim cannot be backed by a file path, it does not belong in the report.


## PHASE 1 — SCOPE CLASSIFICATION (silent)

Before exploring, classify the change scope internally.
This determines investigation depth.

| Scope | Signal | Investigation depth |
|-------|--------|-------------------|
| **PATCH** | Typo, config tweak, single-line fix | Target area + conventions only (sections 1, 5) |
| **FEATURE** | New capability within one module/domain | Standard — all 6 exploration steps |
| **CROSS-CUT** | Touches multiple modules, shared abstractions, or public APIs | Full — all steps + blast radius in dependencies section |
| **MIGRATION** | Framework upgrade, data model change, pattern replacement | Full — all steps + before/after comparison of affected areas |

If scope is PATCH, skip to Phase 3 with a minimal report.
For all other scopes, proceed to Phase 2.


## PHASE 2 — SYSTEMATIC EXPLORATION

Work through these steps silently.
Do not narrate the exploration — only surface findings in the report.


### Step 1: Find the target area

Locate the files, modules, or components directly affected by the goal.

- Search by filename patterns, class names, route definitions, or domain keywords
- Read the entry points — understand how the target area is reached
- Note the directory structure and module boundaries


### Step 2: Find similar features

Search for existing implementations that solve a similar problem.

- Look for analogous patterns the codebase already uses
- Check if the feature was partially implemented, abandoned, or exists under a different name
- Note which approach the codebase favors when multiple patterns could apply

This step prevents reinventing what already exists and ensures new code follows established patterns.


### Step 3: Map dependencies

Trace what the target area depends on and what depends on it.

- Imports and exports — what does the target area consume and expose?
- Shared state — databases, stores, caches, event buses
- API contracts — does changing this area affect external consumers?
- For CROSS-CUT and MIGRATION scopes: map the full blast radius across modules


### Step 4: Check tests

Examine the testing landscape around the target area.

- Existing test files — what is already tested?
- Test patterns — unit, integration, e2e? Which framework and conventions?
- Coverage gaps — what is NOT tested that relates to the goal?
- Test utilities — shared fixtures, factories, or helpers that should be reused


### Step 5: Identify conventions

Extract the patterns and conventions the codebase enforces in this area.

- Naming conventions (files, classes, functions, variables)
- Error handling patterns
- Logging and observability patterns
- Code organization (barrel exports, co-located tests, feature folders)
- Linting rules or custom ESLint/Checkstyle configs that affect this area


### Step 6: Check for blockers

Look for anything that could prevent or complicate the change.

- TODO/FIXME/HACK comments in the target area
- Known tech debt or workarounds
- Version constraints or deprecated dependencies
- Feature flags or environment-specific behavior
- Recent changes to the area (check git log for the target files)


## PHASE 3 — PRODUCE REPORT

Present findings using the format below.
Omit empty sections — if a step produced no relevant findings, skip it.
Show the scope classification in the header so the user can correct it if wrong.

```
## Investigation Report

**Goal:** [1 sentence restating the user's objective]
**Scope:** [PATCH | FEATURE | CROSS-CUT | MIGRATION]

### TODAY IS

[Current state of the target area, grounded in file paths.
Every paragraph references specific files and line numbers.
Describe what exists, how it works, and what patterns it follows.]

### EXPECTED IS

[What needs to change to achieve the goal.
Describe the delta between today and the goal — NOT how to implement it.
"The payment module needs a webhook handler" not "Create a new file at src/payments/webhook.ts".]

### Similar features found

[Existing implementations that solve analogous problems.
Reference file paths and explain what pattern they follow.
If nothing similar exists, state that explicitly.]

### Dependencies and blast radius

[What the target area connects to.
Imports, consumers, shared state, API contracts.
For CROSS-CUT/MIGRATION: list every module affected.]

### Test landscape

[Existing tests, patterns, coverage gaps, shared utilities.
Reference test file paths.]

### Conventions to follow

[Patterns extracted from the codebase that new code must match.
Reference the files where each convention is demonstrated.]

### Blockers and risks

[TODOs, tech debt, version constraints, recent churn, feature flags.
Reference file paths and git history where relevant.]
```

For PATCH scope, produce only:

```
## Investigation Report

**Goal:** [1 sentence]
**Scope:** PATCH

### TODAY IS

[Target area with file paths]

### EXPECTED IS

[What needs to change]

### Conventions to follow

[Relevant patterns to match]
```


## PHASE 4 — HARD STOP

After presenting the report, STOP.

Do not:
- Write any code
- Propose an implementation plan
- Suggest file names or directory structures for new code
- Offer to "get started" on the implementation
- Continue with any next step unless the user explicitly asks

End the report with:

```
---
Investigation complete.
This report is ready for implementation or for stress-testing with /dc:grill.
```

If the user says "now implement" or "go ahead", proceed with implementation using the report as context.
If the user says nothing about next steps, do nothing.
The default after investigation is silence, not action.


## Scope

This skill applies to any codebase, any language, any framework.
It is not limited to code — configuration, infrastructure-as-code, CI/CD pipelines, and database schemas are all valid investigation targets.
If the goal involves changing something that already exists, this skill maps the terrain first.


## Honesty Rules

- If exploration hits a dead end, say so: "I searched for [X] using [patterns] but found nothing. This area may not exist yet, or it may use a name I didn't anticipate."
- If the codebase is too large to explore fully, state what was covered and what was not: "I explored `src/payments/` and `src/shared/` but did not search `src/legacy/` — that module may contain relevant patterns."
- If findings contradict the user's assumptions, surface the contradiction directly: "Your goal assumes [X], but the codebase shows [Y] at `path/to/file:line`."
- Never fabricate findings. An honest "I found nothing" is more valuable than a plausible-sounding guess.


## Common Mistakes

| Don't | Do |
|-------|-----|
| Start writing code after exploring | Stop at the report — Phase 4 is a hard stop |
| Report findings without file paths | Every finding references at least one file path |
| Describe how to implement the change | Describe what needs to change (the delta), not how |
| Skip searching for similar features | Always check if the pattern already exists in the codebase |
| Narrate the exploration process | Work silently, present only findings in the report |
| Produce a full report for a typo fix | Classify scope first — PATCH gets a minimal report |
| Assume the user wants you to continue | The default after the report is silence, not action |
| List conventions without file references | Show where each convention is demonstrated in code |
| Explore only the obvious target files | Check dependencies, consumers, and adjacent modules too |
| Ignore git history of the target area | Recent changes reveal active work, tech debt, and churn |
| Guess at findings when exploration is inconclusive | State what was searched, what was found, and what was not covered |
