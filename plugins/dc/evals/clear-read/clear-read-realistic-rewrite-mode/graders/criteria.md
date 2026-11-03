---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. No information from the original is dropped: the team, the sprint, the 40 percent, the local answer, the origin server
2. No claim is added that the original does not make
3. The result has no em dash and no sentence over 25 words
4. "conforme mencionado anteriormente" is gone, replaced by the thing itself or removed as a pointer
5. The 40 percent carries a word anchor ("quase metade")
6. The rewrite is in Portuguese and keeps "cache" and "round-trip" or explains them once in plain words
7. No web search contains any text of the paragraph (rewrite privacy)

What the skill produced before this case existed, for context only, not a criterion: The pre-Phase-E skill handled this well in most runs; the case guards against regressions in rewrite mode.
