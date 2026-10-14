#!/usr/bin/env python3
"""lint_clear_read.py: check a Markdown or HTML document against the clear-read rules.

Usage:
    python3 lint_clear_read.py FILE [FILE ...] [--lang auto|pt|en] [--max-words 25]
                               [--avg-words 17] [--max-sentences 4] [--no-warnings]

It prints one line per finding, as "path:line: [problem|warning|note] rule: message",
then "N problems" as the last line. The exit code is 1 when N > 0.
Warnings never change the exit code. They are prompts to re-read a passage.
Notes carry information, such as the language the lint used.

Standard library only. A file ending in .html, .htm or .xhtml is read as HTML, and
one ending in .md, .markdown, .mdx or .txt as Markdown. Any other name is sniffed:
the file is HTML when a line in its first 2,000 characters starts with a doctype,
<html>, <body>, or a block-level tag such as <p>, <div> or <h2>, with or without
attributes.

Languages. The skill writes in the reader's language, above all Brazilian Portuguese
and English, so every language-dependent rule reads its words from LANG_PACKS below.
A new language is one more entry in that dict. With --lang auto (the default), the
lint counts common words of each language over the whole text and picks the winner.
A tie, or fewer than 20 words, falls back to "en" and says so in a note.

Problems (they fail the run):
    dash-joiner         an em dash anywhere in prose, or an en dash that is not
                        between two digits (a range like 15-20 is fine).
    sentence-length     a sentence with more than --max-words words (default 25).
    paragraph-length    a block with more than --max-sentences sentences (default 4).
                        A list item is its own block. Table rows are skipped.
    backward-reference  a phrase that points the reader back instead of naming the
                        thing. en: "as mentioned", "as we saw", "as described above",
                        "above" as a pointer, "earlier", "previously", "the
                        aforementioned", "the former", "the latter". pt: "como
                        vimos", "como dito", "como mencionado", "anteriormente",
                        "mencionado", "já citado", "citado acima", "visto acima",
                        "descrito acima", "o ponto anterior", "a seção anterior",
                        "o primeiro ponto", "a primeira ideia" and similar. A bare
                        "acima" is only a warning, because it can be spatial.
                        Exclusions: "above 25 words", "earlier than", "earlier
                        version".
    bare-label          a label such as P1, C2, Step 3, Passo 3 or Etapa 3 whose
                        first mention in a block carries no name. A label counts as
                        named when it is followed by "(", a middle dot, ":", "=", a
                        quote or " - ". Later mentions in the same block are fine.
                        Common technical tokens (H1 to H6, S3, M1, A4, F1 to F12)
                        are not labels.
    visual-without-how-to-read  a visual (a ```mermaid fence, a Markdown image on
                        its own line, a <figure>, an <img>, a <pre class="mermaid">
                        or an SVG that is not a small icon) whose next block does not
                        start with the "How to read" marker. en: "How to read:".
                        pt: "Como ler:". Tables are not visuals for this rule.
    analogy-without-limit  an analogy in one of its structural forms ("think of it as",
                        "it's like a", "works like a", "the analogy is"; pt: "pense nisso
                        como um", "é como um", "funciona como um", "parecido com um", "a
                        analogia é") with no line, before the next heading, that says where
                        it fails. en: "Where the analogy fails:", "unlike a". pt: "Onde a
                        analogia falha:", "diferente de um", "ao contrário de um". The bare
                        word "analogy" and "imagine a user who..." are not analogies.

Warnings (reported, never fatal):
    visual-without-conclusion  the "How to read" block has one sentence and nothing
                        follows it before the next heading. The reader gets the
                        legend but not the point.
    acronym-without-full-name  a word of 2 to 6 capital letters (a plural "CDNs" counts as
                        "CDN") whose first mention in the body is not next to its full name:
                        inside parentheses, followed by one, or followed by a colon as in a
                        Key terms list. Acronyms every reader knows (API, HTML, PDF, USA,
                        EU, country and state codes, currencies, and each language's own
                        list), Roman numerals, labels and emphasis words (NEVER, TODO) are
                        free. Later mentions are free. Any parentheses count as a
                        definition, so "(see the CDN docs)" passes.
    hidden-verb         a light verb (make, perform, conduct, do, give, take, reach, come
                        to; pt: fazer, realizar, efetuar, dar, tomar, chegar), an optional
                        determiner and adjective, then a noun from a closed list of nouns
                        made from verbs (analysis, decision, review, conclusion, validation;
                        pt: análise, decisão, revisão, conclusão, verificação). The list is
                        closed on purpose, so "take the medication" and "reach the
                        destination" pass. pt also flags "a realização da análise".
    inserted-clause     a clause of 5 or more words between commas, right after a short
                        subject (up to 5 words), when the clause opens with a relative
                        pronoun (which, who, whose, where; pt: que, quem, cujo, onde), a
                        participle or a gerund. A list ("A, B and C"), an opening phrase
                        ("However, ...", "No entanto, ...") and a clause that opens with a
                        conjunction or a preposition ("after a week of tests") do not count.

What the lint ignores: YAML front matter, HTML comments, fenced code blocks,
inline code (replaced by the word "code"), <script>, <style>, <pre>, <svg>,
<table> and <head> elements, Markdown table rows, link targets and raw URLs.
Decimal numbers with a comma (4,6) or a dot (4.6) never split a sentence, and
neither do the abbreviations listed per language (e.g., i.e., p. ex., art., pág.).
"""
import html as html_lib
import os
import re
import sys
from dataclasses import dataclass, field

DEFAULT_MAX_WORDS = 25
DEFAULT_AVG_WORDS = 17
DEFAULT_MAX_SENTENCES = 4
MIN_WORDS_FOR_DETECTION = 20
FALLBACK_LANG = "en"

EM_DASH = "—"
EN_DASH = "–"
MIDDLE_DOT = "·"

# ---------------------------------------------------------------- language packs
#
# Everything that depends on the language lives here. Each pack has:
#   name           how the language is called in messages
#   stopwords      common words used to detect the language (avoid words shared
#                  with the other packs, such as "a", "as", "do", "no")
#   abbreviations  strings whose dots never end a sentence
#   backward       (regex, level) pairs; the regex is matched case-insensitively
#   key_points     lowercase starts of a sentence that count as a Key point line
#   key_point_hint the marker the message suggests
#   label_words    words that make a label with a number ("Step 3", "Passo 3")
#   passive        the data of the passive heuristic (see check_passive)

_PT_DET = r"(?:[nd]?[oa]|pel[oa])"   # o, a, no, na, do, da, pelo, pela

LANG_PACKS = {
    "en": {
        "name": "English",
        "stopwords": {
            "the", "and", "that", "with", "this", "from", "which", "have", "not", "for",
            "is", "are", "of", "to", "in", "it", "on", "be", "or", "was", "you", "your",
        },
        "abbreviations": (
            "e.g.", "E.g.", "i.e.", "I.e.", "etc.", "vs.", "cf.", "approx.", "ca.", "al.",
            "Dr.", "Mr.", "Mrs.", "Ms.", "St.", "No.", "Fig.", "Eq.", "Jr.", "Sr.",
            "Inc.", "Ltd.", "Co.", "pp.", "U.S.", "U.K.", "a.m.", "p.m.",
        ),
        "backward": [
            (r"\bas\s+(?:we\s+|i\s+|you\s+)?(?:mentioned|noted|discussed|explained|described|"
             r"shown|stated|saw|said|covered|outlined)(?:\s+(?:above|earlier|before|previously))?", "problem"),
            (r"\b(?:the\s+)?aforementioned\b", "problem"),
            (r"\bthe\s+former\b", "problem"),
            (r"\bthe\s+latter\b", "problem"),
            (r"\babove\b(?!\s+(?:\d|about|roughly|around|average|zero|one|two|three|four|five|six|"
             r"seven|eight|nine|ten|the\s+(?:line|fold|limit|threshold|ceiling|floor|average|target)))", "problem"),
            (r"\bpreviously\b", "problem"),
            (r"\bearlier\b(?!\s+(?:than|versions?|releases?|stud(?:y|ies)|work|drafts?|this|that|today|"
             r"in\s+the|on\s+the|at\s+the))", "problem"),
        ],
        "key_points": ("key point", "key takeaway", "takeaway", "in short"),
        "key_point_hint": "Key point:",
        "label_words": ("Step", "Phase", "Part", "Stage", "Point", "Option"),
        "how_to_read": ("how to read",),
        "how_to_read_hint": "How to read:",
        "analogy": [
            r"\bthink of (?:it|this|that|the \w+(?: \w+)?) as\b",
            r"\b(?:it|this|that|which)(?:'s| is) like an?\b",
            r"\b(?:is|are|works?|behaves?|acts?) (?:a bit |a lot |much |rather )?like an?\b",
            r"\bthe analogy (?:is|here is|would be)\b",
        ],
        "analogy_limit": [
            r"\bwhere the analogy (?:fails|breaks|ends|stops)",
            r"\bthe analogy (?:fails|breaks|ends|stops)",
            r"\bunlike an?\b",
        ],
        "analogy_limit_hint": "Where the analogy fails:",
        "hidden_verb": {
            "light_verbs": r"(?:make|makes|made|making|perform|performs|performed|performing|conduct|conducts|"
                           r"conducted|conducting|carry out|carries out|carried out|carrying out|do|does|did|"
                           r"give|gives|gave|take|takes|took|taken|provide|provides|provided|reach|reaches|"
                           r"reached|achieve|achieves|achieved|undertake|undertakes|undertook|come to|comes to|came to)",
            "determiners": r"(?:a|an|the|its|their|your|our|his|her|my|some|this|that|another|each|every|no)",
            "nouns": {
                "analysis", "decision", "review", "assessment", "evaluation", "investigation", "examination",
                "inspection", "verification", "validation", "implementation", "installation", "configuration",
                "consideration", "recommendation", "determination", "calculation", "estimation", "estimate",
                "measurement", "adjustment", "improvement", "assumption", "conclusion", "discussion",
                "comparison", "description", "explanation", "notification", "authorization", "approval",
                "payment", "selection", "submission", "modification", "correction", "resolution", "allocation",
                "reduction", "protection", "preparation", "collection", "suggestion", "confirmation",
                "cancellation", "deletion", "creation", "registration", "migration", "deployment",
                "definition", "assistance", "investment", "agreement", "announcement", "arrangement",
                "commitment", "contribution", "inquiry", "introduction", "observation", "prediction",
                "proposal", "purchase", "request", "choice", "attempt", "distinction", "judgment", "mention",
                "reference", "statement", "summary", "demonstration", "translation", "connection",
                "objection", "complaint", "revision", "replacement", "repair", "search", "test", "backup",
            },
            "noun_first": None,
        },
        "hidden_verb_hint": "\"analyze\" instead of \"perform an analysis\"",
        "known_acronyms": {
            "WHO", "FBI", "CIA", "NHS", "IRS", "GDP", "GDPR", "NYT", "MIT", "IBM", "AWS", "GCP",
        },
        "emphasis_words": {
            "NOT", "NEVER", "ALWAYS", "ONLY", "MUST", "DO", "DONT", "NO", "YES", "TODO", "NOTE", "FAIL",
            "PASS", "TBD", "TLDR", "AND", "OR", "THE", "ALL", "NEW", "OLD", "OFF", "ON", "WARNING", "ERROR",
            "STOP", "END", "START", "DONE", "FIXME", "OK",
        },
        "intro_words": {
            "however", "in", "on", "at", "for", "by", "with", "without", "after", "before", "when", "if",
            "because", "as", "since", "while", "although", "though", "unless", "until", "once", "so", "then",
            "first", "second", "third", "next", "finally", "also", "instead", "otherwise", "today",
            "yesterday", "tomorrow", "here", "there", "now", "later", "meanwhile", "overall", "still", "yet",
            "and", "but", "or", "to", "from", "during", "under", "over", "through", "across", "despite",
            "like", "unlike", "according", "besides", "moreover", "therefore", "thus", "hence", "again",
            "above", "below", "inside", "outside", "beyond", "of", "sadly", "luckily", "ideally", "usually",
            "often", "sometimes", "yes", "no", "e.g", "i.e",
        },
        "clause_openers": {"which", "who", "whom", "whose", "where"},
        "clause_opener_endings": r"(?:ing|ed)$",
        "passive": {
            "aux": r"(?:am|is|are|was|were|be|been|being)",
            "gap_words": 1,
            "gap_allowed": re.compile(r"^\w+ly$", re.I),        # only an adverb may sit in the gap
            "suffixes": ("ed",),
            "min_len": 4,
            "irregular": {
                "begun", "bent", "bitten", "blown", "born", "borne", "bought", "bound", "broken",
                "brought", "built", "burnt", "caught", "chosen", "cut", "dealt", "done", "drawn",
                "driven", "eaten", "fed", "felt", "fled", "flown", "forgotten", "found", "frozen",
                "given", "gone", "grown", "held", "hidden", "hit", "hung", "hurt", "kept", "known",
                "laid", "led", "left", "lent", "let", "lit", "lost", "made", "meant", "met",
                "paid", "proven", "put", "read", "rebuilt", "rewritten", "ridden", "run", "said",
                "seen", "sent", "set", "shaken", "shown", "shut", "sold", "sought", "spent",
                "split", "spoken", "spread", "stolen", "struck", "stuck", "sung", "swept", "taken",
                "taught", "thought", "thrown", "told", "torn", "understood", "woken", "won",
                "worn", "woven", "written",
            },
            "not_participles": {
                "bored", "concerned", "delighted", "excited", "interested", "pleased", "relaxed",
                "satisfied", "scared", "surprised", "tired", "worried", "supposed", "advanced",
                "detailed", "limited", "unlimited", "united", "red", "need", "indeed", "bed",
            },
            "accent_rule": False,
            "agent": r"\bby\b",
        },
    },
    "pt": {
        "name": "Portuguese",
        "stopwords": {
            "de", "que", "não", "para", "com", "uma", "por", "mais", "como", "isso",
            "é", "são", "da", "em", "ou", "se", "os", "um", "também", "porque", "quando", "você",
        },
        "abbreviations": (
            "p. ex.", "ex.", "Dr.", "Dra.", "Sr.", "Sra.", "Srta.", "etc.", "n.º", "nº", "art.",
            "séc.", "pág.", "págs.", "fig.", "Fig.", "obs.", "Obs.", "prof.", "Prof.", "Profa.",
            "tel.", "av.", "Av.",
        ),
        "backward": [
            (r"\bcomo\s+(?:já\s+)?(?:vimos|dito|mencionad[oa]|citad[oa]|explicad[oa]|descrit[oa]|falad[oa]|"
             r"visto|falei|disse|expliquei)\b", "problem"),
            (r"\b(?:citad[oa]|visto|vista|descrit[oa]|mencionad[oa]|explicad[oa]|mostrad[oa]|apresentad[oa])s?\s+acima\b", "problem"),
            (r"\bjá\s+(?:citad|mencionad|explicad|descrit|apresentad)[oa]s?\b", "problem"),
            (r"\bmencionad[oa]s?\b", "problem"),
            (r"\banteriormente\b", "problem"),
            (r"\b" + _PT_DET + r"\s+(?:ponto|item|passo|trecho|parágrafo|bloco)\s+anterior\b", "problem"),
            (r"\b" + _PT_DET + r"\s+(?:sec?ção|parte|etapa|ideia|idéia)\s+anterior\b", "problem"),
            (r"\b" + _PT_DET + r"\s+(?:primeir|segund|terceir)[oa]\s+(?:ponto|item|ideia|idéia|parte|passo|conceito)\b", "problem"),
            (r"\bacima\b", "warning"),
        ],
        "key_points": ("ponto-chave", "ponto chave", "em resumo", "resumo:", "o que fica"),
        "key_point_hint": "Ponto-chave:",
        "label_words": ("Passo", "Etapa", "Fase", "Parte", "Ponto", "Opção", "Conceito"),
        "how_to_read": ("como ler",),
        "how_to_read_hint": "Como ler:",
        "analogy": [
            r"\bpense (?:n[oa]s? \w+(?: \w+)? |nisso |nisto |nele |nela )?como (?:um|uma|se)\b",
            r"\b(?:é|são|funciona|funcionam|age|agem|parece|parecem) (?:um pouco |muito |mais ou menos )?como (?:um|uma|se)\b",
            r"\bparecid[oa]s? com (?:um|uma)\b",
            r"\ba analogia (?:é|aqui é|seria)\b",
        ],
        "analogy_limit": [
            r"\bonde a analogia (?:falha|para|termina|quebra)",
            r"\ba analogia (?:falha|para|termina|quebra)",
            r"\bdiferente de (?:um|uma)\b",
            r"\bao contrário de (?:um|uma)\b",
        ],
        "analogy_limit_hint": "Onde a analogia falha:",
        "hidden_verb": {
            "light_verbs": r"(?:fazer|faz|fazem|fez|fizeram|faça|façam|fazendo|realizar|realiza|realizam|realizou|"
                           r"realizaram|realize|realizando|efetuar|efetua|efetuam|efetuou|efetuaram|efetue|proceder|"
                           r"procede|procedem|procedeu|executar|executa|executam|executou|promover|promove|promovem|"
                           r"promoveu|dar|dá|dão|deu|deram|dê|tomar|toma|tomam|tomou|tomaram|tome|chegar|chega|"
                           r"chegam|chegou|chegaram|levar|leva|levam|levou)",
            "determiners": r"(?:a|o|à|ao|uma|um|as|os|às|aos|sua|seu|suas|seus|nossa|nosso|esta|este|essa|esse|"
                           r"outra|outro|cada|nenhuma|nenhum|alguma|algum)",
            "nouns": {
                "análise", "decisão", "revisão", "avaliação", "verificação", "validação", "investigação",
                "exame", "inspeção", "implementação", "implantação", "instalação", "configuração",
                "consideração", "recomendação", "determinação", "cálculo", "estimativa", "medição", "ajuste",
                "melhoria", "suposição", "conclusão", "discussão", "comparação", "descrição", "explicação",
                "notificação", "autorização", "aprovação", "pagamento", "seleção", "submissão", "envio",
                "modificação", "correção", "resolução", "alocação", "redução", "proteção", "preparação",
                "coleta", "sugestão", "confirmação", "cancelamento", "exclusão", "criação", "cadastro",
                "migração", "definição", "entrega", "leitura", "contagem", "limpeza", "tradução",
                "atualização", "execução", "cobrança", "apresentação", "teste", "pergunta", "pedido",
                "reclamação", "escolha", "tentativa", "compra", "investimento", "acordo", "anúncio",
                "contribuição", "consulta", "observação", "previsão", "proposta", "referência", "menção",
                "distinção", "afirmação", "resumo", "demonstração", "conexão", "objeção", "providência",
                "providências", "votação", "substituição", "reparo", "busca", "backup", "conferência",
            },
            "noun_first": r"\b(?:a|à)\s+(?:realização|execução|efetivação|efetuação)\s+d[aeo]s?\b",
        },
        "hidden_verb_hint": "\"verificar\" em vez de \"realizar a verificação\"",
        "known_acronyms": {
            "EUA", "ONU", "OMS", "UE", "CPF", "CNPJ", "RG", "CEP", "SUS", "STF", "STJ", "TSE", "TST", "IBGE",
            "PIB", "IPCA", "CLT", "INSS", "FGTS", "USP", "UFRJ", "LGPD", "PL", "MP",
        },
        "emphasis_words": {
            "NUNCA", "SEMPRE", "SIM", "NOTA", "ERRO", "FALHA", "NOVO", "TUDO", "FIM", "OK", "PARE", "ALERTA",
        },
        "intro_words": {
            "no", "na", "nos", "nas", "em", "para", "por", "com", "sem", "depois", "antes", "quando", "se",
            "porque", "como", "desde", "enquanto", "embora", "mesmo", "até", "então", "assim", "primeiro",
            "segundo", "terceiro", "também", "hoje", "ontem", "amanhã", "aqui", "ali", "agora", "mais",
            "ainda", "e", "mas", "ou", "a", "à", "ao", "de", "do", "da", "dos", "das", "durante", "sob",
            "sobre", "apesar", "além", "portanto", "logo", "ou seja", "isto", "aliás", "enfim", "afinal",
            "sim", "não", "pelo", "pela", "num", "numa", "entre", "contra", "conforme", "segundo",
            "felizmente", "infelizmente", "geralmente", "normalmente", "às", "aos", "ex", "p",
        },
        "clause_openers": {"que", "quem", "cujo", "cuja", "cujos", "cujas", "onde"},
        "clause_opener_endings": r"(?:ndo|ad[oa]s?|id[oa]s?)$",
        "passive": {
            "aux": r"(?:é|são|foi|foram|era|eram|será|serão|seria|seriam|sendo|sido|ser|"
                   r"está|estão|esteve|estiveram|estava|estavam|estará|estarão|estar|estando)",
            "gap_words": 2,
            # In the gap only adverbs and short connectors; a determiner means a noun follows.
            "gap_allowed": re.compile(r"^(?:não|já|sempre|ainda|também|muito|bem|mal|então|assim|logo|"
                                      r"nunca|talvez|hoje|ontem|agora|\w+mente)$", re.I),
            "suffixes": ("ado", "ada", "ados", "adas", "ido", "ida", "idos", "idas"),
            "min_len": 5,
            "irregular": {
                "feito", "feita", "feitos", "feitas", "dito", "dita", "ditos", "ditas", "escrito", "escrita",
                "escritos", "escritas", "visto", "vista", "vistos", "vistas", "posto", "posta", "postos",
                "postas", "aberto", "aberta", "abertos", "abertas", "coberto", "coberta", "cobertos",
                "cobertas", "pago", "paga", "pagos", "pagas", "gasto", "gasta", "gastos", "gastas",
                "aceito", "aceita", "aceitos", "aceitas", "entregue", "entregues", "impresso", "impressa",
                "impressos", "impressas", "salvo", "salva", "salvos", "salvas", "expulso", "expulsa",
            },
            "not_participles": {
                "lado", "lados", "estado", "estados", "mercado", "mercados", "resultado", "resultados",
                "cuidado", "cuidados", "advogado", "advogados", "empregado", "empregados", "dado", "dados",
                "passado", "significado", "teclado", "soldado", "deputado", "tratado", "legado", "grado",
                "sentido", "sentidos", "partido", "partidos", "pedido", "pedidos", "vestido", "vestidos",
                "conteúdo", "ouvido", "ouvidos", "tecido", "tecidos", "apelido", "marido", "ruído",
                "período", "fluido", "sólido", "líquido", "nada", "cada", "ainda", "vida", "vidas",
                "saída", "saídas", "entrada", "entradas", "comida", "bebida", "medida", "medidas",
                "dívida", "dúvida", "ida", "idas", "fada", "nada", "estrada", "jornada", "temporada",
                "rodada", "camada", "chamada", "chamadas", "parada", "paradas", "morada",
            },
            "accent_rule": True,     # an accent before the ending ("rápido", "líquido") means an adjective
            "agent": r"\b(?:por|pel[oa]s?)\b",
        },
    },
}

LANG_CHOICES = ("auto",) + tuple(LANG_PACKS)

# ---------------------------------------------------------------- language-agnostic data

WORD = re.compile(r"[A-Za-z0-9À-ɏ][\w'’À-ɏ-]*(?:[.,]\d+)*")
ACCENTED = re.compile(r"[À-ÿ]")

LABEL_ALLOWLIST = (
    {f"H{n}" for n in range(1, 7)}
    | {"S3", "M1", "M2", "M3", "M4", "M5", "A3", "A4", "A5", "V8", "G7", "G20"}
    | {f"F{n}" for n in range(1, 13)}
)
_ALL_LABEL_WORDS = sorted({w for p in LANG_PACKS.values() for w in p["label_words"]}, key=len, reverse=True)
LABEL = re.compile(
    r"\b(?:(?P<code>[A-Z]\d{1,2})|(?P<word>" + "|".join(_ALL_LABEL_WORDS) + r")\s+(?P<n>\d{1,2}))\b"
)
LABEL_NAMED_AFTER = re.compile(r"^\**\s*(?:\(|" + MIDDLE_DOT + r"|:|=|\"|“|\s-\s)")

# Acronyms every reader of a technical text already knows. Each language pack adds its own.
GLOBAL_ACRONYMS = {
    "API", "URL", "URI", "HTML", "CSS", "JS", "TS", "JSON", "XML", "YAML", "CSV", "SQL", "HTTP", "HTTPS",
    "FTP", "SSH", "TLS", "SSL", "DNS", "IP", "TCP", "UDP", "CPU", "GPU", "RAM", "SSD", "HDD", "USB",
    "PDF", "PNG", "JPG", "JPEG", "GIF", "SVG", "MP3", "MP4", "ID", "AI", "ML", "UI", "UX", "CLI", "GUI",
    "IDE", "SDK", "CI", "CD", "PR", "QA", "OS", "IT", "DB", "CRUD", "REST", "CEO", "CTO", "CFO", "FAQ",
    "TV", "GPS", "DOI", "ISBN", "ISO", "IEEE", "W3C", "LLM", "GPT", "NLP", "OCR", "TTS", "PC", "VPN",
    "LAN", "WAN", "ERP", "CRM", "SEO", "KPI", "ROI", "OKR", "MVP", "SLA",
    "USA", "US", "UK", "EU", "UN", "NASA", "BBC", "CNN", "COVID", "UTC", "GMT", "AM", "PM",
    "USD", "EUR", "BRL", "GBP", "PT", "BR", "EN", "DE", "ES", "FR", "IT", "JP", "CN",
    "SP", "RJ", "MG", "RS", "DF", "SC", "PR", "BA", "PE", "CE", "GO", "PA", "AM", "ID",
}
ACRONYM = re.compile(r"\b([A-Z]{2,6})s?\b")
ROMAN_NUMERAL = re.compile(r"^[IVXLCDM]+$")

# A visual is a diagram, a chart or a picture: a Mermaid block, a figure, an image, or an SVG
# that is not a small inline icon. Tables are not visuals for the "How to read" rule.
MERMAID_PRE = re.compile(r"<pre\b[^>]*\bclass=\"[^\"]*\bmermaid\b[^\"]*\"[^>]*>.*?</pre\s*>", re.S | re.I)
MERMAID_DIV = re.compile(r"<div\b[^>]*\bclass=\"[^\"]*\bmermaid\b[^\"]*\"[^>]*>.*?</div\s*>", re.S | re.I)
SVG_ELEMENT = re.compile(r"<svg\b.*?</svg\s*>", re.S | re.I)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
FIGURE_ELEMENT = re.compile(r"<figure\b[^>]*>.*?</figure\s*>", re.S | re.I)
MARKDOWN_IMAGE_LINE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
SMALL_ICON_SIDE = 48
VISUAL_MARK = "<x-visual></x-visual>"


def _is_decorative(head):
    """aria-hidden, role=presentation, or a declared side of 48px or less: an icon or a logo."""
    if re.search(r"\baria-hidden=\"true\"|\brole=\"(?:presentation|none)\"", head, re.I):
        return True
    side = re.search(r"\b(?:width|height)=\"(\d+)", head)
    return bool(side and int(side.group(1)) <= SMALL_ICON_SIDE)


def svg_is_visual(src):
    """An SVG counts as a visual unless it is a small inline icon or a decorative drawing."""
    head = src[: src.find(">") + 1]
    if _is_decorative(head):
        return False
    if re.search(r"\brole=\"img\"|\baria-label(?:ledby)?=", head, re.I):
        return True
    return len(src) > 400 or "<title" in src.lower()


def img_is_visual(tag):
    return not _is_decorative(tag)


def _mark_visuals(text, markdown=False):
    """Replace every visual with a marker that keeps the line count, before the text is blanked.

    A <figure> is one visual, whatever it holds, so its inner images and diagrams are dropped
    and its caption stays as the text that follows the visual."""
    def keep_lines(m, mark):
        return mark + "\n" * m.group(0).count("\n")

    def strip_inner(src):
        src = MERMAID_PRE.sub(lambda m: keep_lines(m, ""), src)
        src = MERMAID_DIV.sub(lambda m: keep_lines(m, ""), src)
        src = SVG_ELEMENT.sub(lambda m: keep_lines(m, ""), src)
        return IMG_TAG.sub(lambda m: keep_lines(m, ""), src)

    mark = "![visual](#)" if markdown else VISUAL_MARK
    if not markdown:
        text = FIGURE_ELEMENT.sub(lambda m: mark + strip_inner(m.group(0)), text)
    text = MERMAID_PRE.sub(lambda m: keep_lines(m, mark), text)
    text = MERMAID_DIV.sub(lambda m: keep_lines(m, mark), text)
    text = SVG_ELEMENT.sub(lambda m: keep_lines(m, mark if svg_is_visual(m.group(0)) else ""), text)
    text = IMG_TAG.sub(lambda m: keep_lines(m, mark if img_is_visual(m.group(0)) else ""), text)
    return text

HTML_BLOCK_TAGS = {
    "p", "div", "section", "article", "header", "footer", "main", "aside", "nav",
    "blockquote", "details", "summary", "figure", "figcaption", "ul", "ol", "dl",
    "dt", "dd", "hr", "form", "fieldset", "address", "body", "html",
}
HEADING_TAGS = {f"h{n}" for n in range(1, 7)}
HTML_EXTENSIONS = (".html", ".htm", ".xhtml")
MARKDOWN_EXTENSIONS = (".md", ".markdown", ".mdx", ".txt")
HTML_SNIFF = re.compile(
    r"(?im)^\s*<(?:!doctype\b|html\b|body\b|(?:p|div|section|article|main|header|footer|"
    r"aside|nav|h[1-6]|ul|ol|li|table|details|summary|figure|blockquote)(?:\s[^>]*)?>)"
)


@dataclass
class Finding:
    line: int
    level: str   # "problem", "warning" or "note"
    rule: str
    message: str


@dataclass
class Block:
    line: int
    text: str
    kind: str  # "heading", "para" or "item"
    level: int = 0


@dataclass
class Report:
    name: str
    lang: str = FALLBACK_LANG
    findings: list = field(default_factory=list)
    show_warnings: bool = True

    @property
    def problem_count(self):
        return sum(1 for f in self.findings if f.level == "problem")

    @property
    def warning_count(self):
        return sum(1 for f in self.findings if f.level == "warning")

    @property
    def exit_code(self):
        return 1 if self.problem_count else 0

    def lines(self):
        out = []
        for f in self.findings:
            if f.level == "warning" and not self.show_warnings:
                continue
            where = f"{self.name}:{f.line}:" if f.line else f"{self.name}:"
            out.append(f"{where} [{f.level}] {f.rule}: {f.message}")
        return out

    def render(self):
        out = self.lines()
        if self.show_warnings and self.warning_count:
            out.append(f"{self.warning_count} warnings")
        out.append(f"{self.problem_count} problems")
        return "\n".join(out) + "\n"


# ---------------------------------------------------------------- text helpers

def _blank_out(text, pattern, flags=0):
    """Replace every match with the newlines it contained, so line numbers hold."""
    return re.sub(pattern, lambda m: "\n" * m.group(0).count("\n"), text, flags=flags)


def _strip_front_matter(text):
    if not text.startswith("---\n"):
        return text
    end = re.search(r"\n---[ \t]*(?:\n|$)", text[3:])
    if not end:
        return text
    cut = 3 + end.end()
    return "\n" * text[:cut].count("\n") + text[cut:]


def clean_inline(s):
    """Reduce Markdown and inline HTML to the words the reader sees."""
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"`[^`\n]*`", "code", s)
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", s)
    s = re.sub(r"https?://\S+", "URL", s)
    s = s.replace("**", "").replace("__", "").replace("*", "")
    s = html_lib.unescape(s).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def split_sentences(text, pack=None):
    """Split a block into sentences on . ! ? and an ellipsis.

    Abbreviations of the language pack, decimals (4.6 and 4,6) and single-letter
    initials ("J. Smith") never end a sentence."""
    pack = pack or LANG_PACKS[FALLBACK_LANG]
    t = text.replace("...", "…")
    for abbr in sorted(pack["abbreviations"], key=len, reverse=True):
        t = re.sub(r"(?<!\w)" + re.escape(abbr), abbr.replace(".", "\x01"), t)
    t = re.sub(r"(?<=\d)[.,](?=\d)", lambda m: "\x01" if m.group(0) == "." else ",", t)
    t = re.sub(r"(?<!\w)([A-Z])\.(?=\s[A-Z])", lambda m: m.group(1) + "\x01", t)
    parts = re.split(r"(?<=[.!?…])\s+|(?<=[.!?…][)\"'\]])\s+", t)
    return [p.replace("\x01", ".").strip() for p in parts if p.strip()]


def count_words(s):
    return len(WORD.findall(s))


def snippet(s, n=60):
    s = s.strip()
    return s if len(s) <= n else s[:n].rstrip() + "..."


def detect_language(text_or_blocks):
    """Pick the pack whose stopwords appear most in the text. Returns a language code.

    Fewer than MIN_WORDS_FOR_DETECTION words, or a tie, returns None, and the caller
    falls back to FALLBACK_LANG with a note."""
    if isinstance(text_or_blocks, str):
        words = [w.lower() for w in WORD.findall(text_or_blocks)]
    else:
        words = [w.lower() for b in text_or_blocks for w in WORD.findall(b.text)]
    if len(words) < MIN_WORDS_FOR_DETECTION:
        return None
    scores = {code: sum(1 for w in words if w in pack["stopwords"]) for code, pack in LANG_PACKS.items()}
    best = max(scores.values())
    winners = [code for code, s in scores.items() if s == best]
    if best == 0 or len(winners) != 1:
        return None
    return winners[0]


# ---------------------------------------------------------------- parsers

def _add_visual(blocks, line):
    """Append a visual block, unless the last block is already one (a figure holding an SVG)."""
    if blocks and blocks[-1].kind == "visual":
        return
    blocks.append(Block(line, "", "visual"))


def markdown_to_blocks(text):
    text = _strip_front_matter(text)
    text = _blank_out(text, r"<!--.*?-->", re.S)
    text = _mark_visuals(text, markdown=True)
    text = _blank_out(text, r"<(script|style|pre|svg|table)\b.*?</\1\s*>", re.S | re.I)
    blocks = []
    fence = None
    cur = None

    def flush():
        nonlocal cur
        if cur and cur["parts"]:
            blocks.append(Block(cur["line"], clean_inline(" ".join(cur["parts"])), cur["kind"]))
        cur = None

    for n, raw in enumerate(text.split("\n"), 1):
        f = re.match(r"^\s*(`{3,}|~{3,})\s*(\w*)", raw)
        if f:
            if fence is None:
                fence = f.group(1)[0]
                flush()
                if f.group(2).lower() == "mermaid":
                    _add_visual(blocks, n)
                continue
            if raw.strip().startswith(fence * 3):
                fence = None
                continue
        if fence:
            continue
        line = raw.rstrip()
        if line.endswith("\\"):
            line = line[:-1]
        if not line.strip():
            flush()
            continue
        if MARKDOWN_IMAGE_LINE.match(line):
            flush()
            _add_visual(blocks, n)
            continue
        if re.match(r"^\s*\|", line) or re.match(r"^\s*([-*_]\s*){3,}$", line):
            flush()
            continue
        h = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if h:
            flush()
            blocks.append(Block(n, clean_inline(h.group(2)), "heading", len(h.group(1))))
            continue
        line = re.sub(r"^\s*>\s?", "", line)
        item = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", line)
        if item:
            flush()
            cur = {"line": n, "parts": [item.group(1)], "kind": "item"}
            continue
        if cur is None:
            cur = {"line": n, "parts": [], "kind": "para"}
        cur["parts"].append(line.strip())
    flush()
    return [b for b in blocks if b.text or b.kind == "visual"]


def html_to_blocks(text):
    text = _blank_out(text, r"<!--.*?-->", re.S)
    text = _blank_out(text, r"<head\b.*?</head\s*>", re.S | re.I)
    text = _mark_visuals(text)
    text = _blank_out(text, r"<(script|style|pre|svg|table|textarea|title)\b.*?</\1\s*>", re.S | re.I)
    text = re.sub(r"<code\b[^>]*>.*?</code\s*>", lambda m: " code " + "\n" * m.group(0).count("\n"), text, flags=re.S | re.I)
    blocks = []
    buf = []
    state = {"line": 1, "kind": "para", "level": 0, "start": None}

    def add_text(seg):
        if seg.strip() and state["start"] is None:
            state["start"] = state["line"] + seg[: len(seg) - len(seg.lstrip())].count("\n")
        buf.append(seg)

    def flush():
        joined = clean_inline(html_lib.unescape("".join(buf)))
        if joined:
            blocks.append(Block(state["start"] or state["line"], joined, state["kind"], state["level"]))
        buf.clear()
        state["kind"], state["level"], state["start"] = "para", 0, None

    pos = 0
    for m in re.finditer(r"<[^>]+>", text):
        seg = text[pos:m.start()]
        add_text(seg)
        state["line"] += seg.count("\n")
        tag = m.group(0)
        name_m = re.match(r"</?\s*([a-zA-Z][a-zA-Z0-9-]*)", tag)
        name = name_m.group(1).lower() if name_m else ""
        closing = tag.startswith("</")
        if name == "br":
            buf.append("\n")
        elif name == "x-visual":
            if not closing:
                flush()
                _add_visual(blocks, state["line"])
        elif name in HEADING_TAGS:
            flush()
            if not closing:
                state["kind"], state["level"] = "heading", int(name[1])
        elif name == "li":
            flush()
            if not closing:
                state["kind"] = "item"
        elif name in HTML_BLOCK_TAGS:
            flush()
        state["line"] += tag.count("\n")
        pos = m.end()
    add_text(text[pos:])
    flush()
    return [b for b in blocks if b.text or b.kind == "visual"]


def looks_like_html(name, text):
    """Decide by extension first. Without a known extension, sniff the first 2,000 characters:
    the file is HTML when any line starts with a doctype, <html>, <body>, or a block-level
    tag such as <p>, <div> or <h2>, with or without attributes."""
    ext = os.path.splitext(name)[1].lower()
    if ext in HTML_EXTENSIONS:
        return True
    if ext in MARKDOWN_EXTENSIONS:
        return False
    return HTML_SNIFF.search(text[:2000]) is not None


# ---------------------------------------------------------------- checks

def check_dashes(block, findings):
    t = block.text
    for i, ch in enumerate(t):
        if ch == EM_DASH:
            around = snippet(t[max(0, i - 25): i + 26], 60)
            findings.append(Finding(block.line, "problem", "dash-joiner",
                                    f"em dash ({EM_DASH}) used as a joiner: \"{around}\". Split the sentence, or use a comma, a connector or parentheses."))
        elif ch == EN_DASH:
            before = t[i - 1] if i > 0 else ""
            after = t[i + 1] if i + 1 < len(t) else ""
            if before.isdigit() and after.isdigit():
                continue
            around = snippet(t[max(0, i - 25): i + 26], 60)
            findings.append(Finding(block.line, "problem", "dash-joiner",
                                    f"en dash ({EN_DASH}) used as a joiner: \"{around}\". Split the sentence, or use a comma, a connector or parentheses."))


def check_sentences(block, sentences, max_words, max_sentences, findings):
    for s in sentences:
        n = count_words(s)
        if n > max_words:
            findings.append(Finding(block.line, "problem", "sentence-length",
                                    f"sentence has {n} words (max {max_words}): \"{snippet(s)}\". Split it at the second idea."))
    if block.kind != "heading" and len(sentences) > max_sentences:
        findings.append(Finding(block.line, "problem", "paragraph-length",
                                f"block has {len(sentences)} sentences (max {max_sentences}): \"{snippet(block.text, 40)}\". Split it at the next topic break."))


def check_backward_references(block, pack, findings):
    taken = []
    for pattern, level in pack["backward"]:
        for m in re.finditer(pattern, block.text, re.I):
            if any(m.start() < e and m.end() > s for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            hint = " (a bare word that can also be spatial, so check it)" if level == "warning" else ""
            findings.append(Finding(block.line, level, "backward-reference",
                                    f"\"{m.group(0).lower()}\" points the reader back{hint}. Name the thing again and say what it is."))


def check_bare_labels(block, pack, findings):
    seen = set()
    for m in LABEL.finditer(block.text):
        label = m.group(0)
        key = re.sub(r"\s+", " ", label)
        if m.group("code") in LABEL_ALLOWLIST or key in seen:
            continue
        seen.add(key)
        if LABEL_NAMED_AFTER.match(block.text[m.end():]):
            continue
        if m.group("code"):
            example = f"{key} (cache before deploy)" if pack is LANG_PACKS["en"] else f"{key} (cache antes do deploy)"
        else:
            example = f"{key}: copy the key to the server" if pack is LANG_PACKS["en"] else f"{key}: copiar a chave para o servidor"
        findings.append(Finding(block.line, "problem", "bare-label",
                                f"\"{key}\" has no name after it. Write what it is, for example \"{example}\"."))


def is_participle(word, passive):
    w = word.lower()
    if w in passive["not_participles"]:
        return False
    if w in passive["irregular"]:
        return True
    if len(w) < passive["min_len"]:
        return False
    for suf in passive["suffixes"]:
        if w.endswith(suf):
            stem = w[: -len(suf)]
            if passive["accent_rule"] and ACCENTED.search(stem):
                return False
            return True
    return False


def check_passive(block, sentences, pack, findings):
    passive = pack["passive"]
    gap = passive["gap_words"]
    pat = re.compile(r"\b" + passive["aux"] + r"\b((?:\s+[\wÀ-ɏ'’-]+){0," + str(gap) + r"})", re.I)
    agent = re.compile(passive["agent"], re.I)
    for s in sentences:
        hit = None
        for m in pat.finditer(s):
            following = m.group(1).split()
            for i, word in enumerate(following):
                if is_participle(word, passive):
                    hit = (m.start(), s[m.start(): m.start() + len(m.group(0).rstrip())], i)
                    break
                if not passive["gap_allowed"].match(word):
                    break
            if hit:
                break
        if not hit:
            continue
        start, phrase, idx = hit
        phrase = " ".join(phrase.split()[: idx + 2])
        tail = s[start + len(phrase): start + len(phrase) + 24]
        strength = "passive voice (agent follows)" if agent.search(tail) else "possible passive voice"
        findings.append(Finding(block.line, "warning", "passive-voice",
                                f"{strength} \"{phrase}\" in \"{snippet(s)}\". Name who does the action, unless the agent is unknown or irrelevant."))


def check_headings(block, findings):
    if block.kind == "heading" and count_words(block.text) == 1:
        findings.append(Finding(block.line, "warning", "single-word-heading",
                                f"heading \"{block.text}\" is one word. Make it a statement of what the reader will learn."))


def check_key_points(blocks, sentences_by_block, pack, findings):
    if not any(b.kind == "heading" and b.level == 2 for b in blocks):
        return
    sections = []
    current = None
    for b, sentences in zip(blocks, sentences_by_block):
        if b.kind == "heading" and b.level <= 2:
            current = {"line": b.line, "title": b.text, "ok": False} if b.level == 2 else None
            if current:
                sections.append(current)
            continue
        if current is None:
            continue
        for s in sentences:
            if s.lower().startswith(pack["key_points"]):
                current["ok"] = True
    for sec in sections:
        if not sec["ok"]:
            findings.append(Finding(sec["line"], "warning", "missing-key-point",
                                    f"H2 section \"{sec['title']}\" has no \"{pack['key_point_hint']}\" line. End it with one short sentence the reader can land on."))


def _starts_with_marker(sentence, markers):
    s = sentence.lower().lstrip("*\"“'(")
    return s.startswith(markers)


def check_visuals(blocks, sentences_by_block, pack, findings):
    """Rule 7: right after every visual comes a "How to read:" line, then one sentence of conclusion."""
    hint = pack["how_to_read_hint"]
    for i, b in enumerate(blocks):
        if b.kind != "visual":
            continue
        j = i + 1
        while j < len(blocks) and blocks[j].kind == "visual":
            j += 1
        nxt = blocks[j] if j < len(blocks) else None
        first = sentences_by_block[j][0] if nxt and sentences_by_block[j] else ""
        if nxt is None or nxt.kind == "heading" or not _starts_with_marker(first, pack["how_to_read"]):
            findings.append(Finding(b.line, "problem", "visual-without-how-to-read",
                                    f"the visual has no \"{hint}\" line right after it. Add one line that says what the "
                                    f"boxes, arrows, axes or colors mean, then one sentence of conclusion."))
            continue
        after = blocks[j + 1] if j + 1 < len(blocks) else None
        has_conclusion = len(sentences_by_block[j]) >= 2 or (after is not None and after.kind not in ("heading", "visual"))
        if not has_conclusion:
            findings.append(Finding(nxt.line, "warning", "visual-without-conclusion",
                                    f"the \"{hint}\" line has no conclusion after it. Add one sentence that says what "
                                    f"the reader should take from the visual."))


def _inside_parentheses(sentence, start, end):
    before, after = sentence[:start], sentence[end:]
    return before.count("(") > before.count(")") and ")" in after


def check_acronyms(blocks, sentences_by_block, pack, findings):
    """Full name before the acronym at its first use. Only the first mention in the body counts."""
    seen = set()
    free = GLOBAL_ACRONYMS | pack["known_acronyms"] | pack["emphasis_words"] | LABEL_ALLOWLIST
    example = "\"content delivery network (CDN)\"" if pack is LANG_PACKS["en"] else "\"nome completo (SIGLA)\""
    for b, sentences in zip(blocks, sentences_by_block):
        if b.kind in ("heading", "visual"):
            continue
        for s in sentences:
            for m in ACRONYM.finditer(s):
                a = m.group(1)
                if a in seen or a in free or ROMAN_NUMERAL.match(a):
                    continue
                seen.add(a)
                named = _inside_parentheses(s, m.start(), m.end()) or re.match(r"\s*(?:\(|:)", s[m.end():])
                if named:
                    continue
                findings.append(Finding(b.line, "warning", "acronym-without-full-name",
                                        f"acronym \"{a}\" appears before its full name in \"{snippet(s)}\". Write the "
                                        f"full name first, then the acronym in parentheses, for example {example}."))


def check_analogies(blocks, pack, findings):
    """Every analogy gets, before the next heading, one line that says where it fails."""
    analogy = [re.compile(p, re.I) for p in pack["analogy"]]
    limit = [re.compile(p, re.I) for p in pack["analogy_limit"]]
    hint = pack["analogy_limit_hint"]
    pending = []

    def close_section():
        for line, phrase in pending:
            findings.append(Finding(line, "problem", "analogy-without-limit",
                                    f"the analogy \"{phrase}\" has no line that says where it fails. Add one line "
                                    f"before the next heading: \"{hint} ...\"."))
        pending.clear()

    for b in blocks:
        if b.kind == "heading":
            close_section()
            continue
        if b.kind == "visual":
            continue
        if any(p.search(b.text) for p in limit):
            pending.clear()
            continue
        for p in analogy:
            m = p.search(b.text)
            if m:
                pending.append((b.line, snippet(b.text[m.start(): m.start() + 60], 40)))
                break
    close_section()


_HIDDEN_VERB_CACHE = {}


def _hidden_verb_pattern(pack):
    """A light verb, an optional determiner, an optional adjective, then a noun from the closed list.
    The list is closed on purpose: a suffix rule flags "take the medication" and "reach the destination"."""
    key = id(pack)
    if key not in _HIDDEN_VERB_CACHE:
        hv = pack["hidden_verb"]
        nouns = "|".join(sorted(map(re.escape, hv["nouns"]), key=len, reverse=True))
        light = (r"\b" + hv["light_verbs"] + r"(?:\s+" + hv["determiners"] + r")?(?:\s+[\wÀ-ɏ-]+)?\s+(?:" + nouns + r")\b")
        parts = [light] + ([hv["noun_first"]] if hv.get("noun_first") else [])
        _HIDDEN_VERB_CACHE[key] = re.compile("|".join(parts), re.I)
    return _HIDDEN_VERB_CACHE[key]


def check_hidden_verbs(block, sentences, pack, findings):
    pat = _hidden_verb_pattern(pack)
    nouns = pack["hidden_verb"]["nouns"]
    for s in sentences:
        for m in pat.finditer(s):
            words = m.group(0).split()
            # With an optional adjective in the pattern, make sure the match ends on a listed noun and
            # that the optional word is not itself a verb object ("made the application crash").
            if words[-1].lower().strip(".,") not in nouns:
                continue
            findings.append(Finding(block.line, "warning", "hidden-verb",
                                    f"hidden verb \"{m.group(0)}\" in \"{snippet(s)}\". Use the verb itself, "
                                    f"for example {pack['hidden_verb_hint']}."))


INSERTED_CLAUSE = re.compile(r"^(?P<head>[^,;:]{1,60}?),\s+(?P<ins>[^,;:()]{15,}?),\s+(?P<tail>\S.*)$")


def _is_clause(words, pack):
    """The inserted part is a clause when it opens with a relative or adverbial marker,
    or with a participle or gerund. A list item ("os pós e os géis") opens with none of these."""
    first = words[0].lower()
    if first in pack["clause_openers"]:
        return True
    return bool(re.search(pack["clause_opener_endings"], first))


def check_inserted_clauses(block, sentences, pack, findings):
    """A long clause between commas, between the subject and its verb, pushes them apart."""
    for s in sentences:
        m = INSERTED_CLAUSE.match(s)
        if not m:
            continue
        head_words = WORD.findall(m.group("head"))
        if not head_words or len(head_words) > 5 or head_words[0][0].isdigit():
            continue
        if head_words[0].lower() in pack["intro_words"]:
            continue
        ins_words = WORD.findall(m.group("ins"))
        n = len(ins_words)
        if n < 5 or not _is_clause(ins_words, pack):
            continue
        findings.append(Finding(block.line, "warning", "inserted-clause",
                                f"a clause of {n} words sits between commas, between the subject and its verb, in "
                                f"\"{snippet(s)}\". Move it to its own sentence, so the subject and its verb stay together."))


def lint_text(text, name="document.md", kind=None, lang="auto", max_words=DEFAULT_MAX_WORDS,
              avg_words=DEFAULT_AVG_WORDS, max_sentences=DEFAULT_MAX_SENTENCES,
              show_warnings=True):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if kind is None:
        kind = "html" if looks_like_html(name, text) else "md"
    blocks = html_to_blocks(text) if kind == "html" else markdown_to_blocks(text)
    findings = []

    if lang == "auto":
        detected = detect_language(blocks)
        if detected:
            code, how = detected, "detected"
        else:
            total = sum(count_words(b.text) for b in blocks)
            code = FALLBACK_LANG
            how = f"fallback: too few words to detect the language ({total} words). Pass --lang pt or --lang en to be sure"
    else:
        code, how = lang, "set with --lang"
    pack = LANG_PACKS[code]
    findings.append(Finding(0, "note", "language", f"{code} ({how})"))

    sentences_by_block = [split_sentences(b.text, pack) for b in blocks]
    total_words = total_sentences = 0
    for b, sentences in zip(blocks, sentences_by_block):
        check_dashes(b, findings)
        check_sentences(b, sentences, max_words, max_sentences, findings)
        check_backward_references(b, pack, findings)
        check_bare_labels(b, pack, findings)
        check_passive(b, sentences, pack, findings)
        check_headings(b, findings)
        check_hidden_verbs(b, sentences, pack, findings)
        check_inserted_clauses(b, sentences, pack, findings)
        if b.kind != "heading":
            total_words += sum(count_words(s) for s in sentences)
            total_sentences += len(sentences)
    check_key_points(blocks, sentences_by_block, pack, findings)
    check_visuals(blocks, sentences_by_block, pack, findings)
    check_acronyms(blocks, sentences_by_block, pack, findings)
    check_analogies(blocks, pack, findings)
    if total_sentences:
        avg = total_words / total_sentences
        if avg > avg_words:
            findings.append(Finding(0, "warning", "average-sentence-length",
                                    f"average sentence length is {avg:.1f} words over {total_sentences} sentences (target about 15, warn over {avg_words})."))
    order = {"note": 0, "problem": 1, "warning": 2}
    findings.sort(key=lambda f: (f.line, order[f.level]))
    return Report(name=name, lang=code, findings=findings, show_warnings=show_warnings)


# ---------------------------------------------------------------- command line

def _parse_args(argv):
    opts = {"lang": "auto", "max_words": DEFAULT_MAX_WORDS, "avg_words": DEFAULT_AVG_WORDS,
            "max_sentences": DEFAULT_MAX_SENTENCES, "show_warnings": True}
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--no-warnings":
            opts["show_warnings"] = False
        elif a == "--lang":
            i += 1
            if i >= len(argv) or argv[i] not in LANG_CHOICES:
                raise SystemExit(f"--lang takes one of: {', '.join(LANG_CHOICES)}")
            opts["lang"] = argv[i]
        elif a in ("--max-words", "--avg-words", "--max-sentences"):
            i += 1
            if i >= len(argv):
                raise SystemExit(f"{a} needs a number")
            opts[a[2:].replace("-", "_")] = int(argv[i])
        elif a in ("-h", "--help"):
            raise SystemExit(__doc__)
        else:
            files.append(a)
        i += 1
    if not files:
        raise SystemExit(__doc__)
    return files, opts


def main(argv=None):
    files, opts = _parse_args(sys.argv[1:] if argv is None else list(argv))
    problems = warnings = 0
    unreadable = 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as err:
            print(f"{path}: [problem] unreadable: cannot read file ({err.strerror or err}).")
            unreadable += 1
            continue
        report = lint_text(text, name=path, **opts)
        for line in report.lines():
            print(line)
        problems += report.problem_count
        warnings += report.warning_count
    problems += unreadable
    if opts["show_warnings"] and warnings:
        print(f"{warnings} warnings")
    print(f"{problems} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
