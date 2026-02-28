---
name: markdown-writing
description: Apply the markdown writing convention before writing any markdown, PR descriptions, code comments, or documentation. Use this skill whenever you're about to write or edit `.md` files, compose PR descriptions, write code comments, or produce any written content. The convention ensures consistency and readability across all written output.
compatibility: None
---

# Markdown Writing Convention

You are about to write markdown or code comments. Follow this convention consistently.

## The Rule

- **One sentence per line** — Each sentence appears on its own line
- **Blank lines between paragraphs** — Separate logical paragraphs with a blank line (not just a newline)
- **No multiple sentences on a single line** — Never write `"Sentence one. Sentence two."`
- **Applies to:** `.md` files, PR descriptions, code comments (TypeScript, Java, etc.), documentation

## Examples

✅ **Correct:**

```
This is line.
This is a new line.

This is a new paragraph.
This is the second line of the second paragraph.
```

❌ **Incorrect:**

```
This is line. This is a new line.
This is a new paragraph. This is the second line of the second paragraph.
```

## How to Apply

When writing markdown or comments, after finishing a sentence, press Enter to put the next sentence on a new line. When moving to a new paragraph or idea, add a blank line (two newlines total) before starting.

**In code comments:**

```typescript
// This is the first sentence.
// This is the second sentence.
//
// This is a new paragraph with more detail.
// It continues on the next line.
```

**In markdown:**

```
This is the opening sentence about the feature.
This is additional context about the same idea.

This is a new paragraph introducing a different aspect.
It continues with more detail on the new topic.
```

---

Now that you've reviewed the convention, apply it as you write.
