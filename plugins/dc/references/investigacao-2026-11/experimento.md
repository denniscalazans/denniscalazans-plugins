# Fase D: o experimento, parte 1, as medidas que não dependem de gente

CRIADO: 2026-11-01 (Berlim), no Claude Code.
FASE: D, do guia `guia-de-investigacao.md` (seção 8).
STATUS: as medidas automáticas e o leitor frio artificial estão prontos. A leitura cega pelo Dennis e por outras pessoas está aberta e sem data de fim.

## 0. O que este arquivo é

O experimento responde uma pergunta: a skill revisada produz um texto melhor, ou só diferente?
Este arquivo guarda o desenho, o que já foi medido e onde as respostas das pessoas chegam.
A conclusão em cinco frases entra na seção 7 quando as respostas chegarem.

Os textos estão em `experimento/textos/`, com nomes cegos: `duckdb-1`, `duckdb-2`, `suplementos-1`, `suplementos-2`.
Qual é a skill antiga e qual é a nova está selado fora deste arquivo, até a leitura cega terminar.

Ponto-chave: dois pares de textos, quatro medidas automáticas, um leitor frio artificial, e a leitura cega aberta numa página.

## 1. O desenho, como rodou

O guia pedia quatro pares. Por causa do limite de uso do Dennis, rodaram dois.
Um tema fica dentro da área dele (DuckDB e formatos de arquivo) e um fora (suplementos, do artigo da BBC).

Cada par tem duas versões do mesmo guia.
Uma foi escrita por um agente com a skill clear-read do branch `investigacao-2026-11` (a antiga).
A outra, por um agente com a skill do branch `investigacao-2026-11-fase-e` (a nova, com os 19 consertos).

Os dois agentes receberam o mesmo pedido, em `experimento/fontes/braco-prompt.md`.
Eles receberam a mesma ficha de fatos e o mesmo mapa de ideias (`experimento/fontes/duckdb-fonte.md` e `suplementos-fonte.md`), sem acesso à web.
Mesmo modelo, mesmo esforço, mesmas ferramentas, e cada um rodou o lint da própria skill até zerar os problemas.

Três coisas mudaram em relação ao guia, seção 8.1.
Dois pares em vez de quatro.
O DuckDB não tem artigo de origem, então a ficha de fatos veio do guia já publicado.
E o áudio e a conversa por voz ficaram para uma segunda rodada.

Ponto-chave: a única diferença entre as duas versões de cada par é a skill.

## 2. As medidas automáticas

O lint novo rodou sobre os quatro textos, com `experimento/medidas.py`.
Os problemas são zero nos quatro, porque cada agente zerou o lint da própria skill antes de entregar.
Os avisos mostram o que o lint novo vê e o antigo não via.

| Texto | Palavras | Avisos do lint | Autoridade sem nome | "Você já sabe que..." | "O que saber antes de ler" | Seções | Visuais |
|---|---|---|---|---|---|---|---|
| duckdb-1 | 2.274 | 12 | 0 | 5 | 0 | 6 | 1 |
| duckdb-2 | 2.462 | 0 | 0 | 1 | 0 | 9 | 3 |
| suplementos-1 | 2.002 | 0 | 0 | 4 | 1 | 6 | 1 |
| suplementos-2 | 2.039 | 4 | 4 | 0 | 0 | 6 | 1 |

Como ler: cada linha é um texto; "Autoridade sem nome" conta frases como "pesquisas mostram" sem nome; "Você já sabe que..." conta as linhas de reentrada entre seções.
Os doze avisos de `duckdb-1` são siglas de SQL e de instituições que a ficha de fatos não expandia.
Nenhum é rótulo nu nem referência para trás.

Ponto-chave: em cada par, só uma versão usa a linha de reentrada, e só uma versão de suplementos tem autoridades vagas.

## 3. O leitor frio artificial

Um agente leu cada texto uma vez e respondeu as perguntas de revisão de memória (`experimento/fontes/perguntas.json`).
Ele também contou quantas vezes voltou no texto e citou três frases em que tropeçou.
Os resultados estão em `experimento/leitor-frio/`.

| Texto | Pontos acertados | Voltas ao texto |
|---|---|---|
| duckdb-1 | 16 de 16 | 3 |
| duckdb-2 | 16 de 16 | 3 |
| suplementos-1 | 15 de 15 | 2 |
| suplementos-2 | 15 de 15 | 2 |

Como ler: o leitor artificial acertou tudo nos quatro textos, então essa medida não separa as versões.
O que separa são os tropeços citados, e eles viraram achados:

- Em `duckdb-1`, um título promete "sete comandos" e a lista abaixo tem quatro itens agrupados. O leitor voltou para conferir se tinha pulado algum. É uma promessa não cumprida, do tipo que a investigação inteira persegue.
- Em `suplementos-1`, a frase "Presidente do Royal College of GPs (...), a professora Victoria Tzortziou Brown resume o problema" fez o leitor tropeçar. O papel veio antes do nome, como a regra pede, mas numa inversão longa. A regra de atribuição no fio precisa de um exemplo na ordem natural.
Assim: "A professora Victoria Tzortziou Brown, presidente do Royal College of GPs, resume o problema".
- Em `suplementos-1`, "disse uma nutricionista à BBC" e, logo depois, "a nutricionista Kristen Stavridis" deixaram a dúvida se eram a mesma pessoa.
- Em `duckdb-2`, o atalho `@~parquet` e a frase sobre lotes de valores por coluna foram os pontos de tropeço, os dois no conteúdo mais técnico.

Ponto-chave: um leitor artificial satura a medida de recordação; a medida que decide é a das pessoas.

## 4. A leitura cega, aberta

A leitura cega roda numa página, não numa sessão marcada.
A página mostra os quatro textos em ordem embaralhada por pessoa, sem dizer qual versão é qual.

Depois de cada texto, ela pede o esforço (1 a 5), quantas releituras, onde travou (toque no parágrafo), e três perguntas de recordação.
Depois de cada par, pede qual dos dois exigiu menos esforço.
Um dia depois, ela pede as mesmas perguntas sem os textos.

Duas cópias da mesma página:

- Privada, com banco de dados: https://claude.ai/artifact/6mJHWPEbZPy1PzPpm5fj8x. Para quem tem conta no Claude. As respostas gravam na página, uma por pessoa, e só o dono lê.
- Pública, sem banco: https://claude.ai/artifact/5AxWJiXQvm7zWYfMuaUtys. Para quem não tem conta. No fim, a página mostra um bloco de texto para copiar e enviar ao Dennis. O Dennis ainda precisa ligar o link público no menu Compartilhar.

O mapa cego (qual texto é qual) está selado em dois lugares.
Um é o banco da página privada, documento `meta/mapa-cego`; o outro é a pasta de trabalho da sessão.
Ele entra neste arquivo depois que o Dennis terminar a leitura.

Ponto-chave: a página coleta; o agente lê as respostas pelo banco e analisa quando elas chegarem.

## 5. O que invalida, e o que ficou de fora

- As duas versões rodaram no mesmo contexto: um agente limpo, só com a skill e a ficha. Nenhuma viu a outra.
- O Dennis não sabe qual é qual até abrir o mapa selado.
- A Fase E mudou 19 coisas de uma vez, e não duas. O experimento mede o conjunto, não cada mudança. Uma segunda rodada pode isolar as duas de maior impacto (rótulos e linha de reentrada).
- Áudio e conversa por voz não entraram nesta rodada.

Ponto-chave: o experimento mede o pacote inteiro da Fase E, e isso precisa ficar dito na conclusão.

## 6. Como analisar quando as respostas chegarem

1. Ler o banco da página privada (coleção `respostas`) e os blocos enviados por quem usou a cópia pública.
2. Abrir o mapa selado e trocar os nomes cegos pelas condições.
3. Para cada par e cada pessoa: esforço, releituras, parágrafos marcados, pontos de recordação na hora e um dia depois. Mais a escolha "qual exigiu menos esforço".
4. Uma tabela por par, condições nas colunas, medidas nas linhas. Sem estatística pesada; o que se procura é direção consistente.
5. Escrever a seção 7 em cinco frases, e só então decidir o merge do PR #81.

## 7. Conclusão, parte 1: a primeira passada do Dennis

O Dennis leu os quatro textos em 1 de novembro, das 22h40 às 23h31 (horário de Londres), como dono da página.
A resposta está em `experimento/respostas/dennis-2026-11-01.json`.
A volta de um dia depois ainda não aconteceu, então o mapa cego continua selado, e esta seção usa os nomes cegos.

| Par | Texto | Ordem de leitura | Minutos lendo | Esforço (1 a 5) | Releituras | Pontos lembrados |
|---|---|---|---|---|---|---|
| suplementos | 2 | primeiro | 7 | 2 | uma | 4 de 6 |
| suplementos | 1 | segundo | 4,5 | 2 | uma | 3,5 de 9 |
| duckdb | 2 | primeiro | 10,5 | 3 | duas ou três | 4,5 de 7 |
| duckdb | 1 | segundo | 19 | 2 | duas ou três | 4,5 de 9 |

Como ler: cada par tem perguntas diferentes por texto, então os pontos não se comparam dentro do par. O esforço e as releituras se comparam.
Os pontos saem da leitura das respostas contra a lista de `experimento/fontes/perguntas.json`, feita pelo agente.

O que a primeira passada diz:

- Nos dois pares o Dennis marcou "deu igual". No par de suplementos, o comentário dele vai além da nota. O texto 1 foi "mais fluido" e "mais suave para o meu cérebro"; o texto 2 foi "mais duro", com os termos "mais soltos". Ele mesmo avisa que leu o 2 primeiro, e a segunda leitura de um assunto é sempre mais fácil.
- No par de DuckDB, o esforço caiu de 3 para 2 entre o texto 2 e o texto 1, com o mesmo número de releituras. O tempo de leitura do texto 1 (19 minutos) inclui as respostas às três perguntas do texto anterior, então não vale como medida.
- A queixa mais útil veio do texto 2 de DuckDB. Nas palavras do Dennis: "o texto não explicou muito bem; essa skill assume que eu sei tudo, e isso não é verdade". É a calibragem da Regra 8, que trata o leitor de TI como quem já sabe o básico de DuckDB. O Dennis diz que não sabe, e isso vira um achado para a Regra 8, seja qual for a versão.
- As respostas de recordação foram curtas e certas na direção, com os detalhes perdidos (os nomes das substâncias, o atalho do Hugging Face, os números). Isso é o esperado logo depois da leitura; a volta de um dia depois mede o que fica.

Ponto-chave: o texto 1 de cada par saiu igual ou um pouco melhor, e a queixa sobre o DuckDB é o achado mais concreto.

## 8. O que falta para fechar

- A volta de um dia depois do Dennis, pelo mesmo link e navegador, a partir de 2 de novembro às 23h31 (Londres).
- Outras pessoas, se o Dennis quiser, pela cópia pública.
- Abrir o mapa selado e reescrever a seção 7 com as condições no lugar dos nomes cegos, em cinco frases.
- Só então decidir o merge do PR #81.
