# Delivery intents: the vocabulary and its six rules

This file belongs to clear-listen (`SKILL.md`, "Delivery intents"). The body keeps the table; the six rules moved here on 1 November 2026 to keep the body short.

## The vocabulary

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
