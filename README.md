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
/plugins install forge@denniscalazans-plugins
/plugins install integrations@denniscalazans-plugins
/plugins install code-quality@denniscalazans-plugins
/plugins install browser@denniscalazans-plugins
```


## Plugins

### dc — Brain Round Trip

The bridge between your brain and AI: decode messy input, stress-test ideas, distill insights back.
These work as a pipeline: **brief** decodes messy input → **grill** stress-tests the plan → **distill** produces clean output.

| Command | What it does |
|---------|-------------|
| `/dc:brief` | Turn chaotic input (voice transcription, brain dumps, messy notes) into structured, actionable output |
| `/dc:grill` | Stress-test a plan, design, or architecture through relentless prepared questioning |
| `/dc:distill` | Extract key insights and restructure content for human readers |
| `/dc:writing` | Apply one-sentence-per-line markdown convention |

**Agent:** `strategic-thinking-partner` — proactive strategic oversight and assumption challenging


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


### browser — Unified Browser Automation

Context-efficient browser automation combining [agent-browser](https://github.com/anthropics/agent-browser) for lightweight exploration with Playwright for Retina recording — both on a shared Chrome session.

| Command | What it does |
|---------|-------------|
| `/browser:login` | Authenticate into web apps using agent-browser + 1Password |
| `/browser:explore` | Inspect pages, generate replayable flows, record Retina videos — three modes, one skill |

**Agents:**
- `recorder` — generates and executes Retina recordings as a subagent, keeping the main context lean
- `playwright-healer` — debug and fix failing Playwright flows using interaction log context

**Requires:** `npm i -g agent-browser && agent-browser install`

**Install:**
```bash
/plugins install browser@denniscalazans-plugins
```


### forge — Codebase Support

Everything code-specific: start a task clean, investigate before implementing, run the adversarial pipeline, finish by cleaning up.

| Command | What it does |
|---------|-------------|
| `/forge:start` | Return to main with a clean working directory — begin a new task |
| `/forge:investigate` | Explore codebase patterns and produce a TODAY IS / EXPECTED IS report |
| `/forge:implement` | Orchestrate the adversarial pipeline with dynamic routing |
| `/forge:finish` | Delete local branches already integrated into the default branch |

**Agents:**
- `forge-investigator` — codebase explorer, auto-generates evaluator criteria
- `forge-challenger` — adversarial reviewer, finds gaps and edge cases
- `forge-planner` — designs file-level implementation approach
- `forge-generator` — writes code following the plan, self-checks against criteria
- `forge-evaluator` — adversarial code reviewer with tool-awareness

**Install:**
```bash
/plugins install forge@denniscalazans-plugins
```


### integrations — External Services

Connectors for external services.

| Command | What it does |
|---------|-------------|
| `/integrations:figma-api` | Interact with the Figma REST API for design data, tokens, and exports |
| `/integrations:op` | Manage 1Password CLI secrets with safe `op run` patterns |

**Install:**
```bash
/plugins install integrations@denniscalazans-plugins
```


## Contributing

Contributions are welcome.
See [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for skill placement rules, directory structure, naming conventions, and frontmatter templates.


## License

[MIT](LICENSE)
