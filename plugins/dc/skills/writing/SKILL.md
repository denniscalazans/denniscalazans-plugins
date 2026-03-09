---
name: markdown-writing
description: 'Use when writing or editing markdown files, PR descriptions, code comments, or documentation. Also use when producing commit bodies, README updates, or deciding whether content should be a table, list, or paragraph. Triggers: "format this", "write a PR description", "one sentence per line", "markdown convention", "writing style", "fix formatting", "paragraph spacing", "trailing spaces", "table or list".'
---

# Markdown Writing Convention

The reader is a highly skilled person with a complex, graph-like mind.
Their thinking expands and contracts in trees, branches, connections — not in flat lines of text.


But **reading is sequential** — top to bottom, one line at a time.
The intake channel is narrow even when the brain behind it is vast.
Focus is easily disrupted by noise, dense paragraphs, or sentences that demand too much mental buffer before the meaning lands.


The AI's job is to **render knowledge structurally** — shaping it so the sequential reading experience maps efficiently to the reader's non-linear thinking.
This is NOT about dumbing down content or making text poor.
It's about using every available formatting resource — line breaks, weight, space, indentation, lists, tables — to give each idea the right shape, size, and placement on the page.


Even a plain text editor offers line breaks, tabs, and dashes for visual structure.
Markdown amplifies that with headings, bold, tables, lists, and code blocks.
Use all of it.


## The Structural Toolkit

Every structural element exists to serve the reader's intake:

| Element | Cognitive purpose | When to use |
|---------|------------------|-------------|
| **Headings** | Navigation landmarks — the reader knows where they are | Sections, topic shifts, named concepts |
| **Bold** | Emphasis and scannability — the eye catches key terms instantly | Key terms, pivotal phrases, critical warnings (use sparingly) |
| **Lists** | Parallel items — the brain processes them as a group, not a sequence | Steps, options, requirements, any set of 3+ related items |
| **Tables** | Comparison — the brain maps rows/columns faster than prose | Comparisons, mappings, don't/do pairs, reference data |
| **Short paragraphs** | Digestibility — each block is one idea the brain can hold | Every paragraph: 2–4 sentences max |
| **White space** | Breathing room — visual rest between ideas | Double blank lines between paragraphs |
| **Code blocks** | Literal precision — no ambiguity about syntax or format | Commands, file paths, configuration, code |


## Sentence Formatting Rules

- **One sentence per line** — each sentence appears on its own line
- **Group related sentences** — sentences about the same idea sit together with only a newline between them (no blank line), forming a visual block
- **Double blank line between paragraphs** — use **two empty lines** between paragraphs so the gap is visually obvious and unmistakable
- **Trailing two spaces** — end each sentence line with two trailing spaces (`  `) to force a `<br>` in rendered markdown; without this, renderers collapse single newlines and join sentences together
- **Never isolate every sentence** — putting a blank line after every sentence destroys paragraph structure and makes text harder to scan
- **No multiple sentences on a single line** — never write `"Sentence one. Sentence two."`
- **Applies to:** `.md` files, PR descriptions, code comments (TypeScript, Java, etc.), documentation


## Choosing the Right Structure

Before writing a paragraph, ask: **what structure would help the reader absorb this fastest?**

| Content type | Best structure | Why |
|-------------|---------------|-----|
| A sequence of steps | Numbered list | The reader sees order and progress |
| A set of parallel items | Bullet list | The brain processes them as a group |
| A comparison (A vs B) | Table | Side-by-side is faster than back-and-forth prose |
| A definition or explanation | Bold term + short paragraph | The reader anchors on the term, then reads the explanation |
| A warning or critical rule | Bold or blockquote | Stands out from the surrounding text |
| A long block of prose (5+ sentences) | Break into sub-sections with headings | Headings give the reader navigation landmarks |


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

❌ **Incorrect — wall of prose when a table or list would be clearer:**

```
There are three types of routing. The first is content-based routing where
the input is classified by topic. The second is complexity-based routing
where simple questions go to cheaper models. The third is priority-based
routing where urgent requests skip the queue.
```

✅ **Correct — same content as a table:**

```
| Routing type | How it works |
|-------------|-------------|
| Content-based | Input classified by topic |
| Complexity-based | Simple questions → cheaper models |
| Priority-based | Urgent requests skip the queue |
```


## Common Mistakes

| Don't | Do | Why |
|-------|-----|-----|
| Isolate every sentence with blank lines | Group related sentences into blocks | Isolated sentences destroy paragraph structure |
| Use only prose for everything | Use lists, tables, headings, bold | Different structures serve different cognitive purposes |
| Write 5+ sentences in one block | Break into 2–4 sentence paragraphs | Large blocks overwhelm working memory |
| Use single blank line between paragraphs | Use double blank line (two empty lines) | Single blank line doesn't create enough visual separation |
| Skip trailing two spaces on sentence lines | End each line with `  ` | Without them, rendered markdown joins lines together |
| Bold entire sentences | Bold only key terms or phrases | Over-bolding defeats the purpose — nothing stands out |
| Use headings for emphasis | Use headings for navigation | Headings are landmarks, not decoration |


---
