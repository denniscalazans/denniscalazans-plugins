# Browser Skills Pipeline — Quick Manual

The browser toolset is a pipeline of four skills and one agent that work together for authenticated browser automation, exploration, and evidence capture.


## The Pipeline

```
dc:op  →  dc:browser-login  →  dc:navigate  →  dc:record
                                     ↓
                            playwright-healer (agent)
```

Each skill handles one concern.
Use them in sequence depending on what you need.


## 1. `/dc:op` — Credential Security

The foundation layer.
Ensures secrets never enter the conversation.

**When:** Setting up 1Password `.env` profiles for your app roles.

**Key rule:** Always `op run`, never `op read` or `op inject`.

**Setup (one-time per project):**

```
.agents.local/login/my-app-admin.env
```

```env
LOGIN_USER="op://Vault/My App Admin/username"
LOGIN_PASS="op://Vault/My App Admin/password"
```

These are vault *references*, not real credentials.
`op run` resolves them in-memory only.


## 2. `/dc:browser-login` — Authenticated Sessions

Opens persistent named browser sessions with credentials injected securely.

**When:** You need to log into an app before navigating or recording.

**Three tiers (fallback chain):**

| Tier | Method | When |
|------|--------|------|
| 1 | Automated script | `op run --env-file=... login.sh app role url` — finds form, fills, submits |
| 2 | Manual + reuse | `playwright-cli -s=app-role open --headed --persistent url` — log in manually once, reuse forever |
| 3 | Guided setup | First-time: create config files, then use Tier 1 or 2 |

**Session management:**

```bash
playwright-cli list                    # active sessions
playwright-cli -s=my-app-admin close   # close one
playwright-cli close-all               # close all
```

**Parallel login (multiple roles at once):**

```bash
parallel-login.sh my-app http://localhost:4200 admin editor viewer
```


## 3. `/dc:navigate` — Exploratory Flow Files

Generates replayable Playwright `.flow.ts` files for UI exploration and verification.

**When:** You want to verify UI behavior, explore a feature, or build a baseline.

**Usage:**

```
/dc:navigate create a record and verify it appears in the listing
/dc:navigate fill the form and submit, then verify the success message
```

**Key concepts:**

- **Disposable** — flow files live in `.agents.tmp/` (gitignored), not committed.
- **Role-agnostic** — set `FLOW_ROLE=admin` env var; the template resolves auth automatically.
- **Four phases:** PLAN → GENERATE → HEAL → IMPROVE.

**Output structure:**

```
.agents.tmp/<ticket>/playwright/<flow-name>/
  <flow-name>.flow.ts
  screenshots/
```

**Running a flow:**

```bash
# Basic run
npx playwright test --config .claude/skills/navigate/playwright.config.ts <path>

# With a specific role
FLOW_ROLE=partner FLOW_APP=myapp npx playwright test <path>
```

**Promotion path:** When an exploratory flow proves valuable, promote it to a committed E2E test in `e2e/`.


## 4. `/dc:record` — Video Evidence

Captures Retina-quality MP4/GIF recordings of browser flows for PR evidence.

**When:** You need visual proof of a feature working — for PRs, demos, or documentation.

**Usage:**

```
/dc:record record me creating a new site
/dc:record capture the login flow as a GIF
```

**How it works (not Playwright's built-in `recordVideo`):**

- Uses CDP `Page.startScreencast` for native Retina PNG frames (2880x1800).
- Red-dot cursor overlay so viewers see where clicks happen.
- Wall-clock timestamps for correct playback speed.
- ffmpeg stitching with `-tune animation` for sharp text.

**Output:**

```
.agents.tmp/recordings/20260323-ffa-475-site-creation.mp4   (~60-200 KB)
.agents.tmp/recordings/20260323-ffa-475-site-creation.gif   (~80-150 KB, with --gif)
```

Both formats render inline on GitHub PRs.


## 5. `playwright-healer` (Agent)

Automated debugger that fixes failing Playwright tests or navigate flows.

**When:** A flow or test fails and you want automated diagnosis + fix.

**Workflow:** Run test → classify failure (selector / timing / auth / navigation / data) → edit code → re-run → repeat until green.

Invoked automatically by the navigate skill's HEAL phase, or manually when tests break.


## Typical Workflow Example

```
# 1. Set up credentials (one-time)
/dc:op   → create .agents.local/login/my-app-admin.env

# 2. Authenticate
/dc:browser-login   → log in as admin on my-app

# 3. Explore
/dc:navigate   → "verify the dashboard loads and shows 3 cards"

# 4. Record evidence for PR
/dc:record   → "record the dashboard loading flow"
```


## Banned Patterns (All Skills)

| Never | Instead |
|-------|---------|
| `waitForTimeout` in tests | `expect(locator).toBeVisible()` or `waitForResponse` |
| `waitForLoadState('networkidle')` | Wait for specific elements or API responses |
| `op read` or `op inject` | `op run --env-file=...` |
| Read `.agents.tmp/.auth/*.json` | `fs.existsSync()` to check existence only |
| Commit `.agents.tmp/` files | Keep gitignored; promote proven flows to `e2e/` |


## Architecture Notes

**storageState bridge:**
The connection between `browser-login` and `navigate` is a storageState JSON file.
`browser-login` exports cookies/localStorage from a persistent `playwright-cli` session.
`navigate` flow files consume it via the `FLOW_ROLE` env var.
Limitation: storageState does NOT include IndexedDB or SessionStorage — apps using MSAL/Auth0 SPA tokens in IndexedDB need persistent sessions instead.

**CDP screencast vs recordVideo:**
Playwright's built-in `recordVideo` hardcodes VP8 at 1Mbps with no API to change it.
CDP `Page.startScreencast` gives raw PNG frames at native resolution, enabling Retina-quality output.

**Three-tier login fallback:**
Full automation → manual-once-then-reuse → guided setup.
You're never blocked — there's always a way to authenticate.
