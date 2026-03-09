---
name: op
description: 'Use when working with 1Password CLI - injecting secrets into apps, managing vault items, or setting up shell plugins for biometric auth. Triggers: "1password", "op run", "secrets", "vault", "biometric auth", "inject secrets", "environment variables", "secure credentials", ".env setup".'
allowed-tools: Bash(op run:*), Bash(op vault:*), Bash(op item:*), Bash(op plugin:*), Bash(op whoami:*), Bash(op account:*)
---

# 1Password CLI

Secure 1Password CLI operations following 1Password's own AI security principles.

This skill enforces the security model described in 1Password's [Security Principles for AI](https://1password.com/blog/security-principles-guiding-1passwords-approach-to-ai), validated by the [SCAM benchmark](https://github.com/1Password/SCAM), and aligned with [OWASP ASI03 — Identity & Privilege Abuse](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).

**Announce at start:** "Using 1Password CLI with security-first patterns."

## Security Hard Gates

These rules are non-negotiable.

Violating any of them means secrets enter the LLM context and are compromised.

> **HARD GATE: NEVER use `op read`.**
>
> It prints secret values to stdout, which enters the conversation context.

> **HARD GATE: NEVER use `op inject`.**
>
> It writes plaintext secrets to files, which could then be read into the conversation context.

> **HARD GATE: NEVER pass secret values as command-line arguments.**
>
> Command-line arguments are visible in process listings and shell history.

> **HARD GATE: NEVER log, echo, or print secret values.**
>
> Any output containing secrets will be captured by the conversation.

> **HARD GATE: NEVER include raw credentials in prompts, code comments, or generated code.**
>
> Use `op://` reference URIs as placeholders instead.

> **HARD GATE: NEVER read files that might contain resolved/plaintext secrets.**
>
> Only read template files containing `op://` references.

> **HARD GATE: ALWAYS ask user confirmation before ANY `op` command.**
>
> Every `op` command triggers biometric approval — the user must consent first.

> **HARD GATE: ONLY use `op run` for secret resolution.**
>
> `op run` injects secrets as env vars into a subprocess, masks them on stdout, and clears them on exit.

### Why `op run` Is the Only Safe Pattern

| Method | What happens | Risk |
|--------|-------------|------|
| `op read` | Prints secret to stdout | Secret enters LLM context — **compromised** |
| `op inject` | Writes plaintext to file | File can be read into LLM context — **compromised** |
| `op run` | Injects as env vars into subprocess | Masked on stdout, cleared on exit — **safe** |

1Password explicitly states: "Raw credentials have no place in prompts, embeddings, or fine-tuning data."

## Quick Reference — Safe Patterns

### Secret injection into apps (the primary pattern)

```bash
# Set op:// references as env vars, then run your app
export DB_PASSWORD="op://vault/db/password"
op run -- node server.js

# Or use an .env file with op:// references (safe to commit)
op run --env-file=.env -- npm start
```

### Securing MCP server configs

```bash
# .env with op:// references (safe to commit)
GITHUB_TOKEN=op://AI/GitHub/token
op run --env-file=.env -- mcp-server start
```

### Item browsing (metadata only, no secret values)

```bash
op item list --vault Production
op vault list
```

### Shell plugin setup

```bash
op plugin init gh      # GitHub CLI
op plugin init aws     # AWS CLI
op plugin list         # List available plugins
op plugin inspect      # Check current configuration
```

## Process

### A. Injecting secrets into a running process

1. Identify which secrets the process needs.

2. Help user create an `.env` file with `op://` references (safe to commit).

   See `references/env-template.example` for the pattern.

3. Show the `op run --env-file=.env -- <command>` pattern.

4. Confirm with user before executing — biometric prompt will appear.

### B. Managing items (metadata only)

1. Use `op item list` / `op vault list` for browsing.

2. Use `op item create` with `--generate-password` for new items.

3. **NEVER** use `op item get` to display secret field values in conversation.

### C. Setting up shell plugins

1. Check available plugins with `op plugin list`.

2. Initialize with `op plugin init <cli-name>`.

3. Follow the interactive setup — 1Password will prompt for vault/item selection.

4. Verify with `op plugin inspect`.

## 1Password's 7 Security Principles for AI

These principles explain WHY the hard gates exist.

They come directly from [1Password's official position](https://1password.com/blog/security-principles-guiding-1passwords-approach-to-ai).

1. **Secrets Stay Secret** — Zero-knowledge architecture.

   AI should never see, store, or transmit raw credentials.

2. **Authorization Must Be Deterministic** — LLMs are not auth engines.

   Biometric approval (not AI judgment) gates every secret access.

3. **Raw Credentials Should Never Enter LLM Context** — The core rule.

   This is why `op read` and `op inject` are banned — both create paths for secrets to reach the LLM.

4. **Auditability Must Be Taken Into Account** — Every access is logged.

   `op run` creates auditable records in 1Password's activity log.

5. **Show What AI Can See — and What It Can't** — Transparency.

   The user always knows which secrets are being accessed and by which process.

6. **Least Privilege and Minimum Exposure by Default** — Minimal scope.

   Only inject the secrets the subprocess actually needs.

7. **Security and Usability Are Co-Requirements** — No security theater.

   `op run` is both the most secure AND the most ergonomic pattern.

## Common Mistakes

| Don't | Do |
|-------|-----|
| `op read op://vault/item/password` | `op run --env-file=.env -- command` |
| `op inject -i tpl -o config.yml` | `op run --env-file=.env -- command` |
| Pass secrets as CLI args | Use `op://` references in env vars |
| Skip user confirmation for `op` commands | Always ask — biometric approval required |
| Use `op item get` to show secret fields | Use `op item list` for metadata only |
| Hardcode credentials in generated code | Use `op://` reference URIs as placeholders |
| Read files that might contain resolved secrets | Only read template files with `op://` references |
