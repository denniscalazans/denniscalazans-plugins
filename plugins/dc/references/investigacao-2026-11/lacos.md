# Fase B: os laços de análise, canal por perfil

CRIADO: 2026-11-01 (Berlim), no Claude Code, branch `investigacao-2026-11`
FASE: B, do guia `guia-de-investigacao.md` (seção 6)
STATUS: entregue para o Dennis ler antes da Fase E

## 0. O que este arquivo é, e como ele foi feito

Este arquivo é a entrega da Fase B (os laços).
O guia pede uma matriz de 4 canais por 4 perfis, com as regras que mudam de status em cada célula.
Ele pede também um rascunho de skill mínima para cada skill, no perfil mais fraco.
Os dois rascunhos estão em arquivos ao lado: `skill-minima-clear-read.md` e `skill-minima-clear-listen.md`.

O trabalho rodou como um workflow de 33 agentes, em 7 fases.
Oito analistas classificaram cada regra do inventário em um perfil, e oito céticos tentaram refutar cada tabela.
Quatro analistas de canal conferiram a coluna "Vale onde" do inventário.

Seis rascunhos de skill mínima passaram por dois juízes.
O rascunho vencedor de cada skill foi testado por um escritor sem ferramentas e por um checador com o lint real.
Um crítico de completude fechou a rodada e apontou 19 lacunas, e esta entrega fecha as que cabiam na Fase B.

Os céticos fizeram 41 correções nas 8 tabelas, e todas entraram nas tabelas desta entrega.
Onde analista e cético discordaram sem decisão, a seção 1 registra a decisão que eu tomei e o motivo.
Nenhuma regra das skills mudou.

Ponto-chave: a matriz saiu de duas fatias (perfil e canal) conferidas por céticos, e as decisões de desempate estão escritas.

## 1. Os quatro perfis, fixados por escrito

O guia reduz 16 ambientes a 4 perfis.
Para a matriz valer, cada perfil precisa de uma definição que não mude de skill para skill.
A Fase B achou duas divergências, e esta seção as fecha.

| Perfil | Raciocínio | Ferramentas | Contexto do Projeto | Lint e shell | Voz |
|---|---|---|---|---|---|
| Mínimo | não | nenhuma | não | não | não produz áudio; entrega o roteiro neutro |
| Chat simples | sim | nenhuma | não | não | só no app, por voz, se o Dennis falar com ele |
| Projeto | sim | pesquisa (web, PubMed, Valency, Consensus, Exa) e o conector da ElevenLabs | sim | não, por definição do guia | produz áudio pelo conector |
| Agêntico | sim | pesquisa, conector da ElevenLabs, ffmpeg, subagentes | sim, pelas cópias em `projeto/` | sim, os dois lints e o check_mermaid | produz áudio pelo conector, mas não fala nem ouve |

**Decisão 1: o perfil Projeto não tem lint nem ffmpeg.**
A seção 6 do guia define Projeto como "raciocínio, ferramentas de pesquisa, contexto do projeto" e reserva "lints rodando" ao Agêntico.
As instruções do Projeto dizem o contrário em dois lugares: a seção 6.4 manda rodar o lint de áudio e juntar os arquivos com ffmpeg.

Isso é uma divergência entre o guia e o produto, e a matriz segue o guia.
Fica registrada como pergunta para o Dennis na seção 8, porque a Fase D precisa saber em qual Projeto roda.

**Decisão 2: um quarto status, "vago".**
Três regras são adjetivos sem exemplo: clear-read R9 (tom), clear-read R8b (calibrar ao leitor) e clear-listen R10 (expressão moderada).
Um analista as marcou "roda" num perfil e outro "degrada" em outro, e nenhum tinha razão, porque vagueza não é falta de capacidade do ambiente.

Elas recebem "vago" em todos os perfis e saem da conta roda, degrada, não roda.
A Fase E as trata com o achado 1 da seção 7.1 do guia: exemplo de entrada e saída.

**Decisão 3: o eixo de esforço virou uma nota.**
A seção 6 do guia tem o eixo esforço alto contra esforço baixo, e a redução a 4 perfis o apagou.
O achado 8 da seção 7.1 diz que, com esforço baixo, o modelo responde de memória.

Então, em esforço baixo, Chat simples e Projeto se comportam como o Mínimo nas fases de pesquisar e de desenhar da clear-read.
A Fase D fixa o esforço nas duas condições, e a matriz vale para esforço alto.

**Decisão 4: a compactação do Claude Code é uma linha à parte.**
Só o Agêntico tem o corte de 5 mil tokens depois de uma compactação de contexto (achado 5 da seção 7.1).
Ele derruba um bloco inteiro de regras em sessões longas, e não uma regra isolada.
Então a coluna Agêntico tem uma linha "depois da compactação", em vez de marcar cada regra como "degrada".

Ponto-chave: Projeto sem lint, "vago" para adjetivos, esforço como nota, e compactação como linha própria.

## 2. Passo 2: as regras que não rodam, por perfil

### 2.1 As contagens

A clear-read tem 46 linhas no inventário, e a clear-listen tem 41.
A tabela diz quantas rodam como estão em cada perfil, depois das 41 correções dos céticos e das decisões da seção 1.

| Skill | Perfil | Roda | Degrada | Não roda | Vago |
|---|---|---|---|---|---|
| clear-read | Mínimo | 32 | 11 | 1 | 2 |
| clear-read | Chat simples | 35 | 8 | 1 | 2 |
| clear-read | Projeto | 39 | 5 | 0 | 2 |
| clear-read | Agêntico | 39 | 5 | 0 | 2 |
| clear-listen | Mínimo | 29 | 10 | 1 | 1 |
| clear-listen | Chat simples | 30 | 10 | 0 | 1 |
| clear-listen | Projeto | 35 | 5 | 0 | 1 |
| clear-listen | Agêntico | 36 | 4 | 0 | 1 |

Duas coisas saltam da tabela.
No Mínimo, só uma regra de cada skill não roda de jeito nenhum: pesquisar sempre (clear-read) e o perfil de motor (clear-listen).
Tudo o mais roda ou degrada, e isso é a boa notícia da portabilidade: as skills são quase todas regras de redação.

A má notícia é a mesma nos dois casos.
A skill não diz o que fazer quando a ferramenta falta.
"Do not skip this phase" sem busca, e "run the lint" sem shell, viram um desejo escrito, e o modelo pula em silêncio.

### 2.2 Clear-read: as linhas que mudam de status

A tabela lista só as regras que não rodam como estão em algum perfil.
As outras 30 rodam nos quatro perfis.
A última coluna é o texto que a skill deveria ter, em inglês, pronto para a Fase E avaliar.
O analista do perfil mais fraco onde a regra falha escreveu esse texto.

| Regra | Mínimo | Chat simples | Projeto | Agêntico | O que a skill deveria dizer (fallback, do perfil mais fraco) |
|---|---|---|---|---|---|
| Fase 1: pesquisar sempre | não roda | não roda | roda | roda | If no search tool is available, write from memory and mark every number, date, law, price or version you could not verify with '(not verified)'; end the reply with one line naming the official source the reader should check before acting. Prefer explaining how something works over quoting figures you cannot confirm. |
| Fase 1, privacidade no modo reescrever | roda | roda | roda | degrada | Treat every call that leaves this session as a search: web fetch, any MCP connector, and any translation or rephrase service. Pass to them only public facts and term definitions, never names, figures, or internal details from the user's content. |
| Fase 2: desenhar (10 itens) | degrada | degrada | roda | roda | If you have no scratchpad or hidden reasoning, open the reply with a 5-line block headed 'Plan' that lists the main concepts, the terms you will define, the section headings and the visual verdicts; the reader may skip it. Skip item 10 and apply Rule 10 from this file alone. |
| Fase 3: escrever e rodar o lint | degrada | degrada | degrada | degrada | If you cannot run the lint, check four things by eye before sending: no sentence over 25 words, no block over 4 sentences, no 'as mentioned above' or bare label such as 'P1', and a 'How to read:' line after every visual. In Claude Code, write the reply to a scratch file and lint it. |
| O arco | degrada | roda | roda | roda | O item 4 da Fase 2 (o arco) vive no scratchpad, que o Mínimo não tem. Sem ele, a ordem sai como vier. |
| R1d: uma frase por linha, conferir o render | degrada | degrada | degrada | degrada | If you cannot see the rendered output, end every sentence in Markdown with a backslash or two trailing spaces and a newline, leave a blank line only between topics, and do not try to confirm the render. Say in one line at the end that sentences should appear stacked. |
| R4: nenhum conhecimento assumido | degrada | roda | roda | roda | Sem raciocínio, decidir onde começa o chão do leitor é um palpite; a regra "trate como iniciante inteligente" é o padrão seguro. |
| R5c: termos técnicos em inglês no português | degrada | degrada | roda | roda | If the language pack is not available, keep in English only the terms an IT team in Brazil says in English at work (API, deploy, cache, token, commit, pull request, log) and translate everything else, giving the Portuguese meaning the first time. |
| R6e: conhecido antes do novo | degrada | degrada | degrada | degrada | If you cannot re-read before sending, open each sentence with a word the previous sentence already used (its subject, its result, or 'this X') and put the new fact at the end. Treat a sentence that opens with a name, a code or a count the reader has not met as a slip. |
| R7a: o teste das 4 perguntas | degrada | roda | roda | roda | If you have no scratchpad, default to no visual. Draw one small diagram only when the concept has 3 or more elements and the question is about a path or a comparison; the text must carry the idea anyway. |
| R7c: a forma pelo conteúdo | roda | roda | degrada | degrada | A skill manda Mermaid, e as instruções do Projeto mandam SVG inline. É conflito de contexto, não falta de capacidade. In a terminal reply, Mermaid does not render, so use the numbered outline or a table. |
| R7d: construir para o celular | degrada | degrada | degrada | roda | If you cannot run the phone check, count every label to 25 characters or fewer, use a top-to-bottom layout with at most 2 nodes per row, and switch to a numbered outline when the diagram would need more than 6 nodes. |
| R7e: três limites | degrada | degrada | roda | roda | If you cannot produce an icon array, state every health risk as a natural frequency in words, such as '3 in every 100 people', and give the comparison group's frequency in the same sentence, never a relative risk alone. |
| R8b: calibrar ao que o leitor sabe | vago | vago | vago | vago | Without a record of what the reader knows, use one rule: if the topic is everyday IT work, keep each basic explanation to one sentence; for anything else, give the full scaffolding. |
| R9: tom calmo, preciso | vago | vago | vago | vago | Write as you would in a work email to a colleague: no jokes, no exclamation marks, no rhetorical questions, no opener like 'Great question'. State the fact and its reason. |
| R10c: pacotes de língua | degrada | degrada | roda | roda | If you cannot open the language pack, write by the eleven rules alone: expand every acronym on first use except the ones the reader meets daily (API, URL, CPU, HTML, PDF), write dates with the month as a word, and write every fixed label in the reader's language. |
| Depois da compactação (só Agêntico) | | | | caem R10a, R10d, R10e, R11a, R11b, R11c, o lint e o arco | Medido a 4 caracteres por token, os 5 mil tokens terminam dentro da Regra 10. Tudo depois dela some numa sessão longa. A Fase E decide o que sobe e o que vai para `references/`. |

Duas linhas quebram a ordem "mais capacidade, status igual ou melhor", e as duas são legítimas.
A R7c (forma pelo conteúdo) piora no Projeto porque o contexto traz um conflito: a skill diz Mermaid e o Projeto diz SVG.
A privacidade da fase de pesquisar piora no Agêntico porque a superfície cresce: conectores, fetch e serviços de tradução também levam dados para fora.

### 2.3 Clear-listen: as linhas que mudam de status

| Regra | Mínimo | Chat simples | Projeto | Agêntico | O que a skill deveria dizer (fallback, do perfil mais fraco) |
|---|---|---|---|---|---|
| Fase 1: fonte verificada | degrada | degrada | roda | roda | If you cannot search and no verified source is given, write only from the text the user pasted, add no fact of your own, and open the producer note with 'facts not verified in this session'. If there is no source text at all, ask for one instead of writing from memory. |
| Fase 2: desenhar (8 itens) | degrada | roda | roda | roda | If you have no hidden reasoning step, write the design as a short visible block before the script: the core idea, one line per part, the spoken names, the cuts, one question per part, one tone per part, and the planned word count at 160 words per minute. |
| R9: ritmo moderado, pausas | degrada | degrada | degrada | degrada | When you produce no audio, write only the pause and key intents, and hand the pace to the producer in one note: 'target about 160 words per minute in Brazilian Portuguese'. No Projeto e no Agêntico, o motor eleven_v4 não tem ajuste de velocidade, e a taxa só se mede depois. |
| R10: expressão moderada | vago | vago | vago | vago | "Moderado" precisa de exemplo. Candidato a lint: mais de um `[key]` por parte. |
| R11: só voz, sinal limpo | degrada | degrada | degrada | degrada | When you do not produce the audio, write the constraint as the first producer note ('voice only: no music, ambience, effects or noise under the voice') and never write a sound-effect intent in the script. No eleven_v4, uma marcação vaga pode virar efeito sonoro, então a regra pede conferência por ouvido. |
| R12: uma voz por papel, medir a taxa | degrada | degrada | degrada | degrada | Nenhum perfil ouve. If you cannot generate or hear audio, skip the voice check and the rate measurement and say so. Put the script's word count in the producer note and ask the producer to divide it by the audio minutes after generating. |
| R13b: a troca de voz puxa a atenção | degrada | degrada | degrada | roda | When you do not choose the voices, keep the placement rules in the script and ask in a producer note for two voices with clearly different pitch. No Agêntico, o tom das vozes se mede no áudio com ffmpeg. |
| R18: tabela em três movimentos | degrada | degrada | roda | roda | When there is no written guide, make the third move an honest limit: say that the full table is not in the audio, and offer to write it for the eye in the same conversation. |
| R21: limites honestos | degrada | degrada | roda | roda | When there is no written guide, say the conclusion and the pattern, then say plainly that the audio does not cover the steps. Never name a guide or a section that does not exist. |
| Fase 4, passo 2: o perfil de motor | não roda | degrada | roda | roda | When you cannot read the engine's documentation, do not answer the profile questions from memory. Hand the twelve questions to the user as a blank profile to fill in, and render plain until it comes back. |
| Fase 4, regras de render | degrada | degrada | roda | roda | When you cannot write files, output the neutral script and the plain rendering as two labeled blocks in the reply, put the three-list render report at the top of the plain block, and reread the plain block once for any leftover bracket before sending. |
| Checar antes de gerar | degrada | degrada | degrada | degrada | When the lint cannot run, do its checks by hand and show them as one producer note: no sentence over 20 words, no digit, no parenthesis, no 'como eu disse', one 'Parte N de M' line and one recall question per part, at most two questions in the closing. Say that the lint and the cold reader did not run. |
| Depois da compactação (só Agêntico) | | | | cai a Fase 4 inteira (renderização) | Os 5 mil tokens terminam antes da Fase 4. A renderização por motor é a parte que uma sessão longa apaga primeiro. |

Na clear-listen, o que degrada em todo perfil é a produção, não o texto.
Ritmo, sinal limpo, voz por papel e a checagem final dependem de ouvir, e nenhum perfil ouve.
A skill já diz "If you cannot hear audio, say so" no passo de conferir o áudio.
Ela precisa dizer o mesmo nas regras de ritmo, de sinal limpo e de voz por papel.

Ponto-chave: nos dois casos, o que falta não é regra, é a frase "sem a ferramenta, faça isto".

## 3. Passo 3: as regras que atrapalham, por canal

Os quatro analistas de canal confirmaram a coluna "Vale onde" do inventário em quase tudo.
A tabela lista só o que atrapalha em cada canal, e o que entra no lugar.

### 3.1 Texto no chat

Nenhuma regra da clear-read atrapalha.
Duas ganham um canal a mais: a R7c (forma pelo conteúdo) e a R7d (construir para o celular).
Elas valem no chat porque o leitor pode estar no telefone, e porque o Mermaid não é garantido no cliente de chat.

Oito regras da clear-listen atrapalham se aplicadas a uma resposta escrita.

| Regra da clear-listen | Por que atrapalha no texto | O que entra no lugar |
|---|---|---|
| Duas camadas e vocabulário de intents | Um `[warm]` numa resposta de chat vira texto literal na tela | Negrito em uma linha por bloco (clear-read R10e) e pontuação |
| Formato do roteiro | Notas `#`, papéis `Guia:` e "Parte um de três" são ruído na tela | O Markdown da clear-read R1d |
| R1b: "Parte N de M" | O título `##` faz o mapa de graça; a contagem é esqueleto anunciado | Títulos-mensagem |
| R2: teto de 20 palavras, sem parênteses | O parêntese é a ferramenta da glosa de termo (clear-read R5a) | Alvos da clear-read R2a: 15 palavras, teto 25 |
| R3: dizer a estrutura | A lista com marcadores já mostra a contagem | A lista mostra; se anunciar, a frase já entrega conteúdo |
| R6: pergunta com pausa | Não há pausa no texto, e um quiz por resposta cansa | "Ponto-chave:" quando a resposta passa de 3 blocos |
| R7: números por extenso, sem link nem tabela | O olho lê "600" mais rápido que "seiscentos" | Dígitos com âncora (clear-read R10d), links e tabelas |

A R8 (falar com uma pessoa) da clear-listen ajuda no texto pela metade "dizer quem afirma".
"Um estudo de 2024 mostra" é o papel antes do nome, e a clear-read ainda não tem essa frase para o chat.

### 3.2 Página HTML

As 46 linhas da clear-read ajudam, porque a página é o canal nativo da skill.
Oito regras da clear-listen atrapalham.
Quatro delas pelos mesmos motivos do texto: o marcador de parte, o teto de 20 palavras, a contagem anunciada e os números por extenso.
Mais quatro, que a tabela lista.

| Regra da clear-listen | Por que atrapalha na página | O que entra no lugar |
|---|---|---|
| R17: estruturas, não pixels | Na página o diagrama existe, e "Como ler" precisa dizer o que cor e seta significam | A figura que passou no teste das 4 perguntas, com as duas linhas da R7b |
| R18: tabela em três movimentos | A página é o guia para onde a R18 aponta; aplicá-la aqui é circular | A tabela inteira, com "Como ler" e a conclusão |
| R19: gráfico em quatro frases | As quatro frases substituiriam o que o olho vê em um segundo | O gráfico, com escala e padrão na linha "Como ler" |
| R21: limites honestos | Cortaria exatamente o código e a tabela que a página existe para mostrar | Código em bloco (R11c), procedimento em estágios (R11a), tabela inteira (R7c) |

Duas regras da clear-listen ajudam na página.
A R6 (recuperar na cabeça) vira o quiz com resposta colapsada, e a R20 (risco em frequência natural) vira o icon array.
Um conflito ficou registrado: o quiz e o bloco colapsável contam como interativo para a R7e (um interativo por documento)?
Os guias do Projeto têm vários dos dois, e a regra não diz.

### 3.3 Áudio longo

As 41 linhas da clear-listen ajudam, inclusive o "Parte N de M", dizer a estrutura e a pergunta com pausa.
Num monólogo de 3 a 20 minutos ouvido caminhando, elas são o ponto de reentrada de quem divagou.
A ressalva fica na contagem nua antes do conteúdo, da R3 (dizer a estrutura), que segue para a Fase D.

Quatro regras da clear-read atrapalham na letra.

| Regra da clear-read | Por que atrapalha no áudio | O que entra no lugar |
|---|---|---|
| R6d: forma curta dentro do bloco | "O significado continua na tela", e não há tela | Repetir o nome inteiro (clear-listen R4) |
| R9: tom calmo para leitura silenciosa | Vira voz plana, que a clear-listen R10 proíbe | Um intent de tom por parte, trocado entre partes |
| R10b: conteúdo inteiro, nenhuma ressalva cai | Contradiz o arredondar da R7 e os cortes da R21 | Toda ideia principal com uma frase falada (R16), e os cortes declarados (R21) |
| R11a: lista numerada de até 7 passos | No ouvido, mais de 5 passos nem entram | Até 5 passos, um por frase, marcados em palavras (R3); acima disso, R21 |

Treze regras da clear-read são neutras no áudio, porque não têm objeto.
São as regras do render, do Mermaid, do celular, do negrito, do código em bloco e dos pacotes de língua.
A fase de pesquisar da clear-read ajuda a montante do roteiro, no guia escrito.
Ela nunca ajuda durante o roteiro, porque a fase de fonte da clear-listen diz "nenhum fato novo".

### 3.4 Conversa por voz

É o canal que mais muda.
O que sobrevive das duas skills é o fio da seção 9.4 do guia.
O que atrapalha é tudo que é esqueleto ou marca, porque o modelo só emite texto e o motor lê o que recebe.

| Regra | Por que atrapalha na conversa | O que entra no lugar |
|---|---|---|
| clear-read Fase 1 e clear-listen Fase 1 | Um turno de 30 segundos não cabe uma pesquisa "sem exceção"; o modelo promete "vou verificar" em vez de entregar | Responder do que sabe, dizer o grau de certeza em meia frase, oferecer conferir por escrito depois |
| clear-read Fase 2 e clear-listen Fase 2 | Dez itens de desenho num turno de 6 frases produzem um mini-documento | Desenhar três coisas: a resposta em uma frase, o termo que precisa de chão, e o que a pessoa acabou de dizer que serve de ponte |
| clear-read R7a: teste das 4 perguntas | Não há visual, e o teste sempre dá "nada" | Dizer o esqueleto em uma frase (clear-listen R17) e oferecer o desenho por escrito |
| clear-read R9: tom calmo | "Calmo, sem personalidade" escrito vira fala uniforme no motor | Escrever como uma pessoa falando com outra (clear-listen R8) e variar o ritmo pela pontuação |
| clear-read R10e: negrito | Emitir asteriscos: o motor os pula ou os lê | A palavra forte no fim da frase, e uma frase curta para o ponto |
| clear-read R11a: lista numerada | "Primeiro, segundo" trava, e o motor lê "1." como ruído | Um passo por frase, objetivo antes da ação, dois ou três passos por turno, o próximo quando a pessoa pede, como o Google Maps |
| clear-read R11c: código em bloco | Sintaxe lida em voz alta, ou um buraco de silêncio | Dizer o que o comando faz e o nome em palavras, e oferecer o comando por escrito |
| clear-listen: duas camadas, vocabulário de intents, formato do roteiro | Qualquer colchete emitido é lido pelo motor ou descartado; não há render entre o modelo e a voz | Prosa corrida, e a pontuação como único controle de som |
| clear-listen R1b: "Parte N de M" | Promessa de um esqueleto numa resposta de seis frases | A virada vem por conteúdo: "Agora, o que fazer com isso" |
| clear-listen R3: dizer a estrutura | Produz o "cinco pontos" e o "primeira, segunda" que travam | Anunciar só quando a frase já entrega conteúdo, e nunca por ordinal |
| clear-listen R6: pergunta com pausa | A pausa de 4 a 6 segundos soa como fim de turno, e a pessoa fala por cima | Quando a resposta passa de três frases, fechar com uma pergunta curta que devolve o turno, sem marca de pausa |

Ponto-chave: texto e página perdem só a clear-listen, o áudio perde 4 regras da clear-read, e a conversa perde o esqueleto das duas.

## 4. A matriz: canal por perfil

Cada célula diz se o perfil consegue produzir o canal, e quais regras mudam de status nela.
"Mudam" quer dizer: em relação às tabelas da seção 2 (perfil) e da seção 3 (canal), somadas.
Uma célula vazia de mudanças herda a coluna do perfil e a linha do canal.

| Canal | Mínimo | Chat simples | Projeto | Agêntico |
|---|---|---|---|---|
| **Texto no chat** | Produz. Clear-read: Fase 1 não roda, Fase 2 e Fase 3 degradam, R10c degrada (rótulos em inglês vazam, ver seção 5). Clear-listen inteira atrapalha, menos R8 e R20 | Produz. Igual ao Mínimo, menos Fase 2 e R7a, que o raciocínio recupera | Produz. Tudo roda, menos R1d (render), R6e (sem releitura pedida) e o conflito Mermaid contra SVG | Produz. Igual ao Projeto, mais a privacidade da Fase 1 (conectores) e a linha "depois da compactação" |
| **Página HTML** | Improvável: sem lint, sem publicação, sem Mermaid conferido. Se produzir, R7d e R7e degradam | Improvável, pelos mesmos motivos. O raciocínio recupera o plano visual (R7a) | Produz. É o canal nativo. Só R1d e R7d degradam, porque o Projeto não vê o render nem roda o check_mermaid | Produz e confere: lint, check_mermaid e leitor frio por subagente. Nada degrada antes da compactação |
| **Áudio longo** | Escreve o roteiro neutro e entrega. Fase 1, Fase 2, perfil de motor (não roda), render e checagem degradam; render "plain" | Escreve o roteiro. Fase 2 roda; perfil de motor e render degradam; R18 e R21 degradam porque não há guia para apontar | Escreve e gera pelo conector, com o playbook. Só a produção degrada: R9, R11, R12, checagem por ouvido | Escreve, gera, mede com ffmpeg e lê o playbook copiado. Degradam R9, R11 e R12, porque ninguém ouve. A Fase 4 cai na compactação |
| **Conversa por voz** | Possível num sistema futuro do Dennis. Vale o conjunto da seção 6, sem nenhuma marca, sem pesquisa | Existe hoje, no app, por voz. É a célula do Achado 5 do guia. Fase 1 não roda, e o conjunto da seção 6 vale | Existe no app com o Projeto carregado. A pesquisa cabe só quando a pergunta pede número, lei ou prazo | Não existe: o Claude Code não fala nem ouve (guia, seção 8.1, item 4) |

Três coisas saem da matriz.
Primeiro, a célula "Chat simples por conversa" é a que a conversa de 1 de novembro expôs.
Nenhuma linha das duas skills foi escrita para ela.

Segundo, a célula "Mínimo por texto" é o teste de portabilidade, e ela falha hoje em três pontos: pesquisar, lint e rótulos em inglês.
Terceiro, a célula "Agêntico por página" é a única em que tudo roda, e ela é a única que uma compactação derruba.

Ponto-chave: a skill foi escrita para a célula Agêntico por página, e o Dennis vive nas células Chat simples por conversa e Projeto por texto.

## 5. Passo 4: a skill no perfil mínimo

### 5.1 Como os rascunhos foram feitos e julgados

Cada skill ganhou três rascunhos, de três ângulos.
O primeiro ângulo é o mais curto possível.
O segundo é o processo-primeiro: desenhar, ler como o leitor, corrigir, escrever.
O terceiro é o substituto do lint, em que as checagens do lint viram autochecagem por olho.
Um juiz por skill pontuou os três em quatro critérios.
Os critérios: portabilidade, fidelidade aos nove itens da seção 2.2 do guia, literalidade (exemplo de saída em cada regra) e tamanho.

| Skill | Rascunho | Portabilidade | Fidelidade | Literalidade | Tamanho | Total |
|---|---|---|---|---|---|---|
| clear-read | mais curto (449 palavras) | 5 | 4 | 5 | 5 | 19 |
| clear-read | processo-primeiro (673) | 3 | 5 | 4 | 4 | 16 |
| clear-read | substituto do lint (698) | 5 | 5 | 4 | 4 | 18 |
| clear-listen | mais curto (448) | 4 | 3 | 5 | 5 | 17 |
| clear-listen | processo-primeiro (699) | 4 | 4 | 3 | 3 | 14 |
| clear-listen | substituto do lint (699) | 5 | 5 | 4 | 4 | 18 |

O processo-primeiro perdeu nas duas skills pelo mesmo motivo.
Ele pede que um modelo sem raciocínio marque linhas e reescreva antes de escrever, e esse modelo não tem onde fazer isso.
Então a camada de processo da seção 9.1 do guia serve ao Chat simples, ao Projeto e ao Agêntico.
No Mínimo ela vira checagem por olho depois de cada bloco.

O juiz sintetizou o vencedor com enxertos dos outros dois.
Na clear-read, o critério que decidiu foi a literalidade: quase toda frase traz a string de saída que o modelo copia.
Esse mesmo critério causou a falha mais clara do leitor frio, e a seção 5.3 conta.

### 5.2 O teste de leitor frio, primeira rodada

Um agente sem ferramentas e com esforço baixo recebeu só a skill mínima e uma tarefa.
Para a clear-read: explicar em português, em 350 palavras e duas seções, como funciona um cache HTTP com etiqueta de versão (ETag).
A explicação precisava dizer por que "no-cache" não é "não guardar".

Para a clear-listen: um roteiro neutro de 3 minutos, em duas partes, sobre por que as férias aliviam o burnout por poucas semanas.
Um checador rodou o lint real no resultado, conferiu as marcas do golden set e respondeu três perguntas só com o texto.

| Medida | clear-read mínima | clear-listen mínima |
|---|---|---|
| Lint | 3 problemas: dois blocos de 5 frases, uma referência para trás ("do bloco anterior") | 1 problema: uma frase de 22 palavras |
| Marcas presentes | significado antes do termo no corpo, reentrada "Você já sabe que... Agora", conhecido antes do novo, analogia com limite, problema com solução | as seis marcas estruturais: ideia central cedo, "Parte um de dois", reentrada, pergunta com `[pause recall]`, nenhum dígito, "Sem voltar..." |
| Marcas ausentes | três rótulos em inglês dentro do texto em português: "Key point:", "Where the analogy fails:", "What works:"; "ETag" no título antes da definição | nenhuma; desvios de polimento: `[stress]` no meio da frase, sem `[pause short]`, três prequestões sem pausa |
| Leitor frio | 3 de 3 | 3 de 3 |

Três lições saíram da primeira rodada.

**O modelo sem raciocínio executou "conhecido antes do novo".**
O inventário marca a R6e (conhecido antes do novo) como "não executável enquanto escreve", e a conversa de 1 de novembro mostrou isso com a skill completa.
A skill mínima deu a string literal ("Você já sabe que... Agora...") e o modelo a produziu sem raciocínio e sem ferramenta.

Então a regra executa quando a skill dá o template, e não executa quando dá só o princípio.
Isso é a primeira evidência da Fase B a favor da tese parte 1.
Ela muda a forma da proposta 9.1: menos processo, mais template.

**O modelo copia a letra, inclusive a língua.**
A skill mínima da clear-read deu os rótulos em inglês, e o texto em português saiu com "Key point:" e "What works:".
Isso confirma os achados 1 e 3 da seção 7.1 do guia.
E mostra uma dependência que a Fase A não tinha visto: os rótulos vivem no pacote de língua, e sem o pacote eles vazam.

O lint não pegou, por dois pontos cegos.
A checagem de "Key point" só roda com título H2, e o detector de analogia em português exige "como um" ou "como se".

**O negrito de abertura conta como frase, e ninguém contou.**
Dois blocos saíram com 5 frases porque a frase em negrito no topo não entrou na conta do escritor.
A regra R1c é executável, mas foi conferida só pela ferramenta.

### 5.3 Os rascunhos revisados e a segunda rodada

Os dois rascunhos entregues já trazem as correções.
Na clear-read: os rótulos na língua do leitor, com os cinco pares escritos, e o negrito de abertura contado como frase.
Nenhuma sigla no título antes da definição.
Mais a frase "from the previous block" na lista de ponteiros proibidos, e um oitavo item de checagem, o rótulo na língua errada.

Na clear-listen: `[stress]` sozinho na linha anterior; `[pause short]` entre ideias e `[pause long]` entre partes; uma ou duas prequestões com pausa.
Mais um décimo item de checagem (parte acima de 5 minutos), e "o resto está na sua fonte" quando não há guia.
Com isso as 12 checagens do lint de áudio têm cada uma um item na autochecagem.

A regra 3 da clear-listen ficou como está na skill ("São três motivos"), porque a Fase A não muda regra.
A segunda rodada testa as duas formas lado a lado, e a seção 5.4 traz o resultado.

### 5.4 Segunda rodada: resultado

A segunda rodada repetiu o teste com os rascunhos revisados, e acrescentou um terceiro escritor.
Esse terceiro recebeu a skill mínima da clear-listen com uma só mudança no exemplo da Regra 3 (dizer a estrutura).
No lugar de "São três motivos", uma contagem que já entrega conteúdo: "São três motivos, e o mais forte é o sono".
Um comparador contou, nos dois roteiros, as contagens sem conteúdo e os ordinais nus.

| Medida | clear-read mínima, rodada 2 | clear-listen mínima, rodada 2 |
|---|---|---|
| Lint | 2 problemas, os dois de frase longa (39 e 28 palavras), nas linhas "Onde a analogia falha:" e "O que funciona:" | 3 problemas, os três de frase longa (21, 21 e 24 palavras) |
| Rótulos em inglês | nenhum | nenhum |
| Marcas presentes | 7 de 8: os três rótulos em português, reentrada, nenhum retrocesso, nenhum bloco de 5 frases, papel antes do nome no corpo | 9 de 9, inclusive `[stress]` na linha própria, `[pause long]` entre as partes, duas prequestões com pausa |
| Marcas ausentes | "ETag" continua no título e no H2 antes da definição | nenhuma |
| Leitor frio | 3 de 3 | 3 de 3 |

O que a revisão consertou: os rótulos saíram em português, os blocos ficaram em 4 frases, e a referência para trás sumiu.
O que apareceu no lugar: frases longas.
O escritor tratou cada linha rotulada como uma frase única e empilhou duas ideias nela.
Na clear-listen, a maior frase longa é justamente a frase `[key]` da parte dois.

A lição é a mesma nas duas skills: a estrutura e as marcas saem certas por instrução, e o comprimento da frase não.
Um modelo sem raciocínio não conta palavras enquanto escreve, e sem lint ninguém conta depois.
Então, no perfil mínimo, a regra de comprimento é a que mais depende de ferramenta.
O rascunho da clear-read ganhou duas linhas: o limite vale também nas linhas rotuladas, e a sigla só entra no título depois de definida.

**A contagem antes do conteúdo seguiu o exemplo da skill.**
Com o exemplo original ("São três motivos."), o roteiro A abriu com "Hoje você vai entender por quê, em duas partes".
Ele marcou os itens com "O primeiro." e "O segundo.": 2 contagens sem conteúdo e 5 ordinais nus.

Com o exemplo trocado, o roteiro B escreveu "São dois fatos aqui, e o mais forte é que a causa continua no trabalho".
Ele marcou os itens pelo conteúdo ("Agora, o fato da causa."): 0 contagens sem conteúdo e 2 ordinais nus.
Nos dois roteiros, o fechamento usou "Primeira, Segunda, Terceira", porque o bloco de fechamento vem de outro trecho da skill.

Isso responde parte da pergunta 1 da seção 7.3 do guia, pelo lado do modelo.
A contagem vazia é comportamento copiado do exemplo, e some quando o exemplo muda.
O ordinal como marcador é hábito mais fundo, que o exemplo reduz e não extingue.
Se a contagem vazia custa memória ao ouvinte continua sem medida, e é a Fase D com o Dennis que responde.

A contagem vazia vem do exemplo da skill, e muda com ele.

Ponto-chave: a skill mínima funciona como óculos na estrutura e nas marcas, e depende do lint no comprimento da frase.

## 6. Onde mora o modo conversa

A seção 9.4 do guia diz que a Fase B decide se o modo conversa vira seção da clear-listen ou arquivo próprio.
A pergunta 2 da seção 12 diz que só o Dennis decide.
Então esta seção entrega a contagem e uma recomendação, e o Dennis decide.

O conjunto que sobrevive na conversa, com a origem de cada regra:

| Regra do fio | Só clear-read | Só clear-listen | Nas duas | Nova, da seção 9.4 |
|---|---|---|---|---|
| Frase de 8 a 15 palavras, teto 20 | | R2 | | |
| Conector em toda ligação | | | R2b e R5 | |
| Conhecido antes do novo, e o "conhecido" é a frase que a pessoa acabou de dizer | R6e | | | a parte "a frase da pessoa" |
| Significado antes do termo, papel antes do nome | | R8 (quem afirma) | R5a e R4 | |
| Nenhum retrocesso; repetir as palavras da pessoa | | | R6b e R4 | |
| Cada frase é um ponto de parada seguro | R6g | | | |
| Até 3 frases antes de qualquer estrutura; 6 no máximo | R1c (o bloco vira o turno) | | | o número |
| Fechar com o essencial quando passa de 3 frases, como pergunta que devolve o turno | R1b (a função) | R15 (deixar uma coisa) | | a forma "pergunta sem pausa" |
| Redefinir um termo quando ele volta depois de 3 trocas | | R4 (significado por parte) | | o número 3 |
| Anunciar estrutura só quando a frase já entrega conteúdo | | R3 (com limite) | | o limite |
| Nunca numerar; um passo por turno, o próximo quando a pessoa pede | | R21 (limite de 5 passos) | | a regra |
| Esqueleto em uma frase no lugar do visual | | R17, R18, R19 | | |
| Problema com a saída na frase seguinte | R3 | | | |
| Pontuação como único controle de som; nenhuma marca | | o último degrau da escada de degradação | | a regra |

A contagem: 14 regras no fio.
Quatro vêm só da clear-read, seis só da clear-listen, três das duas, e cinco têm uma parte nova que nenhuma skill tem hoje.
Nenhuma regra nova é inteira; cada uma é um limite ou um número sobre uma regra que já existe.

**Recomendação: uma seção da clear-listen, chamada "Conversa", não um terceiro arquivo.**
Três motivos.
As 14 regras são, em maioria, regras da clear-listen com um limite, e o limite se escreve em uma linha ao lado da regra.
Um terceiro arquivo repetiria a seção "Who you are writing for" e as regras de frase, que são o que faz as regras parecerem óbvias.

E a decisão de 13 de outubro, de não dividir um método em dois arquivos, continua valendo.
A conversa é um canal do ouvido, e a clear-listen é a skill do ouvido.

O custo da recomendação: a clear-listen já passa de 5 mil tokens, e a seção "Conversa" precisa entrar no topo, antes da renderização por motor.
Isso só funciona se a Fase E mover a renderização para `references/`, como a seção 2.3 já pede.

Ponto-chave: 14 regras, cinco com uma parte nova, e a recomendação é uma seção no topo da clear-listen.

## 7. Adendo ao inventário da Fase A

A Fase B encontrou quatro seções das skills sem linha no inventário, e um erro numa linha.
Este adendo não reescreve a Fase A; ele acrescenta.

| Seção da skill | O que pede | Executável? | Vale onde? | Veredito |
|---|---|---|---|---|
| clear-read, "How this fits a normal conversation" | A resposta de chat é o produto; a preferência por formatação esparsa fica suspensa enquanto a skill está ativa | Sim | Texto no chat, nos quatro perfis. É a única frase da skill que fala ao Chat simples e ao Agêntico | Mantém. É a frase que o perfil Agêntico mais precisa, porque o Claude Code prefere formatação esparsa por padrão |
| clear-listen, "What arc means in audio" | O arco é reconstruído no início de cada parte, em uma frase | Sim | Áudio longo. Na conversa, o arco encolhe para dentro do turno | Mantém. É a linha de reentrada vista de cima |
| clear-listen, "Two renderings that need no profile" (humano e plain) | O render plain: tirar toda marca, pausa vira reticência, `[key]` vira "O ponto-chave é" | Sim, sem ferramenta | Áudio longo nos perfis Mínimo e Chat simples. É o render da célula "Mínimo por áudio" | Mantém com teste. É a regra que faz a skill mínima funcionar, e nenhum teste a cobre |
| clear-listen, "Step 4: Check what came out" | Medir a taxa real e as pausas; "If you cannot hear audio, say so" | Depende de ouvir ou de ffmpeg | Áudio longo, Projeto e Agêntico | Mantém. A frase "if you cannot hear audio" precisa ser repetida nas regras 9, 11 e 12 |

**Errata da linha R7e (três limites).**
O inventário diz "Testável: lint_guide.py do Projeto".
O cético do perfil Agêntico conferiu o arquivo: ele não tem checagem de icon array, de interativo nem de visual decorativo.
A coluna passa a "Ninguém", e o veredito passa de "mantém" para "mantém sem teste".

**Três fatos conferidos no caminho.**
O lint da clear-read aceita `/dev/stdin`, então ele roda em texto de chat no Agêntico.
A frase "o lint só roda em arquivo", da fase de escrever, é falsa.

A skill escreve `web_search` e a ferramenta do Claude Code chama `WebSearch`; é divergência de nome, não ferramenta ausente.
O `research-basis.md` da clear-listen cita Brann e Sidi como 2025, e o da clear-read como 2024, para o mesmo artigo (volume 95, artigo 102051).

Ponto-chave: quatro linhas a mais, uma errata, e a R7e perde o teste que dizia ter.

## 8. O que vai para as próximas fases, e o que só o Dennis responde

**Para a Fase C (pesquisa), sem pergunta:**

- Os itens da seção 9 do inventário continuam valendo.
- Mais um: a hipótese "a regra executa com template e não com princípio" (seção 5.2) pede a literatura sobre exemplos na instrução (few-shot). A seção 7.1 do guia já a toca nos achados 1 e 3.

**Para a Fase E (proposta), sem pergunta:**

- Os fallbacks das seções 2.2 e 2.3 são o rascunho da seção "Sem raciocínio e sem ferramentas" da proposta 9.6 do guia.
- A camada de processo (proposta 9.1) vira template nos perfis sem raciocínio e critério de conferência nos perfis com raciocínio.
- Os rótulos passam a ser parametrizados por língua. O lint ganha dois testes que falham hoje: rótulo em inglês num texto em português, e analogia na forma "é como" mais verbo.
- O lint da clear-read ganha a frase em negrito na conta de frases do bloco, se ela já não entra.
- A seção "Conversa" entra no topo da clear-listen, se o Dennis aceitar a recomendação da seção 6.

**O que só o Dennis responde:**

- Pergunta 2 da seção 12 (seção ou arquivo próprio): a recomendação está na seção 6, com a contagem.
- Pergunta nova: o perfil Projeto tem Python e ffmpeg ou não? O guia diz não, e as instruções do Projeto dizem sim. A Fase D precisa de uma resposta antes de fixar as condições.
- A pergunta 6 da seção 12 (toda contagem trava?) ganha um dado da segunda rodada, na seção 5.4.
- O roteiro neutro para o golden set da clear-listen continua pendente.

Ponto-chave: a Fase C pode começar, a Fase E tem os fallbacks prontos para avaliar, e duas perguntas esperam o Dennis.
