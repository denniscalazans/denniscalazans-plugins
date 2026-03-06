---
name: markdown-writing
description: Use when writing or editing markdown files, PR descriptions, code comments, or documentation. Also use when producing commit bodies, README updates, or any written content that must follow the one-sentence-per-line convention.
---

# Markdown Writing Convention

You are about to write markdown or code comments. Follow this convention consistently.

## The Rule

- **One sentence per line** — each sentence appears on its own line
- **Group related sentences** — sentences about the same idea sit together with only a newline between them (no blank line), forming a visual block
- **Double blank line between paragraphs** — use **two empty lines** between paragraphs so the gap is visually obvious and unmistakable
- **Trailing two spaces** — end each sentence line with two trailing spaces (`  `) to force a `<br>` in rendered markdown; without this, renderers collapse single newlines and join sentences together
- **Never isolate every sentence** — putting a blank line after every sentence destroys paragraph structure and makes text harder to scan
- **No multiple sentences on a single line** — never write `"Sentence one. Sentence two."`
- **Applies to:** `.md` files, PR descriptions, code comments (TypeScript, Java, etc.), documentation

## Examples

Using `··` to show where trailing two spaces go:

✅ **Correct — related sentences grouped, double blank line between paragraphs:**

```
Workflows are systems where LLMs follow predefined paths in code.··
Agents are systems where the LLM decides dynamically what to do.··
The difference is control: in workflows the developer leads; in agents the model leads.


The golden rule is to start with the simplest solution possible.··
For many applications, a single well-optimized LLM call is enough.··
Only add complexity when there is measurable gain.
```

❌ **Incorrect — every sentence isolated (no paragraph structure):**

```
Workflows are systems where LLMs follow predefined paths in code.

Agents are systems where the LLM decides dynamically what to do.

The difference is control: in workflows the developer leads; in agents the model leads.

The golden rule is to start with the simplest solution possible.

For many applications, a single well-optimized LLM call is enough.

Only add complexity when there is measurable gain.
```

❌ **Incorrect — single blank line between paragraphs (not enough visual separation):**

```
Workflows are systems where LLMs follow predefined paths in code.
Agents are systems where the LLM decides dynamically what to do.

The golden rule is to start with the simplest solution possible.
For many applications, a single well-optimized LLM call is enough.
```

❌ **Incorrect — multiple sentences on one line:**

```
Workflows are systems where LLMs follow predefined paths. Agents are systems where the LLM decides dynamically.
```

## How to Decide What Goes in One Block

A paragraph block groups sentences that share the same **topic or logical unit**.

Ask: "Does this next sentence continue the same idea, or start a new one?"
If it continues — newline with trailing two spaces.
If it starts a new idea — double blank line.

## How to Apply

**In code comments:**

```typescript
// This is the first sentence about authentication.
// This adds detail about the token flow.
//
//
// This is a new paragraph about error handling.
// It continues with retry logic.
```

**In markdown:**

```
This is the opening sentence about the feature.··
This is additional context about the same idea.··
This completes the thought.


This is a new paragraph introducing a different aspect.··
It continues with more detail on the new topic.
```

---

Now that you've reviewed the convention, apply it as you write.
