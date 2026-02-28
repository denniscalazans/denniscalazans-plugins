# Marketplace Contribution Guide

## Skill Placement

| Scope | Plugin | When to use |
|-------|--------|-------------|
| General-purpose | `dc` | Portable across any project: git workflow, distillation, video recording, markdown conventions |
| Proprietary | `ak` | Proprietary tooling |
| New plugin | `plugins/<name>/` | A distinct domain that doesn't fit `dc` or `ak` (e.g. a "devops" plugin for CI/CD skills) |

When creating or migrating a skill, present the recommendation before placing it:

```
Skill placement: I recommend [plugin] because [reason].
```

Ask before placing the skill if the placement is ambiguous.

## When to Create a New Plugin

Create a new plugin (instead of adding to `dc` or `ak`) when ALL three criteria are met:

1. **Domain boundary** -- the skills serve a distinct domain not covered by existing plugins
2. **No keyword overlap** -- the skills' trigger keywords don't overlap with existing plugin skills
3. **Multiple future skills** -- you can envision at least 2-3 skills living in this domain

## Directory Structure

```
plugins/<plugin-name>/
  .claude-plugin/
    plugin.json            # Plugin manifest (name, description, version, keywords)
  skills/
    <skill-dir>/
      SKILL.md             # Skill definition (frontmatter + body)
      references/          # Optional: reference files the skill reads
      scripts/             # Optional: executable scripts bundled with the skill
  agents/
    <agent-name>.md        # Agent definition (frontmatter + system prompt)
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Plugin directory | lowercase, short noun | `dc`, `ak`, `devops` |
| Skill directory | lowercase-kebab, short slug | `reset/`, `record/`, `ds-sync-keys/` |
| Skill file | `SKILL.md` (always) | `skills/reset/SKILL.md` |
| Agent file | `<agent-name>.md` | `agents/strategic-thinking-partner.md` |
| Reference files | descriptive filename | `references/recording-template.ts` |
| Script files | descriptive filename | `scripts/collect.ts` |

## Slash Command Mapping

The **directory name** becomes the slash command suffix.

`/plugin-name:directory-name` -- e.g. `plugins/dc/skills/reset/` becomes `/dc:reset`.

Choose directory names that are short and memorable.

## Skill Frontmatter

```yaml
---
name: <short-name>
description: >
  Use when [triggering conditions].
  Also use when [secondary triggers].
  Triggers: "keyword1", "keyword2", "keyword3".
---
```

Field rules:

- **name** + **description** combined must be under 1024 characters
- **description** starts with "Use when..." -- triggering conditions only, not workflow summary
- Third person, technology-agnostic language
- Include symptom keywords for discoverability
- Optional: `allowed-tools`, `argument-hint`

## Agent Frontmatter

```yaml
---
name: <agent-name>
description: <CSO description with examples>
tools: <comma-separated tool list>
model: <opus|sonnet|haiku>
color: <pink|blue|green|orange|purple>
---
```

## Description Rules (CSO Format)

- Start with "Use when..." or "Use this agent when..."
- Describe **triggering conditions**, not workflow steps
- Include concrete keyword triggers
- Add `<example>` blocks showing user message -> assistant action -> agent output
- No workflow summaries in the description -- that belongs in the body

## Skill Body Structure

1. **Title** -- `# Skill Name`
2. **Overview** -- 1-2 sentences explaining what the skill does
3. **Process** -- Step-by-step instructions Claude follows when the skill is invoked
4. **Examples** -- Concrete examples where relevant
5. **Common Mistakes** -- Table of don't/do pairs (optional but recommended)

## Adding a New Plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<name>",
  "description": "<one-line description>",
  "version": "1.0.0",
  "author": { "name": "Dennis Calazans" },
  "keywords": ["keyword1", "keyword2"]
}
```

2. Register in `.claude-plugin/marketplace.json` by adding an entry to the `plugins` array:

```json
{
  "name": "<name>",
  "description": "<one-line description>",
  "source": "./plugins/<name>",
  "category": "productivity"
}
```

3. Create skills under `plugins/<name>/skills/<skill-dir>/SKILL.md`.

4. Commit and install:

```bash
git add -A && git commit -m "Add <name> plugin with <skill> skill"
/plugin install <name>@denniscalazans-plugins
```
