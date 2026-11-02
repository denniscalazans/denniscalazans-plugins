<!-- SET_VERSION: 2026-10-14-r1 -->
# O cache do navegador deixa o site rápido, mas pode mostrar uma versão velha

## Em 30 segundos
O navegador guarda uma cópia dos arquivos de um site (cache), para não baixar tudo de novo.
Isso deixa o site rápido.
No entanto, depois de um deploy, o navegador pode continuar mostrando a cópia velha.
O guia explica por que isso acontece e como evitar.

## Termos-chave
- **Cópia guardada pelo navegador (cache):** os arquivos que o navegador salva no computador do usuário.
- **Prazo de validade da cópia (`Cache-Control: max-age`):** por quantos segundos o navegador pode usar a cópia sem perguntar ao servidor.
- **Etiqueta de versão do arquivo (ETag):** um código que o servidor envia junto com o arquivo e que muda quando o arquivo muda.

## Conceito 1 de 3: o navegador decide pela validade, não pelo conteúdo
A ideia central aqui é que o navegador usa a cópia enquanto ela está dentro do prazo de validade.
O servidor define esse prazo com `Cache-Control: max-age`.
Exemplo: `max-age=31536000` vale por 1 ano (31.536.000 segundos).
Dentro do prazo, o navegador nem pergunta ao servidor.
Por isso, um arquivo novo no servidor não chega ao usuário.
Ponto-chave: dentro do prazo, o servidor não tem como avisar que o arquivo mudou.

## Conceito 2 de 3: quando o prazo acaba, o navegador confere a etiqueta
A ideia central aqui é que a etiqueta de versão (ETag) evita baixar de novo um arquivo que não mudou.
Quando o prazo acaba, o navegador envia a etiqueta que ele tem (`If-None-Match`).
| Situação | Resposta do servidor |
|---|---|
| A etiqueta é a mesma | `304 Not Modified`, sem o arquivo. O navegador reusa a cópia |
| A etiqueta mudou | `200 OK`, com o arquivo novo |

**Mito corrigido:** muita gente acha que `no-cache` significa "não guardar". Isso não confere. `no-cache` significa "guarde, mas confira a etiqueta antes de cada uso". Quem proíbe guardar é `no-store`. Fonte: MDN, Cache-Control.
Ponto-chave: `no-cache` confere sempre, e `no-store` nunca guarda.

## Conceito 3 de 3: a solução é mudar o nome do arquivo a cada versão
A ideia central aqui é dar prazos diferentes para dois tipos de arquivo.
1. Arquivos de JavaScript e CSS recebem um código no nome, por exemplo `app.3f9a1c.js`. O build gera esse código a partir do conteúdo. Eles recebem prazo de 1 ano.
2. O HTML recebe `no-cache`, então o navegador sempre confere se ele mudou.
Depois de um deploy, o HTML novo aponta para um nome de arquivo novo.
Como o nome é novo, o navegador não tem cópia e baixa a versão nova.
Ponto-chave: nome novo a cada versão, prazo longo para os arquivos, e conferência sempre para o HTML.

## Agora tudo se encaixa
O prazo de validade deixa o site rápido, mas esconde arquivos novos.
A etiqueta de versão resolve isso só depois que o prazo acaba.
O nome com código resolve na hora, porque um nome novo nunca tem cópia velha.
