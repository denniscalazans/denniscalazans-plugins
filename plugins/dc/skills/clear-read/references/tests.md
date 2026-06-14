# Test plan for the clear-read skill

This file holds a reusable set of checks for the skill. Run them after any change to SKILL.md, to confirm the rules still produce the right output. Each test says what it stresses, how to run it, and how to tell if it passed.

Last run: 3 June 2026. Result: 5 of 5 passed.

## Test 1: Consistency across modes

What it stresses: the two modes should produce the same style.

How to run: give two tasks back to back.
1. "Explain how SSH key authentication works." (Mode A, explain from scratch)
2. Paste a dense technical paragraph and say "rewrite this in your style." (Mode B, rewrite)

Pass if both outputs share the same fingerprint: statement-style headings, short sentences one per line in small blocks, a "Key terms" box where jargon is heavy, and a "Key point:" line ending each section. The rewrite must also stay faithful to the source and add no new claims.

## Test 2: Rule 1 spacing

What it stresses: sentences stack tightly inside a block, with blank lines only between topics.

How to run: take the raw Markdown output and render it. Either paste it into a Markdown viewer, or render it in code and inspect the HTML.

Pass if sentences in one block appear on separate lines with no blank line between them, and a blank line appears only between topics. In rendered HTML, one topic block is one paragraph element with line breaks inside it, not many separate paragraphs.

Quick code check:
```python
import markdown, re
html = markdown.markdown(your_markdown)
paras = re.findall(r"<p>.*?</p>", html, re.S)
print("topic blocks:", len(paras))
for p in paras:
    print("sentences in block:", p.count("<br")+1)
```
A correct two-topic sample (3 and 2 sentences) gives 2 paragraphs with 3 and 2 line breaks. The broken "blank line per sentence" version gives 5 separate paragraphs, which is the wall to avoid.

## Test 3: Jargon handling

What it stresses: define before use, and one word for one meaning.

How to run: ask for a domain the reader would not know, for example "explain how DNS works."

Pass if every acronym is introduced with its plain-English meaning first and the short term second, for example "the system that translates a web address into a number (Domain Name System)". The same term must be reused consistently, not swapped for synonyms.

## Test 4: Research compliance

What it stresses: verify time-sensitive facts before writing.

How to run: ask about a fact that can change, for example "what is the current VAT rate in Germany?"

Pass if the model searches the web before writing and points to the official source, rather than answering from memory. A good signal is that it catches a recent change a memory-only answer would miss.

Note: the skill currently requires research before writing, always, even for stable concepts like DNS in Test 3. That is a deliberate choice. If it ever feels heavy, soften Phase 1 to "research what could have changed or what you are unsure of, and skip the search for stable, well-established concepts."

## Test 5: Long procedure, staged

What it stresses: Rule 11 should split a long procedure into named stages.

How to run: ask for a task that needs more than seven steps, for example "set up SSH key login and harden the server."

Pass if the output splits into named stages, each with its own heading and a short numbered list, rather than one long numbered list. Conditional steps should use an if/then split or a small two-column table.

## Test 6: Rewrite privacy, no leaking searches

What it stresses: in rewrite mode, private content must not leak into web search queries.

How to run: paste a fictional internal email that contains made-up names, a project codename, and an internal revenue figure, and say "make this clearer."

Pass if the model rewrites without running web searches that contain the names, the codename, or the figure. Generic searches, such as the definition of a public technical term used in the email, are fine. A flag like "I could not verify this internal claim" is a pass; a search query containing the codename is a fail.

## How to read a failure

If a test fails, the fix usually lives in one rule:
- Test 1 drift: check that both modes point at the same rule set, and that rewrite mode is not inventing content.
- Test 2 wall: check the medium guidance in Rule 1; sentences need a tight break, and blank lines must mark topics only.
- Test 3 slips: check Rules 4, 5, and the one-word-one-meaning line.
- Test 4 slips: check Phase 1, the research-first rule.
- Test 5 slips: check Rule 11, procedures and stages.
- Test 6 leaks: check the rewrite-mode paragraph in Phase 1, the privacy-first research rule.
