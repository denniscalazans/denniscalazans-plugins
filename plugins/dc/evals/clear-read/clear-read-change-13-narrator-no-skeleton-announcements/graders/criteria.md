---
type: llm
weight: 1
---

Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.

1. With the paragraphs present, the judge counts zero structure announcements: the reply never says how many causes there are, never numbers them in prose ("primeira causa", "em segundo lugar"), and never previews its own sections ("a seguir veremos", "nesta seção"). Headings, bold openings and the "Ponto-chave:" lines may still organize the text; the prose does not describe them.
2. With the paragraphs removed, the judge counts at least one structure announcement in at least one of three runs, so the two runs differ in the judged count.
3. Each cause is delivered complete before the next one starts: no cause is opened, parked with a promise ("voltaremos a isso"), and finished later.
4. Each transition pulls the reader forward with the next concrete thing, not with a promise about the text: for example "A cópia da configuração ficou no servidor de teste. Em produção, ela não existe." rather than "Vamos agora ao segundo motivo".
5. When the reply repeats an essential idea, it restates the thing and its meaning as someone recalling together ("a variável que só o servidor de teste tinha"), never as a backward pointer ("como vimos", "acima", "o primeiro motivo").
6. The mechanism the prompt asks for (a missing environment variable becoming an error only in production) still comes as explicit steps, in order, each step named: the code reads the variable, gets nothing, uses a default or fails, and the failure appears only where the variable is missing. The story does not replace these steps.
7. Every label is in Portuguese ("Ponto-chave:", "Onde a analogia falha:"), none in English.
8. The reply does not mention the narrator paragraph, the meta-analysis, or any reasoning about how it chose to structure the text. The design stays in the scratchpad.

What the skill produced before this case existed, for context only, not a criterion: Expected from the skill text; this eval has not been run here. The current section "Who you are writing for" describes only the reader and says nothing about who writes. Rule 1 asks for headings, numbered steps and "Key point:" lines, and Phase 2 asks for a narrative arc, so the model has structure as a value and no instruction to keep the structure under the prose. A prompt that hands it four causes comes out with the skeleton announced: an opening such as "Existem quatro causas principais", causes introduced as "Primeira:", "Em segundo lugar", and transitions such as "Vamos agora ao último motivo". Finding 4 of the conversation with Dennis (the basis of change 13 in proposta.md) named this pattern: the text reads like an outline being read aloud, not like someone telling a friend what happened. The limit is also missing: without the Mar, Li, Nguyen and Ta (2021) finding that narrative helps memory more than comprehension, a run that does adopt a story voice may tell the environment-variable failure as an anecdote and skip the step by step the prompt asks for.
