---
name: run-flows
description: >
  Use when the user wants to run multiple Playwright flow files in parallel, batch-execute test
  suites across subagents, or collect results from many flows into a summary report.  
  Also use when repeating the same flow across multiple roles or environments, or when
  cross-batch learning is needed to avoid agents rediscovering the same failures independently.  
  Triggers: "run flows", "parallel flows", "cross-batch",
  "flow runner", "run the flows", "execute all flows".
---

# Run Flows — Parallel Batch Runner with Cross-Batch Learning

Orchestrate multiple Playwright `.flow.ts` files in parallel via subagents, collect pass/fail results, and feed lessons learned from earlier batches into later ones so agents stop rediscovering the same issues independently.


## Quick Start

```
/browser:run-flows .agents.tmp/sonarqube-visual-tests/playwright/
/browser:run-flows .agents.tmp/ffa-475/playwright/ --parallelism 4
/browser:run-flows .agents.tmp/ffa-475/playwright/ --config e2e/playwright.config.ts
```


## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `directory` | Yes | — | Path to directory containing `.flow.ts` files (searched recursively) |
| `parallelism` | No | 3 | Maximum concurrent subagents (each owns one browser context) |
| `config` | No | Project's `playwright.config.ts` | Path to Playwright config file passed to each subagent |


## Process

### Step 1: Discover flow files

Recursively find all `*.flow.ts` files in the provided directory.  
Sort alphabetically and report the total count before proceeding.

If zero files are found, report the error and stop — do not dispatch any subagents.

### Step 2: Partition into batches

Divide the flow files into batches of size equal to the `parallelism` parameter.  
For example, 9 flows with parallelism 3 produces 3 batches of 3.

If all flows fit in a single batch (count <= parallelism), skip cross-batch learning — run them all at once.

### Step 3: Write all flow files before dispatching

This is critical.  
All `.flow.ts` files must already exist on disk before any subagent is dispatched.  
Subagents receive Bash-only tasks — they run flows and fix failing selectors, but never create new files from scratch.

If the user asks to both generate and run flows, generate all files first in the main context, then invoke this skill to run them.

### Step 4: Dispatch Batch 1

For each flow in the batch, dispatch a subagent with the following prompt structure:

```
Run the Playwright flow at <flow-path>.
Use config: <config-path>
Command: npx playwright test <flow-path> --config <config-path>

If the test fails:
1. Read the error output carefully
2. Fix the selector, timing, or assertion in the flow file
3. Re-run the test
4. Repeat up to 3 attempts total

After the final run, report:
- PASS or FAIL
- Duration (from Playwright output)
- Error summary (if FAIL)
- Any DOM quirks, selector corrections, or timing fixes you discovered
```

Each subagent needs the `Bash` tool permission.  
Dispatch all subagents in the batch simultaneously — do not wait for one to finish before starting the next.

### Step 5: Collect Batch 1 results

Wait for all subagents in the batch to complete.  
Record each result: flow name, PASS/FAIL, duration, error summary, and any discoveries.

### Step 6: Extract shared findings

After each batch completes, review all subagent reports and extract shared findings.  
Shared findings are patterns that would help the next batch avoid repeated failures.

Look for:
- **Selector corrections** — a CSS class or `data-test-id` that differs from what the flow expected
- **DOM quirks** — elements that require extra steps (toggles, dropdowns, modals) before the target element is interactable
- **Timing patterns** — pages that need DOM marker waits instead of `networkidle`
- **State preconditions** — filters, toggles, or views that must be cleared/set before assertions
- **Framework-specific behaviors** — Angular Material class names, React portals, Vue transition states

Write the shared findings in the format described in the "Shared Findings Format" section below.

### Step 7: Dispatch subsequent batches with findings

For Batch 2 and later, prepend the shared findings to each subagent's prompt:

```
## Shared Findings from Previous Batches

<findings from Step 6>

Apply these findings proactively — do not wait to rediscover them.

---

Run the Playwright flow at <flow-path>.
...
```

Repeat Steps 5-7 for each remaining batch.

### Step 8: Produce summary report

After all batches complete, produce the summary report described in the "Summary Report Format" section below.


## Cross-Batch Learning

This is the key differentiator of this skill.  
Without cross-batch learning, N agents independently rediscover the same problems — multiplying wasted tokens and time.

The learning loop:

```
Batch 1 → results → extract findings → inject into Batch 2 prompts
Batch 2 → results → merge findings → inject into Batch 3 prompts
...
Batch N → results → final summary
```

Findings are **cumulative** — Batch 3 receives findings from both Batch 1 and Batch 2.  
New findings are appended; contradictions are resolved by preferring the more recent discovery.


## Shared Findings Format

Use this template when extracting findings between batches.  
Each finding is one line: a short label, then the actionable detail.

```markdown
## Shared Findings (after Batch N)

- <label>: <actionable detail with exact selectors, class names, or steps>
- <label>: <actionable detail>
```

Real-world example from a 9-flow test session:

```markdown
## Shared Findings (after Batch 1)

- Map toggle: pages with Google Maps default to map view — click `[data-test-id="map-toggle-button"]` before table assertions
- Filter state: a default filter may be pre-set — click `[data-test-id="clear-filters-btn"]` first
- mat-mdc-row: Angular Material renders `<tr class="mat-mdc-row">`, not `<mat-row>`
- networkidle: Google Maps tiles block networkidle — use `domcontentloaded` + DOM markers instead
```

Keep each finding concrete and actionable.  
Vague findings like "selectors may differ" do not help — include the exact selector or class name.


## Subagent Dispatch Pattern

Follow the "write locally, run remotely" pattern.

1. **Main context writes** all flow files (you have Write permission)
2. **Subagents run** flows via Bash (they have Bash permission)
3. **Subagents can edit** files they are working on (fix selectors, timing, assertions)
4. **Subagents cannot** reliably create new files from scratch

This split avoids permission friction.  
Subagents dispatched with both Write and Bash tasks burn tokens on permission errors without producing results.

### Retry budget

Each subagent gets up to 3 run attempts per flow:
- Attempt 1: run as-is
- Attempt 2: fix the failure, re-run
- Attempt 3: fix again, final re-run

After 3 failed attempts, the subagent reports FAIL with the last error.  
The orchestrator does not retry failed flows in subsequent batches — they appear as FAIL in the summary.


## Summary Report Format

After all batches complete, produce a markdown summary in the main context.

```markdown
## Flow Run Summary

**Directory:** <path>
**Total flows:** <count>  
**Passed:** <count>  **Failed:** <count>  
**Duration:** <total wall-clock time>

| # | Flow | Result | Duration | Notes |
|---|------|--------|----------|-------|
| 1 | create-site.flow.ts | PASS | 12s | — |
| 2 | edit-property.flow.ts | PASS | 8s | Fixed mat-mdc-row selector |
| 3 | delete-site.flow.ts | FAIL | 45s | Timeout on confirmation dialog |

## Shared Findings (all batches)

- <cumulative findings list>

## Failed Flows

### delete-site.flow.ts
- **Error:** Timeout waiting for `[data-test-id="confirm-delete"]`
- **Attempts:** 3
- **Last fix tried:** Increased timeout to 30s, checked dialog status
```

Include the "Failed Flows" section only if there are failures.  
Each failed flow gets its own subsection with the error, attempt count, and last fix attempted.


## Common Mistakes

| Do NOT | Do instead |
|--------|-----------|
| Dispatch subagents to both write AND run flow files | Write all `.flow.ts` files in the main context first, dispatch subagents to run only |
| Run all flows sequentially in a single subagent | Dispatch one subagent per flow file for true parallelism |
| Skip shared findings extraction between batches | Always extract and inject findings — this prevents repeated discovery of the same issues |
| Include vague findings like "selectors may differ" | Include exact selectors, class names, and steps: `mat-mdc-row` not `<mat-row>` |
| Retry failed flows in subsequent batches | Each flow gets 3 attempts within its subagent — the orchestrator does not re-dispatch |
| Dispatch more subagents than the parallelism limit | Respect the limit — each subagent owns a browser context and too many cause resource contention |
| Forget to pass the Playwright config path | Always include `--config <path>` in the subagent command so flows use the correct base URL and settings |
| Wait for one subagent to finish before dispatching the next in a batch | Dispatch all subagents in a batch simultaneously — they run in parallel |
