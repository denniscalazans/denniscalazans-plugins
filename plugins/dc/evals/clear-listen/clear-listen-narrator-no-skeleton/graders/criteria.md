---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. Judge count: the script has zero announcements of structure. No 'são dois motivos', no 'são três passos', no 'vou falar de duas coisas', no 'primeiro,' / 'segundo,' / 'em primeiro lugar'. The turns arrive through content ('Agora, o que o navegador faz antes de usar a cópia.').
2. Delivers the whole thing: every fact of the six source sentences is in the script, and nothing is held back with 'depois eu explico' or 'isso fica para outro áudio'.
3. Pulls the listener forward with what comes next: at least one sentence opens the next part of the story as a hook or a question ('E se o servidor nunca mandou etiqueta?').
4. Repeats the essential as two people remembering together ('lembra que o navegador guarda uma cópia?'), never with a backward pointer ('como eu disse', 'o que falei antes').
5. The limit of the narrator holds: the mechanism (what the browser does before using the copy) is given step by step, in the order it happens, one step per sentence, each link said with 'por isso' or 'porque'. It is not compressed into an image or an anecdote alone.
6. One part only, so no 'Parte um de um' line (Rule 1); the script still opens with the core idea and closes with the takeaway.
7. The script passes python3 scripts/lint_audio_script.py <script.md>.

What the skill produced before this case existed, for context only, not a criterion: Without the narrator paragraph the model applies Rule 3 as a reflex: 'São dois motivos. O primeiro...', 'Agora, o segundo', and opens with 'Neste áudio, duas coisas', so the listener holds an announced skeleton for a one-minute recap. Or, told to narrate, it tells the story of the stale page in one image and drops the step by step of the version check, so the listener remembers the anecdote and cannot say what the browser does before using the copy.
