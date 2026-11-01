---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. Reads references/rendering.md (the Phase 4 method) before rendering, and reads the engine profile named in the request.
2. Keeps the neutral script untouched and writes the rendered text to a second file named after the medium (for example guia-audio-render-eleven-v3.txt).
3. Maps every delivery intent with the profile, or degrades it down the ladder, and leaves no neutral intent ([pause, [key], [stress, [say) in the rendered text.
4. Writes the render report (mapped, degraded, dropped) as producer notes at the top of the rendered file, and tells the user in one line what was degraded or dropped.
5. Runs scripts/check_render.py on the rendered text before generating.
6. Repeats the tone at the start of each generation call, and never retries a charged call by calling it again.

What the skill produced before this case existed, for context only, not a criterion: Before change 6 the method was inline in SKILL.md, so the model rendered from the body. The risk after the move is a model that skips references/rendering.md and renders from memory of the engine: neutral intents left in the text, no render report, no second file.
