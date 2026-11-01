# Decisões do Dennis: as perguntas da seção 12 do guia, respondidas

REGISTRADO: 2026-11-01 (Berlim), no Claude Code, num questionário em quatro rodadas
PARA: as Fases D e E, e qualquer agente que retome o trabalho

## 0. O que este arquivo é

A seção 12 do guia lista as perguntas que só o Dennis responde.
A Fase B acrescentou duas, e a conversa acrescentou mais uma.
Este arquivo registra o que o Dennis respondeu em 1 de novembro de 2026, e o que cada resposta muda.
Onde ele pediu ajuda em vez de decidir, o arquivo registra a ajuda dada e a escolha final.

Ponto-chave: todas as perguntas estão respondidas, inclusive a aprovação do plano da Fase E, e uma (o perfil Projeto) foi respondida por pesquisa.

## 1. As respostas

| Pergunta | Resposta | O que muda |
|---|---|---|
| 8. Onde moram os evals | `tests/evals/` dentro de cada skill, por exemplo `plugins/dc/skills/clear-read/tests/evals/evals.json` | A fonte dos evals ficou nesse caminho. A ferramenta `claude plugin eval` recusa evals dentro de `skills/`, então um script gera as cópias que ela lê em `plugins/dc/evals/`, e o `.gitignore` mudou para deixar as duas pastas entrarem |
| Nova. O perfil Projeto tem Python e ffmpeg? | "Não sei. Pesquise." A pesquisa está na seção 2 | O perfil Projeto passa a ter Python e, com alta probabilidade, ffmpeg. A matriz da Fase B muda em três linhas, e `lacos.md` ganha uma errata |
| 2. Terceira skill ou seção | Voz na clear-listen, texto fica na clear-read. O modo conversa vira a seção "Conversa por voz" no topo da clear-listen. O chat de texto continua com a clear-read, que só ganha a frase "papel antes do nome" | Confirma a recomendação da seção 6 de `lacos.md`. A renderização por motor da clear-listen precisa ir para `references/` para abrir espaço |
| 6. Sinalização na fala: toda contagem trava, ou só antes do conteúdo? | "Não sei, quero sentir no experimento" | A Regra 3 da clear-listen fica como está até a Fase D. A Fase D gera as duas formas e o Dennis ouve às cegas |
| 1a. Nome de "O chão" | "O que saber antes de ler" | Entra na proposta 9.5 da Fase E. Título completo sugerido: "O que saber antes de ler: os conceitos que o artigo não explica" |
| 1b. Nome de "Para este guia ficar" | "Exercícios de fixação" | Entra na proposta 9.5. Título completo sugerido: "Exercícios de fixação: as perguntas deste guia voltam em dias" |
| 3. Custo do áudio no experimento | Gerar os 4 áudios, cerca de 11 mil créditos | A Fase D gera os áudios pela ElevenLabs e mede a taxa real |
| 5. Semana da leitura cega | Nenhuma data. O Dennis quer o experimento como um artefato interativo que se mantém, que ele e outras pessoas (sem conta no Claude) respondem, e que o agente observa | Muda o desenho da Fase D: a leitura cega vira uma página com link público, respostas guardadas, e o agente lê as respostas. A seção 3 detalha |
| 7. Compartilhar na web | O Dennis já publica páginas pelo Projeto e pediu ajuda para entender a pergunta. A seção 4 explica o que a pergunta quer dizer e registra a assunção | Assunção: o relatório do experimento nasce como guia clear-read, em artefato privado, pronto para virar público quando o Dennis quiser |
| Nova. Exportar o roteiro neutro para o golden set da clear-listen | Os dois: suplementos (3 minutos e meio) e burnout (12 minutos) | Pendente de o Dennis colar os roteiros aqui ou salvá-los em `roteiros/`. A clear-listen ganha o golden set quando eles chegarem |
| Nova. Registrar a clear-listen no plugin | Sim, neste branch | Feito: a skill entrou no README, no CLAUDE.md e nas palavras-chave do `plugin.json` |
| 4. Ordem das fases | Resolvida pelo andamento: A, B e C rodaram em sequência no mesmo dia | Nada muda |
| Nova. "Um pesquisador mostrou" basta? | Não. Papel sem nome é autoridade vaga, como "o melhor restaurante, segundo a pesquisa". O papel vem primeiro e o nome e a fonte vêm logo depois | A mudança 2 da proposta ganha a segunda metade da regra e um segundo aviso de lint, `authority-without-name` |
| Nova. O plano da Fase E entra? | Sim, os 15 consertos; a mudança 16 (contagem antes da lista) espera a Fase D. Respondido em 1 de novembro, à noite, depois de uma explicação sem códigos | A implementação roda no branch filho `investigacao-2026-11-fase-e`, um commit por mudança |
| Nova. O parágrafo do narrador entra onde? | Nas duas skills, texto e áudio | A mudança 13 entra na clear-read e na clear-listen |
| Nova. A Regra 9 (tom) abre para falar com o leitor? | Sim. "Sem personalidade" sai; fica "sem enfeite que não sirva a um conceito" e "como num e-mail de trabalho a um colega" | A mudança 14 segue a primeira opção da seção 5 da proposta |
| Nova. Como a atribuição entra no texto? | No fio, como a BBC faz, para tudo que tem nome (pessoa, instituição, lugar, empresa, estudo, lei): "Uma pesquisa da Universidade de Oxford, no Reino Unido, feita pelo psicólogo Fulano, encontrou que...". Fluida, gentil, sem nota solta depois da frase. O Dennis citou o BBC Lê como modelo | A proposta ganha a mudança 17 (atribuição no fio) para as duas skills, e a seção 5.5 de `pesquisa-conferida.md` traz a fonte da BBC |
| Nova. As mudanças 20 e 21 (adendo 2) entram? | Sim, as duas. Respondido em 2 de novembro, depois de uma explicação sem códigos | Feitas no branch filho em 11 commits |
| Nova. As skills guardam de onde vêm as regras? | Sim. O Dennis quer que a skill diga que contém as referências e consiga responder "de onde vem" e buscar mais, sem carregar todos os estudos | A Fase E ganha um PR "research-basis conferido": o mapa regra, afirmação, veredito, fonte, certeza e data de conferência vira tabela no `research-basis.md` das duas skills; o `SKILL.md` ganha uma linha para o caso "o leitor pergunta por quê"; a história da composição fica em `investigacao-2026-11/` com um ponteiro |

## 2. O perfil Projeto, pela pesquisa

A pergunta era se o Claude, dentro do Projeto no app, roda Python e ffmpeg.
O Dennis achou que sim, porque as skills no app rodam Python.
A pesquisa confirma a parte do Python e dá uma resposta provável para o ffmpeg.

A documentação da ferramenta de execução de código da Anthropic diz que o contêiner tem Python 3.11, sem internet, e lista as bibliotecas instaladas.
Ela não cita ffmpeg.

Um usuário publicou um inventário do contêiner de skills do claude.ai, como gist.
Ele lista Python 3.12, Node 22 e FFmpeg 6.1.1 com ffprobe.
As instruções do Projeto (seção 6.4) e o playbook de áudio (seção 12) mandam juntar os áudios com ffmpeg.
Os áudios do Projeto foram produzidos assim.

Então a resposta de trabalho é: o perfil Projeto tem Python e tem ffmpeg.
A fonte oficial confirma o Python, e o ffmpeg vem de um inventário de terceiro mais a prática do próprio Projeto.
O teste de um minuto que fecha a dúvida: pedir ao Claude, dentro do Projeto, que rode `python3 --version` e `ffmpeg -version`.

O que muda na Fase B: a fase de rodar o lint, da clear-read, passa a "roda" no Projeto.
A R12 (voz por papel, medir a taxa) e a checagem final da clear-listen sobem para "degrada só na escuta".
O motivo: a medição de pausas e de taxa passa a existir.
A seção 1 de `lacos.md` fica com a decisão antiga registrada e esta errata ao lado.

Ponto-chave: o guia estava errado e as instruções do Projeto estavam certas; o Projeto roda Python e, quase com certeza, ffmpeg.

## 3. O experimento como artefato interativo

O Dennis não quer agendar a leitura cega.
Ele quer uma página que fica de pé, que ele abre quando puder, e que outras pessoas também podem responder.
Ele quer que o agente observe as respostas.

Isso muda três coisas no desenho da Fase D (seção 8 do guia).
Primeiro, o material vira uma página só: os 4 pares de guias, em ordem aleatória por leitor, sem dizer qual versão é qual.
Segundo, as medidas com o leitor (esforço, onde travou, e as 3 perguntas de recordação) viram formulários dentro da página.
A página guarda as respostas com a data.

Terceiro, a recordação em 24 horas vira um lembrete dentro da página, e não uma sessão marcada.

Duas restrições técnicas precisavam de teste antes de construir, e o teste rodou em 1 de novembro.
Uma página que guarda respostas precisa da capacidade de banco de dados do artefato.
A nota do Projeto de 13 de outubro diz que uma página com banco não tinha link público.

O que a skill `artifact-capabilities` diz, lida na fonte: o banco devolve nulo para quem não está logado no Claude.
Então um visitante sem conta nunca grava no banco, mesmo que a página abra.
A página pode abrir para ele, e ela precisa dizer o que fazer nesse caso.

O teste publicado: https://claude.ai/artifact/4DHcwb2iqK7dkdVr1zgmRH, uma página com banco que mostra o estado do banco a quem a abre.
O que falta é um passo que só o Dennis faz, em um minuto.
Abrir o menu Compartilhar dessa página e ver se existe a opção de link para qualquer pessoa.
Se existir, abrir o link numa janela anônima e ler o que o cartão "Estado do banco" diz.

O desenho que fica, com qualquer resultado desse teste:

- Quem tem conta no Claude (o Dennis e convidados) responde na página, e a resposta vai para o banco.
- Quem não tem conta responde na mesma página, e no fim ela mostra um bloco de texto com as respostas, com botão de copiar.
- A pessoa manda esse texto ao Dennis (WhatsApp ou e-mail), e o Dennis cola na página, logado, ou cola aqui no Claude Code.
- O agente lê o banco pela ferramenta de dados do artefato e escreve a análise.

Se o menu Compartilhar não oferecer link público, a página pública é uma cópia sem banco, só com o bloco de copiar.
O download de arquivo não serve: a página não pode iniciar downloads para quem a vê.

Ponto-chave: a Fase D vira um artefato que coleta pelo banco para quem tem conta e por texto copiado para quem não tem.

## 4. A pergunta sobre a web, explicada

A pergunta 7 do guia é esta: o resultado do experimento vira uma página pública?
Ela não é sobre os guias, que o Projeto já publica.
Ela é sobre o relatório do próprio experimento: a comparação entre a skill atual e a revisada, com as medidas e a conclusão.

A pergunta importa porque muda a escrita.
Um relatório para o Dennis pode usar os nomes do Projeto (Biblioteca, playbook, SET_VERSION) e os dados dele.
Um relatório para a web precisa explicar o que é o Projeto, esconder os dados pessoais de leitura, e carregar as fontes de cada regra.

A assunção que fica, até o Dennis dizer o contrário: o relatório nasce no formato de guia clear-read, como artefato privado.
Ele não leva nomes internos nem dados pessoais no corpo.
Assim ele vira público com um clique, e os dados de leitura ficam numa seção separada que o Dennis decide se mostra.

Ponto-chave: a pergunta é sobre o relatório, não sobre os guias, e a assunção é escrever já no formato público.
