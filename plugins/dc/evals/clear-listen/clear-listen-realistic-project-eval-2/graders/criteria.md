---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. lint_audio_script.py prints 0 problems
2. The second host speaks within the first three lines
3. The second host voices the misconception that no-cache means do not store, and the first host corrects it
4. Deleting every line of the second host removes at least one question or misconception that matters
5. No line is banter, a joke, or a bare agreement ('Legal!', 'Exato!')
6. Only the requested concepts are covered, and no fact is added
7. Every study or author named is attributed who-before-what, with role and name woven into the sentence

What the skill produced before this case existed, for context only, not a criterion: Carried from the Project's eval set of 14 October 2026 (SET_VERSION 2026-10-14-r1): A two-host PT-BR script (Guia and Curioso). The Curioso asks a deep question before each explanation and voices the no-cache misconception, which the Guia corrects. No banter. The key sentence comes right after a voice change.
