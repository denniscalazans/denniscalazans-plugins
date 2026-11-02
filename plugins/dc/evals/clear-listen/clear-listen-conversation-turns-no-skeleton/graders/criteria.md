---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. Each of the five answers is a short prose turn: no part marker such as "Parte um de cinco" or "Part 1 of 5".
2. No square brackets anywhere in the five answers: no [pause short], no [warm], no [key], no [1].
3. No bare ordinal: no sentence starts with "Primeiro,", "Segundo,", "Em primeiro lugar,", "First," or "Second,".
4. No numbered or bulleted list line, no heading, no bold: the procedure of question 4 is given one step per turn, with the offer of the next step.
5. Each turn has at most 6 sentences, and the first sentence is the answer itself.
6. A turn of more than 3 sentences ends with a short question that gives the turn back, and no pause mark follows it.
7. Each turn starts from the words of the question ("Você perguntou se o no-cache manda não guardar. Não manda."), and any study or author is named by role and then by name, never as a bare "um pesquisador".
8. Every answer passes python3 scripts/lint_audio_script.py <turn.txt> --conversa.

What the skill produced before this case existed, for context only, not a criterion: Before change 5 the skill had no section for a live turn, so the model applied the recorded-audio rules to the conversation: answers opened with "Parte um de cinco", carried delivery intents in square brackets ([warm], [pause recall]) that the engine read aloud or dropped, announced "São três motivos" and marked items with "Primeiro,", "Segundo,", and gave the procedure of question 4 as a numbered list. Several turns ran past six sentences and ended on a recall pause that sounded like the end of the turn.
