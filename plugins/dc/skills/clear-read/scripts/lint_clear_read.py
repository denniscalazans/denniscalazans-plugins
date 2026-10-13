#!/usr/bin/env python3
"""lint_clear_read.py: check a Markdown or HTML document against the clear-read rules.

Usage:
    python3 lint_clear_read.py FILE [FILE ...] [--max-words 25] [--avg-words 17]
                               [--max-sentences 4] [--no-warnings]

It prints one line per finding, as "path:line: [problem|warning] rule: message",
then "N problems" as the last line. The exit code is 1 when N > 0.
Warnings never change the exit code. They are prompts to re-read a passage.

Standard library only. A file ending in .html, .htm or .xhtml is read as HTML, and
one ending in .md, .markdown, .mdx or .txt as Markdown. Any other name is sniffed:
the file is HTML when a line in its first 2,000 characters starts with a doctype,
<html>, <body>, or a block-level tag such as <p>, <div> or <h2>, with or without
attributes.

Problems (they fail the run):
    dash-joiner         an em dash anywhere in prose, or an en dash that is not
                        between two digits (a range like 15-20 is fine).
    sentence-length     a sentence with more than --max-words words (default 25).
    paragraph-length    a block with more than --max-sentences sentences (default 4).
                        A list item is its own block. Table rows are skipped.
    backward-reference  "as mentioned", "as we saw", "as described above", "above"
                        used as a pointer, "earlier", "previously", "the
                        aforementioned", "the former", "the latter".
                        "above" followed by a quantity ("above 25 words") and
                        "earlier than" or "earlier version" are not flagged.
    bare-label          a label such as P1, C2 or Step 3 whose first mention in a
                        block carries no name. A label counts as named when it is
                        followed by "(", a middle dot, ":", "=", a quote or " - ".
                        Later mentions in the same block are fine. Common
                        technical tokens (H1 to H6, S3, M1, A4, F1 to F12) are
                        not labels.

Warnings (reported, never fatal):
    average-sentence-length  the average over the whole document is above
                        --avg-words (default 17). The target is about 15.
    passive-voice       a form of "to be" (am, is, are, was, were, be, been,
                        being), an optional adverb, then a past participle: a word
                        ending in "ed" or one of a short list of irregular
                        participles. This is a heuristic. Adjectives such as
                        "tired" and "interested" are excluded, but some false
                        positives remain, so read the line before changing it.
    single-word-heading a heading that is one word. Headings should say what the
                        reader will learn.
    missing-key-point   an H2 section with no sentence that starts with "Key
                        point", "Takeaway", "Key takeaway" or "Ponto-chave".
                        Text before the first H2 is exempt. A document with no H2
                        skips this check.

What the lint ignores: YAML front matter, HTML comments, fenced code blocks,
inline code (replaced by the word "code"), <script>, <style>, <pre>, <svg>,
<table> and <head> elements, Markdown table rows, link targets and raw URLs.
"""
import html as html_lib
import os
import re
import sys
from dataclasses import dataclass, field

DEFAULT_MAX_WORDS = 25
DEFAULT_AVG_WORDS = 17
DEFAULT_MAX_SENTENCES = 4

EM_DASH = "—"
EN_DASH = "–"
MIDDLE_DOT = "·"

KEY_POINT_MARKERS = ("key point", "key takeaway", "takeaway", "ponto-chave", "ponto chave")

WORD = re.compile(r"[A-Za-z0-9À-ɏ][\w'’À-ɏ-]*")

ABBREVIATIONS = (
    "e.g.", "E.g.", "i.e.", "I.e.", "etc.", "vs.", "cf.", "approx.", "ca.", "al.",
    "Dr.", "Mr.", "Mrs.", "Ms.", "St.", "No.", "Fig.", "Eq.", "Jr.", "Sr.",
    "Inc.", "Ltd.", "Co.", "pp.", "U.S.", "U.K.", "a.m.", "p.m.",
)

BE_FORMS = r"(?:am|is|are|was|were|be|been|being)"
IRREGULAR_PARTICIPLES = {
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
}
ADJECTIVE_PARTICIPLES = {
    "bored", "concerned", "delighted", "excited", "interested", "pleased", "relaxed",
    "satisfied", "scared", "surprised", "tired", "worried", "supposed", "advanced",
    "detailed", "limited", "unlimited", "united", "red", "need", "indeed", "bed",
}

LABEL_ALLOWLIST = (
    {f"H{n}" for n in range(1, 7)}
    | {"S3", "M1", "M2", "M3", "M4", "M5", "A3", "A4", "A5", "V8", "G7", "G20"}
    | {f"F{n}" for n in range(1, 13)}
)
LABEL = re.compile(
    r"\b(?:(?P<code>[A-Z]\d{1,2})|(?P<word>Step|Phase|Part|Stage|Point|Option)\s+(?P<n>\d{1,2}))\b"
)
LABEL_NAMED_AFTER = re.compile(r"^\**\s*(?:\(|" + MIDDLE_DOT + r"|:|=|\"|“|\s-\s)")

ABOVE_NOT_POINTER = (
    r"(?!\s+(?:\d|about|roughly|around|average|zero|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|the\s+(?:line|fold|limit|threshold|ceiling|floor|average|target)))"
)
EARLIER_NOT_POINTER = (
    r"(?!\s+(?:than|versions?|releases?|stud(?:y|ies)|work|drafts?|this|that|today|"
    r"in\s+the|on\s+the|at\s+the))"
)
BACKWARD_PATTERNS = [
    re.compile(
        r"\bas\s+(?:we\s+|i\s+|you\s+)?(?:mentioned|noted|discussed|explained|described|"
        r"shown|stated|saw|said|covered|outlined)(?:\s+(?:above|earlier|before|previously))?",
        re.I,
    ),
    re.compile(r"\b(?:the\s+)?aforementioned\b", re.I),
    re.compile(r"\bthe\s+former\b", re.I),
    re.compile(r"\bthe\s+latter\b", re.I),
    re.compile(r"\babove\b" + ABOVE_NOT_POINTER, re.I),
    re.compile(r"\bpreviously\b", re.I),
    re.compile(r"\bearlier\b" + EARLIER_NOT_POINTER, re.I),
]

HTML_BLOCK_TAGS = {
    "p", "div", "section", "article", "header", "footer", "main", "aside", "nav",
    "blockquote", "details", "summary", "figure", "figcaption", "ul", "ol", "dl",
    "dt", "dd", "hr", "form", "fieldset", "address", "body", "html",
}
HEADING_TAGS = {f"h{n}" for n in range(1, 7)}


@dataclass
class Finding:
    line: int
    level: str
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


def split_sentences(text):
    """Split a block into sentences on . ! ? and an ellipsis, keeping abbreviations whole."""
    t = text.replace("...", "…")
    for abbr in ABBREVIATIONS:
        t = re.sub(r"(?<!\w)" + re.escape(abbr), abbr.replace(".", "\x01"), t)
    t = re.sub(r"(?<=\d)\.(?=\d)", "\x01", t)
    t = re.sub(r"(?<!\w)([A-Z])\.(?=\s[A-Z])", lambda m: m.group(1) + "\x01", t)
    parts = re.split(r"(?<=[.!?…])\s+|(?<=[.!?…][)\"'\]])\s+", t)
    return [p.replace("\x01", ".").strip() for p in parts if p.strip()]


def count_words(s):
    return len(WORD.findall(s))


def snippet(s, n=60):
    s = s.strip()
    return s if len(s) <= n else s[:n].rstrip() + "..."


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


HTML_EXTENSIONS = (".html", ".htm", ".xhtml")
MARKDOWN_EXTENSIONS = (".md", ".markdown", ".mdx", ".txt")
HTML_SNIFF = re.compile(
    r"(?im)^\s*<(?:!doctype\b|html\b|body\b|(?:p|div|section|article|main|header|footer|"
    r"aside|nav|h[1-6]|ul|ol|li|table|details|summary|figure|blockquote)(?:\s[^>]*)?>)"
)


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


def check_backward_references(block, findings):
    taken = []
    for pat in BACKWARD_PATTERNS:
        for m in pat.finditer(block.text):
            if any(m.start() < e and m.end() > s for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            findings.append(Finding(block.line, "problem", "backward-reference",
                                    f"\"{m.group(0).lower()}\" points the reader back. Name the thing again and say what it is."))


def check_bare_labels(block, findings):
    seen = set()
    for m in LABEL.finditer(block.text):
        label = m.group(0)
        key = re.sub(r"\s+", " ", label)
        if m.group("code") in LABEL_ALLOWLIST or key in seen:
            continue
        seen.add(key)
        if LABEL_NAMED_AFTER.match(block.text[m.end():]):
            continue
        example = f"{key} (cache before deploy)" if m.group("code") else f"{key}: copy the key to the server"
        findings.append(Finding(block.line, "problem", "bare-label",
                                f"\"{key}\" has no name after it. Write what it is, for example \"{example}\"."))


def check_passive(block, sentences, findings):
    pat = re.compile(r"\b" + BE_FORMS + r"\s+(?:(\w+ly)\s+)?([A-Za-z]+)\b", re.I)
    for s in sentences:
        for m in pat.finditer(s):
            word = m.group(2).lower()
            is_participle = (word in IRREGULAR_PARTICIPLES) or (len(word) > 3 and word.endswith("ed"))
            if not is_participle or word in ADJECTIVE_PARTICIPLES:
                continue
            findings.append(Finding(block.line, "warning", "passive-voice",
                                    f"possible passive voice \"{m.group(0)}\" in \"{snippet(s)}\". Name who does the action, unless the agent is unknown or irrelevant."))
            break


def check_headings(block, findings):
    if block.kind == "heading" and count_words(block.text) == 1:
        findings.append(Finding(block.line, "warning", "single-word-heading",
                                f"heading \"{block.text}\" is one word. Make it a statement of what the reader will learn."))


def check_key_points(blocks, sentences_by_block, findings):
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
            if s.lower().startswith(KEY_POINT_MARKERS):
                current["ok"] = True
    for sec in sections:
        if not sec["ok"]:
            findings.append(Finding(sec["line"], "warning", "missing-key-point",
                                    f"H2 section \"{sec['title']}\" has no \"Key point:\" or \"Takeaway:\" line. End it with one short sentence the reader can land on."))


def lint_text(text, name="document.md", kind=None, max_words=DEFAULT_MAX_WORDS,
              avg_words=DEFAULT_AVG_WORDS, max_sentences=DEFAULT_MAX_SENTENCES,
              show_warnings=True):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if kind is None:
        kind = "html" if looks_like_html(name, text) else "md"
    blocks = html_to_blocks(text) if kind == "html" else markdown_to_blocks(text)
    findings = []
    sentences_by_block = [split_sentences(b.text) for b in blocks]
    total_words = total_sentences = 0
    for b, sentences in zip(blocks, sentences_by_block):
        check_dashes(b, findings)
        check_sentences(b, sentences, max_words, max_sentences, findings)
        check_backward_references(b, findings)
        check_bare_labels(b, findings)
        check_passive(b, sentences, findings)
        check_headings(b, findings)
        if b.kind != "heading":
            total_words += sum(count_words(s) for s in sentences)
            total_sentences += len(sentences)
    check_key_points(blocks, sentences_by_block, findings)
    if total_sentences:
        avg = total_words / total_sentences
        if avg > avg_words:
            findings.append(Finding(0, "warning", "average-sentence-length",
                                    f"average sentence length is {avg:.1f} words over {total_sentences} sentences (target about 15, warn over {avg_words})."))
    order = {"problem": 0, "warning": 1}
    findings.sort(key=lambda f: (f.line, order[f.level]))
    return Report(name=name, findings=findings, show_warnings=show_warnings)


# ---------------------------------------------------------------- command line

def _parse_args(argv):
    opts = {"max_words": DEFAULT_MAX_WORDS, "avg_words": DEFAULT_AVG_WORDS,
            "max_sentences": DEFAULT_MAX_SENTENCES, "show_warnings": True}
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--no-warnings":
            opts["show_warnings"] = False
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
