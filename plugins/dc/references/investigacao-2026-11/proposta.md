# Fase E: a proposta de mudança, com prioridade, teste e evidência

CRIADO: 2026-11-01 (Berlim), no Claude Code.
FASE: E, do guia `guia-de-investigacao.md` (seção 9).
STATUS: plano para o Dennis aprovar.
A implementação roda no branch `investigacao-2026-11-fase-e`, um commit por mudança.

## 0. O que este arquivo é

A regra 8 da seção 4 do guia diz: o Dennis aprova o plano, não cada linha.
Este arquivo é o plano.
Cada mudança tem um número, uma prioridade e o que muda.
Cada uma tem também o teste que falha antes e passa depois, e a evidência das Fases A, B e C.

A implementação acontece num branch filho, `investigacao-2026-11-fase-e`, com um commit por mudança.
Assim o Dennis pode tirar uma mudança sem desfazer as outras.
O que ele aprovar entra em `investigacao-2026-11`, e a Fase D roda sobre esse resultado.

As cinco regras de segurança continuam valendo.
Os testes antigos passam antes e depois de cada commit.
São 98 testes do lint da clear-read, o self-test do Mermaid, e os 5 trechos do golden set.
Nenhuma regra se apaga; o que cai vira `retired` com nota.

Ponto-chave: 19 mudanças planejadas e 2 à espera de aprovação, cada uma com um teste que falha hoje; a seção 6 diz o que entrou.

## 1. As prioridades

As prioridades são três, e cada uma diz quando a mudança entra.

- **P1 (antes do experimento).** São as mudanças que a Fase D testa, ou de que ela depende.
- **P2 (junto, sem depender do experimento).** Correções de evidência e de citação, e os testes que faltam.
- **P3 (depois da Fase D).** O que depende do experimento ou de uma pergunta aberta.

| Nº | Mudança | Skill | Prioridade |
|---|---|---|---|
| 1 | Rótulos na língua do leitor, e dois testes de lint | clear-read | P1 |
| 2 | Papel antes do nome, e o nome logo depois: a Regra 5 estendida, e dois avisos de lint | clear-read | P1 |
| 3 | "Conhecido antes do novo" com template, e a etapa "ler como o leitor" | clear-read | P1 |
| 4 | A seção "Sem raciocínio e sem ferramentas" | clear-read e clear-listen | P1 |
| 5 | A seção "Conversa por voz" no topo da clear-listen | clear-listen | P1 |
| 6 | A renderização por motor vai para `references/` | clear-listen | P1 |
| 7 | Regra 13b reescrita: a troca de voz custa 3 segundos | clear-listen | P1 |
| 8 | Regra 15: a frase da revisão reescrita | clear-listen | P2 |
| 9 | Regra 6: a pergunta de fechamento é a parte provada | clear-listen | P2 |
| 10 | Testes unitários para o lint de áudio, e quatro checagens novas | clear-listen | P2 |
| 11 | O mapa de evidência conferido nos dois `research-basis.md` | clear-read e clear-listen | P2 |
| 12 | A ISO 24495-1 nos pacotes de língua e na Regra 10 | clear-read | P2 |
| 13 | O parágrafo do narrador, com o limite | clear-read e clear-listen | P2 |
| 14 | Regra 9 (tom) e Regra 8b (calibrar) com exemplo | clear-read | P2 |
| 15 | Evals em `tests/evals/`, com e sem a skill | clear-read e clear-listen | P2 |
| 16 | Regra 3 da clear-listen: a prévia que nomeia o tópico | clear-listen | P3, depois da Fase D |
| 17 | Atribuição no fio, como a BBC: papel, nome e instituição na frase, nunca em nota solta | clear-read e clear-listen | P1 |
| 20 | Regra 7: nunca desenhar uma sequência, SVG inline para grafos, a tabela de forma por conteúdo (o adendo 2 a chamou de mudança 18) | clear-read | P2, aprovada e feita |
| 21 | As dez regras do Projeto que são método e não estão na skill (seção 7) | clear-read | P2, aprovada e feita |

Fora das skills, mas na proposta: os nomes das seções do Projeto (seção 3) e a correção das instruções sobre o Projeto rodar o lint.

Ponto-chave: sete mudanças entram antes do experimento, oito entram junto, e uma espera.

## 2. As mudanças, uma a uma

Cada mudança abaixo tem três blocos: o que muda, o teste que falha hoje, e a evidência.

### 1. Rótulos na língua do leitor (P1: antes do experimento)

**O que muda.** A clear-read ganha, na Regra 10, a lista dos cinco rótulos fixos nas duas línguas.
E uma frase: um rótulo na língua errada é uma palavra estrangeira no texto do leitor.

Os cinco pares:

- "Key point" e "Ponto-chave"
- "Where the analogy fails" e "Onde a analogia falha"
- "What works" e "O que funciona"
- "How to read" e "Como ler"
- "You already know... Now..." e "Você já sabe que... Agora..."


**O teste que falha hoje.** Dois testes no `test_lint_clear_read.py`.
Um texto em português com "Key point:" passa hoje sem aviso; depois, o lint avisa `label-in-wrong-language`.

E uma analogia na forma "é como mostrar" sem "Onde a analogia falha" passa hoje.
Depois, o lint a pega, porque o detector em português aceita "é como" mais verbo.

**Evidência.** Fase B, seção 5.2: a skill mínima deu os rótulos em inglês e o texto em português saiu com três deles. Fase C, seção 4.5: o modelo copia a letra do exemplo (Min 2022; a página do Fable 5.1 fala em "literal text to emit").

### 2. Papel antes do nome (P1: antes do experimento)

**O que muda.** A Regra 5 passa a cobrir nome de pessoa, de estudo, de norma e de lei.
O papel vem antes do nome, e o nome e a fonte vêm logo em seguida, na mesma frase ou na próxima.

O Dennis acrescentou em 1 de novembro: um papel sem nome é autoridade vaga, como "o melhor restaurante, segundo a pesquisa".
O leitor inteligente pergunta "que pesquisa?", e a confiança cai.

Exemplo fraco, nome sem papel: "Mayer mostrou que ensinar os termos antes ajuda."
Exemplo fraco, papel sem nome: "Um pesquisador mostrou que ensinar os termos antes ajuda."
Exemplo forte: "Um estudo com alunos de ciências mostrou que ensinar os termos antes da lição ajuda. O estudo é de Richard Mayer, de 2002, e está na lista de fontes."

**O teste que falha hoje.** Dois testes no lint.
"Mayer mostrou que" passa hoje; depois, o lint avisa `name-before-role`, porque o nome veio antes do papel.

"Um pesquisador mostrou que", "estudos mostram que" e "segundo a pesquisa" passam hoje.
Depois, o lint avisa `authority-without-name` quando nenhum nome ou fonte aparece na mesma frase ou na seguinte.

A primeira checagem procura um nome com maiúscula seguido de verbo de evidência ("mostrou", "achou", "demonstrou", "found", "showed") sem substantivo de papel na frase.
A segunda procura o substantivo de papel com verbo de evidência.
Ela exige um nome com maiúscula, um ano ou um link até o fim da frase seguinte.

**Evidência.** Achado 2 da conversa de 1 de novembro, e a correção do Dennis no mesmo dia (autoridade vaga). Fase C, seção 4.2: um rótulo sem referente custa até fechar (catáfora, cerca de 80 ms por tentativa). Nomes desconhecidos prejudicam a escuta em segunda língua (Kobeleva 2012).

### 3. "Conhecido antes do novo" com template, e a etapa "ler como o leitor" (P1: antes do experimento)

**O que muda.** Duas coisas.
A Regra 6 ganha o template literal da linha de reentrada, nas duas línguas, e dois exemplos completos.

E a Fase 2 (desenhar) ganha um item final, "ler como o leitor".
Para cada frase do desenho, duas perguntas: "o que ele já tem que eu posso usar?" e "o que estou deixando aberto?".

Para um modelo com raciocínio, isso é critério de conferência, não pedido de expor o raciocínio (seção 7.1 do guia, achado 7).

**O teste que falha hoje.** Um eval em `tests/evals/`: um prompt de explicação com três partes nomeadas.
Com a skill atual, pelo menos uma de três rodadas traz um rótulo nu ou uma remissão ao que já passou.
Com a nova, nenhuma.

Mais o golden set G2 (a seção que se sustenta sozinha), que a nova versão precisa reproduzir.

**Evidência.** Fase B, seção 5.2: a regra executou sem raciocínio quando a skill deu a string literal, e não executou na conversa com a skill completa. Fase C, seção 4.5: regra mais exemplo é a forma recomendada.

### 4. A seção "Sem raciocínio e sem ferramentas" (P1: antes do experimento)

**O que muda.** Cada skill ganha uma seção curta, antes das regras.
Ela diz o que fazer quando a pesquisa, o lint e o contexto não existem.
O texto vem dos fallbacks das tabelas 2.2 e 2.3 de `lacos.md`.

Para a clear-read, quatro substitutos.
Escrever de memória e marcar o que não verificou.
Um plano visível de 5 linhas no lugar do scratchpad.
As sete checagens por olho no lugar do lint, e rótulos na língua do leitor no lugar do pacote de língua.

Para a clear-listen, três substitutos.
Só fatos da fonte do usuário, e "a fonte não diz" para o resto.
Render plain quando não há perfil de motor, e as doze checagens à mão no lugar do lint.

**O teste que falha hoje.** O teste de leitor frio da Fase B, repetido.
Um escritor sem ferramentas, só com o arquivo completo da skill, escreve o texto do cache HTTP.

Hoje a skill completa não diz como escrever sem busca, e o escritor pula a pesquisa em silêncio ou trava.
Depois, ele marca o que não verificou, e a medida é a frase "(não verificado)" ou equivalente no texto.

**Evidência.** Fase B, seções 2 e 4: no perfil mínimo quase tudo roda ou degrada. O que falta é a frase "sem a ferramenta, faça isto". Proposta 9.6 do guia.

### 5. A seção "Conversa por voz" no topo da clear-listen (P1: antes do experimento)

**O que muda.** Uma seção nova, logo depois de "Who you are writing for", com as 14 regras do fio (seção 6 de `lacos.md`).
A decisão do Dennis: voz na clear-listen, texto fica na clear-read.

As 14 regras:

- Resposta em até 3 frases antes de qualquer estrutura, 6 no máximo.
- Frase de 8 a 15 palavras.
- Conector em toda ligação.
- Conhecido antes do novo, e o conhecido é a frase que a pessoa acabou de dizer.
- Papel antes do nome.
- Nenhum retrocesso.
- Cada frase é um ponto de parada seguro.
- Fechar com uma pergunta que devolve o turno quando passa de 3 frases.
- Redefinir um termo quando volta depois de 3 trocas.
- Anunciar estrutura só pelo conteúdo.
- Nunca numerar, um passo por turno.
- Esqueleto em uma frase no lugar do visual.
- Problema com a saída na frase seguinte.
- Pontuação como único controle de som, nenhuma marca.

**O teste que falha hoje.** Um eval: cinco perguntas curtas sobre um guia, respondidas como turnos de 30 segundos.
Com a skill atual, as respostas saem com "Parte um de", colchetes, ordinais ou listas numeradas; com a nova, nenhum desses.
O lint de áudio ganha um modo `--conversa` que falha com qualquer colchete, marcador de parte ou ordinal nu.

**Evidência.** Achado 5 da conversa de 1 de novembro. Fase B, seções 3.4 e 6. Fase C, 2.6: um passo por frase na instrução de navegação (Dalton 2013, Burnett 1998).

### 6. A renderização por motor vai para `references/` (P1: antes do experimento)

**O que muda.** A Fase 4 (renderizar) inteira sai do corpo da skill e vai para `references/rendering.md`.
Ela tem os quatro passos, a tabela das doze perguntas, a escada de degradação, as cinco regras de render e o exemplo em três meios.

No corpo fica um parágrafo: o que é um perfil de motor, onde ele vive, e a regra "leia `references/rendering.md` antes de gerar".
O corpo da clear-listen cai de cerca de 8 mil tokens para menos de 5 mil, e a seção "Conversa por voz" cabe.

**O teste que falha hoje.** Um teste de tamanho: `wc -w` do corpo da skill abaixo de 3.600 palavras (cerca de 5 mil tokens).
Hoje são cerca de 5.700 palavras.
E o eval de renderização continua passando: o modelo lê o arquivo quando o pedido é gerar áudio.

**Evidência.** Seção 7.1 do guia, achado 5: só os primeiros 5 mil tokens sobrevivem a uma compactação. Fase B, linha "depois da compactação": a Fase 4 (renderizar) é o que cai primeiro.

### 7. Regra 13b reescrita: a troca de voz custa 3 segundos (P1: antes do experimento)

**O que muda.** A Regra 13 passa a dizer: a troca de voz chama a atenção de volta.
O ouvinte perde os primeiros 3 segundos do que vem depois.

Então a frase importante nunca vem logo depois da troca; uma frase de transição vem antes.
Poucas trocas por parte, porque a perda cresce com o número de trocas.

Duas vozes com tom claramente diferente, e a segunda voz cedo, pela orientação.
A frase antiga, "a memória é melhor para o que vem logo depois", vira `retired` com a nota: contrariada por Potter 2000.

**O teste que falha hoje.** O lint de áudio ganha a checagem `key-after-voice-change`.
Um `[key]` na primeira linha depois de uma troca de papel (`Guia:` para `Curioso:`) é problema.
O exemplo de diálogo do próprio arquivo da skill precisa passar.

**Evidência.** Fase C, seções 2.4 e 9. Potter 2000 mostra sobrecarga momentânea, pior com mais trocas. Potter 2019 (41 participantes) mede tom e posição da troca, e Potter 2008 trata recursos estruturais como categoria.

### 8. Regra 15: a frase da revisão reescrita (P2: junto, sem depender do experimento)

**O que muda.** "Um resumo de 2 a 4 minutos funciona melhor do que uma segunda escuta rápida" sai.
Entra: "revisar perto do momento de uso ajuda; ninguém testou o formato da revisão (resumo curto ou reescuta)".
A frase antiga vira `retired`, com a nota: Murphy 2022 nunca testou resumo, e a reescuta em 2x venceu.

**O teste que falha hoje.** Um teste em `tests.md` que confere a frase, e a conferência no `research-basis.md` (mudança 11).

**Evidência.** Fase C, seção 2.5.

### 9. Regra 6: a pergunta de fechamento é a parte provada (P2: junto, sem depender do experimento)

**O que muda.** A Regra 6 fica, com um qualificador escrito.
A pergunta de fechamento sobre o áudio inteiro tem prova (Stern e Halamish 2023).
A pergunta por parte com pausa é hipótese, e a Fase D a testa.

A pausa de 4 a 6 segundos fica marcada como padrão de prática.

**O teste que falha hoje.** O lint de áudio passa a exigir a pergunta de fechamento ("Sem voltar...") em todo roteiro de mais de uma parte.
Hoje ele exige só a pergunta por parte.

**Evidência.** Fase C, seções 2.7 e 6.

### 10. Testes unitários para o lint de áudio, e quatro checagens novas (P2: junto, sem depender do experimento)

**O que muda.** Um arquivo `scripts/test_lint_audio_script.py`, com um teste por checagem existente (12) e quatro checagens novas.
As novas: vocabulário de intents (um colchete fora da tabela é problema), mais de um `[key]` por parte, e parte que abre com direção lenta.
A quarta é risco relativo sem base: "o dobro" ou "por cento maior" sem "em cada" na frase.

Mais um script `check_render.py` que falha se um intent neutro sobra no texto renderizado.

**O teste que falha hoje.** Os quatro testes novos falham com o lint atual. Hoje `[whispers]` num roteiro neutro passa.

**Evidência.** Fase A, seção 1: a clear-listen não tem regressão automática. Fase B, achado 8 da seção 6.

### 11. O mapa de evidência conferido nos dois `research-basis.md` (P2: junto, sem depender do experimento)

**O que muda.** Cada `research-basis.md` ganha, no topo, uma tabela.
As colunas: regra, afirmação, veredito, fonte com DOI, certeza, data da conferência e acesso (texto completo ou resumo).
As linhas vêm da seção 6 de `pesquisa-conferida.md` e das tabelas da seção 2.

As correções da seção 8 entram.
São elas: Haviland e Clark 1974 direto, Brann e Sidi 2025, Potter reatribuído, Ginns 2013 com DOI, Michalek 2014 com o título certo, Alderson corrigido.
Uma linha no fim aponta para `investigacao-2026-11/pesquisa-conferida.md` como a história da conferência.

E o arquivo da skill ganha uma frase.
"Quando o leitor perguntar de onde vem uma regra, leia o mapa e responda com a fonte e a certeza."

**O teste que falha hoje.** Um script `check_research_basis.py` que confere três coisas.
Toda regra da skill tem uma linha no mapa, todo DOI tem a forma certa, e nenhuma linha está sem data de conferência.
Hoje nenhum dos dois arquivos tem a tabela.

**Evidência.** Decisão do Dennis em 1 de novembro (`decisoes-do-dennis.md`). Fase C inteira.

### 12. A ISO 24495-1 nos pacotes de língua e na Regra 10 (P2: junto, sem depender do experimento)

**O que muda.** `lang-pt-br.md` e `lang-en.md` abrem com a norma internacional, ISO 24495-1:2023, e os quatro princípios.
A lei brasileira, a versão brasileira da norma (ABNT NBR ISO 24495-1:2024) e as Federal Plain Language Guidelines entram como aplicação.
O parêntese da Regra 10 do arquivo da skill cita a ISO.

**O teste que falha hoje.** O teste 17 de `tests.md` ganha uma linha: os dois pacotes citam a ISO. Hoje não citam.

**Evidência.** Adendo 1. Fase C, seção 5.3.

### 13. O parágrafo do narrador, com o limite (P2: junto, sem depender do experimento)

**O que muda.** A seção "Who you are writing for" das duas skills ganha um parágrafo sobre quem escreve: alguém que conta uma história boa para um amigo.
Entrega completo, puxa pelo que vem, repete o essencial como quem relembra junto, nunca mostra o esqueleto.

Com o limite: a narrativa ajuda mais a lembrar do que a entender (Mar 2021, memória g maior do que compreensão).
Então o mecanismo continua precisando de passo a passo.

**O teste que falha hoje.** Um eval com juiz: o mesmo pedido, com e sem o parágrafo.
O juiz conta anúncios de estrutura ("são cinco pontos", "primeiro, segundo") no texto.

**Evidência.** Achado 4 da conversa. Fase C, seção 2.3 (Mar 2021; Wolfe e Woodwyk 2010, com o limite reescrito).

### 14. Regra 9 (tom) e Regra 8b (calibrar) com exemplo (P2: junto, sem depender do experimento)

**O que muda.** A Regra 9 divide em duas frases com fontes diferentes.
A primeira: "sem enfeite que não sirva a um conceito" (detalhes sedutores).
A segunda: "escreva como num e-mail de trabalho a um colega", sem proibir falar direto com o leitor (Ginns 2013).

A atribuição a "pesquisa de leitura em tela contra áudio" sai.

A Regra 8b ganha a regra operacional.
Dentro da área do leitor, o básico em uma frase ou num bloco colapsado.
Fora da área, o andaime inteiro; e, sem contexto do leitor, o andaime inteiro.

**O teste que falha hoje.** Um teste em `tests.md`: o mesmo pedido em tema de informática e em tema de saúde.
O segundo tem a seção "O que saber antes de ler" e o primeiro não.

**Evidência.** Fase A: as duas regras são adjetivos sem exemplo. Fase C, seções 2.8 e 6. Seção 7.1 do guia, achado 1.

### 15. Evals em `tests/evals/` (P2: junto, sem depender do experimento)

**O que muda.** Um arquivo `plugins/dc/skills/clear-read/tests/evals/evals.json`, e o mesmo para a clear-listen, no formato do `claude plugin eval`.
São 3 prompts realistas por skill, com e sem a skill, e afirmações concretas.

Os evals de gatilho da clear-listen vêm de `projeto/`.
Um arquivo de leitura de uma tela diz como rodar.

**O teste que falha hoje.** O próprio eval, que não existe.

**Evidência.** Decisão do Dennis: `tests/evals/` dentro da skill. Seção 7.1 do guia, achado 10.

### 16. Regra 3 da clear-listen: a prévia que nomeia o tópico (P3: depois da Fase D)

**O que muda, se a Fase D confirmar.** "Anuncie a contagem antes de uma lista" sai.
Entra "abra a lista com uma frase que nomeia o tópico e o liga ao maior", como nas prévias de Lorch.

O exemplo "São três motivos." vira `retired` com nota.

**Por que espera.** O Dennis quer sentir no experimento (pergunta 6 da seção 12). A Fase D gera as duas formas.

**Evidência.** Fase B, seção 5.4: a contagem vazia segue o exemplo da skill. Fase C, seções 4.1 e 9: as prévias que funcionaram nomeavam o tópico; nenhum estudo testou a contagem nua.

### 17. Atribuição no fio, como a BBC (P1: antes do experimento)

**O que muda.** O Dennis pediu em 1 de novembro, depois de aprovar o plano, que a atribuição entre no fio do texto.
Vale para tudo que tem nome: pessoa, instituição, lugar, empresa, estudo, lei.

O modelo é o BBC Lê: "Uma pesquisa da Universidade de Oxford, no Reino Unido, feita pelo psicólogo Fulano, encontrou que...".
Nunca uma nota solta depois da frase ("o pesquisador é Fulano"), e nunca vaga ("um pesquisador", "segundo a pesquisa").

Na clear-listen, a atribuição vem antes da afirmação, porque o ouvinte não julga o que ouve até saber quem fala.
Na clear-read, a afirmação pode vir primeiro, mas a atribuição completa vem na mesma frase ou na seguinte.
A Regra 5 da clear-read troca o exemplo forte da mudança 2 por um exemplo no fio.
A Regra 13 da clear-listen ganha a frase "diga quem antes do quê".

**O teste que falha hoje.** O lint `authority-without-name` da mudança 2 cobre a parte vaga.
A parte fluida é um eval com juiz: o mesmo pedido, com e sem a frase nova.
O juiz conta atribuições em nota solta ("O estudo é de", "O pesquisador é") e atribuições vagas.

Teste determinístico: um grep de "say who before" no arquivo da clear-listen e de "in the same sentence" na Regra 5 da clear-read.

**Evidência.** Fase C, seção 5.5: o guia de estilo da BBC News de 2003, seção "Attribution first". As Diretrizes Editoriais da BBC de 2025, itens 3.4.4 e 3.4.6. A decisão do Dennis em `decisoes-do-dennis.md`.

### 20. Regra 7: nunca desenhar uma sequência (P2: aprovada em 2 de novembro)

**De onde vem.** O adendo 2 (`adendos/2026-11-01-visuais-e-regras-do-projeto.md`), escrito depois da Fase E, que o chamou de mudança 18.
O número 18 já estava em uso na implementação, então aqui ele é 20.

**O que muda.** O parágrafo "Pick the form by the content" da Regra 7 sai, e entra o texto da seção 4 do adendo.
Uma sequência de passos sem ramificação vira lista numerada ou um stepper em HTML, nunca diagrama, porque caixas em fila repetem a prosa.

Um grafo de verdade vira SVG inline com os tokens de tema.
O Mermaid fica só para um fluxo linear simples que precisa ficar em Markdown.
Até 8 atores e suas ligações viram um mapa em SVG com a relação escrita na seta.
Números viram gráfico em SVG (com a skill `dataviz`) ou tabela.

Muitos atores com vários atributos viram tabela; um grupo grande mostra só os citados, até 8, mais "e outros N".
Eventos datados viram linha do tempo em HTML, nunca diagrama.
Todo diagrama precisa acrescentar uma relação que a prosa carrega mal; o que só repete a prosa é cortado.
`references/html-patterns.md` ganha duas seções: o mapa de atores em SVG (regra pb-004 do playbook) e o stepper para uma sequência.

**O teste que falha hoje.** O lint ganha o aviso `sequence-as-diagram`: um bloco Mermaid `flowchart` com arestas só em cadeia (A, B, C, sem ramo) avisa.
Hoje um documento com um `flowchart TD` de 4 nós em fila passa calado; depois, avisa.
É aviso e não problema, porque o Markdown puro ainda aceita o fluxo linear.

**Evidência.** Berney e Bétrancourt 2016 para a forma por conteúdo, e a regra pb-004 do playbook da Biblioteca. O teste do Projeto de 24 de setembro de 2026 mostrou o app do celular cortando o rótulo de um nó Mermaid. Certeza alta para "nunca sequência em diagrama", média para a preferência por SVG.

### 21. As regras do Projeto que são método (P2: aprovada em 2 de novembro)

**De onde vem.** A seção 5 do adendo 2 lista 14 regras das instruções do Projeto que a skill não tem, ou tem só em parte.
A seção 7 deste arquivo dá o veredito de cada uma.
Dez entram na skill; esta mudança as implementa, uma por commit, depois que o Dennis aprovar.

**O que muda.** As dez entradas da seção 7 marcadas "entra".
Cada uma vira uma frase ou um template literal na regra que a seção 7 nomeia, com o teste que a mesma seção dá.

**O teste que falha hoje.** Um por item, na seção 7.

**Evidência.** As fontes nomeadas na seção 7, todas já conferidas na Fase C ou na pesquisa consolidada do Projeto.

Ponto-chave: toda mudança tem um teste que falha hoje, e a única sem teste pronto é a 16, que espera o experimento.

## 3. Fora das skills: o Projeto

Duas coisas são produto, não método, e ficam para o Dennis aplicar no Projeto.

**Os nomes das seções.** "O chão: o que precisa estar firme antes da leitura" vira "O que saber antes de ler: os conceitos que o artigo não explica".
"Para este guia ficar" vira "Exercícios de fixação: as perguntas deste guia voltam em dias".

As instruções do Projeto usam os nomes antigos em 9 linhas, e o modelo de guia (`dev/guide-template/`) na Biblioteca também.
As 9 linhas novas já estão em `projeto/2026-11-01-nomes-novos-das-secoes.md`, e o Dennis cola no Projeto.

**O Projeto roda o lint.** A seção 6 do guia dizia que não, e a pesquisa diz que sim.
As instruções do Projeto não mudam; o guia ganha uma errata na seção 6.

Ponto-chave: dois nomes novos e uma errata, nada disso mexe nas skills.

## 4. A ordem de execução no branch filho

1. Mudanças 10 e 1: os testes primeiro, porque os outros commits precisam deles para provar que falham antes.
2. Mudanças 2, 3, 4, 7 e 17: as regras P1 (antes do experimento) das duas skills. A 17 roda depois da 2 e da 5, porque mexe nos mesmos trechos.
3. Mudanças 6 e 5: a renderização sai e a conversa entra, nessa ordem, porque a segunda só cabe depois da primeira.
4. Mudanças 8, 9, 11, 12, 13, 14: as correções de evidência e de redação.
5. Mudança 15: os evals, por último, porque medem o resultado de tudo.
6. Regressão completa: 98 testes do lint, self-test do Mermaid, testes novos do lint de áudio, os cinco trechos do golden set, e os evals.

Cada commit tem o número da mudança no título, para o Dennis apontar o que entra e o que fica.

Ponto-chave: testes primeiro, regras P1 (antes do experimento) depois, e a conversa só entra quando a renderização sair.

## 5. O que o Dennis decide

- Quais das 16 mudanças entram em `investigacao-2026-11`. A recomendação é: as sete de P1 (antes do experimento) e as oito de P2 (junto); a 16 espera a Fase D.
- Se o parágrafo do narrador (13) entra nas duas skills ou só na clear-listen.
- Se a Regra 9 (tom) mantém "sem personalidade" apesar de Ginns 2013, ou abre para falar direto com o leitor.

Ponto-chave: o plano tem 16 itens, e a decisão do Dennis é por item, não por linha.

## 6. O que a implementação entregou, em 1 de novembro

As 15 mudanças aprovadas estão no branch `investigacao-2026-11-fase-e`, um commit por mudança, mais quatro commits que a implementação pediu.
Dois fluxos rodaram em paralelo, um por skill, e um verificador independente conferiu cada commit: o teste falha antes, passa depois, e nada foi apagado.
Dois leitores frios leram cada skill inteira no fim e apontaram problemas, que viraram a mudança 18.

| Mudança | O que entrou de fato | Desvio do plano |
|---|---|---|
| 1 a 15 | Como a seção 2 descreve, com 11 testes a mais na clear-read e 46 na clear-listen | A mudança 2 ganhou o segundo aviso de lint (`authority-without-name`) |
| 6b (nova) | Exemplos, Regras 16 a 21, os cinco fatos sobre a escuta e as seis regras de intents saíram do corpo da clear-listen para `references/` | A meta de 3.600 palavras não foi atingida: o corpo ficou em 4.798 palavras, vindo de 5.698 |
| 17 (nova) | Atribuição no fio, estilo BBC, nas duas skills | Nenhum |
| 18 (nova) | As correções dos leitores frios: sexto rótulo fixo ("O que saber antes de ler"), frases longas, contradições entre seções novas e antigas | Nenhum |
| 18b (nova) | As listas do lint da clear-read foram para `references/lint.md`, e o corpo ganhou um teste de tamanho | O corpo da clear-read ficou em 6.272 palavras, vindo de 5.129, porque as 15 mudanças acrescentaram texto |
| 20 e 21 | Feitas em 2 de novembro, em 11 commits: a Regra 7 nova com o aviso `sequence-as-diagram` e as duas seções de `html-patterns.md`; os dez itens da seção 7, com três avisos de lint novos (`double-negative`, `empty-word`), três testes em `tests.md` e quatro evals | O corpo da clear-read foi a 7.022 palavras; o teto do teste subiu para 7.100, com a meta de 3.600 registrada |
| 15 | Fonte dos evals dentro da skill, como o Dennis decidiu | A ferramenta `claude plugin eval` recusa evals dentro de `skills/`. As cópias que ela lê ficam em `plugins/dc/evals/`, geradas por script. O `.gitignore` mudou para deixar as duas pastas entrarem |

O que fica para o Dennis decidir depois do PR:

- O que mais sai do corpo das skills para chegar perto de 3.600 palavras. Os candidatos estão nos comentários dos testes de tamanho (`SkillBodySize`) das duas suítes.
- Se a Regra 3 da clear-listen muda (mudança 16), depois do experimento.

Ponto-chave: 19 commits; a skill de áudio ficou menor, a de texto ficou maior, e a meta de tamanho está registrada como pendente.

## 7. As 14 regras do Projeto, com veredito

A seção 5 do adendo 2 pede um veredito por regra: entra na skill (método), fica no Projeto (produto), ou já existe.
A régua é a da seção 14 das instruções do Projeto.
Método serve a qualquer leitor cansado em qualquer texto; produto é a Biblioteca, a revisão espaçada e os selos.

| Regra do Projeto | Veredito | Onde entra, e o teste |
|---|---|---|
| Marcador de progresso no topo de cada conceito ("Conceito 2 de 4") | Entra, como opção para texto longo | Regra 1: em texto com 4 ou mais conceitos, cada seção de conceito abre com "Conceito N de M" na primeira linha. É posição, não anúncio de contagem, e a Fase D decide a contagem antes de lista, não isto. Teste em `tests.md`: um pedido de 5 conceitos sai com os marcadores |
| A ideia central em palavras na primeira frase da seção ("A ideia central aqui é") | Entra, como template literal | Regra 1 já pede que a seção abra pelo ponto; ganha a forma literal "A ideia central aqui é: ..." nas duas línguas, como a mudança 3 fez com a reentrada. O golden set G2 já a usa. Teste: grep no eval das três partes |
| Bloco "Mito corrigido" com fonte | Entra | Regra 3 ganha o bloco literal: "Muita gente acha que X. Isso não confere. Na verdade, Y. Fonte: Z." A Fase 1, item 5, já manda anotar os erros comuns. Evidência: Muller e Sharma 2007 (dar voz ao erro e refutar). Teste: eval com um tema que tem um mito conhecido |
| Pré-perguntas no começo, respondidas no corpo, repetidas no quiz | Entra em parte | As pré-perguntas e a resposta no corpo são método (Regra 6; a clear-listen já as tem). O quiz repetido é produto da Biblioteca e fica no Projeto. Evidência: Decisão 1 da pesquisa consolidada. Teste: eval, o texto abre com 2 ou 3 perguntas e cada uma tem resposta marcada no corpo |
| "Recapitule de cabeça" no fim: recordação do texto inteiro | Entra | Regra 6 ganha o fecho: "Sem voltar: quais foram as ideias principais?" seguido das respostas num bloco colapsado. Evidência: Stern e Halamish 2023 (texto inteiro venceu por seção). Teste: grep da frase no eval |
| Duas camadas sempre visíveis: o que a fonte diz e o que foi acrescentado | Entra, no modo reescrever | A seção "Two modes" ganha a regra: o que não vem da fonte leva a marca "(acrescentado)" ou vai para a seção "O que o artigo não diz". Para HTML já existe em `html-patterns.md` seção 8. Teste: eval de reescrita com um fato de fora |
| Toda ideia carregada pelo texto, nenhuma só por visual | Já existe | Regra 7, "the text still carries every idea". O Test 14 de `tests.md` ganha uma linha que confere isso com o leitor frio só do texto |
| Rótulo com conteúdo, nunca código nu | Já existe | Regra 6, e o lint `bare-label` |
| Negrito como trilha: só a linha mais importante de cada bloco | Já existe | Regra 10 |
| Toda analogia com "Onde a analogia falha" | Já existe | Regra 5, e o lint `analogy-without-limit` |
| Pouca negação: dizer o que é, não o que não é | Entra | Regra 2 ganha a frase: "diga o que é; uma negação só quando o leitor traz a crença errada". Evidência: Lei 15.263 e as diretrizes de linguagem simples. Teste: aviso de lint `double-negative` para "não ... nenhum", "não deixe de" |
| A ideia principal antes das exceções; várias ramificações viram tabela | Entra | Regra 1 ganha "a regra geral antes das exceções"; a Regra 11 generaliza: 3 ou mais ramos "se X, então Y" viram tabela em qualquer texto, não só em procedimento. Teste em `tests.md` |
| Cortar metaconceitos vazios ("nível", "abordagem") e avaliativos vazios ("crucial", "robusto") | Entra | Regra 9 (sem enfeite) ganha a lista; os pacotes de língua ganham as palavras; o lint ganha o aviso `empty-word`. Teste unitário no lint |
| Explicar o que o artigo deixa implícito: ironia, sarcasmo, tom | Entra, no modo reescrever | A seção "Two modes" ganha: "o que a fonte diz pelo tom, o texto diz em palavras". Teste: eval de reescrita com uma frase irônica |

Ponto-chave: dez regras entram na skill e quatro já existem; nenhuma fica só no Projeto, porque a Biblioteca e os selos não estavam na lista.
