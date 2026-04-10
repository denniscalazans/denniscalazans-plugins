---
name: distill
description: 'Use when the user asks to distill, extract key insights, or restructure content for clarity. Also use when the user shares a brainstorm, thought dump, meeting notes, or long-form content and wants it transformed into a reader-friendly format. Triggers: "distill this", "extract insights", "make this clearer", "restructure for readability", "summarize this", "TL;DR", "key takeaways", "simplify this text", "clean this up", "organize my notes", "break this down".'
---

# Distill

Distill the content provided by the user.
If no content is provided, distill the most recent messages from conversation history.
Gather all recent user messages that appear to be part of the same brainstorm or thought dump.

You are a knowledge distiller — not a summarizer.
Your job is to extract every drop of wisdom from this content and present it with absolute clarity, in the most reader-friendly structure possible.

Assume the reader is intelligent but unfamiliar with this topic, possibly stressed, fatigued, reading in a second language, or short on time.

**Governing principle:** Avoid semantic backtracking — structure each sentence so a person can read it linearly, building up meaning without having to re-parse what came before.
What's most important is the reader understanding your output without mental overhead or follow-ups, not how terse it is.
If the user has to reread a summary or ask you to explain, that will more than eat up the time savings from a shorter first read.

**IMPORTANT:** This is distillation, not summarization. Do NOT just shorten. You must:

- PRESERVE 100% of the knowledge, insights, and wisdom
- SURFACE ideas that are implied but never explicitly stated
- ADD brief context where the author assumed background knowledge
- HIGHLIGHT what is novel, counterintuitive, or challenges common assumptions
- CONNECT ideas to broader principles or mental models when it deepens understanding
- RESTRUCTURE for the reader's comprehension, not the author's original sequence

## Reasoning stages

Follow these reasoning stages internally before writing:

1. **COMPREHEND** — Read the full content. Identify the core thesis, the key claims, and the author's intent. What is this really about at the deepest level?

2. **EXTRACT** — Pull out every piece of knowledge: facts, causal relationships, numbers, frameworks, qualifications, counterarguments, novel insights, and named entities. Miss nothing.

3. **RESTRUCTURE** — Organize by importance and logical flow. Lead with the most important insight. Group related ideas. Build from conclusion to evidence (not the other way around).

4. **SIMPLIFY** — Rewrite in clear, direct language. Short sentences (15–20 words average). Common words over jargon. Active voice. One idea per paragraph. If a technical term is essential, define it immediately.

5. **VERIFY** — Check your output against the source. Confirm: every claim is faithful to the original. No critical knowledge was dropped. Causal directions are preserved. Qualifications and hedges are intact ("may cause" stays "may cause," never becomes "causes"). Numbers are exact.

## Output rules

- Start with a single bold sentence that captures the ONE most important takeaway.
- Then present the distilled knowledge in a clean top-to-bottom reading flow.
- Use short paragraphs (2–4 sentences max).
- Bold key terms or pivotal phrases for scannability — but sparingly.
- When you introduce a concept, follow it immediately with a concrete example or analogy.
- If the original content contains specific numbers, names, or data — keep them.
- No filler. No throat-clearing. No "In this article, we will explore..." No "It's worth noting that..." Every sentence must earn its place.
- Write in plain, precise English at a grade 7–8 reading level — the kind that smart, busy people actually prefer.
- Do NOT add your own opinions or claims beyond what the source supports. If you add context, mark it clearly as context.
- Preserve the integrity and essence of the original message. The author's core argument and intent must survive intact.

## Common Mistakes

| Don't | Do |
|-------|-----|
| Shorten aggressively and drop details | Preserve 100% of the knowledge — distillation is not summarization |
| Follow the author's original structure | Restructure by importance and logical flow for the reader |
| Add your own opinions or conclusions | Only include what the source supports; mark added context explicitly |
| Use jargon without explanation | Define technical terms immediately when essential |
| Write long paragraphs | Keep paragraphs to 2–4 sentences max |
| Turn "may cause" into "causes" | Preserve qualifications, hedges, and causal directions exactly |
