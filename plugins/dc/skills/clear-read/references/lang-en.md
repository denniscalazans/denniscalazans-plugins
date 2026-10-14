# Language pack: English (en)

Read this file when the reader's language is English.
It adds what is specific to English on top of the eleven rules in SKILL.md.
The lint keeps its own copy of these words in `LANG_PACKS["en"]` in `scripts/lint_clear_read.py`. The two are maintained by hand, so when you change one, change the other.

Many readers of English text are reading in their second language.
So the English rules lean on short words, present tense and explicit connectors even more than the Portuguese ones.

## The standard behind the rules

The United States Plain Writing Act of 2010 requires federal agencies to write for their audience.
The Federal Plain Language Guidelines (March 2011) list the techniques.
The current edition lives on Digital.gov, adapted from PlainLanguage.gov.
The skill already carries most of the guidelines, so the table says where each one lives.

| Federal Plain Language Guidelines (heading) | Where the skill carries it |
|---|---|
| Use active voice | Rule 2 (active voice, present tense) |
| Use the simplest form of a verb; Use the present tense | Rule 2 |
| Avoid hidden verbs; Don't turn verbs into nouns | Rule 2, and the lint rule `hidden-verb` |
| Use "must" to indicate requirements | This file, "Modal verbs" |
| Use pronouns to speak directly to readers | This file, "Register" |
| Minimize abbreviations | Rule 5, and the lint rule `acronym-without-full-name` |
| Use short, simple words; Omit unnecessary words | Rule 10 and Rule 8 |
| Use the same term consistently for a specific thought or object | Rule 5 (one word, one meaning) |
| Avoid legal, foreign, and technical jargon | Rule 5 |
| Write short sentences | Rule 2 |
| Keep subject, verb, and object close together | Rule 2, and the lint rule `inserted-clause` |
| Avoid double negatives and exceptions to exceptions | This file, "Negation" |
| Place the main idea before exceptions and conditions | Rule 1 (lead with the goal) |
| Have a topic sentence; Cover only one topic in each paragraph; Write short paragraphs | Rule 1 |
| Use transition words | Rule 2 (explicit connectors) |
| Use examples; Use lists; Use tables; Consider using illustrations | Rule 3, Rule 7 and Rule 11 |
| Minimize cross-references | Rule 6 (repeat the thing, never point back) |

Sources: [Plain language guide series on Digital.gov](https://digital.gov/guides/plain-language) and the [Federal Plain Language Guidelines, 2011 edition (PDF)](https://revenue.ky.gov/DOR%20Training%20Materials/Federal%20Plain%20Language%20Guidelines.pdf).
The PDF link is a state agency's copy of the federal document, because plainlanguage.gov now redirects to Digital.gov.
The 2011 guidelines also set a limit on abbreviations: define each one at first use, and keep a document to about three.

## English-specific rules

**Present tense and active voice by default.** "The cache answers the request", not "the request is answered by the cache" and not "the cache will answer".
Use the past for history and the conditional only when the condition is real.

**Subject, verb and object close together.** A clause between commas in the middle of the sentence separates the subject from its verb, so move it to its own sentence.

- Weak: "The server, which the team installed last week, restarts every night."
- Strong: "The team installed the server last week. It restarts every night."

**A verb, not a hidden verb.** Nouns ending in -tion, -sion, -ment, -ance and -ence often hide a verb.

- Weak: "perform an analysis", "make a decision", "conduct a review", "reach a conclusion".
- Strong: "analyze", "decide", "review", "conclude".

**Modal verbs mean one thing each.**

| Word | Meaning in this skill |
|---|---|
| must | a requirement |
| should | a recommendation |
| may | permission |
| can | ability |

Never use "shall", because readers disagree on what it means.

**Full name before the acronym, at its first use.** "content delivery network (CDN)", then "CDN" alone.
Established tech terms (API, URL, PDF, HTML) need no expansion.

**Register.** Address the reader as "you".
Contractions are fine in a chat answer and in an email. Avoid them in a report or a specification, where the reader may not be native.

**Negation.** One negative at most per sentence, and say what is, not what is not.

- Weak: "It is not uncommon for the cache to fail."
- Strong: "The cache fails often."

**Short words.** Prefer the common word over the long one.
Examples: "use" over "utilize", "help" over "facilitate", "start" over "commence", "end" over "terminate", and "about" over "approximately" when the number is rounded.
This is about the form, never about the content (Rule 10): keep every idea, number, caveat and precise term.

**Numbers with a word anchor.** "7% (fewer than 1 in 10)", "about a third", "1 in 5".
Keep the exact value when it is the point.
Decimal point, as the reader expects: "4.6", not "4,6".

**Dates in words.** "3 June 2026" or "June 3, 2026", never "03/06/2026", because that form reads two ways across countries.

## Markers the lint looks for, in English

| Marker | English form |
|---|---|
| The key-point line that closes a section | "Key point:" |
| The legend line under a visual | "How to read:" |
| The line that limits an analogy | "Where the analogy fails:" |
| A label with a number | "Step 3", "Phase 2", "Part 1" (each one followed by its name) |

## Common slips in English, and the fix

| Slip | Fix |
|---|---|
| "As mentioned above", "the former", "the latter", "the aforementioned" | Name the thing again and say what it is |
| "P1 solves this" | "P1 (cache before deploy) solves this" |
| "The analysis was performed by the team" | "The team analyzed the logs" |
| "It was decided that" | "The team decided that", or "We decided that" |
| "Leverage", "utilize", "facilitate" | "use", "use", "help" |
| "crucial", "robust", "fundamental" | Cut, or keep with the source that supports the judgment |
