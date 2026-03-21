# Contributing

Thanks for your interest in contributing.
This marketplace is open to new plugins and skills.


## Quick start

1. Fork and clone the repo
2. Read [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for the full contribution guide — it covers directory structure, naming conventions, skill frontmatter, and plugin manifests
3. Create your plugin or skill following the patterns in the existing `dc` or `code-quality` plugins
4. Open a PR


## Adding a skill to an existing plugin

```bash
mkdir -p plugins/<plugin>/skills/<skill-name>
# Write your SKILL.md following the frontmatter template in .claude/CLAUDE.md
```

Skills need a `SKILL.md` file with YAML frontmatter (`name` + `description`) and a markdown body.
The description should start with "Use when..." and include trigger phrases.


## Creating a new plugin

Create a new plugin when the skills serve a distinct domain not covered by existing plugins.
See the "When to Create a New Plugin" section in `.claude/CLAUDE.md` for the criteria.


## Running tests

```bash
npm install
npm test
```


## Conventions

- Conventional commits: `feat(plugin):`, `fix(plugin):`, `chore:`
- One sentence per line in markdown
- TDD for any code with logic (scripts, utilities)
