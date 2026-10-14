# Language pack: Brazilian Portuguese (pt-BR)

Read this file when the reader's language is Portuguese.
It adds what is specific to Portuguese on top of the eleven rules in SKILL.md.
The lint keeps its own copy of these words in `LANG_PACKS["pt"]` in `scripts/lint_clear_read.py`. The two are maintained by hand, so when you change one, change the other.

## The legal basis

Brazil has a plain-language law: Lei 15.263, de 14 de novembro de 2025, the Política Nacional de Linguagem Simples.
Its article 5 lists the writing techniques.
The skill already carries most of them, so the table says where each one lives.

| Art. 5 of Lei 15.263 (the law's own words) | Where the skill carries it |
|---|---|
| I. redigir frases em ordem direta | Rule 2 (subject, verb, complement, in that order) |
| II. redigir frases curtas | Rule 2 (about 15 words, 25 as a ceiling) |
| III. desenvolver uma ideia por parágrafo | Rule 1 (one topic per block) |
| IV. usar palavras comuns, de fácil compreensão | Rule 10 (plain words of the reader's language) |
| V. usar sinônimos de termos técnicos e de jargões ou explicá-los no próprio texto | Rule 5 (plain meaning first, then the term) |
| VI. evitar palavras estrangeiras que não sejam de uso corrente | This file, "Which English words stay" |
| VIII. redigir o nome completo antes das siglas | Rule 5, and the lint rule `acronym-without-full-name` |
| IX. organizar o texto de forma esquemática, com listas, tabelas e recursos gráficos | Rule 7 (the visual plan) and Rule 11 (procedures) |
| X. as informações mais importantes aparecem primeiro | Rule 1 (lead with the goal at every level) |
| XII. redigir frases preferencialmente na voz ativa | Rule 2 (active voice, present tense) |
| XIII. evitar frases intercaladas | Rule 2, and the lint rule `inserted-clause` |
| XIV. evitar o uso de substantivos no lugar de verbos | Rule 2, and the lint rule `hidden-verb` |
| XV. evitar redundâncias e palavras desnecessárias | Rule 8 (cut empty words) |
| XVI. evitar palavras imprecisas | Rule 8 (name the real thing) |
| XVIII. testar com o público-alvo se a mensagem está compreensível | `references/tests.md` (the cold-reader tests) |

Source: [Lei 15.263/2025 at the Senado](https://legis.senado.leg.br/norma/41699861/publicacao/41699940).
Items VII, XI and XVII concern tone, gender inflection and accessibility for people with disabilities. They apply as written and need no rule of their own.

## Portuguese-specific rules

**Direct order, with nothing inserted.** Keep subject, verb and complement together.
A clause between commas in the middle of the sentence (a frase intercalada) pushes the subject away from its verb.
So move that clause to its own sentence.

- Weak: "O servidor, que a equipe instalou na semana passada, reinicia toda noite."
- Strong: "A equipe instalou o servidor na semana passada. Ele reinicia toda noite."

**A verb, not a noun made from a verb.** Nouns ending in -ção, -são, -mento, -agem, -ência and -ância often hide a verb.
Use the verb.

- Weak: "fazer a análise", "realizar a verificação", "tomar uma decisão", "chegar à conclusão", "a implementação da regra".
- Strong: "analisar", "verificar", "decidir", "concluir", "implementar a regra".

**Full name before the acronym, at its first use.** Even for a well-known one, unless it is an established tech term (API, URL, PDF).

- "transtorno do déficit de atenção com hiperatividade (TDAH)", then "TDAH" alone.

**Dates with the month in words.** "3 de junho de 2026", never "03/06/2026", because the numeric form reads two ways.

**Numbers with a word anchor.** Round when the exact value is not the point, and say what the number means.

- "7% (menos de 1 em cada 10)", "quase um terço", "1 em cada 5".
- Keep the exact value when it is the point: "32,7%" in a fact-check of that very number.
- Decimal comma, as the reader expects: "4,6", not "4.6".

**Register.** Address the reader as "você".
No "vós", no "tu" (it varies by region), and no "o leitor" in the third person.

**No travessão and no meia-risca as a joiner.** This is the same as Rule 2, and it matters more in Portuguese, because the travessão is common in edited prose.
Split the sentence, or use a comma, a connector or parentheses.

**Connectors that carry the logic out loud.** porque, então, por isso, no entanto, ou seja, como resultado, mesmo assim, em vez de.
Each sentence starts with what the reader already holds and ends with the new information.

**Negation.** Say what is, not what is not, whenever possible.

- Weak: "Não deixe de verificar o cache."
- Strong: "Verifique o cache."

## Which English words stay

The skill keeps established technical terms in English when the reader uses them that way at work (Rule 10).
In Brazilian software teams that covers API, deploy, token, cache, backend, frontend, framework, log and bug.
It also covers commit, branch, pull request, release, build, endpoint, feature, mock, prompt and dashboard.
Write them as they are, with no quotation marks and no italics.

Translate the rest.
A term with a current Portuguese word gets the Portuguese word.
Examples: "requisição" (request), "banco de dados" (database), "fila" (queue), "memória" (memory), "agendamento" (scheduling).

Give the plain meaning first, then the English term in parentheses, the first time: "uma cópia rápida dos dados (cache)".

## Markers the lint looks for, in Portuguese

| Marker | Portuguese form |
|---|---|
| The key-point line that closes a section | "Ponto-chave:" |
| The legend line under a visual | "Como ler:" |
| The line that limits an analogy | "Onde a analogia falha:" |
| A label with a number | "Passo 3", "Etapa 2", "Conceito 1" (each one followed by its name) |

## Common slips in Portuguese, and the fix

| Slip | Fix |
|---|---|
| "Como vimos acima", "o ponto mencionado", "a segunda ideia" | Name the thing again and say what it is |
| "O P1 resolve isso" | "O P1 (cache antes do deploy) resolve isso" |
| "A realização do teste é feita pelo time" | "O time testa" |
| "Foi decidido que" | "O time decidiu que", or "Decidimos que" |
| "Nível de abordagem estratégica" | Name the real thing: "o plano de três passos" |
| "crucial", "robusto", "fundamental" | Cut, or keep with the source that supports the judgment |
