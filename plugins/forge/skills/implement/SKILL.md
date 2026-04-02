---
name: implement
description: >
  Adversarial implementation pipeline — orchestrates investigator, challenger, planner,
  generator, and evaluator agents in a GAN-inspired loop.
  Routes dynamically: trivial tasks skip early agents, clear PRDs skip investigation.
  Auto-generates evaluator criteria on first run in a project.
  Triggers: "implement", "forge implement", "adversarial pipeline",
  "build with forge", "implement feature".
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

Each invocation writes a feedback file at `.agents.tmp/forge/feedback-{timestamp}.md`.
This records each agent's output, evaluator findings, iteration count, and tool availability.
Git-auditable trail of every pipeline run.


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

Spawn the `forge-generator` agent with:
- The planner's full output (files to create/modify, references, constraints, task-specific criteria)
- The evaluator criteria path
- Instruction: "Read the criteria file first. Self-check before reporting done."

**Wait for the generator's output.**

Collect the list of files created/modified.


## Phase 5 — EVALUATE (iteration 1)

Spawn the `forge-evaluator` agent with:
- The list of files created/modified by the generator
- The original task description
- The planner's task-specific criteria
- The planner's constraints (deferred items)
- `iteration: 1`

**Wait for the evaluator's verdict.**


## Phase 6 — LOOP or FINISH

### If verdict is PASS:
- Report success to the user
- Show the evaluator's summary (BLOCKERs: 0, WARNINGs: N)
- Show tool availability (what was checked vs. skipped)
- Write audit trail to `.agents.tmp/forge/feedback-{timestamp}.md`

### If verdict is FAIL and iteration < 3:
- Show the evaluator's findings briefly
- Spawn the `forge-generator` again with:
  - The evaluator's specific findings (file:line, rule, fix hint)
  - Instruction: "Fix ONLY the flagged issues. Do not change anything else."
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

- **Investigator and Challenger** run as `model: sonnet` (fast, good at analysis)
- **Planner** runs as `model: sonnet` (analysis, not generation)
- **Generator** runs as default model (needs full coding capability)
- **Evaluator** runs as `model: sonnet` (fast, adversarial checking)
- **Never run pipeline agents in parallel** — the pipeline is sequential
- **Each agent gets full context** — don't summarize, pass complete output
- **The evaluator criteria file is the contract** — generator and evaluator both read it
- **Pass planner constraints to evaluator** — prevents false positives on deferred items
- **Skip evaluator when deterministic tests exist** — if the task is purely code and build+test+lint pass, that's stronger evidence than evaluator opinion


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
