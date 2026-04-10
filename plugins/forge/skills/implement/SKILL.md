---
name: implement
description: >
  Use when implementing features, fixes, or infrastructure changes that modify code.
  Use when the user wants adversarial quality checking before committing.
  Do not use for trivial single-file changes like typos or comment edits.
  Triggers: "implement", "forge implement", "implement this ticket",
  "build this feature", "start implementing", "implement feature",
  "adversarial pipeline", "build with forge".
---

# /forge:implement — Adversarial Implementation Pipeline

Orchestrates 5 agents in a pipeline with dynamic routing:
**Investigator → Challenger → Planner → Generator ↔ Evaluator**

The Generator tries to produce code that passes.
The Evaluator tries to find real violations.
The loop continues until the Evaluator returns PASS or 3 iterations are reached.


## When to Use

- Implementing features, fixes, or infrastructure changes
- Any task that modifies code and should meet project conventions
- When you want adversarial quality checking before committing

**Skip this pipeline for trivial tasks** (editing a single rule file, fixing a typo, updating a comment).
Multi-agent overhead only pays off on tasks with real complexity.
Use judgment: if the task touches 1 file with an obvious change, just do it directly.


## Audit Trail

Each invocation writes a feedback file at `.agents.tmp/forge/feedback-YYYYMMDD-{description}.md`.
This records each agent's output, evaluator findings, iteration count, and tool availability.
Git-auditable trail of every pipeline run.

### Pipeline Metrics (append to every audit trail)

Track these metrics to measure which agents justify their cost over time:

```markdown
## Pipeline Metrics

- **Route:** TRIVIAL | CLEAR PRD | STANDARD
- **Agents used:** [list]
- **Iterations:** X/3
- **Final verdict:** PASS | FAIL (escalated)
- **Quality dimensions (final):** Convention [X/3], Tests [X/3], Patterns [X/3], Completeness [X/3]

### Per-Agent Value
| Agent | Key contribution | Could skip? |
|-------|-----------------|-------------|
| Investigator | [what it found that wasn't obvious] | [yes/no — why] |
| Challenger | [gaps it caught] | [yes/no — why] |
| Planner | [design choices it made] | [yes/no — why] |
| Generator | N/A (always needed) | no |
| Evaluator | [BLOCKERs caught, iterations needed] | no |

### Reconciliations
[Any cases where the generator's codebase findings contradicted the plan.
These indicate the investigator or planner missed something.]
```

Over time, these metrics show patterns: if the challenger column consistently says "no gaps found," it may not justify its cost for this project's task types.
Review accumulated metrics periodically to decide if the pipeline routing thresholds need adjustment.


## Phase 0 — ROUTE

Before spawning any agent, classify the task:

| Complexity | Route | Agents used |
|-----------|-------|-------------|
| **TRIVIAL** | Direct | Generator → Evaluator only |
| **CLEAR PRD** | Short | Challenger → Planner → Generator → Evaluator |
| **STANDARD** | Full | Investigator → Challenger → Planner → Generator → Evaluator |

Signals for routing:
- TRIVIAL: task touches 1 file, change is obvious, no design decisions
- CLEAR PRD: user provided a detailed spec with requirements, acceptance criteria, edge cases
- STANDARD: task needs codebase exploration, has ambiguity, touches multiple files

Announce the route: "Routing as [TRIVIAL/CLEAR PRD/STANDARD] — using [agent list]."


## Phase 1 — INVESTIGATE (STANDARD route only)

Spawn the `forge-investigator` agent with:
- The task description (from user input or plan file)
- Context about why this change is needed
- Whether `.claude/forge/evaluator-criteria.md` exists

**Wait for the investigator's output before proceeding.**

If the investigator generated a new evaluator-criteria.md:
- Show the user a summary of the generated criteria
- Ask if they want to review before continuing (if the task is complex)

If the investigation report has critical gaps, ask the user before proceeding.


## Phase 2 — CHALLENGE

Spawn the `forge-challenger` agent with:
- The investigation report (or the user's PRD for CLEAR PRD route)
- The original task description
- The evaluator criteria path

**Wait for the challenger's output before proceeding.**

If the challenger found CRITICAL gaps, show them to the user.
If only ADVISORY findings, incorporate them and proceed.


## Phase 3 — PLAN

Spawn the `forge-planner` agent with:
- The investigation report (if available)
- The challenger's refined requirements and findings
- The evaluator criteria path

**Wait for the planner's output before proceeding.**

Read the planner's output.
If the plan has gaps or ambiguities, ask the user before proceeding.
If the plan is clear, move to Phase 4.


## Phase 4 — GENERATE (iteration 1)

Spawn the `forge-generator` agent with inputs based on route:

**STANDARD / CLEAR PRD route:**
- The planner's output, specifically these sections: Task, Approach, Files to Create, Files to Modify, Constraints, Challenger-Sourced Requirements, Dependencies, Task-Specific Criteria
- The evaluator criteria path
- Instruction: "Read the criteria file first. Self-check before reporting done."
- Do NOT pass the planner's reasoning or alternatives — only the actionable plan sections

**TRIVIAL route (no planner):**
- The original task description
- The evaluator criteria path (if it exists)
- Instruction: "This is a trivial change. Implement directly, self-check against criteria if available."
- No planner constraints or task-specific criteria — the task is simple enough not to need them

**Wait for the generator's output.**

Collect the list of files created/modified.


## Phase 5 — EVALUATE (iteration 1)

Spawn the `forge-evaluator` agent with inputs based on route:

**STANDARD / CLEAR PRD route:**
- The list of files created/modified by the generator
- The generator's Interpretation Notes section (for sprint contract validation)
- The original task description
- The planner's Task-Specific Criteria section (extracted verbatim)
- The planner's Constraints section (extracted verbatim — deferred items)
- The planner's Challenger-Sourced Requirements section (extracted verbatim)
- `iteration: 1`

**TRIVIAL route (no planner):**
- The list of files created/modified by the generator
- The original task description
- No task-specific criteria — evaluate against static criteria only
- No planner constraints — nothing is deferred
- `iteration: 1`

**Wait for the evaluator's verdict.**


## Phase 6 — LOOP or FINISH

### If verdict is PASS:
- Report success to the user
- Show the evaluator's summary (BLOCKERs: 0, WARNINGs: N)
- Show tool availability (what was checked vs. skipped)
- Write audit trail to `.agents.tmp/forge/feedback-YYYYMMDD-{description}.md`

### If verdict is FAIL and iteration < 3:
- Show the evaluator's findings briefly
- Extract the **Shared Learnings** block from the evaluator's output (if present)
- Append any new learnings to the accumulated learnings from prior iterations
- Spawn the `forge-generator` again with:
  - The evaluator's specific findings (file:line, rule, fix hint)
  - The accumulated shared learnings from all prior iterations
  - Instruction: "Fix ONLY the flagged issues. Do not change anything else. Read the shared learnings — they contain patterns discovered in prior iterations that may prevent repeated mistakes."
- Then spawn the `forge-evaluator` again with the updated file list and `iteration: N+1`

### If verdict is FAIL and iteration = 3:
- Report: "Evaluator found issues the generator couldn't resolve in 3 iterations."
- Show all remaining BLOCKERs with file:line references
- Write audit trail
- Ask the user how to proceed

### If BLOCKER count did not decrease between iterations:
- Stop immediately — don't waste iterations
- Report: "Generator is stuck — same issues persist. Escalating."
- Show findings and ask the user
- Write audit trail


## Agent Dispatch Rules

- **Challenger and Evaluator** run as `model: opus` — these are adversarial roles where weaker models miss real problems. Non-negotiable.
- **Investigator and Planner** run as `model: opus` — report and plan quality directly affect downstream agents. Weak investigation leads to weak plans.
- **Generator** inherits the session model — the user controls their coding session's capability.
- **Never run pipeline agents in parallel** — the pipeline is sequential
- **Each agent gets full context** — don't summarize, pass complete output
- **Generator has advisory checkpoints** — the generator pauses before substantive work and before declaring done to verify alignment with the plan. If the generator's Notes section reports a reconciliation (codebase contradicts plan), review it before passing to the evaluator — if the deviation is significant, ask the user
- **The evaluator criteria file is the contract** — generator and evaluator both read it
- **Pass planner constraints to evaluator** — prevents false positives on deferred items
- **Skip evaluator only for TRIVIAL route when build+test+lint all pass** — convention checks matter for anything beyond a trivial change


## Criteria Lifecycle

The evaluator-criteria.md lives at `.claude/forge/evaluator-criteria.md` in each project.

| Event | Action |
|-------|--------|
| First run, no criteria exists | Investigator auto-generates from CLAUDE.md, rules, codebase patterns |
| Challenger finds missing convention | Suggests addition to criteria in challenge report |
| Tool becomes unavailable | Evaluator notes it, does not fail — graceful degradation |
| User wants to update criteria | Edit the file directly — it's a versioned project artifact |


## Common Mistakes

| Don't | Do |
|-------|-----|
| Run full pipeline for a typo fix | Route as TRIVIAL — generator + evaluator only |
| Skip the challenger because "the PRD looks complete" | Always run challenger — it finds what you didn't think to look for |
| Summarize agent outputs when passing to next agent | Pass complete output — the next agent needs full context |
| Let the generator run forever on stuck issues | Stuck detection: if BLOCKER count doesn't decrease, escalate |
| Ignore tool availability | Report what was checked and what was skipped |
| Duplicate rules in task-specific criteria | Reference the source document instead |
