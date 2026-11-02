# Evals for clear-read

These cases run the skill against realistic prompts and grade the answer with a model. They are the test that a lint cannot run: did the text come out the way the rules say?

## What is here

- `evals.json`: the source of truth, one case per entry (id, prompt, expected behavior, what the skill did before the case existed).
- The runnable copies, built from the JSON, live in `plugins/dc/evals/clear-read/<id>/` (`prompt.md` and `graders/criteria.md`). They are outside this folder because `claude plugin eval` refuses an eval dir inside the plugin's `skills/` folder.


## How to run

From the repository root, with the plugin `dc` as the target (its eval dir is `plugins/dc/evals/`, the default):

```bash
claude plugin eval plugins/dc --runs 1 --no-publish --case "clear-read-*"
```

Each run is a full Claude session on your own credential, so start with `--runs 1` and one case (`--case "<id>"`). The default compares the answer with and without the skill (`--ablation with-without`). Results land in `plugins/dc/evals/results/`, which git ignores.

## How to add a case

1. Add the entry to `evals.json`: an id in kebab case, the prompt as a user would type it, and expected behaviors that a grader can check one by one.
2. Rebuild the runnable copies: `python3 plugins/dc/skills/clear-read/scripts/build_eval_cases.py plugins/dc/skills/clear-read`.
3. Commit the JSON and the folders together.

Added on 1 November 2026, by change 15 of the investigation (`plugins/dc/references/investigacao-2026-11/proposta.md`).
