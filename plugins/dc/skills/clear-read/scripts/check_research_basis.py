#!/usr/bin/env python3
"""check_research_basis.py: the evidence map of a skill covers every rule and is well formed.

Usage: python3 check_research_basis.py <skill directory> [<skill directory> ...]
Exit code 1 when any problem is found. Works for clear-read and clear-listen, and for any
skill whose SKILL.md numbers its rules as "Rule N" headings and whose
references/research-basis.md has the table "## Evidence map, checked at the source".

Checks:
  rule-without-row     a "Rule N" heading in SKILL.md (or in references/*.md for rules that
                       moved out of the body) has no row whose first cell names it
  bad-doi              a cell says "doi:" and what follows is not of the form 10.NNNN/...
  row-without-date     the Checked cell is neither a date (YYYY-MM-DD) nor the word "carried"
  empty-cell           a row has an empty cell
  bad-verdict          the Verdict cell does not start with one of the five verdicts
"""
import os, re, sys

VERDICTS = ("holds", "holds with a limit", "contradicted", "practice", "untested")
DOI = re.compile(r"doi:\s*(\S+)")
DOI_OK = re.compile(r"^10\.\d{4,9}/\S+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def rules_in(text):
    found = set()
    for m in re.finditer(r"^#{3,4} Rule (\d+)\b", text, flags=re.M):
        found.add(int(m.group(1)))
    for m in re.finditer(r"^#{3,4} Rules (\d+) to (\d+)\b", text, flags=re.M):
        found.update(range(int(m.group(1)), int(m.group(2)) + 1))
    return found


def rules_named(cell):
    named = set()
    for m in re.finditer(r"Rules? (\d+)(?: to (\d+))?", cell):
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        named.update(range(a, b + 1))
    return named


def check(skill_dir):
    problems = []
    skill_md = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
    rb_path = os.path.join(skill_dir, "references", "research-basis.md")
    rb = open(rb_path, encoding="utf-8").read()
    rules = rules_in(skill_md)
    refs = os.path.join(skill_dir, "references")
    for name in sorted(os.listdir(refs)):
        if name.endswith(".md") and name != "research-basis.md":
            rules |= rules_in(open(os.path.join(refs, name), encoding="utf-8").read())
    if "## Evidence map, checked at the source" not in rb:
        return [f"{rb_path}: no section '## Evidence map, checked at the source'"]
    table = rb.split("## Evidence map, checked at the source", 1)[1].split("\n## ", 1)[0]
    rows = [l for l in table.splitlines() if l.startswith("| ") and not l.startswith("| Rule |") and not l.startswith("|---")]
    covered = set()
    for n, line in enumerate(rows, 1):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            problems.append(f"{rb_path}: row {n} has {len(cells)} cells, not 7: {line[:60]}")
            continue
        rule, claim, verdict, source, cert, checked, access = cells
        if any(not c for c in cells):
            problems.append(f"{rb_path}: row {n} ({rule}) has an empty cell")
        covered |= rules_named(rule)
        if not verdict.startswith(VERDICTS):
            problems.append(f"{rb_path}: row {n} ({rule}) verdict '{verdict}' is not one of {', '.join(VERDICTS)}")
        for m in DOI.finditer(source):
            doi = m.group(1).rstrip(";,.)")
            if not DOI_OK.match(doi):
                problems.append(f"{rb_path}: row {n} ({rule}) bad DOI '{doi}'")
        if not (DATE.match(checked) or checked == "carried"):
            problems.append(f"{rb_path}: row {n} ({rule}) Checked is '{checked}', not a date or 'carried'")
    for r in sorted(rules - covered):
        problems.append(f"{skill_dir}: Rule {r} has no row in the evidence map")
    return problems


def main(argv):
    if not argv:
        sys.exit(__doc__)
    problems = []
    for d in argv:
        problems += check(d)
    for p in problems:
        print(p)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
