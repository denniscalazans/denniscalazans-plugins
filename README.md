# denniscalazans-plugins

Personal Claude Code plugin marketplace.

## Plugins

### dc -- General Purpose

Git workflow, knowledge distillation, video recording, markdown conventions, and strategic thinking.

| Command | Description |
|---------|-------------|
| `/dc:reset` | Return to main branch with clean working directory |
| `/dc:distill` | Extract key insights from content |
| `/dc:record` | Record Retina-quality browser screencasts |
| `/dc:writing` | Apply one-sentence-per-line markdown convention |

**Agent:** `strategic-thinking-partner` -- proactive strategic oversight and assumption challenging.

### ak -- REDACTED Forest Flow

Auth0 login, translation management, and Dictionary Service integration.

| Command | Description |
|---------|-------------|
| `/ak:login` | Auth0 login via playwright-cli + 1Password |
| `/ak:i18n` | FFA translation conventions and workflow |
| `/ak:ds-guide` | Dictionary Service API reference |
| `/ak:ds-sync-keys` | Detect DS gaps and generate import CSV |

## Installation

```bash
/plugin marketplace add ~/git/denniscalazans-plugins
/plugin install dc@denniscalazans-plugins
/plugin install ak@denniscalazans-plugins
```

## Contributing

See `.claude/CLAUDE.md` for skill placement rules, directory structure, naming conventions, and frontmatter templates.
