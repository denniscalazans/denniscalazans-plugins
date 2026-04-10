# Forge Pipeline Architecture

The forge implement skill orchestrates five agents in a sequential pipeline with dynamic routing, advisory checkpoints, and cross-iteration learning.


## Pipeline Overview

```mermaid
flowchart TD
    USER[User task] --> ROUTE

    subgraph "Phase 0 — Route"
        ROUTE{Classify complexity}
        ROUTE -->|TRIVIAL| GEN
        ROUTE -->|CLEAR PRD| CHALL
        ROUTE -->|STANDARD| INV
    end

    subgraph "Phase 1 — Investigate"
        INV[Investigator]
        INV -->|"TODAY IS / EXPECTED IS report"| CHALL
        INV -.->|auto-generates if missing| CRITERIA[(evaluator-criteria.md)]
    end

    subgraph "Phase 2 — Challenge"
        CHALL[Challenger]
        CHALL -->|"gaps, edge cases, refined requirements"| PLAN
    end

    subgraph "Phase 3 — Plan"
        PLAN[Planner]
        PLAN -->|"files, references, constraints,\nchallenger-sourced requirements,\ntask-specific criteria"| GEN
    end

    subgraph "Phase 4 — Generate"
        GEN[Generator]
        GEN -->|"advisory checkpoint:\nverify approach before writing"| GEN
        GEN -->|"advisory checkpoint:\nverify intent before reporting done"| GEN
        GEN -->|"files created/modified\n+ interpretation notes"| EVAL
    end

    subgraph "Phase 5 — Evaluate"
        EVAL[Evaluator]
        EVAL -->|reads| CRITERIA
        EVAL -->|"validates generator\ninterpretation notes"| EVAL
        EVAL -->|"BLOCKERs, WARNINGs,\nquality dimensions 0-3,\nshared learnings,\nproactive findings"| DECIDE
    end

    subgraph "Phase 6 — Converge"
        DECIDE{Verdict?}
        DECIDE -->|PASS| DONE[Report success + audit trail]
        DECIDE -->|"FAIL\niteration < 3"| LOOP
        DECIDE -->|"FAIL\niteration = 3"| ESCALATE[Escalate to user]
        DECIDE -->|"BLOCKER count\nnot decreasing"| ESCALATE

        LOOP[Accumulate shared learnings]
        LOOP -->|"findings + learnings"| GEN
    end
```


## Agent Roles

```mermaid
flowchart LR
    subgraph "Read-only agents"
        INV2[Investigator\nmodel: sonnet\ncolor: blue]
        CHALL2[Challenger\nmodel: sonnet\ncolor: purple]
        PLAN2[Planner\nmodel: sonnet\ncolor: blue]
    end

    subgraph "Write agent"
        GEN2[Generator\nmodel: default\ncolor: green]
    end

    subgraph "Adversarial agent"
        EVAL2[Evaluator\nmodel: sonnet\ncolor: orange]
    end

    INV2 -->|"explores codebase,\nproduces grounded report"| CHALL2
    CHALL2 -->|"finds gaps,\nedge cases,\nmissed patterns"| PLAN2
    PLAN2 -->|"designs approach,\nlists files + references"| GEN2
    GEN2 -->|"writes code,\nself-checks,\ndeclares interpretations"| EVAL2
    EVAL2 -->|"finds violations,\nscores dimensions,\nextracts learnings"| GEN2
```


## Routing

| Route | When | Agents | Typical use |
|-------|------|--------|-------------|
| TRIVIAL | 1 file, obvious change, no design decisions | Generator → Evaluator | Typo in a rule, config value change |
| CLEAR PRD | User provided detailed spec with requirements and edge cases | Challenger → Planner → Generator → Evaluator | Well-specified feature ticket |
| STANDARD | Needs codebase exploration, has ambiguity, touches multiple files | All five agents | New feature, cross-cutting refactor |


## Feedback Mechanisms

```mermaid
flowchart TD
    subgraph "Sprint Contract"
        GEN3[Generator] -->|"Interpretation Notes:\nhow ambiguous rules\nwere read"| EVAL3[Evaluator]
        EVAL3 -->|"validates interpretations,\nflags mismatches as BLOCKERs"| GEN3
    end

    subgraph "Cross-Iteration Learning"
        EVAL4[Evaluator] -->|"Shared Learnings:\nreusable patterns"| ACCUM[Implement skill\naccumulates learnings]
        ACCUM -->|"all prior learnings"| GEN4[Generator\nnext iteration]
    end

    subgraph "Quality Dimensions"
        EVAL5[Evaluator] -->|"Convention: 2/3\nTests: 1/3\nPatterns: 3/3\nCompleteness: 2/3"| GEN5[Generator\nknows WHERE\nto improve]
    end

    subgraph "Reconciliation"
        GEN6[Generator] -->|"Plan says X,\nbut codebase has Y.\nI followed Y because..."| IMPL[Implement skill\nreviews deviation]
        IMPL -->|significant?| USER2[Ask user]
    end
```


## Evaluator Output Structure

The evaluator produces these sections in order:

1. **Verdict** — PASS or FAIL
2. **Iteration** — X/3
3. **BLOCKERs (Tier 1)** — rule violations with file:line, cause FAIL
4. **WARNINGs (Tier 2)** — quality suggestions, informational only
5. **Task-Specific BLOCKERs** — planner/challenger requirements not met, cause FAIL
6. **Dynamic Checks** — three-state: PASS / FAIL / NOT RUN (with reason)
7. **Proactive Findings** — adjacent issues, don't affect verdict
8. **Quality Dimensions** — four 0-3 scores, don't affect verdict
9. **Shared Learnings** — patterns for the next iteration
10. **Tool Availability** — what was detected and used
11. **Summary** — counts + dimension scores


## Convergence Rules

- BLOCKER count = 0 → **PASS**
- BLOCKER count > 0, iteration < 3 → **FAIL**, loop with findings + learnings
- BLOCKER count > 0, iteration = 3 → **FAIL**, escalate to user
- BLOCKER count not decreasing → escalate immediately (stuck detection)
- WARNINGs and quality dimension scores are informational — they don't cause FAIL


## Pipeline Metrics (audit trail)

Each run appends metrics to `.agents.tmp/forge/feedback-YYYYMMDD-{description}.md`:

- Route taken, agents used, iterations needed
- Final quality dimensions
- Per-agent value: key contribution + "could skip?" assessment
- Reconciliations where generator contradicted the plan

Over time these metrics show which agents justify their cost and whether routing thresholds need adjustment.
