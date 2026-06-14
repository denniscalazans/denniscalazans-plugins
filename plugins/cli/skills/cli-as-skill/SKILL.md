---
name: cli-as-skill
description: >
  Use when the user wants to turn a researched CLI tool into a reusable, production-quality
  Claude skill for operating that one tool safely. Consumes a research bundle produced by
  learn-a-cli and generates a per-tool skill folder (SKILL.md plus references/, recipes/,
  and a version-drift preflight). Defaults to one skill per tool, refreshed in place.
  Triggers: "package this CLI as a skill", "make a skill for gh/kubectl/aws", "turn the
  research bundle into a skill", "generate a CLI skill", "cli as skill", "create an
  operating skill for this tool".
argument-hint: "<path-to-bundle> [output-dir]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# cli-as-skill — package a research bundle into a per-tool skill

Turn a `learn-a-cli` research bundle into ONE skill folder that teaches Claude to operate
that specific CLI safely and effectively.

You read the bundle and write files.
You do NOT run the target CLI here — that's the generated skill's job, not the packager's.

## Inputs

- **bundle** (required) — path to a bundle dir, e.g. `.agents.tmp/cli-research/gh@2.62.0/`.
  If omitted, look under `.agents.tmp/cli-research/` and ask which tool if more than one.
- **output-dir** (optional) — where to write the skill. Default `~/.claude/skills/`.
  Use a project's `.claude/skills/` instead when the tool is project-specific.

## Output

Create `<output-dir>/<tool>-cli/` using the per-tool template (below).
The folder name is always `<tool>-cli` — the directory name becomes the command,
so keep it lowercase-kebab.

```
<tool>-cli/
├── SKILL.md
├── scripts/preflight.sh          # version-drift check (from this skill's assets/preflight.sh)
├── references/
│   ├── VERSION                   # one line: "<tool> <version> | researched <date>"
│   ├── help.txt
│   ├── man-notes.md
│   ├── examples.md
│   ├── dangerous-operations.md
│   └── troubleshooting.md
└── recipes/
    └── <task>.md
```

## Procedure

1. **Read the bundle.** Load `bundle.md` and `metadata.json` first. Pull in reference files only as needed — don't load everything into context at once.

2. **Decide if a skill is even warranted.** A dedicated skill earns its place when the tool is (used often) AND (complex OR dangerous). If it's a simple, safe, rarely-used tool, tell the user it's cheaper to research live and stop. Note: "used often" isn't in the bundle — it's a judgment call from general knowledge and the user's stated intent. When unsure, ask the user rather than guessing.

3. **One skill per tool — the version rule.** Default to one skill per tool, version-pinned, refreshed in place. Do NOT generate `<tool>-v2`, `<tool>-v3` side by side — parallel version-skills break triggering (descriptions match the same intent, and the installed version isn't a selection signal), multiply context cost, and split safety fixes.

   Before generating, check the output dir for an existing `<tool>-cli/`:
   - **Exists, same tool** → this is a **refresh**. Regenerate in place from the fresh bundle. Git history preserves the prior version; don't fork a copy.
   - **Doesn't exist** → generate normally.

   **When multiple skills ARE justified:** only when both versions are installed AND used concurrently AND their contracts diverge enough that one SKILL.md can't stay clear and safe (e.g. `terraform 0.x` vs `1.x`, `python2` vs `python3`).

   ```
   More than one version installed AND used concurrently?
   ├─ No  → ONE skill, refresh in place on upgrade.            (default — almost always)
   └─ Yes → Contracts diverge enough that one SKILL.md can't stay clear/safe?
             ├─ No  → ONE skill that branches on the preflight DRIFT= verdict.
             └─ Yes → Separate skills, named by major (terraform0-cli / terraform1-cli),
                      scoped with the `paths` frontmatter field so the project auto-selects.
   ```

4. **Generate `SKILL.md`** — concise and operational, under 500 lines. It must:
   - State when to use this CLI and when to reach for something else.
   - Show how to explore safely, **read-only commands first**.
   - Include the **Built for**, **Preflight**, and **If a command fails** sections (templates below).
   - Give 2–4 complete workflows, each split into read-only / mutating / destructive.
   - Document preferred default flags (`--json`, `--quiet`, `--limit`, dry-run).
   - Cover exit-code handling and the top error→recovery flows inline.
   - Link out to `references/*` for depth — never inline raw dumps.

5. **Generate `scripts/preflight.sh`** from this skill's `assets/preflight.sh`, replacing `__TOOL__`, `__BUILT_FOR__`, `__VERSION_CMD__`, `__RESEARCHED_ON__` with values from `metadata.json`. `chmod +x` it. `__VERSION_CMD__` must be a simple space-delimited command (e.g. `jq --version`) — it runs unquoted, so no pipes, quotes, or shell metacharacters.

6. **Generate reference files** from the bundle (one level deep, TOC if >100 lines). The bundle and the skill use different file vocabularies — map them explicitly:

   | Bundle file | → Skill reference file | Notes |
   |-------------|------------------------|-------|
   | `VERSION` | `references/VERSION` | copy verbatim; canonical source for the "Built for" line |
   | `help.txt` | `references/help.txt` | copy |
   | `man-notes.md` | `references/man-notes.md` | copy |
   | `examples.md` | `references/examples.md` | copy |
   | `safety.md` | `references/dangerous-operations.md` | extract the destructive rows + guards |
   | `safety.md` (exit codes) | `references/troubleshooting.md` | build error→code→recovery from exit-code semantics + common errors |
   | `structured-output.md` | carry forward as `references/structured-output.md` | link from SKILL.md if the tool relies on it |
   | `language.md` (if present) | carry forward as `references/language.md` | filter/expression tools — link prominently, it's the command surface |

7. **Generate `recipes/`** — task-oriented end-to-end flows, each leading with the dry-run/preview step.

8. **Carry the scorecard forward.** If the bundle flagged gaps (no `--json`, interactive-only), encode the workaround in SKILL.md.

9. **Report** the created tree and how to test it (see packaging checklist).

## Required SKILL.md sections (templates)

Inject these verbatim, filling the placeholders:

```markdown
## Built for
This skill was researched against **<tool> <version>** on **<date>**.

## Preflight — ALWAYS run first
Before any <tool> command, run `bash "${CLAUDE_SKILL_DIR}/scripts/preflight.sh"` and read the `DRIFT=` verdict (plus the separate `STALE=` flag):
- **EXACT / PATCH** → proceed normally.
- **MINOR / DOWNGRADE / UNKNOWN** → surface the ⚠️ banner verbatim, then proceed,
  but verify any flag against `<tool> <cmd> --help` before relying on it.
- **MAJOR** → surface the 🛑 banner verbatim. Do NOT run mutating or destructive commands.
  Recommend `/cli:learn-a-cli <tool>` to refresh. Continue only on explicit "proceed anyway".
- **MISSING** → stop. Tell the user to install <tool>. Do not improvise.
- **STALE=yes** (independent of the DRIFT level) → surface the staleness ⚠️ banner; verify flags against `--help` before mutating even if the version matches.

## If a documented command fails
If a command from this skill returns "unknown flag", "unknown command", or "unexpected argument",
do NOT guess an alternative — the skill has likely drifted from the installed version.
1. Run `<tool> <cmd> --help` to find the current flag.
2. Tell the user the skill appears out of date and recommend `/cli:learn-a-cli <tool>`.
3. Only adapt the single command after confirming against --help.
```

## Safety defaults baked into every generated skill

- Read-only discovery before any mutation.
- Mutating commands run only when the user's intent is clearly to change state.
- Destructive commands require explicit intent ("apply", "delete", "force") AND a dry-run first where supported.
- Prefer structured output, pagination, and filters to keep output bounded.
- Avoid interactive prompts; document the non-interactive flag instead.

## Common mistakes

| Don't | Do |
|-------|-----|
| Inline the full help dump in SKILL.md | Summarize; link `references/help.txt` |
| Generate a skill for every tool | Only when used-often AND (complex OR dangerous) |
| Fork `<tool>-v2` for a new version | Refresh the one skill in place; git keeps history |
| Bury destructive ops among safe ones | Separate read-only / mutating / destructive sections |
| Omit the dry-run step from mutating recipes | Lead every mutating recipe with its preview |
| Skip the preflight wiring | Always generate `scripts/preflight.sh` + the Preflight section |
| Use `bash scripts/preflight.sh` (relative path) in the injected preflight line | Use `bash "${CLAUDE_SKILL_DIR}/scripts/preflight.sh"` — agents run with the user's CWD, not the skill's dir |
