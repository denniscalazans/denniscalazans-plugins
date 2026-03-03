---
name: figma-api
description: >
  Use when interacting with the Figma REST API to read design files, extract components, export images,
  list projects, read variables, manage comments, or query any Figma design data programmatically.
  Also use when the user provides a Figma URL and wants to inspect its structure, extract design tokens,
  or export assets from it.
  Use this skill instead of the Figma MCP server when you need raw API access, batch operations,
  or endpoints the MCP doesn't cover (comments, versions, projects, team components, variables, dev resources).
  Triggers: "figma api", "figma file", "figma components", "figma export", "figma tokens",
  "figma variables", "design tokens from figma", "figma comments", "figma versions".
---

# Figma REST API

Query the Figma REST API securely using 1Password for token management and sub-agents for API call isolation.

## Security Model

The Figma API token lives in 1Password at `op://Development/Figma/credential`.

It is resolved at runtime via `op run` and injected as an environment variable into the curl subprocess.

The token never appears in command arguments, shell history, or LLM context.

**Rules:**
- NEVER use `op read` or `op inject` — these expose secrets to stdout or files
- ONLY use `op run` to resolve the token
- ALWAYS confirm with the user before the first `op` command in a session (biometric approval required)
- API responses stay inside the sub-agent — only extracted summaries return to the main context

## Architecture

```
Main context                    Sub-agent
+-----------+    "get file     +------------------+
|           |    components    |                  |
| Delegates |  ------------->  | 1. Runs script   |
| task with |                  | 2. Calls Figma   |
| clear     |  <-------------  | 3. Processes JSON|
| extraction|    summary +     | 4. Returns only  |
| criteria  |    key data      |    what's needed  |
+-----------+                  +------------------+
```

Every Figma API call runs inside a sub-agent (Agent tool with `subagent_type: "general-purpose"`).

This keeps potentially large JSON responses out of the main conversation context.

## Helper Script

The skill bundles `scripts/figma-api.sh` (relative to this skill directory).

It wraps curl with `op run` for secure token injection.

```bash
# Usage (from within a sub-agent):
SCRIPT="<skill-dir>/scripts/figma-api.sh"

# GET request
bash "$SCRIPT" GET /v1/me

# GET with query params
bash "$SCRIPT" GET "/v1/files/ABC123?depth=1"

# POST with JSON body
bash "$SCRIPT" POST /v1/files/ABC123/comments '{"message":"Review this"}'
```

The script handles authentication errors (401/403) and rate limiting (429) with clear error messages.

## Process

### Step 1: Parse the user's intent

Determine which Figma API endpoint(s) are needed.

If the user provides a Figma URL, extract the file key and node ID:

```
https://www.figma.com/design/:fileKey/:fileName?node-id=:nodeId
```

Convert node IDs from URL format (hyphens: `1-3`) to API format (colons: `1:3`).

Read `references/endpoints.md` (relative to this skill directory) if you need the full endpoint catalog.

### Step 2: Confirm 1Password access

Before the first API call in a session, tell the user:

> "I'll use 1Password to resolve your Figma API token. This requires biometric confirmation on your end."

Wait for user acknowledgment before proceeding.

### Step 3: Spawn a sub-agent for the API call

Launch an Agent with `subagent_type: "general-purpose"` for each API call.

Give the sub-agent a precise prompt that includes:

1. **The script path** — absolute path to `scripts/figma-api.sh`
2. **The exact API call** — method, path, and body if applicable
3. **What to extract** — be specific about what data you need from the response
4. **Output format** — tell the agent exactly what to return (e.g., "return a markdown table of component names and keys")

**Example sub-agent prompt:**

```
Run this Figma API call and extract the requested data.

Script: /path/to/scripts/figma-api.sh
Command: bash "/path/to/scripts/figma-api.sh" GET "/v1/files/ABC123?depth=1"

From the response, extract:
- File name
- Last modified date
- List of top-level pages (CANVAS nodes) with their names and IDs

Return as a concise markdown summary. Do NOT return the raw JSON.
```

**Batching:** If you need data from multiple related calls (e.g., file structure + images), spawn multiple sub-agents in parallel using a single Agent tool message with multiple invocations.

### Step 4: Present results

Take the sub-agent's extracted data and present it to the user in a clear, actionable format.

If the task requires follow-up calls (e.g., user wants to drill into a specific component), repeat step 3 with the new parameters.

## Common Workflows

### Inspect a Figma file structure

```
GET /v1/files/:fileKey?depth=2
```

Extract page names, top-level frames, and component counts.

### Export nodes as images

```
GET /v1/images/:fileKey?ids=1:3,4:5&format=png&scale=2
```

Returns URLs to rendered images (expire after 30 days).

### Extract design tokens

```
GET /v1/files/:fileKey/styles       (colors, text styles, effects)
GET /v1/files/:fileKey/variables/local  (Enterprise only)
```

### List team components

```
GET /v1/teams/:teamId/components?page_size=100
GET /v1/teams/:teamId/styles
```

### File version history

```
GET /v1/files/:fileKey/versions
```

### Manage comments

```
GET  /v1/files/:fileKey/comments
POST /v1/files/:fileKey/comments  {"message": "..."}
```

## When to Use This vs. Figma MCP

| Use this skill | Use Figma MCP |
|---|---|
| Raw API access with custom queries | Design-to-code workflow (get_design_context) |
| Batch operations across files/teams | Screenshot capture (get_screenshot) |
| Comments, versions, dev resources | FigJam boards (get_figjam) |
| Variables and design token extraction | Code Connect mappings |
| Team-level component/style queries | Quick single-node inspection |
| Webhooks management | Diagram generation |

## Common Mistakes

| Don't | Do |
|---|---|
| Run curl in main context | Always use a sub-agent |
| Use `op read` or `op inject` | Use `op run` via the helper script |
| Return raw JSON to main context | Extract only needed data in the sub-agent |
| Use hyphenated node IDs in API calls | Convert to colon format (1-3 -> 1:3) |
| Fetch full file without depth limit | Use `?depth=1` or `?depth=2` to limit response size |
| Make many individual node requests | Batch with `?ids=1:3,4:5,6:7` |
| Poll for changes | Use webhooks when possible |
| Skip user confirmation for op | Always confirm before first op run in session |
