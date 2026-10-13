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

Warnings (reported, never fatal):
    average-sentence-length  the average over the whole document is above
                        --avg-words (default 17). The target is about 15.
    passive-voice       a heuristic, so read the line before changing it.
                        en: a form of "to be", an optional adverb, then a past
                        participle (a word ending in "ed" or an irregular form),
                        minus adjectives such as "tired" or "interested".
                        pt: a form of "ser" or "estar" (é, são, foi, foram, era,
                        eram, será, serão, está, estão, esteve, ...), then within
                        two words a participle ending in ado, ada, ados, adas,
                        ido, ida, idos or idas. A determiner in the gap ("é um
                        dado") or an accent before the ending ("rápido") means
                        it is not a participle. Nouns that end the same way
                        ("estado", "resultado", "sentido") are excluded by list.
                        In both languages, an agent marker after the participle
                        ("by", "por", "pelo") raises the confidence, and the
                        message says so.
    single-word-heading a heading that is one word. Headings should say what the
                        reader will learn.
    missing-key-point   an H2 section with no sentence that starts with a Key point
                        marker. en: "Key point", "Key takeaway", "Takeaway", "In
                        short". pt: "Ponto-chave", "Em resumo", "Resumo:", "O que
                        fica". Text before the first H2 is exempt. A document with
                        no H2 skips this check.

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

WORD = re.compile(r"[A-Za-z0-9À-ɏ][\w'’À-ɏ-]*")
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

def markdown_to_blocks(text):
    text = _strip_front_matter(text)
    text = _blank_out(text, r"<!--.*?-->", re.S)
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
        f = re.match(r"^\s*(`{3,}|~{3,})", raw)
        if f:
            if fence is None:
                fence = f.group(1)[0]
                flush()
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
    return [b for b in blocks if b.text]


def html_to_blocks(text):
    text = _blank_out(text, r"<!--.*?-->", re.S)
    text = _blank_out(text, r"<head\b.*?</head\s*>", re.S | re.I)
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
        name_m = re.match(r"</?\s*([a-zA-Z][a-zA-Z0-9]*)", tag)
        name = name_m.group(1).lower() if name_m else ""
        closing = tag.startswith("</")
        if name == "br":
            buf.append("\n")
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
    return [b for b in blocks if b.text]


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
        if b.kind != "heading":
            total_words += sum(count_words(s) for s in sentences)
            total_sentences += len(sentences)
    check_key_points(blocks, sentences_by_block, pack, findings)
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
