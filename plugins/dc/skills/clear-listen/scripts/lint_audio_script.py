#!/usr/bin/env python3
"""lint_audio_script.py: check an audio script against the clear-listen rules.

Usage: python lint_audio_script.py script.md [--max-words 20] [--part-words 800]
Exit code 1 when any problem is found.

Script format it expects: plain text, one sentence per line. Each part starts with a
line that says "Parte N de M" (or "Part N of M"). Lines starting with "#" are notes
and are ignored, except "# closing", which ends the last part before the final recall.
A script with two or more parts must have that closing, with its recall question.
Audio tags in square brackets ([short pause]) are ignored. A short script (up to 700
words) may be a single part with no marker.
"""
import re, sys

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
def opt(name, default):
    return int(args[args.index(name) + 1]) if name in args else default
MAX_WORDS = opt("--max-words", 20)
PART_WORDS = opt("--part-words", 800)   # 5 minutes at 160 words per minute: the ceiling of Rule 1
WPM = 160

raw = open(args[0], encoding="utf-8").read()
CLOSING = "\x00closing"
numbered = []   # (file line number, text), so every report points at the line in the editor
for n, l in enumerate(raw.splitlines(), 1):
    l = l.strip()
    if re.match(r"#\s*closing\b", l, re.I):
        numbered.append((n, CLOSING))
    elif l and not l.startswith("#"):
        numbered.append((n, l))
lines = [l for _, l in numbered]
problems = []
BACK = r"\b(como (eu )?(disse|vimos|falei|mencion\w+)|acima|anteriormente|o (primeiro|segundo|terceiro) (ponto|item)|as (I|we) (said|saw)|as mentioned|above)\b"
PART = re.compile(r"\b(Parte|Part) (\d+|\w+) (de|of) (\d+|\w+)\b", re.I)

parts, current = [], None
closing = None   # spoken lines after "# closing": the final recall and the takeaway
SINGLE_MAX_WORDS = 700   # a single-part audio (about 4 minutes) needs no part markers
for n, line in numbered:
    if line == CLOSING:
        current, closing = None, []
        continue
    if PART.search(line):
        current = {"start": n, "text": [], "lines": []}
        parts.append(current)
        closing = None
    spoken = re.sub(r"\[[^\]]*\]", " ", line)          # drop audio tags
    label = re.match(r"^\s*[A-Za-zÀ-ÿ]{1,20}:\s", spoken)
    spoken = re.sub(r"^\s*[A-Za-zÀ-ÿ ]{1,20}:\s", "", spoken)  # drop "Guia: " speaker labels
    said = re.findall(r"[\wÀ-ÿ'-]+", spoken)
    if label and 0 < len(said) <= 2 and "?" not in spoken:
        problems.append(f"line {n}: agreement noise or filler line in a dialogue. Answer with the point itself.")
    if current is not None:
        current["text"].append(spoken); current["lines"].append(spoken)
    elif closing is not None:
        closing.append(spoken)
    for sent in re.split(r"(?<=[.!?…])\s+", spoken):
        words = re.findall(r"[\wÀ-ÿ'-]+", sent)
        if len(words) > MAX_WORDS:
            problems.append(f"line {n}: sentence has {len(words)} words (max {MAX_WORDS}): {sent[:60]}...")
    if re.search(r"[()]", spoken):
        problems.append(f"line {n}: parentheses cannot be heard. Make the aside its own sentence.")
    if re.search(r"\d", spoken):
        problems.append(f"line {n}: digit found. Write numbers as words.")
    if re.search(r"[%&@#€$=+*/<>|]|https?:|www\.", spoken):
        problems.append(f"line {n}: symbol or URL found. Say it in words, or cut it.")
    if re.search("[\u2014\u2013]", spoken):
        problems.append(f"line {n}: dash found. Use a period or an ellipsis.")
    if re.search(BACK, spoken, re.I):
        problems.append(f"line {n}: backward reference. Say the thing again by name.")

lines = [l for l in lines if l != CLOSING]
total_words = len(re.findall(r"[\wÀ-ÿ'-]+", re.sub(r"\[[^\]]*\]", " ", " ".join(lines))))
if not parts and total_words > SINGLE_MAX_WORDS:
    problems.append(f'no part markers found in a script of {total_words} words. Start each part with "Parte um de N".')
if not parts and not any("?" in l for l in lines):
    problems.append("single-part script has no question. Add one recall question.")
for i, p in enumerate(parts, 1):
    size = len(re.findall(r"[\wÀ-ÿ'-]+", " ".join(p["text"])))
    if size > PART_WORDS:
        problems.append(f"part {i} (line {p['start']}): {size} words, about {size/WPM:.1f} min at {WPM} wpm, over {PART_WORDS} words. Split it.")
    tail = p["lines"][-6:]
    if not any("?" in l for l in tail):
        problems.append(f"part {i} (line {p['start']}): no recall question near its end.")
    if sum(l.count("?") for l in tail) > 2:
        problems.append(f"part {i} (line {p['start']}): more than two questions at its end. Keep one recall question.")
if len(parts) >= 2:
    if closing is None:
        problems.append('multi-part script has no closing recall. After the last part, add "# closing", then "Sem voltar, quais foram as ideias principais?" and the answer.')
    elif not any("?" in l for l in closing):
        problems.append('closing has no recall question. After "# closing", ask "Sem voltar, quais foram as ideias principais?" and answer it.')

words = len(re.findall(r"[\wÀ-ÿ'-]+", re.sub(r"\[[^\]]*\]", " ", " ".join(lines))))
print(f"words: {words}, about {words/WPM:.1f} min at {WPM} wpm, parts: {len(parts)}, problems: {len(problems)}")
for p in problems:
    print("  FAIL " + p)
sys.exit(1 if problems else 0)
