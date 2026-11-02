---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. Every fact in the script comes from the four sentences the user pasted; the script adds no fact about HTTP caching from memory (no header names, no default times, no browser behaviour that the text does not state).
2. The extra question about the default time is answered with 'a fonte não diz' or an equivalent, never with a number from memory.
3. The first producer note opens with 'facts not verified in this session' (or the same meaning in the producer's language).
4. No engine profile is invented: the reply hands the user the blank profile questions (or names references/rendering.md) and renders plain, with the intents turned into punctuation only, until a profile comes back.
5. One producer note lists the twelve checks done by hand (read aloud, over 20 words, parenthesis, digit or symbol, dash, backward pointer, filler, part marker, recall question per part, closing questions, part over 800 words, each main idea has its sentence) and says that the lint and the cold reader did not run.
6. The neutral script itself still follows the Phase 3 rules: 'Parte um de duas', one recall question per part, the closing 'Sem voltar' question.

What the skill produced before this case existed, for context only, not a criterion: Before change 4-listen the skill said 'If no verified source exists, run clear-read Phase 1 first' and nothing about what to do when no search exists. The model either skipped the research in silence and filled the default cache time from memory, or stopped and said it could not proceed. Without an engine profile it rendered from memory of one engine, and it reported the script as linted when no lint had run.
