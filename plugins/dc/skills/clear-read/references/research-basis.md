# Research basis for the clear-read rules

This file holds the evidence behind the clear-read method. SKILL.md gives the rules; this file explains why each one exists and where it comes from. Read it when a rule needs justifying, when someone pushes back, or when deciding how to bend a rule in an edge case.

The reader clear-read serves is intelligent and works in IT, but loses focus easily (ADHD tendencies), reads English as a second language, and is often tired or in a noisy place. That profile sits at the meeting point of several research areas. They converge on a consistent set of moves: short connected sentences, one idea per unit, front-loaded structure, defined terms, concrete examples, visual chunking, and reduced memory load.

The evidence comes from seven areas, drawn from a literature review across ADHD and reading, dyslexia and cognitive accessibility, plain-language standards, second-language reading, cognitive load theory, readability measurement, and technical writing.

## Quick map: which evidence backs which rule

- Rule 1 (structure, lead with the goal, small blocks, one sentence per line): COGA front-loading and chunking; Federal Plain Language headings; Mayer signaling and segmenting; BDA short blocks.
- Rule 2 (sentence length, connectors, subject-verb, no em dashes): plain-language 15-word target; STE sentence ceilings; COGA no nested clauses; Federal transition words.
- Rule 3 (problem plus counter-pattern): instructional-design worked-example practice.
- Rule 4 (no assumed domain knowledge): COGA clear words; plain-language define-your-terms.
- Rule 5 (jargon then term; one word, one meaning): COGA acronym-on-first-use; ASD-STE100 one word one meaning; L2 vocabulary-frequency research.
- Rule 6 (teach on the way; do not rely on memory): COGA Objective 6 (working memory); Federal cross-reference warning.
- Rule 7 (visuals): BDA flow charts; Mayer multimedia, but watch the redundancy effect.
- Rule 8 (depth in small chunks): Mayer segmenting; cognitive load theory.
- Rule 9 (calm tone, screen reading): screen-versus-audio reading research.
- Rule 10 (simple English, numbers as words, dates, bold not italics): ADHD figurative-language difficulty; COGA numbers guidance; BDA emphasis guidance.
- Rule 11 (procedures and code): COGA separate-each-instruction; STE one instruction per step; Google goal-before-action; Microsoft step limits.

## 1. ADHD and reading

The core finding is that the struggle is rarely about intelligence. It is about holding a coherent mental picture of the text over time, which is limited by working memory and attention control.

A 2025 eye-tracking study of irony in adults with ADHD found they were as accurate as controls but paid an extra processing cost (longer reading times), and that higher working-memory capacity was what let them match controls' speed. This is the basis for every rule that lowers memory load: small chunks, repeated definitions, and the do-not-rely-on-memory rule.

Related work shows adults with ADHD are slower with figurative language such as metaphors, idioms, and proverbs. This directly supports the literal-language rule in Rule 10.

Practitioner guidance adds: state the purpose before reading, summarize each section, and convert prose to visuals. In a writing skill these become built-in scaffolds: lead with the goal (Rule 1), Key point recaps (Rule 1), and diagrams or outlines (Rule 7).

Certainty note: the working-memory bottleneck and figurative-language difficulty are well supported. Much of the rest is practitioner advice, not controlled trials, so treat it as reasonable but lower-certainty.

## 2. Dyslexia and cognitive accessibility

The reader profile overlaps with common reading difficulties, so two recognized guides apply.

The British Dyslexia Association Dyslexia Style Guide (2023) recommends, for content and structure: short simple sentences; active voice; concise text with no long dense paragraphs; bullet points and numbering instead of continuous prose; regular section headings; and flow charts for procedures. It also gives a specific emphasis rule: avoid underlining and italics, because they make text run together and crowd, and use bold for emphasis instead. That is the basis for the bold-not-italics rule in Rule 10. Its typography items (font, color, spacing) are out of scope for a skill that controls text and markup, not visual styling.

The W3C COGA "Making Content Usable" guidance is the richest directly usable source, because it is written for people who control content and markup. Key patterns the skill adopts:

- 4.4.1 Use clear words: prefer the most common words; remove vague fillers; explain uncommon terms nearby. (Rules 4, 5.)
- 4.4.2 Simple tense and voice: present tense, active voice, put the aim of the sentence at the start. (Rule 1 lead-with-goal, Rule 2.)
- 4.4.3 Avoid nested clauses and double negatives. (Rule 2.)
- 4.4.5 Keep text succinct: one topic per paragraph, one point per sentence, break a paragraph over about 50 words. (Rule 1 small blocks, Rule 2.)
- 4.4.9 Separate each instruction, including obvious steps; put conditional steps in an if/then table. (Rule 11.)
- 4.4.13 Reinforce numbers with words and explain what a number means. (Rule 10.)
- Objective 6, do not rely on memory: typical working memory holds about 7 items, but an impaired one may hold only 1 to 4, so minimize cross-references and restate needed context. (Rule 6.)

## 3. Plain-language standards

ISO 24495-1:2023 is the international plain-language standard. It defines plain language by reader outcomes: the reader can find what they need, understand it, and use it. The practical lesson for clear-read is that clarity is not only sentence-level. Findability matters too, through useful headings and an order that matches the reader's questions. This supports the heading and arc rules.

The U.S. Federal Plain Language Guidelines add concrete, adoptable items: average sentence length 15 to 20 words; put the topic sentence up front so readers do not hold information in their heads before reaching the point; use transition words; one topic per short paragraph; use "must" for requirements; and use plenty of useful headings, lists, and examples. They also warn that cross-references overtax short-term memory, which reinforces Rule 6. Statement and question-and-answer headings are called especially helpful, which supports the message-heading rule.

## 4. Second-language reading

L2 reading is slower and more effortful than first-language reading, with higher working-memory demand, because both languages are partly active at once. So the ADHD load and the L2 load compound in this reader, which means reducing load matters doubly.

Vocabulary frequency dominates L2 comprehension: high and mid-frequency word knowledge predicts comprehension, and rare or unfamiliar words draw extra attention and slow reading. This is the empirical basis for preferring common words and glossing any rare term at once (Rules 4, 5).

ASD-STE100 Simplified Technical English (Issue 9, 2025) is the most mature controlled language for non-native technical readers. Directly relevant rules: about 20 words per sentence for procedures and 25 for descriptive text; one instruction per step; one topic per paragraph; active voice and simple tenses; and one word, one meaning, meaning you pick one term for a concept and never swap synonyms (for example always "start", never also "begin" or "initiate"). The one-word-one-meaning discipline is the basis for that addition to Rule 5; the per-sentence ceilings support Rule 2; one instruction per step supports Rule 11.

Caveat: STE was designed for readers with very limited English and can feel stilted. The clear-read reader is an intelligent professional, so borrow STE's discipline and consistency, not its rigid dictionary or flat tone.

## 5. Cognitive load theory

Cognitive load theory (Sweller) and Mayer's multimedia principles give the theoretical backbone.

- Segmenting: breaking material into learner-paced chunks reliably lowers load and improves comprehension, including for second-language readers. Supports Rule 8 and the small-block rule.
- Signaling: cueing the essential through headings and highlights reduces wasted load. Supports message headings and Key point lines.
- Coherence: exclude extraneous words and decoration. Supports cutting anything that does not serve the goal.
- Redundancy effect, important and double-edged: presenting the same information in two competing streams at once can increase load and hurt learning. So a diagram or a Key point line must add structure or compress, never simply restate the prose. This is a caution on Rule 7 and the recaps in Rule 1.
- Split-attention: when a diagram and its explanation must be understood together, keep them adjacent.

## 6. Readability measurement, and why not to chase a score

Readability formulas (Flesch Reading Ease, Flesch-Kincaid, Gunning Fog, SMOG, and similar) mostly reduce to sentence length plus word length. Their limits are well evidenced and matter for this skill:

- They do not measure comprehension. They ignore order, coherence, and prior knowledge. Research found that rewriting only to lower a grade level did not improve understanding.
- They are inconsistent. The same text can score several grade levels apart across formulas.
- They break on short sentences, lists, fragments, and code, which is exactly what clear-read produces. So a score on clear-read output is unreliable.
- A 2025 study found most formulas, including Flesch-Kincaid, correlate poorly with human readability judgments, while a language-model judge did substantially better.

Practical stance for the skill: any readability check is a loose floor-check only (flag sentences over the ceiling, flag likely-rare words, flag long paragraphs), never a target. The real test is comprehension. A cloze test (delete every fifth to seventh word; about 60% correct means readable) or a recall check beats any formula. Since the skill runs on a language model, disciplined rule-based self-review is itself a better judge than a formula.

## 7. Technical and instructional writing

The Google developer documentation style guide and the Microsoft Writing Style Guide converge with the above and add procedure craft:

- State the goal before the action in a step ("to start a new document, click File then New"), not the reverse. This is the basis for goal-before-action in Rule 11 and lead-with-goal in Rule 1.
- One action per numbered step; introduce a procedure with a one-line "what you are about to do"; state action then result; limit a procedure to about seven steps. (Rule 11.)
- Prescriptive voice: "must" for required, "can" for optional, "might" for possible; avoid the ambiguous "should".
- Lead with what matters; front-load the keywords the reader is looking for. (Rule 1.)
- Accessibility for a global audience: never put an instruction only inside an image; give a text equivalent; use real text, not images of text or code; avoid idioms; write the month in words to avoid date ambiguity. (Rules 10, 11.)

## Trade-offs to weigh, not ignore

- One sentence per line versus cohesion. Forcing a blank line after every sentence fragments the text into a wall, which is the failure clear-read fixes with tight blocks (Rule 1). Keep sentences on their own line inside small blocks, with blank lines only between topics.
- Connectors versus one point per sentence. Use connector words between two short sentences to show the logical link, but do not stack clauses inside one sentence.
- Readability score versus comprehension. Covered above: floor-check only, never a target.
- Controlled vocabulary versus an intelligent reader. Adopt STE's discipline, not its stilted register, because the reader is an expert, just attention-limited and non-native.
- Diagrams and recaps versus the redundancy effect. They must add structure or compress, not duplicate the prose.

## Certainty and caveats

- High certainty: vocabulary frequency drives L2 comprehension; segmenting lowers load; readability formulas do not measure comprehension; working-memory limits in ADHD; the structural rules from BDA, COGA, STE, and plain-language standards.
- Lower certainty or heuristic: the specific numbers (about 1,500 common words, five choices per screen, 50-word paragraphs, 1 to 4 memory items, 60 to 70 characters per line). These are sensible expert defaults, not hard constants, and should be tuned by testing with the real reader.
- The skill controls text and markup, not visual CSS, so typography, color, and font advice is out of scope except where it shows up in markup (bold versus italic, lists, headings, line breaks).

## Key sources

- Kyriacou, Rummelhoff and Koder (University of Oslo), Journal of Attention Disorders, 2025; 29(9):724 to 744. Eye-tracking study of irony in adults with ADHD.
- W3C, Making Content Usable for People with Cognitive and Learning Disabilities (COGA Working Group Note), especially the clear-words, separate-instruction, numbers, and memory objectives.
- British Dyslexia Association, Dyslexia Style Guide, 2023.
- ISO 24495-1:2023, Plain language, Part 1: Governing principles and guidelines.
- U.S. Federal Plain Language Guidelines (plainlanguage.gov).
- ASD-STE100 Simplified Technical English, Issue 9, 2025 (53 writing rules; about 900 approved words; one word, one meaning).
- Sweller (cognitive load theory) and Mayer (multimedia principles: segmenting, signaling, coherence, redundancy, split-attention).
- Cachola, Khashabi and Dredze (Johns Hopkins), "Evaluating the Evaluators", arXiv:2508.19221, 2025, on the weak correlation between readability formulas and human judgment.
- Google developer documentation style guide; Microsoft Writing Style Guide.
- Masrai (2019) and related work on L2 vocabulary frequency and reading comprehension.
