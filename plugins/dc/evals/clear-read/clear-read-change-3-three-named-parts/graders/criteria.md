---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. Sections 2 and 3 each open with the re-entry template with both slots filled, "Você já sabe que X. Agora Y.", where X is one thing from the earlier section with its meaning and Y is what this section adds.
2. No sentence points back with a bare pointer: no "como vimos", "como dito acima", "na seção anterior", "o primeiro" or "o segundo" standing in for the thing itself. When the text refers back, it repeats the thing and its meaning.
3. The first mention of ETag, cópia and no-cache in each block carries its meaning in the same sentence (Tier 1). A bare label at a block's first mention, such as "o ETag resolve isso", does not appear.
4. Each sentence starts with what the reader already holds and ends with the new information (known before new). No section opens on a term the reader has not met yet.
5. Every label is in Portuguese ("Ponto-chave:", "Onde a analogia falha:"), none in English.
6. Each of the three sections can be read on its own by a cold reader: a reader who reads only section 3 can answer "o que no-cache faz?" from that section alone.
7. The reply does not contain the two design questions ("what does the reader already have that I can use?", "what am I leaving open?") or any reasoning about them. The design stays in the scratchpad.

What the skill produced before this case existed, for context only, not a criterion: In at least one of three runs, the current skill produces a bare label at a block's first mention ("o ETag" or "a cópia" with no meaning restated in that block) or a backward reference to what already passed ("como vimos na seção 1", "a etiqueta acima"). Section 2 or 3 opens without the re-entry line, because Rule 6 states the principle ("its first line says in one clause what it builds on") with one English example and no literal template to fill, and the model treats it as a principle to honor rather than a line to produce. Phase B (lacos.md, section 5.2) saw the same rule execute without reasoning once the skill gave the literal string, and fail to execute with the full skill.
