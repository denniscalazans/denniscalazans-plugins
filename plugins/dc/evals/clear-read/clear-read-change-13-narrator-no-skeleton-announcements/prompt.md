---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

[Run this case twice with the full clear-read SKILL.md loaded: once as it is, and once with the two paragraphs "Who writes" and "Where the story stops helping" removed from the section "Who you are writing for". A judge model counts structure announcements in each reply: phrases that describe the text's own skeleton instead of delivering content, such as "são quatro causas", "existem N motivos", "primeiro", "segundo", "em primeiro lugar", "nesta seção vamos ver", "a seguir veremos", "como veremos", "os pontos abaixo". A numbered list of steps inside a mechanism does not count; a sentence that announces the list does.] Explique, em português, em cerca de 400 palavras, por que um deploy pode passar no ambiente de teste e falhar em produção, para uma pessoa de TI que nunca investigou isso. As causas comuns são quatro: variáveis de ambiente diferentes, versões de dependência diferentes, dados reais maiores e mais sujos, e carga real. Para uma delas, explique o mecanismo passo a passo: como uma variável de ambiente ausente vira um erro só em produção.
