---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. lint_audio_script.py prints 0 problems
2. The core idea of the guide is stated within the first 80 words
3. Each part starts with 'Parte N de M' written in words, followed by a re-entry line that names what the part builds on
4. Every part ends with exactly one recall question followed by its answer
5. No header syntax is read literally (no 'max-age=31536000', no 'If-None-Match' spelled as code)
6. Every factual claim in the script is in the source guide, and all three main concepts are present
7. At least one dense element of the guide (the response table or the file name with a hash) is spoken as plain explanation or pointed to the written guide
8. Every study or author named is attributed who-before-what, with role and name woven into the sentence

What the skill produced before this case existed, for context only, not a criterion: Carried from the Project's eval set of 14 October 2026 (SET_VERSION 2026-10-14-r1): A PT-BR narration script for one voice, written for the ear from the guide: spoken map, core idea in the first 30 seconds, one part per main concept with a re-entry line, a recall question closing each part, no tables, code, digits, URLs or parentheses, and the response table and header syntax replaced by plain spoken explanation.
