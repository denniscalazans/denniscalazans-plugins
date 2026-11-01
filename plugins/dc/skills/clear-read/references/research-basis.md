# Research basis for the clear-read rules

This file holds the evidence behind the clear-read method. SKILL.md gives the rules; this file explains why each one exists and where it comes from. Read it when a rule needs justifying, when someone pushes back, or when deciding how to bend a rule in an edge case.

The reader clear-read serves is intelligent and works in IT, but loses focus easily (ADHD tendencies), reads at work in a second language (English) and at home in the native one (Brazilian Portuguese), and is often tired or in a noisy place. The skill writes in whichever language the reader asks for, so the evidence below is about reading under load, not about one language. That profile sits at the meeting point of several research areas. They converge on a consistent set of moves: short connected sentences, one idea per unit, front-loaded structure, defined terms, concrete examples, visual chunking, and reduced memory load.

The evidence comes from seven areas, drawn from a literature review across ADHD and reading, dyslexia and cognitive accessibility, plain-language standards, second-language reading, cognitive load theory, readability measurement, and technical writing. Section 8 adds the evidence verified on 13 October 2026, with effect sizes and DOIs.

## Evidence map, checked at the source

This table is the answer to "where does this rule come from?". One row per claim. Verdict: **holds** (the source says it), **holds with a limit** (the source says it, with a narrower scope than the rule), **contradicted** (the source says the opposite; the old sentence is under Retired), **practice** (expert guidance or the project's own tests, no controlled study), **untested** (no study found). Checked: the date someone read the source for this map, or "carried" for a source carried over from an earlier version and not re-read. Access: what was read, the full text, the abstract, or a summary page. The checking history is in the plugin's `references/investigacao-2026-11/pesquisa-conferida.md`.

| Rule | Claim, as the skill makes it | Verdict | Source | Certainty | Checked | Access |
|---|---|---|---|---|---|---|
| Rule 1 | Small blocks and segmenting lower the load | holds with a limit | Rey and others 2019, Educational Psychology Review 31(2), doi:10.1007/s10648-018-9456-4; retention d = 0.32, transfer d = 0.36; only 4 of 88 comparisons in pure audio | high | 2026-11-01 | full text |
| Rule 1 | Guidance before each stage helps adults with and without ADHD | holds with a limit (analogy) | Brann and Sidi 2025, Learning and Instruction 95:102051, doi:10.1016/j.learninstruc.2024.102051; 210 adults, the scaffold was self-regulation prompts | medium | 2026-11-01 | abstract |
| Rule 1 | Lead with the goal, message headings, front-loading | practice | W3C COGA, Making Content Usable; Federal Plain Language Guidelines | medium | carried | summary page |
| Rule 2 | Explicit connectors speed up causal understanding | holds with a limit | Cevasco 2009, The Spanish Journal of Psychology 12(1), PMID 19476219; one connective ("but"), 36 students, a speed gain, not accuracy | medium | 2026-11-01 | abstract |
| Rule 2 | Removing discourse markers from a lecture lowers comprehension | holds with a limit | Flowerdew and Tauroza 1995, Studies in Second Language Acquisition 17(4), doi:10.1017/S0272263100014406; 63 second-language listeners; organization markers, not causal connectives | medium | 2026-11-01 | abstract |
| Rule 2 | 15-word target, 25-word ceiling, active voice | practice (standards) | ISO 24495-1:2023; ASD-STE100 Issue 9; Federal Plain Language Guidelines | medium | carried | summary page |
| Rule 3 | A problem is paired with the pattern that works | practice | Instructional-design worked-example practice; the project's cold-reader tests | low | carried | summary page |
| Rule 4 | Assume no domain knowledge | practice | W3C COGA clear words; plain-language define-your-terms | medium | carried | summary page |
| Rule 5 | Unknown names hurt second-language listening | holds with a limit | Kobeleva 2012 (details in pesquisa-conferida.md, section 4.2); listening, not reading | medium | 2026-11-01 | abstract |
| Rule 5 | A label whose referent comes later costs about 80 ms per attempt (cataphora) | holds with a limit | Reading-time studies summarized in pesquisa-conferida.md, section 4.2 | medium | 2026-11-01 | abstract |
| Rule 5 | Say who before what; a named source beats a vague one | practice (standard) | BBC News Styleguide, John Allen 2003, section "Attribution first", page 22; BBC Editorial Guidelines 2025, section 3, items 3.4.4 and 3.4.6 | high | 2026-11-01 | full text |
| Rule 5 | An analogy needs its limit line | practice | The project's own cold-reader tests; nearest study is seductive details (Rule 9) | low | carried | summary page |
| Rule 6 | Resuming after an interruption costs time, more with longer interruptions | holds with a limit | Monk, Trafton and Boehm-Davis 2008, JEP: Applied 14(4), doi:10.1037/a0014402; 599 ms in experiment 1; a manual lab task, not reading | medium | 2026-11-01 | abstract |
| Rule 6 | A given part with no antecedent costs 65 to 181 ms | holds with a limit | Haviland and Clark 1974, Journal of Verbal Learning and Verbal Behavior 13(5), 512 to 521; 53 students, isolated sentence pairs; measures a missing antecedent, not given-new order | medium | 2026-11-01 | full text |
| Rule 6 | Given before new helps, depending on the construction | holds with a limit | Clifton and Frazier 2004, Memory and Cognition 32(6), doi:10.3758/BF03196867; double-object construction only | medium | 2026-11-01 | abstract |
| Rule 6 | Retrieval and repetition help adults with ADHD remember | holds | Knouse and others 2011; Minear and others 2023 (section 8.5) | medium | carried | abstract |
| Rule 6 | The literal re-entry template is what the model copies | holds | Min and others 2022 on in-context examples; the Anthropic skill documentation ("literal text to emit"); Phase B of the investigation, section 5.2 | medium | 2026-11-01 | full text |
| Rule 7 | Visuals help when the reader builds the relation; two lines under each visual | holds with a limit | Schroeder and others 2018; Garcia-Retamero and Cokely 2017; Berney and Bétrancourt 2016 (section 8.3) | medium | carried | abstract |
| Rule 8 | Support that helps a novice hurts an expert (expertise reversal) | holds | Kalyuga, Ayres, Chandler and Sweller 2003, Educational Psychologist 38(1), doi:10.1207/S15326985EP3801_4; narrative review with students | medium | 2026-11-01 | abstract |
| Rule 9 | Interesting but irrelevant details lower learning | holds | Sundararajan and Adesope 2020, meta-analysis (section 8.2) | high | carried | abstract |
| Rule 9 | Speaking to the reader ("you") improves retention and transfer in short lessons | holds with a limit | Ginns, Martin and Marsh 2013, Educational Psychology Review 25(4), doi:10.1007/s10648-013-9228-0; d = 0.30 and 0.54; the effect fades past 35 minutes | high | 2026-11-01 | abstract |
| Rule 9 | "No personality" is backed by screen-versus-audio research | contradicted | No such study exists; Rogowsky 2016 and Daniel and Woody 2010 compare modalities without measuring tone. Retired on 2026-11-01 | high | 2026-11-01 | abstract |
| Rule 10 | Plain language has an international standard with four principles | holds (standard) | ISO 24495-1:2023; ABNT NBR ISO 24495-1:2024; Lei 15.263 of 2025; Federal Plain Language Guidelines | high | 2026-11-01 | summary page |
| Rule 10 | Bolding word beginnings (Bionic Reading) does not help | holds | Snell 2024; Parker and others 2026 (section 9.3) | medium | carried | abstract |
| Rule 10 | A label in the wrong language is a foreign word; the model copies the example's letter | holds | Phase B of the investigation, section 5.2; Min and others 2022 | medium | 2026-11-01 | full text |
| Rule 11 | One action per step, goal before action, about seven steps | practice | W3C COGA; ASD-STE100; Google and Microsoft style guides | medium | carried | summary page |
| Who writes | Narrative helps memory more than understanding | holds with a limit | Mar, Li, Nguyen and Ta 2021, Psychonomic Bulletin and Review 28(3), doi:10.3758/s13423-020-01853-1; 78 samples, 33,078 participants, g = 0.55, memory g above comprehension g (0.48); compares whole genres, non-clinical samples | high | 2026-11-01 | abstract |
| Who writes | Expository text integrates better with prior knowledge | holds with a limit | Wolfe and Woodwyk 2010, British Journal of Educational Psychology 80(3), doi:10.1348/000709910X485700; "narrative helps less with mechanisms" is not its finding | medium | 2026-11-01 | abstract |
| Without reasoning and without tools | A skill must say what to do when a tool is missing | practice | Phase B of the investigation (lacos.md, sections 2 and 4); the Anthropic skill documentation | medium | 2026-11-01 | full text |
| Rule 7 | A sequence of steps is a list, never a diagram; real graphs are inline SVG; form follows content | holds with a limit | Berney and Bétrancourt 2016 (form by content); the Project's phone test of 24 September 2026 and its playbook rule pb-004 (practice) | high for "never a sequence", medium for the SVG preference | 2026-11-02 | full text |

When the reader asks where a rule comes from, answer from this table: the source, the certainty and the date it was checked. The quick map below is the older summary and stays for context.

## Quick map: which evidence backs which rule

- Rule 1 (structure, lead with the goal, small blocks, one sentence per line): COGA front-loading and chunking; Federal Plain Language headings; Mayer signaling and segmenting; BDA short blocks; Brann and Sidi 2025 on stage-by-stage guidance for adults with ADHD (section 8.5).
- Rule 2 (sentence length, connectors, subject-verb, no em dashes, active voice and present tense): plain-language 15-word target; STE sentence ceilings; COGA no nested clauses; Federal transition words; COGA 4.4.2, the BDA style guide and ASD-STE100 on active voice and simple tenses; Yeari et al. 2018 on fewer inferred links between ideas in adults with ADHD (section 8.5).
- Rule 3 (problem plus counter-pattern): instructional-design worked-example practice.
- Rule 4 (no assumed domain knowledge): COGA clear words; plain-language define-your-terms.
- Rule 5 (jargon then term; one word, one meaning): COGA acronym-on-first-use; ASD-STE100 one word one meaning; L2 vocabulary-frequency research.
- Rule 5 (an analogy pays its loan): a practice rule from the project's own cold-reader tests, with no controlled study behind it in this file. The nearest evidence is the seductive-details work in section 8.2, which is about irrelevant additions, not analogies, so treat the rule as reasoned practice.
- Rule 6 (teach on the way; do not rely on memory; zero backtracking in two tiers): COGA Objective 6 (working memory); Federal cross-reference warning; Knouse et al. 2011 and Minear et al. 2023 on retrieval in adults with ADHD (section 8.5); Monk, Trafton and Boehm-Davis 2008 on resuming after an interruption (section 9.1).
- Rule 7 (visual plan): BDA flow charts; Mayer multimedia, but watch the redundancy effect; Schroeder et al. 2018 on constructed concept maps; Garcia-Retamero and Cokely 2017 on visual aids for risk; Berney and Bétrancourt 2016 on animation; Sundararajan and Adesope 2020 on seductive details (section 8.3).
- Rule 8 (depth in small chunks, calibrated to what the reader knows, in three cases): Mayer segmenting; cognitive load theory; Kalyuga et al. 2003 on expertise reversal (section 9.2). The three cases (inside the field, outside it, no reader context) are the operational form of that review's finding.
- Rule 9 (no ornament that does not serve a concept; write as in a work email to a colleague): Sundararajan and Adesope 2020 on seductive details (section 8.2); Ginns, Martin and Marsh 2013 on conversational style (section 10.1). Phase C of the November 2026 investigation found no modality study that measures tone (section 10.2).
- Rule 10 (plain words in the reader's language, numbers as words, dates, bold not italics, language packs): ADHD figurative-language difficulty; COGA numbers guidance; BDA emphasis guidance; Snell 2024 and Parker et al. 2026 on Bionic Reading (section 9.3); Lei 15.263/2025 and the Federal Plain Language Guidelines (section 9.4).
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
- 4.4.2 Simple tense and voice: present tense, active voice, put the aim of the sentence at the start. (Rule 1 lead-with-goal, Rule 2 active voice and present tense.)
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

## 8. Evidence added on 13 October 2026

These entries come from a research round of 13 October 2026 that was checked at the source (PubMed, Valency, and each study's own page). Each entry gives the claim, the effect size when the round confirmed it, the source with its DOI, and the limit to keep in mind. Effect sizes are Hedges' g or Cohen's d, so 0.2 is small, 0.5 is medium, and 0.8 is large. Where the round could not confirm a number, the entry says so and the number stays out.

### 8.1 Retrieval, spacing and testing (basis for Key point recaps, prequestions and quizzes)

- **Spaced retrieval beats massed retrieval.** g = 0.74 across 39 effects. An expanding schedule and a uniform schedule do not differ (g = 0.034 across 54 effects). Source: Latimier, Peyre and Ramus 2021, Educational Psychology Review, [doi:10.1007/s10648-020-09572-8](https://doi.org/10.1007/s10648-020-09572-8). Limit: mostly students.
- **Practice testing beats rereading.** g = 0.51 across 195 comparisons, and g = 0.93 against a filler activity, from 272 effects and 15,427 participants. Source: Adesope, Trevisan and Sundararajan 2017, Review of Educational Research, [doi:10.3102/0034654316689306](https://doi.org/10.3102/0034654316689306). So a recall prompt at the end of a text is worth more than a second summary.
- **Prequestions and prediction before reading.** The round found no verified meta-analysis on prequestions. The nearest evidence is a theoretical review on predicting before seeing: Brod 2021, Psychonomic Bulletin and Review, [doi:10.3758/s13423-021-01904-1](https://doi.org/10.3758/s13423-021-01904-1). It calls its own evidence early, and the one measured effect it reports (d = 0.56) comes from children aged 6 to 9. So treat prequestions as a reasonable practice with lower certainty, and aim them only at the main concepts.

### 8.2 Pre-training, segmenting and seductive details (basis for Key terms, small blocks and cutting curiosities)

- **Pre-training helps.** Teaching the names and features of the key concepts before the lesson improved learning in 13 of 16 tests, median d = 0.75. **Segmenting helps.** Presenting the material in learner-paced chunks improved learning in 10 of 10 tests, d = 0.79. Source: Mayer and Pilegard 2014, in The Cambridge Handbook of Multimedia Learning, second edition, [chapter page](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258). Limit: this is the authors' own count of studies, not an independent meta-analysis, and pre-training helps most when the reader knows little about the topic. This is the basis for the "Key terms" section in Rule 6 and for the small blocks in Rules 1 and 8.
- **Seductive details hurt learning.** Interesting but irrelevant additions lower learning of the main content. Source: Sundararajan and Adesope 2020, Educational Psychology Review, [doi:10.1007/s10648-020-09522-4](https://doi.org/10.1007/s10648-020-09522-4). Limit: the round confirmed the direction in the abstract. The often-quoted size (g = -0.33) could not be read at the source, so do not quote the number. The consequence for the skill: an addition that serves no main concept is cut or moved to an optional depth block.

### 8.3 Visuals (basis for Rule 7, the visual plan)

- **Constructing a concept map beats studying a finished one.** g = 0.72 for constructing against g = 0.43 for studying, from 142 effects and 11,814 participants. Source: Schroeder et al. 2018, Educational Psychology Review, [doi:10.1007/s10648-017-9403-9](https://doi.org/10.1007/s10648-017-9403-9). This is why a visual must let the reader build the relation (the "How to read" line plus a conclusion). A decorative picture gives the reader nothing to build.
- **Transparent visual aids improve risk understanding**, and most for readers with low numeracy. Source: Garcia-Retamero and Cokely 2017, Human Factors, a review of 36 publications with 27,885 participants, [doi:10.1177/0018720817690634](https://doi.org/10.1177/0018720817690634). This is the basis for the icon array with natural frequencies for every health risk.
- **Animation beats a static picture only slightly.** g = 0.226 overall. The effect was larger with system pacing (0.309) and with no text alongside (0.883). Source: Berney and Bétrancourt 2016, Computers and Education, [doi:10.1016/j.compedu.2016.06.005](https://doi.org/10.1016/j.compedu.2016.06.005). Limit: a small average effect, so the skill relies on segmenting, not on animation, and caps manipulable interactives at one per document.

### 8.4 Audio (basis for keeping audio a separate, shorter script)

- **Long audio reverses the modality advantage.** With long spoken segments, the usual benefit of narration over on-screen text turns into a cost, and shortening the audio brings the benefit back. Source: Leahy and Sweller 2016, Instructional Science, [doi:10.1007/s11251-015-9362-9](https://doi.org/10.1007/s11251-015-9362-9). Limit: one task type (a contour map). The consequence, carried by the sibling skill clear-listen, is that audio retells the main ideas in short parts and never reads a guide aloud.

### 8.5 Direct evidence on adults with ADHD

Section 1 of this file leaned on one eye-tracking study and on practitioner advice. The 13 October 2026 round found direct studies on reading, screens and retrieval in adults with ADHD. They are small and use university students, but they point the same way.

- **Retrieval practice helps adults with ADHD as much as controls.** 36 students with ADHD and 36 without. Source: Minear et al. 2023, Frontiers in Psychology, [doi:10.3389/fpsyg.2023.1186566](https://doi.org/10.3389/fpsyg.2023.1186566). So recall prompts and quizzes are not wasted on this reader.
- **Adults with ADHD self-test less, and that gap explains the memory difference.** 34 adults with ADHD and 34 without. Source: Knouse, Anastopoulos and Dunlosky 2011, Journal of Attention Disorders, [doi:10.1177/1087054711417231](https://doi.org/10.1177/1087054711417231). So the text must ask the question itself, because the reader will not remember to self-test.
- **In a long digital text, guidance at each stage closes the gap.** 210 adults aged 20 to 50, half with ADHD. Without guidance, the ADHD group understood less, and mind-wandering explained the difference. With guidance before, during and after reading, the groups tied. Source: Brann and Sidi 2025, Learning and Instruction, [doi:10.1016/j.learninstruc.2024.102051](https://doi.org/10.1016/j.learninstruc.2024.102051). This is the strongest support for the scaffolds in Rules 1 and 6: lead with the goal, Key point recaps, and a final recall.
- **On a screen, the ADHD group understood less and over-trusted its own score; on paper, the groups tied.** 45 students with ADHD and 61 without. Source: Ben-Yehudah and Brann 2019, Research in Developmental Disabilities, [doi:10.1016/j.ridd.2019.04.001](https://doi.org/10.1016/j.ridd.2019.04.001). So a felt sense of understanding is not a check, which is why the skill prefers a recall prompt over "does this make sense?".
- **Adults with ADHD recognize the central ideas but recall less, and their reading suggests fewer links between ideas.** 28 students with ADHD and 27 without. Source: Yeari et al. 2018, Journal of Clinical and Experimental Neuropsychology, [doi:10.1080/13803395.2018.1501000](https://doi.org/10.1080/13803395.2018.1501000). This is the direct basis for explicit connectors (Rule 2) and for restating the link between ideas instead of pointing back (Rule 6).

Limits of this group: small samples, university students, English or Hebrew texts, and none of them tested diagrams or interactives. The visual rules therefore rest on the general multimedia evidence in section 8.3, not on ADHD-specific studies.

## 9. Evidence added on 14 October 2026

### 9.1 Interruption and resumption (basis for the two-tier zero-backtracking rule in Rule 6)

- **Resuming a task after an interruption costs time, and the cost grows with the length and the demand of the interruption.** Resumption lag rose steeply over the first seconds of an interruption and then leveled off, and a demanding interruption (a verbal n-back task) cost more than a blank screen. Three experiments with 12, 11 and 36 participants. Source: Monk, Trafton and Boehm-Davis 2008, Journal of Experimental Psychology: Applied, [doi:10.1037/a0014402](https://doi.org/10.1037/a0014402). Limit: a laboratory task, not reading. The consequence for the skill: the reader reloads context from the last lines on screen, so the first mention in each block carries the full name and its meaning (tier 1), and a bare label or a pointer back gives the reader nothing to reload.

### 9.2 Expertise reversal (basis for the depth calibration paragraph in Rule 8)

- **Instructional support that helps a novice can lose its value, or hurt, for a more experienced learner.** The review calls this the expertise reversal effect: worked examples, integrated explanations and other load-reducing formats interact with the learner's prior knowledge. Source: Kalyuga, Ayres, Chandler and Sweller 2003, Educational Psychologist, 38(1), 23 to 31, [publisher record via the University of Wollongong](https://ro.uow.edu.au/edupapers/136). The DOI could not be confirmed in this round, so cite the journal reference. The consequence for the skill: on a topic inside the reader's own field, keep the basic explanations short or collapsed, because explaining what the reader already knows also costs attention.

### 9.3 Bionic Reading (basis for the "never bold word beginnings" line)

- **Bolding the first half of each word does not speed up reading.** 100 paragraphs, half in the bolded format, with no significant difference in reading time. Source: Snell 2024, Acta Psychologica, 247, 104304, [doi:10.1016/j.actpsy.2024.104304](https://doi.org/10.1016/j.actpsy.2024.104304).
- **A registered eye-tracking report found the same.** 90 skilled adult readers; start-bolding moved the first fixation closer to the start of long words, but gaze duration, total reading time and comprehension (about 95% correct in every condition) did not change, and 43 of 90 readers rated the unbolded text as most readable. Source: Parker, Lee, Wang and Joseph 2026, Royal Society Open Science, [doi:10.1098/rsos.250177](https://doi.org/10.1098/rsos.250177). Limit: skilled adult readers, so the result says nothing about readers with dyslexia.
- The consequence for the skill: bold marks the one most important line of a block (the "bold trail"), never the beginnings of words. Note the scope: Snell 2024 measured reading time only; comprehension comes from Parker et al. 2026 alone.

### 9.4 Plain-language standards (basis for the language packs)

- **Brazil.** Lei 15.263, de 14 de novembro de 2025, the Política Nacional de Linguagem Simples. Article 5 lists the techniques: direct order, short sentences, one idea per paragraph, common words, the full name before an acronym, active voice, no inserted clauses, verbs instead of nouns made from verbs, the most important information first, and testing with the audience. Source: [the law at the Senado](https://legis.senado.leg.br/norma/41699861/publicacao/41699940). `references/lang-pt-br.md` maps each item to a rule.
- **United States.** The Plain Writing Act of 2010 and the Federal Plain Language Guidelines (March 2011), now carried on Digital.gov: active voice, present tense, hidden verbs, "must" for requirements, pronouns, abbreviations (define at first use, about three per document), short sentences, subject-verb-object together, main idea before exceptions, transition words, examples, lists and tables, and minimal cross-references. Sources: [Digital.gov plain language guide](https://digital.gov/guides/plain-language) and the [2011 guidelines (PDF)](https://revenue.ky.gov/DOR%20Training%20Materials/Federal%20Plain%20Language%20Guidelines.pdf), a state agency's copy of the federal PDF, used because plainlanguage.gov now redirects to Digital.gov and the original site is archived in the GSA/plainlanguage.gov repository on GitHub. `references/lang-en.md` maps each heading to a rule.

## 10. Evidence added on 1 November 2026

These entries come from the November 2026 investigation, checked at the source. The record is in `plugins/dc/references/investigacao-2026-11/pesquisa-conferida.md`, sections 2.8 and 6.

### 10.1 Conversational style (basis for the second rule of Rule 9, "write as in a work email to a colleague")

- **A text that addresses the reader directly teaches better, in short lessons.** A meta-analysis of personalization, the conversational "you" in place of a neutral third person, found better retention (d = 0.30), better transfer (d = 0.54) and a friendlier rating of the text (d = 0.46). Source: Ginns, Martin and Marsh 2013, Educational Psychology Review, 25(4), 445 to 472, [doi:10.1007/s10648-013-9228-0](https://doi.org/10.1007/s10648-013-9228-0). Limit: short lessons; the effect disappears in sessions above 35 minutes. The consequence for the skill: Rule 9 no longer says "no personality", because this evidence runs against it. Rule 9 now says write as in a work email to a colleague, with "you" ("você"), and cuts only the ornament that serves no concept, on the seductive-details evidence in section 8.2.

### 10.2 Tone and modality: no source found

- Rule 9 once attributed its calm tone to "screen-versus-audio reading research". Phase C of the November 2026 investigation looked for that research and found none that measures tone. The two studies it found that compare reading with listening, Rogowsky 2016 and Daniel and Woody 2010, measure comprehension and retention across the two modes and say nothing about tone. So the attribution is retired below, and the two rules of Rule 9 rest on sections 8.2 and 10.1.

## Trade-offs to weigh, not ignore

- One sentence per line versus cohesion. Forcing a blank line after every sentence fragments the text into a wall, which is the failure clear-read fixes with tight blocks (Rule 1). Keep sentences on their own line inside small blocks, with blank lines only between topics.
- Connectors versus one point per sentence. Use connector words between two short sentences to show the logical link, but do not stack clauses inside one sentence.
- Readability score versus comprehension. Covered above: floor-check only, never a target.
- Controlled vocabulary versus an intelligent reader. Adopt STE's discipline, not its stilted register, because the reader is an expert, just attention-limited and often reading in a second language.
- One method, several languages. The structural evidence (chunking, signaling, connectors, retrieval, working-memory limits) is not tied to English, and the Brazilian plain-language law (Lei 15.263 de 2025) asks for the same moves: direct word order, no inserted clauses, verbs instead of nominalizations, the full name before an acronym. The second-language load applies when the reader reads in English; the attention and fatigue load applies in both languages.
- Diagrams and recaps versus the redundancy effect. They must add structure or compress, not duplicate the prose.

## Certainty and caveats

- High certainty: vocabulary frequency drives L2 comprehension; segmenting lowers load; readability formulas do not measure comprehension; working-memory limits in ADHD; the structural rules from BDA, COGA, STE, and plain-language standards; spaced retrieval and practice testing (large meta-analyses, section 8.1).
- Medium certainty: the direct studies on adults with ADHD (section 8.5), which are small but agree with each other; the visual evidence in section 8.3, which comes from general learners, not from readers with ADHD.
- Lower certainty or heuristic: the specific numbers (about 1,500 common words, five choices per screen, 50-word paragraphs, 1 to 4 memory items, 60 to 70 characters per line, the four-question thresholds of Rule 7). These are sensible expert defaults, not hard constants, and should be tuned by testing with the real reader. Prequestions and the size of the seductive-details effect also sit here (sections 8.1 and 8.2).
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
- Ginns, Martin and Marsh (2013), meta-analysis of the personalization (conversational style) principle, Educational Psychology Review; DOI in section 10.1.
- The sources added on 13 October 2026 (Latimier 2021, Adesope 2017, Brod 2021, Mayer and Pilegard 2014, Sundararajan and Adesope 2020, Schroeder 2018, Garcia-Retamero and Cokely 2017, Berney and Bétrancourt 2016, Leahy and Sweller 2016, Minear 2023, Knouse 2011, Brann and Sidi 2025, Ben-Yehudah and Brann 2019, Yeari 2018) are listed with their DOIs in section 8.

## Retired

Retired on 2026-11-01: "the plain-language standard behind the rules (Lei 15.263 in Brazil, the Federal Plain Language Guidelines in the United States)" (Rule 10). Reason: change 12 of the November 2026 investigation. The parenthesis now names the international standard, ISO 24495-1:2023, first, and lists the national law and guidelines as applications of it, so the packs stay portable to a third language.
Retired on 2026-11-01: the heading "## The legal basis" in `lang-pt-br.md`, and the heading "## The standard behind the rules" in `lang-en.md` over the United States guidelines. Reason: change 12. Both packs now open with a section "The standard behind the rules" about ISO 24495-1, and the national sections are "How Brazil applies it" and "How the United States applies it". No sentence under the old headings was removed.
Retired on 2026-11-01: "Rule 9 (calm tone, screen reading): screen-versus-audio reading research." (quick map, Rule 9). Reason: change 14 of the November 2026 investigation. Phase C found no study that compares screen reading with audio and measures tone; Rogowsky 2016 and Daniel and Woody 2010 compare the two modes without measuring tone (section 10.2). Rule 9 now names its two sources.
Retired on 2026-11-01: "The text is for silent reading on a screen." (Rule 9). Reason: change 14. The sentence carried the screen-versus-audio attribution above, which has no source. Audio stays with the sibling skill clear-listen; this skill's description already says it writes for a reader.
Retired on 2026-11-01: "It is not playful, creative, or performative, because effort spent decoding personality is effort not spent understanding." (Rule 9). Reason: change 14. Ginns, Martin and Marsh 2013 found that a text which speaks to the reader directly teaches better in short lessons (section 10.1), so "no personality" had evidence against it. What survives is "no ornament that does not serve a concept", on the seductive-details evidence (section 8.2), and the new second rule, "write as in a work email to a colleague".
Retired on 2026-11-01: "These rules are not arbitrary. They come from research on attention difficulties, plain-language writing, and second-language reading. ... Consult it as needed; it is not required for everyday use." and the paragraph that listed what `references/tests.md` covers (SKILL.md, "Why these rules work"). Reason: change 18b, the body shrinks; the pointer stays in one paragraph and the lists moved to `references/lint.md` and `references/tests.md`.
Retired on 2026-11-02: "A flow or a branching structure becomes a small Mermaid diagram, or a numbered outline when Mermaid does not fit." (SKILL.md, Rule 7, 'Pick the form by the content'). Reason: change 20 (addendum 2 of the November 2026 investigation). The Project's test of 24 September 2026 showed the phone app cutting Mermaid labels, and a chain of boxes for a sequence repeats the prose and fails the four-question test. Sequences are lists; real graphs are inline SVG.
