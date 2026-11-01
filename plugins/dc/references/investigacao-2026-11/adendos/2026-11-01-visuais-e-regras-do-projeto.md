# Adendo 2: o que o Projeto já aprendeu sobre visuais e a clear-read ainda não sabe

ESCRITO: 2026-11-01 23:40 (Berlim), pelo Claude, numa conversa com o Dennis depois da Fase E.
PARA: o agente que executa o guia de investigação.

Quando incorporar: antes de começar o branch filho `investigacao-2026-11-fase-e`, ou como primeira mudança dele.
O que muda: a proposta ganha uma mudança 18, sobre a Regra 7 da clear-read. O inventário muda o veredito de R7c.

## 1. O que o Dennis apontou

O Dennis leu a proposta e viu que ela não mexe nos visuais.
A observação dele: o Projeto gastou muitos tokens aprendendo o que funciona numa página, e nada disso foi para a skill.
O exemplo que ele deu: a clear-read manda fazer diagrama Mermaid para uma sequência, e o Projeto já tinha corrigido isso.

A conferência confirma.
A Regra 7 da clear-read diz, na linha "Pick the form by the content": um fluxo ou uma estrutura ramificada vira um diagrama Mermaid.
O inventário da Fase A marcou essa regra (R7c) como "mantém" e "neutra".
A proposta de 17 mudanças não toca na Regra 7.

Ponto-chave: a Regra 7c manda usar Mermaid onde o Projeto já decidiu não usar, e a Fase A deixou passar.

## 2. O que o Projeto decidiu, e onde está escrito

As instruções do Projeto (cópia em `projeto/clear-read-web-project-instructions.md`, seção 7, "Technical rules") têm uma tabela de escolha de forma e uma lista de regras de diagrama.
A pesquisa consolidada (`projeto/clear-read-pesquisa-consolidada.md`, seção 3, item 6) registra a decisão.
"Manter Mermaid" caiu.
A regra ativa pb-004 do playbook da Biblioteca manda SVG inline, e os 3 guias lidos têm zero Mermaid.

As regras do Projeto, em resumo:

| Conteúdo | O que o Projeto manda | O que a clear-read diz hoje |
|---|---|---|
| Passos sem ramificação (uma sequência) | Lista numerada, ou um stepper em HTML. Nunca diagrama, porque um diagrama de caixas em fila repete a prosa e não mostra relação | "Um fluxo vira um diagrama Mermaid" |
| Estrutura de grafo de verdade (ramos, junções, mapa de conceitos) | SVG inline com tokens de tema. Mermaid só para fluxo linear simples, e com as regras de celular | O mesmo Mermaid, sem a preferência por SVG |
| Até 8 atores e suas ligações (quem é dono de quem, quem controla quem) | SVG inline com a relação ou o percentual ao lado da seta | Não existe regra |
| Números para comparar | Gráfico em SVG inline, com a skill `dataviz` carregada antes | "Um gráfico simples ou uma tabela" |
| Muitos atores com vários atributos | Tabela | Não existe regra |
| Grupo grande com dezenas de subsidiárias | Só os atores que o artigo cita, no máximo 8, mais um nó "e outras N empresas" | Não existe regra |
| Eventos datados | Lista em HTML estilizada como linha do tempo. Nunca Mermaid, porque o texto precisa quebrar no celular | Já está na skill, e em `html-patterns.md` seção 6 |

A regra de ouro do Projeto, escrita na lista "Diagrams" da seção 7: cada diagrama precisa acrescentar estrutura, nunca repetir a prosa.
Isso é mais forte que o teste das 4 perguntas da Regra 7a.
O teste decide se entra um visual.
A regra de ouro decide qual forma ele não pode ter.

Ponto-chave: o Projeto tem uma tabela de 7 linhas de forma por conteúdo, e a clear-read tem uma frase que manda para o Mermaid.

## 3. O motivo, para a skill guardar

O Mermaid foi derrubado por três motivos, e os três estão nos arquivos do Projeto.

Primeiro, o teste de 24 de setembro de 2026.
O app do Claude no celular não quebra o rótulo de um nó Mermaid, então um rótulo longo é cortado na borda.
E a página roda o Mermaid em modo estrito, que apaga `<br/>` e cola as palavras ("imobiliáriassuecas").
O `check_mermaid.cjs` existe por causa disso, e ele é um remendo para um problema que o SVG inline não tem.

Segundo, um diagrama de caixas em fila para uma sequência não mostra nada que a lista numerada não mostre.
Ele gasta espaço, corta no celular, e falha no teste das 4 perguntas da própria Regra 7a (zero "sim", porque a relação é só "depois").

Terceiro, o SVG inline usa os tokens de tema da página, então funciona no claro e no escuro.
O texto dele quebra como o `html-patterns.md` manda.

Ponto-chave: o Mermaid falha no celular, repete a prosa em sequências, e não segue o tema; o SVG inline resolve os três.

## 4. A mudança 18 para a proposta

**Regra 7, parágrafo "Pick the form by the content", reescrito.**

Texto proposto, em inglês, para o SKILL.md.
Ele segue a própria clear-read: um tópico por bloco, e no máximo 4 frases por bloco.

```
**Pick the form by the content, and never draw a sequence.**
A sequence of steps with no branch is a numbered list or an HTML stepper, never a diagram.
Boxes in a row repeat the prose and show no relation.

A real graph (branches, merges, a concept map) becomes inline SVG with the page's theme tokens.
Mermaid is only for a simple linear flow that must stay in Markdown, with the phone rules below.
Up to about 8 actors and their links become an inline SVG map, with the relation written on the arrow.

Numbers to compare become an inline SVG chart (load the `dataviz` skill first) or a table.
Many actors with several attributes each become a table.
A big group with dozens of members shows only the members the text names, at most 8, plus one node "and N others".
Dated events become an HTML timeline, never a diagram, because the text must wrap on a phone.

Every diagram must add a relation that the prose carries badly.
A diagram that only repeats the prose is cut.
```

O que entra em `references/html-patterns.md`: duas seções novas.
Uma é "An actor map as inline SVG (Rule 7)", com o snippet do mapa de atores que o Projeto usa (pb-004).
A outra é "A stepper for a sequence (Rule 7)".

O que entra no lint: um aviso novo, `sequence-as-diagram`.
Ele dispara quando um bloco Mermaid `flowchart` tem só arestas em cadeia (A --> B --> C, sem ramificação).
É aviso, não problema, porque um fluxo linear simples ainda é permitido quando o documento é Markdown puro.

Teste que falha antes e passa depois: um documento com um `flowchart TD` de 4 nós em fila, sem ramo.
Hoje o lint não diz nada.
Depois, ele avisa.

O inventário muda: R7c sai de "mantém, neutra" e vai para "muda", com este adendo como motivo.

Evidência: Berney e Bétrancourt 2016 para a forma por conteúdo (já no inventário).
Mais o teste do Projeto de 24 de setembro de 2026 para o celular, e a regra pb-004 do playbook.

Certeza: alta para "nunca sequência em diagrama", porque é o teste das 4 perguntas aplicado.
Média para a preferência por SVG, porque é prática do Projeto, não estudo.

Ponto-chave: a mudança 18 troca uma frase da Regra 7 por uma tabela de forma por conteúdo, mais um aviso de lint.

## 5. Outras regras do Projeto que a Fase E deve conferir contra a skill

O Dennis disse que há "muitas coisas" do Projeto que não foram para a skill.
A lista abaixo vem de uma leitura das instruções do Projeto, seções 7 e 8.
São regras que o SKILL.md da clear-read não tem.
Cada item precisa de um veredito na Fase E: entra na skill (método), fica no Projeto (produto), ou já existe de outra forma.

| Regra do Projeto | Onde está | Está na clear-read? | Veredito a dar |
|---|---|---|---|
| Marcador de progresso no topo de cada conceito ("Conceito 2 de 4") | Seção 7, item 6 | Só em `html-patterns.md` seção 3, não no SKILL.md | Candidata a método: serve a qualquer texto longo, não só ao Projeto |
| A ideia central em palavras na primeira frase da seção ("A ideia central aqui é") | Seção 7, item 6 | Não | Candidata a método |
| Bloco "Mito corrigido" com fonte | Seção 7, item 6 | Não. A Regra 3 pede problema mais contrapadrão, que é parecido mas não é | Candidata a método, porque corrigir um erro comum tem prova (Muller e Sharma, na pesquisa conferida) |
| Pré-perguntas no começo, respondidas no corpo, repetidas no quiz | Seção 7, itens 3 e 15 | Não | Candidata a método. A pesquisa consolidada tem a evidência (Decisão 1) |
| "Recapitule de cabeça" no fim: recordação do texto inteiro, não por seção | Seção 7, item 13 | Não | Candidata a método. Stern e Halamish 2023 está na pesquisa conferida |
| Duas camadas sempre visíveis: o que a fonte diz e o que foi acrescentado | Seção 7, "Two layers" | Só em `html-patterns.md` seção 8 | Já existe para HTML. Falta no SKILL.md para texto |
| Toda ideia carregada pelo texto; nenhuma só por tabela, gráfico ou interativo | Seção 13, "Never do" | Em parte: a Regra 7 diz "the text still carries every idea" | Já existe. Conferir se o leitor frio da clear-read (`tests.md`, Test 14) mede isso |
| Rótulo com conteúdo, nunca código nu ("P1 · cache antes do deploy") | Seção 8.1, item 1 | Sim, Regra 6 | Já existe |
| Negrito como trilha: só a linha mais importante de cada bloco | Seção 8 | Sim, Regra 10 | Já existe |
| Toda analogia com a linha "Onde a analogia falha" | Seção 7, item 6 | Sim, Regra 5 | Já existe |
| Pouca negação: dizer o que é, não o que não é | Seção 8 | Não | Candidata a método, vem da Lei 15.263 |
| A ideia principal antes das exceções; várias ramificações "se X, então Y" viram tabela | Seção 8 | Em parte, Regra 11 fala de if/then em procedimentos | Conferir se cobre o caso geral |
| Cortar metaconceitos vazios ("nível", "abordagem") e avaliativos vazios ("crucial", "robusto") | Seção 8 | Não | Candidata a método, e a lint pega fácil |
| Explicar o que o artigo deixa implícito: ironia, sarcasmo, tom | Seção 8 | Não | Candidata a método para o modo reescrever |

A regra para decidir é a que o Projeto já usa na seção 14.
O que é método vai para a skill: serve a qualquer leitor cansado, em qualquer texto.
O que é produto fica no Projeto: a Biblioteca, a revisão espaçada, os selos de checagem.

Ponto-chave: pelo menos sete regras do Projeto são método e não estão no SKILL.md; cada uma precisa de veredito.

## 6. Por que a Fase A não pegou isso

O inventário da Fase A partiu das regras da skill e perguntou "esta regra tem prova?".
Ele não partiu das regras do Projeto e perguntou "esta regra está na skill?".
São duas direções, e só a primeira foi percorrida.

A assunção 2 do guia dizia isso de forma explícita: "o inventário cobre as regras do SKILL.md, não as das instruções do Projeto".
A assunção estava errada para o objetivo do Dennis, que é levar para a skill o que o Projeto aprendeu.
Este adendo corrige a direção.

Ponto-chave: faltou a leitura no sentido Projeto para skill, e a seção 5 deste adendo é essa leitura.
