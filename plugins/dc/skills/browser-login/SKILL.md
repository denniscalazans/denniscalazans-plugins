---
name: browser-login
description: >
  Use when the user needs to authenticate into a web app, open a persistent browser session, log in as a
  specific role, switch between users, or manage named browser sessions via playwright-cli and 1Password.
  Handles automated login, session reuse, parallel multi-role login, and already-authenticated detection.
  Triggers: "login", "browser session", "authenticate", "playwright-cli", "persistent session", "op run",
  "log in as", "switch user", "open app".
---

# Browser Login with playwright-cli + 1Password

Manage persistent named browser sessions for authenticated web applications.

Credentials are managed by 1Password CLI and **never appear in conversation output**.

> **SECURITY:** Never construct `playwright-cli fill` commands with credential values directly.
> Always use the bundled login script which suppresses credential output.


## Three-Tier Login Process

### Tier 1 — Automated (bundled script)

Full automation: opens browser, finds login form, fills credentials, submits.

```bash
SCRIPTS_DIR="${CLAUDE_SKILL_DIR}/scripts"
op run --env-file=".agents.local/login/<app>-<role>.env" -- "$SCRIPTS_DIR/login.sh" <app> <role> <url>
```


### Tier 2 — Manual login + session reuse

When Tier 1 cannot find the login form, or for first-time setup:

```bash
# Open a persistent browser session
playwright-cli -s=<app>-<role> open --headed --persistent <url>
# Log in manually in the browser
# All subsequent opens reuse the authenticated session
```


### Tier 3 — Guided setup

For new projects: create the per-repo configuration files described below, then use Tier 1 or 2.


## Prerequisites

- `@playwright/cli` — install globally with `npm install -g @playwright/cli`
- `op` CLI — 1Password command-line tool for credential injection
- The `dc:op` skill for understanding 1Password security patterns


## Session Lifecycle

### Open a persistent session

```bash
playwright-cli -s=my-app-admin open --headed --persistent http://localhost:4200
```

### List active sessions

```bash
playwright-cli list
```

### Close a session

```bash
playwright-cli -s=my-app-admin close
```

### Close all sessions

```bash
playwright-cli close-all
```


## Per-Repo Configuration

Each project stores its login configuration in `.agents.local/` (gitignored, developer-local).

### `.agents.local/login/config.json`

```json
{
  "app_name": "my-app",
  "app_url": "http://localhost:4200",
  "roles": [
    { "name": "admin", "description": "Full access administrator" },
    { "name": "editor", "description": "Content editor with limited access" },
    { "name": "viewer", "description": "Read-only access" }
  ]
}
```

This file is optional — the login script takes app name, role, and URL as CLI arguments.

The config serves as a reference for available roles in the project.

### `.agents.local/login/<app>-<role>.env`

1Password `op://` vault path references (not plaintext credentials).

```env
LOGIN_USER="op://Vault/My App Admin/username"
LOGIN_PASS="op://Vault/My App Admin/password"
```

Store credentials in 1Password; the `.env` file contains vault paths, never plaintext.


## Credential Flow (Security Model)

1. `.env` profile files contain `op://` references — vault paths, NOT real credentials
2. `op run` resolves references via 1Password (biometric auth on macOS)
3. Credentials exist only in the `op run` child process environment (memory)
4. The login script fills the form with output suppressed (`> /dev/null 2>&1`)
5. Post-fill snapshots (which could contain filled values) are discarded
6. The conversation only sees: session name, app URL, and "Logged in" confirmation
7. `--persistent` saves the browser profile so subsequent opens skip login entirely


## Already-Authenticated Detection

The login script checks the current page URL to determine authentication state.

If the URL is an app URL (not an identity provider URL), the session is already authenticated.

The script exits immediately with: `"Already authenticated as <role> on <app>."` (exit code 0).


## Login Page Discovery

The login script handles three scenarios when the app URL does not land directly on a login form:

1. **Auto-detect login link** — Scans the page snapshot for buttons/links containing "Login", "Sign in", etc., and clicks the first match.

2. **Interactive prompt** — If no login link is found automatically:
   - `[w]` Wait — navigate to the login page manually, then press Enter
   - `[r]` Retry — re-scan the current page for a login form
   - `[a]` Abort — exit without logging in, leaving the session open

3. **Already authenticated** — If a persistent session is still valid, the script detects this and exits cleanly.

> When running via Claude Code, the script is interactive.
> If the script prompts for input (`[w/r/a]`), tell the user what is happening and let them interact with the terminal.


## Parallel Login

Open multiple role sessions for the same app simultaneously:

```bash
SCRIPTS_DIR="${CLAUDE_SKILL_DIR}/scripts"
"$SCRIPTS_DIR/parallel-login.sh" my-app http://localhost:4200 admin editor viewer
```

### How it works

1. Validates all role profiles exist upfront (fails fast if any missing)
2. Launches `op run ... login.sh` in the background for each role
3. Waits for all logins to complete
4. Prints a summary table showing success/failure per role
5. Cleans up temp logs on full success; preserves them on failure for debugging

### Biometric prompts

1Password serializes biometric authentication — one biometric prompt per role, appearing sequentially.

This is expected behavior; approve each prompt as it appears.

### Re-running (idempotent)

If some or all roles are already authenticated, the login script detects this per-session and exits immediately.

This makes `parallel-login.sh` safe to re-run.


## Integration with Other Skills

- **dc:op** — credential security patterns (never `op read`, always `op run`)
- **dc:record** — pre-authenticate before recording browser flows
- **dc:navigate** — persistent sessions for exploratory flow files (if installed)

For a full overview of how these skills connect, see `dc/references/browser-pipeline-guide.md`.


## Troubleshooting

### "No login form found" (interactive prompt appears)

The script tries to find and click a login link automatically.

If that fails, it prompts you to navigate manually or abort.

Common reasons:
- The app has a landing page before the login (click through manually)
- The app uses a custom login flow that does not match standard patterns
- The session is already authenticated (choose `a` to abort and use the session)

### Session expired

Re-run the `op run` login command to re-authenticate.

### 1Password prompts for auth

Normal — biometric or master password is required to release secrets.

### Parallel login: one role fails

Check the preserved log file shown in the summary output.

Re-run `parallel-login.sh` — already-authenticated roles will skip instantly.
