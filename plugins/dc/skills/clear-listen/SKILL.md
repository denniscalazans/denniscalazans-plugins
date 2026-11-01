---
name: "clear-listen"
description: "Use when the output will be heard: a narration, the audio version of a guide, a podcast or two-host dialogue, an audio summary, a voice-over, any text-to-speech script, or one turn of a live voice conversation that an engine will speak. Triggers: \"quero ouvir\", \"versão em áudio\", \"narra isso\", \"faz um podcast disso\", \"resumo em áudio\", \"read this to me\". Not for screen-only text (use clear-read) or for transcribing audio."
---

# Clear-Listen

This skill serves one listener. It is the sibling of clear-read. Clear-read removes the effort of reading. Clear-listen removes the effort of listening.

Never produce audio by reading a clear-read text aloud. A text that is easy for the eye is often hard for the ear, because the ear loses everything that clear-read relies on: headings, bold, line breaks, tables, diagrams, parentheses, and the option to look back.

## Who you are writing for

The listener is the clear-read reader, now with headphones.

- They are an IT professional, so they are smart and can handle real depth.
- They have ADHD tendencies, so attention drifts, and it drifts more while listening than while reading.
- They are often tired, in a noisy place, or doing something else at the same time (walking, commuting, housework).
- They listen in their native language, so the second-language load of clear-read is gone. The attention load is larger.

**Who is speaking:** someone telling a good story to a friend. They deliver the whole thing, pull the listener forward with what comes next, and repeat the essential as friends remembering together ("lembra que o navegador guarda uma cópia?"). They never show the skeleton: no "são cinco pontos", no "primeiro, segundo". A teacher with slides does the opposite. Rule 1's spoken map and Rule 3's item marks are the exceptions: each replaces a heading the ear cannot see. One limit comes from a 2021 meta-analysis of 78 samples and 33,078 people, by Mar, Li, Nguyen and Ta. Narrative helps memory more than it helps understanding. So a mechanism still gets its step by step, in the order it happens.

**The one goal:** the listener gets every main idea on the first listen, with no rewinding. When the mind drifts and comes back, the listener knows within a few seconds where they are and what the current part is about. When a rule and this goal seem to conflict, the goal wins.

## Conversation by voice

This section is for one turn of a live voice conversation: the person speaks, you answer in about 30 seconds, and a voice engine reads the answer exactly as written. Text chat stays in clear-read. The four phases of a recorded audio do not apply to a turn: no producer note, no engine profile, no rendering. The turn is plain text that the engine speaks as written, so every character you write is heard. The other rules of this skill hold, with these limits.

1. **Answer first, in up to 3 sentences, before any structure.** Six sentences is the ceiling. Offer the rest instead of squeezing it in.
2. **Keep each sentence at 8 to 15 words.** The ceiling of 20 holds.
3. **Put a connector at every link.** "Por isso", "mas", "ou seja". Two facts side by side are two facts.
4. **Start from what the person just said**, in their words. "Você perguntou se o cache guarda a página. Guarda, mas confere antes de usar."
5. **Say the role before the name, and the name right after.** "Um estudo de dois mil e vinte e três, de Stern e Halamish, mostrou que..." A bare "um pesquisador mostrou" makes a smart listener ask which one. When you lack the name, say so.
6. **Never point backward.** Say the thing again, with the person's own words.
7. **Make every sentence a safe stopping point.** The person may interrupt after any sentence and still hold a whole idea.
8. **Past 3 sentences, end with a short question that gives the turn back.** No pause mark: a 4 to 6 second silence sounds like the end of the turn, and the person talks over it. "Quer que eu explique como o servidor manda essa etiqueta?"
9. **Redefine a term when it returns after 3 exchanges**, in the same words as the first time.
10. **Announce structure only through content.** "Agora, o que fazer com isso." Never "São três pontos" or "Parte um de dois": a count is a promise the ear must hold.
11. **Never number. One step per turn, the next when the person asks.** No "primeiro, segundo", no "1.": the engine reads the digit or drops it. Goal, then action, like a navigation app. "Agora, abra o terminal. Me avisa quando estiver aberto."
12. **Say the skeleton in one sentence, in place of the visual.** "Imagine três caixas: o navegador, o cache e o servidor." Then offer the drawing in writing.
13. **Name the problem, and the way out in the next sentence.** "O cache pode servir uma cópia velha. A saída é a etiqueta de versão, que o servidor confere antes de usar." A problem alone adds worry; the way out, right after, closes it.
14. **Punctuation is the only sound control.** No square brackets, no delivery intents, no bold, no italics, no backticks, no markdown. A period is the pause, a short sentence is the stress. The engine reads the mark or drops it, and both cost the listener.

Before the turn is spoken, run `python3 scripts/lint_audio_script.py <turn.txt> --conversa`. It fails on any square bracket, part marker, bare ordinal, list line or heading, on more than 6 sentences, and on more than 3 sentences without a closing question.

## Why the ear needs its own rules

Speech disappears, the pace is not the listener's, the mind wanders more while listening, visual structure is gone, and the voice carries meaning. These five facts drive every rule below; `references/research-basis.md` opens with them and holds the evidence.

## What the audio is for

The audio is a first pass (to get the gist before reading) or a review (after reading). It never replaces the written text for content that needs step-by-step reasoning.

So decide, for each piece of content:

- **Main ideas, causes, examples, the conclusion:** in the audio.
- **Long chains of reasoning, tables, comparisons with many numbers, code, procedures:** summarized in one or two sentences, with a pointer in words ("o detalhe está no guia escrito").

What fits whole in the audio: the main idea of each section, a structure of up to 3 or 4 items, a comparison of 2 options, up to 1 number per sentence, and a risk said as a natural frequency.

What does not fit: a table bigger than 3 by 3, code, a procedure with more than 5 steps, and a network with more than 6 nodes. For these, the audio says the conclusion, the main pattern, and where the rest is (Rules 16 to 21, in `references/visuals-for-the-ear.md`).

## Two layers: what the voice does, and how the medium does it

This skill separates two things that are easy to mix up.

- **What the voice should do** is decided here: where it pauses, which tone a part has, which word carries the stress, how a hard name sounds. The script states these as **delivery intents**, in a small neutral vocabulary (see "Delivery intents").
- **How a medium does it** is not decided here. One voice engine uses inline tags, another uses a separate instruction field, another uses SSML, and a human reader needs stage notes. Even two models of the same vendor differ. That knowledge lives in an **engine profile** that the environment supplies (see "Phase 4").

So the neutral script is the source of truth, and it never contains the syntax of one engine. Changing the engine, or the model, means rendering the same script again. It never means rewriting the script.

## Without reasoning and without tools

With only this file, no search, no engine profile, no lint: three substitutes.

1. **Only facts from the user's source**, and "a fonte não diz" for the rest. Open the producer note with "facts not verified in this session". No source text: ask for one, never write from memory.
2. **Render plain when there is no engine profile** (`references/rendering.md`). Never fill the profile from memory as fact: hand it to the user blank, or mark every line as a guess to test, as `references/rendering.md` says, and render plain until it returns.
3. **The lint's checks by hand**, in one producer note, which says the lint and cold reader did not run.
   - Read each part aloud; a stumble is the listener's.
   - Over 20 words: split.
   - A parenthesis: its own sentence.
   - A digit, symbol, address or code: words.
   - A dash: two sentences or a connector.
   - "Como eu disse": say it again.
   - Filler ("Exato!"): the key point instead.
   - Part marker missing or in digits: "Parte dois de três".
   - No recall question per part: add one, pause, answer.
   - Over two closing questions: one recall plus "Sem voltar".
   - A part over 800 words: split.
   - Each main idea has its sentence.
   - A relative risk ("o dobro") without its base ("em cada cem"): add the base.
   - A `[key]` on the first line after a voice change: a transition line first.
   - A tag outside the intents table: cut it, or fix the sentence.
   - A part that opens slow (`[key]` or `[pause long]` first): move it.
   - No closing question about the whole audio: add "Sem voltar...".

## Four phases

Work in order: source, design, write, render. The neutral script and its rendered form are the output.

### Phase 1: Source

The script adds no new fact. Its source is a verified text: a clear-read guide, or content checked with the clear-read research phase. If no verified source exists, run clear-read Phase 1 first.

### Phase 2: Design (scratchpad)

1. **Main concepts.** The 3 to 5 ideas the listener must keep. One part per concept.
2. **Parts.** Each part is 3 to 4 minutes (range 2 to 5). Plan: re-entry line, goal sentence, content, recall question, key point.
   - **Core idea.** Write the single core idea of the whole audio in one sentence. It goes into the first 30 seconds, and it returns at the start of each later part.
3. **Spoken names.** For each term, decide the one name you will say every time, and one short meaning to repeat with it. Also decide how each technical term, acronym or code-like name sounds aloud, and write it that way (a header such as `Cache-Control` becomes "a instrução cache control"). Syntax is never read: say what the thing does.
4. **Cuts and coverage.** List what stays in the written text only, with the fit list in "What the audio is for". Then check the other direction: every main idea of the source has a sentence in the script. A main idea that lives only in a table or a chart of the source still gets its spoken sentence (Rule 16, in `references/visuals-for-the-ear.md`).
5. **Questions.** One prequestion per main concept for the opening. One recall question per part. One closing question about the whole audio, after the last part.
6. **Delivery.** One tone intent per part, from the vocabulary in "Delivery intents" (for example warm, curious, serious), so the voice changes between parts. Also plan the stressed term of each part, and every hard name that needs a pronunciation. Change the *kind* of novelty from part to part (a question, an example, a contrast, a voice change), because the same device repeated stops working.
7. **Medium.** Name the medium this audio will be produced with: which voice engine and model, or a human reader. Ask the environment, not your memory (Phase 4; `references/rendering.md`, step 1). The medium does not change the writing. It only decides the rendering, and the measured rate you plan with.
8. **Length.** Target length in minutes, then words. Use the measured rate of the chosen voice on the chosen medium. Until it is measured, plan with 160 words per minute for Brazilian Portuguese (range 150 to 175). Never copy an English or Spanish words-per-minute target: Portuguese words have about 2.1 syllables, English words about 1.4, so the same number means a different speed.

### Phase 3: Write

#### Rule 1: Short standalone parts, with a spoken map and the core idea first
Open the audio with what it is about, why it matters, and how many parts it has. **Say the core idea within the first 30 seconds**, because a mind that wanders early misses the foundation for everything after. Start each part with "Parte N de M", then a **re-entry line**: one sentence that makes sense without the earlier parts and re-anchors the core idea ("Agora, a segunda causa do problema: ..."). Then the goal of the part in one sentence. Keep each part to 3 or 4 minutes, and never over 5.

A part is one main concept, not a time slot. When the source is short, the parts are short. Never pad a part to reach a length. An audio with a single part (a one-minute recap, or one concept on request) skips the part count and the "Parte N de M" line, because announcing "part one of one" is noise. It still opens with the core idea and still ends with the takeaway.

#### Rule 2: One idea per sentence, sayable in one breath
Aim for 8 to 15 words. Ceiling: 20. Subject, verb, complement, in that order. No clause inserted in the middle of another. **No parentheses and no brackets with content**, because the ear cannot hear them: a definition becomes its own sentence. If you run out of air reading a sentence aloud, split it.

#### Rule 3: Say the structure
Headings do not exist in audio, so speak them. Announce the count before a list ("São três motivos."). Mark each item ("O primeiro.", "Agora, o segundo."). Mark every turn ("Até aqui, o problema. Agora, a solução."). Never list more than three items in a row without a recap.

#### Rule 4: Repeat on purpose
In text, repetition is waste. In audio, repetition is the listener's only way to look back.
- Repeat the **name** instead of "isso", "ele" or "esse ponto". Use the same name every time.
- Repeat the **meaning** of a term the first time it appears in each part.
- Repeat the **key point** at the end of each part, in different words from the first time. A restatement is a second route to the idea. A word-for-word echo is wasted time for an expert listener.
- Never point backward ("como eu disse", "o segundo item"). Say the thing again.

#### Rule 5: Say every "because"
The first thing a drifting listener loses is the link between facts. So state each causal link in words ("por isso", "o motivo é", "como resultado"), and state the conclusion yourself. Do not leave an inference for the listener to make.

#### Rule 6: Make the listener retrieve, in the head
Open with one or two prequestions, each followed by a pause. Close the audio with "Sem voltar, quais foram as ideias principais?", a recall pause, then the list. This closing question is the proven part of the rule: in a study with 36 university students with ADHD and 36 without (Stern and Halamish 2023), recalling the whole text once at the end beat recalling it section by section. Every script of more than one part has it, and the lint checks for it. Also close each part with **one** recall question, a recall pause (the `[pause recall]` intent, 4 to 6 seconds), then the answer in one sentence. The question per part is practice, not proof: it is the condition that lost in that study, and the listener's own test decides whether it stays (`references/tests.md`, test 10). The 4 to 6 second pause is a practice default too, because no study measured the pause length. Every question must be answerable in one short phrase, silently, while walking, because this listener has no hands free and will not write. The learning benefit of built-in questions is solid, also for students with ADHD. The attention benefit is likely but less certain. Students with ADHD test themselves less on their own, so the audio does the prompting.

#### Rule 7: Few numbers, in words
At most one number per sentence. Round it unless the exact value is the point. Give it an anchor ("quase um terço"). Write numbers, dates, units and symbols as words, so the voice cannot misread them. Never read a URL, a citation, or a table.

#### Rule 8: Talk to one person
Write as one person explaining to one person: "você", active voice, everyday words, the present tense. Not a lecture, and not a text being read. Mark who says what in words ("O autor defende que...", "Um estudo de 2024 mostra...").

#### Rule 9: Keep a moderate pace, and pause between ideas
Do not slow the voice down to make it "clear". Recall is best at a moderate rate, and worse when speech is slow or fast. For Brazilian Portuguese the target is about 160 words per minute (range 150 to 175, which is about 5.5 to 6 syllables per second with pauses). Give thinking time with **pauses between ideas** (`[pause short]`, about half a second), a longer pause at each part boundary (`[pause long]`, about 2 seconds), and slow words only on the key point of a part (`[key]`). Produce the audio at normal speed, and tell the listener that changing the player speed is fine: up to about 1.5 times costs little, and choosing your own speed goes with less mind wandering.

#### Rule 10: Moderate expression, varied between parts
A flat voice loses the listener, and an over-acted voice loses credibility. The best results come from moderate intonation at a medium rate. Change the tone intent between parts, let pitch move, and stress 1 or 2 words per sentence at most (3 to 5 key terms per part). Mark only the most important of them with `[stress: ...]`, at most one per part, and let word order carry the others. Stress on everything is the same as stress on nothing. Calm does not mean flat.

#### Rule 11: Voice only, clean signal
No music, no ambience and no sound effects under the voice. This holds even when the medium can generate them: a capability of the engine is not a reason to use it. Background sound makes speech harder to follow, more so for a listener with ADHD in a noisy place. Keep the level constant, and help a noisy environment with repeated key terms, not with loudness. If a jingle is ever used, it plays alone, before or after the speech. Never mix white or pink noise into the audio. If the listener wants to try noise, he adds it himself and tests it.

#### Rule 12: One clean, constant voice per role
Each role keeps its voice inside an audio and between audios of the same series. A modern synthetic voice gives the same learning as a human voice in the studies that exist, but those used English voices. So check the chosen Portuguese voice by ear for naturalness, and replace a voice that sounds rough, robotic or unstable. After generating, **measure the real rate** (words divided by minutes of audio), because a voice engine's speed setting is not words per minute.

#### Rule 13: A second voice must earn its place
In a two-host script, the second host asks the deep question a smart listener would ask ("por quê?", "como?", "e se...?") **before** the explanation, and voices the common wrong belief so the first host can correct it. No banter, no jokes, and no agreement noises ("Isso.", "Exato!", "Legal."). When the second host summarizes back, the first host answers with the key point itself, not with a confirmation. Each exchange moves a main concept forward.

A change of voice pulls attention back, and the listener loses the first 3 seconds of what follows it. So the important sentence never comes right after a voice change: a transition sentence comes first, then the point. Keep the changes few in each part, because the loss grows with the number of changes. Choose two voices with clearly different pitch, and bring the second voice in early, so the listener knows who is who from the start. Always write the dialogue yourself. Automatic two-host generators add chat and ignore these rules.

The lint check `key-after-voice-change` fails a `[key]` on the first line of a new speaker. The example below passes it: the Guia opens with a transition line, and the key point comes on the second line.

```
# Modo: diálogo. Papéis: Guia e Curioso.
Curioso: Então no-cache significa não guardar?
Guia: Essa é a dúvida mais comum, e a resposta surpreende.
Guia: No-cache significa guardar, mas conferir a etiqueta de versão antes de cada uso.
[pause short]
Curioso: E quem proíbe guardar?
Guia: Essa é outra instrução.
Guia: [key] Quem proíbe guardar é no-store, e no-cache só manda conferir.
```

#### Rule 14: Stimulation from form, not from extra content
Novelty keeps this listener engaged, but an interesting side fact hurts learning. So get novelty from the voice change, a question, a speaker change, a contrast, or a concrete example. Never from a detail that serves no main concept. Rotate the devices, because an identical device repeated many times stops catching attention.

#### Rule 15: Land the ending, and name the moment to review
The last part connects the main concepts in a few sentences and gives one thing to remember. The listener should feel finished, not cut off. For later review, reviewing close to the moment of use helps: in a memory study by Murphy and colleagues (2022; 231 students, recorded lectures of 13 to 15 minutes), a second full viewing at 2 times speed right before the test gave the best recall. Nobody has tested the format of the review, a short summary or a re-listen. So offer the review and name the moment ("ouça de novo antes da reunião"), and leave the format to the listener.

#### Rules 16 to 21: what the eye had in a table, a chart, a diagram or code
Every main idea of the source gets its own spoken sentence, even when the source carries it in a table, a chart or a diagram (Rule 16). Details may point to the written guide; a main idea never may. When the source has a table, a chart, a diagram, code, or a procedure with more than five steps, read `references/visuals-for-the-ear.md` before writing that part: it has the six rules, with the spoken shape for each form, the risk as a natural frequency with its denominator (Rule 20), and the honest limit said out loud (Rule 21).

Key point: each rule replaces something the eye had for free, so apply them together.

## What "arc" means in audio

The script still moves from what the listener knows to what they understand at the end. However, the arc must survive drifting. So the arc is rebuilt at the start of every part, in one sentence.

## Script format

The neutral script is a plain text file. A person can read it aloud as it is, and any voice engine can speak it after rendering (Phase 4). The lint script depends on this format.

- One sentence per line. A blank line between parts.
- A line starting with `#` is a note for the producer. It is never spoken. Start the file with a note that names the mode and the roles. Do not name a voice engine here, because the same script serves every medium.
- A delivery intent goes in square brackets, for example `[curious]` or `[pause short]`. Nothing inside brackets is spoken. Use only the vocabulary in "Delivery intents". Never write the syntax of one engine in this file.
- In a dialogue, each line starts with the role and a colon: `Guia:` or `Curioso:`.
- Each part starts with "Parte um de três" (numbers as words), except in a single-part audio.
- Put the note `# closing` before the final recall and takeaway, so the last part ends cleanly before them.

## Delivery intents

A delivery intent says what the voice should do, in words that mean the same on every medium. The vocabulary is small on purpose: a small set can be mapped to any engine, and it keeps the delivery moderate (Rule 10).

Write intents in English, in square brackets. A tone intent and `[key]` sit at the start of the sentence they affect. A tone intent holds until the next tone intent. The other intents sit alone on their own line, right before the sentence they affect.

| Intent | Write | Meaning for the listener |
|---|---|---|
| Tone | `[warm]`, `[curious]`, `[serious]`, `[thoughtful]`, `[inviting]` | The attitude of the passage. `[warm]` is the default for explanation. One per part, plus one more only where the tone really turns |
| Tone, dialogue only | `[surprised]`, `[amused]` | A short reaction of the second host. Never a laugh written as words |
| Key point | `[key]` | This sentence is the key point of the part: a little slower, with weight. At most one per part |
| Stress | `[stress: palavra]` | That word, in the next sentence, carries the stress. At most one per part |
| Short pause | `[pause short]` | About half a second, between two ideas |
| Long pause | `[pause long]` | About 2 seconds, at a part boundary or before a turn in the argument |
| Recall pause | `[pause recall]` | 4 to 6 seconds of silence after a recall question, so the listener can answer in the head |
| Pronunciation | `[say: termo = respelling]` | How a hard name in the next sentence sounds, written as a respelling in the listener's language. Add the phonetic alphabet form after a second `=` when you know it: `[say: cache = quéche = /kæʃ/]` |

Six rules for intents live in `references/intents.md`. The short form: intents never carry content, so a dropped intent costs polish and never meaning; never invent an intent, fix the sentence instead; never open a part with a slow direction, slowness belongs to `[key]` only; speaker roles are not intents; performance (`[perform: whispering]`) only when the user asks for a demonstration; and older `[short pause]` and `[long pause]` read as `[pause short]` and `[pause long]`.

## Phase 4: Render for the medium

Rendering turns the neutral script into what one medium needs. It changes marks, never words. How one medium does each intent lives in an **engine profile** that the environment supplies, one per engine and model. Read `references/rendering.md` before generating audio: it has the four steps, what a profile must answer, the degradation ladder, the render rules, and one passage rendered for three media.

## Examples

Two worked examples live in `references/examples.md`: the same passage written for the eye and for the ear, and a table and a chart said aloud (Rules 18 and 19 in `references/visuals-for-the-ear.md`). Read them the first time you write a script.

## Check before generating

Run `scripts/lint_audio_script.py <script.md>` on the **neutral script** and fix every failure. Do not lint the rendered text, because an engine's own marks are not part of the format. Then read the script aloud once, or at least read one part aloud. If you stumble, the listener will too.

Then check coverage (Rule 16): list the main ideas of the source and point to the sentence of the script that carries each one. When possible, give the script alone to a cold reader and ask the main questions; the reader should answer at least eight in ten.

Then check the rendering, as `references/rendering.md` says: every intent is mapped, degraded or dropped on purpose, and `scripts/check_render.py <rendered.txt>` passes on the rendered text.

## Why these rules work

Read `references/research-basis.md` for the evidence, the trade-offs, and what is still unknown. Run the checks in `references/tests.md` after any change to this skill.
