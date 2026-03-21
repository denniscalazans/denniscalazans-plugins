# denniscalazans-plugins

[![CI](https://github.com/denniscalazans/denniscalazans-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/denniscalazans/denniscalazans-plugins/actions/workflows/ci.yml)
[![SonarCloud](https://sonarcloud.io/api/project_badges/measure?project=denniscalazans_denniscalazans-plugins&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=denniscalazans_denniscalazans-plugins)
[![codecov](https://codecov.io/gh/denniscalazans/denniscalazans-plugins/branch/main/graph/badge.svg)](https://codecov.io/gh/denniscalazans/denniscalazans-plugins)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A personal collection of Claude Code plugins shaped by daily use.
These skills started as shortcuts for my own workflow — dealing with messy voice transcriptions, forgetting to investigate before coding, merging branches I forgot to clean up.
Over time they became structured enough to share.


Some are portable (you can drop them into any project), others are opinionated (they reflect how I like to work).
Take what's useful, ignore what isn't.


## Installation

```bash
/plugins marketplace add denniscalazans/denniscalazans-plugins
/plugins install dc@denniscalazans-plugins
/plugins install code-quality@denniscalazans-plugins
```


## Plugins

### dc — General Purpose

Skills I reach for every day: thinking before coding, cleaning up after merging, turning brain dumps into something actionable.

#### Thinking skills

These work together as a pipeline: **brief** decodes messy input, **investigate** maps the codebase, **grill** stress-tests the plan.

| Command | What it does |
|---------|-------------|
| `/dc:brief` | Turn chaotic input (voice transcription, brain dumps, messy notes) into structured, actionable output |
| `/dc:investigate` | Explore codebase patterns and constraints before implementing — produces a TODAY IS / EXPECTED IS report, then stops |
| `/dc:grill` | Stress-test a plan, design, or architecture through relentless prepared questioning |
| `/dc:distill` | Extract key insights and restructure content for human readers |

#### Workflow skills

| Command | What it does |
|---------|-------------|
| `/dc:reset` | Return to main branch with a clean working directory |
| `/dc:clean-branches` | Delete local branches already integrated into the default branch |
| `/dc:writing` | Apply one-sentence-per-line markdown convention |
| `/dc:record` | Record Retina-quality browser screencasts via CDP |
| `/dc:figma-api` | Interact with the Figma REST API for design data, tokens, and exports |
| `/dc:op` | Manage 1Password CLI secrets with safe `op run` patterns |

#### Browser testing skills

| Command | What it does |
|---------|-------------|
| `/dc:browser-login` | Manage persistent browser sessions with playwright-cli and 1Password for authenticated apps |
| `/dc:navigate` | Generate disposable Playwright .flow.ts files for exploratory browser testing |

**Agents:** `strategic-thinking-partner` — proactive strategic oversight and assumption challenging.
`playwright-healer` — debug and fix failing Playwright tests automatically.


### code-quality — SonarQube Integration

SonarQube-driven code quality workflows via MCP.

| Command | What it does |
|---------|-------------|
| `/code-quality:sonar-status` | Check quality gate status and dashboard metrics |
| `/code-quality:sonar-issues` | Browse and search SonarQube issues with safe pagination |
| `/code-quality:sonar-fix` | Fix a SonarQube issue with rule lookup and local verification |
| `/code-quality:sonar-verify` | RED/GREEN validation — cross-reference server issues with local analysis |
| `/code-quality:sonar-triage` | Mark issues as false positive, accepted, or reopened |
| `/code-quality:sonar-rule` | Look up a SonarQube rule with compliant/noncompliant examples |
| `/code-quality:sonar-setup` | Set up SonarQube MCP integration and diagnose connectivity |
| `/code-quality:sonar-env` | Inspect local SonarQube infrastructure (IDE ports, MCP containers) |

**Agent:** `code-quality-agent` — orchestrates multi-step quality workflows (audits, batch fixes, PR reviews).


## Contributing

Contributions are welcome.
See [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for skill placement rules, directory structure, naming conventions, and frontmatter templates.


## License

[MIT](LICENSE)
