#!/usr/bin/env python3
"""
lint_guide.py: confere um guia Clear Read (um arquivo HTML em PT-BR) contra as
regras de escrita do projeto. Só usa a biblioteca padrão do Python 3.

Uso:
  python3 lint_guide.py <guia.html> [--json] [--max-sentence 25] [--avg-sentence 17]

Saída em texto: uma linha por problema, no formato "REGRA  [local]  mensagem",
depois os avisos, uma linha de estatísticas e, por fim, "N problemas, M avisos".
O script sai com código 1 quando N > 0, e com 0 nos outros casos.
Saída com --json: um objeto {"problems": [...], "warnings": [...], "stats": {...}}.

Como o HTML é lido:
- O parser é o html.parser da biblioteca padrão, montado em uma árvore simples.
- O conteúdo de script, style, svg, audio, pre, code, template, nav e select é
  ignorado. Um <code> dentro de uma frase vira o marcador "(código)", para a
  contagem de palavras não quebrar.
- São blocos de texto: p, li, h1 a h4, td, th, summary, figcaption, dt, dd,
  button e label. Texto solto dentro de div, span ou section vira um bloco
  "solto" (é assim que os marcadores "Conceito 1 de 4" aparecem nos guias).
- Um <br> dentro de um bloco é uma quebra de linha. A frase termina em ".", "!",
  "?" ou "…" seguidos de espaço e de algo que não é letra minúscula, ou numa
  quebra de linha. Abreviações ("p. ex.", "Dr.", "etc."), números decimais e
  URLs não quebram a frase.
- Cada bloco pertence a uma seção lógica: a <section> com id que o envolve ou,
  quando não há <section>, o trecho entre um <h2> e o próximo. Um marcador de
  progresso logo antes de um título pertence à seção desse título.
- Uma seção de conceito é uma <section> com id no formato c1, c2, p1, p2 (...)
  ou uma seção que contém um bloco curto "Conceito N de M".

Regras (P = problema, faz o script sair com 1; W = aviso):
  P travessao                 travessão (U+2014), meia-risca (U+2013) ou barra horizontal (U+2015) no texto visível; uma meia-risca sozinha numa célula sem letras é aceito.
  P frase-longa               frase com mais de --max-sentence palavras (padrão 25).
  W media-alta                média de palavras por frase, nos blocos de prosa, acima de --avg-sentence (padrão 17).
  P bloco-longo               <p> ou <li> com mais de 4 linhas (quebras <br> + 1, ou frases quando não há <br>); ignora blocos dentro de <pre> e blocos cuja classe é mono, code, pre ou sample (ou começa ou termina com isso e um hífen).
  P referencia-para-tras      "como vimos", "como já vimos", "anteriormente", "mencionad...", "primeira ideia", "segunda ideia", "segundo ponto", "terceiro ponto", "já citado", "citado acima", "visto acima", "o ponto anterior", "a seção anterior".
  W acima                     a palavra "acima" sozinha (pode ser espacial), com a frase; "acima de" seguido de número não conta.
  P rotulo-vazio              rótulo nu como P1 ou C2 sem o significado logo depois (" ·", " (" ou ":").
  P sem-ponto-chave           seção de conceito sem uma linha que começa com "Ponto-chave".
  P contexto-extra-sem-fonte  bloco "Contexto extra" (classe com "contexto" ou "extra", ou texto que começa assim) sem link http dentro dele nem nos irmãos até o próximo título.
  P analogia-sem-falha        "analogia" ou "Pense nisso como" numa seção sem "Onde a analogia falha".
  P prequestao-sem-resposta   pergunta N da seção "Antes de ler" sem um "Resposta da pergunta N" no corpo.
  W sem-prequestoes           não existe seção cujo título contém "Antes de ler" (regra extra, só aviso).
  P sem-marcador              seção de conceito sem "Conceito N de M", "Parte N de M" ou "Degrau N".
  P sem-recapitule            nenhum bloco com "Recapitule de cabeça" ou "Sem voltar no texto".
  P sem-teste                 nenhum título com "Teste rápido".
  P secao-sem-id              <h2> fora de uma <section id="..."> e sem id próprio (as âncoras servem às perguntas de revisão).
  P visual-sem-como-ler       svg grande (viewBox ou width acima de 100), pre.mermaid, figure ou table sem uma linha "Como ler" na mesma seção. Uma table só conta quando tem algum número e fica fora das seções cujo título contém Termos, Checagem, Quem é quem, Fontes, Leitura adicional ou Relacionado.
  W visual-sem-conclusao      o mesmo visual sem um bloco de texto logo depois (o bloco seguinte não existe ou é um título).
  W nominalizacao             frase com 2 ou mais palavras diferentes terminadas em -ção, -ções, -mento ou -mentos; ignora palavras em data-term, em <code> e uma lista curta de substantivos que não vêm de verbo (momento, suplemento, alimento, medicamento, documento, elemento, instrumento, argumento, segmento, apartamento, departamento).
  W intercalada               frase com mais de 18 palavras e uma oração entre vírgulas começando com que, como, quando, embora, apesar ou porque.
  W sigla-sem-nome            primeira ocorrência de uma sigla (2 a 6 letras maiúsculas) fora da lista conhecida (siglas de tecnologia, palavras-chave de SQL, GDPR, LGPD, CEO, PIB, STF, TSE, EUA, OMS, FDA, NHS etc.), sem "(" logo antes ou logo depois, e fora de um parêntese aberto ("(Instant Voice Cloning, IVC)" é aceito).
  Estatísticas                blocos, frases, palavras, média por frase (prosa), frase mais longa, seções de conceito, visuais.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "track", "wbr",
        "area", "base", "col", "embed", "param"}
IGNORE = {"script", "style", "svg", "audio", "video", "pre", "template",
          "noscript", "select", "option", "textarea", "iframe", "canvas",
          "nav", "head", "title", "math", "object", "datalist"}
BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th",
              "summary", "figcaption", "dt", "dd", "button", "label",
              "caption", "legend"}
INLINE = {"a", "b", "strong", "em", "i", "span", "small", "abbr", "sup", "sub",
          "mark", "time", "u", "s", "kbd", "q", "cite", "var", "samp", "del",
          "ins", "bdi", "bdo", "data", "font", "tt", "big", "img", "wbr"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
PROSE_TAGS = {"p", "li", "dd", "dt", "summary", "figcaption", "loose"}
BLOCK_LEVEL = {"p", "div", "ul", "ol", "table", "section", "blockquote", "pre",
               "dl", "figure", "details", "header", "footer", "main",
               "article", "aside", "nav", "hr", "li", "dt", "dd", "tr", "td",
               "th", "h1", "h2", "h3", "h4", "h5", "h6", "form", "fieldset",
               "thead", "tbody", "tfoot"}

DASHES = {"\u2014": "U+2014 (travessão)", "\u2013": "U+2013 (meia-risca)",
          "\u2015": "U+2015 (barra horizontal)"}

BACKREFS = ["como vimos", "como já vimos", "anteriormente", "mencionad",
            "primeira ideia", "segunda ideia", "segundo ponto",
            "terceiro ponto", "já citado", "citado acima", "visto acima",
            "o ponto anterior", "a seção anterior"]

ABBR = {"p", "ex", "dr", "dra", "sr", "sra", "srta", "prof", "profa", "etc",
        "art", "n", "nº", "no", "num", "vol", "fig", "cap", "ed", "séc", "sec",
        "min", "máx", "max", "aprox", "obs", "pág", "pg", "tel", "av", "al",
        "vs", "www", "inc", "ltd", "ltda", "co", "jr", "st", "mr", "mrs", "ms",
        "cf", "ca", "approx", "e.g", "i.e", "a.c", "d.c", "ph.d", "u.s"}

KNOWN_SIGLAS = {"API", "SQL", "CSV", "JSON", "HTML", "CSS", "URL", "PDF", "SEK",
                "EUR", "USD", "BBC", "MP3", "SVG", "AI", "IA", "TTS", "UI", "UX",
                "ID", "OK", "PT", "BR", "EN", "DE", "RAM", "CPU", "GPU", "GB",
                "MB", "KB", "HTTP", "HTTPS", "JS", "TS", "SDK", "LLM", "ETF",
                "BTC", "NFT", "DNS",
                # acréscimos de uso corrente, que ninguém precisa abrir
                "EUA", "UE", "ONU", "DNA", "II", "III", "IV", "VI", "VII",
                "VIII", "IX", "XI", "XII",
                # palavras-chave de SQL mostradas como texto
                "SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "LIMIT",
                "JOIN", "COUNT", "SUM", "AVG", "AS", "ON", "AND", "OR", "NOT",
                "NULL",
                # siglas correntes em português e em notícias
                "GDPR", "LGPD", "CEO", "CFO", "PIB", "IPCA", "STF", "TSE", "PL",
                "MDB", "PSD", "OMS", "FDA", "NHS"}

# Tabelas só contam como visual fora das seções de apoio (título contém uma destas palavras)
TABLE_SKIP_HEADINGS = ("termos", "checagem", "quem é quem", "fontes",
                       "leitura adicional", "relacionado")
# Blocos de código ou de amostra não contam para bloco-longo
BLOCO_LONGO_SKIP_CLASSES = ("mono", "code", "pre", "sample")

NOMINAL_SUFFIX = re.compile(r"(ção|ções|mento|mentos)$")
NOMINAL_IGNORE = {"não", "momento", "suplemento", "suplementos", "alimento",
                  "alimentos", "medicamento", "medicamentos", "documento",
                  "documentos", "elemento", "elementos", "instrumento",
                  "instrumentos", "argumento", "argumentos", "segmento",
                  "segmentos", "apartamento", "apartamentos", "departamento",
                  "departamentos"}

MARKER_RE = re.compile(r"\b(?:Conceito|Parte)\s+\d+\s+de\s+\d+\b|\bDegrau\s+\d+\b")
CONCEITO_RE = re.compile(r"\bConceito\s+\d+\s+de\s+\d+\b")
MARKER_ONLY_RE = re.compile(
    r"^(?:Conceito|Parte|Degrau)\s+\d+(?:\s+de\s+\d+)?(?:\s*[·:\-].*)?$", re.S)
MAIN_ID_RE = re.compile(r"^(c|p)\d+$")
ROTULO_RE = re.compile(r"(?<![\w-])([PC]\d)(?![\w-])(?!\s*[·(:])")
SIGLA_RE = re.compile(r"(?<![\w/.\-])([A-Z]{2,6})s?(?![\w\-])")
INTERCALADA_RE = re.compile(
    r",\s*(que|como|quando|embora|apesar|porque)\b[^,]*,", re.I)
ACIMA_RE = re.compile(r"\bacima\b(?!\s+d[eao]s?\s+\d)", re.I)
SENT_END_RE = re.compile(r"[.!?…]+[\"”»')\]]*\s+(?=\S)")
ENUM_RE = re.compile(r"^\s*(?:\d{1,3}|[a-zA-Z])[.)]\s+")
WORD_RE = re.compile(r"\w", re.U)
DATA_URI_RE = re.compile(r"data:[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]{64,}")


# ---------------------------------------------------------------------------
# Árvore HTML
# ---------------------------------------------------------------------------

class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = {}
        for k, v in attrs:
            if k not in self.attrs:
                self.attrs[k] = v if v is not None else ""
        self.children = []
        self.parent = parent

    def get(self, name):
        return self.attrs.get(name) or ""

    def classes(self):
        return self.get("class").lower().split()

    def ancestors(self):
        n = self.parent
        while n is not None:
            yield n
            n = n.parent

    def descendants(self):
        for ch in self.children:
            if isinstance(ch, Node):
                yield ch
                yield from ch.descendants()

    def all_text(self):
        parts = []
        for ch in self.children:
            if isinstance(ch, str):
                parts.append(ch)
            else:
                parts.append(ch.all_text())
        return "".join(parts)


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None)
        self.cur = self.root

    # fecha um <p> aberto quando chega um elemento de bloco
    def _close_open_p(self):
        n = self.cur
        while n is not None and n.tag in INLINE:
            n = n.parent
        if n is not None and n.tag == "p":
            self.cur = n.parent

    def _close_if_open(self, tags, stop):
        n = self.cur
        while n is not None and n is not self.root and n.tag not in stop:
            if n.tag in tags:
                self.cur = n.parent
                return
            n = n.parent

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in BLOCK_LEVEL:
            self._close_open_p()
        if tag == "li":
            self._close_if_open({"li"}, {"ul", "ol", "menu"})
        elif tag in ("dt", "dd"):
            self._close_if_open({"dt", "dd"}, {"dl"})
        elif tag in ("td", "th"):
            self._close_if_open({"td", "th"}, {"tr", "table"})
        elif tag == "tr":
            self._close_if_open({"tr"}, {"table", "thead", "tbody", "tfoot"})
        elif tag == "option":
            self._close_if_open({"option"}, {"select", "datalist"})
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in VOID:
            return
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is None or n is self.root:
            return
        self.cur = n.parent

    def handle_data(self, data):
        if data:
            self.cur.children.append(data)


def parse_html(src):
    src = DATA_URI_RE.sub("data:stripped", src)
    tb = TreeBuilder()
    tb.feed(src)
    tb.close()
    return tb.root


# ---------------------------------------------------------------------------
# Extração de blocos, visuais e seções
# ---------------------------------------------------------------------------

class Block:
    __slots__ = ("el", "tag", "text", "lines", "index", "key", "is_heading",
                 "list_depth", "kind")

    def __init__(self, el, tag, text, kind):
        self.el = el
        self.tag = tag
        self.kind = kind
        self.text = text
        self.lines = [l for l in (x.strip() for x in text.split("\n")) if l]
        self.index = -1
        self.key = None
        self.is_heading = kind == "block" and tag in HEADINGS
        self.list_depth = sum(1 for a in el.ancestors() if a.tag in ("ul", "ol"))

    def short(self, n=40):
        s = " ".join(self.text.split())
        return s if len(s) <= n else s[:n - 1] + "…"


def normalize(text):
    text = text.replace("\xa0", " ").replace("\r", "")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    lines = [l.strip() for l in text.split("\n")]
    out, prev_blank = [], True
    for l in lines:
        if l:
            out.append(l)
            prev_blank = False
        elif not prev_blank:
            out.append("")
            prev_blank = True
    return "\n".join(out).strip()


def svg_is_visual(el):
    for a in el.ancestors():
        if a.tag in ("button", "a"):
            return False
    size = None
    vb = el.get("viewbox").replace(",", " ").split()
    if len(vb) == 4:
        try:
            size = max(float(vb[2]), float(vb[3]))
        except ValueError:
            size = None
    if size is None:
        w = el.get("width").lower().replace("px", "").strip()
        try:
            size = float(w)
        except ValueError:
            size = None
    if size is not None:
        return size > 100
    return bool(el.get("role") == "img" or el.get("aria-label"))


class Extractor:
    def __init__(self, root):
        self.root = root
        self.blocks = []
        self.visuals = []
        self.term_words = set()
        self.h2_index = 0

    def run(self):
        self.walk(self.root, False)
        self._attach_markers()
        return self

    def key_for(self, el):
        for a in [el] + list(el.ancestors()):
            if a.tag == "section":
                sid = a.get("id")
                if sid:
                    return ("sec", sid)
                break
        return ("h2", self.h2_index)

    def emit(self, el, text, kind):
        tag = el.tag if kind == "block" else "loose"
        b = Block(el, tag, text, kind)
        if b.is_heading and el.tag == "h2":
            self.h2_index += 1
        b.key = self.key_for(el)
        b.index = len(self.blocks)
        self.blocks.append(b)

    def walk(self, el, in_figure):
        buf = []

        def flush():
            text = normalize("".join(buf))
            buf.clear()
            if text:
                self.emit(el, text, "block" if el.tag in BLOCK_TAGS else "loose")

        def glued_label(kids, i):
            # Um rótulo inline colado no texto seguinte ("<span>6 de julho</span>A agência")
            # depende de CSS para virar linha. Aqui ele vira uma quebra de linha.
            if i + 1 >= len(kids):
                return False
            own = kids[i].all_text()
            nxt = kids[i + 1]
            if isinstance(nxt, Node):
                if nxt.tag not in INLINE:
                    return False
                nxt = nxt.all_text()
            return bool(own and own[-1].isalnum() and nxt
                        and (nxt[0].isupper() or nxt[0].isdigit()))

        def inline(node):
            kids = node.children
            for i, ch in enumerate(kids):
                if isinstance(ch, str):
                    buf.append(ch)
                    continue
                t = ch.tag
                if t == "br":
                    buf.append("\n")
                    continue
                if t == "code":
                    buf.append("(código)")
                    continue
                if t == "pre":
                    flush()
                    if "mermaid" in ch.classes():
                        self.add_visual("mermaid", ch, in_figure)
                    continue
                if t == "svg":
                    if svg_is_visual(ch):
                        flush()
                        self.add_visual("svg", ch, in_figure)
                    continue
                if t in IGNORE:
                    continue
                if t in INLINE:
                    if "data-term" in ch.attrs:
                        for w in re.findall(r"\w+", ch.all_text()):
                            self.term_words.add(w.lower())
                    inline(ch)
                    if glued_label(kids, i):
                        buf.append("\n")
                    continue
                flush()
                if t == "figure":
                    v = self.add_visual("figure", ch, in_figure)
                    self.walk(ch, True)
                    v["end"] = len(self.blocks)
                elif t == "table":
                    v = self.add_visual("table", ch, in_figure)
                    self.walk(ch, in_figure)
                    if v is not None:
                        v["end"] = len(self.blocks)
                else:
                    self.walk(ch, in_figure)

        inline(el)
        flush()

    def add_visual(self, kind, el, in_figure):
        if in_figure:
            return None
        v = {"kind": kind, "el": el, "key": self.key_for(el),
             "start": len(self.blocks), "end": len(self.blocks)}
        self.visuals.append(v)
        return v

    def _attach_markers(self):
        bl = self.blocks
        for i, b in enumerate(bl):
            if (i + 1 < len(bl) and MARKER_ONLY_RE.match(b.text.strip())
                    and bl[i + 1].is_heading and bl[i + 1].key != b.key):
                b.key = bl[i + 1].key


class Group:
    """Uma seção lógica: a <section> com id, ou o trecho de um <h2> ao próximo."""

    def __init__(self, key):
        self.key = key
        self.blocks = []
        self.heading = None
        self.sec_id = key[1] if key[0] == "sec" else None

    def add(self, b):
        self.blocks.append(b)
        if b.is_heading:
            if self.heading is None or (b.tag == "h2" and self.heading.tag != "h2"):
                self.heading = b
                if self.sec_id is None and b.tag == "h2" and b.el.get("id"):
                    self.sec_id = b.el.get("id")

    @property
    def heading_text(self):
        return self.heading.text.replace("\n", " ") if self.heading else ""

    def text(self):
        return "\n".join(b.text for b in self.blocks)

    def location(self):
        if self.heading:
            short = " ".join(self.heading_text.split())
            short = short if len(short) <= 40 else short[:39] + "…"
        elif self.blocks:
            short = self.blocks[0].short()
        else:
            short = ""
        return ("#%s %s" % (self.sec_id, short)).strip() if self.sec_id else short

    def is_main_concept(self):
        if self.key[0] == "sec" and MAIN_ID_RE.match(self.key[1]):
            return True
        for b in self.blocks:
            if (b.is_heading or count_words(b.text) <= 8) and CONCEITO_RE.search(b.text):
                return True
        return False


def build_groups(blocks):
    groups, order = {}, []
    for b in blocks:
        g = groups.get(b.key)
        if g is None:
            g = groups[b.key] = Group(b.key)
            order.append(g)
        g.add(b)
    return order, groups


# ---------------------------------------------------------------------------
# Frases e palavras
# ---------------------------------------------------------------------------

def count_words(s):
    return sum(1 for t in s.split() if WORD_RE.search(t))


def split_sentences(line):
    line = ENUM_RE.sub("", line)
    parts, start = [], 0
    for m in SENT_END_RE.finditer(line):
        before = line[start:m.start()]
        last = before.split()[-1] if before.split() else ""
        core = last.lower().rstrip(".")
        nxt = line[m.end()]
        if nxt.islower():
            continue
        if core in ABBR or (len(core) == 1 and core.isalpha()):
            continue
        if m.group(0)[0] == "." and last[-1:].isdigit() and nxt.isdigit():
            continue
        parts.append(line[start:m.start() + len(m.group(0).rstrip())])
        start = m.end()
    parts.append(line[start:])
    return [p.strip() for p in parts if p.strip()]


def has_http_link(node):
    for d in node.descendants():
        if d.tag == "a" and d.get("href").lower().startswith("http"):
            return True
    return False


# ---------------------------------------------------------------------------
# Linter
# ---------------------------------------------------------------------------

class Linter:
    def __init__(self, root, max_sentence=25, avg_sentence=17.0):
        self.max_sentence = max_sentence
        self.avg_sentence = avg_sentence
        self.ex = Extractor(root).run()
        self.blocks = self.ex.blocks
        self.order, self.groups = build_groups(self.blocks)
        self.visuals = [v for v in self.ex.visuals if self.visual_counts(v)]
        self.problems = []
        self.warnings = []
        self.stats = {}
        self._seen_siglas = set()

    # -- utilidades ---------------------------------------------------------

    def visual_counts(self, v):
        """Uma tabela só é visual quando tem algum número e fica fora das seções de apoio."""
        if v["kind"] != "table":
            return True
        if not re.search(r"\d", v["el"].all_text()):
            return False
        heads = []
        g = self.groups.get(v["key"])
        if g is not None and g.heading is not None:
            heads.append(g.heading_text.lower())
        for b in reversed(self.blocks[:v["start"]]):
            if b.is_heading:
                heads.append(b.text.lower())
                break
        return not any(k in h for h in heads for k in TABLE_SKIP_HEADINGS)

    def loc(self, b):
        g = self.groups.get(b.key)
        if g is not None and g.heading is not None:
            return g.location()
        return b.short()

    def add(self, level, rule, b_or_group, message):
        if isinstance(b_or_group, Group):
            g = b_or_group
            loc, sec, head, snippet = g.location(), g.sec_id, g.heading_text, ""
        else:
            b = b_or_group
            g = self.groups.get(b.key)
            loc = self.loc(b)
            sec = g.sec_id if g else None
            head = g.heading_text if g else ""
            snippet = b.short(80)
        item = {"rule": rule, "location": loc, "message": message,
                "section": sec, "heading": " ".join(head.split()), "block": snippet}
        (self.problems if level == "P" else self.warnings).append(item)

    @staticmethod
    def snip(s, n=70):
        s = " ".join(s.split())
        return s if len(s) <= n else s[:n - 1] + "…"

    # -- execução -----------------------------------------------------------

    def run(self):
        self.check_blocks()
        self.check_groups()
        self.check_global()
        return self

    def check_blocks(self):
        n_sent = n_words = 0
        prose_sent = prose_words = 0
        longest = (0, "", "")
        for b in self.blocks:
            self.check_travessao(b)
            self.check_bloco_longo(b)
            self.check_contexto_extra(b)
            for line in b.lines:
                for sent in split_sentences(line):
                    n = count_words(sent)
                    if n == 0:
                        continue
                    n_sent += 1
                    n_words += n
                    if b.tag in PROSE_TAGS:
                        prose_sent += 1
                        prose_words += n
                    if n > longest[0]:
                        longest = (n, self.snip(sent), self.loc(b))
                    self.check_sentence(b, sent, n)
        avg = round(prose_words / prose_sent, 1) if prose_sent else 0.0
        self.stats.update({
            "blocos": len(self.blocks),
            "frases": n_sent,
            "palavras": n_words,
            "media_frase": avg,
            "frase_mais_longa": {"palavras": longest[0], "frase": longest[1],
                                 "local": longest[2]},
        })
        if avg > self.avg_sentence:
            self.warnings.append({
                "rule": "media-alta", "location": "guia inteiro",
                "message": "média de %.1f palavras por frase (limite %.0f)" % (avg, self.avg_sentence),
                "section": None, "heading": "", "block": ""})

    def check_travessao(self, b):
        found = [d for d in DASHES if d in b.text]
        if not found:
            return
        if b.tag in ("td", "th") and not re.search(r"[^\W\d_]", b.text):
            return
        for d in found:
            pos = b.text.find(d)
            ctx = self.snip(b.text[max(0, pos - 30):pos + 30], 60)
            self.add("P", "travessao", b, "%s em «%s»" % (DASHES[d], ctx))

    def check_bloco_longo(self, b):
        if b.tag not in ("p", "li"):
            return
        if any(c == k or c.startswith(k + "-") or c.endswith("-" + k) for c in b.el.classes() for k in BLOCO_LONGO_SKIP_CLASSES):
            return
        if any(a.tag == "pre" for a in b.el.ancestors()):
            return
        if len(b.lines) > 1:
            n = len(b.lines)
            how = "linhas"
        else:
            n = sum(len(split_sentences(l)) for l in b.lines)
            how = "frases sem <br>"
        if n > 4:
            self.add("P", "bloco-longo", b, "%d %s: «%s»" % (n, how, b.short(60)))

    def check_contexto_extra(self, b):
        el = b.el
        by_class = any(("contexto" in c or "extra" in c) for c in el.classes())
        by_text = re.match(r"\s*contexto extra\b", b.text, re.I) is not None
        if not (by_class or by_text):
            return
        if not hasattr(self, "_ctx_seen"):
            self._ctx_seen = set()
        if id(el) in self._ctx_seen:
            return
        self._ctx_seen.add(id(el))
        if has_http_link(el):
            return
        parent = el.parent
        if parent is not None:
            started = False
            for sib in parent.children:
                if sib is el:
                    started = True
                    continue
                if not started or isinstance(sib, str):
                    continue
                if sib.tag in HEADINGS:
                    break
                if has_http_link(sib):
                    return
        self.add("P", "contexto-extra-sem-fonte", b,
                 "sem link http no bloco nem até o próximo título: «%s»" % b.short(60))

    def check_sentence(self, b, sent, n):
        low = sent.lower()
        if n > self.max_sentence:
            self.add("P", "frase-longa", b, "%d palavras: «%s»" % (n, self.snip(sent)))
        hits = [p for p in BACKREFS if p in low]
        if hits:
            self.add("P", "referencia-para-tras", b,
                     "%s em «%s»" % (", ".join('"%s"' % h for h in hits), self.snip(sent)))
        elif ACIMA_RE.search(sent):
            self.add("W", "acima", b, "«%s»" % self.snip(sent))
        for m in ROTULO_RE.finditer(sent):
            self.add("P", "rotulo-vazio", b,
                     "rótulo %s sem significado em «%s»" % (m.group(1), self.snip(sent)))
        nominal, stems = [], set()
        for w in re.findall(r"\w+", sent):
            lw = w.lower()
            if (NOMINAL_SUFFIX.search(lw) and lw not in NOMINAL_IGNORE
                    and lw not in self.ex.term_words):
                stem = re.sub(r"ções$", "ção", re.sub(r"mentos$", "mento", lw))
                if stem not in stems:
                    stems.add(stem)
                    nominal.append(w)
        if len(nominal) >= 2:
            self.add("W", "nominalizacao", b,
                     "%s em «%s»" % (", ".join(nominal), self.snip(sent)))
        if n > 18 and INTERCALADA_RE.search(sent):
            self.add("W", "intercalada", b, "%d palavras: «%s»" % (n, self.snip(sent)))
        for m in SIGLA_RE.finditer(sent):
            sig = m.group(1)
            if sig in KNOWN_SIGLAS or sig in self._seen_siglas:
                continue
            self._seen_siglas.add(sig)
            before = sent[:m.start()].rstrip().rstrip("\"'“”«»")
            after = sent[m.end():].lstrip().lstrip("\"'“”«»")
            if before.rstrip().endswith("(") or after.lstrip().startswith("("):
                continue
            # dentro de um parêntese ainda aberto: "(Instant Voice Cloning, IVC)"
            if before.count("(") > before.count(")"):
                continue
            self.add("W", "sigla-sem-nome", b,
                     "%s aparece pela primeira vez sem o nome por extenso: «%s»" % (sig, self.snip(sent)))

    def check_groups(self):
        n_main = 0
        for g in self.order:
            text = g.text()
            low = text.lower()
            if g.is_main_concept():
                n_main += 1
                if not any(l.lower().startswith("ponto-chave") for b in g.blocks for l in b.lines):
                    self.add("P", "sem-ponto-chave", g, "seção de conceito sem linha \"Ponto-chave:\"")
                if not MARKER_RE.search(text):
                    self.add("P", "sem-marcador", g,
                             "seção de conceito sem marcador \"Conceito N de M\"")
            if ("analogia" in low or "pense nisso como" in low) and "onde a analogia falha" not in low:
                self.add("P", "analogia-sem-falha", g,
                         "a seção usa uma analogia e não tem \"Onde a analogia falha\"")
            if "antes de ler" in g.heading_text.lower():
                self.check_prequestoes(g)
            for b in g.blocks:
                if b.tag == "h2" and not g.key[0] == "sec" and not b.el.get("id"):
                    self.add("P", "secao-sem-id", b,
                             "<h2> sem id e fora de <section id>: «%s»" % b.short(60))
        self.stats["secoes_conceito"] = n_main
        self.stats["visuais"] = len(self.visuals)
        self.check_visuals()

    def check_prequestoes(self, g):
        self._has_pre = True
        text = g.text()
        ns = {int(x) for x in re.findall(r"\bPergunta\s+(\d+)", text)}
        if not ns:
            ns = {int(m.group(1)) for b in g.blocks
                  for m in [re.match(r"\s*(\d+)[.)]\s", b.text)] if m}
        if not ns:
            lis = [b for b in g.blocks if b.tag == "li"]
            if lis:
                d = min(b.list_depth for b in lis)
                ns = set(range(1, sum(1 for b in lis if b.list_depth == d) + 1))
        if not ns:
            self.add("W", "sem-prequestoes", g, "não achei perguntas numeradas na seção \"Antes de ler\"")
            return
        body = "\n".join(b.text for b in self.blocks).lower()
        for n in sorted(ns):
            if ("resposta da pergunta %d" % n) not in body:
                self.add("P", "prequestao-sem-resposta", g,
                         "a pergunta %d não tem \"Resposta da pergunta %d\" no corpo" % (n, n))

    def check_visuals(self):
        for v in self.visuals:
            g = self.groups.get(v["key"])
            if g is None:
                g = Group(v["key"])
            has_como_ler = any(re.match(r"como ler\b", l, re.I)
                               for b in g.blocks for l in b.lines)
            label = "%s" % v["kind"]
            if not has_como_ler:
                self.add("P", "visual-sem-como-ler", g,
                         "%s sem uma linha \"Como ler:\" na mesma seção" % label)
            nxt = None
            if v["kind"] == "figure":
                inner = self.blocks[v["start"]:v["end"]]
                caps = [b for b in inner if b.tag == "figcaption"]
                nxt = caps[-1] if caps else None
            if nxt is None and v["end"] < len(self.blocks):
                nxt = self.blocks[v["end"]]
            if nxt is None or nxt.is_heading:
                self.add("W", "visual-sem-conclusao", g,
                         "%s sem um bloco de texto logo depois" % label)

    def check_global(self):
        full = "\n".join(b.text for b in self.blocks).lower()
        if "recapitule de cabeça" not in full and "sem voltar no texto" not in full:
            self.problems.append({"rule": "sem-recapitule", "location": "guia inteiro",
                                  "message": "nenhum bloco com \"Recapitule de cabeça\" ou \"Sem voltar no texto\"",
                                  "section": None, "heading": "", "block": ""})
        if not any(b.is_heading and "teste rápido" in b.text.lower() for b in self.blocks):
            self.problems.append({"rule": "sem-teste", "location": "guia inteiro",
                                  "message": "nenhum título com \"Teste rápido\"",
                                  "section": None, "heading": "", "block": ""})
        if not getattr(self, "_has_pre", False):
            self.warnings.append({"rule": "sem-prequestoes", "location": "guia inteiro",
                                  "message": "nenhuma seção com título \"Antes de ler\"",
                                  "section": None, "heading": "", "block": ""})


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------

def lint_file(path, max_sentence=25, avg_sentence=17.0):
    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()
    return lint_source(src, max_sentence, avg_sentence)


def lint_source(src, max_sentence=25, avg_sentence=17.0):
    root = parse_html(src)
    return Linter(root, max_sentence, avg_sentence).run()


def format_text(lt):
    out = []
    for p in lt.problems:
        out.append("%s  [%s]  %s" % (p["rule"], p["location"], p["message"]))
    for w in lt.warnings:
        out.append("%s  [%s]  %s" % (w["rule"], w["location"], w["message"]))
    s = lt.stats
    fl = s.get("frase_mais_longa", {})
    out.append("estatísticas: %d blocos, %d frases, %d palavras, média %.1f palavras por frase, "
               "frase mais longa %d palavras, %d seções de conceito, %d visuais"
               % (s.get("blocos", 0), s.get("frases", 0), s.get("palavras", 0),
                  s.get("media_frase", 0.0), fl.get("palavras", 0),
                  s.get("secoes_conceito", 0), s.get("visuais", 0)))
    out.append("%d problemas, %d avisos" % (len(lt.problems), len(lt.warnings)))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere um guia Clear Read contra as regras de escrita.")
    ap.add_argument("guide", help="arquivo HTML do guia")
    ap.add_argument("--json", action="store_true", help="imprime JSON em vez de texto")
    ap.add_argument("--max-sentence", type=int, default=25, help="máximo de palavras por frase (padrão 25)")
    ap.add_argument("--avg-sentence", type=float, default=17.0, help="média máxima de palavras por frase (padrão 17)")
    args = ap.parse_args(argv)

    lt = lint_file(args.guide, args.max_sentence, args.avg_sentence)
    if args.json:
        print(json.dumps({"problems": lt.problems, "warnings": lt.warnings,
                          "stats": lt.stats}, ensure_ascii=False, indent=1))
    else:
        print(format_text(lt))
    return 1 if lt.problems else 0


if __name__ == "__main__":
    sys.exit(main())
