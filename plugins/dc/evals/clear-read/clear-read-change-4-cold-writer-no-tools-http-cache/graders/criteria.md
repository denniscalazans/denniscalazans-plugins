---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. The writer does not stall on Phase 1 and does not silently skip it: the reply is written from memory and says so, with every number, version, date or default it could not check marked "(não verificado)" in the text (the Portuguese form of "(not verified)"), in particular the browser default freshness time.
2. The reply ends with one line naming the official source to check before acting (for example the RFC 9111 text on HTTP caching, or MDN's Cache-Control page), not a vague "consulte a documentação".
3. The reply opens with a 5-line block headed "Plano" that lists the main concepts, the terms to be defined, the two section headings, the visual verdicts and the arc from known to new. The block is short enough to skip and is not followed by any other exposed reasoning.
4. Every block passes the seven by-eye checks: no dash joining two ideas, no sentence over 25 words, no block over 4 sentences counting the bold opening, no "como vimos" or "acima" pointer, no bare label such as "ETag" at a block's first mention without its meaning, a "Como ler:" line after any visual, and an "Onde a analogia falha:" line after any analogy.
5. Every fixed label is in Portuguese ("Ponto-chave:", "O que funciona:", "Onde a analogia falha:", "Como ler:"), none in English, even though the language pack file was not available to read.
6. The method of the skill still shows: meaning before the term before the acronym for ETag, section 2 opens with "Você já sabe que X. Agora Y.", and each section ends with a "Ponto-chave:" line.

What the skill produced before this case existed, for context only, not a criterion: Phase 1 says "Do not skip this phase" and "Do not rely on memory", and Phase 2 says to keep the design "in your scratchpad", but neither says what to do when the tool or the scratchpad does not exist. In the Phase B cold-reader test (lacos.md, sections 2.2 and 5.2) a writer with the full skill and no tools either stalled on the research step or skipped it in silence, quoting the browser default and the ETag mechanics as checked facts with no "(não verificado)" mark and no source line, and ran no replacement for the lint, so blocks of 5 sentences and a backward pointer ("do bloco anterior") got through. The skill-minima file of the investigation gave the four substitutes and the by-eye checks, and the same writer then marked what it had not verified and kept the blocks within the limits.
