# Fonte para o guia "DuckDB, formatos de arquivo, notebook e Hugging Face"

Pedido original do leitor (7 de outubro de 2026, no chat): "Me explica do zero ao avançado o que são CSV, JSON, JSONL e Parquet, o que é o DuckDB, o que é um notebook Jupyter e como o Hugging Face entra nisso. Quero chegar no nível de quem usa o Claude Code há anos."

Não existe artigo de origem. Esta ficha de fatos foi conferida nas fontes abaixo e é a única fonte permitida. Não pesquise na web. Não invente fatos fora desta ficha.

## Mapa de ideias (os conceitos principais, na ordem de dependência)

1. Formatos por linha e por coluna: CSV, JSON e JSONL escrevem a tabela linha por linha; o Parquet guarda cada coluna em um bloco separado, então uma soma de uma coluna lê menos.
2. DuckDB como biblioteca, sem servidor: um banco de dados que roda dentro do programa que o chama e trata arquivos como tabelas.
3. Notebook, kernel e ordem das células: o kernel guarda as variáveis na memória e só conhece o que as células já rodadas criaram; a memória segue a ordem dos cliques, não a da página.
4. Hugging Face e o endereço hf://: um site que hospeda datasets, gera uma cópia em Parquet ao lado do arquivo publicado, e o DuckDB consulta pelo endereço.
5. Por que o Claude Code usa o DuckDB: o arquivo inteiro não cabe na janela de contexto; o DuckDB lê fora da conversa e devolve só o resumo.
6. Dados maiores que a memória: o DuckDB grava dados temporários no disco quando a memória acaba; algumas consultas complexas ainda podem falhar.

## Fatos conferidos

### Dado, tabela, arquivo, formato
- Um dado é um fato anotado ("o pedido 1 foi para São Paulo e custou 564 reais" tem três dados).
- Uma tabela é uma grade: uma linha é uma coisa inteira, uma coluna é uma característica de todas as coisas.
- Um arquivo tem nome e conteúdo; a extensão (depois do ponto) avisa o que tem dentro. Arquivos de texto abrem em qualquer editor; arquivos binários só fazem sentido para o programa certo.
- Um formato é a regra de como escrever a tabela dentro do arquivo.

### Os quatro formatos
- CSV: "comma-separated values". Cada linha do arquivo é uma linha da tabela, vírgula separa as colunas, a primeira linha traz os nomes das colunas. Tudo é texto: o arquivo não diz se "564.31" é número. A RFC 4180 diz que nunca existiu uma regra formal para o CSV, e por isso cada programa grava de um jeito (vírgula ou ponto e vírgula). Fonte: RFC 4180, https://www.rfc-editor.org/rfc/rfc4180.
- JSON: "JavaScript Object Notation". Uma ficha em que cada valor tem uma etiqueta ("cidade": "Recife"). Chaves { } abrem uma ficha, colchetes [ ] abrem uma lista, uma ficha pode morar dentro de outra. Custo: cada ficha repete as etiquetas, o arquivo fica grande. O settings.json e o .mcp.json do Claude Code são JSON. Fonte: https://code.claude.com/docs/en/claude-directory.
- JSONL: "JSON Lines", uma ficha JSON completa por linha. O programa acrescenta uma linha no fim sem reescrever o arquivo; por isso é o formato comum de registros (logs). O Claude Code grava cada sessão em JSONL, uma mensagem por linha, em ~/.claude/projects/<projeto>/<sessão>.jsonl. Esses arquivos não são protegidos por senha: uma senha mostrada na tela fica gravada. Fontes: https://jsonlines.org/ e a documentação do Claude Code.
- Parquet: escreve coluna por coluna (todas as cidades juntas, depois todos os valores). Arquivo binário. Comprime bem porque valores da mesma coluna se parecem ("pago, 3 vezes" em vez de "pago, pago, pago"). Anota o número de linhas no fim do arquivo, por isso contar linhas é rápido.
- Teste feito para o guia original (dados aleatórios, máquina pequena, DuckDB 1.5.6): 1 milhão de pedidos com seis colunas; o Parquet ficou 4 vezes menor que o CSV e respondeu 12 vezes mais rápido à pergunta "total dos pedidos pagos por cidade"; o JSON deu o maior arquivo.
- Quando usar: CSV se uma pessoa vai abrir no editor ou no Excel; JSON se há ficha dentro de ficha; JSONL se o arquivo cresce uma linha por vez; Parquet se o arquivo é grande e serve para somar e contar.

### SQL e DuckDB
- SQL: "Structured Query Language". Uma consulta (query) tem SELECT (o que mostrar), FROM (de onde vem a tabela), WHERE (quais linhas entram), GROUP BY (como juntar em grupos).
- Programa (código que você manda rodar), biblioteca (código pronto que um programa carrega), servidor (programa que fica ligado esperando pedidos). A maioria dos bancos de dados é servidor: o PostgreSQL precisa ser instalado, ligado e mantido.
- O DuckDB é um banco de dados em forma de biblioteca: responde SQL de dentro do programa que o chama, sem servidor, e lê CSV, JSON, JSONL e Parquet direto como tabelas (FROM 'pedidos.csv'). Fonte: https://duckdb.org/why_duckdb.html.
- O DuckDB deduz os tipos de um CSV lendo uma amostra. Fonte: https://duckdb.org/docs/current/data/csv/auto_detection.
- O DuckDB processa um lote grande de valores da mesma coluna por passo (como o Parquet); PostgreSQL, MySQL e SQLite processam uma linha por vez. Por isso Parquet e DuckDB combinam: nenhum gasta trabalho com colunas que a pergunta não usa.
- Origem: Mark Raasveldt e Hannes Mühleisen criaram o DuckDB no CWI, centro de pesquisa de Amsterdã; o artigo de 2019 (SIGMOD) parte do sucesso do SQLite, um banco em forma de biblioteca, e propõe um banco em biblioteca para somar e contar muitos dados. Fonte: https://www.duckdb.org/library/duckdb-sigmod-demo/.
- Dados maiores que a memória: o DuckDB grava dados temporários no disco quando a memória acaba; algumas consultas complexas ainda podem falhar por falta de memória.
- Exemplo de consulta: SELECT cidade, round(sum(valor)) AS total FROM 'pedidos.parquet' WHERE status = 'pago' GROUP BY cidade ORDER BY total DESC; (1 milhão de linhas entram, 6 linhas voltam).

### Notebook
- O Jupyter é o programa mais conhecido para notebooks. Um notebook é uma lista de células; uma célula é um bloco de texto ou de código que roda sozinho. O código costuma ser Python; uma variável é um nome que guarda um valor.
- O kernel é o programa que executa as células e guarda as variáveis na memória; a tela envia o código ao kernel e recebe o resultado. Uma célula que roda antes da célula que cria a variável dá erro. O número entre colchetes mostra a ordem real de execução. Fonte: https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html.
- Estudo de Pimentel e colegas (Universidade Federal Fluminense e Universidade de Nova York, MSR 2019): rodaram de novo cerca de 864 mil notebooks públicos do GitHub; 24 em cada 100 rodaram sem erro e 4 em cada 100 repetiram o mesmo resultado. Causas: bibliotecas faltando, memória escondida, células fora de ordem. O que funciona: "Restart and Run All". Fonte: https://2019.msrconf.org/details/msr-2019-papers/36/.
- O arquivo .ipynb é um JSON; a etiqueta "cells" guarda a lista de células. Fonte: https://nbformat.readthedocs.io/en/latest/format_description.html.
- Prática: explorar no notebook e, com a análise pronta, passar o código para um arquivo .py.

### Hugging Face
- Site que hospeda modelos de IA, datasets e aplicativos de demonstração. Um dataset é um conjunto de dados publicado com dono e nome (stanfordnlp/imdb: 25 mil críticas de filmes); cada dataset é um repositório com histórico; pode ser público ou privado. Fonte: https://huggingface.co/docs/hub/datasets-overview.
- O Hugging Face gera uma cópia em Parquet de um dataset publicado em CSV ou JSONL e guarda ao lado; o atalho @~parquet no endereço alcança a cópia. Fonte: https://huggingface.co/docs/dataset-viewer/parquet.
- O endereço hf://datasets/<dono>/<nome>/<caminho> liga o DuckDB ao dataset; o asterisco no caminho significa "todos os arquivos que combinam". Fonte: https://duckdb.org/docs/stable/core_extensions/httpfs/hugging_face.
- Teste feito para o guia original: contar as linhas de stanfordnlp/imdb pela internet levou cerca de 1 segundo (25.000 críticas); medir o tamanho médio dos textos levou cerca de 6 segundos, porque os textos viajam pela internet.
- "Sem download" precisa de contexto: nenhum arquivo é salvo no computador, mas os dados necessários viajam pela internet. O que funciona: explorar pela internet e gravar um recorte local (COPY (SELECT ... LIMIT 1000) TO 'recorte.parquet').
- Um dataset privado pede um token (senha longa criada no site), registrado no DuckDB uma vez.

### Claude Code
- A janela de contexto é a quantidade limitada de texto que o Claude lê por conversa; um CSV de 47 megabytes não cabe.
- Três motivos para o Claude usar o DuckDB: a resposta é pequena (1 milhão de linhas entram, 6 voltam); não precisa de servidor (um comando funciona em qualquer máquina); a mesma consulta lê qualquer formato.
- Sete comandos que cobrem quase todo o uso (DuckDB 1.5.6): FROM 'pedidos.csv' LIMIT 3; DESCRIBE FROM 'pedidos.csv'; SUMMARIZE FROM 'pedidos.csv'; FROM read_ndjson('logs/*.jsonl'); SELECT message.role AS quem, count(*) FROM read_ndjson('logs/*.jsonl') GROUP BY ALL; COPY (FROM 'pedidos.csv') TO 'pedidos.parquet'; em Python, duckdb.connect('loja.duckdb') e CREATE TABLE pedidos AS FROM 'pedidos.parquet' (1 milhão de pedidos ocuparam 5 megabytes).
- Usos: perguntar às sessões do Claude Code (read_ndjson sobre ~/.claude/projects/*/*.jsonl com ignore_errors = true); preparar dados do TSE para um app offline; explorar um dataset antes de baixar; guardar resultados de testes de IA em JSONL; ver sessões de agentes no visualizador de datasets do Hugging Face (Data Studio, seção Agent traces), em dataset privado porque pode haver senhas.

## Perguntas de revisão que o leitor vai responder depois (não copie as respostas literalmente, mas o texto precisa ensinar cada ponto)

1. Por que o computador lê menos em Parquet do que em CSV para somar uma única coluna?
2. Por que o DuckDB responde a consultas SQL sem servidor para instalar ou manter?
3. Por que uma célula de notebook dá erro quando roda antes da célula que cria a variável usada?
4. Como o DuckDB consulta um dataset do Hugging Face que foi publicado em CSV?
5. Por que o Claude roda uma consulta do DuckDB em vez de abrir um CSV grande?
6. Qual é a diferença entre o Parquet e o DuckDB, e por que os dois combinam?
7. Como o DuckDB lida com dados maiores que a memória do computador, e qual é o limite?
