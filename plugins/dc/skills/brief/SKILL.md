---
name: brief
description: 'Use when the user shares a brain dump, messy thoughts, stream-of-consciousness notes, or unstructured ideas and wants them turned into a structured brief for an AI coding agent. Also use when the user says "structure this for a coding session", "turn this into a task", or pastes raw requirements. Triggers: "brain dump", "messy thoughts", "structure this", "turn into a brief", "organize for coding session", "make this actionable", "structure my thoughts".'
---

# Brief — Structure Raw Thoughts into Executable Briefs

Transform messy developer brain dumps into structured briefs that an AI coding agent can execute in a fresh session with zero prior context.

This is NOT summarization.
Every technical detail matters.
A missed file path, URL, constraint, or implicit requirement can derail an entire coding session.

**Announce at start:** "Structuring your thoughts into an executable brief."

## Reasoning Stages

Follow these stages internally before writing:

1. **DECODE** — Read through the mess. Fix typos mentally. Identify the core goal underneath all the thinking-out-loud.

2. **EXTRACT EVERYTHING** — Pull out every concrete detail:
   - File paths, folder names, URLs, repo references
   - Tool names, library names, service names, API references
   - Specific commands, scripts, configurations mentioned
   - Constraints and rules ("only create files in X", "don't modify Y", "read-only")
   - Environment details (dev/staging/prod, local vs remote)
   - Naming conventions, patterns, namespaces mentioned
   - References to existing docs, examples, or source-of-truth files
   - Workflow steps (how things currently work)
   - What the developer explicitly does NOT know and wants to discover
   - Dependencies between steps

3. **SEPARATE FACTS FROM EXPLORATION** — Clearly distinguish:
   - What the developer **KNOWS** (established facts, current workflow)
   - What the developer **WANTS TO FIND OUT** (questions, unknowns, ideas to validate)
   - What the developer **WANTS TO BUILD/CHANGE** (desired outcome)

4. **STRUCTURE** — Organize into the output template below.

5. **VERIFY** — Check against the raw thoughts:
   - Every URL mentioned? ✓
   - Every file path mentioned? ✓
   - Every constraint mentioned? ✓
   - Every open question captured? ✓
   - Every tool/service/library named? ✓
   - Developer's intent accurately represented? ✓
   - Nothing added that the developer didn't say or imply? ✓

## Output Template

```
## Goal

One to three sentences. What is the developer trying to accomplish? Start with the verb.

## Context

Essential background an AI agent needs. Current system, current workflow, current pain points.
Only what's needed — but miss nothing.

## Current Workflow (if described)

Step-by-step: how things work today. Numbered steps.
This gives the AI agent the "before" picture.

## What We Want

Desired end state or deliverables. Be specific.
If the developer described multiple deliverables, list each one.

## Open Questions

Things the developer explicitly wants to investigate or doesn't know yet.
These become research tasks for the AI agent.

## References & Resources

Every file path, URL, repo, script, doc, and example file mentioned — organized and deduplicated.
Use the EXACT paths/URLs from the raw thoughts. Format:

- `path/to/file` — what it is, why it matters
- `https://url` — what it is

## Constraints & Rules

Things the AI agent must respect.
Permissions, read-only repos, folders to use, git exclusions, naming conventions, environment rules.

## Suggested Approach

If the developer described or implied an order of operations, lay it out as numbered steps.
If not, propose a logical sequence based on the extracted requirements.
Do not add steps the developer didn't mention or imply (like testing, documentation, or cleanup).
```

Omit empty sections — if the developer didn't describe a current workflow, skip that section.

## Hard Rules

> **NEVER add your own opinions, recommendations, or scope beyond what the developer said or implied.**
>
> If a decision is unresolved, put it in Open Questions — do not pick a side.

> **NEVER paraphrase exact technical terms.**
>
> Preserve `public/i18n/FFA_dev_translations.csv` exactly — do not write "the translations CSV".

> **Flag ambiguity explicitly.**
>
> If something can be interpreted multiple ways: "⚠️ UNCLEAR: [what's ambiguous] — clarify before starting"

> **The brief must be self-contained.**
>
> The AI agent receiving it will have ZERO context from this conversation.

## Writing Rules

- Direct, clear language. No filler.
- Fix obvious typos in the output (the developer knows what they meant).
- Constraints go in the Constraints section, not buried inside other sections.
- References go in the References section, not scattered inline.
- Keep the brief scannable — headings, bullets, tables where appropriate.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Recommend solutions the developer didn't ask for | Put unresolved decisions in Open Questions |
| Paraphrase exact file paths or URLs | Preserve technical terms verbatim |
| Bury constraints inside task descriptions | Collect all constraints in the Constraints section |
| Mix known facts with unknowns | Separate into Context (known) vs Open Questions (unknown) |
| Skip the current workflow | Document the "before" picture if the developer described it |
| Add a "Verification" or "Testing" section the developer didn't mention | Only include what was said or clearly implied |
| Write "the config file" when they said `apps/forest-flow/project.json` | Use exact paths always |
