---
name: "clear-listen"
description: "Use when the output will be heard: a narration, the audio version of a guide, a podcast or two-host dialogue, an audio summary, a voice-over, or any text-to-speech script. Triggers: \"quero ouvir\", \"versão em áudio\", \"narra isso\", \"faz um podcast disso\", \"resumo em áudio\", \"read this to me\". Not for screen-only text (use clear-read) or for transcribing audio."
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

**The one goal:** the listener gets every main idea on the first listen, with no rewinding. When the mind drifts and comes back, the listener knows within a few seconds where they are and what the current part is about. When a rule and this goal seem to conflict, the goal wins.

## Why the ear needs its own rules

Five facts about listening drive every rule below. `references/research-basis.md` has the evidence.

1. **Speech disappears.** A reader can look back. A listener holds everything in working memory, so long or dense speech overloads it.
2. **The pace is not the listener's.** A reader slows down on a hard sentence. A listener cannot. On average, listening and reading give the same comprehension. However, reading wins when the reader sets the pace, when the text explains something, and when the question needs inference. Explanatory audio is all three.
3. **The mind wanders more while listening** than while reading. In adults with ADHD, mind wandering is the path to poorer comprehension, and structure given step by step closes the gap. Wandering near the start does the most damage.
4. **Visual structure is gone.** Structure must be said out loud, or it does not exist.
5. **The voice carries meaning.** Pace, pauses and pitch change what is noticed and what is remembered.

## What the audio is for

The audio is a first pass (to get the gist before reading) or a review (after reading). It never replaces the written text for content that needs step-by-step reasoning.

So decide, for each piece of content:

- **Main ideas, causes, examples, the conclusion:** in the audio.
- **Long chains of reasoning, tables, comparisons with many numbers, code, procedures:** summarized in one or two sentences, with a pointer in words ("o detalhe está no guia escrito").

What fits whole in the audio: the main idea of each section, a structure of up to 3 or 4 items, a comparison of 2 options, up to 1 number per sentence, and a risk said as a natural frequency.

What does not fit: a table bigger than 3 by 3, code, a procedure with more than 5 steps, and a network with more than 6 nodes. For these, the audio says the conclusion, the main pattern, and where the rest is (Rules 16 to 21).

## Two layers: what the voice does, and how the medium does it

This skill separates two things that are easy to mix up.

- **What the voice should do** is decided here: where it pauses, which tone a part has, which word carries the stress, how a hard name sounds. The script states these as **delivery intents**, in a small neutral vocabulary (see "Delivery intents").
- **How a medium does it** is not decided here. One voice engine uses inline tags, another uses a separate instruction field, another uses SSML, and a human reader needs stage notes. Even two models of the same vendor differ. That knowledge lives in an **engine profile** that the environment supplies (see "Phase 4").

So the neutral script is the source of truth, and it never contains the syntax of one engine. Changing the engine, or the model, means rendering the same script again. It never means rewriting the script.

## Four phases

Work in order: source, design, write, render. The neutral script and its rendered form are the output.

### Phase 1: Source

The script adds no new fact. Its source is a verified text: a clear-read guide, or content checked with the clear-read research phase. If no verified source exists, run clear-read Phase 1 first.

### Phase 2: Design (scratchpad)

1. **Main concepts.** The 3 to 5 ideas the listener must keep. One part per concept.
2. **Parts.** Each part is 3 to 4 minutes (range 2 to 5). Plan: re-entry line, goal sentence, content, recall question, key point.
   - **Core idea.** Write the single core idea of the whole audio in one sentence. It goes into the first 30 seconds, and it returns at the start of each later part.
3. **Spoken names.** For each term, decide the one name you will say every time, and one short meaning to repeat with it. Also decide how each technical term, acronym or code-like name sounds aloud, and write it that way (a header such as `Cache-Control` becomes "a instrução cache control"). Syntax is never read: say what the thing does.
4. **Cuts and coverage.** List what stays in the written text only, with the fit list in "What the audio is for". Then check the other direction: every main idea of the source has a sentence in the script. A main idea that lives only in a table or a chart of the source still gets its spoken sentence (Rule 16).
5. **Questions.** One prequestion per main concept for the opening. One recall question per part.
6. **Delivery.** One tone intent per part, from the vocabulary in "Delivery intents" (for example warm, curious, serious), so the voice changes between parts. Also plan the stressed term of each part, and every hard name that needs a pronunciation. Change the *kind* of novelty from part to part (a question, an example, a contrast, a voice change), because the same device repeated stops working.
7. **Medium.** Name the medium this audio will be produced with: which voice engine and model, or a human reader. Ask the environment, not your memory (Phase 4, step 1). The medium does not change the writing. It only decides the rendering, and the measured rate you plan with.
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
Open with one or two prequestions, each followed by a pause. Close each part with **one** recall question, a recall pause (the `[pause recall]` intent, 4 to 6 seconds), then the answer in one sentence. Close the audio with "Sem voltar, quais foram as ideias principais?", a pause, then the list. Every question must be answerable in one short phrase, silently, while walking, because this listener has no hands free and will not write. The learning benefit of built-in questions is solid, also for students with ADHD. The attention benefit is likely but less certain. Students with ADHD test themselves less on their own, so the audio does the prompting.

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

A change of voice pulls attention back, and memory is better for what comes right after it. So place the important sentence right after a voice change, choose two voices with clearly different pitch, and bring the second voice in early. Always write the dialogue yourself. Automatic two-host generators add chat and ignore these rules.

#### Rule 14: Stimulation from form, not from extra content
Novelty keeps this listener engaged, but an interesting side fact hurts learning. So get novelty from the voice change, a question, a speaker change, a contrast, or a concrete example. Never from a detail that serves no main concept. Rotate the devices, because an identical device repeated many times stops catching attention.

#### Rule 15: Land the ending, and offer a short review
The last part connects the main concepts in a few sentences and gives one thing to remember. The listener should feel finished, not cut off. For later review, a separate summary of 2 to 4 minutes, heard close to when the knowledge is needed, works better than a second full listen at high speed.

#### Rule 16: Main ideas are always carried by the audio
Every main idea of the source gets its own spoken sentence, even when the source carries it in a table, a chart or a diagram. Details may point to the written guide; a main idea never may. The test: a listener who never opens the guide still leaves with every main idea. A cold-reader check of the script (someone who answers the main questions from the script alone) is the proof.

#### Rule 17: Say structures, not pixels
A diagram becomes a spoken shape of at most 3 or 4 items: "Imagine três caixas, da esquerda para a direita. A primeira é...". Say what connects to what and in which direction. Never describe colors, positions or sizes for their own sake. A structure with more than 4 items is cut to its spine, and the rest goes to the guide (Rule 21).

#### Rule 18: A table becomes a comparison in three moves
First say what is compared and on which criteria. Then say the winner per criterion, one criterion per sentence. Then point to the guide for the full table. A table of up to 3 by 3 can be said in full this way; a bigger one is never read cell by cell.

#### Rule 19: A chart becomes four sentences
What the chart shows. The scale in one phrase ("de zero a cem por cento", "ao longo de oito anos"). The single pattern that matters ("a fatia quase triplicou"). The takeaway. Never read the data points one by one.

#### Rule 20: Risk in natural frequencies, with the denominator
Say a risk as "treze em cada cem", never as a relative risk alone ("o dobro", "quarenta por cento maior") and never as a bare percentage without its base. When the source gives a relative risk, convert it to the two absolute frequencies, or say that the base is unknown.

#### Rule 21: Honest limits, said out loud
For code, a procedure with more than 5 steps, a table bigger than 3 by 3, or a network with more than 6 nodes, the audio says three things: the conclusion, the main pattern, and what the listener is not getting here and where to find it ("o passo a passo completo está no guia escrito, na seção tal"). Never pretend the audio covered it.

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

Rules for intents:

1. **Intents never carry content.** If an intent is dropped by a medium that cannot do it, the listener must lose nothing but polish. So the words still say that a question is a question and that a key point is the key point.
2. **Do not invent intents.** If the script needs something outside the table, the need is usually a writing problem. Fix the sentence.
3. **Never open a part with a slow direction**, and never mark a whole part as slow. A slow uniform pace is the main risk for this listener. Slowness belongs to `[key]` only.
4. **Speaker roles are not intents.** A role is the label at the start of the line (`Guia:`). The medium maps each role to a voice.
5. **Performance is outside the method.** Whispering, shouting, singing, accents and sound effects are not part of an explanation. Use them only when the user explicitly asks to demonstrate what a voice engine can do. Then write them as `[perform: whispering]`, so the rendering step can find every one of them, and say in the producer note that the audio is a demonstration.
6. Older scripts use `[short pause]` and `[long pause]`. Read them as `[pause short]` and `[pause long]`.

## Phase 4: Render for the medium

Rendering turns the neutral script into what one medium needs. It changes marks, never words. Keep the neutral script, and write the rendered text to a second file, named after the medium (for example `guia-audio-script.md` and `guia-audio-render-eleven-v4.txt`).

### Step 1: Find out which medium, and get its profile

Never assume the medium, and never render from memory of how an engine used to work, because engines change between models and between months.

1. **Which medium?** Look, in this order: what the user said in this request, the project's instructions and saved preferences, and the voice tools this session really has. If two engines or two models are possible and nothing chooses between them, ask one question.
2. **Where is its profile?** An engine profile is a short document that the environment keeps: a project doc such as an audio playbook, a section of the project instructions, or a file next to the scripts. Read the profile of the exact model in use. A profile for "v4" does not describe "v3".
3. **No profile?** Build one before generating. Read the engine's own guide (a model-guide tool, the tool's schema, or the official documentation), fill in the contract below, and save it where the environment keeps profiles, so the next audio reuses it. Mark each line as stated by the documentation, or as a guess to test.
4. **Nothing to read at all?** Use the **plain** rendering below, and tell the user that the delivery intents were turned into punctuation only.

### Step 2: What an engine profile must answer

A profile is complete when it answers these questions for one engine and one model.

| Question | Why the rendering needs it |
|---|---|
| Which engine and model, and when was the profile last checked? | Behavior changes between models and over time |
| How is tone directed: inline marks, a separate instruction field, a setting, or not at all? | Decides where each tone intent goes |
| What happens to text in brackets or angle brackets that the engine does not know? | Some engines read it aloud. Then every unmapped mark must be removed |
| How is a pause made, and how long does each pause mark really last? | Maps the three pause intents. Measure it, because a mark named "long pause" can last about one second |
| How is one word stressed? | Maps `[stress]` and `[key]` |
| How is a pronunciation forced: phonetic alphabet, respelling, a dictionary, or nothing? | Maps `[say]` |
| Can speed be set? What rate was measured for each voice? | Planning length, and fixing "too fast" |
| One voice per call, or several voices in one call? | Decides how a dialogue is split |
| How are numbers, dates, symbols and links read? | Whether the script's words-only rule is enough |
| How many characters per call? What does a call cost? Is a retry charged? | Splitting, and telling the user the cost |
| What is unreliable or experimental? | What to check by ear, and what not to depend on |
| Which mark does each intent of this skill become? | The mapping table itself, one row per intent |

### Step 3: Map every intent, or degrade it

For each intent in the script, use the profile's mapping. When the medium cannot do an intent, go down this ladder and stop at the first step the medium supports. The last step works on every medium, because it is only text.

| Intent | First choice | Then | Last step, always possible |
|---|---|---|---|
| Tone | The engine's own tone direction | One instruction for the whole call, when the engine has an instruction field | Nothing. The wording already carries the attitude |
| Key point | The engine's direction for slower, weighted speech | A pause before the sentence | Start the sentence with the words that name it ("O ponto-chave é") |
| Stress | The engine's emphasis mark | A pause right before the word | Move the word to the end of the sentence, where speech stresses it by itself |
| Pause short | The engine's pause mark | An ellipsis | A paragraph break |
| Pause long | The engine's pause mark | Two paragraph breaks, or the end of a generation call | A spoken bridge ("Agora, a segunda parte.") |
| Pause recall | An engine pause that really lasts 4 to 6 seconds | Real silence added when the audio files are joined: end one call at the question, and start the next call at the answer | A spoken wait ("Pense um instante.") followed by a long pause |
| Pronunciation | The phonetic alphabet form, if the engine reads it | The respelling written in place of the word | The plain word, with the respelling kept in the producer note for a human check |
| Performance | The engine's mark, only in a requested demonstration | Drop it | Drop it |

Rules for rendering:

1. **Leave no neutral intent behind.** After rendering, search the rendered text for every intent of this skill (`[pause`, `[key]`, `[stress`, `[say`, `[perform`, and each tone word the profile maps to another mark). On an engine that reads unknown marks aloud, one forgotten `[pause short]` becomes spoken words.
2. **Change marks, never words.** The spoken words of the rendered text and of the neutral script are the same, except for a degradation from the ladder, which is listed in the report.
3. **One call starts from zero.** When the audio is generated in several calls, repeat the tone at the start of each call, because an engine does not remember the previous call.
4. **Respect the engine's own limits** from the profile: characters per call, concurrent calls, cost. Never retry a charged call by calling it again.
5. **Write a render report** of three short lists at the top of the rendered file, as producer notes: intents mapped, intents degraded (and to what), intents dropped. Tell the user anything degraded or dropped in one line.

### Two renderings that need no profile

- **Human reader.** Keep the neutral script as it is. The intents are stage notes, and a person reads them correctly. Add a first note that explains the marks in one line each.
- **Plain** (unknown engine, or an engine with no direction at all). Remove every mark. Turn `[pause short]` into an ellipsis, `[pause long]` into a blank line, `[pause recall]` into a spoken wait plus a blank line, `[key]` into the opening words "O ponto-chave é", and `[say]` into the respelling written in place of the word. Drop tone and stress.

### Example: one neutral passage, three media

Neutral script:

```
[pause short]
[curious] O que a instrução no-cache manda o navegador fazer?
[pause recall]
[key] Ela manda guardar a cópia e conferir a etiqueta antes de usar.
```

The same lines for an engine that takes inline marks in brackets, for an engine that takes SSML, and as plain text. The exact marks come from each engine's profile. These three only show the shape. In the first one, the recall pause is real silence added at the join of two calls, because that engine's pause mark is too short.

```
# call 1
[curious] O que a instrução no-cache manda o navegador fazer?
# join: 5 seconds of silence
# call 2
[slower, emphatic] Ela manda guardar a cópia e conferir a etiqueta antes de usar.
```

```
<break time="0.5s"/> O que a instrução no-cache manda o navegador fazer?
<break time="3s"/><break time="2s"/>
Ela manda guardar a cópia e conferir a etiqueta antes de usar.
```

```
... O que a instrução no-cache manda o navegador fazer?

Pense um instante.

O ponto-chave é este: ela manda guardar a cópia e conferir a etiqueta antes de usar.
```

### Step 4: Check what came out

After generating, measure the real rate (words divided by minutes), and compare the length with the plan. Measure the pauses too when you can (a silence detector on the audio file), because a pause that is shorter than planned takes away the listener's time to answer. If you cannot hear audio, say so, and ask the listener to judge the tone, the stress and each pronunciation. When the listener reports a problem, fix it at the right layer: a wrong idea or a lost listener is a script problem, and a wrong sound is a profile problem. Record a profile fix in the profile, so every later audio gets it.

## Example: the same content for the eye and for the ear

**For the eye (a clear-read guide):**

> `no-cache` significa "guarde, mas confira a etiqueta (ETag) antes de cada uso". Quem proíbe guardar é `no-store`.

**For the ear (clear-listen, the neutral script):**

```
[serious] Aqui existe um engano comum.
Muita gente acha que no-cache significa não guardar.
Isso não confere.
[stress: guardar]
No-cache significa guardar, mas conferir a etiqueta de versão antes de cada uso.
Quem proíbe guardar é outra instrução, chamada no-store.
[pause short]
[curious] O que a instrução no-cache manda o navegador fazer?
[pause recall]
[key] Ela manda guardar a cópia e conferir a etiqueta antes de usar.
```

What changed, and why: the parenthesis became its own sentence, because the ear cannot hear brackets. The code formatting became spoken names. The wrong belief is said out loud before the correction. The name "no-cache" is repeated where a reader would accept "ela". A question makes the listener retrieve the point. The intents say what the voice should do, and no line says how an engine does it.

## Example: a table and a chart, for the ear

**In the guide:** a table with four substances, a verdict per substance and a note from the sources; and a bar chart where the share of liver injuries caused by supplements goes from seven percent to about twenty percent in eight years.

**In the script (Rules 18 and 19):**

```
[serious] O guia compara quatro substâncias pelo risco de lesão no fígado.
Três delas têm risco documentado: a vitamina A em dose alta, o extrato de chá verde e a ashwagandha.
A quarta, a glutamina, fica fora dessa lista, porque as fontes a classificam como causa improvável.
A tabela completa, com as fontes, está no guia escrito.
[pause short]
O gráfico mostra a fatia das lesões no fígado que vem de suplementos.
Ele cobre cerca de oito anos.
[key] Nesse tempo, a fatia quase triplicou.
Ou seja, o problema cresce, e não é raro.
```

## Check before generating

Run `scripts/lint_audio_script.py <script.md>` on the **neutral script** and fix every failure. Do not lint the rendered text, because an engine's own marks are not part of the format. Then read the script aloud once, or at least read one part aloud. If you stumble, the listener will too.

Then check coverage (Rule 16): list the main ideas of the source and point to the sentence of the script that carries each one. When possible, give the script alone to a cold reader and ask the main questions; the reader should answer at least eight in ten.

Then check the rendering: every intent is mapped, degraded or dropped on purpose, no neutral intent is left in the rendered text, and the render report says what was degraded.

## Why these rules work

Read `references/research-basis.md` for the evidence, the trade-offs, and what is still unknown. Run the checks in `references/tests.md` after any change to this skill. The markup of a voice engine (its tags, its pause syntax, its pronunciation format) is not part of this skill. It lives in the engine profile that the environment supplies, one profile per engine and model.