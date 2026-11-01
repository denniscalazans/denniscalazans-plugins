# What the clear-read lint reports

This file belongs to clear-read (`SKILL.md`, "Before you deliver"). It lists every finding the lint can report, with the rule behind each one, and the phone check for Mermaid diagrams. The lint's own docstring and `scripts/test_lint_clear_read.py` are the authority on behavior.

## How to run it

```bash
python3 scripts/lint_clear_read.py path/to/document.md
```

It reads Markdown or HTML, prints one line per finding, and ends with `N problems`. It needs only Python 3, with no extra packages. It detects the language of the text (Portuguese or English) from common words, or takes `--lang pt` or `--lang en`. Then it applies that language's word lists, which mirror the language packs in `references/`.

## Problems: fix every one

A **problem** is a rule break. The lint reports eight kinds:

- A dash used as a joiner (Rule 2).
- A sentence over 25 words (Rule 2).
- A block over 4 sentences (Rule 1).
- A backward reference (Rule 6). It points the reader back to a passage instead of repeating the thing itself.
- A bare label such as "P1" with nothing that names it (Rule 6).
- A visual with no "How to read:" line right after it (Rule 7). A visual is a Mermaid block, a figure, an image, or an SVG that is not an icon.
- An analogy with no "Where the analogy fails:" line before the next heading (Rule 5).
- A fixed label in the wrong language, such as "Key point:" in a Portuguese text (Rule 10).

## Warnings: keep the text only on purpose

A **warning** is a prompt to re-read that line. The lint reports eleven kinds:

- A possible passive (Rule 2).
- A hidden verb, such as "perform an analysis" or "realizar a verificação" (Rule 2).
- A clause of 5 or more words between commas, between the subject and its verb (Rule 2).
- An acronym whose first mention has no full name next to it (Rule 5).
- A name before its role, such as "Mayer mostrou que" (Rule 5). The sentence names no researcher, study, standard or law.
- A role with no name, such as "um pesquisador mostrou que" or "segundo a pesquisa" (Rule 5). No name, year or link appears by the end of the next sentence.
- A one-word heading (Rule 1), the kind `single-word-heading`.
- An H2 section with no "Key point:" line (Rule 1).
- A "How to read:" line with no conclusion after it (Rule 7).
- A bare "acima" in Portuguese, which can be spatial or a pointer back (Rule 6).
- An average sentence length over 17 words (Rule 2).

## The phone check for Mermaid diagrams

When the document has Mermaid diagrams, also run the phone check. A label that fits a desktop can be cut on a phone, and the lint cannot see that:

```bash
npm install --no-save mermaid@11 playwright@1   # once per working directory
npx playwright install chromium                 # once per machine, or set CHROMIUM_PATH
node scripts/check_mermaid.cjs path/to/document.html
```

It renders every diagram the way a published page does, at 390px. It fails on a cut label, a `<br/>` inside a label, a label over 25 characters, text under 12px, or sideways scroll. It reads `.md` files too (the ```mermaid fences), and `--self-test` checks the checker itself.

## The kind names, as the lint prints them

Each finding line carries its kind in brackets, so a search for the kind finds every case. The kinds are: `dash-joiner`, `sentence-length`, `paragraph-length`, `backward-reference`, `bare-label`, `visual-without-how-to-read`, `analogy-without-limit`, `label-in-wrong-language`, `passive-voice`, `hidden-verb`, `inserted-clause`, `acronym-without-full-name`, `name-before-role`, `authority-without-name`, `single-word-heading`, `missing-key-point`, `visual-without-conclusion`, `average-sentence-length`. The Portuguese "acima" warning is reported as `backward-reference` at warning level, and `language` is the note that names the detected language.
