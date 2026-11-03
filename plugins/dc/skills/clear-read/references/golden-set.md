# Golden set: cinco trechos que não mudam

Este arquivo pertence à clear-read (`references/tests.md`, Test 18).
São cinco trechos de guias escritos com a skill que mostram o que está certo.
Uma versão nova da skill precisa reproduzir o mesmo comportamento neles.

Cada trecho traz o guia de origem, a seção, o texto, as regras que ele mostra, e o que um leitor frio precisa acertar.
A clear-listen ainda não tem trecho dourado.

### G1: a abertura que entrega, e a analogia que paga o empréstimo

Guia: Burnout, estresse e férias, seção `s30` ("Em 30 segundos").

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

Guia: Burnout, estresse e férias, mesmo guia, seção `c2`, primeiro bloco.

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

Guia: Suplementos todo dia, versão 2, seção `chao`, item "Lesão no fígado causada por substância".

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
O formato de cinco partes é uma escolha de página, mas a ordem dentro da definição é a Regra 5.

Leitor frio acerta: "uma hepatite por vírus entra na conta das lesões por substância?" (não).

### G4: o problema com a solução ao lado

Guia: Do zero ao avançado, DuckDB, notebook e Hugging Face, Parte 2 (os formatos), bloco "Mito corrigido".

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

Guia: ElevenLabs e o Eleven v4, seção `c2`, figura das 150 ferramentas.

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
