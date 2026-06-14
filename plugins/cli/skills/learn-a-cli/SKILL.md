---
name: learn-a-cli
description: >
  Use when the user wants to deeply research and understand a CLI tool before using
  it, or to produce a reusable research bundle about a command-line tool. Inspects
  local --help and man pages first, then official docs and the source repo, and
  captures the command surface, flags, structured-output modes, config, exit codes,
  safety profile, and examples into a structured bundle on disk.
  Triggers: "learn the X CLI", "research this command-line tool", "understand gh/kubectl/aws",
  "how does this CLI work", "map a CLI's commands", "is this CLI agent-friendly",
  "build a research bundle for a tool".
argument-hint: "<tool-name> [version] [scope: core|full]"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, Grep, Glob
---

# learn-a-cli — research any CLI into a reusable bundle

Produce a structured, on-disk **research bundle** for one CLI tool.
This bundle is the durable output.
It is consumed later by `cli-as-skill`, and is useful on its own.

Research is **read-only**.
You inspect, read, and search the web.
You write only into the bundle directory.
You never run a command that changes the system you are researching.

## Inputs

- **tool** (required) — the command name, e.g. `gh`, `kubectl`, `ffmpeg`.
- **version** (optional) — pin research to a version. If omitted, detect the installed version and record it.
- **scope** (optional, default `core`) — `core` covers top-level + the most-used subcommands; `full` walks the entire subcommand tree. Start `core` unless asked otherwise; full trees are large and burn context.

## Output location

Write to `.agents.tmp/cli-research/<tool>@<version>/`.
Record the EXACT version you based research on — behavior is version-specific.
Also record `researched_on` (today's date) so downstream staleness checks work.

```
.agents.tmp/cli-research/<tool>@<version>/
├── bundle.md              # front page: metadata, scorecard, summaries
├── metadata.json          # machine-readable: name, version, researched_on, homepage, docs, scorecard
└── references/
    ├── VERSION            # one line: "<tool> <version> | researched <date>"
    ├── help.txt           # verbatim --help captures
    ├── man-notes.md       # ENVIRONMENT / FILES / EXIT STATUS / EXAMPLES
    ├── command-tree.md    # subcommand hierarchy / invocation options + key flags
    ├── language.md        # ONLY for filter/expression tools (jq, awk, sed): operators, builtins, idioms
    ├── structured-output.md
    ├── safety.md
    └── examples.md
```

## Procedure

Follow these phases in order. Official docs override community sources on any conflict.

### Phase 1 — Local inspection (authoritative for installed behavior)

Run these read-only commands and capture output verbatim into `references/help.txt`:

- `command -v <tool>` and `<tool> --version` (or `version`, `-V`) — confirm presence and exact version.
- `<tool> --help` (and `-h`, `help`) — top-level description, subcommand list, global flags.
- For each key subcommand (in `core`, the 5–10 most important): `<tool> <sub> --help` — required vs optional args, subcommand flags, inline examples.
- `man <tool>` if present — extract DESCRIPTION, SYNOPSIS, ENVIRONMENT, FILES, EXIT STATUS, EXAMPLES, BUGS, NOTES into `references/man-notes.md`.

If a help command appears to launch a pager or prompt, pipe through `cat` or add the tool's non-interactive flag — never block on interaction.

### Phase 2 — Web research (authoritative for canonical reference)

- **Official docs site** — canonical command reference, structured-output flags, version notes, breaking changes.
- **Official repo** (GitHub/GitLab) — README, usage, CHANGELOG/release notes for behavioral changes at the pinned version.
- **Credible community** (only after the above) — pitfalls, edge cases, real-world idioms. Mark these as community-sourced.

### Phase 3 — Extract & classify

First identify the tool's **grammar class** — it determines how to structure `command-tree.md`:

- **Subcommand-based** (`gh`, `kubectl`, `aws`) — noun/verb tree. Default structure.
- **Filter/expression-based** (`jq`, `awk`, `sed`, `dc`) — no subcommands; the *expression language* is the command surface. Capture the language (operators, builtins, common idioms) in `references/language.md` and use `command-tree.md` for invocation options/flags only. State plainly that the tool has no subcommands.
- **Single-purpose** (`curl`, `rsync`) — one action, many flags. `command-tree.md` is a flag catalog.

Populate the reference files. At minimum capture:

- **Command grammar** → `references/command-tree.md`: structure per the grammar class above; what each command/expression operates on.
- **Flags** → `command-tree.md`: required vs optional; global vs subcommand-specific.
- **Structured output & streams** → `references/structured-output.md`: `--json` / `-o json` / `--format`; stdout (data) vs stderr (diagnostics); quiet/bare modes; pagination/limit/filter flags (`--limit`, `--page-size`, `--filter`, `--selector`, `--query`, `--jq`); stdin/piping support.
- **Config & auth** → `structured-output.md` or `safety.md`: config file locations, honored env vars, auth methods and headless-auth options.
- **Safety classification** → `references/safety.md`: every notable command sorted into **read-only / mutating-safe / destructive**; dry-run flags (`--dry-run`, `--check`, `plan`, `--dry-run=server`); confirmation-bypass flags (`--yes`, `--force`, `--no-confirm`) and when each is safe; exit-code meanings (distinct codes per failure class are an emerging convention, not standardized — record the tool's actual documented codes).
- **Examples** → `references/examples.md`: copy-pasteable, using best-practice flags — at least one read-only and one mutating workflow, with the dry-run preview shown first.

### Phase 4 — Agent-friendliness scorecard

Grade the tool yes/no on these 12 criteria and record in `metadata.json` + `bundle.md`:

1. Machine-readable output with a stable schema
2. Data→stdout, diagnostics→stderr
3. Detects TTY, switches to non-interactive when piped
4. Non-interactive bypass exists and never hangs on a prompt
5. Headless auth via env/token (no mandatory browser)
6. Distinct documented exit codes per failure class
7. Structured errors (code + remediation), not just prose
8. Dry-run that emits a structured diff
9. Output bounding mechanism exists (flags like `--limit`/`--fields`/`--filter`, OR in-language bounding as in jq)
10. Idempotent mutations; destructive ops gated behind flags
11. Stable contract (additive; unknown commands hard-fail)
12. Machine-discoverable capabilities (help/schema introspection)

**Scoring N/A criteria:** when a criterion doesn't apply because the tool lacks that whole capability (e.g. a read-only tool has no mutations, so #8 dry-run and #10 destructive-gating are moot), mark it `N/A`, not pass or fail. Compute the tier over *applicable* criteria only, and list N/A items so the gap is honest. Don't score absence-of-feature as a vacuous pass for some criteria and a fail for others — that silently moves the tier boundary.

**Tier:** *friendly* = passes 1,2,4 · *ready* = friendly + 3,6,8,9 · *native* = ready + 5,7,10,11,12 (N/A criteria don't block a tier).
List the failing criteria explicitly under "Gaps" so a future skill knows what to guard around (e.g. "no `--json`: must parse text output", "interactive confirm only: needs env bypass").

## Bundle summary (`bundle.md`)

Keep this concise — it's the front page. Use this structure:

```
# <tool> @ <version> — research bundle
## Metadata
tool · version · researched_on · homepage · docs URL · install source
## Agent-friendliness: <tier> (<n>/12)  — see scorecard below
## What it is / what it's for
## Command hierarchy (summary) → references/command-tree.md
## Structured output & streams (summary) → references/structured-output.md
## Safety profile (summary) → references/safety.md
## Examples (summary) → references/examples.md
## Scorecard (12 rows) + Gaps
```

## Common mistakes

| Don't | Do |
|-------|-----|
| Run mutating commands "to see what happens" | Stay read-only; learn mutations from docs/help, never by executing them |
| Dump raw `--help` into `bundle.md` | Summarize in `bundle.md`, put verbatim captures in `references/` |
| Walk the full subcommand tree by default | Default to `core` scope; only go `full` when asked |
| Trust a community blog over official docs | Official docs win on every conflict; tag community claims |
| Forget the version | Record the exact version and date — behavior changes between releases |
