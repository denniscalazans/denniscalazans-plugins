You are writing one guide for the Phase D experiment of the clear-read investigation. You are one arm of a blind comparison, so follow your skill exactly and do not improvise beyond it.

Your skill is the folder {SKILL_DIR}. Read its SKILL.md in full first, then every file in its references/ that SKILL.md tells you to read for a Portuguese text (the Portuguese language pack at least). Treat that SKILL.md as your operating instructions for this task: it decides the research behavior, the design, the writing rules and the checks.

Constraints that are the same for every arm:
- The reader is the one SKILL.md describes. The text is in Brazilian Portuguese.
- You have NO web access and must not use WebSearch or WebFetch. The only source is the file {SOURCE}. Read it in full. It holds the request, the idea map (use it as your main concepts, in that order) and the facts. If you need a fact that is not there, follow what your skill says about unverified facts; never invent a number, a name or a study.
- Output: Markdown, written to {OUT}. Headings with # and ##, paragraphs, lists, tables and ```mermaid fences are allowed; no HTML. Use the rendered-spacing rule your skill gives for Markdown (two trailing spaces to break lines inside a block) where it applies.
- Length: a complete guide of the whole idea map, about 1,400 to 2,000 words. Do not pad and do not cut concepts.
- Before you finish, run the lint your skill names on the output file, with the Portuguese language: python3 {SKILL_DIR}/scripts/lint_clear_read.py --lang pt {OUT}. Fix every problem it reports (not necessarily every warning) and run it again. Do not touch the lint script.
- Do not read, mention or compare with any other skill folder or any other arm's output. Do not read the investigation folder plugins/dc/references/investigacao-2026-11.

Your final answer: the lint's last line ("N problems"), the word count of the file, and one sentence on anything you could not do.
