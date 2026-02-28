---
name: login
description: Securely log into Auth0-protected apps using playwright-cli with 1Password CLI. Use when the user asks to open/load an app that requires authentication, log in as a specific role, or manage browser sessions for different users.
allowed-tools: Bash(playwright-cli:*), Bash(op run:*)
---

# Auth0 Login with playwright-cli + 1Password

Securely authenticate into Auth0-protected applications using named persistent browser sessions. Credentials are managed by 1Password CLI and **never appear in conversation output**.

> **SECURITY:** Never construct `playwright-cli fill` commands with credential values directly. Always use the login script which suppresses credential output.

## Quick Reference

### First-time login (or expired session)

```bash
op run --env-file="$HOME/.auth0/profiles/<app>-<role>.env" -- ~/.auth0/login.sh <app> <role>
```

### Reuse existing session (already logged in)

```bash
playwright-cli -s=<app>-<role> open --headed --persistent <url>
```

### List active sessions

```bash
playwright-cli list
```

## Available Apps and Roles

Check `~/.auth0/apps.conf` for registered apps and `~/.auth0/profiles/` for available role profiles.

Common profiles:
- `ffa-manager` — Forest Flow as Forest-Activities-Manager
- `ffa-partner` — Forest Flow as Forest-Activities-Partner
- `ffa-auditor` — Forest Flow as Forest-Activities-Auditor

## Examples

### Open Forest Flow as Manager

```bash
# If not yet logged in:
op run --env-file="$HOME/.auth0/profiles/ffa-manager.env" -- ~/.auth0/login.sh ffa manager

# If already logged in (persistent session):
playwright-cli -s=ffa-manager open --headed --persistent https://localhost:4488
```

### Switch between roles

```bash
# Open both — each has isolated cookies and storage
playwright-cli -s=ffa-manager open --headed --persistent https://localhost:4488
playwright-cli -s=ffa-partner open --headed --persistent https://localhost:4488

# Interact with a specific session
playwright-cli -s=ffa-manager snapshot
playwright-cli -s=ffa-partner snapshot
```

### Check if a session is still authenticated

```bash
playwright-cli -s=ffa-manager snapshot
# Look at the page URL/title — if it's the app dashboard, you're logged in.
# If it's the Auth0 login page, re-run the login command.
```

### Close sessions

```bash
# Close one
playwright-cli -s=ffa-manager close

# Close all
playwright-cli close-all
```

## Parallel Login

Open multiple role sessions for the same app simultaneously using `parallel-login.sh`:

```bash
~/.auth0/parallel-login.sh <app> <role1> [role2] [role3] ...
```

### Examples

```bash
# Open Forest Flow as both manager and partner
~/.auth0/parallel-login.sh ffa manager partner

# All three roles
~/.auth0/parallel-login.sh ffa manager partner auditor
```

### How it works

1. Validates all role profiles exist upfront (fails fast if any missing)
2. Launches `op run ... login.sh` in the background for each role
3. Waits for all logins to complete
4. Prints a summary table showing success/failure per role
5. Cleans up temp logs on full success; preserves them on failure for debugging

### Biometric prompts

1Password serializes biometric authentication — you'll get one Touch ID prompt per role, appearing sequentially. This is expected behavior; approve each prompt as it appears.

### Re-running (idempotent)

If some or all roles are already authenticated, `login.sh` detects this per-session and exits immediately with `"Already authenticated"`. This makes `parallel-login.sh` safe to re-run.

## Adding a New App

1. Add the app URL to `~/.auth0/apps.conf`:
   ```
   new-app=https://localhost:5000
   ```

2. Create a profile in `~/.auth0/profiles/new-app-<role>.env`:
   ```
   AUTH0_USER="op://Development/NewApp Role/username"
   AUTH0_PASS="op://Development/NewApp Role/password"
   ```

3. Store the actual credentials in your 1Password vault under the matching path.

4. Login:
   ```bash
   op run --env-file="$HOME/.auth0/profiles/new-app-<role>.env" -- ~/.auth0/login.sh new-app <role>
   ```

## Login Page Discovery

The login script handles three scenarios when the app URL doesn't land directly on an Auth0 login form:

1. **Auto-detect login link** — Scans the page snapshot for buttons/links containing "Login", "Sign in", etc., and clicks the first match. Waits for the Auth0 login form to appear.

2. **Interactive prompt** — If no login link is found automatically, the script prompts with:
   - `[w]` Wait — lets you navigate to the login page manually in the browser, then press Enter to continue
   - `[r]` Retry — re-scans the current page for a login form
   - `[a]` Abort — exits without logging in, leaving the session open

3. **Already authenticated** — If the app loads a dashboard directly (persistent session still valid), the script detects this automatically and exits with: `"Already authenticated as <role> on <app>."` No credentials are filled and exit code is 0.

> **Note:** When running via Claude Code, the script is interactive. If the script prompts for input (`[w/r/a]`), tell the user what's happening and let them interact with the terminal or navigate the browser as needed.

## How It Works (Security Model)

1. `.env` profile files contain `op://` references — vault paths, NOT real credentials
2. `op run` resolves references via 1Password (biometric auth on macOS)
3. Credentials exist only in the `op run` child process environment (memory)
4. `login.sh` fills the login form with output suppressed (`> /dev/null 2>&1`)
5. Post-fill snapshots (which could contain filled values) are discarded
6. The conversation only sees: session name, app URL, and "Logged in" confirmation
7. `--persistent` saves the browser profile so subsequent opens skip login entirely

## Troubleshooting

### "No login form found" (interactive prompt appears)
The script will first try to find and click a login link automatically. If that fails, it prompts you to navigate manually or abort. Common reasons:
- The app has a landing page before the login (click through manually)
- The app uses a custom login flow that doesn't match Auth0 patterns
- The session is already authenticated (choose `a` to abort and just use the session)

### Auth0 session expired
Re-run the `op run` login command to re-authenticate.

### Wrong element refs detected
Auth0 login pages vary by tenant config. If the script can't find the form fields:
1. When prompted, choose `w` to wait
2. Navigate to the login page manually in the browser
3. Press Enter to let the script re-scan and fill credentials

### 1Password prompts for auth
Normal — Touch ID or master password is required to release secrets. This is the security feature, not a bug.

### Parallel login: multiple Touch ID prompts
When using `parallel-login.sh`, 1Password serializes biometric prompts — you'll see one Touch ID dialog per role, appearing one after another. Approve each prompt as it appears. The logins still run in parallel; only the biometric step is sequential.

### Parallel login: one role fails
Check the preserved log file shown in the summary output. Common causes:
- Session was on the Auth0 page (expired) and the script couldn't find the form
- 1Password prompt was dismissed or timed out
Re-run `parallel-login.sh` — already-authenticated roles will skip instantly.
