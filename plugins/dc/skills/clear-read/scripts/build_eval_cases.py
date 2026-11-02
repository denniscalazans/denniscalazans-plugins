#!/usr/bin/env python3
"""build_eval_cases.py: turn tests/evals/evals.json into the case folders `claude plugin eval` reads.

Usage: python3 build_eval_cases.py <skill directory> [<skill directory> ...]

The source of truth is <skill>/tests/evals/evals.json, inside the skill. The eval CLI refuses an
eval dir inside the plugin's skills/ folder, so the runnable copies go to the plugin's own eval
dir: <plugin>/evals/<skill name>/<id>/prompt.md (the prompt, with run limits in front matter) and
<plugin>/evals/<skill name>/<id>/graders/criteria.md (one LLM grader for every expected behavior).
Edit the JSON, run this script, commit both. Exit code 1 when a case has no id, no prompt or no
expected_behavior.
"""
import json, os, sys

FRONT = "---\nmax_turns: 12\nallowed_tools: [Read, Glob, Grep, Skill]\n---\n\n"


def build(skill_dir):
    skill_dir = os.path.abspath(skill_dir)
    evals_dir = os.path.join(skill_dir, "tests", "evals")
    plugin_dir = os.path.dirname(os.path.dirname(skill_dir))
    out_dir = os.path.join(plugin_dir, "evals", os.path.basename(skill_dir))
    cases = json.load(open(os.path.join(evals_dir, "evals.json"), encoding="utf-8"))
    problems = []
    for c in cases:
        if not (c.get("id") and c.get("prompt") and c.get("expected_behavior")):
            problems.append(f"case without id, prompt or expected_behavior: {str(c)[:60]}")
            continue
        d = os.path.join(out_dir, c["id"]); os.makedirs(os.path.join(d, "graders"), exist_ok=True)
        with open(os.path.join(d, "prompt.md"), "w", encoding="utf-8") as f:
            f.write(FRONT + c["prompt"].rstrip() + "\n")
        checks = "\n".join(f"{n}. {b}" for n, b in enumerate(c["expected_behavior"], 1))
        with open(os.path.join(d, "graders", "criteria.md"), "w", encoding="utf-8") as f:
            f.write("---\ntype: llm\nweight: 1\n---\n\n"
                    f"Score the response against every item below. Each item is pass or fail; the score is the share of items that pass. Quote the sentence that decides each item.\n\n{checks}\n\n"
                    f"What the skill produced before this case existed, for context only, not a criterion: {c.get('failure_with_current_skill', '')}\n")
    print(f"{skill_dir}: {len(cases)} cases written to {out_dir}, {len(problems)} problems")
    return problems


if __name__ == "__main__":
    if not sys.argv[1:]:
        sys.exit(__doc__)
    bad = []
    for d in sys.argv[1:]:
        bad += build(d)
    for b in bad:
        print(b)
    sys.exit(1 if bad else 0)
