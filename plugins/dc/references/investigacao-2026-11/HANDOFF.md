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

O script `scripts/check_review_questions.py` confere as perguntas.
O `tests.md` da clear-read ganhou o Teste 18, que aponta para o golden set.

Os seis conectores de pesquisa (Valency, PubMed, Consensus, Exa, Tavily, Parallel Search) estão ligados no Claude Code.
Então a Fase C pode rodar aqui.
A próxima sessão começa pela Fase B (seção 6 do guia), a partir das colunas "Vale onde" e "Executável" do inventário.
Nenhuma pergunta ao Dennis bloqueou a Fase A, e a seção 9 do inventário diz quando cada uma chega.

## 3.2 Estado em 1 de novembro de 2026, noite: Fase B entregue

A Fase B está em `lacos.md`, nesta pasta, com os dois rascunhos de skill mínima ao lado: `skill-minima-clear-read.md` e `skill-minima-clear-listen.md`.
Ela fixa os quatro perfis e dá o status de cada regra por perfil, com o fallback que a skill deveria dizer.
Ela lista o que atrapalha por canal e monta a matriz 4 por 4.

Ela traz também o teste de leitor frio das skills mínimas, em duas rodadas.
E fecha com a recomendação sobre onde mora o modo conversa, e um adendo de quatro linhas ao inventário.

O trabalho rodou como dois workflows de agentes: 33 na primeira rodada e 6 na segunda.
Os resultados brutos ficam fora do repo, no diretório da sessão.
A próxima sessão começa pela Fase C (seção 7 do guia), com os itens da seção 9 do inventário e da seção 8 de `lacos.md`.
Antes disso, o branch `investigacao-2026-11-adendo-1` entra por merge, e as seções 7.3 e 7.4 do guia recebem o que o adendo pede.

## 3.3 Estado em 1 de novembro de 2026, madrugada: Fase C entregue

A Fase C está em `pesquisa-conferida.md`, nesta pasta.
Ela confere na fonte cada estudo que as duas skills citam, por tema, e diz o que ficou de pé e o que caiu.
Ela traz as buscas novas (contagem, rótulos, troca de voz, narrativa, instrução literal) e as skills e normas que já existem.
Ela fecha com as mudanças que o inventário ganha e com as correções de citação, que já entraram no guia (seção 13.2).

O adendo 1 entrou por merge, e as seções 7.3 e 7.4 do guia receberam o que ele pedia.
O questionário com o Dennis rodou no mesmo dia, e as respostas estão em `decisoes-do-dennis.md`.

## 3.4 Estado em 1 de novembro de 2026, madrugada: Fase E, o plano

O plano da Fase E está em `proposta.md`, nesta pasta: 16 mudanças, em três prioridades.
Cada mudança tem o que muda, o teste que falha hoje, e a evidência das Fases A, B e C.
O Dennis aprova por item.
A implementação roda no branch filho `investigacao-2026-11-fase-e`, um commit por mudança.

A próxima sessão começa pela aprovação do plano.
Depois, implementa na ordem da seção 4 de `proposta.md`, com os testes primeiro.
A Fase D (seção 8 do guia) vira um artefato interativo, e a seção 3 de `decisoes-do-dennis.md` diz como.

## 3.5 Estado em 1 de novembro de 2026, noite: Fase E implementada

As 15 mudanças aprovadas, mais as mudanças 17 e 18 e dois commits de tamanho, estão no branch `investigacao-2026-11-fase-e`.
A seção 6 de `proposta.md` lista o que entrou e os desvios.
Os dois corpos de skill têm agora um teste de tamanho com a meta de 3.600 palavras registrada e o teto real.

Os testes rodam assim, da raiz do repo: `python3 plugins/dc/skills/clear-read/scripts/test_lint_clear_read.py`, `python3 plugins/dc/skills/clear-listen/scripts/test_lint_audio_script.py`, e `node plugins/dc/skills/clear-read/scripts/check_mermaid.cjs --self-test`.
Os evals rodam com `claude plugin eval plugins/dc --runs 1 --case "<id>"`, e custam créditos do Dennis.

A próxima sessão começa pela revisão do PR do branch filho e pela Fase D: a página do experimento, com 2 pares de guia primeiro.
A seção 3 de `decisoes-do-dennis.md` diz como a página coleta respostas.

## 3.6 Estado em 1 de novembro de 2026, noite: Fase D, parte 1

As medidas automáticas e o leitor frio artificial estão em `experimento.md` e na pasta `experimento/`.
Os quatro textos têm nomes cegos, e o mapa está selado no banco da página privada e fora do repo.
A leitura cega está aberta em duas páginas, listadas na seção 4 de `experimento.md`.

A próxima sessão lê as respostas pela ferramenta de dados do artefato, abre o mapa, e escreve a seção 7 de `experimento.md`.
Só depois disso o PR #81 pode entrar no main.

## 3.7 Estado em 2 de novembro de 2026: adendo 2 incorporado

O adendo 2 (`adendos/2026-11-01-visuais-e-regras-do-projeto.md`) entrou por merge nos dois branches.
A proposta ganhou a mudança 20 (Regra 7, nunca desenhar uma sequência) e a mudança 21 (as regras do Projeto que são método).
As duas esperam a aprovação do Dennis.
A seção 7 da proposta dá o veredito das 14 regras, e a linha R7c do inventário mudou para "muda".

## 4. O que já está decidido

- A clear-listen entra no plugin `dc`, ao lado da clear-read. O Dennis confirmou em 1 de novembro, e ela já está no `plugin.json`, no README e no CLAUDE.md.
- As dez perguntas da seção 12 do guia estão respondidas em `decisoes-do-dennis.md`. Evals em `tests/evals/` dentro da skill. Voz na clear-listen e texto na clear-read. "O que saber antes de ler" e "Exercícios de fixação" como nomes das seções.
- As entregas ficam em `plugins/dc/references/investigacao-2026-11/`, porque o `.gitignore` do repo ignora `docs/` e `**/evals/`.
- A ordem das fases é A, B, C, E (proposta num branch), D (experimento sobre o branch), e só então o merge.
- Nenhuma mudança entra em skill sem um teste que falhe antes e passe depois, e com os testes antigos passando.

## 5. O que ainda está aberto

As perguntas da seção 12 do guia estão respondidas. O que ainda está aberto:

1. A aprovação do plano da Fase E, item a item (`proposta.md`, seção 5).
2. Os dois roteiros neutros (suplementos e burnout) que o Dennis vai colar, para o golden set da clear-listen.
3. Se a contagem antes do conteúdo trava ou ajuda: o Dennis quer sentir no experimento (pergunta 6).

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
