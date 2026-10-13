# Test plan for the clear-read skill

This file holds a reusable set of checks for the skill. Run them after any change to SKILL.md, to confirm the rules still produce the right output. Each test says what it stresses, how to run it, and how to tell if it passed.

Last run: 3 June 2026. Result: 5 of 5 passed.
Tests 7 to 9 were added on 13 October 2026 and have not been run with the model yet. Tests 10 to 12 (the lint, in English and in Portuguese) passed on that date.

## Test 1: Consistency across modes

What it stresses: the two modes should produce the same style.

How to run: give two tasks back to back.
1. "Explain how SSH key authentication works." (Mode A, explain from scratch)
2. Paste a dense technical paragraph and say "rewrite this in your style." (Mode B, rewrite)

Pass if both outputs share the same fingerprint: statement-style headings, short sentences one per line in small blocks, a "Key terms" box where jargon is heavy, and a "Key point:" line ending each section. The rewrite must also stay faithful to the source and add no new claims.

## Test 2: Rule 1 spacing

What it stresses: sentences stack tightly inside a block, with blank lines only between topics.

How to run: take the raw Markdown output and render it. Either paste it into a Markdown viewer, or render it in code and inspect the HTML.

Pass if sentences in one block appear on separate lines with no blank line between them, and a blank line appears only between topics. In rendered HTML, one topic block is one paragraph element with line breaks inside it, not many separate paragraphs.

Quick code check:
```python
import markdown, re
html = markdown.markdown(your_markdown)
paras = re.findall(r"<p>.*?</p>", html, re.S)
print("topic blocks:", len(paras))
for p in paras:
    print("sentences in block:", p.count("<br")+1)
```
A correct two-topic sample (3 and 2 sentences) gives 2 paragraphs with 3 and 2 line breaks. The broken "blank line per sentence" version gives 5 separate paragraphs, which is the wall to avoid.

## Test 3: Jargon handling

What it stresses: define before use, and one word for one meaning.

How to run: ask for a domain the reader would not know, for example "explain how DNS works."

Pass if every acronym is introduced with its plain meaning first, in the reader's language, and the short term second. For example "the system that translates a web address into a number (Domain Name System)", or in Portuguese "o sistema que traduz um endereço da web em um número (Domain Name System)". The same term must be reused consistently, not swapped for synonyms.

## Test 4: Research compliance

What it stresses: verify time-sensitive facts before writing.

How to run: ask about a fact that can change, for example "what is the current VAT rate in Germany?"

Pass if the model searches the web before writing and points to the official source, rather than answering from memory. A good signal is that it catches a recent change a memory-only answer would miss.

Note: the skill currently requires research before writing, always, even for stable concepts like DNS in Test 3. That is a deliberate choice. If it ever feels heavy, soften Phase 1 to "research what could have changed or what you are unsure of, and skip the search for stable, well-established concepts."

## Test 5: Long procedure, staged

What it stresses: Rule 11 should split a long procedure into named stages.

How to run: ask for a task that needs more than seven steps, for example "set up SSH key login and harden the server."

Pass if the output splits into named stages, each with its own heading and a short numbered list, rather than one long numbered list. Conditional steps should use an if/then split or a small two-column table.

## Test 6: Rewrite privacy, no leaking searches

What it stresses: in rewrite mode, private content must not leak into web search queries.

How to run: paste a fictional internal email that contains made-up names, a project codename, and an internal revenue figure, and say "make this clearer."

Pass if the model rewrites without running web searches that contain the names, the codename, or the figure. Generic searches, such as the definition of a public technical term used in the email, are fine. A flag like "I could not verify this internal claim" is a pass; a search query containing the codename is a fail.

## Test 7: Visual plan, a fundamental visual

What it stresses: Rule 7 (the visual plan) should produce a visual when the four-question test says "fundamental". The visual must come with its two lines.

How to run: ask for an explanation of how a request moves through a reverse proxy, a load balancer, three app servers, and a shared cache. Ask it to include what happens on a cache miss.

Why it should score 3 or 4:
- The idea has more than 3 elements the reader holds together: yes.
- The central question is about a path: yes.
- The relation takes more than 4 sentences in prose: yes.
- A cold reader with only the text would likely get a question about the path wrong, for example "which component does a miss reach first?": yes.

Pass if the output contains one small diagram or numbered outline of the path. Right after it, a line must start with "How to read:", and one sentence of conclusion must state what the visual shows. The prose around it must still carry the whole path, so a reader who skips the visual loses nothing. Fail if the diagram repeats the prose node for node, has no "How to read" line, or is decorative.

## Test 8: Visual plan, no visual

What it stresses: Rule 7 should keep a visual out when the four-question test scores 0.

How to run: ask "explain what an idempotent HTTP method is."

Why it should score 0:
- The idea has one element, a property of a method: no.
- The central question is a definition, not structure, comparison, magnitude or a path: no.
- The relation fits in 2 or 3 sentences and one example: no.
- A cold reader with only the text answers a question about it correctly: no.

Pass if the output has no diagram, chart or image, and explains the concept with a definition, one concrete example, and one counter-example. Fail if a diagram appears for a single-element concept. A scoring of 1 or 2 with a cheap outline is acceptable only if the output says what the outline adds.

## Test 9: Active voice and present tense

What it stresses: Rule 2 should default to active voice and present tense, and keep a passive only under one of the three named exceptions.

How to run: paste this paragraph and say "rewrite this in your style":

"The configuration file is loaded by the server at startup. Changes are picked up only after a restart has been performed by the operator. In 2024 the default location was changed by the maintainers. The key was leaked, so all tokens were rotated."

Pass if the rewrite meets three conditions:
- The first two sentences become active: "the server loads the configuration file at startup", and "the operator restarts the server, and then the server picks up the changes".
- The 2024 sentence keeps the past tense, because it is a past event.
- "The key was leaked" may stay passive, because the agent is unknown.

Running the lint on the rewrite (Test 10) should show at most the passives that fall under an exception.

## Test 10: The lint

What it stresses: `scripts/lint_clear_read.py` catches the rule breaks that are easy to make and hard to see.

How to run, from the skill folder:
```bash
python3 scripts/test_lint_clear_read.py
python3 scripts/lint_clear_read.py path/to/output.md
```

Pass if the unit tests print `OK`, and if a lint run on a finished clear-read output ends with `0 problems`. Warnings are allowed when each one is a deliberate choice (a passive under an exception, for example).

A quick manual check: write a paragraph with an em dash, a 30-word sentence and a pointer back to the previous section into a file. Run the lint on it. It must report all three and exit with code 1.

## Test 11: Portuguese, dirty sample

What it stresses: the rules and the lint work on Brazilian Portuguese the same way they work on English. The lint must detect the language on its own.

How to run: save this text in a file with no `--lang` flag, and run the lint on it.

```
## Contexto

Como vimos na seção anterior, o cache fica entre o aplicativo e o banco de dados.
O Passo 2 resolve o problema da leitura antiga, porque a cópia expira antes de a fonte mudar de novo.
A chave foi trocada pelo operador ontem à noite, por isso todos os processos recarregaram a configuração de manhã.
O arquivo de configuração é carregado pelo servidor na inicialização, o que significa que toda mudança no arquivo obriga a reiniciar o serviço inteiro e todos os seus processos, p. ex. os de fila.
```

Pass if the lint reports, as problems: the backward references ("como vimos", "a seção anterior"), the bare label "Passo 2", and the sentence over 25 words (the one with "p. ex.", which must count as one sentence, not two). As warnings: the two passives ("foi trocada pelo", "é carregado pelo"), the one-word heading "Contexto", and the missing "Ponto-chave:" line. The summary must say the detected language is pt.

The rewrite that passes: "O cache fica entre o aplicativo e o banco de dados. O Passo 2 (cache antes do deploy) resolve a leitura antiga, porque a cópia expira antes de a fonte mudar. O operador trocou a chave ontem à noite. Por isso, todos os processos recarregaram a configuração de manhã. O servidor carrega o arquivo de configuração na inicialização. Então, toda mudança no arquivo obriga a reiniciar o serviço inteiro. Ponto-chave: o servidor só lê a configuração ao iniciar."

## Test 12: Portuguese, clean sample

What it stresses: a clean Portuguese guide passes the lint with 0 problems and 0 warnings, so the language packs do not produce false positives on correct Portuguese.

How to run: save this text in a file and run the lint on it.

```
# Como um cache de leitura protege o banco de dados

Este guia explica como um cache de leitura funciona e por que ele protege o banco de dados.\
Ele importa agora porque o novo serviço dobra o volume de leituras.

## O cache responde primeiro, então o banco descansa

Um cache de leitura é um depósito rápido que fica na frente do banco de dados.\
Quando o aplicativo pede um valor, o cache responde se tiver esse valor.\
Caso contrário, o cache busca o valor no banco e guarda uma cópia.

Ponto-chave: o cache responde à maioria das leituras, então o banco só vê as faltas.

## A leitura antiga acontece quando a cópia é mais velha que a fonte

A cópia no cache pode ficar atrás do banco de dados.\
A solução é um prazo de validade para cada cópia (um tempo de vida, ou TTL).\
O P1 (cache antes do deploy) aquece o cache, então os primeiros usuários não veem leituras lentas.

Ponto-chave: um TTL curto mantém a cópia fresca, e o P1 (cache antes do deploy) esconde o aquecimento.
```

Pass if the lint ends with `0 problems` and prints no warnings. Note that "é mais velha" and "é um depósito" are not passives (no participle follows), and "P1 (cache antes do deploy)" is a named label.

## How to read a failure

If a test fails, the fix usually lives in one rule:
- Test 1 drift: check that both modes point at the same rule set, and that rewrite mode is not inventing content.
- Test 2 wall: check the medium guidance in Rule 1; sentences need a tight break, and blank lines must mark topics only.
- Test 3 slips: check Rules 4, 5, and the one-word-one-meaning line.
- Test 4 slips: check Phase 1, the research-first rule.
- Test 5 slips: check Rule 11, procedures and stages.
- Test 6 leaks: check the rewrite-mode paragraph in Phase 1, the privacy-first research rule.
- Test 7 or 8 slips: check Rule 7, the four-question test and its thresholds, and the Phase 2 visual plan item.
- Test 9 slips: check the active voice paragraph in Rule 2 and its three exceptions.
- Test 10 slips: a failing unit test means the lint changed; a false positive on real output means a heuristic in the lint needs a documented exclusion, not a loosened rule.
- Test 11 or 12 slips: check the `pt` entry of `LANG_PACKS` in the lint (word lists, abbreviations, passive forms), or the language detection when the summary names the wrong language. A new language is one more entry in that dict.
