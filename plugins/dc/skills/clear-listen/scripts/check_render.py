#!/usr/bin/env python3
"""check_render.py: fail if a neutral intent is left in a rendered text.

Usage: python check_render.py rendered.txt [--allow curious,warm]
Exit code 1 when any neutral intent of the clear-listen table is still in the text.

Run it on the output of Phase 4 (the text for one engine, or the plain text), never on
the neutral script. An engine's own marks are not neutral intents and pass. Use --allow
for a tone word that the profile keeps as the engine's own mark, on purpose.
Lines starting with "#" are producer notes and are skipped.

As a module: check(text, allow=()) returns the list of problems.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_audio_script import TAG, intent_name, is_neutral_intent  # noqa: E402


def check(text, allow=()):
    """Return one problem per neutral intent left in the rendered text."""
    allowed = {intent_name(a) for a in allow}
    problems = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        for tag in TAG.findall(line):
            name = intent_name(tag)
            if not is_neutral_intent(tag) or name in allowed or name.split(":")[0] in allowed:
                continue
            problems.append(f"line {n}: neutral intent [{tag.strip()}] left in the rendered text. Map it, degrade it, or drop it on purpose.")
    return problems


def main(argv):
    args = list(argv)
    if not args:
        sys.exit(__doc__)
    allow = args[args.index("--allow") + 1].split(",") if "--allow" in args else []
    with open(args[0], encoding="utf-8") as f:
        text = f.read()
    problems = check(text, allow)
    print(f"rendered text: {len(text.splitlines())} lines, neutral intents left: {len(problems)}")
    for p in problems:
        print("  FAIL " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
