# Rendering: Phase 4 of clear-listen (the four steps, the engine profile contract, the degradation ladder, the render rules and one passage for three media). Read it before generating audio; the SKILL.md body only points here.

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

### Check the rendered text, before generating

Then check the rendering: every intent is mapped, degraded or dropped on purpose, no neutral intent is left in the rendered text, and the render report says what was degraded. Run `scripts/check_render.py <rendered.txt>` on the rendered text, because it fails on every neutral intent that is still there.

### Step 4: Check what came out

After generating, measure the real rate (words divided by minutes), and compare the length with the plan. Measure the pauses too when you can (a silence detector on the audio file), because a pause that is shorter than planned takes away the listener's time to answer. If you cannot hear audio, say so, and ask the listener to judge the tone, the stress and each pronunciation. When the listener reports a problem, fix it at the right layer: a wrong idea or a lost listener is a script problem, and a wrong sound is a profile problem. Record a profile fix in the profile, so every later audio gets it.
