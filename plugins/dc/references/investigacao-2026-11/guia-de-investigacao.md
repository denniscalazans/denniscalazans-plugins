# Guia de investigação: clear-read, clear-listen e o modo conversa

CRIADO: 2026-11-01 15:20 (Berlim)
ORIGEM: conversa por voz de 1 de novembro de 2026
STATUS: rascunho para execução

Revisão desta versão: o lint da clear-read deu 0 problemas.
Um leitor frio respondeu 8 de 8 perguntas e apontou gavetas abertas, fechadas nesta versão.
Este doc ainda não entrou no conjunto versionado do Projeto (seção 0 das instruções), e o Dennis decide se ele entra.

## 0. Para quem é este guia e como usar

Este guia é uma instrução de trabalho para uma IA.
A IA vai revisar duas skills, a clear-read e a clear-listen, e o Projeto "Clear Read the Web".
Depois ela vai propor melhorias com prova.
O Dennis lê o guia também, para aprovar o plano antes de qualquer mudança.

Leia na ordem.
A seção 1 diz de onde o guia vem.
A seção 2 diz o que já existe e não pode ser perdido.
A seção 3 diz a tese que a investigação vai testar.

As seções 4 a 9 são o trabalho, em fases.
A ordem de execução é: A (inventário), B (laços), C (pesquisa), E (proposta, num branch), D (experimento sobre o branch), e só então o merge.
A letra D vem antes de E no texto porque o experimento foi desenhado antes da proposta, mas ele roda depois dela.

As seções 10 a 12 dizem onde rodar, o que eu assumi e o que só o Dennis responde.
A seção 13 tem as fontes.

Uma regra vale para todo o guia.
Nenhuma mudança entra em skill, lint ou instrução sem um teste que falhe antes e passe depois.
E os testes antigos continuam passando (seção 4).

Ponto-chave: este guia é um plano de investigação com prova, não uma lista de respostas.

## 1. De onde este guia vem

### 1.1 O que a conversa de 1 de novembro mostrou

O Dennis conversou com o Claude por voz, no app Android, por cerca de uma hora.
A conversa produziu os achados abaixo.
Cada um vira uma linha de investigação.

**Achado 1: a skill descreve o leitor, não o processo do modelo.**
As duas skills dizem o que o leitor precisa: frases curtas, conectores, zero retrocesso.
Elas não dizem o que o modelo deve fazer com a própria cabeça antes de escrever.
Então a skill vira uma lista para conferir depois.

Ela não vira um ciclo: desenhar, ler como o ouvinte, corrigir, e só então falar.
Um modelo com raciocínio tem o lugar para esse ciclo, que é a etapa entre o pedido e a resposta.
A skill não usa esse lugar.

**Achado 2: o modelo carrega reflexos de texto acadêmico e de página web.**

Na conversa, o Claude seguiu a skill e ainda assim disse "Mayer mostrou", sem dizer quem é Mayer.
Ele citou "ASD-STE100" antes de dizer o que é.
A ASD-STE100 é a norma da indústria aeronáutica para manuais técnicos.
E ele abriu "cinco pontos" numerados para quem acabou de dizer que numeração faz travar.

Cada um desses reflexos é uma promessa: um nome solto, um código, uma contagem.
Uma promessa abre uma gaveta na cabeça do leitor.
A gaveta fica aberta até o conteúdo chegar.
Para quem tem TDAH, cansaço ou ruído em volta, essa gaveta custa a memória que mais falta.

**Achado 3: existe um atalho, e ele é apontar para o que o leitor já tem.**

Na conversa, o Dennis deu um exemplo: se alguém lhe diz "o seu país", ele já sabe que é o Brasil.
A frase transmite nada e aponta tudo, porque a resposta já estava na cabeça dele.
"Pense na sua memória mais antiga até hoje" é uma instrução que roda nos dados do ouvinte.
Por isso ela cabe em uma frase e serve para todo mundo.

Isso é a regra "conhecido antes do novo" levada ao limite.
Em vez de empurrar conteúdo, o texto cria um vazio que a cabeça da pessoa preenche sozinha.
O Dennis chamou isso de pressão negativa.

**Achado 4: o fio da fofoca é o andaime dos estudos, sem parecer andaime.**
Quem conta uma fofoca abre com "tu não sabe o que aconteceu", e isso é a pergunta antes.
Entrega pedaços completos, e isso é o apoio durante.
Repete "sabe aquilo que ela fez?", e isso é a recapitulação depois.

Esses três movimentos são o andaime de um estudo de 2024 com 210 adultos, metade com TDAH (Brann e Sidi).
Com esse andaime, o grupo com TDAH entendeu tanto quanto o grupo de controle.
O narrador de cinema que anuncia "três partes e um grande fechamento" também tem andaime.
Mas ele mostra o esqueleto e deixa a pessoa segurar.

A diferença entre os dois é o que cria a tensão.
No cinema, a tensão vem da estrutura anunciada, e o ouvinte segura um esqueleto vazio.
Na fofoca, a tensão vem do conteúdo, e o ouvinte só quer saber o que aconteceu.

**Achado 5: a conversa é um terceiro canal, e as duas skills não cobrem ele.**
A clear-read escreve para o olho.
A clear-listen escreve para o ouvido, em monólogo de 3 a 20 minutos.
Numa conversa por voz, a pessoa pode perguntar a qualquer momento, e a resposta tem 30 segundos.

Então três regras do áudio longo ficam estranhas na conversa.
São elas: o marcador de parte, a pergunta de recordação com pausa, e a repetição da ideia central em cada segmento.
O que vale na conversa é o fio.
O fio é feito de conectores, chão dado antes do novo, e fechamento quando a resposta passa de três frases.

Ponto-chave: a skill existe no texto, e a conversa mostrou que ela pode não existir na execução.

### 1.2 Por que isso importa além do Dennis

O Dennis descreveu o objetivo como um par de óculos.
Quem tem miopia não rouba no jogo quando usa óculos.
Ele equaliza a entrada.

A skill faz o mesmo para a compreensão.
Ela ajusta a forma como a informação chega, e a cabeça dele joga com as mesmas cartas que as outras.
A prova é o estudo de 2024 com adultos com TDAH: com o andaime certo, a diferença some.

O alvo é um método portátil.
Ele funciona no Claude hoje.
Amanhã pode funcionar num sistema que o Dennis construa, ou num sistema que um sobrinho dele encontre na escola.

Por isso o resultado desta investigação guarda o porquê de cada regra, com fonte.
Assim ele pode ser mostrado na web como prova, e não só como opinião.

Ponto-chave: o método é um ajuste de entrada, e precisa funcionar fora do Claude.

### 1.3 O que o Dennis pediu, nas palavras dele

- Não quero respostas agora. Quero um guia de revisão e de novas pesquisas.
- Analisar tudo como um laço dentro de um laço. Os laços são: ambientes, modelos com ou sem raciocínio, nível de esforço, ferramentas de pesquisa ou não, contexto do projeto ou não.
- Saber o que as skills já fazem bem. Garantir por testes que as partes boas não sejam jogadas fora a cada iteração.
- Pesquisar na documentação e nos cursos da Anthropic como escrever instruções para o modelo de hoje. A instrução que servia para um modelo de 2023 não serve para o Fable 5.1, o modelo do Claude em novembro de 2026.
- Decidir onde o trabalho roda: aqui no app ou no Claude Code.
- Agir de forma autônoma, listar as assunções, e deixar para o momento certo as perguntas que só ele responde.
- Um exemplo que ele deu é o Google Maps. Ele diz "em 800 metros, pegue a terceira saída da rotatória à esquerda". Só isso já tira a atenção de quem dirige.
- Reanalisar textos já gerados e gerar de novo com as instruções revisadas. Ver se o resultado melhora de verdade ou só muda.

Ponto-chave: o pedido é investigar com prova e proteger o que já funciona.

## 2. O que já existe e não pode ser perdido

Esta seção é o inventário de partida.
A Fase A (seção 5) transforma cada item em um veredito.

### 2.1 As duas skills

| Skill | Onde | Tamanho | Partes |
|---|---|---|---|
| clear-read 2.3.3 | plugin `dc`, repo `denniscalazans-plugins` | SKILL.md de 29 KB | 11 regras, 3 fases (pesquisar, desenhar, escrever), 2 modos (explicar, reescrever) |
| | `references/` | lang-pt-br.md, lang-en.md, html-patterns.md, research-basis.md (185 linhas), tests.md (17 testes) | |
| | `scripts/` | lint_clear_read.py (15 regras, 100 testes unitários), check_mermaid.cjs (com `--self-test`) | |
| clear-listen | skill solta, fora do plugin `dc`. Vive em Settings > Skills da conta do Dennis, e uma cópia de 13 de outubro está na Biblioteca em `dev/docs/clear-listen-SKILL-2026-10-13.md` | SKILL.md de 32 KB | 21 regras, 4 fases (fonte, desenhar, escrever, renderizar), intents de entrega (marcas neutras de pausa, tom e ênfase), perfil de engine (como cada motor de voz lê essas marcas) |
| | `references/` | research-basis.md (209 linhas, com mapa regra → evidência), tests.md (10 testes) | |
| | `scripts/` | lint_audio_script.py (12 checagens) | |

As 12 checagens do lint de áudio são estas:

- frase longa, parênteses, dígito, símbolo e travessão;
- referência para trás e ruído de diálogo;
- marcador de parte, tamanho da parte e pergunta de recordação por parte;
- excesso de perguntas no fim, e roteiro de uma parte sem pergunta.

### 2.2 O que cada skill já faz bem, segundo a própria conversa

Estas são as partes que a conversa confirmou.
A Fase A protege cada uma com um teste de regressão antes de qualquer outra coisa.

- **Zero retrocesso em dois níveis** (clear-read Regra 6; instruções seção 8.1). É a regra número um do Dennis. O lint já pega referência para trás e rótulo nu.
- **Conhecido antes do novo** (clear-read Regra 6). É a base do atalho do Achado 3.
- **Conectores explícitos em toda frase** (clear-read Regra 2; clear-listen Regra 5). Vem de um estudo de 2018 (Yeari) que achou que adultos com TDAH lembram menos as ligações entre ideias.
- **Andaime nunca cortado**: prequestão, marcador, recapitulação. Vem do estudo de 2024 com 210 adultos (Brann e Sidi).
- **Confiança antes da resposta** na revisão espaçada. Vem de um estudo de 2019 (Ben-Yehudah e Brann) sobre a ilusão de entender na tela.
- **A pergunta vem até o leitor**, no quiz e na revisão. Vem de um estudo de 2011 (Knouse) que achou que adultos com TDAH se testam menos sozinhos.
- **O áudio reconta, não lê** (clear-listen, fase 1 e Regra 16). Vem do efeito de informação transitória: a fala some depois de dita, então um texto denso lido em voz alta sobrecarrega a memória.
- **Intents de entrega neutros, perfil por engine** (clear-listen, fase 4). O roteiro marca o que a voz faz (pausa, tom, ênfase) em palavras neutras, e um perfil por motor de voz traduz cada marca. Foi decisão do Dennis em 8 de outubro, e protege a portabilidade.
- **Lints que rodam em qualquer máquina**, com Python 3 e sem pacotes.

Ponto-chave: nove partes já estão certas, e cada uma precisa de um teste que impeça a reescrita de apagá-la.

### 2.3 O que a pesquisa consolidada já fechou

O doc `claude/clear-read-pesquisa-consolidada.md`, de 13 de outubro, conferiu na fonte as evidências sobre leitura, retenção e visuais.
Ele vale como referência única para texto.
Esta investigação não repete essa conferência.

Ela cobre o que esse doc marcou como lacuna na sua seção 7, chamada "Sem prova ainda".
As lacunas são: fala, diálogo, e qualquer estudo de diagramas, interativos ou sobrecarga em adultos com TDAH.

### 2.4 O que o Projeto tem de material para experimento

Guias publicados que podem ser gerados de novo (seção 8):

- Suplementos todo dia (versão 2, no modelo novo, com a seção "O chão", que ensina os conceitos antes do artigo): https://claude.ai/artifact/4ne3fUeQK5kGtk9x2wVTAf
- Do zero ao avançado: DuckDB, notebook e Hugging Face (tema dentro da área do Dennis): https://claude.ai/artifact/Tj7r3LvtwtJhUiwRubKfmZ
- ElevenLabs e o Eleven v4 (tema dentro da área): https://claude.ai/artifact/Nz6X3PncnmHAC21gDMCJ3G
- Constelação familiar (tema fora da área, contestado): https://claude.ai/artifact/FWUcdktSyUPXEuCrPYdQzc
- O que você ouviu sobre a eleição (evento recente, checagem): https://claude.ai/artifact/B2HwtZqX2w1rAxYFrw8N9b
- Burnout, estresse e férias (tema fora da área): https://claude.ai/artifact/QsR3MrqZksdsSVbcPpPpwj
- O aviso do Mac da empresa (tema misto): https://claude.ai/artifact/8rss9msVVKnyN6qWQTpMCN

O artigo de origem de cada guia está na Biblioteca, na coleção `articles`, campo `url`.
A Biblioteca é a base de conhecimento do Projeto: uma página com banco de dados, em https://claude.ai/artifact/DbeaArDSi7zaTTBQ2q2mAy.

Outros materiais:

- Áudios já gerados, com as taxas medidas: Rafael cerca de 180 palavras por minuto, Marilita cerca de 170.
- Perguntas de revisão à espera em 3 guias: DuckDB, ElevenLabs e suplementos. Os outros guias não têm perguntas, e a Fase A escreve as do quarto guia do experimento.
- Os evals da clear-listen em `claude/clear-listen-evals.json` e `claude/clear-listen-trigger-evals.json`.
- O lint do Projeto, `dev/tools/lint_guide.py` (24 testes), guardado na Biblioteca.

### 2.5 Uma inconsistência já conhecida

Cada guia tem uma seção "O chão", com os conceitos que o artigo assume.
E tem um bloco "Para este guia ficar", que explica a revisão espaçada.
Em 24 de outubro de 2026 o Dennis disse que os dois nomes soam como português traduzido ao pé da letra.

As instruções do Projeto, de 14 de outubro, ainda usam os dois nomes em 6 lugares.
Isso entra na Fase A como item com veredito "muda".
A Fase E propõe os nomes novos.

Ponto-chave: o inventário tem 2 skills, 3 lints, 7 guias e uma inconsistência de nome já conhecida.

## 3. A tese que a investigação testa

A tese tem três partes: regra sem processo não executa, promessa é carga, e a conversa é um canal próprio.
Cada uma pode ser falsa.
A Fase C (pesquisa) e a Fase D (experimento) existem para descobrir.

**Parte 1: regra sem processo não executa.**
Uma regra escrita na skill, como "conhecido antes do novo", existe no texto e pode não existir na execução.
A prova é o "Mayer mostrou" da conversa: a skill estava carregada e o reflexo venceu.

A hipótese tem duas metades.
O modelo executa melhor quando a skill descreve um ciclo de trabalho: desenhar, ler como o ouvinte, corrigir.
O modelo executa pior quando a skill descreve só o resultado.
Isso depende de o modelo ter raciocínio, e por isso o laço de ambientes (seção 6) separa os dois casos.

**Parte 2: promessa é carga, entrega é alívio.**
Anunciar estrutura ("são cinco pontos") abre uma gaveta.
Citar um nome antes do que ele fez abre uma gaveta.
Criar um rótulo antes do conteúdo abre uma gaveta.

A hipótese é esta.
Para este leitor, uma frase que entrega algo completo custa menos do que uma frase que promete.
Uma frase que aponta para algo que ele já tem custa menos ainda.

Se a hipótese for verdadeira, a regra de sinalização da clear-listen (Regra 3, "diga a estrutura") precisa de um limite.
O limite seria: sinalizar pelo conteúdo, não pelo esqueleto.
Se for falsa, a Regra 3 fica como está.
A seção 7.2 lista o que a literatura diz, e ela não concorda inteira com a hipótese.

**Parte 3: a conversa é um canal próprio.**
As regras da clear-listen foram feitas para monólogo de 3 a 20 minutos.
Numa troca de 30 segundos, parte delas vira ruído.

A hipótese é que um modo conversa precisa de um conjunto menor de regras.
A seção 9.4 lista as candidatas.

Se a hipótese for verdadeira, o modo conversa vira uma seção da clear-listen ou um terceiro pacote.
Em 13 de outubro, o Claude decidiu não criar uma terceira skill para visuais, porque dividiria um método em dois arquivos.
Se a conversa é um canal próprio, essa decisão é revista com razão.

Ponto-chave: três hipóteses, e cada uma tem uma fase que pode derrubá-la.

## 4. Regras de segurança (o steering)

O medo do Dennis é concreto.
A cada conversa boa, uma reescrita.
E a reescrita apaga o que a conversa anterior tinha acertado.
Então estas regras valem para toda a investigação e para qualquer IA que a execute, aqui ou em outro ambiente.

1. **Inventário antes de proposta.** Nenhuma mudança é proposta antes de a Fase A terminar com um veredito por regra.
2. **Teste que falha antes.** Cada mudança vem com um teste que falha com a skill atual e passa com a skill proposta. O teste pode ser unitário no lint, um caso no `tests.md`, ou um eval.
3. **Regressão sempre.** Antes e depois de cada mudança, quatro conjuntos rodam. São os 100 testes do lint da clear-read, as 12 checagens do lint da clear-listen, o `--self-test` do check_mermaid e os evals do Projeto. Um teste antigo que quebra é um bloqueio, não um aviso.
4. **Golden set.** Antes de mudar qualquer regra, a Fase A escolhe 5 trechos de guias publicados que são exemplos do que está certo. Eles entram em `tests.md` como "não mude isso". A versão nova da skill reproduz o mesmo comportamento neles.
5. **Uma mudança por pull request.** Cada PR em `denniscalazans-plugins` muda uma regra, com o teste, a evidência e o antes e depois.
6. **Nada se apaga, tudo se aposenta.** Uma regra que cai vira `retired` com nota, como o playbook da Biblioteca já faz.
7. **Versão visível.** A skill ganha uma linha de versão no SKILL.md. O Projeto segue a regra de SET_VERSION da seção 0 das instruções. Essa regra diz que os 9 arquivos do Projeto (instruções e 8 docs de contexto) levam a mesma marca de versão.
8. **O Dennis aprova o plano, não cada linha.** A Fase E entrega um plano de mudanças com prioridade, e ele decide o que entra.
9. **Tudo vive no repo.** O Claude Code não lê docs do Projeto. Então o trabalho copia para o repo, antes da Fase A, a pesquisa consolidada, os evals e o lint do guia. O passo 0 da seção 5.1 diz como.

Ponto-chave: nenhuma linha das skills muda sem um teste que prove a mudança e sem os testes antigos passando.

## 5. Fase A: inventário com veredito

### 5.1 O que fazer

**Passo 0: trazer tudo para o repo.**

Criar a pasta `plugins/dc/references/investigacao-2026-11/` em `denniscalazans-plugins`.
A pasta não se chama `docs/` porque o `.gitignore` do repo ignora `docs/` e `**/evals/`.
Copiar para ela: `claude/clear-read-pesquisa-consolidada.md`, `claude/clear-listen-evals.json`, `claude/clear-listen-trigger-evals.json` e `dev/tools/lint_guide.py` da Biblioteca.
Toda entrega das fases vai para essa pasta.

Copiar a clear-listen inteira (SKILL.md, references, scripts) para `plugins/dc/skills/clear-listen/`.
Feito em 1 de novembro de 2026, no branch `investigacao-2026-11`, a partir da cópia de Settings > Skills.

**Passo 1: a tabela.**
A clear-read tem 11 regras, mais as sub-regras da Regra 6 (zero retrocesso) e da Regra 7 (o plano visual).
A clear-listen tem 21 regras, mais as regras de intents e de renderização.
Para cada regra, preencher uma linha com as colunas da tabela abaixo.

| Coluna | Pergunta que ela responde |
|---|---|
| Regra | Nome e número |
| O que ela pede | Uma frase |
| Evidência | Qual estudo ou padrão a sustenta, e com que certeza: alta, média, baixa ou nenhuma. Usar o `research-basis.md` de cada skill e a pesquisa consolidada copiada no passo 0 |
| Testável? | O lint pega? Um teste de `tests.md` pega? Um leitor frio pega? Ou é só um desejo escrito? |
| Executável? | O modelo consegue aplicar a regra enquanto escreve, ou só conferir depois? A conversa mostrou que "conhecido antes do novo" é do segundo tipo |
| Vale onde? | Texto, página, áudio longo, conversa. Marcar onde a regra ajuda, onde é neutra e onde atrapalha |
| Promessa ou entrega? | A regra faz o modelo prometer (anunciar, rotular, contar) ou entregar? |
| Veredito | Mantém com teste · mantém sem prova (precisa de pesquisa) · testa antes de mudar · muda · aposenta |

### 5.2 Onde a conversa já apontou um veredito

Estas linhas já têm um veredito provável.
A Fase A confirma ou derruba.

| Regra | Veredito provável | Motivo |
|---|---|---|
| clear-listen Regra 3, "diga a estrutura" (anunciar a contagem antes de uma lista) | testa antes de mudar | O Achado 2 e a tese parte 2 dizem que a contagem é promessa. Mas dois estudos (seção 7.2) dizem que a prévia ajuda. Proposta a testar na Fase D: anunciar só quando a frase que anuncia já entrega conteúdo |
| clear-listen Regra 1, "Parte N de M" | mantém no áudio longo, aposenta na conversa | Vale para quem volta de uma divagação em 15 minutos de áudio. Numa conversa de 30 segundos vira ruído |
| clear-listen Regra 6, pergunta de recordação com pausa | mantém no áudio longo, muda na conversa | Na conversa, a pessoa faz a própria pergunta. O modelo pode fechar com uma pergunta, sem pausa |
| clear-read Regra 6, "conhecido antes do novo" | mantém, e vira processo | A regra existe e não executou. Entra na Fase E como etapa de um ciclo: desenhar, ler como o leitor, corrigir, escrever (seção 9.1) |
| clear-read Regra 5, termo com significado antes | mantém, e estende para nomes próprios e códigos | "Mayer" (um pesquisador), "ASD-STE100" (a norma da aviação) e "Lei 15.263" (a lei brasileira de linguagem simples) são termos. A regra fala de jargão e sigla, e o lint pega sigla sem nome. Não pega nome próprio solto |
| clear-read Regra 1, "Key point" em cada seção | mantém | É a recapitulação do andaime |
| clear-listen Regra 4, repetir de propósito | mantém, e aproxima do "sabe aquilo que ela fez?" | A repetição como pergunta ("lembra que...") puxa recuperação. A repetição como eco só gasta tempo |
| clear-listen Regra 13, a segunda voz do podcast (o Curioso) pergunta antes e dá voz ao erro comum | mantém, com uma conferência | Tem prova forte (seção 7.2). A frase "a troca de voz reseta a atenção", na mesma regra, não teve prova achada. Abrir a fonte que o `research-basis.md` cita |
| Instruções seção 7, nomes "O chão" e "Para este guia ficar" | muda | Feedback do Dennis de 24 de outubro |
| clear-read e clear-listen, seção "Who you are writing for" | mantém | É a parte que faz as regras parecerem óbvias. A Fase E pode adicionar o modelo de narrador, que é contar como quem conta uma história a um amigo (seção 9.3) |

### 5.3 Entrega da Fase A

Um arquivo `plugins/dc/references/investigacao-2026-11/inventario-das-regras.md` com a tabela completa.
Mais o golden set (regra 4 da seção 4): 5 trechos copiados dos guias da seção 2.4, com a URL de origem de cada um.
Mais as perguntas de revisão do quarto guia do experimento, escritas no formato da seção 11.1 das instruções do Projeto.
Tamanho esperado: 40 a 50 linhas de tabela.

Ponto-chave: a Fase A entrega um veredito por regra, e dez vereditos já têm candidato.

## 6. Fase B: os laços de análise

O Dennis pediu "um for dentro de um for".
Esta é a forma concreta.

```
para cada canal       em [texto no chat, página HTML, áudio longo, conversa por voz]:
  para cada ambiente  em [com raciocínio, sem raciocínio] × [esforço alto, esforço baixo]
                       × [com ferramentas de pesquisa, sem] × [com contexto do projeto, sem]:
    para cada regra   do inventário da Fase A:
      a regra vale aqui?          (ajuda, neutra, atrapalha)
      o modelo executa ou confere? (a regra precisa de raciocínio para rodar?)
      a regra precisa de ferramenta? (verificar um fato, rodar um lint)
      a regra depende do contexto?  (glossário, Biblioteca, preferências)
```

São 4 canais, 16 ambientes e cerca de 45 regras.
Ninguém preenche isso a mão.
O que se faz é reduzir, e os passos estão abaixo.

**Passo 1: reduzir os 16 ambientes a 4 perfis que existem de verdade.**

- **Mínimo**: modelo sem raciocínio, sem ferramentas, sem contexto. Só o SKILL.md carregado. É o pior caso, e é o caso de um sistema próprio do Dennis no futuro.
- **Chat simples**: raciocínio, sem ferramentas, sem contexto do projeto. É um chat solto no app.
- **Projeto**: raciocínio, ferramentas de pesquisa, contexto do projeto. É o Clear Read the Web hoje.
- **Agêntico**: raciocínio, ferramentas, contexto, subagentes e lints rodando. É o Claude Code.

**Passo 2: para cada perfil, marcar as regras que não rodam.**
Exemplo: a fase 1 da clear-read (pesquisar antes) não roda no perfil mínimo.
Hoje a skill diz "não pule", e o modelo sem ferramenta pula mesmo assim.
A skill precisa dizer o que fazer nesse caso.

**Passo 3: para cada canal, marcar as regras que atrapalham.**
A seção 5.2 já tem três candidatas para a conversa.

**Passo 4: para o perfil mínimo, escrever a versão mais curta da skill que ainda funciona.**
Isso é o teste de portabilidade.
Uma skill que só funciona com raciocínio e lint não é um par de óculos.
Ela é uma prótese que só funciona num hospital.

Entrega: uma matriz canal por perfil.
Em cada célula, a lista de regras que mudam de status.
Mais um rascunho de "SKILL.md mínimo" para cada uma das duas skills, no perfil mínimo.
Tudo em `plugins/dc/references/investigacao-2026-11/`.

Ponto-chave: a Fase B reduz os 16 ambientes a 4 perfis, e entrega uma matriz de 4 canais por 4 perfis.

## 7. Fase C: pesquisa nova

A pesquisa consolidada cobriu leitura.
Esta fase cobre o que faltou.
Duas pesquisas foram feitas em 1 de novembro de 2026 para abrir o caminho, e os achados estão aqui.

Cada achado precisa da conferência na fonte antes de virar regra.
O protocolo é o da pesquisa consolidada: abrir a página do DOI ou do artigo, e conferir o número ou a afirmação.
Depois marcar com um dos vereditos: confirmado, precisa de contexto, incorreto, desatualizado, ou não verificável.
Sem os conectores de pesquisa, a conferência usa web fetch nas páginas do DOI.

Entrega da Fase C: `plugins/dc/references/investigacao-2026-11/pesquisa-conferida.md`, no formato da pesquisa consolidada.
Prioridade de conferência: primeiro os 4 estudos marcados "conferir" na seção 13.2, depois os que sustentam um veredito da seção 5.2, depois o resto.

### 7.1 Como escrever instruções para o modelo de hoje (documentação da Anthropic)

Pesquisa feita em 1 de novembro de 2026 na documentação da Anthropic.
Os links estão na seção 13.1.
As páginas `docs.claude.com` e `docs.anthropic.com` agora redirecionam para `platform.claude.com`.
Os achados abaixo mudam como as skills devem ser escritas, e cada um tem uma consequência.

**1. O modelo de hoje segue a letra.**

A documentação diz que o Claude 4 e os modelos seguintes seguem o pedido de forma literal e precisa.
Uma instrução que descreve o resultado ("frases de 15 palavras") produz o resultado.
Uma instrução vaga ("seja claro") produz pouco.

Consequência: cada regra das skills precisa descrever o comportamento exato, com exemplo de entrada e saída.
As regras que hoje são adjetivos ("tom calmo", "profundidade real") entram na Fase A como "muda" ou "precisa de exemplo".

**2. Dar o motivo funciona melhor do que proibir.**

O exemplo da própria documentação é sobre áudio.
"Nunca use reticências" funciona pior do que explicar que um motor de voz vai ler o texto.
E "escreva em prosa corrida" funciona melhor do que "não use markdown".

Consequência: toda regra "nunca X" das skills vira "faça Y, porque Z".
As duas skills já fazem isso na maior parte, e o inventário marca as exceções.

**3. Exemplos são copiados de perto.**

O modelo copia detalhes dos exemplos.
Então um exemplo só pode mostrar o comportamento desejado.
A documentação recomenda 3 a 5 exemplos variados.

Consequência: cada exemplo "fraco versus forte" das skills precisa de um exemplo forte sem nenhum defeito.
Este guia segue a mesma regra.

**4. Ênfase em maiúsculas atrapalha.**

"IMPORTANTE", "NUNCA" em caixa alta e "CRITICAL: You MUST" fazem o modelo de hoje aplicar a regra demais.
A recomendação é uma frase simples com o motivo.
Se uma regra precisa valer sempre, ela vira um lint ou um hook, não uma palavra em caixa alta.
Um hook é um gatilho automático do Claude Code, que roda sem depender do modelo.

Consequência: buscar caixa alta nas duas skills e nas instruções do Projeto.
As regras "sempre" viram lint.

**5. O corpo da skill tem um teto prático de 5 mil tokens.**

A documentação pede corpo abaixo de 500 linhas e perto de 5 mil tokens.
No Claude Code, depois de uma compactação de contexto, só os primeiros 5 mil tokens de cada skill sobrevivem.
A clear-read tem 29 KB, cerca de 7 mil tokens, e a clear-listen tem 32 KB, cerca de 8 mil.

Consequência: as duas passam do teto.
O que está no fim do arquivo pode sumir no meio de uma sessão longa.
Na clear-listen, o fim é a renderização por engine.
A Fase E decide o que vai para `references/` e o que fica no corpo, com as regras mais importantes no topo.

**6. A skill é lida uma vez, não a cada resposta.**

O texto entra no contexto quando a skill dispara, e não é relido.
Então uma regra escrita como "rode o lint" pode ser esquecida na terceira resposta.

A recomendação tem duas partes.
Escrever a regra para cobrir toda a tarefa, como "depois de cada bloco escrito".
E mover o que não pode falhar para um hook.

Consequência direta para o Achado 1 da conversa, que é a skill descrever o leitor e não o processo.
"Conhecido antes do novo" não executou porque é uma regra entre 40, lida uma vez.
O caminho é virar etapa do ciclo (seção 9.1) ou lint.

**7. O modelo pode ser instruído a se conferir antes de terminar, com uma exceção.**

"Antes de terminar, confira a resposta contra estes critérios" funciona.
O Fable 5.1 tem um padrão próprio de checagem antes do fim.
A exceção é o modelo Opus 5, onde essa instrução causa verificação em excesso.

Um modelo 5.x pode recusar um pedido para escrever o raciocínio na resposta.
Então a skill pede uma explicação curta, não o raciocínio inteiro.
Consequência: a etapa "ler como o leitor" (seção 9.1) é compatível com o modelo de hoje.
Ela precisa ser escrita como critério de conferência, não como pedido de expor o raciocínio.

**8. Com esforço baixo, o modelo responde de memória.**

No Fable 5.1 com esforço `low`, o modelo responde de memória em vez de pesquisar.
A documentação recomenda uma frase "pesquise antes de responder".

Consequência: a fase 1 da clear-read (pesquisar sempre) depende do esforço.
O perfil mínimo da Fase B precisa dizer o que fazer sem pesquisa.
A Fase D fixa o esforço nas duas condições.

**9. Mínimo, depois adicionar a partir de falhas observadas.**

A recomendação da Anthropic é começar com o menor conjunto de instruções que define o comportamento, no melhor modelo.
Só depois adicionar regra, e só quando uma falha medida pede.

Consequência: isso é o oposto do medo do Dennis, que é cada conversa adicionar regra.
O ciclo do Projeto já faz isso: feedback vira regra `testing`, e 3 execuções viram `active`.
A Fase E segue o mesmo ciclo para a skill.

**10. Evals: com e sem a skill, cego, com juiz separado.**

A documentação de skills pede 2 ou 3 prompts realistas em `evals/evals.json`.
Cada caso roda com e sem a skill, em contextos limpos, com afirmações concretas.
Afirmações que passam nos dois braços são descartadas.
A comparação entre versões é cega, A contra B.

O juiz LLM tem rubrica de passa ou falha, é um modelo diferente do avaliado, e roda com raciocínio ligado.
O comando `claude plugin eval` roda cada caso 3 vezes com e sem o plugin e reporta a diferença.

Consequência: a Fase D usa esse formato, e a Fase E entrega os evals junto com cada PR.
A clear-read tem `tests.md` (17 testes para um humano rodar) e 100 testes unitários do lint, mas não tem `evals/evals.json`.
A clear-listen tem evals no Projeto, não na skill.

Um obstáculo do repo: o `.gitignore` ignora `**/evals/`.
Então os evals só entram no Git se essa linha mudar, ou se eles morarem em outra pasta, como `tests/evals/`.
Isso é uma decisão do Dennis (seção 12, pergunta 8).

**O que a pesquisa não achou.**
Nada sobre bajulação (sycophancy) nos docs de prompt.
Nada específico sobre como instruir um modelo a escrever para um leitor com TDAH.
Nada sobre instruir o modo de voz, além do exemplo das reticências e do motor de voz.

Ponto-chave: as skills passam de 5 mil tokens, não têm evals da Anthropic, e o modelo lê as regras só uma vez.

### 7.2 O que a literatura diz sobre fala, narrativa e diálogo

Pesquisa feita em 1 de novembro de 2026, em busca na web, no Valency (PubMed, arXiv, PsyArXiv) e no PubMed.
Ela abre o caminho e não fecha nada.
Cada número abaixo precisa da conferência na fonte antes de virar regra.
Os estudos com pessoas com TDAH estão marcados com [TDAH], e os outros são população geral.

Os links estão na seção 13.2.
Os nomes dos autores aparecem entre parênteses, só para achar a fonte.

#### O que a pesquisa confirma do que a conversa disse

**Ouvir perde mais atenção do que ler.**
Um estudo com 211 adultos mediu a divagação na mesma tarefa em três formas.
Ouvir deu a maior divagação, cerca de metade das sondagens, e a pior memória.
Ler em voz alta deu a menor (Varao Sousa e colegas, 2013).

Outro estudo, com 175 adultos, mostrou que ruído de fundo aumenta a divagação.
A compreensão caiu tanto na leitura quanto na escuta (Steindorf e colegas, 2023).
Isso sustenta a decisão do Projeto de tratar o áudio como primeira passada ou revisão, nunca como substituto.

**Pergunta no meio segura a atenção.**
Um estudo com 80 adultos usou uma aula em vídeo de 21 minutos.
Um teste curto a cada 5 minutos derrubou a divagação de cerca de 40% para 19% e subiu a nota final.
Reestudar sem pergunta não ajudou (Szpunar, Khan e Schacter, 2013).

Isso é a base da pergunta de recordação por parte (clear-listen Regra 6).
E é o "sabe aquilo que ela fez?" da fofoca.

**Para o adulto com TDAH, a divagação é espontânea e não se regula sozinha.** [TDAH]
Um estudo comparou 27 adultos com TDAH e 29 sem (Bozhilova e colegas, 2020).
A divagação caiu quando a tarefa exigia mais da memória de trabalho.
Ela não caiu quando a tarefa exigia só atenção sustentada.

Ou seja, uma narração passiva e longa é o pior caso.
Uma demanda frequente, como uma pergunta ou uma tarefa, é o que segura.
Isso reforça o Achado 4 da conversa, o fio da fofoca: o andaime precisa trabalhar pela pessoa.

**Conectores ditos em voz alta ajudam.**
Um estudo com fala espontânea mostrou que conectivos ajudam a entender relações causais (Cevasco, 2009).
Outro tirou os marcadores ("então", "agora", "certo") de uma aula, e a compreensão caiu (Flowerdew e Tauroza, 1995, com ouvintes de segunda língua).
Isso é a Regra 5 da clear-listen e a Regra 2 da clear-read.

**Narrativa é lembrada melhor que exposição, com um limite.**
Uma meta-análise de 2021 juntou mais de 75 amostras e 33 mil participantes (Mar e colegas).
Narrativas são entendidas e lembradas melhor do que textos expositivos.

Mas um estudo de 2010 achou o limite (Wolfe e Woodwyk).
O texto expositivo integra melhor o conteúdo com o que a pessoa já sabe.
Então o modelo de narrador (seção 9.3) ajuda a lembrar fatos, e ajuda menos a entender mecanismo.
A proposta precisa desse limite escrito.

**O questionador que pergunta fundo funciona. O que faz conversa fiada, não.**

Dois estudos, de 2000 e 2003, puseram alunos para ouvir um diálogo de tutoria (Craig e colegas; Driscoll e colegas).
O ganho apareceu só quando o aluno ouvido perguntava "por quê" e "como".
Perguntas rasas ou comentários não deram nada.

Um terceiro estudo usou mais de mil alunos de física (Muller e Sharma, 2007 e 2008).
O formato que dá voz à concepção errada e a refuta ganhou de 0,5 a 1 desvio-padrão sobre a exposição simples.
Os alunos não sentiram que aprenderam mais.

Isso é exatamente o Curioso da clear-listen (Regra 13), a segunda voz do podcast que pergunta e dá voz ao erro comum.
A regra tem prova.

**Uma ação por frase na instrução de navegação.**
Um estudo em simulador testou instruções compostas de dois passos (Dalton e colegas, cerca de 2013).
Elas aumentaram os perigos não vistos, de 1,5% para 5,5%, e a variação de direção.
Instruções simples não aumentaram.

Outro estudo mediu o guia por marco ("na rotatória") contra o guia por distância ("em 800 metros") (Burnett, 1998).
Por marco, o motorista olhou para a tela cerca de 1,6 vezes.
Por distância, 5 vezes.
O exemplo do Google Maps do Dennis tem prova.

**Adultos com TDAH se distraem mais com som e têm menos memória auditiva de trabalho.** [TDAH]
Três estudos mostram isso: um com 69 contra 66 adultos, um com 17 contra 17 com ressonância, e uma meta-análise.
Então a regra de voz limpa sem fundo (clear-listen Regra 11) tem base direta.

**Voz sintética custa memória quando a prosódia erra.**
Um estudo de 2000 achou que a recordação de frases era pior com voz sintética (Paris e colegas).
A causa principal era a prosódia errada, que carrega a memória de trabalho.
Estudos recentes com vozes neurais modernas, em tarefas de aprendizagem, não acharam diferença.

Então a escolha de voz por ouvido, que o Dennis já faz, tem base.
Na conversa, o Claude disse que a pontuação é o único controle de som que ele tem.
Essa ideia também tem base.

#### O que a pesquisa contradiz, ou deixa sem prova

**Anunciar a estrutura ajuda, pelo menos no que foi medido.**

Dois estudos, de 2012 e 2018, testaram frases de prévia com universitários (Lorch e colegas; Chen e Lorch).
Uma prévia como "esta seção cobre três causas" melhorou a compreensão da estrutura, tanto em texto quanto em áudio sintético.
Um título dito em áudio só funcionou quando a voz restaurou o que o título mostra no papel, com pausa e entonação.
Isso vai contra a tese parte 2 (promessa é carga) como ela está.

O que esses estudos mediram foi a estrutura lembrada, ou seja, o esboço que a pessoa reconstrói.
Eles não mediram esforço, nem carga durante a escuta, nem pessoas com TDAH.

Então a tese parte 2, promessa é carga, precisa de uma forma mais cuidadosa.
A prévia que já entrega conteúdo ("são três causas, e a mais forte é o preço") pode ter o ganho sem a gaveta.
É uma hipótese para a Fase D, não uma regra.

**A "gaveta aberta" da contagem não foi testada.**
Nenhum estudo achado mediu se "são cinco pontos" carrega a memória de trabalho antes do conteúdo chegar.
A preocupação do Dennis fica como não testada, não como refutada.
O experimento da Fase D é a primeira medida.

**"Troca de voz puxa a atenção de volta" não apareceu.**
A clear-listen Regra 13 diz que uma mudança de voz reseta a atenção.
Ela diz também que a memória é melhor para o que vem logo depois.
A busca não achou essa evidência.

O `research-basis.md` da clear-listen cita "orienting to voice changes".
A Fase A abre essa fonte e confere se ela diz isso mesmo.

**Recuperação espaçada nem sempre vence reestudar, em TDAH.** [TDAH]
Um estudo de 2023 comparou 36 universitários com TDAH e 36 sem, em hebraico (Stern e Halamish).
A recordação do texto inteiro venceu a recordação por seção.
O Projeto já aplica isso em "Recapitule de cabeça".

Mas nenhuma das duas venceu reestudar no teste de 2 dias.
É um estudo só.
Ele pede cautela ao prometer que a revisão espaçada funciona para este leitor.
A medição de adesão e recordação na aba Revisar é o que vai responder.

**Dado antes do novo: a prova é de leitura, e depende da construção da frase.**
A regra "conhecido antes do novo" vem de estudos dos anos 1970 (Haviland e Clark).
Eles mediram cerca de 150 a 200 milissegundos a mais quando a parte "dada" da frase não tinha antecedente.

Um estudo de 2004 achou que o ganho aparece em algumas construções e não em outras (Clifton e Frazier).
Não há estudo em fala, nem em adultos com TDAH.
A regra fica, porque o custo de aplicar é baixo.
A certeza é média.

**Velocidade: até 1,5 vez é seguro, para a população geral.**
Um estudo com 231 adultos achou queda significativa só em 2,5 vezes (Murphy e colegas, 2022).
Em português brasileiro, há dois estudos de inteligibilidade, não de compreensão.
Nada sobre TDAH e velocidade.

**Assistentes de voz para TDAH: só co-design e estudos pequenos.** [TDAH]
Um estudo de 2026 fez co-design de um chatbot com voz com 9 jovens com TDAH (Bryant e colegas).
Um estudo de 2024 deu um robô companheiro de estudo a 11 universitários com TDAH (O'Connell e colegas).
Nesse, 73% queriam que o robô detectasse a distração e chamasse de volta.

Nada controlado.
Princípios reutilizáveis: turnos curtos, lembrete externo quando a atenção escapa, e não copiar as normas da conversa humana sem testar.

Ponto-chave: a literatura confirma o Curioso e a pergunta no meio, contradiz a tese da contagem, e deixa a troca de voz sem prova.

### 7.3 Perguntas que continuam abertas

Estas são as perguntas que nenhuma fonte respondeu.
A Fase D responde as três primeiras com o Dennis.
As outras ficam registradas como "sem prova", no mesmo formato da seção 7 da pesquisa consolidada.

1. A contagem antes do conteúdo ("são cinco pontos") custa memória de trabalho para este leitor? E a contagem que já entrega conteúdo custa menos?
2. Um fechamento com "lembra que..." (repetição como pergunta) retém mais do que um fechamento com "ponto-chave:" (repetição como afirmação)?
3. Em conversa por voz de 30 segundos, o modelo de narrador (seção 9.3) produz respostas com menos travamentos do que a clear-listen aplicada como está?
4. A troca de voz reseta a atenção? A Fase A abre a fonte citada pela clear-listen.
5. Qual a velocidade de fala explicativa em português brasileiro que este leitor tolera? Hoje o valor, 160 palavras por minuto, é um padrão de prática, não uma medida.
6. Ouvir ou ler, sob distração, em adultos com TDAH: não há comparação direta.
7. O nome próprio antes do papel ("Mayer mostrou") custa mais do que o papel antes do nome? Nenhum estudo achado mediu isso.

Três pesquisas que valem a pena na próxima rodada, com a ferramenta certa:

- Abrir na fonte os dois estudos de prévia em áudio (2012 e 2018) e ler o que exatamente a prévia dizia. Se ela entregava conteúdo junto com a contagem, a tese sobre promessa e esses estudos concordam. Ferramenta: web fetch nas páginas do DOI.
- Buscar no Valency, por significado: "working memory load of enumeration in spoken instructions" e "forward reference cost in discourse comprehension". A busca de 1 de novembro foi por palavras-chave.
- Uma busca no Consensus, porque o plano é pequeno: "advance organizers spoken lecture working memory attention deficit".

Ponto-chave: sete perguntas abertas, e as três primeiras têm resposta no experimento com o Dennis.

## 8. Fase D: o experimento

O experimento responde uma pergunta.
A skill revisada produz um texto melhor, ou só diferente?
"Melhor" tem uma medida: um leitor frio responde mais pontos, e o Dennis sente menos esforço.

### 8.1 Desenho

1. **Material**: 4 guias já publicados, em pares de tema. Um par dentro da área do Dennis (DuckDB, ElevenLabs). Um par fora (suplementos, burnout e férias).
2. **Condições**: para cada guia, gerar duas versões, uma com a skill atual e outra com a skill revisada do branch da proposta (Fase E). As duas partem do mesmo artigo e do mesmo mapa de ideias, salvo em arquivo. Mesmo modelo, mesmo esforço, mesmas ferramentas.
3. **Áudio**: para 2 dos guias, gerar o roteiro de modo C (resumo de 3 minutos) nas duas condições. O áudio com ElevenLabs só depois de o Dennis aprovar o custo.
4. **Conversa**: 5 perguntas sobre cada guia, respondidas em texto como turnos de 30 segundos, nas duas condições. O Claude Code não tem voz, então a condição de voz real roda no app com o Dennis, e o app guarda a transcrição.
5. **Medidas automáticas**: os dois lints, o tamanho, e a contagem de promessas (anúncios de contagem, nomes próprios sem papel, rótulos nus). Mais o leitor frio: um subagente que vê só o texto responde as perguntas de revisão do guia, com meta de 9 em 10. Três guias já têm perguntas, e a Fase A escreve as do quarto.
6. **Medidas com o Dennis**: para cada par, ele lê as duas versões em ordem aleatória, sem saber qual é qual. Ele responde: qual exigiu menos esforço, e onde travou. 24 horas depois, 3 perguntas de recordação.
7. **Análise**: uma tabela por guia, com as condições nas colunas e as medidas nas linhas. Sem estatística pesada, porque são 4 pares. O que se procura é direção consistente.

### 8.2 O que invalida o experimento

- Gerar as duas versões em sessões com contextos diferentes, por exemplo uma com a Biblioteca carregada e outra sem.
- O Dennis saber qual versão é qual.
- Mudar mais de uma regra entre as condições. Se a Fase E propuser 5 mudanças, o experimento testa primeiro as 2 de maior impacto. As outras ficam para uma segunda rodada.

### 8.3 Entrega

Um doc `plugins/dc/references/investigacao-2026-11/experimento.md` com a tabela, os 8 arquivos gerados, as transcrições e a conclusão em 5 frases.
O merge dos PRs da Fase E só acontece depois desta conclusão.

Ponto-chave: 4 pares de guias, duas condições, leitor frio e leitura cega pelo Dennis.

## 9. Fase E: a proposta de mudança

A Fase E começa depois das Fases A, B e C.
Ela entrega a skill revisada num branch.
Ela entrega também um plano de PRs, um por mudança, com prioridade.
O experimento da Fase D roda sobre esse branch, e o merge vem depois.
A conversa já deixa os candidatos abaixo.

### 9.1 Uma camada de processo nas duas skills

Hoje a clear-read tem três fases: pesquisar, desenhar, escrever.
E tem um lint no fim.
A proposta é uma quarta etapa entre desenhar e escrever, chamada "ler como o leitor".

1. Desenhar a resposta, com as fases existentes.
2. Reler o desenho como o leitor. Para cada frase, perguntar: "o que ele já tem que eu posso usar?" e "o que estou deixando aberto?".
3. Marcar cada promessa: nome solto, código, contagem, "a ideia de antes". Trocar por entrega, ou por ponteiro para o que ele já tem.
4. Só então escrever.

Para um modelo sem raciocínio, a etapa 2 vira checagem de lint.
O lint já pega rótulo nu e referência para trás.
Ele ganha duas checagens: nome próprio sem papel (seção 9.2) e contagem antes do conteúdo.

Para um modelo com raciocínio, a skill pede que a etapa 2 aconteça no raciocínio.
A seção 7.1, achado 7, diz como a Anthropic recomenda pedir isso: como critério de conferência, não como pedido de expor o raciocínio.

### 9.2 A regra de nomes próprios e códigos

A Regra 5 da clear-read fala de jargão e sigla.
A proposta estende a regra para nome de pessoa, de estudo, de norma e de lei.
O papel vem antes do nome.
O nome só entra quando a próxima frase precisa dele.

Exemplo da conversa:

- Fraco: "Mayer mostrou que ensinar os termos antes ajuda."
- Forte: "Pesquisas com alunos mostram que ensinar os termos antes da lição ajuda. O pesquisador é Richard Mayer, e os links estão no fim."

O lint ganha uma checagem.
Ela procura um nome próprio com maiúscula seguido de verbo de evidência ("mostrou", "achou", "demonstrou", "found", "showed").
Se não há um substantivo de papel na mesma frase, é problema.

### 9.3 O modelo de narrador

A seção "Who you are writing for" das duas skills descreve o leitor.
A proposta adiciona um parágrafo que descreve o narrador.
O narrador é alguém que conta uma história boa para um amigo.

Ele entrega completo.
Ele puxa pelo que vem.
Ele repete o essencial como quem relembra junto ("lembra que...").
Ele nunca mostra o esqueleto.

O professor com slides faz o contrário: mostra a estrutura e deixa a pessoa segurar.
Esse parágrafo vale mais do que cinco regras, porque muda o reflexo de origem.

A seção 7.2 diz que a literatura sustenta a narrativa para lembrar fatos, e menos para entender mecanismo.
As fontes são a meta-análise de Mar e colegas (2021) e o estudo de Wolfe e Woodwyk (2010).
O parágrafo precisa desse limite.

### 9.4 O modo conversa

Um pacote pequeno, dentro da clear-listen ou como terceiro arquivo.
A Fase B decide qual.
Cada candidato a regra é testado na Fase D.

- Responder em blocos de até 3 frases antes de qualquer estrutura.
- Anunciar estrutura só quando a frase que anuncia já entrega conteúdo.
- Conhecido antes do novo em cada frase.
- Conector causal em cada ligação.
- Redefinir um termo quando ele volta depois de 3 ou mais trocas.
- Fechar com o essencial quando a resposta passa de 3 frases.
- Nunca numerar para quem disse que numeração trava.
- Pontuação como único controle de som. O modelo não controla tom nem pausa; ele só entrega texto, e o motor de voz lê a pontuação. Então: frase curta sai firme, vírgula vira hesitação, "porque" puxa para frente, e ponto final deixa cair.

### 9.5 Nomes em português natural

Trocar "O chão" e "Para este guia ficar" por nomes que digam o que a seção faz.
Candidatos para o Dennis escolher: "Antes de ler: os conceitos que o artigo assume" e "Para lembrar depois".
A proposta vai com 3 opções cada, e ele escolhe.

### 9.6 A skill no perfil mínimo

Um `SKILL.md` curto, ou uma seção "Sem raciocínio e sem ferramentas".
Ela diz o que fazer quando a fase de pesquisa e o lint não existem.
É o que garante a portabilidade.

Ponto-chave: seis candidatos, e o maior é a etapa "ler como o leitor" entre desenhar e escrever.

## 10. Onde rodar

| Trabalho | Onde | Por quê |
|---|---|---|
| Fases A e B (inventário, laços) | Claude Code, no repo `denniscalazans-plugins` | A skill mora lá, os lints rodam lá, e o inventário vira arquivo no repo |
| Fase C (pesquisa) | Aqui no app, neste Projeto, ou no Claude Code com os conectores | Os conectores de pesquisa (Valency, PubMed, Consensus, Exa) estão neste Projeto. No Claude Code, só se esses conectores (servidores MCP) forem configurados. Sem eles, web fetch nas páginas do DOI |
| Fase D (experimento) | Claude Code | Gera 8 arquivos, roda 2 lints e subagentes leitores frios em paralelo. No app isso cabe mal |
| Fase E (PRs) | Claude Code | Um PR por mudança, com teste |
| Aprovação do plano e escolha de nomes | Aqui, por voz ou texto | É decisão do Dennis |
| Leitura cega das versões e recordação em 24 horas | Celular do Dennis | É medida com ele |

Este guia é o primeiro arquivo que um agente lê no Claude Code.
Ele não assume nada da conversa de 1 de novembro.

Ponto-chave: planejar e aprovar aqui, executar no Claude Code.

## 11. Assunções que eu fiz

Cada uma pode estar errada.
A IA que executar o guia confere com o Dennis antes de agir sobre ela.

1. A clear-listen entra no plugin `dc`, ao lado da clear-read. O Dennis confirmou isso em 1 de novembro de 2026, e a cópia está no branch `investigacao-2026-11`. Falta decidir se ela entra no `plugin.json` e no README do plugin.
2. O inventário cobre as regras do SKILL.md, não as das instruções do Projeto. As instruções são produto, não método, e ficam para depois.
3. O experimento usa o modelo de hoje, Fable 5.1, nas duas condições. Testar um modelo sem raciocínio fica para quando o Dennis tiver um.
4. O "modo conversa" é para voz com o Claude, não para chat de texto. A clear-read já cobre o chat de texto.
5. A decisão de 13 de outubro, de não criar uma terceira skill, pode ser revista, porque o Achado 5 é novo.
6. Os lints continuam em Python e Node, sem pacotes, para rodar em qualquer máquina.
7. "Melhor" no experimento se mede com leitor frio e com o Dennis, não com uma nota de um juiz LLM. Um juiz LLM pode entrar como terceira medida, nunca como única.
8. O guia não entra no conjunto versionado (SET_VERSION) até o Dennis decidir. Por isso ele não forçou uma nova versão nos 9 arquivos.

Ponto-chave: oito assunções, e a primeira (onde a clear-listen mora) já foi confirmada pelo Dennis.

## 12. Perguntas que só o Dennis responde

Não responder agora.
A IA responsável pela execução pergunta uma coisa por vez, só quando a resposta bloquear o trabalho.

1. **Nomes das seções** (Fase E, 9.5): quais os nomes para "O chão" e "Para este guia ficar"?
2. **Terceira skill ou seção**: o modo conversa vira seção da clear-listen ou arquivo próprio?
3. **Custo do áudio no experimento**: gerar 4 áudios de 3 minutos (cerca de 11 mil créditos) ou só os roteiros?
4. **Ordem das fases**: fazer a Fase A inteira antes da pesquisa, ou pesquisar em paralelo?
5. **Tempo de leitura cega**: ele tem 4 pares de guias para ler em ordem aleatória, com recordação 24 horas depois. Em que semana?
6. **Sinalização na fala**: ele disse que "primeira, segunda" trava. Vale para toda contagem, ou só quando a contagem vem antes do conteúdo? A tese parte 2 (promessa é carga) assume a segunda leitura.
7. **Compartilhar na web**: o resultado do experimento vira página pública? Isso muda a forma de escrever o experimento.
8. **Onde moram os evals**: tirar `**/evals/` do `.gitignore`, ou guardar os evals em outra pasta?

Ponto-chave: oito perguntas, e a sexta decide a forma final da tese sobre contagem.

## 13. Fontes

Os links abaixo são os que as duas pesquisas de 1 de novembro de 2026 usaram.
Os marcados "conferir" vieram da memória do agente de pesquisa e não foram abertos.

### 13.1 Documentação da Anthropic (seção 7.1)

- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompting Claude Fable 5.1: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Fable 5.1 migration guide: https://platform.claude.com/docs/en/models/fable-5-1/migration-guide
- Extended thinking: https://platform.claude.com/docs/en/build-with-claude/thinking
- Thinking steering and cost: https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost
- Reduce hallucinations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Define success: https://platform.claude.com/docs/en/test-and-evaluate/define-success
- Develop tests: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Agent Skills best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code best practices: https://code.claude.com/docs/en/best-practices
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code plugin evals: https://code.claude.com/docs/en/plugin-evals
- Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Building effective agents: https://www.anthropic.com/research/building-effective-agents
- Evaluating skills (agentskills.io): https://agentskills.io/skill-creation/evaluating-skills
- Post sobre skill-creator: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- skill-creator SKILL.md: https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md

### 13.2 Literatura (seção 7.2)

Divagação e escuta:

- Varao Sousa, Carriere e Smilek 2013, Frontiers in Psychology, 211 adultos: https://doi.org/10.3389/fpsyg.2013.00892
- Steindorf, Pink, Rummel e Smallwood 2023, Cognitive Research, 175 adultos: https://doi.org/10.1186/s41235-023-00483-0
- Szpunar, Khan e Schacter 2013, Proceedings of the National Academy of Sciences (PNAS), 80 adultos: https://doi.org/10.1073/pnas.1221764110
- [TDAH] Bozhilova e colegas 2020, Journal of Attention Disorders, 27 contra 29: https://doi.org/10.1177/1087054720956714
- [TDAH] Seli e colegas 2015, Psychonomic Bulletin and Review, divagação espontânea e TDAH: https://doi.org/10.3758/s13423-014-0793-0

Sinalização na fala:

- Lorch, Chen e Lemarié 2012, Journal of Experimental Psychology: Applied, prévia em texto e áudio (conferir): https://doi.org/10.1037/a0029342
- Chen e Lorch 2018, Journal of Experimental Psychology: Applied, título dito com prosódia: https://doi.org/10.1037/xap0000143
- Flowerdew e Tauroza 1995, Studies in Second Language Acquisition, marcadores retirados de uma aula: https://doi.org/10.1017/S0272263100014406
- Cevasco 2009, Memory and Cognition, conectivos na fala espontânea: https://pubmed.ncbi.nlm.nih.gov/19476219/

Narrativa:

- Mar, Li, Nguyen e Ta 2021, meta-análise, Psychonomic Bulletin and Review: https://doi.org/10.3758/s13423-020-01853-1
- Wolfe e Woodwyk 2010, British Journal of Educational Psychology, o limite da narrativa: https://doi.org/10.1348/000709910X485700

Dado antes do novo:

- Clark 1975, "Bridging", que descreve a estratégia dado-novo de Haviland e Clark 1974: https://web.stanford.edu/~clark/1970s/Clark.Bridging.75.pdf
- Clifton e Frazier 2004, Memory and Cognition, o ganho depende da construção: https://doi.org/10.3758/bf03196867

Diálogo:

- Craig, Gholson, Ventura e Graesser 2000, International Journal of AI in Education, 48 alunos: https://people.cs.pitt.edu/~litman/courses/slate/pdf/paper.pdf
- Driscoll e colegas 2003, Journal of Educational Computing Research, só a pergunta profunda funciona: https://digitalcommons.memphis.edu/facpubs/8941
- Chi e Roy 2006, Cognitive Science Society, observar diálogo: https://repositories.cdlib.org/content/qt5k61x8cw/qt5k61x8cw.pdf
- Muller e Sharma 2007 e 2008, mais de mil alunos de física, refutação da concepção errada: https://openjournals.library.sydney.edu.au/IISME/article/view/6345

Velocidade, prosódia e voz sintética:

- Murphy e colegas 2022, Applied Cognitive Psychology, 231 adultos, 1x a 2,5x (conferir): https://doi.org/10.1002/acp.3899
- Rabelo e Schochat 2007, Clinics, português brasileiro, inteligibilidade: https://doi.org/10.1590/S1807-59322007000300002
- Paris e colegas 2000, Human Factors, prosódia errada carrega a memória: https://doi.org/10.1518/001872000779698132
- Dinçer 2022, Journal of Pedagogical Research, voz sintética moderna sem diferença: https://doaj.org/article/a14435a205f54240bdd0b0db2fa06f91
- Bione e Cardoso 2020, Language Learning and Technology, 29 brasileiros: https://www.lltjournal.org/item-detail/944/
- Fraundorf e Watson 2011, Journal of Memory and Language, pausas preenchidas ajudam a recordação: https://doi.org/10.1016/j.jml.2011.03.004

Navegação falada:

- Dalton e colegas, cerca de 2013, Accident Analysis and Prevention, instrução composta e perigos não vistos: https://pure.royalholloway.ac.uk/files/12497853/Dalton_et_al._AA_P_accepted.pdf
- Burnett 1998, tese de Loughborough, guia por marco contra por distância: https://repository.lboro.ac.uk/articles/_Turn_right_at_the_King_s_Head_drivers_requirements_for_route_guidance_information/9355379
- Antrobus, Large, Burnett e Hare 2019, Journal of Navigation, 61 motoristas (conferir): https://doi.org/10.1017/S0373463318000875

Adultos com TDAH e audição:

- [TDAH] Dige, Maahr e Backenroth-Ohsako 2009, Journal of Attention Disorders, 69 contra 66: https://doi.org/10.1177/1087054709347245
- [TDAH] Blomberg e colegas 2021, Frontiers in Human Neuroscience, 17 contra 17: https://doi.org/10.3389/fnhum.2021.771711
- [TDAH] Alderson e colegas 2013, Journal of Abnormal Psychology, meta-análise de memória de trabalho: https://doi.org/10.1037/a0031742
- [TDAH] Stern e Halamish 2023, Frontiers in Psychology, 36 contra 36, recordação do texto inteiro: https://doi.org/10.3389/fpsyg.2023.1301726

Assistentes de voz e TDAH:

- [TDAH] Bryant e colegas 2026, Journal of Medical Internet Research (JMIR) Formative Research, co-design de chatbot: https://doi.org/10.2196/85013
- [TDAH] O'Connell e colegas 2024, conferência Human-Robot Interaction (HRI), robô companheiro de estudo: https://doi.org/10.1145/3610977.3634929

### 13.3 Do próprio Projeto

- Instruções do Projeto, SET_VERSION 2026-10-14-r1.
- `claude/clear-read-pesquisa-consolidada.md`, 13 de outubro de 2026.
- clear-read 2.3.3: SKILL.md, references/research-basis.md, references/tests.md, scripts/lint_clear_read.py.
- clear-listen: SKILL.md, references/research-basis.md, references/tests.md, scripts/lint_audio_script.py.
- Memória do Projeto: notas de 13, 14 e 24 de outubro de 2026 sobre a clear-read, o Projeto e os nomes das seções.

Ponto-chave: 19 páginas da Anthropic, cerca de 30 estudos, e os arquivos do próprio Projeto.
