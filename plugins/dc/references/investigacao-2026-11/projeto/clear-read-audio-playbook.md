# Clear Read the Web: Audio Playbook (engine profiles)

CHECKED: 2026-10-08 · v4-docs-dissected-and-quality-standard
SET_VERSION: 2026-10-14-r1

This file is the **environment's side** of the audio method.
The `clear-listen` skill decides WHAT the voice should do, and writes it as neutral delivery intents (`[curious]`, `[pause short]`, `[key]`, `[stress: palavra]`, `[say: termo = respelling]`).
This file decides HOW each voice engine does it. It holds one **engine profile** per engine and model.

So the work has two steps:
1. Write the neutral script with the skill. It contains no ElevenLabs syntax.
2. Render it for the model in use, with the profile of that exact model (section 11). Save the rendered text to a second file, `{slug}-audio-render-{model}.txt`.

Changing the model means rendering again. It never means rewriting the script.

Sections 1 to 9 are the detail of the Eleven v4 profile, which is the default.
Section 10 is what this Project adds to the skill.
Section 11 is the profiles: the mapping tables for v4, v3 and the older models, and the template for a new engine.

Section 12 is the quality standard that every audio of this Project must meet.

Sources, all read on 8 de outubro de 2026:
- ElevenLabs docs, "Eleven v4": https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4
- ElevenLabs docs, "Best practices" (sections "Prompting Eleven v4", "Controls", "Pronunciation", "Emotion", "Pace", "Text normalization"): https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- ElevenLabs blog, "Audio Tags list for Eleven v4": https://elevenlabs.io/blog/elevenlabs-audio-tags-list
- The connector's model schema for `eleven_v4` (`creative_get_model_schema`).
- The connector's own model guide (`creative_get_model_guide`, read on 8 de outubro de 2026). It covers v4, v3, Multilingual v2, Flash v2.5 and Turbo v2.5.
- Measurements on the demo audio of 8 de outubro de 2026 (10 generations on `eleven_v4`, Rafael and Marilita).

Each rule is marked **[docs]** when ElevenLabs states it, **[guide]** when the connector's model guide states it, **[measured]** when it was measured on our audio, and **[to test]** when it is Claude's inference and still needs Dennis's ear.

## 1. Which medium, and which model

How Claude finds the medium for an audio, in this order:
1. What Dennis said in the request ("usa o v3", "faz com outra ferramenta").
2. `preferences/main` in the Biblioteca (`audio_model`, `audio_model_fallback`, `voices`).
3. The voice tools this session really has, and the `model_id` values the speech tool offers.

Today the answer is `eleven_v4`, through the ElevenLabs connector.

- **[docs]** ElevenLabs calls Eleven v4 a net upgrade over Eleven v3 in almost every case, and recommends switching.
- **[docs]** A voice can sound clearly different on v4 than on v3, because v4 copies the source voice more closely. ElevenLabs recommends comparing both with your own content.
- **[docs]** v4 is still changing after launch, so its behavior can shift over time. Re-check the profile when an audio starts to sound different.
- The connector's speech tool offers `eleven_v4`, `eleven_v3`, `eleven_multilingual_v2`, `eleven_flash_v2_5` and `eleven_turbo_v2_5`. It does not offer `eleven_v4_turbo`, which is the low-latency variant for live agents and is not needed here.

Decision rule:
1. `eleven_v4` is the default for all three modes. Dennis chose it on 8 de outubro de 2026, after listening to the narrator on both models and to a two-host conversation on both. He found v4 more natural and better at following tags, and the v3 conversation "mais tensa, mais séria".
2. `eleven_v3` is the fallback when v4 is not offered. Render with the v3 profile (section 11.2), not with the v4 one.
3. When Dennis asks for another model or another tool, use its profile in section 11. If it has none, build one from the template in section 11.5 before generating.
4. When Dennis says an audio "sounds different" or worse, run the one-sentence comparison again before changing the script rules.

## 2. What v4 cannot do, and what to do instead

| Not available on v4 | Source | What to do instead |
|---|---|---|
| SSML, including `<break>` pause tags | [docs] | Ellipses, a pause tag, and short paragraphs (section 4) |
| A Speed slider and a Style slider | [docs] | Control pace with a delivery tag and with sentence length (section 3) |
| Voice settings in this connector's speech tool | Tool schema | The same: tags and text structure are the only controls |
| A silence of a chosen length | [measured] | Silence added with `ffmpeg` when the parts are joined (section 4.1) |

Consequence for feedback: when Dennis says "voz muito rápida", the fix is in the script.
Use shorter sentences, more pause intents, and more ellipses in the rendering.
There is no speed number to lower.

## 3. Audio tags: how v4 and v3 take direction

An audio tag is a short instruction in square brackets, placed right before the text it affects.
It is the ElevenLabs form of a clear-listen delivery intent.
The neutral script never contains these tags. The rendering step writes them, with the mapping table in section 11.

- **[docs]** v4 follows tags more reliably than earlier models.
- **[docs]** A tag works best when the voice already has that delivery in its training audio. Match the tag to the voice's character.
- **[docs]** v4 also generates sound effects. So a vague tag can come out as a noise instead of a way of speaking. A tag that clearly describes the voice avoids this.
- **[docs]** Tags can be combined, and can be free descriptions such as "low, steady voice".
- **[docs]** A tag holds until the next one. Put a new tag where the delivery should change. Two contrasting tags on the same words blur the performance.
- **[docs]** Several qualities go in one bracket, separated by commas: `[tense, cautious]`.
- **[docs]** A tag can describe the manner, the situation, the character or a shift, in free words: `[hushed and reverent, like a nature documentary narrator]`, `[starting calm, then losing patience]`. This is the strongest tool for a narrator, because it gives the voice a role and not only a mood (section 12.2).
- **[docs]** v4 performs better when it gets a full scene. So a longer call with context is directed better than a call with one sentence.
- **[docs]** When a delivery misses, swap in a neighboring word and generate again, or add detail to the tag (`[nervous]` becomes `[nervous, trying to sound confident]`).
- **[docs]** Pacing tags exist: `[slowly]`, `[rushed]`, `[drawn out]`. Pause tags are `[pause]`, `[short pause]` and `[long pause]`.
- **[docs]** Do not direct emotion with narrative text ("ele disse, triste"). The model speaks those words.
- **[guide]** Stage directions such as `[grinning]` or `[music]` are not performed. Use plain words with no hyphens: `[high voice]`, not `[high-pitched]`.

Rules for this Project:
1. **Write tags in English.** Every documented tag is in English. PT-BR tags such as `[pausa]` are untested. **[to test]**
2. **Describe the voice, never a scene.** Right: `[warm, natural narration]`. Wrong: `[library]`, `[night]`, `[music]`.
3. **Stay inside a narrator's range.** The narrator is a professional narration voice. Use calm, warm, curious, thoughtful, serious, emphatic. Do not use giggling, shouting, whispering or crying. The only exception is a demonstration that Dennis asks for, written with the skill's `[perform: ...]` intent.
4. **One delivery tag at the start of each segment**, and a new one only when the tone really changes. At most about one tag per 3 or 4 sentences.
5. **Never put script words inside brackets.** The model does not speak bracketed text.
6. **No sound-effect tags** (applause, door, rain). The guide is an explanation, and effects distract.
7. **Leave no neutral intent in the text sent to the engine.** A bracket that v4 does not understand as a voice direction can come out as a sound, or be skipped. After rendering, search the text for `[pause`, `[key]`, `[stress`, `[say` and `[perform`.

## 4. Punctuation and layout are part of the direction

- **[docs]** Ellipses add a pause and weight.
- **[docs]** A word in CAPITALS gets more emphasis.
- **[docs]** Normal punctuation gives the natural rhythm, and the structure of the text strongly changes the result.

Rules for rendering on v4 and v3:
1. One sentence per line, and a blank line between ideas. The blank line reads as a breath.
2. An ellipsis after each spoken prequestion, and before each key point.
3. CAPITALS on at most one word per segment: the word of the `[stress: ...]` intent. More than that sounds like shouting.
4. No em dashes and no travessões (already a Project rule). Use a period or an ellipsis.
5. A question mark only on a real question, because it changes the melody of the sentence.

### 4.1 Pauses: what was measured

Measured on 8 de outubro de 2026, on the closing block of the demo (`eleven_v4`, Rafael), with `ffmpeg silencedetect`:

| What the text had | Silence that came out |
|---|---|
| A normal sentence end | 0.36 to 0.54 seconds |
| `[short pause]` at the start of a line | 0.4 to 0.5 seconds, the same as a normal sentence end |
| `[long pause]` alone on a line, after a question | about 1.3 seconds |

So on v4:
- `[pause short]` needs no tag. A sentence end, or an ellipsis, already gives it.
- `[pause long]` gets about 1.3 seconds from `[long pause]`. For a part boundary of 2 seconds, end the generation call there and add the silence when joining.
- **`[pause recall]` cannot be made with a tag.** The skill asks for 4 to 6 seconds, and the tag gave 1.3. Make it with real silence: end the call at the recall question, start the next call at the answer, and join with 5 seconds of silence.

How to add the silence when joining parts:
`ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 5 -q:a 9 silence-5s.mp3`, then put `silence-5s.mp3` between the two parts in the concat list.

This is one measurement, on one voice. Measure again when the model or the voice changes.

### 4.2 Keep the scene, and stretch the pause afterwards

Ending a call at every recall question makes many short calls, and v4 directs a short call worse than a full scene (section 3).
So the preferred method for a narration is:
1. Generate one whole part in one call (3 to 4 minutes, far under the 10,000 characters that v4 accepts).
2. In the rendered text, put `[long pause]` alone on a line where the neutral script has `[pause recall]` or `[pause long]`.
3. After downloading, find those silences with `ffmpeg -af silencedetect=noise=-35dB:d=1.0`. In the measurement of section 4.1, the `[long pause]` was the only silence longer than 1 second.
4. Cut the file in the middle of each such silence, and join the pieces with extra silence: 4 seconds more for a recall pause, 1 second more for a part boundary.

**[to test]** This was designed from one measurement and has not produced a full audio yet. On the first audio, check that the number of long silences found equals the number of `[long pause]` tags. If it does not, fall back to ending the call at the question.

## 5. Make every token speakable

- **[docs]** Text normalization is on by default, but numbers, dates, currencies, units, URLs and abbreviations can still be read wrongly. ElevenLabs recommends writing them out in the script.

The skill already writes numbers, dates, units and symbols as words, and never reads a link.
Rules this Project adds:
1. Acronyms: decide per acronym whether it is spelled or read as a word, and write it that way. "API" stays. "LLM" may need "éle-éle-ême". **[to test]**
2. A model name with a letter and a number is written the way it is said: "Eleven vê quatro".

## 6. Hard names and English terms: pronunciation

The skill marks a hard name with `[say: termo = respelling]`, and adds the IPA form when it is known.
This section says how v4 and v3 render it.

- **[docs]** v4 reads a pronunciation written in the International Phonetic Alphabet (IPA) when it sits between forward slashes, inside double quotes, for example `"/ˈkæʃ/"`.
- **[docs]** Include the stress marks, use it only on the words that need it, and test with the chosen voice, because results vary by voice and phrase.
- **[guide]** The connector's guide says the same form works on v3. One research source says it is v4 only. So on v3, test it first. **[to test]**

Rules for this Project:
1. First try the plain word. Most English tech terms that Dennis uses at work need nothing.
2. If a name comes out wrong in a test, use the respelling in Portuguese letters, written in place of the word. It is easier to maintain.
3. Use IPA only for a name that matters to the guide and still fails. Save the working form in the term's `glossary` entry (field "how to say it out loud"), so the next audio reuses it.
4. Never test a pronunciation inside a long paid generation. Test it in one short sentence.

## 7. The podcast (mode B)

- **[docs]** v4 handles several voices in one script when each speaker has its own voice.
- In this connector, the speech tool takes one `voice_id` per call. So the Project keeps its method: one flow, and each host's block generated with that host's voice.

Rules for this Project:
1. The neutral script labels each line with its role (`Guia:`, `Curioso:`). The rendering maps `Guia` to the narrator voice and `Curioso` to the second-host voice, from `preferences`.
2. Group consecutive lines of the same host into one block, so there are fewer calls.
3. Start each block with a delivery tag, because each call starts with no memory of the previous block's tone.
4. Keep the Curioso's reactions short and written as words plus one tag ("[surprised] Sério?"). Do not write laughter as "ha ha".
5. Join the parts with `ffmpeg` (section 6.4 of the instructions). Generate at most 4 calls at a time, because more than 5 at once fails.

## 8. Generation checklist

1. The neutral script passes the clear-listen lint and the audio checklist in section 12 of the instructions.
2. The medium and the model are named, and the rendering used the profile of that model (section 11).
3. The rendered text has no neutral intent left, and its tags are in English, describe the voice, and stay inside the narrator's range.
4. No SSML on v4 or v3. No bracket tags on the v2-family models. No digits, symbols, URLs or em dashes left.
5. Every `[pause recall]` became real silence at a part join (section 4.1).
6. Any new hard name was tested in one short sentence first.
7. `estimate_only: true` first when the script is longer than about 5 minutes.
8. `generations_count: 1`. The tool's default is 4.
9. Poll the status. Never call the generation again to retry.
10. The render report (mapped, degraded, dropped) is at the top of the rendered file, and Dennis was told what was degraded or dropped.

## 9. Open points

| Point | Status |
|---|---|
| Does v4 sound better than v3 with the narrator voice in PT-BR? | Settled on 8 de outubro de 2026: Dennis chose v4 |
| Credit cost of v4 per character | About 1 credit per character, the same as v3. Launch promotion until 12 de outubro de 2026: on Creator plans and above, v4 does not use credits, up to 2 times the monthly allowance (one place on the pricing page says 3 times). From 13 de outubro de 2026, budget 1 per character and report the real `price.credits` of the first generation |
| Speech rate on v4 | Measured: Rafael about 180 words per minute (171 to 190), Marilita about 170. The demo with both voices and effects: 166. Faster than the 160 used for planning, and there is no speed setting |
| Maximum characters per generation on v4 | 10,000 in the app, stated on the ElevenLabs tags page. Not tested through the connector. Keep one generation per part (3 to 4 minutes) |
| How long is a pause tag on v4? | Measured once (section 4.1): `[long pause]` about 1.3 seconds, `[short pause]` no longer than a sentence end |
| Do PT-BR tags work as well as English tags? | To test. Until then, English only |
| Does IPA between slashes work on v3? | Sources disagree. Test in one sentence before the first v3 audio that needs it |
| Do Rafael and Marilita sound different enough together? | To check in the first real podcast |
| Did the demo's whisper, shout, song, accent and effects come out well? | Waiting for Dennis's ear. The volume measurement only shows the whisper about 10 dB below the shout |

## 10. What this Project adds to the clear-listen skill

The writing method for audio lives in the `clear-listen` skill, the sibling of `clear-read`.
Read its `SKILL.md` before writing any audio script, and its `references/research-basis.md` when a rule needs a reason.
The skill writes the neutral script. This playbook renders it.

### 10.1 What the deep research changed in this Project's audio rules

| Topic | Before | Now | Why |
|---|---|---|---|
| Speech rate | "about 150 words per minute" in section 6.2 of the instructions | Plan with **160 words per minute**, range 150 to 175 | Recall is best at a moderate rate. Portuguese words are longer than English words, so English targets do not transfer. Brazilian radio news reading was measured at 164 |
| Part length | 2 to 3 minutes | **3 to 4 minutes**, never over 5 | Segmenting has strong support, but no study gives an optimum for audio. This is a default to test |
| Core idea | Anywhere in the opening | **In the first 30 seconds**, and again at the start of each part | Mind wandering near the start does the most damage |
| Recall question | Only at the end of the audio | **One at the end of each part**, answerable in the head, with a pause of 4 to 6 seconds | Built-in questions improve learning, also for students with ADHD |
| Narrator | "One narrator per audio" | **One constant voice per role** | A change of voice pulls attention back, so two roles with two voices are an advantage |
| Expression | Calm | **Moderate and varied**: calm, but not flat and not acted | Moderate intonation gave the best attention and credibility |
| Speed | Not mentioned | Generate at normal speed. Tell Dennis the player's speed control is fine, up to about 1.5 times | Small cost up to 1.5 times in video studies. Audio alone is untested |
| Measured rate | Not measured | After each generation, compute words divided by minutes, and save it in `preferences` | The engine's delivery is not a words-per-minute setting |

### 10.2 Consequences for the three modes

- **Mode A, narração:** 10 to 20 minutes, 3 to 5 parts. Budget: about 160 words per minute, so 1,600 to 3,200 words.
- **Mode B, podcast:** the Curioso must have a voice with clearly different pitch from the narrator, and speak within the first 20 seconds. The important sentence of each exchange comes right after a voice change. Claude writes every line. No banter.
- **Mode C, resumo:** 2 to 4 minutes, one part, about 320 to 640 words. Its best use is a review close to when Dennis needs the knowledge, more than a first listen.

### 10.3 Delivery tags, revised

The key point of a part is the skill's `[key]` intent. On v4 and v3 it becomes `[slower, emphatic]`, on that one sentence only.
Do not open a part with a "slow" or "measured" direction, because a slow uniform pace is the main risk for this listener.
Rotate the tone between parts (warm, curious, serious, thoughtful), because the same device repeated stops catching attention.

### 10.4 Never in the audio

Music, ambience, sound effects, white or pink noise, jokes between hosts, and side facts that serve no main concept.
v4 can generate effects, singing and accents. That is not a reason to use them in a guide.
If Dennis wants to try pink noise, he adds it himself, and the result goes into `preferences`.

### 10.5 Open tests with Dennis

The research cannot settle these for one person, so `clear-listen/references/tests.md` has the procedures:
rate (150 against 170), narration against two hosts, part length (2 against 4 minutes), with and without the recall question.
Run one test at a time, and record each result in `preferences`.

## 11. Engine profiles

One profile per engine and model.
Each profile answers the questions of the skill's profile contract, and ends with the mapping table: one row per delivery intent.
When a medium cannot do an intent, the rendering goes down the skill's ladder (engine mark, then punctuation, then wording) and the render report says so.

### 11.1 Profile: ElevenLabs `eleven_v4` (default)

Last checked: 8 de outubro de 2026.

| Question | Answer |
|---|---|
| How is tone directed? | Inline tags in square brackets, in English, right before the text. A tag holds until the next one [guide] |
| Unknown bracket text | Not spoken. It can be performed as a sound, or skipped. So remove every neutral intent [docs] |
| Pauses | Sentence ends and ellipses. `[long pause]` gives about 1.3 seconds [measured]. No SSML [docs]. A silence of a chosen length comes from `ffmpeg` at a join (section 4.1) |
| Stress on one word | The word in CAPITALS [docs] |
| Pronunciation | IPA between slashes inside double quotes, or a respelling in the text (section 6) |
| Speed | No setting on v4 [docs]. Measured rate: Rafael about 180 words per minute, Marilita about 170 |
| Voice settings | Stability and Similarity exist on v4 [docs]. Lower Stability is more expressive and more varied. The connector does not expose them: its v4 node accepts only `language_code` [schema]. They can be changed only in the ElevenLabs app |
| Language | The v4 node accepts `language_code` (BCP-47, for example `pt-BR`) through `creative_update_node` [schema]. The speech tool does not set it. **[to test]** whether setting it improves PT-BR reading of English tech terms |
| Voices per call | One `voice_id` per call in this connector. A dialogue is one call per block of one host |
| Numbers, dates, symbols | Normalized by default, but can be misread. The skill's words-only rule is enough [docs] |
| Limits and cost | 10,000 characters per generation in the app [docs, blog]. Not tested through the connector. About 1 credit per character. At most 4 calls at a time. A retry is charged |
| Unreliable | Tags are not deterministic. Accents and singing are experimental. A vague tag can become a sound effect |

Mapping table for `eleven_v4`:

| Intent in the neutral script | Rendered as |
|---|---|
| `[warm]` | `[warm, natural narration]`. At the start of each call, the narrator's scene direction of section 12.2 comes first |
| `[curious]` | `[curious]` |
| `[serious]` | `[serious]` |
| `[thoughtful]` | `[thoughtful]` |
| `[inviting]` | `[warm, inviting]` |
| `[surprised]` (dialogue) | `[surprised]` |
| `[amused]` (dialogue) | `[soft chuckle]` |
| `[key]` | An ellipsis at the end of the sentence before, then `[slower, emphatic]` on the key sentence, then the tone tag again on the next sentence |
| `[stress: palavra]` | That word in CAPITALS in the next sentence. The line with the intent is removed |
| `[pause short]` | Removed. The sentence end already gives it. Use an ellipsis when the pause must be felt |
| `[pause long]` | `[long pause]` alone on a line, stretched by 1 second in post-production (section 4.2). At the end of a call: 2 seconds of silence at the join |
| `[pause recall]` | `[long pause]` alone on a line, stretched to 5 seconds in post-production (section 4.2). Fallback: end the call at the question, and join with 5 seconds of silence |
| `[say: termo = respelling = /ipa/]` | First the plain word. If a test fails: the respelling in place of the word. If that fails: `"/ipa/"` in place of the word |
| `[perform: ...]` (demonstration only) | The matching v4 tag: `[whispers]`, `[shouting]`, `[laughs]`, `[sighs]`, `[singing]`, `[strong X accent]`, `[applause]` |
| Role label `Guia:` | Narrator voice from `preferences`. The label is removed |
| Role label `Curioso:` | Second-host voice from `preferences`. The label is removed |

### 11.2 Profile: ElevenLabs `eleven_v3` (fallback)

Last checked: 8 de outubro de 2026. Source: the connector's model guide, which gives one set of rules for v4 and v3, plus Dennis's listening test.

What is the same as v4: inline tags in English, capitals for stress, ellipses for pauses, no SSML, one voice per call, about 1 credit per character.
So the mapping table of section 11.1 is the starting point for v3.

What differs, and what to do:

| Point | On v3 | What to do |
|---|---|---|
| Tag following | Less reliable than v4 [docs] | Use fewer tags: the tone tag at the start of each call, and `[slower, emphatic]` for `[key]`. Degrade `[surprised]` and `[amused]` to wording when a test shows they fail |
| Tone of a dialogue | Dennis found the v3 conversation "mais tensa, mais séria" | Render `[warm]` on every block of the Curioso too, and avoid `[serious]` in a dialogue unless the content needs it |
| Characters per call | 5,000, half of v4 (research of 8 de outubro de 2026) | Split parts so each call stays under about 4,500 characters |
| Pronunciation in IPA | Sources disagree (section 6) | Render `[say]` as the respelling first. Test IPA in one sentence before using it |
| Pause lengths | Not measured on v3 | Use the v4 method (real silence at joins) and measure on the first v3 audio |
| Measured rate | Rafael 163 to 173 words per minute | Plan at 165 for v3, against 180 for v4 |
| Effects, singing, accents | Not part of this profile | Drop `[perform: ...]` on v3 unless a test shows the tag works |

### 11.3 Profile: ElevenLabs `eleven_multilingual_v2`, `eleven_flash_v2_5`, `eleven_turbo_v2_5`

Last checked: 8 de outubro de 2026. Source: the connector's model guide. Dennis has not listened to this method on these models, so every line is **[to test]** for PT-BR.

These models have no audio tags. **They read bracket text aloud as words** [guide].
So the rendering must remove every bracket, and carry the delivery with punctuation and with a pause tag in SSML.

| Intent in the neutral script | Rendered as |
|---|---|
| Any tone intent | Removed. The wording carries the attitude |
| `[key]` | `<break time="0.7s" />` before the sentence. The sentence starts with "O ponto-chave é" |
| `[stress: palavra]` | That word in CAPITALS, at most one per part [guide] |
| `[pause short]` | A sentence end or an ellipsis |
| `[pause long]` | `<break time="2.0s" />`. The guide allows up to 3 seconds, and only a few per script |
| `[pause recall]` | Real silence at a join, as on v4 (section 4.1), because one break tag is at most 3 seconds |
| `[say: termo = respelling]` | The respelling in place of the word. No IPA on these models [guide] |
| `[perform: ...]` | Dropped. Tell Dennis the demonstration needs v3 or v4 |
| Role labels | One voice per call, the same as v4 |

Also on these models: Flash reads numbers worse than the larger models, so the words-only rule matters more. Multilingual v2 is the steadiest on long text.

### 11.4 Profile: a human reader

When Dennis or another person will read the script aloud, the neutral script is the final text.
Add one note at the top that explains each intent in one line.
Nothing is rendered, and nothing is dropped.

### 11.5 Template: a profile for a new engine

Before the first audio on an engine that has no profile here, fill this in and add it as section 11.x.
Read the engine's own guide first (a model-guide tool, the tool's schema, the official docs). Mark each line [docs], [guide], [measured] or [to test].

```
### Profile: <engine> <model>
Last checked: <date>. Sources: <links or tool names>.

How is tone directed (inline marks, an instruction field, a setting, nothing)?
What happens to bracket or angle-bracket text the engine does not know (spoken, skipped, performed)?
How is a pause made, and how long can it be? Measured length of each pause mark:
How is one word stressed?
How is a pronunciation forced (IPA, respelling, a dictionary)?
Can speed be set? Measured words per minute, per voice:
One voice per call, or several?
How are numbers, dates, symbols and links read?
Characters per call, cost per call, concurrent calls, is a retry charged?
What is unreliable or experimental?

Mapping table: one row for each of
[warm] [curious] [serious] [thoughtful] [inviting] [surprised] [amused]
[key] [stress: ...] [pause short] [pause long] [pause recall] [say: ...] [perform: ...]
and for the role labels.
```

Then test one short sentence per mapped intent, with `generations_count: 1`, and let Dennis's ear confirm before a long audio.
Record what he says in the profile.

## 12. The quality standard: cinematic production, in the service of memory

Dennis asked on 8 de outubro de 2026 for every audio to have cinematic quality, while keeping the purpose: the content must end up in his head.

These two goals agree on the voice and on the production, and they disagree on one point.
The research behind `clear-listen` shows that music, ambience and effects under the voice make speech harder to follow, and more so for a listener with ADHD.
So in this Project "cinematic" means **the craft of a film's narration and sound mix, applied to a voice alone**. It never means a soundtrack under the explanation.

### 12.1 What cinematic means here, and what it does not

| Cinematic, and it helps memory | Cinematic, but it hurts memory. Not used |
|---|---|
| A narrator with a role and a point of view, not a neutral reader | Music or ambience under the voice |
| Contrast between parts: each part has its own tone | Sound effects inside an explanation |
| Real silence after a question, long enough to answer | Acted emotion: whisper, shout, laughter, accents |
| Weight on the one sentence that matters in each part | The same dramatic tone on every sentence |
| One constant level across voices and parts | Level jumps between hosts |
| Clean starts and ends, no clicks, no cut breaths | Loudness pushed until the voice distorts |

One allowed option, only if Dennis asks for it: a short sound signature that plays alone, before the first word and between parts. This connector can generate a sound effect (section 12.6). It cannot generate music.

### 12.2 Performance: direct the narrator like a film narrator

1. **Give the voice a role at the start of every call**, with a write-your-own tag from the docs. For the narrator: `[warm, intimate documentary narrator, speaking to one person, unhurried but alive]`. For the Curioso: `[curious, quick, genuinely wants to understand]`. **[to test]** with Dennis's ear, on one paragraph, against the plain `[warm, natural narration]`.
2. **One scene per call.** Generate a whole part in one call, so the model has context (section 4.2).
3. **Contrast between parts.** The tone intent of each part is different from the one before. The skill plans this in its design phase.
4. **Weight on the key point**, and nowhere else: an ellipsis before it, then `[slower, emphatic]`.
5. **Silence is part of the performance.** The recall pause is 4 to 6 real seconds (section 4.2).
6. **Stay inside the voice's range.** A professional narration voice does calm, warm, curious, thoughtful, serious and emphatic well. A tag far from its recordings is followed badly [docs].
7. **A take that misses is fixed by a better tag**, not by the same call again. Swap in a neighboring word or add detail [docs]. Regenerating one part is a new charged call, so Dennis decides it.

### 12.3 Production: master every audio before it is published

Measured on the demo of 8 de outubro de 2026: the blocks came out between -23.1 and -17.8 LUFS. One line of Marilita was about 5 LU louder than Rafael's narration. That is a level jump the listener hears.

Every audio goes through these steps, with `ffmpeg`, after downloading and before publishing:

1. **Measure each generated file**: `ffmpeg -i part.mp3 -af loudnorm=print_format=summary -f null -`. Read "Input Integrated".
2. **Bring every file to the same level: -19 LUFS**, the usual target for mono speech. Use a fixed gain, so the dynamics inside the file stay as performed: `volume=<-19 minus the measured value>dB`.
3. **Protect the peaks** with a limiter after the gain: `alimiter=limit=0.89` (about -1 dB).
4. **Stretch the pauses** to their planned length (section 4.2).
5. **Join** with a fixed gap between calls: 0.4 seconds between turns of a dialogue, 2 seconds between parts.
6. **Export** mono, 44.1 kHz, 128 kbps MP3 or better. The connector delivers 128 kbps.
7. **Measure the result**: integrated loudness within 1 LU of -19, true peak under -1 dB, total length, words per minute, and the length of each recall pause.
8. **Report the numbers** to Dennis in one line, and record them in the article's `audio` entry.

What `ffmpeg` cannot fix: a wrong tone, a mispronounced name, a flat reading. Those are judged by Dennis's ear, because Claude cannot hear audio.

### 12.4 What is not available through this connector

- **Stability and Similarity** (section 11.1). The more expressive setting can only be chosen in the ElevenLabs app.
- **Several takes to choose from.** The tool can make up to 4, and Dennis decided on 1 per call. ElevenLabs itself advises more than one take for important lines. Until 12 de outubro de 2026 a second take on v4 costs no credits, so this is the cheapest moment to compare takes.
- **Music.** Only in the full connector. Sound effects are available here (section 12.6).

### 12.5 Quality checklist, before publishing an audio

1. The neutral script passed the lint, and the rendering used the profile of the model in use.
2. Every call starts with the role direction of section 12.2 and a tone tag.
3. Each part has a tone different from the part before.
4. Exactly one key-point direction per part.
5. Every recall pause measures 4 to 6 seconds in the final file.
6. Every file was brought to -19 LUFS, and the final file is within 1 LU of it.
7. True peak under -1 dB.
8. No music, ambience or effect under the voice.
9. The measured numbers were reported, and Dennis was asked to judge tone, stress and names.

### 12.6 Sounds and voice effects: what v4 does alone, and what needs layers

Tested on 8 de outubro de 2026, at Dennis's request, with two short stories. This is for demonstrations and stories. It is not for the guides (section 12.1).

The set of sounds is open. A tag is free text that the model interprets, and the official lists are examples, not a closed list [docs]. So any sound can be asked for, and none is guaranteed.

| What was asked | What `eleven_v4` did with a tag alone | What works |
|---|---|---|
| A phrase spoken as if underwater: `[speaking underwater, muffled, gurgling voice, bubbles]` | The high frequencies of the phrase were not reduced [measured]. The voice stayed a normal voice | Generate the phrase normally, then filter that phrase with `ffmpeg`: `lowpass=f=520,lowpass=f=520,vibrato=f=6.5:d=0.45,aecho=0.8:0.6:35:0.35`. Measured: 23 dB less energy above 3 kHz |
| Singing while it rains: `[light rain falling outside]` and `[singing cheerfully, rain continues in the background]` | No rain under the voice. The gaps between phrases were silent, and Dennis confirmed by ear | Two layers. Generate the voice alone. Generate the rain with the sound-effect node (`creative_generate_in_flow`, `node_type: "sfx"`, model `eleven_text_to_sound_v2`). Mix with `ffmpeg amix` |

What this shows:
1. **A tag gives an event, not a bed.** v4 can place a sound at one moment (`[applause]`). It did not keep a sound running under the speech.
2. **A tag changes how the voice performs, not the acoustics around it.** Whisper and shout worked. "Underwater" did not.
3. **A continuous sound, or an acoustic effect on the voice, is post-production**: a second layer, or a filter.

About the sound-effect node, measured once: a prompt that asked for 10 seconds returned 2 seconds, and cost about 17 credits (the estimate said 55). The speech tool cannot set the duration. So loop the clip with `ffmpeg -stream_loop`, or ask for the duration in the ElevenLabs app. The effect came out very quiet (about -41 LUFS), so it needed about 20 dB of gain to be heard under a voice at -19.
