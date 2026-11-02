# Inventário das regras: clear-read e clear-listen, com veredito

CRIADO: 2026-11-01 (Berlim), no Claude Code, branch `investigacao-2026-11`
FASE: A, do guia `guia-de-investigacao.md` (seção 5)
STATUS: entregue para o Dennis aprovar antes da Fase B

## 0. O que este arquivo é

Este arquivo é a entrega da Fase A.
Ele não propõe nenhuma mudança nas skills.
Ele registra o que existe, o que cada regra pede, que prova cada regra tem, e um veredito por regra.

A ordem de leitura é esta.
A seção 1 registra o estado de partida: os testes que rodaram hoje e o que eles deram.
A seção 2 diz quais conectores de pesquisa este ambiente tem, porque a Fase C depende deles.

A seção 3 é a tabela da clear-read, e a seção 4 é a tabela da clear-listen.
A seção 5 confere os dez vereditos que o guia já tinha como candidatos.
A seção 6 lista o que o inventário achou de errado ou inconsistente no caminho.

A seção 7 é o golden set: cinco trechos publicados que uma versão nova da skill precisa reproduzir.
A seção 8 traz as perguntas de revisão do quarto guia do experimento, o de burnout.
A seção 9 diz o que fica para a Fase B e o que só o Dennis responde.

Os vereditos usam as cinco palavras da seção 5.1 do guia.
São elas: mantém com teste, mantém sem prova (precisa de pesquisa), testa antes de mudar, muda, aposenta.
Nenhuma regra recebeu "aposenta" no texto.
Duas regras recebem "aposenta na conversa", que é um canal, e continuam no áudio longo.

Ponto-chave: este arquivo é o retrato de partida, e nada nas skills muda até o Dennis aprovar o plano.

## 1. Estado de partida: o que rodou hoje e o que deu

A regra 3 da seção 4 do guia pede quatro conjuntos de testes antes de qualquer mudança.
A tabela diz o que cada um deu em 1 de novembro de 2026, neste branch, no commit `96ab426`.

| Conjunto | Comando | Resultado | Nota |
|---|---|---|---|
| Testes do repo | `npm test` | 31 testes, 31 passaram | São os testes do script de versão, não das skills |
| Lint da clear-read, unitários | `python3 plugins/dc/skills/clear-read/scripts/test_lint_clear_read.py` | 98 testes, OK | O guia fala em 100. O número real é 98 |
| Checador de Mermaid | `node plugins/dc/skills/clear-read/scripts/check_mermaid.cjs --self-test` | Passou, depois de `npm install --no-save mermaid@11` | Sem o pacote, o comando falha com "Cannot find mermaid". O Playwright já vem instalado neste ambiente |
| Lint da clear-listen | `python3 -c "import ast; ast.parse(open(...).read())"` | Sintaxe OK | O lint de áudio não tem testes unitários nem `--self-test`. Só dá para conferir a sintaxe e rodar em um roteiro |
| Lint do guia do Projeto | `python3 projeto/lint_guide.py --help` | Roda | A cópia no repo não traz os 24 testes que o guia menciona. Eles vivem na pasta `dev/` da Biblioteca |
| Evals do Projeto | nenhum | Não rodaram | Os dois JSON de evals estão em `projeto/`, mas não há executor no repo. O formato é o do `claude plugin eval`, que precisa do Claude Code com o plugin instalado |

Três coisas saem desta tabela.
Primeiro, o conjunto de regressão real hoje é: 98 testes do lint da clear-read e o self-test do Mermaid.
Segundo, a clear-listen não tem regressão automática, só sintaxe.
Então a Fase E precisa criar testes unitários para `lint_audio_script.py` antes de mexer nele.

Terceiro, o `--self-test` do Mermaid precisa do pacote `mermaid` instalado.
O passo de regressão da Fase E precisa dizer isso.

Ponto-chave: dois conjuntos protegem a clear-read, e nenhum protege a clear-listen de verdade.

## 2. Os conectores de pesquisa estão aqui

O guia diz, na seção 10, que a Fase C roda no app ou no Claude Code com conectores.
Este ambiente do Claude Code tem os seis conectores ligados e com as ferramentas carregadas.

| Conector | Estado | Para que serve na Fase C |
|---|---|---|
| Valency | ligado | Busca por significado em PubMed, arXiv e PsyArXiv |
| PubMed | ligado | Confirmar estudos biomédicos pelo PMID |
| Consensus | ligado | A busca "advance organizers spoken lecture working memory attention deficit" (seção 7.3) |
| Exa | ligado | Busca na web e leitura de páginas |
| Tavily | ligado | Extrair o texto de uma página de DOI |
| Parallel Search | ligado | Busca gratuita, útil quando os outros limitam |

Mais o `WebFetch` nativo, para abrir a página de cada DOI.
Então a Fase C pode rodar inteira aqui, sem voltar ao app.

Ponto-chave: a Fase C não precisa mudar de ambiente.

## 3. Clear-read: a tabela

A clear-read tem 11 regras, 3 fases, 2 modos e uma seção sobre o leitor.
A tabela separa as regras compostas em sub-regras, porque o veredito muda dentro da mesma regra.
Por exemplo, a Regra 6 tem uma sub-regra que o lint pega e outra que só um humano pega.

Como ler as colunas.
"Evidência" cita a fonte como o `research-basis.md` da skill a nomeia, e a certeza entre parênteses.
"Testável" diz quem pega a quebra: o lint, um teste do `tests.md` (marcado T mais o número), um leitor frio, ou ninguém.

"Executável" diz se o modelo aplica a regra enquanto escreve, ou só confere depois.
"Vale onde" usa quatro canais: texto no chat, página HTML, áudio longo, conversa por voz.
"Promessa ou entrega" é a pergunta da tese parte 2: a regra faz o modelo anunciar, ou faz entregar.

### 3.1 Moldura, modos e fases

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| Quem é o leitor | Escrever para um profissional inteligente com pouco orçamento de atenção, cansado, em segunda língua | Perfil montado a partir da literatura: TDAH e leitura, L2, carga cognitiva (alta para os fatos, é moldura e não regra) | Leitor frio, de forma indireta | Sim, é a moldura mental | Todos | Entrega | Mantém. A Fase E adiciona o parágrafo do narrador (seção 9.3 do guia) |
| Dois modos: explicar e reescrever | Decidir antes da Fase 1 qual é a fonte da verdade | Prática do Projeto (baixa) | T1, T6, T13 | Sim | Texto, página. Áudio via clear-listen fase 1. Conversa: neutra | Entrega | Mantém com teste |
| Fase 1: pesquisar sempre | Verificar todo fato antes de escrever, sem exceção | Prática (confiança do leitor); docs da Anthropic, achado 8 da seção 7.1 do guia (esforço baixo responde de memória) | T4, humano. Nenhum lint | Só com ferramenta de busca. Sem ferramenta, a skill diz "não pule" e o modelo pula | Texto e página: ajuda. Conversa de 30 segundos: atrapalha se for "sempre". Perfil mínimo: não roda | Neutra | Testa antes de mudar. Precisa de um caminho sem ferramenta (Fase B, passo 2) |
| Fase 1, privacidade no modo reescrever | Nunca pôr nome, número ou detalhe interno numa busca | Prática (média) | T6 | Sim | Texto, página | Neutra | Mantém com teste |
| Fase 2: desenhar (10 itens) | Conceitos, mapa de jargão, lacunas, arco, títulos-mensagem, exemplos, contrapadrões, plano visual, tipo de bloco, pacote de língua | Mayer e Pilegard 2014, pré-treino d = 0,75 (alta); Schroeder 2018 para o plano visual (alta) | T7, T8, T14 veem o resultado. Ninguém vê o rascunho | É processo, mas é uma lista de 10 itens, não um ciclo | Todos | Entrega | Mantém, e vira ciclo. A seção 9.1 do guia põe a etapa "ler como o leitor" entre desenhar e escrever |
| Fase 3: escrever e rodar o lint | Aplicar as 11 regras, rodar o lint em arquivo, conferir por olho em chat | Prática (média) | 98 testes unitários do lint | O lint só roda em arquivo. Em chat, "por olho" é um desejo escrito | Texto e página. Áudio: outro lint. Conversa: não roda | Neutra | Mantém com teste. A Fase B escreve o que fazer quando o lint não existe |
| O arco (começo, meio, chegada) | O texto vai do que o leitor sabe ao que entende, e a ordem importa | Mar et al. 2021 para narrativa (alta); Wolfe e Woodwyk 2010 para o limite (média) | Leitor frio, T14 | Sim, no item 4 da Fase 2 | Todos | Entrega | Mantém. A Fase E escreve o limite: narrativa ajuda a lembrar fatos, menos a entender mecanismo |

### 3.2 Regras 1 e 2: estrutura e frase

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R1a: abrir com o ponto, em cada nível | 2 ou 3 frases de abertura; cada seção começa pelo seu ponto | Federal Plain Language, frase-tópico antes; COGA 4.4.2; Brann e Sidi 2024 (alta) | Lint: aviso de título de uma palavra. Leitor frio | Sim | Texto, página. Áudio: vira a Regra 1 da clear-listen. Conversa: ajuda em uma frase | Entrega quando a frase já diz o ponto. Promessa quando só anuncia "este texto cobre X" | Mantém com teste. A redação ganha o exemplo: a primeira frase entrega o ponto, não a lista do que vem |
| R1b: "Key point" por seção | Uma frase que começa com "Key point:" no fim de cada seção grande | Brann e Sidi 2024 (recapitulação depois); Adesope 2017 (alta). Cuidado: redundância (Mayer) | Lint: aviso `missing-key-point` | Sim | Texto, página. Áudio: Regra 4 da clear-listen. Conversa: só quando a resposta passa de 3 frases | Entrega | Mantém com teste |
| R1c: blocos pequenos | Um tópico por bloco, 3 ou 4 linhas | COGA 4.4.5 (50 palavras), BDA (alta) | Lint: problema `block over 4 sentences` | Sim | Texto, página. Áudio: vira parte. Conversa: "até 3 frases" (seção 9.4 do guia) | Entrega | Mantém com teste |
| R1d: uma frase por linha, quebra justa entre frases, linha em branco entre tópicos | Produzir o que o meio precisa (dois espaços, `<br>`, soft return) e conferir o render | Prática do Projeto, BDA (média) | T2 (render) | Sim, depende do meio | Texto, página. Áudio: o roteiro já é uma frase por linha. Conversa: não se aplica | Entrega | Mantém com teste |
| R2a: 15 palavras, teto 25, piso 7 | Frases curtas e ligadas, não picadas | Federal 15 a 20; ASD-STE100 20 e 25 (alta) | Lint: problema acima de 25, aviso de média acima de 17 | Sim | Todos. No áudio o alvo cai para 8 a 15 (Regra 2 da clear-listen) | Entrega | Mantém com teste |
| R2b: conectores explícitos em toda ligação | Dizer o porquê, o então, o porém | Yeari et al. 2018, TDAH (média); Federal transition words; Cevasco 2009 e Flowerdew 1995 na fala (média) | Ninguém. O lint não conta conectores | Sim | Todos, inclusive conversa (seção 9.4) | Entrega | Mantém sem prova de teste. Criar um aviso no lint: bloco de 3 frases ou mais sem nenhum conector |
| R2c: sem travessão como junção | Dividir em duas frases ou usar conector | COGA, sem orações encaixadas (média) | Lint: problema `dash` | Sim | Todos | Entrega | Mantém com teste |
| R2d: voz ativa e presente, 3 exceções | Quem faz o quê, num só tempo | COGA 4.4.2, BDA, ASD-STE100, Lei 15.263 (alta) | Lint: aviso de passiva. T9 | Sim | Todos | Entrega | Mantém com teste |
| R2e: sujeito e verbo juntos | Sem oração intercalada entre vírgulas | COGA 4.4.3, Lei 15.263 (alta) | Lint: aviso `inserted-clause` | Sim | Todos. É a Regra 2 da clear-listen | Entrega | Mantém com teste |
| R2f: o verbo, não o substantivo feito dele | "Analisar", não "fazer uma análise" | Federal hidden verbs, Lei 15.263 (alta) | Lint: aviso `hidden-verb` | Sim | Todos | Entrega | Mantém com teste |

### 3.3 Regras 3, 4 e 5: problema, conhecimento assumido, termos

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R3: problema mais contrapadrão | Nunca nomear um problema sem a solução, com exemplo "fraco versus forte" | Prática de exemplos resolvidos (worked examples), sem DOI no `research-basis.md` (baixa) | Ninguém. Leitor frio | Sim | Todos | Entrega. Um problema sem solução é uma gaveta aberta | Mantém sem prova (precisa de pesquisa). A literatura de worked examples existe (Sweller) e falta citar |
| R4: nenhum conhecimento de domínio assumido | Tratar o leitor como iniciante inteligente em qualquer área especializada | COGA palavras claras; Mayer pré-treino (alta para o pré-treino) | T3, leitor frio | Em parte. Precisa de um modelo do que o leitor sabe | Todos. Conversa: redefinir um termo quando ele volta depois de 3 trocas | Entrega | Mantém. Precisa do exemplo de calibração que a R8b também pede |
| R5a: significado antes, termo entre parênteses | Só usar a sigla depois de apresentar assim | COGA sigla no primeiro uso; vocabulário L2 (alta) | Lint: aviso `acronym-without-full-name`. T3 | Sim para siglas. Para nome próprio, a conversa mostrou que não executa ("Mayer mostrou") | Todos. No áudio a definição vira frase própria | Entrega. O nome antes do papel é promessa | Mantém, e estende para nome de pessoa, estudo, norma e lei (seção 9.2 do guia). O teste que falha hoje: o lint aceita "Mayer mostrou que" |
| R5b: uma palavra, um significado | Nunca trocar o termo por sinônimo | ASD-STE100, L2 (alta) | Ninguém automático. T3 e T15, humano | Sim, com o mapa de jargão da Fase 2 | Todos | Entrega | Mantém sem teste automático. Candidata: conferir o glossário pelo lint, que a pesquisa consolidada já pedia |
| R5c: termos técnicos ficam em inglês dentro do português | API, deploy, cache, com o significado em português na primeira vez | Prática do leitor (baixa) | T17, leitura | Sim | Texto e página em português. Áudio: a fase 2 da clear-listen decide o nome falado | Entrega | Mantém |
| R5d: a analogia paga o empréstimo | Linha "Onde a analogia falha:" antes do próximo título | Prática do Projeto; o `research-basis.md` admite que não há estudo (baixa) | Lint: problema `analogy-without-limit`. T16 | Sim | Todos | Entrega | Mantém com teste. Pesquisa opcional: Muller 2008 (refutar a concepção errada) toca o tema |

### 3.4 Regra 6: ensinar no caminho e zero retrocesso

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R6a: ensinar no caminho, "Key terms" quando há muitos termos | Explicar cada conceito novo em 1 a 3 frases com exemplo, e repetir a definição quando volta | Mayer e Pilegard 2014, pré-treino d = 0,75; COGA Objetivo 6 (alta) | Leitor frio, T14. O lint não vê | Sim | Todos | Entrega | Mantém com teste. Nota: no Projeto, "Key terms" virou "O chão", que é produto |
| R6b: não confiar na memória, sem "como mencionado" | Repetir o contexto em vez de apontar para trás | COGA Objetivo 6; Federal, referências cruzadas; Monk, Trafton e Boehm-Davis 2008 (alta e média) | Lint: problema `backward-reference` | Sim | Todos. Conversa: ajuda muito | Entrega | Mantém com teste |
| R6c: nível 1, nome mais significado na primeira menção de cada bloco | "P1 (cache antes do deploy) resolve isso" | Monk, Trafton e Boehm-Davis 2008, retomada depois de interrupção (média, é analogia de laboratório) | Lint: problema `bare-label`. T15 | Sim | Todos. Áudio: Regra 4 da clear-listen | Entrega | Mantém com teste. É a regra número um do Dennis |
| R6d: nível 2, forma curta dentro do mesmo bloco | Depois da primeira menção, o pronome ou a sigla servem | Mesma fonte, prática (média) | Ninguém. O lint não distingue níveis | Sim | Todos | Entrega | Mantém |
| R6e: conhecido antes do novo | Começar a frase pelo que o leitor já tem, terminar pelo novo | Haviland e Clark 1974, 150 a 200 ms (leitura, média); Clifton e Frazier 2004 (depende da construção) | Ninguém. T15 diz "precisa de leitura humana" | Não enquanto escreve. A conversa de 1 de novembro mostrou que ela só confere depois | Todos. Conversa: seção 9.4 | Entrega. É a base do atalho do Achado 3 (apontar para o que o leitor já tem) | Mantém, e vira processo (seção 9.1 do guia). O teste que falha hoje: um eval em chat simples que produz "Mayer mostrou" com a skill carregada |
| R6f: cada seção se sustenta sozinha | A primeira linha diz em uma oração o que a seção constrói | Brann e Sidi 2024, orientação antes de cada etapa (média) | Leitor frio por seção. O lint não vê | Sim | Texto, página, áudio (linha de reentrada da Regra 1 da clear-listen). Conversa: não se aplica | Entrega | Mantém com teste. Golden set, trecho G2 |
| R6g: blocos terminam em pensamento completo | Todo ponto de parada é seguro | Monk 2008 (média) | Ninguém | Sim | Todos | Entrega | Mantém |

### 3.5 Regra 7: o plano visual

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R7a: o teste das 4 perguntas | Contar os "sim" e decidir: fundamental, reforço ou nada | Schroeder 2018, construir vence estudar (alta). Os limiares 3-4, 1-2, 0 são heurística (baixa) | T7, T8 | Sim, na Fase 2. É a única regra já escrita como processo | Página. Texto no chat com Mermaid. Áudio: Regra 17 da clear-listen. Conversa: atrapalha | Neutra | Mantém com teste. Os números são padrões a ajustar, não constantes |
| R7b: "How to read" mais uma frase de conclusão | Toda figura ganha as duas linhas | Schroeder 2018; atenção dividida (média) | Lint: problema `visual-without-how-to-read`, aviso sem conclusão | Sim | Página, texto | A conclusão é entrega. "How to read" sem conclusão é promessa | Mantém com teste. Golden set, trecho G5 |
| R7c: a forma pelo conteúdo | Fluxo vira diagrama; números viram tabela; datas viram lista | Prática; Berney e Bétrancourt 2016 para animação (média). Adendo 2: o Projeto derrubou o Mermaid para sequências em 24 de setembro de 2026 | `check_mermaid.cjs`, em parte | Sim | Página | Promessa: manda desenhar uma sequência, e o desenho repete a prosa | Muda (adendo 2, mudança 20 da proposta): nunca desenhar uma sequência, SVG inline para grafos, tabela de forma por conteúdo |
| R7d: construir para o celular | Rótulo com 25 caracteres ou menos, 2 nós lado a lado | Prática, tela de 390 px (baixa) | `check_mermaid.cjs` e seu `--self-test` | Sim | Página | Neutra | Mantém com teste. Documentar que o self-test precisa de `npm install mermaid@11` |
| R7e: três limites | Nada decorativo; 1 interativo por documento; icon array em todo risco de saúde | Sundararajan e Adesope 2020, direção confirmada e número não (média); Berney 2016; Garcia-Retamero e Cokely 2017 (alta para o icon array) | `lint_guide.py` do Projeto, não da skill | Sim | Página | Entrega | Mantém. O icon array tem a prova mais forte da regra |

### 3.6 Regras 8 a 11: profundidade, tom, língua, procedimentos

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R8a: profundidade em passos pequenos, nunca uma parede | Passo a passo e exemplo antes da teoria | Mayer e Pilegard 2014, segmentação d = 0,79 (alta) | Lint: bloco acima de 4 frases, em parte | Sim | Todos | Entrega | Mantém com teste |
| R8b: calibrar ao que o leitor já sabe | Dentro da área dele, encurtar ou colapsar o básico | Kalyuga et al. 2003, reversão da expertise (média; o DOI não foi confirmado) | Ninguém. "Profundidade real" é adjetivo | Precisa de contexto: a Biblioteca, o `knowledge_state`. Então depende do perfil | Todos. Conversa: decide se redefine ou não | Neutra | Muda. Precisa de regra operacional com exemplo: quando colapsar, e o que fazer sem contexto |
| R9: tom calmo, preciso, sem performance | Texto para leitura silenciosa, sem personalidade | "Pesquisa de leitura em tela contra áudio", sem fonte nomeada (baixa) | Ninguém. São adjetivos | Vago | Texto, página. Áudio tem a Regra 10 própria. Conversa: "calmo" pode virar monótono | Neutra | Muda. Reescrever com exemplo de entrada e saída (achado 1 da seção 7.1 do guia), e achar a fonte ou cortar a frase |
| R10a: palavras simples, sem idioma nem metáfora, glosa na língua nativa | Plain words, com o termo exato quando ele é o certo | Linguagem figurada em TDAH (alta); frequência de vocabulário em L2 (alta) | Ninguém automático. T13 | Sim | Todos | Entrega | Mantém. Teste humano |
| R10b: forma simples, conteúdo inteiro | Nenhuma ideia, número ou ressalva cai | Fórmulas de legibilidade não medem compreensão (alta) | T13 | Sim | Todos | Entrega | Mantém com teste |
| R10c: pacotes de língua | Ler `lang-pt-br.md` ou `lang-en.md` antes de escrever | Lei 15.263 de 2025; Federal Plain Language Guidelines (alta, como norma) | T17 e as listas `LANG_PACKS` do lint | Sim | Texto, página. Áudio: não se aplica | Neutra | Mantém com teste |
| R10d: número com âncora em palavras, mês por extenso | "permissão 600 (só o dono lê e escreve)" | COGA 4.4.13; Garcia-Retamero e Cokely 2017 (alta) | Ninguém no lint da skill. O lint do Projeto pega parte | Sim | Todos. Áudio: Regra 7 da clear-listen | Entrega | Mantém. Candidata a aviso no lint: número sem palavra ao lado |
| R10e: negrito em uma linha por bloco, sem itálico, sem Bionic Reading | A trilha de negritos conta a história | BDA (prática); Snell 2024 e Parker et al. 2026 para Bionic (alta) | Ninguém | Sim | Texto, página | Neutra | Mantém |
| R11a: procedimento com forma própria | Lista numerada, objetivo antes da ação, até 7 passos, estágios | COGA 4.4.9; ASD-STE100; Google e Microsoft (alta) | T5 | Sim | Texto, página. Áudio: Regra 21 da clear-listen (mais de 5 passos vai para o guia). Conversa: atrapalha, porque "primeiro, segundo" trava | Entrega | Mantém com teste. Registrar o conflito com a conversa (seção 9.4: nunca numerar) |
| R11b: "se, então" explícito, tabela quando há vários ramos | Nenhuma condição escondida no meio da frase | COGA 4.4.9 (alta) | T5 | Sim | Texto, página | Entrega | Mantém |
| R11c: código em bloco próprio, com uma linha de explicação, nunca só em imagem | O leitor pode não ver a imagem | Google e Microsoft, acessibilidade (alta) | Ninguém | Sim | Texto, página | Entrega | Mantém |

Na clear-read, 33 das 40 linhas ficam como estão.
Quatro ganham processo ou extensão, e duas mudam de redação: a calibração ao leitor e o tom.
A fase de pesquisar sempre precisa de teste antes de mudar.

Ponto-chave: a clear-read quase não muda de regra, e muda de processo.

## 4. Clear-listen: a tabela

A clear-listen tem 21 regras, 4 fases, uma tabela de intents com 6 regras, e uma fase de renderização com 5 regras.
O lint de áudio tem 12 checagens, e a coluna "Testável" nomeia cada uma quando ela existe.

### 4.1 Moldura e fases

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| Quem ouve | O leitor da clear-read, de fones, na língua nativa, com mais carga de atenção | `research-basis.md` seções 1 a 3 (alta e média) | Indireto | Moldura | Áudio longo, conversa | Entrega | Mantém |
| Cinco fatos sobre ouvir | A fala some; o ritmo não é do ouvinte; a mente vagueia mais; a estrutura visual sumiu; a voz carrega sentido | Clinton-Lisell 2022, g = 0,07 (alta); Varao Sousa 2013; Brann e Sidi (média) | Indireto | Moldura | Áudio longo, conversa | Entrega | Mantém. É a parte que faz as regras parecerem óbvias |
| Para que serve o áudio | Primeira passada ou revisão, nunca substituto. Cabe: ideia principal, até 3 ou 4 itens, 2 opções, 1 número por frase | Leahy e Sweller 2016 (alta, uma tarefa); pesquisa consolidada, decisão 4 | T2, T3 | Sim | Áudio longo. Conversa: não se aplica | Entrega | Mantém com teste. Ver a inconsistência "1 ou 2 números por frase" na seção 6 |
| Duas camadas: intents neutros e perfil de engine | O roteiro nunca tem a sintaxe de um motor | Decisão do Dennis em 8 de outubro; prática (média) | Hoje ninguém. "Nenhum intent neutro sobra no render" é lintável | Sim | Áudio. Conversa: o modelo só entrega texto, então a camada não existe | Neutra | Mantém com teste a criar: um lint do texto renderizado |
| Fase 1: fonte verificada | Nenhum fato novo; a fonte é um texto já conferido | Prática (média) | T3 | Sim | Áudio | Neutra | Mantém |
| Fase 2: desenhar (8 itens) | Conceitos, partes, ideia central, nomes falados, cortes e cobertura, perguntas, entrega, meio, tamanho | Rey et al. 2019, segmentação (alta); 160 palavras por minuto é conversão (baixa) | T3; o lint vê parte | É lista, não ciclo | Áudio longo. Conversa: só "nomes falados" e "ideia central" | Entrega | Mantém, e vira ciclo com "ouvir como o ouvinte", igual à seção 9.1 do guia |
| Formato do roteiro | Uma frase por linha, `#` para nota, intent entre colchetes, `Guia:` e `Curioso:`, "Parte um de três", `# closing` | Convenção que o lint exige (média) | Lint: todas as 12 checagens dependem dele | Sim | Áudio | Neutra | Mantém com teste. Os marcadores antigos `[short pause]` ficam como legado aceito |

### 4.2 Regras 1 a 8: o que o roteiro diz

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R1a: ideia central nos primeiros 30 segundos, e de novo no início de cada parte | A mente que vagueia cedo perde a base | Divagação no começo prevê pior compreensão (média); Brann e Sidi (média) | Ninguém. Leitor frio | Sim | Áudio longo. Conversa: a primeira frase já entrega a resposta | Entrega | Mantém com teste a criar |
| R1b: "Parte N de M" no começo de cada parte | O mapa falado | Sinalização (Mayer); Lorch 2012 e Chen 2018, prévia em áudio (média) | Lint: `no part markers`, `part too long` | Sim | Áudio longo: ajuda quem volta de uma divagação. Conversa de 30 segundos: ruído | Promessa (anuncia um esqueleto) | Mantém no áudio longo com teste; aposenta na conversa (seção 5.2 do guia, confirmado) |
| R1c: linha de reentrada e objetivo da parte em uma frase | Uma frase que faz sentido sem as partes anteriores | Brann e Sidi (média) | Ninguém | Sim | Áudio longo. Conversa: não se aplica | Entrega | Mantém |
| R1d: parte de 3 a 4 minutos, nunca acima de 5; não encher | Uma parte é um conceito, não um tempo | Rey et al. 2019 (alta para segmentar; o tamanho é padrão a testar, baixa) | Lint: `part chars > 4800` | Sim | Áudio longo | Neutra | Mantém com teste. T9 decide 2 contra 4 minutos |
| R1e: roteiro de uma parte só pula o "Parte um de um" | Anunciar "parte um de um" é ruído | Prática | Lint: `SINGLE_MAX_WORDS`, pergunta obrigatória | Sim | Áudio curto | Entrega | Mantém com teste |
| R2: 8 a 15 palavras, teto 20, sem parênteses | Uma ideia por frase, dita num fôlego | Informação transitória; memória de trabalho em TDAH (alta e média) | Lint: `sentence > 20 words`, `parentheses` | Sim | Áudio longo e conversa: ajuda | Entrega | Mantém com teste |
| R3: dizer a estrutura | Anunciar a contagem ("São três motivos"), marcar cada item, marcar cada virada, recapitular a cada 3 itens | Sinalização (Mayer); Lorch 2012 e Chen 2018 (prévia ajuda a estrutura lembrada; não mediu carga nem TDAH); Flowerdew e Tauroza 1995 (média) | Ninguém. O lint não checa | Sim | Áudio longo: ajuda, provável. Conversa: só quando a frase que anuncia já entrega conteúdo | Promessa, na forma atual | Testa antes de mudar (Fase D, pergunta 1 da seção 7.3 e pergunta 6 da seção 12). Hipótese a testar: "são três causas, e a mais forte é o preço" |
| R4: repetir de propósito | Repetir o nome, não "isso"; o significado na primeira vez em cada parte; o ponto-chave em outras palavras; nunca apontar para trás | Informação transitória; COGA Objetivo 6 (média) | Lint: `backward reference` | Sim | Áudio longo. Conversa: fechar com "lembra que..." (seção 9.4) | Entrega | Mantém, e aproxima do "sabe aquilo que ela fez?". Teste: eval com fechamento em pergunta contra fechamento em afirmação (pergunta 2 da seção 7.3) |
| R5: dizer cada "porque" | A ligação entre fatos é a primeira coisa que o ouvinte distraído perde | Yeari et al. 2018, TDAH (média); Cevasco 2009; Flowerdew 1995 (média) | Ninguém | Sim | Áudio longo e conversa: ajuda | Entrega | Mantém. Mesmo aviso de conectores que a R2b da clear-read |
| R6: fazer o ouvinte recuperar na cabeça | Prequestões com pausa; uma pergunta de recordação por parte com pausa de 4 a 6 segundos; fechar com "Sem voltar, quais foram as ideias?" | Szpunar, Khan e Schacter 2013 (alta para aprender, provável para atenção); Knouse 2011 e Minear 2023, TDAH (média). A pausa de 4 a 6 segundos é padrão (baixa) | Lint: `no recall question near end`, `more than two questions` | Sim | Áudio longo: ajuda. Conversa: a pessoa faz a própria pergunta; o modelo fecha com pergunta, sem pausa | Entrega. A pergunta pede recuperação | Mantém no áudio longo com teste; muda na conversa (seção 5.2 do guia, confirmado) |
| R7: poucos números, por extenso | No máximo 1 por frase, arredondado, com âncora; sem URL, citação ou tabela lida | Carga de memória de trabalho; prática de rádio (média) | Lint: `digit`, `symbol or URL` | Sim | Áudio longo e conversa | Entrega | Mantém com teste. Resolver "1 número" (skill) contra "até 2" (pesquisa consolidada 8.4) |
| R8: falar com uma pessoa | "Você", voz ativa, presente, dizer quem afirma ("um estudo de 2024 mostra") | Personalização, Ginns, Martin e Marsh 2013 (citação não confirmada, média) | Ninguém | Sim | Áudio longo e conversa | Entrega. "Um estudo de 2024 mostra" é o papel antes do nome | Mantém. A Fase C confirma a citação de Ginns 2013 |

### 4.3 Regras 9 a 15: a voz

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R9: ritmo moderado, pausas entre ideias | 160 palavras por minuto (150 a 175); `[pause short]` meio segundo; `[pause long]` 2 segundos; lento só no `[key]` | Rodero 2016 em espanhol, convertido por sílaba (média para baixa); Murphy et al. 2022, até 1,5 vez (média) | T6: medir palavras por minuto | É do motor, não do texto | Áudio longo. Conversa: o motor decide | Neutra | Mantém como padrão a medir (T8). Não é regra de escrita |
| R10: expressão moderada e variada | Trocar o tom entre partes; 1 ou 2 palavras de ênfase por frase; um `[stress]` por parte | Rodero et al. 2022, equilíbrio expressivo (média) | Lintável e não lintado: contar `[key]` e `[stress]` por parte | Sim | Áudio longo | Neutra | Mantém. "Moderado" é adjetivo e pede exemplo (achado 1 da seção 7.1). Candidato a lint: mais de um `[key]` por parte |
| R11: só voz, sinal limpo | Sem música, ambiente, efeito ou ruído sob a voz | Coerência (alta); fala em ruído em TDAH, Michalek 2014 e Blomberg 2021 (alta) | É produção, não texto | Sim | Áudio longo | Neutra | Mantém. É a regra com base direta mais forte da skill |
| R12: uma voz limpa e constante por papel; medir a taxa real | Conferir a voz em português por ouvido; palavras divididas por minutos depois de gerar | TTS igual a humano em duas vezes, em inglês (média) | T6 | Sim | Áudio longo | Neutra | Mantém |
| R13a: a segunda voz precisa merecer o lugar | O Curioso pergunta "por quê" antes, dá voz ao erro comum, sem conversa fiada nem "Exato!" | Craig et al. 2000; Driscoll 2003; Muller e Sharma 2007 e 2008 (alta) | Lint: `agreement noise or filler line`. T7 | Sim | Áudio longo. Conversa: a pessoa é o Curioso, então a regra vira "responda à pergunta funda" | Entrega | Mantém com teste |
| R13b: a troca de voz puxa a atenção de volta, e a memória melhora logo depois | Pôr a frase importante logo depois da troca; vozes de tom bem diferente; segunda voz cedo | O `research-basis.md` cita Potter 2000, Potter, Lang e Bolls 2008 e Potter, Lynch e Krause 2015, em rádio, lidos só como resumo (média). A seção 7.2 do guia não achou a prova | Ninguém | Sim | Áudio longo | Neutra | Mantém sem prova. A Fase C abre Potter 2000 (DOI 10.1207/S1532785XMEP0202_3) e Potter 2008 (DOI 10.1027/1864-1105.20.4.168) |
| R14: novidade pela forma, nunca por conteúdo extra; rodar os recursos | Pergunta, exemplo, contraste, troca de voz; nenhum detalhe que não sirva a um conceito | Sundararajan e Adesope 2020 (direção confirmada); habituação (média) | Ninguém | Sim | Áudio longo. Conversa: em parte | Entrega | Mantém |
| R15: fechar bem, e oferecer uma revisão curta | A última parte liga os conceitos e deixa uma coisa; resumo de 2 a 4 minutos para depois | "Estudo de reassistir", sem DOI (baixa); divagação no começo (média) | Ninguém | Sim | Áudio longo | Entrega | Mantém. A Fase C acha a fonte do "estudo de reassistir" ou corta a frase |

### 4.4 Regras 16 a 21: o que o olho tinha e o ouvido não tem

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| R16: toda ideia principal tem uma frase falada | Mesmo a que vive numa tabela ou num gráfico; leitor frio acerta 8 em 10 | Matriz de cobertura, pesquisa consolidada 8.3 (prática) | T3 e leitor frio | Sim | Áudio longo | Entrega | Mantém com teste |
| R17: estruturas, não pixels | "Imagine três caixas"; até 3 ou 4 itens; sem cor, posição ou tamanho | Memória de trabalho (prática) | Ninguém | Sim | Áudio longo | Entrega | Mantém |
| R18: tabela em três movimentos | O que se compara, o vencedor por critério, o ponteiro para o guia | Prática | Ninguém | Sim | Áudio longo | Entrega | Mantém |
| R19: gráfico em quatro frases | O que mostra, a escala, o padrão, a conclusão | Prática | Ninguém | Sim | Áudio longo | Entrega | Mantém |
| R20: risco em frequência natural com denominador | "Treze em cada cem", nunca "o dobro" sozinho | Garcia-Retamero e Cokely 2017 (alta) | Lint: `digit` força palavras, mas não pega "o dobro" sem base | Sim | Áudio, conversa e texto (é a R7e da clear-read) | Entrega | Mantém com teste. Candidato a lint: "o dobro", "por cento maior" sem "em cada" na mesma frase |
| R21: limites honestos, ditos em voz alta | Para código, mais de 5 passos, tabela maior que 3 por 3, rede com mais de 6 nós: conclusão, padrão e onde está o resto | Prática | Ninguém | Sim | Áudio longo | Entrega | Mantém |

### 4.5 Intents, renderização e checagem

| Regra | O que ela pede | Evidência (certeza) | Testável? | Executável? | Vale onde? | Promessa ou entrega? | Veredito |
|---|---|---|---|---|---|---|---|
| Vocabulário de intents (tabela) | Tom, `[key]`, `[stress]`, três pausas, `[say]`; em inglês, entre colchetes | Decisão de 8 de outubro; R10 (média) | Lintável e não lintado: hoje o lint ignora tudo entre colchetes, então `[whispers]` num roteiro neutro passa | Sim | Áudio longo | Neutra | Mantém com teste a criar: lint do vocabulário de intents |
| Intent nunca carrega conteúdo | Se o meio derruba o intent, o ouvinte perde só polimento | Prática (média) | Leitor frio com o roteiro sem intents | Sim | Áudio longo | Entrega | Mantém |
| Não inventar intent; nunca abrir parte com lento; papel não é intent; performance fora do método | Quatro proibições, cada uma com o motivo | Prática; R10 (média) | Lintável e não lintado | Sim | Áudio longo | Neutra | Mantém com teste a criar |
| Fase 4, passo 1: descobrir o meio e pegar o perfil | Nunca renderizar de memória; perfil do modelo exato; sem perfil, construir um; sem nada, render "plain" | Motores mudam entre modelos e meses (prática) | Ninguém | Precisa de contexto (o playbook) ou de ferramenta (guia do modelo) | Áudio longo | Neutra | Mantém. A Fase C compara com a skill oficial da ElevenLabs (seção 7.4) e decide o que vira ponteiro |
| Fase 4, passo 2: o que um perfil responde (12 perguntas) | Tom, colchetes desconhecidos, pausa, ênfase, pronúncia, velocidade, vozes por chamada, números, limites, instável, mapa | Prática | Ninguém | Sim | Áudio longo | Neutra | Mantém, e move para `references/`. É o fim do arquivo, e passa do teto de 5 mil tokens |
| Fase 4, passo 3: mapear cada intent ou degradar pela escada | Primeira escolha, depois, último degrau sempre possível | Prática | "Nenhum intent sobra" é lintável | Sim | Áudio longo | Neutra | Mantém com teste a criar |
| Fase 4, 5 regras de render e o relatório | Nada sobra; marcas mudam, palavras não; cada chamada começa do zero; limites do motor; relatório de 3 listas | Prática | Lintável | Sim | Áudio longo | Neutra | Mantém com teste a criar |
| Checar antes de gerar | Lint no roteiro neutro, ler em voz alta, cobertura, checar o render | Prática | T1, T3 | Sim | Áudio longo | Neutra | Mantém |

Na clear-listen, 30 das 35 linhas ficam como estão.
Duas mudam de status só na conversa: o "Parte N de M" e a pergunta de recordação com pausa.
Uma pede teste antes de mudar: dizer a estrutura.
Sete têm testes fáceis de criar que hoje não existem.

Ponto-chave: a clear-listen fica inteira no áudio longo, e perde três regras na conversa.

## 5. Os dez vereditos da seção 5.2 do guia, conferidos

| Regra | Veredito provável no guia | Veredito desta fase | O que mudou |
|---|---|---|---|
| clear-listen R3, dizer a estrutura | testa antes de mudar | Confirmado | A prova a favor (Lorch 2012, Chen 2018) mediu estrutura lembrada, não carga. A pergunta 6 da seção 12 decide a forma da hipótese |
| clear-listen R1, "Parte N de M" | mantém no áudio, aposenta na conversa | Confirmado | A Regra 1 tem cinco sub-regras, e só o "Parte N de M" é promessa. A ideia central e a reentrada ficam na conversa |
| clear-listen R6, pergunta com pausa | mantém no áudio, muda na conversa | Confirmado | Sem a pausa, o fechamento com pergunta vira a R4 "lembra que..." |
| clear-read R6, conhecido antes do novo | mantém, e vira processo | Confirmado | É a única regra da clear-read que o inventário marca "não executável enquanto escreve" |
| clear-read R5, termo com significado antes | mantém, e estende para nomes e códigos | Confirmado | O lint pega sigla sem nome e não pega "Mayer mostrou". Esse é o teste que falha hoje |
| clear-read R1, "Key point" | mantém | Confirmado | Com um cuidado: a redundância (Mayer). O "Key point" compressa, não repete |
| clear-listen R4, repetir de propósito | mantém, aproxima do "lembra que" | Confirmado | Vira a pergunta 2 da seção 7.3, para a Fase D |
| clear-listen R13, o Curioso | mantém, com uma conferência | Confirmado, e a conferência tem alvo | O `research-basis.md` cita Potter 2000 e Potter 2008 para a troca de voz. A Fase C abre os dois |
| Instruções, "O chão" e "Para este guia ficar" | muda | Confirmado, com contagem | "O chão" aparece em 8 linhas das instruções e "Para este guia ficar" em 3. O guia dizia 6 lugares |
| Seção "Who you are writing for" | mantém | Confirmado | Nas duas skills |

Ponto-chave: os dez candidatos ficaram de pé, e dois ganharam alvo concreto (o teste que falha e a fonte a abrir).

## 6. O que o inventário achou no caminho

Estas são inconsistências ou lacunas que apareceram ao ler tudo junto.
Nenhuma delas é uma proposta de mudança.
Cada uma entra na Fase C ou na Fase E com o dono certo.

1. **Os números do guia sobre os testes estão um pouco fora.** O lint da clear-read tem 98 testes unitários, não 100. Ele reporta 16 tipos de achado (7 problemas e 9 avisos), e o guia fala em 15 regras. O lint de áudio tem 12 checagens, e esse número confere.
2. **"Um número por frase" contra "até dois".** A clear-listen Regra 7 diz "no máximo 1 número por frase". A pesquisa consolidada, seção 8.4, diz "até 2 números por frase" e propõe uma Regra 20 com "at most 2". A skill venceu na prática, e o motivo não está escrito em nenhum dos dois lugares.
3. **O mesmo estudo com dois anos.** O `research-basis.md` da clear-read cita Brann e Sidi 2024. O da clear-listen cita Brann e Sidi 2025, com o mesmo volume e número de artigo (95:102051). A Fase C fixa o ano certo nos dois.
4. **A fonte da troca de voz existe, só não foi aberta.** A seção 7.2 do guia diz que a busca não achou prova para "a troca de voz reseta a atenção". O `research-basis.md` da clear-listen cita três artigos de Potter, com DOI, lidos como resumo. A conferência na fonte é possível e tem alvo.
5. **Duas regras são adjetivos sem exemplo.** A clear-read Regra 9 ("calmo, preciso") e a Regra 8b ("profundidade real", "calibrar") não têm exemplo de entrada e saída. A clear-listen Regra 10 ("expressão moderada") também não. O achado 1 da seção 7.1 do guia diz que o modelo de hoje precisa do exemplo.
6. **Nenhuma caixa alta nas duas skills.** A busca por "IMPORTANT", "NEVER", "ALWAYS", "CRITICAL" e "MUST" em maiúsculas não achou nada nos dois `SKILL.md`. O achado 4 da seção 7.1 não se aplica às skills. As instruções do Projeto não foram checadas, porque ficam fora deste inventário (assunção 2 do guia).
7. **As duas skills passam do teto de 5 mil tokens.** Pela conta de 4 caracteres por token, a clear-read tem cerca de 7.350 tokens e a clear-listen cerca de 8.050. Na clear-listen, o fim do arquivo é a Fase 4 (renderização por motor) inteira. Na clear-read, o fim é a tabela de arquivos e o lint.
8. **Sete regras da clear-listen são fáceis de lintar e não são.** São estas: vocabulário de intents, mais de um `[key]` por parte, abrir parte com direção lenta, intent sobrando no render, risco relativo sem base. Mais as duas da renderização: nenhum intent sobra, e as palavras não mudam. Cada uma vira um teste que falha hoje, o que a regra 2 da seção 4 do guia pede.
9. **O lint do guia e os evals não têm executor no repo.** A cópia de `lint_guide.py` está aqui, mas os 24 testes dele ficaram na Biblioteca. Os evals da clear-listen estão em JSON, mas apontam para `evals/evals.json` dentro da skill, que não existe, e o `.gitignore` ignora `**/evals/`. É a pergunta 8 da seção 12.
10. **A clear-read Regra 11 e a conversa discordam sobre numerar.** A Regra 11 pede lista numerada para procedimentos, e a seção 9.4 do guia propõe "nunca numerar para quem disse que numeração trava". As duas podem estar certas, porque uma é para o olho e a outra para o ouvido. A matriz da Fase B registra esse par.
11. **A citação de Ginns, Martin e Marsh 2013 continua não confirmada** no `research-basis.md` da clear-listen, e ela sustenta a Regra 8 (falar com uma pessoa).

Ponto-chave: onze achados, e os mais caros são o teto de tokens e a ausência de testes na clear-listen.

## 7. Golden set: cinco trechos que não mudam

A regra 4 da seção 4 do guia pede cinco trechos de guias publicados que são exemplos do que está certo.
A versão nova de cada skill precisa reproduzir o mesmo comportamento neles.
Cada trecho traz a URL, a seção, o texto como está publicado, as regras que ele mostra, e o que um leitor frio precisa acertar.

Os quatro guias do experimento estão representados: burnout, suplementos, DuckDB e ElevenLabs.
Nenhum roteiro de áudio está no repo, então a clear-listen não tem trecho dourado ainda.
A seção 9 diz o que o Dennis precisa exportar para isso.

### G1: a abertura que entrega, e a analogia que paga o empréstimo

Guia: Burnout, estresse e férias, https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj, seção `s30` ("Em 30 segundos").

> Férias aliviam de verdade, mas o efeito some de uma a quatro semanas depois da volta, porque a causa fica esperando.
> **O que resolve burnout é mudar o que o causa no trabalho e recuperar o corpo, com acompanhamento quando o quadro é clínico.**
> Pense no cache que você conhece: limpar o cache alivia o sintoma, mas a consulta lenta continua lá.
> **Onde a analogia falha:** o cache se limpa com um comando, e a recuperação do corpo leva semanas.

E, no bloco seguinte do guia:

> Ponto-chave: férias são manutenção; a cura passa pelo trabalho.

Regras que ele mostra:

- R1a (abrir com o ponto): a primeira frase já entrega a resposta.
- R2b (conectores): o "porque" e o "mas" estão escritos.
- R5d (a analogia paga o empréstimo): a linha "Onde a analogia falha" vem logo depois.
- R10e (negrito): uma linha em negrito por bloco.
- R1b (Key point) fecha a seção.
- R6e (conhecido antes do novo): "o cache que você conhece" aponta para o que o leitor já tem.

Não mude isto: a abertura responde a pergunta antes de anunciar o que vem.
A analogia vem de casa (IT) e tem a linha de limite logo depois.

Leitor frio acerta: "quanto tempo dura o efeito das férias?" e "por que o efeito some?".

### G2: a seção que se sustenta sozinha

Guia: Burnout, estresse e férias, mesma URL, seção `c2`, primeiro bloco.

> A ideia central aqui é que burnout não é cansaço grande, e sim o resultado de um desequilíbrio que dura.
> Os três lados do desequilíbrio: exigências altas, recursos baixos e nenhuma recuperação no meio.
> Você já sabe que estresse crônico é a exigência que não para. Agora, o que ele faz com o tempo.

Regras que ele mostra:

- R6f (cada seção se sustenta sozinha): a primeira linha diz o que a seção constrói.
- R6e (conhecido antes do novo): "você já sabe que..." vem antes do novo.
- R1a (abrir com o ponto): a ideia central está na primeira frase.
- R6c (nível 1 do zero retrocesso): "estresse crônico" vem com o significado, "a exigência que não para".

Não mude isto: toda seção de conceito dos guias abre com "A ideia central aqui é".
Quando a seção depende de outra, ela abre com "Você já sabe que... Agora...".
É a forma publicada da linha de reentrada.

Leitor frio acerta, lendo só esta seção: "o que é estresse crônico?".

### G3: o termo com o significado antes, e a confusão nomeada

Guia: Suplementos todo dia, versão 2, https://claude.ai/artifact/4ne3fUeQK5kGtk9x2wVTAf, seção `chao`, item "Lesão no fígado causada por substância".

O item tem quatro blocos, e cada um é um parágrafo na página.

> **O que é:** Dano ao fígado causado por um remédio ou outra substância ingerida, e não por vírus ou álcool.

> **Exemplo do dia a dia:** Uma pessoa que não bebe e não tem hepatite começa um chá de ervas para emagrecer. Semanas depois, os exames mostram o fígado inflamado. Se a causa for o chá, o caso entra nesta categoria.

> **Confunde-se com:** As outras doenças do fígado, como hepatite por vírus, álcool e gordura no fígado. Elas ficam fora desta conta. Quando a causa é uma erva ou um suplemento, os médicos também usam a sigla HILI (herb-induced liver injury).

> **Onde o artigo usa:** No conceito 2, sobre dose alta e fígado. Nos Estados Unidos, suplementos causam cerca de 20% das lesões no fígado por substância. A tradução da BBC diz 20% de todas as doenças do fígado, e isso está errado.

O título do item é "Lesão no fígado causada por substância (drug-induced liver injury, DILI)".

Regras que ele mostra:

- R5a (significado antes do termo): primeiro o significado em português, depois o termo em inglês, depois a sigla.
- R6a (ensinar no caminho): a definição vem com um exemplo.
- R4 (nenhum conhecimento assumido): o leitor é tratado como iniciante inteligente.
- R3 (problema mais contrapadrão): o erro da tradução vem junto com o dado certo.

Não mude isto: a ordem "significado, termo, sigla" e o bloco "confunde-se com".
O formato de cinco partes é produto do Projeto, mas a ordem dentro da definição é a Regra 5.

Leitor frio acerta: "uma hepatite por vírus entra na conta das lesões por substância?" (não).

### G4: o problema com a solução ao lado

Guia: Do zero ao avançado, DuckDB, notebook e Hugging Face, https://claude.ai/artifact/Tj7r3LvtwtJhUiwRubKfmZ, Parte 2 (os formatos), bloco "Mito corrigido".

> Muita gente acha que o CSV tem uma regra única e oficial.
> A crença não confere.
> Na verdade, o documento mais citado sobre CSV (RFC 4180) diz que nunca existiu regra formal.

> Por isso, cada programa grava o CSV de um jeito: com vírgula ou com ponto e vírgula.
> O que funciona: deixar a ferramenta detectar o separador e conferir o resultado.

Regras que ele mostra:

- R3 (problema mais contrapadrão): a solução vem no mesmo bloco, com "O que funciona:".
- R2b (conectores): o "por isso" liga a causa ao efeito.
- R5a (significado antes do termo): o código RFC 4180 vem depois do papel, "o documento mais citado sobre CSV".
- R2a (frases curtas): as frases têm de 6 a 16 palavras.

Não mude isto: a sequência "crença, não confere, na verdade, por isso, o que funciona".
É a forma publicada da Regra 3, e ela dá voz ao erro comum antes de corrigir, como o Curioso da clear-listen.

Leitor frio acerta: "por que dois programas gravam CSV de jeitos diferentes?".

### G5: a figura com "Como ler" e a conclusão em frequência natural

Guia: ElevenLabs e o Eleven v4, https://claude.ai/artifact/Nz6X3PncnmHAC21gDMCJ3G, seção `c2`, figura das 150 ferramentas.

> **Como ler:** cada bolinha é 1 ferramenta. São 150 ferramentas, e quase 8 em cada 10 são de agentes.

E, na mesma seção, logo antes da figura:

> **A ideia central aqui é: o conector deixa o Claude usar o ElevenLabs por você, com os seus créditos.**

Regras que ele mostra:

- R7b (as duas linhas da figura): "Como ler" diz o que cada marca é, e a frase seguinte conclui.
- R10d (número com âncora): "quase 8 em cada 10" dá o número em palavras.
- R7a (o teste das 4 perguntas): o visual existe porque há 150 elementos a segurar juntos.

Não mude isto: toda figura tem "Como ler" mais uma conclusão em palavras, e o número vem como frequência natural.
Uma versão nova da skill que gere a figura sem a conclusão falha neste trecho.

Leitor frio acerta, lendo só o texto: "que fração das ferramentas do conector é de agentes?".

### Como usar o golden set

1. Antes de mudar uma regra, rodar o lint da clear-read em cada trecho. Hoje os cinco dão 0 problemas.
2. Depois da mudança, pedir ao modelo, com a skill nova, que reescreva o mesmo conteúdo de origem. O trecho novo precisa ter as mesmas marcas: a ordem significado-termo-sigla, o "Onde a analogia falha", o "Você já sabe que... Agora", o "O que funciona", o "Como ler" com conclusão.
3. Um trecho que perde uma marca é um bloqueio, não um aviso.

Ponto-chave: os cinco trechos cobrem as regras 1, 2, 3, 5, 6, 7 e 10, e são o que a reescrita não pode apagar.

## 8. Perguntas de revisão do guia de burnout

O experimento da Fase D usa quatro guias, e três já têm perguntas na Biblioteca.
O quarto é o de burnout, e as perguntas dele estão aqui, no formato da seção 11.1 das instruções do Projeto.

São 5 perguntas "explicar" (uma por conceito), 1 "comparar" e 1 "controle".
Os pontos têm no máximo 15 palavras, as perguntas no máximo 30, e não há travessão.
O script no fim desta seção conferiu os limites.

O `guide_url` é a URL do artifact, e o `anchor` é o `id` da seção que tem a resposta.
Os campos de estado (`status`, `box`, `due`, `activated`, `last`, `history`) ficam fora deste arquivo, porque só a página os escreve depois de criados.

```json
[
  {
    "id": "burnout-estresse-depressao-ferias--1",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c1",
    "concept": "os cinco estados",
    "kind": "explicar",
    "prompt": "No guia sobre burnout e férias: como separar cansaço, estresse, burnout e depressão? Diga as três perguntas que o guia usa.",
    "cue": "pense nas três colunas da tabela de estados",
    "points": [
      "A primeira pergunta é de onde o estado vem",
      "A segunda pergunta é onde o estado aparece: no trabalho ou em toda a vida",
      "A terceira pergunta é o que resolve o estado"
    ],
    "terms": ["burnout", "depressão", "estresse crônico"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--2",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c2",
    "concept": "como o burnout se forma",
    "kind": "explicar",
    "prompt": "No guia sobre burnout e férias: como o burnout se forma, segundo o modelo de exigências e recursos do trabalho?",
    "cue": "exigências contra recursos, e o tempo",
    "points": [
      "As exigências do trabalho ficam maiores que os recursos por muito tempo",
      "Não há recuperação entre uma exigência e a outra",
      "Desse desequilíbrio saem exaustão, cinismo e eficácia reduzida"
    ],
    "terms": ["burnout", "modelo exigências e recursos", "recuperação"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--3",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c3",
    "concept": "burnout e depressão",
    "kind": "explicar",
    "prompt": "No guia sobre burnout e férias: por que burnout e depressão se confundem, e o que separa os dois na prática?",
    "cue": "olhe onde o sofrimento aparece",
    "points": [
      "Burnout e depressão compartilham exaustão, sono ruim e irritação",
      "No burnout, o sofrimento fica no trabalho e o prazer fora dele continua",
      "Na depressão, a perda de prazer toma todas as áreas da vida"
    ],
    "terms": ["burnout", "depressão", "transtorno depressivo maior"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--4",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c4",
    "concept": "como se resolve",
    "kind": "explicar",
    "prompt": "No guia sobre burnout e férias: por que descansar não basta para sair de um burnout, e o que resolve?",
    "cue": "três dimensões, e só uma responde ao descanso",
    "points": [
      "As intervenções individuais só mexem na exaustão, e com efeito pequeno",
      "O cinismo e a ineficácia só mudam quando o trabalho muda",
      "A recuperação de um burnout clínico leva meses"
    ],
    "terms": ["burnout", "exaustão", "cinismo"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--5",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c5",
    "concept": "as férias",
    "kind": "explicar",
    "prompt": "No guia sobre burnout e férias: por que o efeito das férias some, e quanto tempo ele dura depois da volta?",
    "cue": "a causa ficou esperando no trabalho",
    "points": [
      "O efeito das férias dura de uma a quatro semanas depois da volta",
      "A causa do burnout continua no trabalho e refaz o desgaste"
    ],
    "terms": ["férias", "burnout"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--6",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c5",
    "concept": "descanso e recuperação",
    "kind": "comparar",
    "prompt": "No guia sobre burnout e férias: qual é a diferença entre descanso e recuperação, e qual experiência mais reduz a fadiga?",
    "cue": "ficar parado não é voltar ao nível de antes",
    "points": [
      "Descanso é ficar parado; recuperação é voltar ao nível de antes do esforço",
      "A recuperação exige desligar de verdade do trabalho",
      "O desligamento psicológico é a experiência mais forte contra a fadiga"
    ],
    "terms": ["recuperação", "desligamento psicológico", "descanso"],
    "created": "2026-11-01"
  },
  {
    "id": "burnout-estresse-depressao-ferias--7",
    "guide": "burnout-estresse-depressao-ferias",
    "guide_title": "Burnout é estresse do trabalho sem recuperação, e férias aliviam por poucas semanas",
    "guide_url": "https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj",
    "anchor": "c1",
    "concept": "a classificação da OMS",
    "kind": "controle",
    "prompt": "No guia sobre burnout e férias: como a OMS classifica o burnout, e por que muita gente acha que ele virou doença em 2019?",
    "cue": "fenômeno, não doença",
    "points": [
      "A OMS classifica o burnout como fenômeno ocupacional, não como doença",
      "O anúncio de 2019 falou em doença e a OMS corrigiu no dia seguinte"
    ],
    "terms": ["OMS", "fenômeno ocupacional", "CID-11"],
    "created": "2026-11-01"
  }
]
```

O item 11 da seção 11.1 pede um script de conferência.
Ele está em `scripts/check_review_questions.py`, nesta pasta, e lê o JSON deste arquivo.
Ele confere os limites de palavras, a ausência de travessão, os ids únicos, e a contagem por tipo de pergunta.
Ele imprimiu `7 questions, 0 problems` em 1 de novembro de 2026.

Ponto-chave: o quarto guia tem as sete perguntas, no formato da Biblioteca, prontas para o experimento.

## 9. O que fica para as próximas fases, e o que só o Dennis responde

Nada desta fase bloqueou em pergunta.
As decisões abaixo vão aparecer, e a fase certa pergunta uma por vez.

**Para a Fase B (laços), sem pergunta:**

- A matriz canal por perfil parte das colunas "Vale onde" e "Executável" das tabelas das seções 3 e 4.
- Três regras da clear-listen já têm status diferente por canal: o "Parte N de M", a pergunta com pausa, e dizer a estrutura. A clear-read R11a (procedimentos) ganha o par "numerar para o olho, não numerar para o ouvido".
- Na clear-read, a Fase 1 (pesquisar) e a Fase 3 (rodar o lint) não rodam no perfil mínimo. A skill não diz o que fazer nesse caso.

**Para a Fase C (pesquisa), sem pergunta:**

- Abrir Potter 2000 e Potter 2008, as fontes da troca de voz na clear-listen R13b (a segunda voz).
- Abrir Lorch 2012 e Chen 2018 e ler o que a prévia dizia, para a clear-listen R3 (dizer a estrutura).
- Confirmar Ginns, Martin e Marsh 2013, a fonte da clear-listen R8 (falar com uma pessoa).
- Confirmar o ano de Brann e Sidi, e achar o "estudo de reassistir" da clear-listen R15 (fechar bem).
- Achar a fonte da clear-read R9 (tom) ou marcar a frase para cortar.
- Decidir "1 ou 2 números por frase" pela fonte (achado 2 da seção 6).

**Para a Fase E (proposta), sem pergunta:**

- Sete testes de lint que falham hoje (achado 8 da seção 6). Mais o teste da R5a (significado antes do termo), que hoje aceita "Mayer mostrou", e o aviso de conectores.
- Testes unitários para `lint_audio_script.py`, porque hoje não há regressão.
- O corte das duas skills para baixo de 5 mil tokens, com a renderização da clear-listen em `references/`.

**O que só o Dennis responde, e quando a pergunta chega:**

- Pergunta 8 da seção 12 (onde moram os evals) bloqueia a Fase E no primeiro PR com eval. Não bloqueia A, B ou C.
- Pergunta 6 da seção 12 pergunta se toda contagem trava, ou só a contagem antes do conteúdo. Ela bloqueia o desenho da Fase D, e a Fase C anda sem ela.
- Pergunta 1 da seção 12 (nomes das seções) bloqueia só a proposta 9.5 da Fase E.
- Para o golden set da clear-listen, o Dennis exporta um roteiro neutro já gerado. Serve o de suplementos, de 3 minutos e meio, ou o de burnout, de 12 minutos. Sem ele, a clear-listen não tem trecho dourado.

Ponto-chave: a Fase B pode começar agora, e a primeira pergunta ao Dennis só chega na Fase D ou E.

## 10. Adendo 2: a leitura no sentido Projeto para skill

O adendo `adendos/2026-11-01-visuais-e-regras-do-projeto.md` corrigiu uma direção que o inventário não percorreu.
Ele lista 14 regras das instruções do Projeto e pergunta se cada uma está na skill.
Os vereditos estão na seção 7 de `proposta.md`: 10 entram na skill como método e 4 já existem.
A linha R7c da seção 3.5 mudou de "mantém" para "muda" por causa dele.

Ponto-chave: o inventário tinha só a direção skill para prova; o adendo 2 acrescentou a direção Projeto para skill.
