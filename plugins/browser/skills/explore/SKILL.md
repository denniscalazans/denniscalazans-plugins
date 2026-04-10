---
name: explore
description: >
  Use when the user wants to inspect a web page, check UI state, verify element presence, explore
  an app interactively, create a replayable Playwright flow, or record a Retina-quality video of
  a browser interaction.
  Uses agent-browser for lightweight exploration (93% less context than Playwright MCP) and
  Playwright connectOverCDP for flows and recording — both on the same shared Chrome session.
  Framework-agnostic — works with any web application on any URL (localhost or remote).
  Triggers: "explore page", "check the UI", "what does the page look like", "snapshot", "quick look",
  "inspect the app", "agent-browser", "create a flow", "make this replayable", "record this",
  "make a video", "screen record", "capture a screencast", "PR evidence video".
---

# Explore — Inspect, Flow, Record

One skill, three modes — all on agent-browser's shared Chrome session.

**Inspect** pages with agent-browser snapshots (93% less context than Playwright MCP).
**Flow** — translate agent-browser interactions into replayable Playwright `.flow.ts` files.
**Record** — flow + CDP screencast for Retina-quality MP4/GIF evidence videos.


## Quick Start

```
/browser:explore what does the dashboard look like
/browser:explore create a flow that creates a new site
/browser:explore record the site creation process --record
```


## Prerequisites

At session start, check which tools are available:

- **agent-browser** — required for all modes; primary interaction tool.
- **Playwright** — required for Flow and Record modes; connects via `connectOverCDP`.
- **ffmpeg** — required for Record mode only; assembles frames into MP4/GIF.
- **op CLI** — required for authenticated flows using 1Password secrets.

If a required tool is missing, report it clearly before proceeding.


## Three Modes

| Mode | Triggered by | Tool used | Files generated |
|---|---|---|---|
| **Inspect** | "explore the page", "check the UI", "what's on the dashboard" | agent-browser only | None |
| **Flow** | "create a flow", "make this replayable" | agent-browser then Playwright `connectOverCDP` | `.flow.ts` |
| **Record** | "record this", `--record`, "make a video" | agent-browser then Playwright `connectOverCDP` + CDP screencast | `.flow.ts` + MP4/GIF |

### Phase order: Inspect → Generate → Run → Heal

Modes are **sequential phases**, not alternatives.
Flow and Record mode **require a complete interaction log** before they start.

1. **Inspect** — explore the app with agent-browser. Every command is auto-logged. Continue until all intended interactions are captured.
2. **Generate** — read the complete log, write the complete `.flow.ts` in one pass. Do NOT run the flow between writing steps.
3. **Run** — execute the finished `.flow.ts` once.
4. **Heal** — if the run fails, dispatch `browser:playwright-healer` to fix the flow and re-run.

If the user says "record this" or "create a flow" but no interaction log exists yet, **start with Inspect mode first**.
Explore the app, build the log, then proceed to Generate.
Never write flow steps incrementally while exploring — the log is the handoff between phases.


## Inspect Mode

Use agent-browser commands directly against the shared Chrome session.

- `agent-browser open <url>` — navigate to a URL.
- `agent-browser snapshot -i` — capture current page state (aria tree, refs, text).
- `agent-browser screenshot --annotate` — visual snapshot with numbered labels on interactive elements; use when `snapshot -i` is insufficient (canvas, icon buttons, spatial layouts). Refs are cached — interact immediately after.
- `agent-browser click @ref` — click an element by its ref id.
- `agent-browser fill @ref "text"` — type into an input by ref.
- `agent-browser scroll` — scroll the page.
- `agent-browser wait --text "Welcome"` — wait for visible text (preferred). Also: `--url "**/path"`, `--fn "expression"`, `@ref`, `--load networkidle` (last resort).
- `agent-browser eval` — execute JavaScript for DOM inspection.
- `agent-browser screenshot` — visual capture of the current viewport.
- `agent-browser diff snapshot` — text diff of accessibility tree after an interaction.
- `agent-browser diff screenshot --baseline before.png` — pixel diff with mismatch percentage.
- `agent-browser dialog status` — check for pending JS dialogs. Use `dialog accept` / `dialog dismiss` to unblock. Dialogs block all commands until dismissed.

**Efficiency:** chain independent commands with `&&` when intermediate output is not needed:

```bash
agent-browser open <url> && agent-browser wait --load networkidle && agent-browser snapshot -i
```

For longer known sequences, pipe a JSON array to `agent-browser batch --json`.

**Security:** enable `AGENT_BROWSER_CONTENT_BOUNDARIES=1` to wrap page output in nonce-tagged markers — guards against prompt injection from untrusted pages.

No files are generated in Inspect mode.
No Playwright is involved.
The interaction logger hook auto-logs every command to `.agents.tmp/.browser-log/session.jsonl` — zero manual effort.


## Flow Mode

When a replayable flow is needed, translate the **complete** interaction log into a Playwright `.flow.ts` file in **one pass**.
Do NOT write a step, run the flow, append the next step, run again — that causes O(n²) cumulative replay.
Write the complete file, then run it once.

### Step 1: Read the complete interaction log

Read `.agents.tmp/.browser-log/session.jsonl` — it contains selectors, element metadata, and interaction order captured automatically during Inspect mode.
If the log is empty or missing, go back to Inspect mode first — Flow mode cannot start without a complete log.

### Step 2: Translate to Playwright

Map each log entry to Playwright API calls using captured selectors.
Connect to the existing Chrome session via `connectOverCDP` — never launch a new browser.

Read `references/flow-template.ts` in this skill's directory for the full template.
Read `references/playwright-antipatterns.md` for banned patterns to avoid in generated flows.

In generated flows, prefer `page.getByText('Welcome').waitFor()` over `page.waitForLoadState('networkidle')` when a specific UI state is expected.
Use `agent-browser wait --text` during Inspect mode to discover the right text anchor before codifying it in the flow.

### Step 3: Write the flow file

Output path: `.agents.tmp/<ticket>/playwright/<flow-name>/<flow-name>.flow.ts`

Flows follow a two-track model that separates exploratory work from committed tests.

| | Track 2 — Exploratory Flows | Track 1 — Committed Tests |
|---|---|---|
| Files | `.agents.tmp/**/*.flow.ts` | `e2e/*.spec.ts` |
| Git | Gitignored, disposable | Committed, reviewed |
| Purpose | Exploration, investigation, recording | CI regression, permanent |
| Promotion | Promote proven flows to Track 1 | N/A |

Never write flows to `/tmp`, repo root, or any committed directory.

### Environment variables for role-agnostic flows

```bash
FLOW_ROLE=partner FLOW_APP=myapp npx playwright test <path-to-flow>
```

`FLOW_ROLE` + `FLOW_APP` env vars resolve the auth file automatically.
The flow template reads `.agents.tmp/.auth/<app>-<role>.json` when the file exists.


## Record Mode

Record mode is Flow mode plus CDP screencast.
**This mode is token-intensive** — dispatch to the `browser:recorder` agent to keep the main context lean.

### Dispatch to recorder agent

When the user triggers Record mode, dispatch to the `browser:recorder` agent with:

- **ticket** — extract from branch name (e.g., `feat/ffa-475-...` → `ffa-475`); fallback to `recording`.
- **summary** — 2-4 word kebab-case slug from the user's request (e.g., `site-creation`).
- **app URL** — the base URL of the app being recorded.
- **interaction log path** — `.agents.tmp/.browser-log/session.jsonl`.
- **produce GIF** — `true` if the user said `--gif` or asked for a GIF.
- **flow description** — what the recording should demonstrate.

The recorder agent reads the interaction log, generates a Playwright recording flow from `references/recording-template.ts`, executes it with CDP screencast, stitches frames via ffmpeg, and returns the output path.
If the flow fails, the recorder agent invokes the `browser:playwright-healer` agent internally.

### What happens inside the recorder agent

- **Viewport:** 1440x900 at `deviceScaleFactor: 2` = 2880x1800 Retina frames.
- **Cursor:** Red dot (20px), yellow flash on click, MutationObserver re-creation on DOM changes.
- **Keep-rendering:** Toggles a 1px element via `requestAnimationFrame` — forces Chrome to paint every frame during idle periods so frame capture is continuous.
- **CDP screencast:** `Page.startScreencast` at Retina resolution — yields PNG frames with wall-clock timestamps.
- **ffmpeg MP4:** 12fps, H.264, CRF 22, `-tune animation` — keeps text crisp at Retina resolution.
- **ffmpeg GIF:** 6fps, `hqdn3d` denoise, palette-optimized — append `--gif` to also generate a GIF.
- **After every navigation:** `navigateAndInject()` re-injects cursor and keep-rendering scripts.
- **Disconnect:** reset viewport and disconnect Playwright after recording completes.

### Output paths

```
.agents.tmp/recordings/YYYYMMDD-<ticket>-<summary>.mp4
.agents.tmp/recordings/YYYYMMDD-<ticket>-<summary>.gif   (with --gif)
```

### What the main agent receives

The recorder agent returns a structured report with the output file path(s) and file sizes.
No frame data, ffmpeg logs, or healing iterations leak into the main context.


## Selector Strategy

Follow the priority order below.
Read `references/selector-strategy.md` for full details and examples.

1. `data-test-id` / `data-testid` — most stable, explicit test contract.
2. `id` attribute — stable if not auto-generated.
3. `name` + tag — good for form inputs.
4. `formcontrolname` — Angular reactive forms.
5. Structural CSS — position-based, use when others are absent.
6. Role + accessible name — last resort; fragile with i18n changes.


## Interaction Log

Every agent-browser command is auto-logged by the PostToolUse hook.

Log path: `.agents.tmp/.browser-log/session.jsonl`

Each line is a JSON object:

```jsonl
{"ts":"2026-03-31T10:00:00Z","cmd":"snapshot","args":{"-i":true},"ref":null}
{"ts":"2026-03-31T10:00:01Z","cmd":"click","args":{},"ref":"@a1b2c3","text":"Create site"}
{"ts":"2026-03-31T10:00:02Z","cmd":"fill","args":{},"ref":"@d4e5f6","value":"Stockholm"}
```

Read this log before generating flows — it has the actual refs and values captured during exploration.


## Integration with Login

Use `/browser:login` before exploring apps that require authentication.

The login skill writes a persistent Chrome session that agent-browser reuses — no auth export needed.
Named sessions follow the pattern `--session <app>-<role>`.

Same agent-browser session means no additional auth wiring for flows or recordings.


## Common Mistakes

| Do NOT | Do instead |
|--------|-----------|
| Use Playwright MCP `browser_snapshot` for diagnostics | Use `agent-browser snapshot -i` (same Chrome, 93% less context) |
| Launch a new Chrome for flows | Connect via `connectOverCDP` to agent-browser's Chrome |
| Use `page.goto()` in recording flows | Use `navigateAndInject()` to re-inject cursor scripts |
| Generate Playwright config files | Use the project's permanent config |
| Write flows to repo root or /tmp | Always write to `.agents.tmp/<ticket>/playwright/<flow-name>/` |
| Use `addInitScript()` for cursor injection | Use `page.evaluate()` — it works with `connectOverCDP` |
| Skip the interaction log | Read it first — it has selectors and element metadata |
| Use text-based selectors as first choice | Follow selector priority: test-id > id > name > formcontrol > CSS > role |
| Commit `.agents.tmp/` files | Track 2 is gitignored; promote to Track 1 when proven |
| Default to `wait --load networkidle` for every wait | Use `wait --text`, `wait --url`, or `wait @ref` when a specific condition is known |
| Ignore unexpected command timeouts | Check `agent-browser dialog status` — a pending dialog blocks everything |
| Issue many single-command Bash calls for a known sequence | Chain with `&&` or use `agent-browser batch --json` |
| Write flow steps incrementally, running after each append | Write the complete `.flow.ts` from the log in one pass, run once at the end |
| Start Flow/Record mode without a complete interaction log | Complete Inspect mode first — the log is the handoff between phases |
| Dispatch subagents to both write AND run flow files | Write all flow files in the main context, then dispatch subagents to run only (Bash) |
| Use `waitForApi` after navigation to verify data loaded | Prefer DOM markers (`[data-test-id="data-loaded"]`) — they verify the full rendering pipeline |
