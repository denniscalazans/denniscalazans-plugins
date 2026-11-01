# Handoff: investigação das skills clear-read e clear-listen

ESCRITO: 2026-11-01 15:00 (Berlim), pelo Claude, no fim de uma sessão de voz e texto com o Dennis.
BRANCH: `investigacao-2026-11` em `denniscalazans/denniscalazans-plugins`.
PARA: o agente que vai executar o trabalho no Claude Code, e o Dennis.

## 1. O que este branch contém

| Caminho | O que é | Estado |
|---|---|---|
| `plugins/dc/references/investigacao-2026-11/guia-de-investigacao.md` | A instrução de trabalho. Tudo começa por ela | Pronto. Lint da clear-read com 0 problemas. Leitor frio respondeu 8 de 8 |
| `plugins/dc/references/investigacao-2026-11/HANDOFF.md` | Este arquivo | Pronto |
| `plugins/dc/references/investigacao-2026-11/projeto/` | Cópias dos docs do Projeto "Clear Read the Web" (conjunto SET_VERSION 2026-10-14-r1) e do lint da Biblioteca | Cópias de 1 de novembro de 2026. Fonte da verdade continua no Projeto do claude.ai |
| `plugins/dc/skills/clear-listen/` | A skill clear-listen inteira: SKILL.md, references (research-basis, tests), scripts (lint) | Copiada de Settings > Skills do Dennis. Ainda não está no `plugin.json` nem no README |
| `plugins/dc/skills/clear-read/` | A skill clear-read 2.3.3 | Já estava em `main`. Sem mudança neste branch |

Arquivos em `projeto/`:

- `clear-read-web-project-instructions.md`: as instruções do Projeto, em inglês. É o produto que usa as skills.
- `clear-read-pesquisa-consolidada.md`: a pesquisa conferida na fonte sobre leitura, retenção e visuais (13 de outubro).
- `clear-read-audio-playbook.md`: o perfil de engine da ElevenLabs v4 e v3, que a clear-listen usa na fase 4.
- `clear-read-mcp-playbook.md`: os conectores do Projeto e como usá-los sem gastar tokens.
- `2026-10-13-revisao-na-biblioteca-design.md`: a spec da revisão espaçada, com o formato das perguntas.
- `clear-listen-evals.json`, `clear-listen-trigger-evals.json`, `clear-listen-eval-source-guia-cache-http.md`: os evals da clear-listen e o guia de exemplo que eles usam.
- `lint_guide.py`: o lint específico das páginas do Projeto (24 testes).

## 2. De onde isto veio, em cinco linhas

Em 1 de novembro de 2026, o Dennis conversou com o Claude por voz durante cerca de uma hora.
A conversa mostrou que as skills descrevem o leitor e não o processo do modelo.
Mostrou também que o modelo carrega reflexos de texto acadêmico mesmo com a skill carregada: nome solto, código, contagem antes do conteúdo.
E mostrou que a conversa por voz é um terceiro canal, que nenhuma das duas skills cobre.

O Dennis pediu um guia de investigação com prova, não respostas.
Ele pediu também que o que já funciona seja protegido por testes.
O guia é o resultado, e a seção 1 dele conta a história inteira.

## 3. Como começar

1. Fazer checkout deste branch.
2. Ler `guia-de-investigacao.md` inteiro. Ele não assume nada da conversa.
3. Começar pela Fase A (seção 5 do guia), no passo 1. O passo 0, trazer os arquivos para o repo, já está feito neste branch.
4. Trabalhar neste branch. Um commit por entrega de fase. Nunca fazer merge em `main` sem o Dennis.

Prompt sugerido para a primeira sessão no Claude Code:

```
Leia o arquivo plugins/dc/references/investigacao-2026-11/guia-de-investigacao.md inteiro antes de qualquer outra coisa. Ele é a instrução de trabalho desta investigação, e não assume nada de conversas anteriores.

Depois leia plugins/dc/references/investigacao-2026-11/HANDOFF.md, que diz o que já está feito.

Siga as regras de segurança da seção 4 do guia e comece pela Fase A (seção 5), a partir do passo 1. O passo 0 está feito neste branch.

Faça uma pergunta por vez, e só quando a resposta bloquear o trabalho. As perguntas que só eu respondo estão na seção 12 do guia. Antes de propor qualquer mudança nas skills, termine o inventário com um veredito por regra e o golden set, e rode os testes existentes para registrar o estado de partida.

Trabalhe neste mesmo branch, investigacao-2026-11. Um commit por entrega de fase, com mensagem curta em inglês. Não faça merge em main.
```

## 3.1 Estado em 1 de novembro de 2026, fim do dia: Fase A entregue

A Fase A está em `inventario-das-regras.md`, nesta pasta.
Ela tem o estado de partida dos testes e o veredito por regra das duas skills, em 75 linhas.
Ela confere os dez vereditos do guia, lista onze achados, e traz o golden set com 5 trechos.
Ela fecha com as 7 perguntas de revisão do guia de burnout.
O script `scripts/check_review_questions.py` confere as perguntas, e o `tests.md` da clear-read ganhou o Teste 18, que aponta para o golden set.

Os seis conectores de pesquisa (Valency, PubMed, Consensus, Exa, Tavily, Parallel Search) estão ligados no Claude Code.
Então a Fase C pode rodar aqui.
A próxima sessão começa pela Fase B (seção 6 do guia), a partir das colunas "Vale onde" e "Executável" do inventário.
Nenhuma pergunta ao Dennis bloqueou a Fase A, e a seção 9 do inventário diz quando cada uma chega.

## 4. O que já está decidido

- A clear-listen entra no plugin `dc`, ao lado da clear-read. O Dennis confirmou em 1 de novembro. Falta registrar no `plugin.json` e no README, e isso é um PR dele.
- As entregas ficam em `plugins/dc/references/investigacao-2026-11/`, porque o `.gitignore` do repo ignora `docs/` e `**/evals/`.
- A ordem das fases é A, B, C, E (proposta num branch), D (experimento sobre o branch), e só então o merge.
- Nenhuma mudança entra em skill sem um teste que falhe antes e passe depois, e com os testes antigos passando.

## 5. O que ainda está aberto

As perguntas que só o Dennis responde estão na seção 12 do guia. As que bloqueiam mais cedo:

1. Onde moram os evals: tirar `**/evals/` do `.gitignore`, ou usar outra pasta (pergunta 8).
2. Nomes novos para as seções "O chão" e "Para este guia ficar" (pergunta 1). Ele disse em 24 de outubro que os dois soam como português traduzido.
3. Se o modo conversa vira seção da clear-listen ou arquivo próprio (pergunta 2).

## 6. O que a sessão de 1 de novembro descobriu e ainda não entrou em lugar nenhum

- A ElevenLabs tem um repositório oficial de skills (`elevenlabs/skills`, MIT). A Fase C decide o que reaproveitar. Detalhe na seção 7.4 do guia.
- Na documentação da Anthropic, o corpo de uma skill deve ficar perto de 5 mil tokens. As duas skills passam disso (cerca de 7 mil e 8 mil). No Claude Code, depois de uma compactação, só os primeiros 5 mil tokens sobrevivem. Detalhe na seção 7.1 do guia.
- A literatura contradiz parte da tese sobre contagem antes do conteúdo. E não achou prova para "a troca de voz reseta a atenção" (clear-listen Regra 13). Detalhe na seção 7.2 do guia.

## 7. O que não está neste branch

- A Biblioteca (a base de conhecimento do Projeto). Ela é um artifact no claude.ai: https://claude.ai/artifact/DbeaArDSi7zaTTBQ2q2mAy. O agente no Claude Code não a alcança. O que ele precisar de lá, o Dennis exporta.
- Os guias publicados que o experimento usa. As URLs estão na seção 2.4 do guia.
- Os áudios gerados. Eles estão no ElevenLabs e na pasta "Clear Read" do Google Drive.
- O `check_mermaid.js` antigo do Projeto. A versão atual é `plugins/dc/skills/clear-read/scripts/check_mermaid.cjs`, que já está em `main`.

## 8. Como conferir que este handoff está íntegro

```
git log --oneline -3 origin/investigacao-2026-11
python3 plugins/dc/skills/clear-read/scripts/lint_clear_read.py --lang pt plugins/dc/references/investigacao-2026-11/guia-de-investigacao.md
python3 plugins/dc/skills/clear-read/scripts/test_lint_clear_read.py
python3 -c "import ast; ast.parse(open('plugins/dc/skills/clear-listen/scripts/lint_audio_script.py').read())"
```

O lint do guia deve imprimir `0 problems`.
Os testes do lint da clear-read devem passar.
