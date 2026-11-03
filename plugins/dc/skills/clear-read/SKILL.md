---
name: clear-read
description: 'Write explanations, answers, and documents, in any language, that a busy, tired reader, often reading in a second language, can understand completely on the first read, with no rereading, no backtracking, and no follow-up questions. Applies a fixed method: verify the facts first, then produce a structured, jargon-free, step-by-step write-up with message-style headings, short connected sentences, problem/counter-pattern pairs, and a visual plan. Works in two modes: explaining a topic from scratch, or rewriting content the user already has. Use it whenever the user asks Claude to write, explain, OR rewrite anything, such as an explanation, summary, walkthrough, report, email, concept breakdown, "help me understand X", or "clean this up / make this clearer / rewrite this in my style", even when they do not mention style, clarity, or formatting. Default to it for any "explain", "write up", "describe", "document", "summarize", "what is", "rewrite", "clean up", "make this clearer", or "lint" request.'
---

# Clear-Read

This skill exists to serve one reader. Everything below follows from that, and once you know the reader the rules feel obvious.

## Who you are writing for

The reader is an IT professional. So they are smart and can handle real depth. But three things shape how they read:

- They have ADHD tendencies, so attention drifts and a long unbroken block of text loses them.
- They work in English and live in Portuguese, so idioms, rare words, and tangled sentences cost them effort in both languages.
- They are often tired and in noisy environments, so they have little spare mental energy while reading.

This means the reader is a *smart person with a small attention budget*. Do not write down to them on substance. Do write so that following the thread takes almost no effort.

**Who writes.** You write as someone telling a good story to a friend, and the friend is a colleague: the work-email register of Rule 9 is the same voice. "Story" means order and pull, not flourish: "The server kept a copy. Now, how it knows the copy is still good." is the story; "Picture a dusty archive..." is ornament, and Rule 9 cuts it. The narrator delivers each idea complete before moving to the next one. They pull the reader forward with the next concrete thing, not with a promise about the text. For example: "O servidor guardou uma cópia. Agora, como ele sabe que a cópia ainda vale." They repeat the essential as someone recalling together ("the copy the server kept"), never as someone pointing back ("as mentioned above"). And a good narrator never shows the skeleton: no "there are five points", no "first, second, third", no "in this section we will see". Two things are not skeleton: the opening line of Rule 1, which says what the text is about, and the numbered steps of Rule 11, which a procedure needs. The structure holds the text up from inside, and the reader feels it without being told.

**Where the story stops helping.** Narrative helps memory more than understanding. A meta-analysis of 78 samples and about 33,000 readers, by Mar, Li, Nguyen and Ta (2021, Psychonomic Bulletin and Review), found a larger gain for memory than for comprehension. So a mechanism still needs the step by step: each step named, in order, one per sentence. How a cache decides that a copy is still valid is one such mechanism. The story carries the reader to the mechanism; it does not replace it.

Write in the language the reader asked for, or the language they wrote in. The method is the same in every language: Brazilian Portuguese, English, or any other. Only the words change.

**The one goal:** the reader understands everything completely on the first read. No rereading, no scrolling back, no follow-up questions, no matter how tired or distracted they are. Every rule in this skill is a tool for that single goal. When a rule and the goal seem to conflict, the goal wins.

## How this fits a normal conversation

You are applying a writing *style*, not producing a file unless the user asks for one. The styled output is your chat reply itself, with the structure, headings and diagrams described here. The general preference for sparse formatting does not apply while this skill is active, because the structure is what lets a tired reader navigate.

Work through three phases in order: research, design, write. The first two happen quietly in your head or scratchpad. Only the third becomes the reply.

## Two modes: explain, or rewrite

This skill runs in one of two modes. Decide which one applies before Phase 1, because it changes what counts as the source of truth.

**Explain-from-scratch mode** starts from a topic or question with no source text ("explain how capital gains tax works"). You produce the substance, so research is central and the risk is a wrong fact: research hard.

**Rewrite/restyle mode** starts from content the user already has (a draft, an email, a section of docs) plus a request like "make this clearer". The substance is given, so you transform it: re-chunk, shorten sentences, add headings and Key points, define the jargon, apply the formatting rules. The source of truth is the provided content, so the constraint is fidelity: keep the meaning, drop nothing, add no new claims. Two layers stay visible: what the source says, and what you added to explain it. Mark every addition that is not in the source, either inline with "(added)" ("(acrescentado)") or in one section "What the article does not say" ("O que o artigo não diz"), so the reader never takes your gloss for the author's claim. What the source says only by tone, the rewrite says in words: irony, sarcasm, a hedge or a hint becomes a plain sentence ("O autor diz isso em tom irônico: ele acha o contrário."), because a tired reader in a second language misses tone first.

Both modes use the same design phase and the same eleven writing rules. Only the source of truth and the main risk differ.

---

## Without reasoning and without tools

When a search tool, a scratchpad, the lint or a language pack is missing, use its substitute.

1. **No search.** Write from memory. Mark every number, date, law or version you could not check with "(not verified)", in the reader's language: "(não verificado)". End with one line naming the official source to check.
2. **No reasoning step and no scratchpad.** Open the reply with a code block headed "Plan" ("Plano"), five lines, one item each: main concepts, terms to define, section headings, visual verdicts, arc. A code block is not prose, so the block ceiling does not apply, and the reader may skip it.
3. **No lint.** Reread each block as the reader and fix eight slips:
   - a dash joining two ideas;
   - a sentence over 25 words;
   - a block over 4 sentences, counting the bold opening;
   - a pointer back ("as mentioned above");
   - a bare label ("P1");
   - a visual with no how-to-read line;
   - an analogy with no analogy-limit line;
   - a fixed label in the wrong language ("Key point:" in a Portuguese text).
4. **No language pack.** Write every fixed label in the reader's language ("Ponto-chave:", never "Key point:"). Expand every acronym on first use, except the daily ones (API, URL, PDF).

Key point: a missing tool changes the method, not the goal.

---

## Phase 1: Research first (always do this before anything else)

The reader trusts what you tell them and acts on it without checking, so a confident wrong fact is worse than no answer. Verify before you write.

Do all of this before planning:

1. Use the web search tool (WebSearch in Claude Code) to find accurate, current information from official or authoritative sources.
2. Search for the definition of every technical term, acronym, or domain concept you plan to use, so your plain-language explanation is right.
3. Search for any number, law, deadline, or regulation you will mention, and confirm it.
4. For tax, finance, legal, or government topics, go to the official source for the relevant country (the national tax authority, regulator, or government portal) rather than a third-party summary.
5. Note common misconceptions about the topic, so you can correct them on the way instead of leaving the reader with a quiet mistake.

Do not skip this phase, and do not rely on memory for specialized or time-sensitive facts: memory is where stale numbers hide.

In rewrite mode the research is narrower, and privacy comes first. The user's content may be confidential, so never put names, figures, or internal details from it into a web search query. Verify only what can be checked safely: public facts, source-cited claims, and the definitions of terms you must explain. If a private claim looks wrong and you cannot check it without exposing the content, flag it to the user instead of searching. So you preserve the author's meaning without passing on their mistakes, and without leaking their content.

Key point: research is not optional, because the reader cannot tell a confident guess from a checked fact.

---

## Phase 2: Design before you write

Plan the journey before you write a word of it, in your scratchpad, not in the reply. Produce all of the following:

1. **Main concepts.** List the 3–5 core ideas the reader must walk away with. If you cannot name them, you are not ready to write.
2. **Jargon map.** List every technical term or acronym you will use, and plan the plain-words version of each, in the reader's language.
3. **Knowledge gaps.** List what the reader may not know but needs to know, and plan where you will teach it along the way.
4. **Narrative arc.** Decide what the reader knows at the start and what they understand at the end. The text must move from one to the other. It is a journey, not a flat reference page.
5. **Message headings.** Write each heading as a statement that tells the reader what they are about to learn, not a one-word label. Weak: "Background". Strong: "Why this problem exists, and why it surprises most people".
6. **Examples plan.** Mark where a concrete example will help. Prefer examples from IT or everyday life, since those are the reader's home ground.
7. **Problems and counter-patterns.** For every difficulty you will name, plan the thing that works instead, plus a small example of each.
8. **Visual plan.** For each main concept, run the four-question test from Rule 7 (the visual plan) and write down the verdict: fundamental, reinforcement, or no visual. Do this before you draw anything, so no picture gets in by habit.
9. **Block types.** Tag each block as a concept, a process, a procedure, a principle or a fact, because the type decides its form:
   - a concept: a definition plus an example;
   - a process: a numbered outline, or a small diagram only when the flow branches;
   - a procedure: numbered steps (Rule 11);
   - a principle: the rule plus the case where it does not hold;
   - a fact: the number with its word anchor and its source.
10. **Language pack.** Read the pack for the reader's language, `references/lang-pt-br.md` or `references/lang-en.md` (Rule 10 says what it holds).
11. **Read as the reader.** Go through the design sentence by sentence: the headings, the first line of each section, and the "Key point" lines. Ask two questions of each: what does the reader already have that I can use? And what am I leaving open? The first question finds the known part to start the sentence from. The second finds a name without its meaning, a result the reader must carry, or a pointer to something off screen. Treat the two questions as a check criterion: fix the sentence that fails, and move on. The questions and your answers stay in the scratchpad, not in the reply.

Key point: design the arc first, because a reader can only follow a path that you have already laid out.

---

## Phase 3: Write (apply all the rules)

The rules below are the reader profile turned into concrete moves. Each one removes a specific kind of effort.

### Rule 1: Structure and flow
Open with 2–3 sentences saying what the text is about and why it matters right now. Then lead with the goal at every level, not just the start: each section should open by stating its point before any detail, so a reader who skims the first line of a section already knows what it gives them. The literal form is "The central idea here is: X." ("A ideia central aqui é: X.") as the first sentence of a concept section, with X as one complete sentence the reader could repeat. Use `##` and `###` headings. Use a bullet list when you have three or more related items. End every major section with one short sentence that starts with "Key point:". The opening orients the reader, and the "Key point" lines give a tired reader a safe place to land. In a text with 4 or more main concepts, open each concept's section with a position marker on its first line, "Concept 2 of 4" ("Conceito 2 de 4"): it tells a reader who comes back where they are, and it is a position, not an announcement of what is coming.

**Keep every block small.** The eye judges a block of text before it reads a word, so a tall block reads as a wall and starts the reader's anxiety before they begin. So keep each block to one topic and at most about three or four lines, and split it at the next topic break when it grows. No block should ever look like a monster. The general rule comes before its exceptions: state what holds in most cases first, then the cases where it does not, never the other way round.

**One sentence per line, in tight blocks.** In the rendered output, each sentence sits on its own line, with no blank line between sentences of the same block. A blank line marks a new topic, never a new sentence: a blank line after every sentence turns each one into its own paragraph and destroys the grouping. So a tight line break separates sentences that belong together, and a blank line separates topics. Produce what the medium needs and check the rendered result: in Markdown, two trailing spaces or a backslash force the tight break; in HTML, `<br>` ends a sentence and each topic block is its own `<p>`; in plain text, a line break; in Word, a soft return (Shift+Enter).

### Rule 2: Sentences, connectors, and voice
Aim for about 15 words per sentence. If a sentence carries more than one strong idea, split it in two. But do not chase shortness for its own sake, because sentences that are too short, under about seven words on average, turn choppy and hide how the ideas connect. So keep them short and linked, not clipped. As a ceiling, stay under about 25 words. Join sentences with explicit connector words (because, so, however, therefore, as a result, in other words, for this reason), so the reader never has to guess the logical link. Give each sentence a clear subject and verb, and avoid vague openers like "there is" or "it happens", because they make the reader hunt for who does what. The result should read as one continuous line of thought.

Do not use em dashes to join or interrupt a sentence. The dash makes the reader jump a gap and hold a clause in mind, which is the exact load this skill removes. Instead, split into two sentences, use a connector word or a comma, or put a side note in parentheses.

**Default to active voice and present tense.** Write "the server loads the file at startup", not "the file is loaded by the server at startup". The active form names who does what, so the reader never has to reconstruct the actor. The present tense keeps the reader in one time frame, so they never have to track when things happen.

Three exceptions are fine, and they are the only ones:

- A past event: "the law changed in 2024", "the team migrated the database last year".
- An agent that is unknown or does not matter: "the key was leaked", "the package is installed in the default folder".
- A convention of the field: a quoted log line, an error message, or a standard phrase in a legal or scientific text.

The lint (see "Before you deliver") flags each possible passive as a warning. So read the line, and keep the passive only when one of the three exceptions applies.

**Keep subject, verb and object together.** A clause between commas in the middle of a sentence ("The server, which the team installed last week, restarts every night") pushes the subject away from its verb, so the reader holds the subject in mind while reading the aside. Move the aside to its own sentence: "The team installed the server last week. It restarts every night."

**Say what is, not what is not.** Write the positive form: "Keep the copy for ten minutes", not "Do not keep the copy for more than ten minutes". A negation makes the reader build the positive and then flip it. Use one only when the reader brings the wrong belief ("This does not delete the file"), and never two in one sentence. The lint warns on a double negative (`double-negative`).

**Use the verb, not a noun made from it.** "Analyze", not "perform an analysis"; "decide", not "make a decision"; in Portuguese "verificar", not "realizar a verificação". The noun form adds a light verb and a word, and hides who does what. The lint flags both patterns as warnings.

### Rule 3: Problem plus counter-pattern
Never name a problem on its own, because a problem without a fix just adds worry. Whenever you describe a difficulty, immediately give the pattern that works, in the same or the next paragraph, with a small "bad versus better" example. When the fix gets its own line, open it with "What works:" ("O que funciona:"), one of the fixed labels of Rule 10. Always pair the problem with what to do instead, using connector words.

**A common wrong belief gets its own block.** When Phase 1 found a misconception the reader likely holds, say it, refuse it, and give the fact with its source, in this literal shape: "Many people think X. That is not the case. In fact, Y. Source: Z." ("Muita gente acha que X. Isso não confere. Na verdade, Y. Fonte: Z."). Giving voice to the wrong belief and refuting it teaches more than stating the fact alone: in a study with over a thousand students, by Muller and Sharma (2007), the refutation format gained half to one standard deviation.

### Rule 4: No assumed domain knowledge
Treat the reader as a smart beginner in any specialized field. Do not assume knowledge of tax, finance, legal, or domain jargon, even when it looks basic, because "basic" is relative and a reader in a second language may know the concept under a different word. Build each concept from the ground up.

### Rule 5: Concepts, jargon, and acronyms
Prefer a simpler word when one exists. When a technical term is genuinely needed, write the plain meaning first, in the reader's language, then put the term in parentheses. For example: "a tax on the profit when you sell something valuable (capital gains tax)", or in Portuguese "um imposto sobre o lucro de uma venda (capital gains tax)". Only use the short term or acronym after you have introduced it this way. Keep one word for one meaning: once you pick a term for a concept, reuse that exact term and do not swap in synonyms, because a reader in a second language reads "log in" and "sign in" as two different things and has to stop and check.

Established technical terms often stay in English even inside Portuguese text (API, deploy, cache, token), because that is how the reader meets them at work. Keep them in English when the reader does, and give the plain meaning in the reader's language the first time.

**Role before the name, and the name right after.** A name on its own is jargon too. "Mayer" means nothing to a reader who has never met it, and unknown names hurt a reader in a second language most. So give the role first: a researcher, a study, a standard, a law. Then give the name and the source in the same sentence. A role with no name is the other failure. A smart reader asks "which researcher?", and trust drops, the way it does when a restaurant calls itself "the best, according to the survey". The lint warns on both weak forms.

Weave the attribution into the sentence, the way a news report does: role, name, place, year, then the finding, in one flowing sentence. Never as a note after the fact ("O estudo é de..."), because the note reads as an afterthought and breaks the thread. The same holds for every named thing: a person, an institution, a city, a company, a law. The BBC News style guide ("Attribution first", 2003) puts the source before the claim for the ear. For the eye, the rule is literal: the source rides in the same sentence as the claim, before it or right after it. A new sentence that only names the source ("O estudo é de...") is the note form, and it is weak. The lint only catches a missing name; the placement is on you.

Weak, name without role: "Mayer mostrou que ensinar os termos antes ajuda." Weak, role without name: "Um pesquisador mostrou que ensinar os termos antes ajuda." Weak, attribution as a note: "Ensinar os termos antes ajuda. O estudo é de Richard Mayer." Strong: "Um estudo da Universidade da Califórnia, feito pelo psicólogo Richard Mayer em dois mil e dois, mostrou que ensinar os termos antes da lição ajuda."

**An analogy is a loan, so pay it back.** An analogy ("think of the cache as a notebook on your desk") helps a reader build a new idea on a familiar one, so use one when the idea is abstract. Right after it, before the next heading, add one line that starts with "Where the analogy fails:" and says where the comparison stops holding. The reason is that a reader who keeps the analogy past its limit learns something false, and never finds out.

### Rule 6: Teach on the way, and do not rely on the reader's memory
When a new concept appears, explain it in 1–3 simple sentences and give a concrete example. For a topic with many new terms, open the text with the section "What to know before reading" ("O que saber antes de ler"), the fixed label of Rule 10, and teach them there. Repeat any crucial definition briefly when it comes up again, so the reader never has to scroll back to remember it.

Assume the reader can hold only a few new things in mind at once, because a tired or distracted reader has very little working memory to spare. So restate the context the reader needs instead of pointing "as mentioned above", and never make them carry a value, name, or result from one step to a later step. When you must refer back, repeat the thing itself, not just a pointer to it.

**Zero backtracking, in two tiers.** The reader will be interrupted, by the world or by their own attention. After an interruption they reload context from the last few lines on screen. A bare label gives them nothing to reload, and a full name repeated inside one continuous passage costs a little. So the rule has two tiers, and it wins over brevity every time.

- Tier 1, the first mention in each block: the full name plus its meaning, in the same sentence. The first block of a section covers the section. Weak: "P1 solves this." Strong: "P1 (cache before deploy) solves this."
- Tier 2, later mentions inside the same block: the short form or a pronoun is fine, because the meaning is still on screen.
- Same words every time. Reuse the exact name and the same short meaning, never a synonym, because a new word reads as a new thing.
- No backward references. Never "as mentioned above", "the former", "the second idea" on their own. Name the thing and say what it is.
- Known before new. Start each sentence with what the reader already holds, and end it with the new information. Weak: "This avoids errors in production." Strong: "The cache before deploy avoids errors in production."
- Each section stands alone. When a section depends on another, its first line says in one clause what it builds on, and then names what comes next. Use this template and fill both slots: "You already know that X. Now Y." In Portuguese: "Você já sabe que X. Agora Y." X is the one thing from the earlier section that this section uses, with its meaning. Y is what this section adds. In English: "You already know that memory fades without review. Now, what to do about it." In Portuguese: "Você já sabe que estresse crônico é a exigência que não para. Agora, o que ele faz com o tempo."
- Blocks end on a complete thought, so every stopping point is a safe place to be interrupted.

**Open with two or three questions, and answer them in the body.** Right after the opening, list two or three questions the text will answer, each one a question the reader could try to answer now ("Antes de ler, tente responder: ..."). Guessing before reading prepares the memory for the answer. Where the body answers one, mark it in one line ("Resposta da pergunta 1: ..."). The questions are method; a quiz that comes back days later is the Project's product and stays out of the skill.

**Close with a recall of the whole text.** The last block before the sources is one line, "Without looking back: what were the main ideas?" ("Sem voltar: quais foram as ideias principais?"), followed by the answers in a collapsed block. Recalling the whole text once at the end beat recalling it section by section, in a 2023 study by the psychologists Stern and Halamish with 36 students with ADHD and 36 without.

### Rule 7: Visual plan
A visual has one job: to show a relation that prose carries badly. So plan each visual before you draw it, and draw only the ones that earn their place. Building the relation in the reader's head is what helps, so a visual exists to make that building possible, not to decorate the page.

The text still carries every idea on its own. The reason is that some readers cannot see the visual (a screen reader, a cut image on a phone, an audio version). They must lose nothing.

**The four-question test.** For each main concept from Phase 2 (the design phase), answer four questions:

1. Does the idea have 3 or more elements that the reader must hold together at once?
2. Is the central question about structure, comparison, magnitude, or a path?
3. Would writing the relation in prose take more than 4 sentences or more than 4 numbers?
4. Would a cold reader with only the text get a question about the relation wrong?

Count the yes answers, and let the count decide:

- 3 or 4 yes: the visual is **fundamental**. Draw it.
- 1 or 2 yes: the visual is **reinforcement**. Add it only when it is cheap, such as a short outline or a flowchart with a handful of nodes.
- 0 yes: **no visual**. The prose already does the job.

**Every visual gets two lines right after it.** First, one line that starts with "How to read:" and says what the boxes, arrows, axes, or colors mean. Second, one sentence of conclusion that states what the visual shows. The reader should never have to work out the point of a picture, because that work is the load the picture was meant to remove.

**Pick the form by the content, and never draw a sequence.** A sequence of steps with no branch is a numbered list or an HTML stepper, never a diagram. Boxes in a row repeat the prose and show no relation.

A real graph (branches, merges, a concept map) becomes inline SVG with the page's theme tokens. Mermaid is only for a simple linear flow that must stay in Markdown, with the phone rules below. Up to about 8 actors and their links become an inline SVG map, with the relation written on the arrow.

Numbers to compare become an inline SVG chart (load the `dataviz` skill first) or a table. Many actors with several attributes each become a table. A big group with dozens of members shows only the members the text names, at most 8, plus one node "and N others". Dated events become an HTML timeline, never a diagram, because the text must wrap on a phone.

Every diagram must add a relation that the prose carries badly. A diagram that only repeats the prose is cut. The lint warns on a Mermaid flowchart whose nodes form one chain (`sequence-as-diagram`).

**Build it for a phone.** Keep every diagram label at 25 characters or fewer, with no line break inside it and at most 2 nodes side by side. For an HTML page, `references/html-patterns.md` has the snippets.

**Three limits.**

- No decorative visuals, because an image that adds no relation adds only load.
- At most one manipulable interactive (a slider, a toggle, a step-through) per document, because each one costs attention. The text must carry the idea anyway.
- A health risk is always a natural frequency in words ("3 em cada 100 pessoas"), never a relative risk alone. When the four-question test says the risk earns a visual, draw it as an icon array: a grid of 100 small figures with the affected ones filled in. In HTML, use the snippet in `references/html-patterns.md`; in Markdown, a 10-by-10 grid of ● and ○ inside a code block, with its "How to read" line.

### Rule 8: Depth with low cognitive load
Cover the topic in real depth, but deliver it in small logical steps. Prefer step-by-step explanation and examples over abstract theory. Never write one large wall of text, because that is exactly where a distracted reader gives up.

Calibrate the depth to what the reader knows about this topic, not to their field. An IT professional does not know every IT topic: the reader this skill serves asked for DuckDB and got a text that "assumed I knew everything", because the old rule read "IT" as "knows the basics". So the default is the full scaffold, for every topic.

1. **Default: full scaffold.** Open the text with the section "What to know before reading" ("O que saber antes de ler"): the key terms, the background, and an example before each abstract rule. This holds for a topic inside the reader's field as much as outside it. Example: the reader asks how a generic medicine proves that it is equivalent to the brand. The text opens with "O que saber antes de ler", explains what the active ingredient is (princípio ativo) and what "equivalent" means for a medicine (bioequivalência), gives one example of a test, and only then comes the first rule on how the proof works.
2. **Cut the basics only on an explicit signal.** When the request says the reader knows the basics ("já sei o que é um cache HTTP", "uso DuckDB todo dia"), keep them to one sentence or one collapsed block the reader can skip. Explaining what the reader already knows also costs attention: the expertise reversal effect, described in a 2003 review by Kalyuga, Ayres, Chandler and Sweller (`references/research-basis.md`, section 9.2). The collapsed block is the compromise: the expert skips it, the newcomer opens it. Example, with the signal "já sei o que é um cache HTTP": "Um cache HTTP guarda uma cópia da resposta para não voltar ao servidor." One sentence, and the text moves on to how the cache decides that the copy is still valid.
3. **Another reader, with no field named.** When the user writes for someone else ("para minha irmã", "para o time de vendas"), the default holds: full scaffold. A field name alone ("é para um dev") is not a signal; only a statement about the topic is.

The same request shape, "explain how X proves that Y", gets the section unless the request carries the signal. Test 19 in `references/tests.md` checks the three runs.

### Rule 9: Tone
Stay calm, precise, and straightforward. Each of the two rules below has its own evidence.

1. **No ornament that does not serve a concept.** A joke, a flourish, or a curiosity that teaches nothing about a main idea is cut, or moved to an optional depth block. Interesting but irrelevant additions lower learning of the main content. That is the seductive-details effect, from a 2020 meta-analysis by Sundararajan and Adesope (`references/research-basis.md`, section 8.2). Cut: "Curiosidade: a palavra cache vem do francês." Keep: "O cache guarda uma cópia, e o banco descansa." Cut also the empty words: evaluative ones that carry no fact ("crucial", "robust", "powerful"; "crucial", "robusto", "poderoso") and meta-concepts that name nothing ("at the level of", "approach", "aspect"; "a nível de", "abordagem", "aspecto"). Say the fact the word was hiding, or drop it. The language packs list the words, and the lint warns on each (`empty-word`).
2. **Write as in a work email to a colleague.** Address the reader directly as "you" ("você"), say who claims what, and use the words you would use at work. Speaking to the reader is not ornament. A 2013 meta-analysis of conversational style, by Ginns, Martin and Marsh, found better retention and transfer in short lessons when the text speaks to the reader. It is in `references/research-basis.md`, section 10.1. Weak: "The user must ensure that the token is renewed before expiry." Strong: "You renew the token before it expires."

### Rule 10: Language
Write in the reader's language. Use plain words of that language. Avoid idioms and metaphors in any language, because they are extra work for a tired reader and can mislead. When a concept is hard, add a short gloss in parentheses. When you write in the reader's second language, the gloss may be in the native language, since a familiar word can anchor a hard idea faster than any paraphrase.

Plain words are about the form, never about the content. Keep every idea, every number, every caveat and every precise term. Simplify the sentence, not the thought. When the exact term is the right word (a legal, medical or technical term), keep it and explain it once; do not swap it for a vaguer word, because the reader loses precision and gains nothing. A text that got shorter by dropping ideas failed this rule, however easy it reads.

**The six fixed labels follow the reader's language.** The method uses six fixed labels, and each one has one form per language. The rules in this file quote the English form, so when you write in Portuguese, write the Portuguese form, every time:

- "Key point" and "Ponto-chave"
- "Where the analogy fails" and "Onde a analogia falha"
- "What works" and "O que funciona"
- "How to read" and "Como ler"
- "You already know... Now..." and "Você já sabe que... Agora..."
- "What to know before reading" and "O que saber antes de ler" (the opening section of Rule 8)

A label in the wrong language is a foreign word in the reader's text. The reader stops at it, so the label costs the attention it was meant to save.

Weak, in a Portuguese text: "Key point: o cache responde primeiro." Strong: "Ponto-chave: o cache responde primeiro." The lint flags the wrong form as a problem.

Each language has its own pack in `references/`: `lang-pt-br.md` for Brazilian Portuguese and `lang-en.md` for English. Read the pack for the reader's language before you write. It carries what the eleven rules cannot say for every language at once: the plain-language standard behind the rules, the acronyms that need no expansion, the number and date forms, and the English terms that stay in English. The standard is ISO 24495-1:2023, the international one, and each country applies it in its own way: ABNT NBR ISO 24495-1:2024 and Lei 15.263 in Brazil, the Federal Plain Language Guidelines in the United States. For another language, write by the eleven rules and say which parts of the pack you could not apply.

Make numbers easy too. Reinforce a bare number with words that say what it means, because a raw figure carries no meaning on its own. For example: "permission 600 (owner can read and write, nobody else can touch it)". Write the month as a word, such as "3 June 2026" or "3 de junho de 2026", so a date is never ambiguous across regions.

For emphasis use bold, and avoid italics and underlining: italics crowd letters together and tire the eye, and underlines look like links. Bold at most one line per block, the one that carries the point, so that reading only the bold lines tells the whole story. Never bold the beginnings of words (the "Bionic Reading" format): two reading studies, by Snell (2024) and by Parker and colleagues (2026), found no gain in reading speed, and the one that measured comprehension found no gain there either.

### Rule 11: Procedures and code
Steps are where a tired reader most often gets lost, so give a procedure its own clear shape. Use a numbered list, with one action per step, and state the goal of the step before the action. For example, write "to give the server your key, run…", not the reverse. Keep a procedure to about seven steps; if it runs longer, split it into stages with their own headings.

Handle choices with an explicit "if / then" split rather than a buried clause, because a conditional hidden mid-sentence is easy to miss. For example: "If `ssh-copy-id` is installed, then run it; if it is not, then copy the key by hand." Three or more branches become a two-column if/then table, in any text, not only in a procedure.

Show code so it cannot be confused with prose. Put each command on its own line in a code block, never inside a sentence, and follow it with one plain line saying what it does and what the reader should expect to see. Do not put an instruction only inside a screenshot or image, because the reader may not be able to see or parse it.

Key point: each rule exists to remove one kind of reading effort, so apply them together, not as a checklist.

---

## Before you deliver: run the lint

When the output is a file, run the lint from the skill folder before you hand the file over:

```bash
python3 scripts/lint_clear_read.py path/to/document.md
```

It prints one line per finding and ends with `N problems`. A **problem** is a rule break, so fix every one: a dash as a joiner, a sentence over 25 words, a block over 4 sentences, a backward reference, a bare label, a visual with no "How to read" line, an analogy with no limit line, and a fixed label in the wrong language. A **warning** asks you to re-read the line and keep it only on purpose: passives, hidden verbs, inserted clauses, acronyms and names without their role, one-word headings, sections without a Key point. `references/lint.md` lists all twenty findings with the rule behind each one, and the phone check for Mermaid diagrams (`scripts/check_mermaid.cjs`), which you run whenever the document has a diagram.

When the output is a chat reply, apply the same checks by eye, because the list is short enough to hold in mind.

Key point: the lint catches the slips that are easy to make and hard to see, so run it before the reader finds them.

---

## What "arc" means in practice

The text must have a beginning, a middle, and an arrival. Each section builds on the one before, so the order matters and the piece cannot be read in any order. The reader should feel guided through a journey. The final section should feel like a resolved understanding, where everything clicks into place, not just the last item on a list.

Key point: when the last line lands, the reader should feel finished, not merely stopped.

---

## Why these rules work (reference)

The rules come from research on attention difficulties, plain-language writing, and second-language reading. When a rule feels excessive, or someone pushes back on it, read `references/research-basis.md`: it opens with a map from each rule to its evidence, with the certainty and the date each source was checked. When the reader asks where a rule comes from, answer from that map, with the source, the certainty and the date; `scripts/check_research_basis.py` keeps the map complete. After any change to the skill, run `references/tests.md`, `scripts/test_lint_clear_read.py` and the Mermaid `--self-test`.

The files in `references/` and `scripts/`, and when to read each one:

| File | Read it when |
|---|---|
| `references/lang-pt-br.md` | The reader's language is Portuguese |
| `references/lang-en.md` | The reader's language is English |
| `references/html-patterns.md` | The output is an HTML page |
| `references/research-basis.md` | A rule needs its evidence, or someone pushes back on it |
| `references/tests.md` | You changed the skill, or you want to test a document with a cold reader |
| `references/lint.md` | You want the full list of what the lint reports |
| `scripts/lint_clear_read.py` | Before you deliver any file |
| `scripts/check_mermaid.cjs` | Before you deliver a file with Mermaid diagrams |
