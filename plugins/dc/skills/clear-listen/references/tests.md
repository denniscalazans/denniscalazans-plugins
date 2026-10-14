# Test plan for the clear-listen skill

Run these checks after any change to SKILL.md. Tests 1 to 3 are automatic or done by the model. Tests 4 to 10 need the real listener, because the only real test of an audio is what the listener keeps.

Last run: 8 October 2026. Tests 1 to 3 ran on three evals (narration, two hosts, one-minute recap), written by the same model that wrote the skill, so they are a sanity check and not an independent test. Result: 3 of 3 passed after one round of fixes to the skill and the lint. Tests 4 to 10 need the listener and have not run.

The evals are not in this repository, because it ignores `evals/` folders. They live in the docs of the project that uses the skill. `clear-listen-evals.json` holds the three cases, each with its prompt, its source guide and its expectations. `clear-listen-trigger-evals.json` holds requests that should and should not trigger the skill.

## Test 1: Lint

What it stresses: Rules 1, 2, 4, 6, 7.

How to run: `python scripts/lint_audio_script.py script.md`

Pass if it prints 0 problems. It checks sentence length, parentheses, digits and symbols, URLs, backward references, part markers, part length in words (at most 800, which is 5 minutes at 160 words per minute), a question near the end of each part, and the closing recall after `# closing` in a script with two or more parts.

The lint has its own unit tests. After any change to the lint, run `python3 scripts/test_lint_audio_script.py`. Every test must pass.

## Test 2: Text is not audio

What it stresses: the script is written for the ear, not converted.

How to run: take a clear-read guide and ask for its narration.

Pass if the script has no headings, tables, badges or links read aloud, if every definition is its own sentence, and if at least one dense section of the guide is replaced by a one-sentence pointer to the written text.

## Test 3: Fidelity

What it stresses: the script adds no fact and loses no main concept.

How to run: list the main concepts of the source and every factual claim in the script.

Pass if every main concept is in the script, and every claim in the script is in the source.

## Test 4: Listen once, then recall

What it stresses: the one goal.

How to run: the listener hears the audio once, in a normal situation (for example walking). Then he says the main ideas from memory.

Pass if he recalls all main concepts but at most one. Record which concept was lost, because the fix is in that part. For a stricter version, ask for the recall 24 hours later: 3 minutes to say the main points, scored against the list of 5 to 8 key ideas.

## Test 5: Re-entry

What it stresses: Rules 1 and 4.

How to run: start the audio at three random points.

Pass if, within about 20 seconds each time, the listener can say which part it is and what it is about.

## Test 6: Pace

What it stresses: Rule 9.

How to run: measure words per minute of a generated part (word count divided by audio minutes). Then ask the listener: too slow, right, or too fast.

Pass if he says "right", and if the measured rate is between 150 and 175 words per minute for Brazilian Portuguese. Record the measured rate in the project preferences and use it for length planning.

## Test 7: Second voice

What it stresses: Rule 13.

How to run: in a two-host script, delete every line of the second host.

Pass if the script now misses questions or misconceptions that matter. If nothing is missing, the second host was decoration, and the script fails.

## Tests 8 to 10: comparisons that settle open questions

The research cannot answer these for this listener, so he answers them himself. For each one: use topics of similar difficulty, pick the order at random, score free recall 24 hours later, and run at least 4 sessions per condition before deciding.

- **Test 8, rate:** the same kind of part at 150 and at 170 words per minute. Then the winner at normal speed against 1.3 times in the player.
- **Test 9, format:** narration against two hosts, with the same content. Also parts of 2 minutes against parts of 4 minutes.
- **Test 10, questions:** with and without the recall question at the end of each part. Also count how many times he caught his mind wandering.

Optional: silence against pink noise added by the listener at home, walking against sitting, and listening before reading against reading before listening.

Write each result into the project preferences, and change the default in SKILL.md when a result is clear.

## How to read a failure

- Test 1 fails: fix the named rule in the script.
- Test 2 fails: the script was converted, not rewritten. Redo Phase 2.
- Test 4 loses a concept: that part is too dense, too long, or has no recall question.
- Test 5 fails: part openings do not restate the context, or pronouns replaced names.
- Test 6 "too slow": remove slow delivery directions. "Too fast": add pauses between ideas before slowing the voice.
- Test 7 fails: rewrite the second host's lines as deep questions and misconceptions, or use one voice.
