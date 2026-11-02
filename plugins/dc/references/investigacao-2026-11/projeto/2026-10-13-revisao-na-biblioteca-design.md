# Spec da Onda 1A: revisão espaçada na Biblioteca

STATUS: implementada e publicada em 13 de outubro de 2026 · versão 3, com o que mudou na implementação (seção 18)
SET_VERSION: 2026-10-14-r1

O Dennis pediu implementação autônoma.
Então as decisões 1 a 4 da seção 16 seguem o padrão proposto, e ele pode mudar qualquer uma depois.
A decisão 5 (lembrete) continua esperando o sim dele, porque ela muda uma preferência que ele gravou.

## 1. O que isto resolve

Hoje nenhum guia guarda o que o Dennis respondeu, e nada volta para ser lembrado depois.
Então o projeto mede exposição, e não aprendizado.

Esta spec cria uma fila de revisão dentro da Biblioteca.
Cada guia gera poucas perguntas.
A Biblioteca traz cada pergunta de volta em intervalos crescentes e guarda o resultado.

O que a evidência sustenta, conferido na fonte:

- recuperar de forma espaçada vence recuperar tudo de uma vez (g = 0,74);
- agenda crescente e agenda uniforme dão o mesmo resultado, então caixas simples bastam;
- adultos com TDAH usam menos o autoteste por conta própria, e o autoteste funciona igual para eles;
- na tela, leitores com TDAH confiam demais na própria compreensão.

O que a evidência não sustenta: que um aviso no celular faça alguém abrir a revisão.
Nos estudos, um pesquisador aplicou o teste.
Por isso o lembrete desta spec é uma aposta, e o critério de adesão da seção 2 mede se ela funcionou.

## 2. O que é sucesso

1. **Adesão.** Nos 14 dias depois de ativar o primeiro guia, há sessão em pelo menos 10 dias. Com menos que isso, o lembrete e o tamanho da sessão são repensados.
2. **Aprendizado.** No dia 30, a lembrança das perguntas revisadas é comparada com a pergunta de controle de cada guia, que nunca foi revisada.
3. **Calibração.** O painel mostra quantas vezes ele teve certeza e não lembrou.
4. **Tamanho.** Uma sessão tem no máximo 6 perguntas e cabe em cerca de 5 minutos.
5. **Sem regressão.** As abas que existem mostram os mesmos dados, com as leituras corrigidas da seção 10.

Limite honesto do critério 2: com poucos guias, a comparação é um sinal fraco.
A pergunta de controle trata de uma ideia secundária, então ela pode ser mais fácil ou mais difícil que as outras.

## 3. Fora desta spec

- Mudanças na página do guia ("O chão", guia que lembra a posição). Isso é a Onda 1B, com spec própria.
- Coleção `events`, painel completo de retenção e testes de comparação entre formatos.
- Perguntas sobre termos do glossário. Elas nascem com "O chão", na Onda 1B.
- Agendador sofisticado, resposta digitada e correção por IA.
- Reescrever as abas que já existem.

## 4. Decisão de arquitetura

A plataforma impõe um limite: uma página que declara o banco `db` não pode ter link público.
Os guias precisam continuar compartilháveis.
O playbook registra isso em duas regras: pb-008 (outra pessoa precisa abrir o guia) e pb-014 (página pública).

| Opção | Como funciona | Problema |
|---|---|---|
| A. Revisão na Biblioteca | As perguntas moram no banco da Biblioteca. O Dennis responde lá | Ele precisa abrir a Biblioteca |
| B. Cada guia com seu banco | O guia grava as respostas e o Claude sincroniza depois | O guia perde o link público, e os dados ficam espalhados |
| C. Guias como páginas dentro da Biblioteca | Um artifact só, um banco só | Os links atuais mudam, e não há garantia de que subpáginas alcancem o banco |

**Escolha: opção A.**
Ela mantém um único lugar de registro, não quebra nenhum link e usa só recursos que a Biblioteca já usa em produção.

## 5. Quem decide o que entra na fila

Publicar um guia não é ler o guia.
Então as perguntas nascem em espera e só entram na fila quando o Dennis ativa o guia.

- O Claude escreve as perguntas quando publica o guia, com `status: "waiting"`.
- A aba "Revisar" mostra os guias em espera, cada um com dois botões: "Li e quero lembrar" e "Não quero".
- "Li e quero lembrar" ativa as perguntas daquele guia. Elas vencem no dia seguinte.
- "Não quero" tira o guia da lista de espera, sem apagar nada.
- A mesma ativação pode ser pedida no chat, logo depois da leitura.

Isso evita a enchente: nada entra na fila sem um toque dele.
Os guias antigos seguem a mesma regra, um de cada vez.

## 6. Modelo de dados

Nova coleção `reviews` no banco da Biblioteca.
Um documento por pergunta, com o histórico dentro dele.

```
reviews/{guia}--{n}
  guide        slug do guia em `articles`
  guide_title  título do guia
  guide_url    link do guia
  anchor       âncora da seção no guia, opcional
  concept      nome curto do conceito
  kind         "explicar" | "comparar" | "controle"
  prompt       a pergunta, que se entende sozinha
  cue          uma pista curta, opcional
  points       2 ou 3 pontos que uma boa resposta contém, até 15 palavras cada
  terms        slugs do glossário ligados à pergunta, opcional
  status       "waiting" | "active" | "suspended" | "done"
  box          1 a 5
  due          "AAAA-MM-DD", ou null enquanto espera
  created      "AAAA-MM-DD"
  activated    "AAAA-MM-DD", ou null
  last         data da última resposta, ou null
  history      mapa: a chave é o instante da resposta, o valor é {r, c, cue, n}
```

Os campos de cada entrada de `history`:

- `r` é o resultado: 2, 1 ou 0;
- `c` é a confiança, de 1 a 3;
- `cue` diz se a pista foi usada;
- `n` é quantos pontos ele marcou;
- `d` é a data local da resposta, no formato AAAA-MM-DD.

A chave de cada entrada é a letra "t" seguida do instante em milissegundos, por exemplo `t1791877512123`.
Ela só tem letras e números, para nunca ser lida como um caminho.

Quem grava o quê:

- **O Claude** cria o documento e pode corrigir o texto da pergunta. Ele nunca recria um documento que existe e nunca reusa um número.
- **A página** grava `status`, `box`, `due`, `activated`, `last` e `history`.

A regra de acesso do banco não muda: todos leem, só quem edita grava.
O Dennis é o dono, então ele grava pela página.

## 7. Regras da fila

**Caixas e intervalos.** Caixa 1: 1 dia. Caixa 2: 3 dias. Caixa 3: 7 dias. Caixa 4: 21 dias. Caixa 5: 60 dias.

**Resultado.** O Dennis marca quais pontos da resposta ele produziu de cabeça.

| O que ele marcou | Resultado | Caixa | Próxima data |
|---|---|---|---|
| Todos os pontos, sem pista | Lembrei | sobe uma, até a 5 | hoje mais o intervalo da nova caixa |
| Parte dos pontos, ou todos com pista | Em parte | desce uma, até a 1 | hoje mais o intervalo da nova caixa |
| Nenhum ponto | Não lembrei | volta para a 1 | amanhã |

**Sessão do dia.** Entram as perguntas ativas com `due` até hoje.
A ordem é: caixa mais baixa primeiro, depois a mais atrasada, alternando os guias.
O teto é de 6 perguntas. O que sobrar fica para o dia seguinte, e a página diz quantas ficaram.

**Pergunta de controle.** Cada guia tem uma, sobre uma ideia secundária.
Ela vence 30 dias depois da ativação, é feita uma vez e não volta.
Ela não entra nos números do painel.

**Datas.** "Hoje" é a data local do aparelho, lida no começo da sessão e quando a aba volta a ficar visível.
As datas são texto no formato AAAA-MM-DD e só são comparadas como texto.
Somar dias usa o calendário, e não milissegundos, para não errar na troca de horário de verão.

## 8. O que o Dennis vê

Uma aba nova, "Revisar", que vira a primeira aba.
Ela abre sozinha uma vez, quando existe pergunta vencida e ele não escolheu outra aba.

Fluxo de uma pergunta:

1. Aparecem o título do guia e a pergunta.
2. O botão "Pista" é opcional.
3. O Dennis responde de cabeça e toca na confiança: "Chute", "Acho que sei" ou "Tenho certeza".
4. O toque na confiança revela os pontos da resposta e o link "Rever no guia".
5. Ele marca os pontos que produziu e toca em "Pronto".
6. A página grava e mostra a próxima pergunta.

A confiança vem antes da resposta de propósito.
Ela registra a sensação de saber antes de ele ver se sabia.

Marcar ponto por ponto substitui o julgamento global "lembrei ou não".
O motivo: este leitor tende a se dar nota alta na tela.

No fim da sessão aparece um resumo: quantas lembrou, quantas ficaram para amanhã e quando é a próxima revisão.

Acima da fila ficam 3 números:

- perguntas vencidas hoje;
- taxa de "Lembrei" nos últimos 30 dias;
- quantas vezes ele marcou "Tenho certeza" e o resultado foi "Não lembrei".

Com menos de 5 respostas, os dois últimos números mostram um traço.

Estados vazios:

- sem nenhuma pergunta: "Nenhuma pergunta ainda. Elas nascem com cada guia novo.";
- só guias em espera: a lista de espera, com os dois botões;
- nada vencido: "Nada vence hoje. A próxima revisão é em" e a data.

## 9. De onde vêm as perguntas

O Claude escreve as perguntas quando publica um guia, na fase de registro.

- Uma por conceito principal, do tipo "explicar" (por quê ou como). Isso dá de 3 a 5.
- Uma do tipo "comparar", só quando dois conceitos do guia se confundem.
- Uma de controle, sobre uma ideia secundária.
- Nenhuma de múltipla escolha, porque reconhecer é mais fácil que lembrar.
- Cada pergunta cita o tema do guia, para ser entendida sem contexto.
- Os pontos da resposta usam as mesmas palavras do guia.

Carga inicial: o Claude escreve as perguntas de 3 guias que já existem (DuckDB, ElevenLabs e suplementos).
Elas ficam em espera até o Dennis ativar cada guia.

## 10. A página passa a ler os nomes que o banco tem

A página da Biblioteca lê nomes de campo diferentes dos que estão gravados.
Como este trabalho já edita o arquivo, ele torna essas leituras tolerantes.
Nenhum dado do banco é alterado.

| Aba | Problema medido | Conserto |
|---|---|---|
| Glossário | 49 de 65 termos gravam `pt` e `original`. A página lê `term_pt` e `term_original`, então 49 cartões ficam sem título e fora de ordem | Ler os dois nomes, também na ordenação. Ler `say` e `say_aloud` |
| Fatos | Há 12 grafias de veredito, 4 delas com símbolo na frente. 38 de 44 fatos confirmados aparecem em amarelo | Tirar o que não é letra do começo e classificar pelo início da palavra, sem diferenciar maiúscula |
| Fatos | Duas fontes são texto comum e viram link quebrado | Só criar link quando o valor começa com http |
| Log | Em 4 das 5 execuções lidas, o checklist é um objeto e aparece como "[object Object]" | Listar os itens do objeto |
| Log | 3 de 14 feedbacks gravam `what` e a página lê `said` | Ler os dois nomes |
| Biblioteca | Um guia grava `processed_date` e a página lê `processed` | Ler os dois nomes |
| Áudios | 1 de 11 áudios grava `flow` no lugar de `link` | Ler os dois nomes |
| Playbook | 6 regras gravam `tags` como lista e a página lê `tag` | Ler os dois nomes |

A página também ganha um estado de carregamento.
Hoje o aviso "sem banco" é apagado pelo redesenho seguinte, e os estados vazios piscam enquanto os dados chegam.

## 11. Erros e ausências

- **Sem banco nesta visualização:** a aba mostra o aviso e ele não some.
- **Gravação.** A página monta o conteúdo completo da gravação no momento do toque e guarda esse conteúdo. Uma nova tentativa reenvia o mesmo conteúdo, então tentar duas vezes não promove a pergunta duas vezes.
- **Botões.** Ficam desligados enquanto a gravação está pendente.
- **Falha.** A pergunta fica na tela com o código e a mensagem do erro. "Tentar de novo" só aparece quando o erro é passageiro. Nos outros casos aparece "Pular".
- **Dois aparelhos.** Uma pergunta que já foi respondida hoje em outro aparelho é pulada.
- **Atualização no meio da sessão.** A tela é desenhada a partir do estado da sessão, guardado em memória. Uma atualização do banco não apaga a resposta revelada, a confiança escolhida nem o aviso de erro.
- **Começo da sessão.** A fila só é montada quando o banco entrega os dados definitivos, e não a primeira leva parcial.
- **Dado inválido.** Pergunta com campo faltando ou data fora do formato é pulada, e a página mostra quantas foram puladas.

## 12. Lembrete

A fila precisa de um aviso, porque este leitor não se testa sozinho.

Proposta: uma tarefa agendada diária lê o banco.
Quando existe pergunta vencida, ela avisa no celular com a quantidade e com o texto da primeira pergunta.
Assim a lembrança começa mesmo que ele não abra a página.
Em dia sem pergunta, ela não avisa nada.

A preferência `review_reminders` da Biblioteca hoje está desligada.
Ela passa a guardar a escolha desta spec: ligado ou desligado, e a hora.

Se a tarefa agendada não conseguir ler o banco sem pedir aprovação a cada dia, não há plano B automático.
Nesse caso o Claude avisa o Dennis, e a decisão volta para ele.

A opção "Agendar revisão" do fim de cada guia, que criava eventos no Calendar, sai das instruções.
No lugar dela entra "Quero lembrar deste guia", que ativa as perguntas.

## 13. Como será testado

- **Regras da fila:** testes de unidade para a agenda, a montagem da sessão, a pergunta de controle, as datas e os 3 números. Os testes de data rodam em fusos diferentes, na virada do dia e na troca de horário de verão.
- **Página:** testes no Chromium a 390px, tema claro e escuro, com um banco falso.
- **Banco falso fiel:** ele imita o que o banco real faz e um banco ingênuo esconderia. Ele entrega documentos congelados e manda uma primeira leva parcial. Ele recusa atualizar documento que não existe e dispara atualização depois de cada gravação. Ele também permite simular demora e falha.
- **Abas antigas:** os dados reais de amostra devem produzir os mesmos cartões, mais os consertos da seção 10.
- **Publicação:** depois de publicar, o Claude lê a coleção `reviews` no banco real e confere a carga inicial.
- **Volta atrás:** a republicação do arquivo guardado é testada antes da publicação da versão nova.

Limite conhecido: o Claude não consegue tocar nos botões da página real como o Dennis.
A gravação real só é provada na primeira sessão dele.
Por isso a página mostra o código do erro quando uma gravação falha.

## 14. Segurança da mudança

- A página antiga fica guardada junto da página nova, em `dev/backup/biblioteca-2026-10-13.html.txt`.
- A publicação usa o mesmo link e mantém as permissões que a página já tem.
- A coleção nova não toca nas coleções que existem.
- Voltar atrás é publicar o arquivo guardado. Isso foi testado antes da publicação da versão nova.

## 15. Entregas

1. Página da Biblioteca com a aba "Revisar" e as leituras corrigidas.
2. Coleção `reviews` com as perguntas de 3 guias, em espera.
3. Lembrete diário, se o Dennis aprovar.
4. Fonte, testes e instruções de manutenção guardados junto da página, na pasta `dev/` do artifact. Eles não ficam nos docs do projeto, para não gastar contexto em toda conversa.
5. Instruções do projeto atualizadas, em arquivo completo. Elas ganham a coleção `reviews` e a regra de escrever as perguntas. "Agendar revisão" vira "Quero lembrar deste guia", e o `HUB_URL` é preenchido.

## 16. Decisões que são do Dennis

| # | Decisão | Padrão proposto |
|---|---|---|
| 1 | Onde a revisão acontece | Na Biblioteca |
| 2 | O que entra na fila | Só o guia que ele ativar com "Li e quero lembrar" |
| 3 | Teto por sessão | 6 perguntas |
| 4 | Pergunta de controle no dia 30 | Sim, uma por guia |
| 5 | Lembrete | Tarefa agendada, só quando há pergunta, às 8h45 de Berlim |

## 17. O que a revisão independente mudou

Dois revisores leram a versão 1 sem o raciocínio do autor.

| Problema apontado | Mudança |
|---|---|
| A fila encheria no primeiro dia, e publicar não é ler | Perguntas nascem em espera. Só entram com "Li e quero lembrar" |
| Ele poderia pular a recordação e se dar nota alta | Marcar ponto por ponto no lugar do "lembrei ou não". Pista limita o resultado a "Em parte" |
| 10 perguntas em 3 minutos não cabe | Teto de 6, cerca de 5 minutos, sem botão de "mais" |
| Os critérios de sucesso passariam mesmo sem aprendizado | Critério de adesão e pergunta de controle no dia 30 |
| A spec dizia que o lembrete tem base em estudo | Corrigido: o lembrete é uma aposta medida |
| "Em parte" na caixa 4 voltaria a 60 dias com um acerto | "Em parte" desce uma caixa |
| Tentar gravar de novo promoveria a pergunta duas vezes | Conteúdo da gravação fixado no toque. Histórico vira mapa por instante |
| A tela perderia a resposta revelada a cada atualização | Tela desenhada a partir do estado da sessão |
| O Claude poderia apagar o progresso ao regravar perguntas | Regra de quem grava o quê |
| Datas erradas em viagem e na troca de horário | Regra de datas da seção 7 |
| Havia mais 5 leituras erradas além das 3 achadas | Tabela da seção 10 |
| Plano B no Calendar contrariava a preferência dele | Removido |

Recusado: nada. Uma ressalva foi mantida: a pergunta de controle é sobre ideia secundária, para não deixar um conceito principal sem revisão.

## 18. O que mudou na implementação

A implementação seguiu esta spec, com as diferenças desta tabela.
Cada linha foi decidida pelo Claude durante o trabalho, e o Dennis pode reverter qualquer uma.

| Assunto | O que a página faz | Motivo |
|---|---|---|
| Abertura da aba | A aba "Revisar" abre sozinha quando há pergunta vencida ou guia em espera | Sem isso, as perguntas novas ficam escondidas |
| Começo da sessão | A primeira pergunta já aparece, sem botão "Começar" | Um toque a menos |
| Teto de 6 | O teto vale para o dia inteiro, e não para cada abertura da página | Recarregar a página furava o teto |
| Números do painel | "Certeza sem lembrar" também conta só os últimos 30 dias | Um número de sempre só cresce e para de informar |
| Números do painel | Os 3 números ficam escondidos antes da primeira ativação | Zero e dois traços não informam nada |
| Guia ativado | A linha do guia fica no mesmo lugar, com "Desfazer" | Um segundo toque caía no botão do guia seguinte |
| Guia dispensado | "Não quero" tem "Desfazer". Depois, o guia aparece em "Guias tirados da lista", com "Voltar para a espera" | Um toque errado não deve exigir pedir ao Claude |
| Toque duplo | Por meio segundo depois da confiança, a página ignora toques nos pontos | Os pontos aparecem onde estavam os botões |
| Dois aparelhos | Pergunta aberta e já respondida em outro aparelho sai da tela. Se a resposta já estava aberta, "Pronto" não grava | Evita dois registros no mesmo dia |
| Dia que vira | A data da resposta é lida no toque. A fila é refeita na pergunta seguinte, na volta à aba e no toque em qualquer aba | A fila do dia novo não aparecia |
| Gravação sem resposta | Depois de 15 segundos sem resposta do banco, aparece um erro com "Tentar de novo" | A tela ficava presa em "Gravando" |
| Erro | "Pular" aparece ao lado de "Tentar de novo" | Um erro que se repete prenderia a sessão |
| Fatos | Veredito desatualizado ou não verificável aparece em cinza. O campo de nota passa a aparecer | Amarelo diria "precisa de contexto", o que seria falso |
| Biblioteca e Áudios | Original sem link aparece como texto. O filtro de Áudios olha o artigo inteiro | A página antiga mostrava isso |

Números da verificação, em 13 de outubro de 2026:

- 26 testes de unidade, rodados em 4 fusos;
- 34 testes de página no Chromium a 390px, tema claro e escuro;
- 25 quebras de propósito no código, todas pegas por algum teste;
- 1 revisão independente do código: nenhum achado crítico, 6 importantes corrigidos, 4 menores adiados.

O que só o uso real prova:

- a gravação pela página real, com a conta do Dennis;
- se o link "Rever no guia" rola até a seção certa;
- se a data é relida quando o app do celular volta do segundo plano.
