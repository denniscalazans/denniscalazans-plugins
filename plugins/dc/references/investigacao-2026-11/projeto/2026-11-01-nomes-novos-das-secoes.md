# Os nomes novos das seções do guia, linha por linha

CRIADO: 2026-11-01 (Berlim), no Claude Code.
PARA: o Dennis colar nas instruções do Projeto "Clear Read the Web" e no modelo de guia.
ORIGEM: a decisão do Dennis em 1 de novembro (`decisoes-do-dennis.md`, pergunta 1).

## 0. O que este arquivo é

O Dennis escolheu dois nomes novos para as seções do guia.
"O chão" vira "O que saber antes de ler".
"Para este guia ficar" vira "Exercícios de fixação".

As instruções do Projeto (`clear-read-web-project-instructions.md`, cópia de 14 de outubro) usam os nomes antigos em 9 linhas.
Este arquivo dá a linha nova para cada uma, pronta para colar.
As linhas ficam em inglês porque as instruções estão em inglês; só os nomes das seções ficam em português, como hoje.

Ponto-chave: 9 linhas para colar, mais o modelo de guia e o lint do Projeto, que o Dennis ajusta na Biblioteca.

## 1. Os títulos completos

| Hoje | Novo | Onde aparece no guia |
|---|---|---|
| O chão: o que precisa estar firme antes de ler | O que saber antes de ler: os conceitos que o artigo não explica | Título da seção de mini-lições, `id="chao"` |
| Para este guia ficar | Exercícios de fixação: as perguntas deste guia voltam em dias | Bloco antes das fontes |

O `id` das seções não muda (`chao` continua), porque os links antigos da Biblioteca apontam para ele.

## 2. As linhas novas, por número de linha

A coluna "Linha" é o número na cópia de 14 de outubro, em `projeto/clear-read-web-project-instructions.md`.

**Linha 177 (Phase 3: the stop rule).**

```text
- **O que saber antes de ler (what to know before reading).** List every concept the article uses without explaining. For each one, go down one floor at a time and stop at the first floor that holds: (1) an earlier guide already taught it, so it becomes one line with a link; (2) any adult can give an example of it without help; (3) no sentence of the guide depends on it; (4) it does not change the answer to the guide's central question, so it goes to "Aprofundar". What is left becomes a mini-lesson (section 7, item 4). Order by dependency, base first. Three to seven mini-lessons per guide.
```

**Linha 331 (section 7, item 4).**

```text
4. **O que saber antes de ler: os conceitos que o artigo não explica.** It replaces "O chão" since 1 de novembro de 2026, and "Termos-chave" before that. Three to seven mini-lessons, chosen with the stop rule of Phase 3, in dependency order. Each mini-lesson has five parts: what it is, in one sentence; an example from daily life; what it is confused with, and the difference in one sentence; where the article uses it; and a check question with its answer in a collapsed `<details>`. Each has a source link and a "Já sei" button: the button opens the check question, and only "Confirmei, pode fechar" collapses the block. A term that an earlier guide already taught becomes one line with a link to that guide's "O que saber antes de ler". Terms that fail the stop rule but still deserve a definition go into a collapsed `<details>` at the end of the section.
```

**Linha 350 (section 7, item 15b).**

```text
15b. **Exercícios de fixação: as perguntas deste guia voltam em dias.** One block before the sources: the questions of this guide are waiting in the Biblioteca; a link to the Biblioteca's "Revisar" tab (HUB_URL plus `#review`) and the chat sentence that activates them. It never activates anything by itself.
```

**Linha 407 (the guide model).**

```text
- The guide model. Start every new guide from `dev/guide-template/template.html` in the Biblioteca artifact (read it with the Artifact tool, `action: "read"`, `path: "dev/guide-template/template.html"`; its README is next to it). The model carries: every section with an `id` (`s30`, `chao`, `antes`, `c1`, `c2`, and so on), the "O que saber antes de ler" blocks with "Já sei", the local memory of the reading position (a "Continuar de lá" banner on return), the figure with "Como ler" and conclusion, the icon array for risk, the HTML timeline, and the "Exercícios de fixação" block. The memory lives only in his browser (`localStorage`, every call in try/catch). Never add `capabilities` to a guide: it would lose its public link.
```

**Linha 603 (checklist, item 22).**

```text
22. "O que saber antes de ler" has 3 to 7 mini-lessons with the five parts and a source each, in dependency order, and no term that fails the stop rule.
```

**Linha 604 (checklist, item 23).**

```text
23. Every section has an `id`, and "Exercícios de fixação" is present before the sources.
```

**Linha 676 (what the set already has).**

```text
- The guide model (`dev/guide-template/`) with "O que saber antes de ler", local memory, section ids and the "Exercícios de fixação" block. The suplementos guide was rebuilt on it as a pilot (version 2, a new link; the Biblioteca points to it, and version 1 still exists).
```

**Linha 690 (what stays only in this project).**

```text
- What stays only in this project, because it is the product and not the method: the Biblioteca and the spaced review, "O que saber antes de ler", "Contexto de fundo", the fact-check badges, the audio playbook, and `dev/tools/lint_guide.py` (the page-specific lint, item 19).
```

**Linha 697 (open items, 5).**

```text
5. **Read the suplementos guide, version 2**, and say whether "O que saber antes de ler" helped or got in the way. That answer decides whether every old guide is rebuilt on the model.
```

## 3. O que mais muda, fora das instruções

- O modelo de guia, `dev/guide-template/template.html` e seu README, na Biblioteca: os dois títulos visíveis.
- O guia de suplementos, versão 2, que já usa o modelo: os dois títulos visíveis.
- O lint do Projeto, `dev/tools/lint_guide.py`: só se ele procurar o texto dos títulos. A cópia de 14 de outubro não procura.
- A regra de SET_VERSION: as instruções ganham uma versão nova, e os 8 docs de contexto acompanham.

Ponto-chave: dois títulos, nove linhas, e o `id` das seções fica.
