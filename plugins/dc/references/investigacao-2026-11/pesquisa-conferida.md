# Pesquisa conferida: fala, narrativa, diálogo e as skills que já existem

VERIFICADO: 2026-11-01 (Berlim), no Claude Code.
FASE: C, do guia `guia-de-investigacao.md` (seção 7).
STATUS: entregue; a seção 9 traz a rodada de fechamento.

Legenda dos vereditos: ✅ confirmado na fonte · 🟡 precisa de contexto · ❌ incorreto · 🕒 desatualizado · ⚪ não verificável nesta rodada.

## Em 30 segundos

- **Dos 45 estudos citados, 18 conferem como estão e 24 conferem com um qualificador.** Três dizem o contrário do que o guia ou a skill afirmam.
- **Três regras da clear-listen perdem parte da prova.** A R13b (a segunda voz) perde "a frase importante logo depois da troca de voz". A R15 (fechar bem) perde "o resumo curto vence a reescuta". A R6 (recuperar na cabeça) perde a pergunta por parte como parte provada.
- **Cinco citações do guia estavam erradas** no DOI ou no periódico, e a seção 13 do guia já foi corrigida.
- **A contagem nua antes do conteúdo continua sem estudo**, a favor ou contra. As prévias que funcionaram entregavam o nome dos tópicos junto com a contagem.
- **A skill oficial da ElevenLabs cuida só da API.** Nenhuma skill de ASD-STE100 traz o dicionário em forma de lint, e o Brasil já tem a ABNT NBR ISO 24495-1:2024.

## 1. Como a conferência foi feita

Um workflow de 61 agentes rodou a Fase C em cerca de 1 hora e 45 minutos.
Um verificador por estudo abriu a página do DOI, leu o resumo e, quando conseguiu, o método e os resultados.
Para os 15 estudos que sustentam um veredito da seção 5.2 do guia, um cético tentou refutar cada "confirmado", e nenhum caiu.

Cinco buscadores cobriram as perguntas da seção 7.3.
Quatro leitores cobriram as skills e normas da seção 7.4.
Um crítico fechou a rodada com 12 lacunas, e a seção 9 registra a rodada que as cobre.

Onde o verificador conseguiu chegar:

| Acesso | Estudos |
|---|---|
| Texto completo | 27 |
| Só o resumo | 11 |
| Só o registro do PubMed | 5 |
| Preprint ou página secundária | 2 |

Um número lido só no resumo vale menos do que um número lido no método.
As tabelas marcam o acesso quando ele muda a confiança.

Ponto-chave: 45 estudos abertos, 15 passados por um cético, e nenhum "confirmado" caiu na refutação.

## 2. Os estudos, por tema

As colunas são quatro.
A afirmação como o guia ou a skill a fez, o veredito, e a fonte com a citação correta.
A quarta coluna diz o que a fonte diz de fato, com o limite.

### 2.1 Divagação e escuta

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| 211 adultos; ouvir deu a maior divagação (metade das sondagens) e a pior memória; ler em voz alta deu a menor | ✅ | Varao Sousa, Carriere e Smilek 2013, Frontiers in Psychology 4:892, [doi:10.3389/fpsyg.2013.00892](https://doi.org/10.3389/fpsyg.2013.00892) | 235 estudantes menos 24 excluídos = 211; ouvir M = 0,506 de divagação contra 0,356 lendo em silêncio; pior memória ao ouvir (p < 0,001). Limite: universitários sem TDAH, áudio puro sem texto na tela, memória imediata |
| 175 adultos; ruído de fundo aumenta a divagação; a compreensão caiu na leitura e na escuta | ✅ | Steindorf, Pink, Rummel e Smallwood 2023, Cognitive Research 8, [doi:10.1186/s41235-023-00483-0](https://doi.org/10.1186/s41235-023-00483-0) | N = 175, desenho 2 por 2; o "ruído" era ruído gaussiano sobre o próprio sinal (texto granulado, chiado sobre a voz), não música nem fala de fundo. A R11 ganha prova para "ruído sob a voz" e não para "sem música" |
| 80 adultos; aula de 21 minutos; teste a cada 5 minutos derrubou a divagação de 40% para 19% e subiu a nota; reestudar não ajudou | ✅ (cético: mantido) | Szpunar, Khan e Schacter 2013, PNAS 110(16), [doi:10.1073/pnas.1221764110](https://doi.org/10.1073/pnas.1221764110) | 19% contra 39% e 41% (p = 0,041); nota do último segmento 89% contra 65% e 70%. Limite: graduandos de Harvard, vídeo com slides, teste escrito de seis perguntas respondidas, não uma pergunta falada com pausa |
| 27 adultos com TDAH e 29 sem; a divagação caiu com mais memória de trabalho, não com só atenção sustentada | ✅ | Bozhilova e colegas 2020, Journal of Attention Disorders 25(14), [doi:10.1177/1087054720956714](https://doi.org/10.1177/1087054720956714) | TDAH: 66% de divagação no 0-back e 45% no 1-back (p = 0,001); na vigilância, 53% a 69%. Limite: tarefas visuais de laboratório; a ponte para a pergunta por parte é inferência |
| A divagação em TDAH é espontânea, não deliberada | ✅ | Seli e colegas 2015, Psychonomic Bulletin and Review 22(3), [doi:10.3758/s13423-014-0793-0](https://doi.org/10.3758/s13423-014-0793-0) | Duas amostras de 1.354 estudantes; r = 0,52 e 0,47 para a espontânea contra 0,23 e 0,25 para a deliberada. Limite: autorrelato de traço, sem tarefa de leitura ou escuta; "não se regula sozinha" é interpretação |
| Meta-análise: sem diferença entre ler e ouvir (g = 0,07); ler vence no ritmo próprio e em inferência | ✅ | Clinton-Lisell 2022, Review of Educational Research 92(4), [doi:10.3102/00346543211060871](https://doi.org/10.3102/00346543211060871) | 46 estudos, N = 4.687; g = 0,07 (p = 0,23); ritmo próprio g = 0,13 (p = 0,049, marginal); inferência g = 0,36. Limite: só o resumo; sem adultos com TDAH |
| Meta-análise da segmentação: 56 investigações, 88 comparações; ganhos pequenos a médios | ✅ | Rey e colegas 2019, Educational Psychology Review 31(2), [doi:10.1007/s10648-018-9456-4](https://doi.org/10.1007/s10648-018-9456-4) | Retenção d = 0,32; transferência d = 0,36; carga d = 0,23; segmentar custa tempo (d = -0,92). Limite: só 4 de 88 comparações em áudio puro; ganho maior quando o sistema define os cortes |

### 2.2 Sinalização e estrutura falada

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| Frases de prévia ("esta seção cobre três causas") melhoraram a compreensão da estrutura, em texto e em áudio sintético | 🟡 | Lorch, Chen e Lemarié 2012, JEP: Applied 18(3), 265 a 276, [doi:10.1037/a0029547](https://doi.org/10.1037/a0029547) | O DOI do guia apontava para outro artigo. A medida foi a qualidade do esboço (outline), não compreensão. Só o resumo foi lido; a seção 9 diz o que a prévia dizia |
| Um título dito em áudio só funcionou com pausa e entonação | 🟡 | Chen e Lorch 2018, JEP: Applied 24(2), 207 a 221, [doi:10.1037/xap0000143](https://doi.org/10.1037/xap0000143) | A tese de 2015 (206 e 200 universitários) mostra que o título lido pelo TTS já ajudou, e a renderização por troca de voz foi a mais útil. "Só funcionou" é mais forte do que a fonte |
| Tirar os marcadores ("so", "now", "OK") de uma aula derrubou a compreensão, em segunda língua | ✅ | Flowerdew e Tauroza 1995, Studies in Second Language Acquisition 17(4), [doi:10.1017/S0272263100014406](https://doi.org/10.1017/S0272263100014406) | 63 universitários de Hong Kong, vídeo de aula real. Limite: marcadores de organização, não conectivos causais; ouvintes de segunda língua |
| Conectivos na fala espontânea ajudam a entender relações causais | 🟡 | Cevasco 2009, The Spanish Journal of Psychology 12(1), 56 a 65, [PMID 19476219](https://pubmed.ncbi.nlm.nih.gov/19476219/) | O guia citava Memory and Cognition. Um só conectivo ("but"), 36 universitários, inglês; o ganho foi de velocidade (2.462 ms contra 2.779 ms), não de acerto |

### 2.3 Narrativa e dado antes do novo

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| Meta-análise com mais de 75 amostras e 33 mil participantes: narrativas são entendidas e lembradas melhor | ✅ | Mar, Li, Nguyen e Ta 2021, Psychonomic Bulletin and Review 28(3), [doi:10.3758/s13423-020-01853-1](https://doi.org/10.3758/s13423-020-01853-1) | 78 amostras, 33.078 participantes, g = 0,55; memória g maior do que compreensão (g = 0,48). Limite: compara gêneros inteiros; populações não clínicas |
| O expositivo integra melhor com o conhecimento prévio; é o limite da narrativa | 🟡 | Wolfe e Woodwyk 2010, British Journal of Educational Psychology 80(3), 341 a 362, [doi:10.1348/000709910X485700](https://doi.org/10.1348/000709910X485700) | Com 61 pessoas, o expositivo foi até recordado melhor; com 160, modelo de situação só marginalmente mais forte. A frase "menos a entender mecanismo" não é achado do estudo |
| 150 a 200 milissegundos a mais quando a parte dada não tem antecedente | 🟡 | Haviland e Clark 1974, Journal of Verbal Learning and Verbal Behavior 13(5), 512 a 521; o PDF de Clark 1975 não traz o número | 181 ms no experimento principal (835 contra 1.016 ms), 137 ms e 74 ms nos outros dois; 53 estudantes, pares de frases isoladas. O estudo mediu falta de antecedente, não a ordem dado-novo dentro da frase |
| O ganho de dado antes do novo depende da construção | ✅ (cético: mantido) | Clifton e Frazier 2004, Memory and Cognition 32(6), 886 a 895, [doi:10.3758/BF03196867](https://doi.org/10.3758/BF03196867) | Duplo objeto: 3.442 ms e 89,6% de aceitação contra 4.274 ms e 71,6%; na construção com preposição, sem vantagem. Limite: mediu a ordem de dois objetos depois do verbo, não o início da frase |
| Reversão da expertise: o apoio que ajuda o novato atrapalha o experiente (DOI não confirmado) | ✅ | Kalyuga, Ayres, Chandler e Sweller 2003, Educational Psychologist 38(1), 23 a 31, [doi:10.1207/S15326985EP3801_4](https://doi.org/10.1207/S15326985EP3801_4) | DOI confirmado em três registros. Limite: revisão narrativa com estudantes |
| Retomar depois de uma interrupção custa tempo, e o custo cresce com a duração e a demanda | ✅ (cético: mantido) | Monk, Trafton e Boehm-Davis 2008, JEP: Applied 14(4), 299 a 313, [doi:10.1037/a0014402](https://doi.org/10.1037/a0014402) | 12, 11 e 36 participantes; custo de 599 ms no experimento 1; a curva nivela entre 13 e 23 segundos. Limite: tarefa manual de laboratório, não leitura; apoio indireto ao zero retrocesso |

### 2.4 Diálogo e a segunda voz

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| 48 alunos ouviram um diálogo de tutoria; o ganho apareceu só com perguntas "por quê" e "como" | 🟡 | Craig, Gholson, Ventura e Graesser 2000, International Journal of AI in Education 11, [PDF](https://people.cs.pitt.edu/~litman/courses/slate/pdf/paper.pdf) | O estudo comparou diálogo rico em perguntas (66) contra monólogo (8), em agentes animados na tela; o ganho veio em recordação livre (46,2 contra 36,3 proposições). A comparação rasa contra profunda está em Driscoll 2003 |
| Só a pergunta profunda funciona; rasas e comentários não deram nada | 🟡 | Driscoll e colegas 2003, Journal of Educational Computing Research 29(4), [repositório](https://digitalcommons.memphis.edu/facpubs/8941) | Pergunta profunda d = 0,71 e 0,64; rasas e comentários não diferiram do monólogo, mas "não deram nada" é mais forte do que "sem ganho detectável". 48 e 96 alunos com pouco conhecimento de informática |
| Observar um diálogo de tutoria ensina | 🟡 | Chi e Roy 2006, Cognitive Science Society, [PDF](https://repositories.cdlib.org/content/qt5k61x8cw/qt5k61x8cw.pdf) | Resumo de uma página: observar em pares 59,5% contra estudar sozinho 41,1%; observar sozinho e passivo não se destacou. Só funciona com observador ativo |
| Mais de mil alunos; o formato que refuta a concepção errada ganhou de 0,5 a 1 desvio-padrão; os alunos não sentiram que aprenderam mais | ✅ (cético: mantido) | Muller e Sharma 2007, UniServe Science Proceedings, [artigo](https://openjournals.library.sydney.edu.au/IISME/article/view/6345) | Palavra por palavra. Limite: a refutação com um narrador só teve efeito igual ao diálogo, então a prova é para "dar voz ao erro", não para a segunda voz |
| A troca de voz dispara orientação e a memória melhora logo depois (R13b) | ❌ | Potter 2000, Media Psychology 2(2), 147 a 177, [doi:10.1207/S1532785XMEP0202_3](https://doi.org/10.1207/S1532785XMEP0202_3) | 62 ouvintes, nove mensagens de 2 minutos. A orientação cardíaca é robusta e não habitua, mas o reconhecimento logo depois da troca piora, e piora mais com mais trocas. A seção 9 traz o texto completo |
| Nove recursos estruturais de áudio; a resposta não se desgastou em seis trocas | 🟡 | Potter, Lang e Bolls 2008, Journal of Media Psychology 20(4), 168 a 177, [doi:10.1027/1864-1105.20.4.168](https://doi.org/10.1027/1864-1105.20.4.168) | Oito de nove recursos produziram orientação, e o reconhecimento do que vem logo depois melhorou, como categoria. Os dados "seis trocas, dois minutos, sem habituação" são de Potter 2000, não deste |
| Tom mais diferente entre as vozes fortalece a orientação; trocas cedo funcionam melhor | ❌ | Potter, Lynch e Kraus 2015, Communication Monographs 82(3), [doi:10.1080/03637751.2015.1019529](https://doi.org/10.1080/03637751.2015.1019529) | O artigo não estuda troca de voz nem tom: testa habituação a jingles, efeitos e silêncio em 40 minutos de rádio (57 e 72 universitários). A fonte das duas frases é Potter e colegas 2019, que a seção 9 abre |
| Estilo conversacional ("você") melhora a aprendizagem (citação não confirmada) | ✅ (cético: mantido) | Ginns, Martin e Marsh 2013, Educational Psychology Review 25(4), 445 a 472, [doi:10.1007/s10648-013-9228-0](https://doi.org/10.1007/s10648-013-9228-0) | Retenção d = 0,30; transferência d = 0,54; amigabilidade d = 0,46. Limite: lições curtas; o efeito some em sessões acima de 35 minutos |

### 2.5 Velocidade, voz e pausas

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| 231 adultos; queda significativa só em 2,5x; até 1,5x é seguro | ✅ | Murphy e colegas 2022, Applied Cognitive Psychology 36(1), [doi:10.1002/acp.3899](https://doi.org/10.1002/acp.3899) | 1x contra 2,5x p = 0,004, d = 0,24; nenhuma outra diferença. Limite: universitários da UCLA, aulas de 13 a 15 minutos com slides |
| Estudo de reassistir: um resumo de 2 a 4 minutos vence uma segunda escuta rápida (R15) | ❌ | A fonte é o mesmo Murphy 2022 | Não existe condição com resumo. A condição vencedora foi a segunda escuta completa em 2x logo antes da prova (d = 0,54). O estudo diz o inverso da regra |
| Inteligibilidade de fala comprimida em português brasileiro | 🟡 | Rabelo e Schochat 2007, Clinics 62(3), 261 a 272, [doi:10.1590/S1807-59322007000300010](https://doi.org/10.1590/S1807-59322007000300010) | O DOI do guia estava errado. 144 adultos repetindo palavras isoladas; nenhuma taxa em palavras por minuto, nenhuma compreensão |
| Em rádio em espanhol, reconhecimento melhor entre 170 e 190 palavras por minuto; abaixo de 170 a atenção caiu | 🟡 | Rodero 2016, Media Psychology 19(2), 224 a 242, [doi:10.1080/15213269.2014.1002942](https://doi.org/10.1080/15213269.2014.1002942) | 200 estudantes, ritmos de 150 a 230 em passos de 20. Só 150 foi testado abaixo de 170; mediu reconhecimento, não atenção |
| Entonação moderada dá a melhor credibilidade e atenção | 🟡 | Rodero, Larrea, Rodríguez-de-Dios e Lucas 2022, Journal of Language and Social Psychology 41(5), [doi:10.1177/0261927X221078317](https://doi.org/10.1177/0261927X221078317) | Moderada venceu em eficácia e credibilidade percebidas; em atenção (frequência cardíaca) a enfática ganhou ou empatou, e a monótona foi a pior. Vídeo de 24 segundos com atores |
| Voz sintética piora a recordação; a causa é a prosódia errada | 🟡 | Paris e colegas 2000, Human Factors 42(3), 421 a 431, [doi:10.1518/001872000779698132](https://doi.org/10.1518/001872000779698132) | Sintetizadores do ano 2000, frases isoladas; a causa prosódica é interpretação dos autores. Sustenta "trocar voz com prosódia ruim", não "pontuação como controle de som" |
| Vozes neurais modernas: sem diferença em aprendizagem | 🟡 | Dinçer 2022, Journal of Pedagogical Research 6(3), 17 a 26, [doi:10.33902/JPR.202214591](https://doi.org/10.33902/JPR.202214591) | 51 homens de engenharia, inglês intermediário, vídeo de 4 minutos; humana 60,6 contra moderna 54,1 (sem significância, n = 17 contra 18). "Estudos recentes" no plural é um estudo só |
| 29 brasileiros; voz sintética igual à humana | 🟡 | Bione e Cardoso 2020, Language Learning and Technology 24(1), 169 a 186, [artigo](https://www.lltjournal.org/item-detail/944/) | Igual em compreensão e ditado; menos natural e menos precisa em frases curtas. Ouviam inglês, não português |
| Pausas preenchidas ajudam a recordação do que vem depois | 🟡 | Fraundorf e Watson 2011, Journal of Memory and Language 65(2), 161 a 175, [doi:10.1016/j.jml.2011.03.004](https://doi.org/10.1016/j.jml.2011.03.004) | "Uh" e "um" aumentaram a recordação 1,57 vez, efeito global e não local; uma tosse da mesma duração piorou (0,64). Não é prova de pausa silenciosa em TTS |

### 2.6 Instrução falada e navegação

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| Instrução composta de dois passos aumentou os perigos não vistos de 1,5% para 5,5% | 🟡 | Dalton e colegas 2013, Accident Analysis and Prevention 50, 298 a 303, [manuscrito](https://pure.royalholloway.ac.uk/files/12497853/Dalton_et_al._AA_P_accepted.pdf) | 1,5% é sem instrução; a instrução simples deu 3,2% e a composta 5,5% (p = 0,055, marginal). A prova forte está no desvio de direção. 25 estudantes, ordem fixa |
| Guia por marco: 1,6 olhadas para a tela; por distância: 5 | ✅ | Burnett 1998, tese de Loughborough, [repositório](https://repository.lboro.ac.uk/articles/_Turn_right_at_the_King_s_Head_drivers_requirements_for_route_guidance_information/9355379) | 1,60 (n = 8) contra 5,04 (n = 12), p < 0,0001, em estrada real. Limite: dois ensaios separados comparados a posteriori; os exemplos "na rotatória" e "em 800 metros" não aparecem na tese |
| 61 motoristas; marcos contra distância | 🟡 | Antrobus, Large, Burnett e Hare 2019, Journal of Navigation 72(3), 513 a 527, [doi:10.1017/S037346331800108X](https://doi.org/10.1017/S037346331800108X) | O DOI do guia apontava para outro artigo. Quatro condições de apoio à navegação (satnav, passageiro, passageiro colaborativo, interface em linguagem natural); mede carga e memória espacial |

### 2.7 Adultos com TDAH e audição

| Afirmação | Veredito | Fonte | O que a fonte diz, e o limite |
|---|---|---|---|
| 69 adultos com TDAH contra 66; menos memória auditiva e mais distração com som | 🟡 | Dige, Maahr e Backenroth-Ohsako 2010, Journal of Attention Disorders 13(6), 677 a 683, [doi:10.1177/1087054709347245](https://doi.org/10.1177/1087054709347245) | Teste de memória dicótica com fala invertida como distrator para os dois grupos; prejuízo no grupo TDAH. Não compara voz limpa com voz sobre fundo |
| 17 contra 17 com ressonância; fala em ruído | 🟡 | Blomberg e colegas 2021, Frontiers in Human Neuroscience 15:771711, [doi:10.3389/fnhum.2021.771711](https://doi.org/10.3389/fnhum.2021.771711) | O distrator era tom puro durante um n-back visual, não fala em ruído; acurácia no 2-back 0,74 contra 0,89. A fala em ruído é Blomberg 2019, com adolescentes |
| Meta-análise de memória de trabalho em adultos com TDAH | 🟡 | Alderson e colegas 2013, Neuropsychology 27(3), [doi:10.1037/a0032371](https://doi.org/10.1037/a0032371) | O DOI do guia era um estudo com 37 adultos no Journal of Abnormal Psychology; a meta-análise de 38 estudos é outro artigo do mesmo ano |
| 36 com TDAH e 36 sem; recordar o texto inteiro venceu a por seção; nenhuma venceu reestudar em 2 dias | ✅ (cético: mantido) | Stern e Halamish 2023, Frontiers in Psychology 14:1301726, [doi:10.3389/fpsyg.2023.1301726](https://doi.org/10.3389/fpsyg.2023.1301726) | Texto inteiro 0,45 contra por seção 0,37 (d = 0,45); reestudar 0,42. A pergunta por parte da R6 é a condição que perdeu |
| 210 adultos, metade com TDAH; orientação por etapa igualou os grupos (2024) | 🟡 | Brann e Sidi 2025, Learning and Instruction 95:102051, [doi:10.1016/j.learninstruc.2024.102051](https://doi.org/10.1016/j.learninstruc.2024.102051) | O ano de citação é 2025 (online em novembro de 2024). 210 adultos de 20 a 50 anos, 50,05% com TDAH. O andaime eram instruções de autorregulação, então o apoio ao "Key point" é por analogia |
| Co-design com 9 jovens com TDAH; turnos curtos e lembrete externo | 🟡 | Bryant e colegas 2026, JMIR Formative Research, [doi:10.2196/85013](https://doi.org/10.2196/85013) | Grupo de 13 (9 jovens e 4 apoiadores); só 6 testaram o protótipo. "Turnos curtos" fica; "lembrete externo" é só sugestão para um app futuro |
| 11 universitários com TDAH; 73% queriam que o robô detectasse a distração | ✅ | O'Connell e colegas 2024, HRI, [doi:10.1145/3610977.3634929](https://doi.org/10.1145/3610977.3634929) | 8 de 11 (73%) sugeriram isso em entrevista; sintomas autorrelatados (ASRS), robô mudo. É desejo declarado, não função testada |

### 2.8 Fontes sem referência que o inventário mandou achar

| Afirmação | Veredito | O que a Fase C achou |
|---|---|---|
| Clear-read R9 (tom): "pesquisa de leitura em tela contra áudio" | 🟡 | Não existe pesquisa de modalidade que fale de tom. Rogowsky 2016 e Daniel e Woody 2010 comparam ler e ouvir sem medir tom. Ginns 2013 mostra que falar direto com o leitor ajuda em textos curtos, o que vai contra "sem personalidade". Sobra base para "sem enfeite irrelevante" (detalhes sedutores) |

Ponto-chave: a direção de quase tudo se mantém, mas 24 afirmações precisam de qualificador e três dizem o inverso da fonte.

## 3. O que caiu ou perdeu força

1. ❌ **"Ponha a frase importante logo depois da troca de voz" (clear-listen R13b, a segunda voz).** Potter 2000 mostra sobrecarga momentânea e pior reconhecimento logo após a troca, pior ainda com muitas trocas. A troca de voz orienta, mas custa, e a regra precisa ser reescrita.
2. ❌ **"Vozes de tom bem diferente" e "segunda voz cedo" vêm de Potter 2015.** Não vêm. Esse artigo é sobre jingles e silêncio. A fonte provável é Potter e colegas 2019, que a seção 9 abre.
3. ❌ **"Um resumo de 2 a 4 minutos vence uma segunda escuta rápida", da clear-listen R15 (fechar bem).** A fonte, Murphy 2022, nunca testou um resumo. A segunda escuta completa em 2x logo antes da prova foi a condição que venceu.
4. 🟡 **A pergunta de recordação por parte, da clear-listen R6 (recuperar na cabeça).** No único estudo com adultos com TDAH, recordar por seção perdeu para recordar o texto inteiro. Nenhuma das duas venceu reestudar em 2 dias. A pergunta de fechamento tem prova; a pergunta por parte vira hipótese para a Fase D.
5. 🟡 **"A regra com base direta mais forte", a clear-listen R11 (só voz).** Blomberg 2021 é sobre tons irrelevantes sob carga visual, não fala em ruído. A base em TDAH fica em Michalek 2014 (inteligibilidade, não compreensão) e Blomberg 2019 (adolescentes). A prova direta em população geral é Steindorf 2023.
6. 🟡 **"150 a 200 ms" de dado antes do novo.** O número é de Haviland e Clark 1974, não de Clark 1975: 181 ms no experimento principal, 74 ms no menor. E mede falta de antecedente, não a ordem dentro da frase.
7. 🟡 **"Narrativa ajuda menos a entender mecanismo" (limite do narrador).** Wolfe e Woodwyk 2010 não dizem isso. Eles mostram que o expositivo puxa mais o conhecimento prévio e, numa amostra, foi até recordado melhor.
8. 🟡 **"Dois estudos puseram alunos para ouvir um diálogo; o ganho veio só com perguntas profundas."** Craig 2000 não testou pergunta rasa contra profunda; essa comparação é de Driscoll 2003. E "não deram nada" é mais forte do que "sem ganho detectável".
9. 🟡 **"TTS igual a humano em duas vezes", da clear-listen R12 (voz por papel).** Dinçer 2022 tem 17 contra 18 pessoas em inglês intermediário, com a voz humana 6 pontos acima. Bione e Cardoso 2020 acham a voz sintética menos natural em frases. "Igual" é forte demais.
10. 🟡 **"Abaixo de 170 a atenção caiu" (Rodero 2016).** Só 150 foi testado abaixo de 170, e a medida foi reconhecimento, não atenção.
11. 🟡 **Entonação moderada e atenção (Rodero 2022).** Moderação venceu em credibilidade percebida; em atenção, a enfática ganhou ou empatou. A clear-listen R10 (expressão moderada) perde "moderada" como regra de atenção e mantém "variada".
12. 🟡 **Fraundorf e Watson 2011 como prova de pausas.** O estudo é sobre "uh" e "um" em fala humana, com efeito global; uma interrupção sem conteúdo piorou. Não sustenta pausa silenciosa em TTS.

## 4. As buscas novas da seção 7.3

### 4.1 A contagem antes do conteúdo (pergunta 1)

Nenhum estudo mede o custo de uma contagem nua ("são cinco pontos") antes do conteúdo, em escuta.
A preocupação do Dennis fica como não testada, não refutada.

O que existe aponta para "ajuda", com uma condição.
Nas prévias que funcionaram, a frase entregava os nomes dos tópicos ou "os três passos principais".
Ou seja, contagem junto com conteúdo (Lorch 2012; Lorch, Lemarié e Chen 2013; Mautone e Mayer 2001).

Em listas de palavras, saber o número de itens antes não piorou a recordação.
Em listas curtas, melhorou um pouco (Babu e colegas 2026, ηp² = 0,11).

Do lado do custo, qualquer item pendente na memória de trabalho deixa a escuta mais lenta, e mais em adultos com TDAH.
Lemel 2022 mediu 140 ms a mais com carga de 4 dígitos, em 24 adultos com TDAH.
Mas o item pendente nesses estudos era um dígito ou uma pergunta, não uma contagem.

A síntese para a Fase D: a contagem que vem com conteúdo tem prova a favor.
A contagem nua não tem prova nenhuma, e tem um mecanismo plausível contra.

### 4.2 A referência adiante e o rótulo sem referente (pergunta 7)

A literatura é consistente: um pronome ou rótulo sem referente não fica "em espera" de graça.
Cinco estudos de rastreamento ocular e leitura autocadenciada mostram dificuldade imediata e busca ativa pelo antecedente.
São Filik e Sanford 2008, van Gompel e Liversedge 2003, Kazanina 2007, Giskes e Kush 2021 e Kush e Dillon 2026.
Cada tentativa frustrada custa cerca de 80 ms (647 contra 728 ms em Giskes e Kush).

Estudos de potenciais cerebrais (Pablos 2015; van Berkum 2003) mostram uma negatividade frontal sustentada, lida como carga de memória.
Um referente novo sem ancoragem eleva o N400 e produz uma positividade tardia de atualização (Burkhardt 2006; Wang e Schumacher 2013; Nieuwland 2019).

Para "Mayer mostrou", o dado é indireto: nenhum estudo mede nome próprio antes do papel.
Mas o mecanismo da catáfora é o mesmo: um rótulo aberto custa até fechar.
Isso sustenta a extensão da R5a (significado antes do termo) para nomes próprios como "razoável", não como provado.

### 4.3 Organizadores prévios em fala, para TDAH (a busca no Consensus)

Nenhum estudo testa organizadores prévios em texto falado com adultos com TDAH.
Em população geral, pistas organizacionais ditas em voz alta durante uma aula ajudaram.
Elas aumentaram em 39% os pontos organizacionais anotados e de 15% a 45% a nota (Titsworth e Kiewra 2004).
Em adolescentes com dificuldades de aprendizagem, a prévia só ajudou quando os alunos foram ensinados a usá-la (Lenz 1987).

Em adultos com TDAH, o gargalo da leitura é a atenção sustentada, não a memória de curto prazo (Segal 2023, 50 contra 57).
A perda recai nas ideias centrais (Parks 2021; Yeari e Lavie 2021).
Michalek 2014 avisa que pistas a mais ajudaram menos o grupo TDAH sob carga de memória de trabalho.

### 4.4 A família da linguagem fácil (pergunta 8, do adendo 1)

Os cinco regulamentos foram lidos na fonte.
Para o alemão: Netzwerk Leichte Sprache 2022 e o rascunho E DIN SPEC 33429:2023, em versão fácil.
Para o Easy Read: Department of Health 2010 e NHS England 2018.
Para o espanhol e o francês: UNE 153101:2018 EX e Inclusion Europe 2009 (FALC).

Todos convergem num núcleo.
Frases curtas (DIN de 8 a 10 palavras; Easy Read até 15), e uma afirmação por frase.
Cada frase em sua linha, sem quebrar a unidade de sentido no fim da linha.
Mais ordem sujeito-verbo-objeto, voz ativa, a mesma palavra para a mesma coisa, e teste com leitores do grupo.

A regra que já é a Regra 1 da clear-read é "uma afirmação por frase" mais "cada frase em nova linha".
O que a família não tem é a distinção da clear-read entre quebra justa dentro do bloco e linha em branco entre tópicos.
A DIN é mais radical do que a clear-read tolera (uma informação por linha, 8 a 10 palavras).

As regras que servem a este leitor sem reduzir conteúdo são as de percepção e estrutura.
A linha que não quebra a unidade de sentido, o título que antecipa, e a mesma palavra sempre.
As regras de conteúdo (cortar números, cortar ressalvas, só o essencial) não servem, porque a clear-read mantém o conteúdo inteiro (R10b).
Duas revisões sistemáticas (Sutherland e Isherwood 2016; Chinn e Homeyard 2017) dizem que a eficácia do Easy Read é pouco conhecida.

### 4.5 Exemplo literal contra princípio (o achado da Fase B)

A documentação da Anthropic sustenta a hipótese em três lugares.
A página de boas práticas diz que exemplos são "one of the most reliable ways to steer Claude's output format, tone, and structure".
A página de skills diz que "Examples convey the desired style and level of detail to Claude more clearly than descriptions alone".
A página do Fable 5.1 dá como remédio para um desvio de escrita "add one complete example of a correct response".

A mesma página avisa que o modelo pode tratar texto do exemplo como "literal text to emit".
Esse é o fenômeno dos rótulos em inglês copiados, que a Fase B achou.

A literatura explica o mecanismo.
Min e colegas 2022 e Long e colegas 2024 mostram que o modelo extrai dos exemplos o formato e o vocabulário de saída.
Fu e colegas 2026 acham que regras explícitas vencem exemplos sozinhos, com vantagem menor em tarefas de estilo.
Então a forma certa para a skill é regra mais um exemplo completo, e o exemplo na língua do leitor.

Ponto-chave: a contagem nua segue sem estudo, o rótulo aberto tem custo medido por analogia, e regra mais exemplo é a forma recomendada.

## 5. As skills e normas da seção 7.4

### 5.1 A skill oficial da ElevenLabs

O repositório `elevenlabs/skills` foi clonado, no commit de 28 de outubro de 2026.
A skill `text-to-speech` foi lida inteira, com as referências e a skill interna `update-skills-from-changelog`.
Ela é um guia de API e SDK, não um guia de direção de voz.

Sobre o v4 ela diz três coisas: só `stability` e `similarity_boost`, sem SSML, e "direct delivery with audio tags such as [whispers], [laughs], [sarcastic]".
Ela não traz limite de caracteres, lista de pausas, IPA nem dicionário de pronúncia.

A divisão de trabalho que o guia propôs se confirma.
A clear-listen é dona do roteiro e dos intents.
O perfil de engine do playbook é dono da direção de voz, e o playbook pode cortar o que repete a API.

O que a documentação oficial resolve dos itens "[to test]" do playbook:

| Item do playbook | O que a fonte diz | Fonte |
|---|---|---|
| Limite de caracteres por chamada | v4: 10.000 (cerca de 10 minutos); v3: 5.000; Flash v2.5: 40.000 | página de modelos |
| `language_code` | ISO 639-1 ("pt"), não BCP-47 ("pt-BR"); ignorado se o modelo não suporta | skill oficial e referência da API |
| Costura entre chamadas | `previous_text` e `next_text`, ou até 3 `previous_request_ids`, evitam cortes e mudanças de tom na junção | skill oficial |
| Normalização de texto | `apply_text_normalization` com três modos; o Flash lê números pior | skill oficial |
| Tags de pausa | O blog oficial lista `[pause]` e `[long pause]`; `[short pause]` aparece só nas boas práticas | blog e boas práticas |
| Leito de ruído nativo | A API tem `audio_effects` com `background_noise_id` sob a voz; a regra "nada sob a voz" continua, mas a nota "uma tag dá um evento, não um leito" ficou datada | referência da API |

O mecanismo `update-skills-from-changelog` roda toda semana por um bot, em 23 dos últimos 25 PRs do repo.
Ele lê o changelog do produto e dispara revisão da skill quando um modelo entra ou sai, ou um parâmetro muda.
Três ideias dele servem ao perfil de engine e não dependem do repo da ElevenLabs.
Uma tabela "o que no changelog dispara revisão", a data de última conferência no perfil, e a verificação na documentação antes de mudar.

### 5.2 As skills de ASD-STE100

As duas skills do skills.sh foram lidas no GitHub: `danyuchn/asd-ste100-skill` (MIT, 4.900 estrelas) e `samber/cc-skills/humanizer-en-asd-ste100` (MIT).
A terceira, no skillsmp.com, não é uma skill própria.
Ela é uma cópia da skill de TheAngryByrd dentro de um repositório de F#.

Nenhuma traz o dicionário em forma que um lint consiga usar, e as três dizem isso de propósito.
A página 2 da Issue 9 exige autorização escrita da ASD para reproduzir qualquer parte.
A única lista pronta está fora das três, no repositório 0xpili.
São 869 palavras da Issue 7 (2017), com um aviso de que a lista é propriedade da ASD, e a recomendação é não vendorizar.

O que vale reaproveitar, com licença MIT:

| Item | Onde entra na clear-read | Como |
|---|---|---|
| Os grupos de sinônimos e a checagem "synonym rotation" do lint da danyuchn | R5b (uma palavra, um significado) e o lint | Um aviso de troca de sinônimo no pacote inglês, com os grupos de verbos |
| A tabela de contagem de palavras da samber (regras 8.1 a 8.7 da norma) | R2a e a contagem do lint | Reduzir falsos positivos em texto técnico: "10 °C", "ssh-copy-id" e "Lei 15.263" contam como uma palavra |
| O léxico inicial da samber (cerca de 45 pares "prefira/evite") | R5, "prefer a simpler word" | Aviso no pacote inglês, nunca problema |
| A divisão "regras estruturais contra lexicais" da danyuchn | A seção do lint no SKILL.md | Uma linha: o lint confere forma, não vocabulário, e a skill não reivindica conformidade com a norma |
| O padrão do TheAngryByrd: o usuário baixa o PDF oficial e um script lê a cópia dele | A pergunta do adendo 1 | O caminho legal para consultar o dicionário, se um dia for preciso |

Três conflitos a registrar.
A norma não proíbe o travessão, e a clear-read proíbe.
A norma permite passiva só com agente desconhecido em texto descritivo, e a clear-read tem três exceções.
A norma permite 6 frases por parágrafo, contra 4 da clear-read.

### 5.3 A ISO 24495-1, a DIN 8581-1 e a ABNT

A ISO 24495-1:2023 confere como o guia a descreve.
Ela define linguagem simples pelo resultado no leitor.
A definição: "wording, structure and design are so clear that intended readers can easily find what they need, understand what they find, and use" it.
Os quatro princípios são: o leitor recebe o que precisa (relevante), encontra (localizável), entende (compreensível) e usa (usável).

A cláusula 5.2.2 pede "introduce new information by building on information readers already know".
Isso é o "conhecido antes do novo" da clear-read, escrito numa norma internacional.

Duas correções no guia e no adendo 1.
O Brasil já tem a ABNT NBR ISO 24495-1:2024, publicada em 25 de julho de 2024, como adoção idêntica da ISO.
Ela é o equivalente da tradução alemã DIN ISO 24495-1, e não da DIN 8581-1.

E a Lei 15.263 não cita nem copia a ISO.
A tríade "encontrar, entender e usar" vem da definição da International Plain Language Federation, que a ISO também adota.

O `research-basis.md` da clear-read já cita a ISO duas vezes.
O que falta é a citação nos dois pacotes de língua e no parêntese da Regra 10 do SKILL.md.
A proposta para a Fase E: a ISO como base, e a ABNT, a Lei 15.263 e as Federal Plain Language Guidelines como aplicação.

### 5.4 Outros motores de voz

A clear-listen não precisa de nenhuma regra nova para seis motores.
As 12 perguntas do perfil e a escada de degradação cobrem todos, e o que falta é escrever os perfis.

| Motor | Direção disponível | Vozes em português brasileiro | O que o perfil faria |
|---|---|---|---|
| Google Cloud TTS | SSML completo: pausa em milissegundos, ênfase, prosódia, IPA | 43, sendo 30 Chirp 3 HD | Mapa direto de todos os intents |
| OpenAI gpt-4o-mini-tts | Um campo de instrução para a chamada inteira; sem pausa nem pronúncia garantidas | Vozes otimizadas para inglês | Tom pela instrução; pausa e `[say]` caem para o último degrau |
| Kokoro-82M (aberto, Apache) | Pronúncia por fonema no texto; velocidade | 3 vozes (pf_dora, pm_alex, pm_santa) | Render plain mais `[say]` por fonema |
| Piper (GPL, arquivado em 2025) | Fonemas do espeak-ng; silêncio uniforme entre frases | 4 vozes | Render plain mais `[say]` |
| edge-tts (GPL) | Só velocidade, volume e tom; SSML próprio bloqueado pela Microsoft | Depende do Azure | Render plain |
| Coqui XTTS-v2 | Nenhuma marca | Português na lista | Render plain |

Ponto-chave: as skills que existem confirmam a divisão de trabalho, a ISO já tem adoção brasileira, e os outros motores cabem na escada da clear-listen.

## 6. O que muda no inventário da Fase A

A Fase C muda a evidência de 21 linhas do inventário.
Quatro mudam o veredito de fato.

| Regra | Veredito na Fase A | Veredito depois da Fase C | Por quê |
|---|---|---|---|
| clear-listen R13b (troca de voz; frase importante logo depois) | mantém sem prova | **muda: reescrever** | A troca orienta (Potter 2000, 2008), mas o reconhecimento logo depois piora (Potter 2000). "Tom diferente" e "cedo" dependem de Potter 2019, na seção 9 |
| clear-listen R15 (fechar bem; resumo curto para depois) | mantém | **muda: reescrever a frase da revisão** | Murphy 2022 nunca testou resumo; a reescuta completa em 2x venceu. Sobrevive "revisar perto do uso" |
| clear-listen R6 (pergunta por parte com pausa) | mantém no áudio com teste | **mantém com qualificador forte** | A pergunta de fechamento sobre o texto inteiro tem prova (Stern e Halamish 2023); a por parte perdeu nesse estudo e vira hipótese da Fase D |
| clear-listen R11 (só voz) | mantém, "base direta mais forte" | **mantém com certeza média para TDAH** | Steindorf 2023 é a prova direta, em população geral; em TDAH as fontes medem inteligibilidade, não compreensão |
| clear-listen R13a (o Curioso) | mantém com teste, alta | mantém com certeza média | A prova é para "dar voz ao erro e perguntar por quê", não para a segunda voz em si |
| clear-listen R8 (falar com uma pessoa) | mantém, citação não confirmada | mantém, citação confirmada | Ginns 2013, d = 0,30 e 0,54; vale para lições curtas |
| clear-listen R9 (ritmo, pausas) | mantém como padrão a medir | mantém como padrão a medir, com menos apoio | Perde Fraundorf 2011 e Chen e Lorch 2018 como prova de pausas; Rodero 2016 qualificada |
| clear-listen R10 (expressão moderada) | mantém, vago | mantém "variada", reescreve "moderada" | Rodero 2022 sustenta moderação para credibilidade, não para atenção |
| clear-listen R12 (voz por papel) | mantém | mantém com qualificador | "TTS igual a humano" vira "sem diferença significativa em amostras pequenas" |
| clear-listen R1b e R3 (Parte N de M; dizer a estrutura) | testa antes de mudar | igual, evidência reescrita | Nenhuma fonte testou contagem nua, carga ou TDAH |
| clear-read R9 (tom) | muda | muda, dividindo | A fonte não existe; "sem enfeite" fica com detalhes sedutores; "sem personalidade" tem evidência contra (Ginns 2013) |
| clear-read R6e (conhecido antes do novo) | mantém, vira processo | igual, número corrigido | 65 a 181 ms, Haviland e Clark 1974 citado direto |
| clear-read R8b (calibrar) | vago, DOI não confirmado | vago, DOI confirmado | 10.1207/S15326985EP3801_4 |
| clear-read "arco" (narrativa) | mantém, com limite | mantém, limite reescrito | Narrativa ganha mais em memória do que em compreensão; "menos a entender mecanismo" sai |
| clear-read R2b e clear-listen R5 (conectores) | mantém | mantém, alcance reduzido | Cevasco só "but" e velocidade; Flowerdew só marcadores em segunda língua |
| Brann e Sidi (várias regras) | 2024 | 2025 | Ano de citação; o andaime era autorregulação, não "Key point" |
| Alderson 2013 (moldura) | meta-análise, DOI a0031742 | dois artigos | A meta-análise é Neuropsychology, DOI a0032371 |
| clear-listen R14 (novidade pela forma) | mantém | mantém, com fonte a mais | Potter, Lynch e Kraus 2015: jingles e efeitos habituam após a terceira repetição; a troca de voz não |
| clear-listen Fase 2 e R1d (segmentação) | alta | alta com qualificador | Só 4 de 88 comparações em áudio; segmentar custa tempo |
| clear-listen moldura (Clinton-Lisell) | g = 0,07, alta | igual, lido direito | g = 0,07 é ausência de diferença; ritmo próprio é marginal (g = 0,13) |
| clear-read R7e (três limites) | mantém, testável pelo lint_guide | mantém sem teste | Errata da Fase B, confirmada |

## 7. Sem prova ainda

- A contagem nua antes do conteúdo, em escuta: nenhum estudo (pergunta 1 da seção 7.3).
- O nome próprio antes do papel: só por analogia com a catáfora (pergunta 7).
- Ouvir contra ler sob distração em adultos com TDAH: buscado em 25 resumos e não achado (pergunta 6, seção 9).
- A velocidade de fala explicativa em português brasileiro que este leitor tolera (pergunta 5).
- A pausa de 4 a 6 segundos depois de uma pergunta: padrão de prática, sem estudo.
- "Um número por frase" contra "até dois": nenhum estudo fixa o número; é prática de rádio (seção 9).
- Diagramas, interativos e sobrecarga em adultos com TDAH: continua sem estudo, como a pesquisa consolidada já dizia.

## 8. Correções já aplicadas e as que ficam para a Fase E

Já aplicadas na seção 13 do guia: os DOIs de Lorch 2012, Antrobus 2019, Rabelo e Schochat 2007 e Alderson 2013.
Mais o periódico de Cevasco 2009.

Para a Fase E, no `research-basis.md` da clear-read:

- Haviland e Clark 1974 citado direto, com "até 181 ms".
- Kalyuga 2003 com o DOI.
- Brann e Sidi 2025.
- O limite do narrador reescrito.
- A R9 (tom) dividida em duas frases com fontes diferentes.

Para a Fase E, no `research-basis.md` da clear-listen:

- Brann e Sidi 2025.
- Potter 2000 e 2008 reatribuídos; Potter 2015 movido para a R14 (novidade pela forma), com o sobrenome Kraus.
- Ginns 2013 com DOI.
- Murphy 2022 como fonte do "estudo de reassistir", com a frase da R15 (fechar bem) reescrita.
- Blomberg 2019 separado de Blomberg 2021; Alderson corrigido; Michalek 2014 com números.
- Fraundorf 2011 e Chen e Lorch 2018 retirados das pausas.

Ponto-chave: cinco correções já estão no guia, e as outras entram com os PRs da Fase E, uma por regra.

## 9. Rodada de fechamento

Dez agentes cobriram as lacunas que o crítico apontou.
Os textos completos de Potter 2000, Potter 2008 e Potter 2019 continuam fechados (paywall, e a cópia de 2000 no ResearchGate é um scan ilegível).
Para esses três, o resumo é a fonte primária, e a janela em segundos vem de quem citou o artigo depois de lê-lo.

| Item | Veredito | O que a rodada achou | Consequência |
|---|---|---|---|
| Potter 2000: a memória melhora logo depois da troca de voz | ❌ | O resumo diz "momentary cognitive overload", pior quanto mais trocas. Quem leu o texto situa a queda nos primeiros 3 segundos, com recuperação depois (Rodero 2019; Xie 2009; Potter 2018). A orientação cardíaca dura de 6 a 10 segundos | A R13b (a segunda voz) passa a dizer: a troca chama a atenção, mas o ouvinte perde os primeiros 3 segundos; abra com uma frase descartável e só então dê a informação; use poucas trocas |
| Potter, Lang e Bolls 2008: nove recursos e reconhecimento | 🟡 | O resumo diz que os recursos, como categoria, melhoram o reconhecimento do que vem logo depois. A lista dos nove não está no resumo; o estudo-irmão de 1997 (ERIC ED415554) a traz, com a troca de voz entre eles | Não citar 2008 para "queda depois da troca"; citar 1997 para a lista; sem tamanho de efeito nem janela para 2008 |
| Potter e colegas 2019: diferença de tom e troca cedo | 🟡 | 41 participantes, uma troca por comercial, três diferenças de tom (12, 22 e 63 Hz). Maior diferença, orientação mais forte (p = 0,004). A troca nos primeiros 20 segundos orientou; nos últimos 20, não. Mas a informação logo depois da troca de maior diferença foi lembrada pior (45% contra 63%), segundo relato de segunda mão | As duas frases da R13b ganham fonte, limitadas à atenção. "Dê alguns segundos entre a troca e a informação-chave" entra junto |
| Lorch 2012: o que a prévia dizia | 🟡 (texto completo do companheiro de 2013) | As prévias nomeiam o tópico e sua posição: "Yet another problem we face... is environmental damage", "One of the environmental problems is air pollution". A enumeração é só enquadramento; nunca um número isolado | A hipótese da Fase D fica "prévia que nomeia o tópico", não "contagem que entrega conteúdo". O exemplo "esta seção cobre três causas" sai do guia |
| Chen e Lorch 2018: "cortou as pausas pela metade" | 🟡 (tese de 2015, texto completo) | Com troca de voz nos títulos: 5,73 pausas contra 12,48 e 13,27 nos outros títulos; mas não menos do que sem título (7,15), efeito pequeno (η²p = 0,037, p perto de 0,057), e sumiu no experimento 2 | O número tem fonte, com três qualificadores; a parte sólida é que títulos audíveis aumentaram as ideias anotadas (η²p = 0,32), sem diferença entre os tipos |
| Michalek 2014 | 🟡 (texto completo) | 25 adultos com TDAH contra 38; repetição de frases em balbucio; com só áudio o grupo TDAH não diferiu; a perda veio quando um fluxo a mais (o rosto) entrou sob ruído. O título que circulava estava errado | Apoio indireto à parte "nenhum fluxo a mais" da R11 (só voz); não apoia compreensão. Título correto: "Effects of noise and audiovisual cues on speech processing in adults with and without ADHD" |
| Números por frase | ⚪ | Nenhum estudo fixa um número. O mais perto é Fridman 2022: em consultas médicas, o conhecimento cai quando palavras quantitativas passam de 4% da conversa. A origem da regra é prática de rádio (NPR Training) | A R7 (poucos números) marca "um por frase" como prática, certeza baixa; a pesquisa consolidada 8.4 passa a "1, ou 2 quando a comparação exige"; vira parâmetro da Fase D |
| Exemplos resolvidos (clear-read R3) | 🟡 | Sweller, van Merriënboer e Paas 2019 (revisão, sem tamanho de efeito); Barbieri e colegas 2023, meta-análise em matemática, 55 estudos, g = 0,48. Exemplos corretos sozinhos rendem mais do que corretos misturados com incorretos | Apoio indireto à R3: o "fraco" deve ficar curto e o "forte" carregar o peso; o efeito cai em leitores experientes |
| Pergunta 6: ouvir ou ler sob distração, TDAH adulto | buscado e não achado | 25 resumos lidos no Consensus e no Valency. Vizinhos: Cain e Bignell 2014 (crianças, sem distração), Socher 2026 (crianças, com ruído, sem TDAH), Lemel 2023 (adultos com TDAH, só escuta) | A pergunta fica aberta, agora com a busca registrada |
| Pergunta 7: nome antes do papel | buscado e não achado | Evidência indireta: nomes desconhecidos prejudicam a escuta em segunda língua (Kobeleva 2012, 110 participantes); um nome cuja forma indica a categoria custa menos (Kobeleva 2008) | Favorece dar o papel junto com o nome; continua "razoável, não provado" |
| Rodero, Potter e Prieto 2017 | 🟡 (texto completo) | 51 ouvintes, uma voz masculina, quatro padrões de entonação. Só o padrão agudo-depois-grave melhorou recall (21,5%), e o outro padrão variado foi o pior; os dois variados venceram em reconhecimento; a frequência cardíaca não diferiu | A R10 (expressão) mantém "variada" com um limite: variação dentro da frase, não qualquer variação; e perde "atenção" como medida |

Dois pontos fecham a rodada.
A R13b (a segunda voz) é a regra que mais muda.
A troca de voz vale pela orientação e custa 3 segundos de memória.
Então ela pede poucas trocas e uma frase de transição antes da informação-chave.

E a hipótese da Fase D muda de nome.
Não é "contagem que entrega conteúdo", é "prévia que nomeia o tópico", porque é isso que as fontes testaram.

Ponto-chave: três textos completos continuam fechados, e mesmo pelos resumos a R13b precisa ser reescrita e a hipótese da contagem precisa ser renomeada.
