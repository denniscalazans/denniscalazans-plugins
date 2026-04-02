---
name: login
description: >
  Use when the user needs to authenticate into a web app using agent-browser and 1Password,
  open a persistent browser session, log in as a specific role, switch between users, or manage
  named agent-browser sessions.
  Handles automated login via snapshot+refs discovery, session reuse, parallel multi-role login,
  and already-authenticated detection.
  Handles form-based login including Auth0 and Angular Material via agent-browser's fill command.
  Triggers: "login", "browser session", "authenticate", "agent-browser", "persistent session",
  "op run", "log in as", "switch user", "open app", "browser login".
---

# Login — agent-browser + 1Password

Authenticate into web apps using agent-browser's persistent Chrome daemon and 1Password CLI.

Credentials are managed by 1Password CLI and **never appear in conversation output**.

> **SECURITY:** Never construct `agent-browser fill` commands with credential values directly.
> Always use `op run` which injects credentials as environment variables in a subprocess.


## Quick Start

```
/browser:login as ffa-manager on http://localhost:4488
/browser:login to https://staging.example.com as admin
/browser:login — open all roles for ffa
```


## Prerequisites

- `agent-browser` — install globally with `npm i -g agent-browser` (or use `npx agent-browser`)
- `op` CLI — 1Password command-line tool for credential injection
- Per-repo login configuration in `.agents.local/login/` (see below)


## Login Workflow

### Step 1: Open the app

```bash
agent-browser --session <app>-<role> open <url>
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Use `--session <app>-<role>` to create a named persistent session (e.g., `--session ffa-manager`).

### Step 2: Discover the login form

Read the `snapshot -i` output to identify interactive elements.
Look for textbox fields (email/username, password) and a submit button.

If the page shows a landing page instead of a login form:
1. Look for a "Login" / "Sign in" button in the snapshot and click it
2. Re-snapshot after navigation to find the form
3. If no form found, tell the user to navigate manually in the browser

### Step 3: Fill credentials and submit

```bash
op run --env-file=".agents.local/login/<app>-<role>.env" -- sh -c \
  'agent-browser fill @<email-ref> "$AUTH0_USER" && agent-browser fill @<pass-ref> "$AUTH0_PASS" && agent-browser click @<submit-ref>'
```

The `op run` wrapper:
1. Reads `op://` vault references from the `.env` file
2. Resolves them via 1Password (biometric auth on macOS)
3. Injects as environment variables into the subprocess
4. The subprocess runs `agent-browser fill` commands
5. Credentials exist only in memory, never in conversation output

### Step 4: Verify authentication

```bash
agent-browser wait --text "Dashboard" || agent-browser wait --load networkidle
agent-browser get url
```

Prefer `wait --text` with a known post-login indicator (e.g., "Dashboard", "Welcome") over `wait --load networkidle`.
If the URL is on the app domain (not an auth provider URL), login succeeded.

If verification times out, check `agent-browser dialog status` — auth flows sometimes trigger JS dialogs that block all commands.

### Already-authenticated detection

Before filling credentials, check if the session is already authenticated:
1. Get the current URL with `agent-browser get url`
2. If the URL is on the app domain and NOT a login/auth/SSO page, the session is still valid
3. Report "Already authenticated as <role> on <app>" and skip login


## Per-Repo Configuration

Each project stores login configuration in `.agents.local/` (gitignored, developer-local).

### `.agents.local/login/config.json` (optional)

```json
{
  "app_name": "ffa",
  "app_url": "http://localhost:4488",
  "roles": [
    { "name": "manager", "description": "FFA Manager — full access" },
    { "name": "partner", "description": "Partner — limited access" },
    { "name": "auditor", "description": "Auditor — read-only" }
  ]
}
```

### `.agents.local/login/<app>-<role>.env`

1Password `op://` vault path references (not plaintext credentials).

```env
AUTH0_USER="op://Development/FFA Manager/username"
AUTH0_PASS="op://Development/FFA Manager/password"
```


## Credential Flow (Security Model)

1. `.env` files contain `op://` references — vault paths, NOT real credentials
2. `op run` resolves references via 1Password (biometric auth on macOS)
3. Credentials exist only in the `op run` child process environment
4. `agent-browser fill` uses CDP `Input.insertText` — value goes directly to the input element
5. The conversation only sees: session name, app URL, and success/failure confirmation
6. Named sessions persist across commands — subsequent `agent-browser` calls reuse the session


## Parallel Login

Open multiple role sessions simultaneously:

```bash
SCRIPTS_DIR="${CLAUDE_SKILL_DIR}/scripts"
"$SCRIPTS_DIR/parallel-login.sh" <app> <url> <role1> [role2] [role3] ...
```

### How it works

1. Validates all role profiles exist in `.agents.local/login/` (fails fast if any missing)
2. Launches `agent-browser --session <app>-<role> open <url>` in background for each role
3. Runs `op run ... agent-browser fill` for each role
4. Waits for all logins to complete
5. Prints a summary table showing success/failure per role

### Biometric prompts

1Password serializes biometric authentication — one prompt per role, appearing sequentially.
This is expected behavior; approve each prompt as it appears.


## Session Management

### List sessions

```bash
agent-browser session list
```

### Close a session

```bash
agent-browser --session <app>-<role> close
```

### Close all sessions

```bash
agent-browser close --all
```


## Integration with Other Skills

- **browser:explore** — uses the same agent-browser session for page inspection, flow generation, and recording
- **integrations:op** — 1Password security patterns (never `op read`, always `op run`)


## Common Mistakes

| Do NOT | Do instead |
|--------|-----------|
| Run `agent-browser fill @ref "actual-password"` with plaintext | Always wrap with `op run --env-file` |
| Use `playwright-cli` for sessions | Use `agent-browser --session` instead |
| Read or print `.agents.local/login/*.env` contents | These contain `op://` refs but treat as sensitive |
| Assume the login form is immediately visible | Snapshot first; the app may have a landing page |
| Use `agent-browser type` for auth forms | Use `agent-browser fill` — it bypasses JS listeners |
| Skip `--session` flag | Always name sessions for reusability: `--session <app>-<role>` |
| Use `wait 3000` after login submission | Use `wait --text "Dashboard"` or `wait --url "**/dashboard"` for reliable verification |
| Ignore timeouts during login | Check `agent-browser dialog status` — auth dialogs block all commands silently |
