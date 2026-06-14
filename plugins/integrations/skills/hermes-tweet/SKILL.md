---
name: hermes-tweet
description: >
  Use when installing or operating Hermes Tweet for Hermes Agent X/Twitter
  research, timeline reading, tweet analysis, mention checks, launch monitoring,
  giveaway audits, or approval-gated account actions. Also use when a workflow
  needs current X/Twitter context through Hermes Agent. Triggers: "hermes tweet",
  "x/twitter", "tweet research", "twitter monitoring", "x monitor",
  "tweet action", "xquik".
---

# Hermes Tweet

Hermes Tweet adds an X/Twitter integration to Hermes Agent.
Use it for read-first social research, launch monitoring, mention triage, giveaway audits, and guarded account actions.

## Setup

Install Hermes Tweet into the Hermes Agent Python environment:

```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install hermes-tweet
hermes plugins enable hermes-tweet
```

Set credentials on the Hermes runtime host, not in prompts:

```bash
export XQUIK_API_KEY="<your-api-key>"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Keep `HERMES_TWEET_ENABLE_ACTIONS` set to `false` unless the session explicitly needs account-changing routes.

## Process

1. Clarify the objective: research, monitoring, support triage, giveaway audit, or action preparation.
2. Collect the target: handle, tweet URL, keyword, list, monitor, or trend.
3. Search the bundled endpoint catalog with `tweet_explore` before choosing a route.
4. Read X/Twitter data through `tweet_read` after selecting a catalog-listed route.
5. Propose account-changing routes separately and wait for explicit user approval.
6. Execute approved account actions with `tweet_action` only when `HERMES_TWEET_ENABLE_ACTIONS=true`.

## Tool Model

| Tool | Use |
|------|-----|
| `tweet_explore` | Discover matching endpoint catalog routes without an API key. |
| `tweet_read` | Call catalog-listed read-only routes with `XQUIK_API_KEY`. |
| `tweet_action` | Call approved account-changing routes when action gating is enabled. |

## Output Format

```text
Summary:
- What was checked and why

Read routes:
- Catalog route, input, and useful findings

Action plan:
- Proposed account-changing calls, each awaiting approval

Next check:
- Follow-up route or monitoring cadence, if useful
```

## Examples

Research a public account before drafting:

```text
Use Hermes Tweet to inspect recent public context for @example before drafting a reply.
Keep actions disabled.
```

Monitor launch mentions:

```text
Track X/Twitter mentions for "Example Launch" today.
Summarize themes and notable accounts.
Do not post.
```

Prepare a guarded post:

```text
Draft a launch tweet and show the exact tweet_action call you would use.
Wait for approval before any action route.
```

## Common Mistakes

| Don't | Do |
|-------|-----|
| Paste API keys into prompts | Store `XQUIK_API_KEY` in the Hermes runtime environment |
| Guess endpoint paths | Discover catalog routes with `tweet_explore` |
| Enable actions for research | Keep actions disabled for read-only sessions |
| Post without confirmation | Wait for explicit approval before `tweet_action` |
| Return raw route dumps | Summarize only the data needed for the task |

## Reference

Hermes Tweet source and install notes: https://github.com/Xquik-dev/hermes-tweet#readme
