# Adendo 1: normas de linguagem simples e skills que já existem

ESCRITO: 2026-11-01 15:30 (Berlim), pelo Claude, numa conversa com o Dennis depois do handoff.
PARA: o agente que executa o guia de investigação.

Quando incorporar: na Fase C, no fim da fase em andamento.
O que muda: a seção 7.4 do guia ganha dois itens, e a seção 7.3 ganha uma pergunta.
O inventário da Fase A não muda.

## 1. Skills de ASD-STE100 já existem em catálogos públicos

A ASD-STE100 é a norma da indústria aeroespacial para inglês técnico simplificado: 53 regras de escrita e um dicionário de cerca de 900 palavras aprovadas.
A clear-read cita a Issue 9 dela como base das Regras 2, 5 e 11.

Em 1 de novembro de 2026, uma busca achou skills prontas sobre a norma em catálogos públicos:

- `asd-ste100-skill`, no skills.sh: https://www.skills.sh/danyuchn/asd-ste100-skill/simplified-technical-english-(asd-ste100)
- `humanizer-en-asd-ste100`, no skills.sh: https://www.skills.sh/samber/cc-skills/humanizer-en-asd-ste100
- Uma skill no skillsmp.com: https://skillsmp.com/creators/tw0po1nt/fshttp.studio/agents-skills-simplified-technical-english

Nenhuma foi lida.
A tarefa para a Fase C é a mesma da seção 7.4 do guia sobre a ElevenLabs.
Ler, comparar com o que a clear-read já tem, e decidir o que reaproveitar.
A pergunta que importa: alguma delas traz o dicionário da norma em forma que um lint consiga usar?
Hoje o lint da clear-read não confere vocabulário, só forma.

## 2. A clear-read deve citar a norma ISO de linguagem simples

O pacote de língua `references/lang-pt-br.md` cita a Lei 15.263, de 14 de novembro de 2025 (Política Nacional de Linguagem Simples).
O pacote `references/lang-en.md` cita as Federal Plain Language Guidelines dos Estados Unidos.
Nenhum dos dois cita a norma internacional, ISO 24495-1:2023.

Essa norma é o guarda-chuva das duas.
Ela é neutra em relação à língua, e tem quatro princípios: o leitor recebe o que precisa, encontra, entende e consegue usar.
O artigo 4º da lei brasileira ("encontrar, entender e usar") segue esses princípios.
A norma alemã DIN 8581-1, de maio de 2024, é a aplicação da ISO ao alemão.
Ela é o modelo do que uma norma ABNT faria para o português.

Proposta para a Fase E: o SKILL.md da clear-read e os dois pacotes de língua citam a ISO 24495-1 como base.
A lei e as diretrizes nacionais entram como aplicação.
Isso deixa a skill portátil para uma terceira língua, porque a norma é o que não muda de país para país.

Fontes: https://www.iso.org/standard/78907.html e https://www.dinmedia.de/en/standard/din-8581-1/377238273.

## 3. Uma classificação para o inventário

As regras de texto fácil no mundo se dividem em três famílias.
A classificação ajuda a Fase A a marcar de onde vem cada regra da clear-read.

| Família | Para quem | O que controla | Exemplos |
|---|---|---|---|
| Linguagem controlada | Profissionais lendo instruções, muitas vezes em segunda língua | Vocabulário fechado e regras de gramática | ASD-STE100, Caterpillar Technical English |
| Linguagem simples | O público geral | Estrutura, frase, palavras, layout, teste com leitores | ISO 24495-1, Lei 15.263, Plain Writing Act de 2010, DIN 8581-1 |
| Linguagem fácil | Pessoas com deficiência intelectual ou grande dificuldade de leitura | Tudo da linguagem simples, mais regras muito estritas e revisão por leitores do grupo | Leichte Sprache (Alemanha), Easy Read (Reino Unido), FALC (França), UNE 153101 (Espanha) |

A clear-read fica entre a primeira e a segunda família.
Ela pega da linguagem simples a estrutura e o teste com o leitor.
Ela pega da linguagem controlada a regra "uma palavra, um significado" e o limite de palavras por frase.
O zero retrocesso não vem de nenhuma das três, porque nenhuma foi feita para leitura interrompida.

Pergunta nova para a seção 7.3 do guia: a família da linguagem fácil tem alguma regra que sirva a este leitor sem reduzir o conteúdo?
A regra "uma ideia por linha" já é a Regra 1 da clear-read.
As outras precisam de leitura.

Ponto-chave: três famílias de normas, a clear-read mistura duas, e a ISO 24495-1 é a base que falta citar.
