#!/usr/bin/env python3
"""lint_audio_script.py: check an audio script against the clear-listen rules.

Usage: python lint_audio_script.py script.md [--max-words 20] [--part-chars 4800] [--conversa]
Exit code 1 when any problem is found.

Script format it expects: plain text, one sentence per line. Each part starts with a
line that says "Parte N de M" (or "Part N of M"). Lines starting with "#" are notes
and are ignored, except "# closing", which ends the last part before the final recall.
A script with more than one part must end with a closing recall question about the whole
audio: a question after "# closing", or a line that says "Sem voltar" or "Without going
back" and asks a question (Rule 6). Audio tags in square brackets ([short pause]) are
ignored. A short script (up to 700 words) may be a single part with no marker. In a
dialogue, each line starts with the role and a colon (Guia:); the check
key-after-voice-change reads those labels.

--conversa lints one turn of a live voice conversation instead of a script (SKILL.md,
"Conversation by voice"). A turn is read by the engine as it is, so the mode fails on any
square bracket, any part marker, any bare ordinal ("Primeiro,", "Second,"), any numbered or
bulleted line, and any heading. It also fails a turn of more than 6 sentences, and a turn of
more than 3 sentences that does not end with a question. The sentence checks (length,
parentheses, digits, symbols, dashes, backward references, relative risk) run in both modes.

As a module: lint(text, max_words=20, part_chars=4800, conversa=False) returns the list of problems.
Tests: test_lint_audio_script.py in this directory.
"""
import re, sys

MAX_WORDS = 20
PART_CHARS = 4800          # about 5 minutes at 160 words per minute
SINGLE_MAX_WORDS = 700     # a single-part audio (about 4 minutes) needs no part markers
CLOSING = "\x00closing"
BACK = r"\b(como (eu )?(disse|vimos|falei|mencion\w+)|acima|anteriormente|o (primeiro|segundo|terceiro) (ponto|item)|as (I|we) (said|saw)|as mentioned|above)\b"
PART = re.compile(r"\b(Parte|Part) (\d+|\w+) (de|of) (\d+|\w+)\b", re.I)
CLOSING_RECALL = re.compile(r"\b(sem voltar|without going back)\b", re.I)  # Rule 6, the proven part
TAG = re.compile(r"\[([^\]]*)\]")

# The Delivery intents table of SKILL.md. Keep both in sync.
TONE_INTENTS = {"warm", "curious", "serious", "thoughtful", "inviting", "surprised", "amused"}
PAUSE_INTENTS = {"pause short", "pause long", "pause recall"}
LEGACY_INTENTS = {"short pause": "pause short", "long pause": "pause long"}  # rule 6 of the intents
NEUTRAL_INTENTS = TONE_INTENTS | PAUSE_INTENTS | {"key"} | set(LEGACY_INTENTS)
INTENT_PREFIXES = ("say:", "stress:", "perform:")
SLOW_INTENTS = {"key", "pause long"}

# Rule 20: a relative risk needs its base in the same sentence.
RELATIVE_RISK = re.compile(
    r"\b(o dobro|o triplo|dobrou|dobraram|triplicou|triplicaram|quadruplicou|\w+ vezes (mais|menos)|por cento (maior|menor|a mais|a menos)"
    r"|twice as|\w+ times (as|more|higher|lower)|percent (higher|lower|more|less))\b", re.I)
RISK_BASE = re.compile(r"\b(em cada|de cada|in every|out of)\b", re.I)

# Conversation by voice: a turn has no structure the ear cannot hear.
TURN_MAX_SENTENCES = 6      # rule 1 of the section
TURN_FREE_SENTENCES = 3     # up to this many, no closing question is needed (rule 8)
SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")
BARE_ORDINAL = re.compile(
    r"^(?:(?:o|a|em)\s+)?(?:primeir[oa]|segund[oa]|terceir[oa]|quart[oa]|quint[oa]"
    r"|first|second|third|fourth|fifth)(?:\s+lugar)?\s*[,.:]", re.I)
LIST_LINE = re.compile(r"^\s*(\d+[.)]|[-*•])\s+")
HEADING_LINE = re.compile(r"^\s*#")


def intent_name(tag):
    """Normalize the inside of a bracket tag: '[Pause Long ]' -> 'pause long'."""
    return re.sub(r"\s+", " ", tag.strip().lower())


def is_neutral_intent(tag):
    """True when the tag is in the Delivery intents table, or has one of its three prefixed forms."""
    name = intent_name(tag)
    return name in NEUTRAL_INTENTS or name.startswith(INTENT_PREFIXES)


def canonical_intent(tag):
    name = intent_name(tag)
    return LEGACY_INTENTS.get(name, name)


def words_of(text):
    return re.findall(r"[\wÀ-ÿ'-]+", text)


def sentence_checks(n, spoken, max_words, problems):
    """The checks on one spoken line that hold for a script and for a conversation turn alike."""
    for sent in SENTENCE_END.split(spoken):
        words = words_of(sent)
        if len(words) > max_words:
            problems.append(f"line {n}: sentence has {len(words)} words (max {max_words}): {sent[:60]}...")
        if RELATIVE_RISK.search(sent) and not RISK_BASE.search(sent):
            problems.append(f"line {n}: relative risk without its base. Say it as \"treze em cada cem\": {sent[:60]}...")
    if re.search(r"[()]", spoken):
        problems.append(f"line {n}: parentheses cannot be heard. Make the aside its own sentence.")
    if re.search(r"\d", spoken):
        problems.append(f"line {n}: digit found. Write numbers as words.")
    if re.search(r"[%&@#€$=+*/<>|]|https?:|www\.", spoken):
        problems.append(f"line {n}: symbol or URL found. Say it in words, or cut it.")
    if re.search("[—–]", spoken):
        problems.append(f"line {n}: dash found. Use a period or an ellipsis.")
    if re.search(BACK, spoken, re.I):
        problems.append(f"line {n}: backward reference. Say the thing again by name.")


def analyze_turn(text, max_words=MAX_WORDS):
    """Lint one turn of a voice conversation (SKILL.md, "Conversation by voice").

    Nothing is dropped before the checks: the engine reads every character of the turn,
    so a note, a tag or a list marker is a problem, not a format. Returns the same shape
    as analyze(), plus "sentences".
    """
    problems = []
    sentences = []
    lines = [l.rstrip() for l in text.splitlines()]
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        if HEADING_LINE.match(line):
            problems.append(f"line {n}: heading or note line in a voice turn. Nothing here is unspoken; say the turn in prose.")
            continue
        if LIST_LINE.match(line):
            problems.append(f"line {n}: list line. Never number in a conversation; one step per turn, the next when the person asks.")
        if "[" in line or "]" in line:
            problems.append(f"line {n}: square bracket in a voice turn. The engine reads the mark or drops it; punctuation is the only sound control.")
        if PART.search(line):
            problems.append(f'line {n}: part marker in a voice turn. A turn has no parts; announce structure only through content.')
        if "`" in line or re.search(r"(^|\s)_\w[^_]*\w_(\s|[.,;!?]|$)", line) or re.search(r"\*\w", line):
            problems.append(f"line {n}: markdown mark in a voice turn (italics, bold or backticks). The engine reads the mark or drops it; punctuation is the only sound control.")
        # The marks are already reported; look at the words the engine would say around them.
        spoken = LIST_LINE.sub("", re.sub(r"[\[\]]", " ", TAG.sub(" ", line))).strip()
        for sent in SENTENCE_END.split(spoken):
            if not words_of(sent):
                continue
            sentences.append(sent.strip())
            if BARE_ORDINAL.match(sent.strip()):
                problems.append(f"line {n}: bare ordinal. Never number in a conversation: {sent.strip()[:60]}")
        sentence_checks(n, spoken, max_words, problems)
    count = len(sentences)
    if count > TURN_MAX_SENTENCES:
        problems.append(f"turn has {count} sentences (max {TURN_MAX_SENTENCES}). Answer in three, six at most, and offer the rest.")
    if count > TURN_FREE_SENTENCES and not sentences[-1].endswith("?"):
        problems.append(f"turn has {count} sentences and does not end with a question. Past three sentences, give the turn back with a short question.")
    words = len(words_of(" ".join(sentences)))
    return {"problems": problems, "words": words, "parts": 0, "sentences": count}


def analyze(text, max_words=MAX_WORDS, part_chars=PART_CHARS, conversa=False):
    """Lint a neutral script. Returns {"problems": [...], "words": int, "parts": int}.
    With conversa=True, lint one conversation turn instead (analyze_turn)."""
    if conversa:
        return analyze_turn(text, max_words)
    lines = [CLOSING if re.match(r"#\s*closing\b", l.strip(), re.I) else l.strip() for l in text.splitlines()]
    lines = [l for l in lines if l and (l == CLOSING or not l.startswith("#"))]
    problems = []

    parts, current = [], None
    speaker = None   # the role of the last spoken line that had a label (Rule 13)
    closing_lines = []   # spoken lines after "# closing"
    closing_recall = False   # a "Sem voltar ...?" line anywhere in the script
    after_closing = False
    for n, line in enumerate(lines, 1):
        if line == CLOSING:
            current, after_closing = None, True
            continue
        if PART.search(line):
            current = {"start": n, "text": [], "lines": [], "raw": []}
            parts.append(current)
        tags = TAG.findall(line)
        for tag in tags:
            if not is_neutral_intent(tag):
                problems.append(f"line {n}: [{tag.strip()}] is not in the Delivery intents table. Use the table, or fix the sentence.")
        spoken = TAG.sub(" ", line)                        # drop audio tags
        label = re.match(r"^\s*[A-Za-zÀ-ÿ]{1,20}:\s", spoken)
        spoken = re.sub(r"^\s*[A-Za-zÀ-ÿ ]{1,20}:\s", "", spoken)  # drop "Guia: " speaker labels
        said = words_of(spoken)
        if label and 0 < len(said) <= 2 and "?" not in spoken:
            problems.append(f"line {n}: agreement noise or filler line in a dialogue. Answer with the point itself.")
        # Rule 13 (key-after-voice-change): the listener loses the first three seconds after a
        # voice change, so the first line of a new speaker is a transition, never the key point.
        if label and said:
            role = label.group(0).strip().rstrip(":")
            if speaker is not None and role != speaker and "key" in (canonical_intent(t) for t in tags):
                problems.append(f"line {n}: [key] on the first line after a voice change ({speaker} to {role}). "
                                "Say a transition sentence first; the listener loses the first three seconds (key-after-voice-change).")
            speaker = role
        if current is not None:
            current["text"].append(spoken); current["lines"].append(spoken); current["raw"].append(line)
        elif after_closing:
            closing_lines.append(spoken)
        if CLOSING_RECALL.search(spoken) and "?" in spoken:
            closing_recall = True
        sentence_checks(n, spoken, max_words, problems)

    lines = [l for l in lines if l != CLOSING]
    total_words = len(words_of(TAG.sub(" ", " ".join(lines))))
    if not parts and total_words > SINGLE_MAX_WORDS:
        problems.append(f'no part markers found in a script of {total_words} words. Start each part with "Parte um de N".')
    if not parts and not any("?" in l for l in lines):
        problems.append("single-part script has no question. Add one recall question.")
    for i, p in enumerate(parts, 1):
        size = len(" ".join(p["text"]))
        if size > part_chars:
            problems.append(f"part {i} (line {p['start']}): {size} characters, over {part_chars}. Split it.")
        tail = p["lines"][-6:]
        if not any("?" in l for l in tail):
            problems.append(f"part {i} (line {p['start']}): no recall question near its end.")
        if sum(l.count("?") for l in tail) > 2:
            problems.append(f"part {i} (line {p['start']}): more than two questions at its end. Keep one recall question.")
    # Rule 6: the closing recall about the whole audio is the proven part of the rule, so every
    # script of more than one part must have it. A single-part audio has its one question already.
    if len(parts) > 1 and not closing_recall and not any("?" in l for l in closing_lines):
        problems.append(f"script has {len(parts)} parts but no closing recall question about the whole audio. "
                        'End with a "# closing" note and "Sem voltar, quais foram as ideias principais?" (Rule 6).')

    # Intent checks per part. A script with no markers is one part.
    units = [(i, p["start"], p["raw"]) for i, p in enumerate(parts, 1)] if parts else [(1, 1, lines)]
    for i, start, raw in units:
        intents = [canonical_intent(t) for l in raw for t in TAG.findall(l)]
        keys = intents.count("key")
        if keys > 1:
            problems.append(f"part {i} (line {start}): {keys} [key] intents. Keep one key point per part.")
        opening = []
        for k, l in enumerate(raw):
            opening.extend(canonical_intent(t) for t in TAG.findall(l))
            is_marker = k == 0 and bool(PART.search(l))
            if words_of(TAG.sub(" ", l)) and not is_marker:
                break
        slow = sorted(SLOW_INTENTS & set(opening))
        if slow:
            problems.append(f"part {i} (line {start}): opens with a slow direction ({', '.join(f'[{s}]' for s in slow)}). Open at a normal pace.")

    return {"problems": problems, "words": total_words, "parts": len(parts)}


def lint(text, max_words=MAX_WORDS, part_chars=PART_CHARS, conversa=False):
    """Return the list of problems in a neutral script. Empty list means it passes."""
    return analyze(text, max_words, part_chars, conversa)["problems"]


def main(argv):
    args = list(argv)
    if not args:
        sys.exit(__doc__)
    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    max_words = opt("--max-words", MAX_WORDS)
    part_chars = opt("--part-chars", PART_CHARS)
    conversa = "--conversa" in args
    with open(args[0], encoding="utf-8") as f:
        raw = f.read()
    result = analyze(raw, max_words, part_chars, conversa)
    words, problems = result["words"], result["problems"]
    if conversa:
        print(f"words: {words}, sentences: {result['sentences']}, about {round(words / 160 * 60)} seconds at 160 wpm, problems: {len(problems)}")
    else:
        print(f"words: {words}, about {words/160:.1f} min at 160 wpm, parts: {result['parts']}, problems: {len(problems)}")
    for p in problems:
        print("  FAIL " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
