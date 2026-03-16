# denniscalazans-plugins

Personal Claude Code plugin marketplace.


## Plugins

### dc -- General Purpose

Git workflow, knowledge distillation, video recording, markdown conventions, and strategic thinking.

| Command | Description |
|---------|-------------|
| `/dc:reset` | Return to main branch with a clean working directory |
| `/dc:clean-branches` | Delete local branches already integrated into the default branch |
| `/dc:distill` | Extract key insights and restructure content for human readers |
| `/dc:brief` | Turn brain dumps and messy thoughts into structured briefs for AI agents |
| `/dc:record` | Record Retina-quality browser screencasts via CDP |
| `/dc:writing` | Apply one-sentence-per-line markdown convention |
| `/dc:figma-api` | Interact with the Figma REST API for design data, tokens, and exports |
| `/dc:op` | Manage 1Password CLI secrets with safe `op run` patterns |

**Agent:** `strategic-thinking-partner` -- proactive strategic oversight and assumption challenging.


### code-quality -- SonarQube Integration

SonarQube-driven code quality workflows via MCP.

| Command | Description |
|---------|-------------|
| `/code-quality:sonar-status` | Check quality gate status and dashboard metrics |
| `/code-quality:sonar-issues` | Browse and search SonarQube issues with safe pagination |
| `/code-quality:sonar-fix` | Fix a SonarQube issue with rule lookup and local verification |
| `/code-quality:sonar-verify` | RED/GREEN validation -- cross-reference server issues with local analysis |
| `/code-quality:sonar-triage` | Mark issues as false positive, accepted, or reopened |
| `/code-quality:sonar-rule` | Look up a SonarQube rule with compliant/noncompliant examples |
| `/code-quality:sonar-setup` | Set up SonarQube MCP integration and diagnose connectivity |
| `/code-quality:sonar-env` | Inspect local SonarQube infrastructure (IDE ports, MCP containers) |

**Agent:** `code-quality-agent` -- orchestrates multi-step quality workflows (audits, batch fixes, PR reviews).


## Installation

```bash
/plugins marketplace add denniscalazans/denniscalazans-plugins
/plugins install dc@denniscalazans-plugins
/plugins install code-quality@denniscalazans-plugins
```


## Contributing

See `.claude/CLAUDE.md` for skill placement rules, directory structure, naming conventions, and frontmatter templates.
