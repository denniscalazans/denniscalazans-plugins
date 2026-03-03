# Figma REST API Endpoint Reference

Base URL: `https://api.figma.com`

Authentication: `X-Figma-Token: <personal-access-token>` header

## URL Parsing

Extract file key and node ID from Figma URLs:

```
https://www.figma.com/design/:fileKey/:fileName?node-id=:nodeId
```

Node IDs use hyphens in URLs (e.g., `1-3`) but colons in API calls (e.g., `1:3`).

URL-encode colons as `%3A` in query parameters.

## Files

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key` | 1 | Full file as JSON document tree |
| GET | `/v1/files/:file_key/nodes?ids=:id1,:id2` | 1 | Specific nodes with subtrees |
| GET | `/v1/files/:file_key/meta` | 3 | File metadata only (name, thumbnail, permissions) |

### GET File Query Params

- `version` — specific version ID
- `ids` — comma-separated node IDs to include
- `depth` — how deep to traverse (use to limit response size)
- `geometry` — include vector path data (`paths`)
- `plugin_data` — include plugin data for specified plugin IDs
- `branch_data` — include branch metadata (`true`)

### GET Nodes Query Params

- `ids` (required) — comma-separated node IDs
- `version`, `depth`, `geometry`, `plugin_data` — same as GET File

## Images

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/images/:file_key` | 1 | Render nodes as images |
| GET | `/v1/files/:file_key/images` | 2 | Download URLs for all image fills |

### GET Images Query Params

- `ids` (required) — comma-separated node IDs to render
- `scale` — 0.01 to 4 (default 1)
- `format` — `jpg`, `png`, `svg`, `pdf` (default `png`)
- `svg_outline_text` — outline text in SVGs (default `true`)
- `svg_include_id` — include node IDs in SVG output
- `svg_simplify_stroke` — simplify inner/outer strokes
- `contents_only` — clip to node bounds, skip background (default `true`)
- `use_absolute_bounds` — use full dimensions including strokes
- `version` — specific file version

Image URLs expire after 30 days.

Image fills URLs expire after 14 days.

Max export size: 32 megapixels (larger images are scaled down).

## Comments

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key/comments` | 2 | List all comments |
| POST | `/v1/files/:file_key/comments` | 3 | Post a new comment |
| DELETE | `/v1/files/:file_key/comments/:comment_id` | 3 | Delete a comment |

### POST Comment Body

```json
{
  "message": "Comment text",
  "comment_id": "optional-parent-id-for-reply",
  "client_meta": { "x": 100, "y": 200 }
}
```

## Version History

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key/versions` | 3 | List version history |

Paginated — use `pagination.next_page` URL for older versions.

## Projects

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/teams/:team_id/projects` | 2 | List team projects |
| GET | `/v1/projects/:project_id/files` | 2 | List project files |

## Components & Styles (Published Team Library)

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key/components` | 2 | File components |
| GET | `/v1/files/:file_key/styles` | 2 | File styles |
| GET | `/v1/teams/:team_id/components` | 2 | Published team components |
| GET | `/v1/teams/:team_id/styles` | 2 | Published team styles |
| GET | `/v1/teams/:team_id/component_sets` | 2 | Published component sets |
| GET | `/v1/components/:key` | 2 | Single component by key |
| GET | `/v1/styles/:key` | 2 | Single style by key |

Supports pagination with `page_size` (max 1000) and cursor.

## Variables (Enterprise Only)

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key/variables/local` | 1 | Local variables and collections |
| GET | `/v1/files/:file_key/variables/published` | 1 | Published variables |
| POST | `/v1/files/:file_key/variables` | 1 | Create/update/delete variables |

Requires `file_variables:read` / `file_variables:write` scopes.

Requires a Full seat in an Enterprise org.

## Dev Resources

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/files/:file_key/dev_resources` | 2 | Get dev resources attached to nodes |
| POST | `/v1/files/:file_key/dev_resources` | 3 | Create dev resources |
| PUT | `/v1/dev_resources/:id` | 3 | Update a dev resource |
| DELETE | `/v1/dev_resources/:id` | 3 | Delete a dev resource |

## Users

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v1/me` | 3 | Authenticated user info |

## Webhooks (v2)

| Method | Path | Tier | Description |
|--------|------|------|-------------|
| GET | `/v2/webhooks/:webhook_id` | 3 | Get a webhook |
| POST | `/v2/webhooks` | 3 | Create a webhook |
| PUT | `/v2/webhooks/:webhook_id` | 3 | Update a webhook |
| DELETE | `/v2/webhooks/:webhook_id` | 3 | Delete a webhook |
| GET | `/v2/webhooks/:webhook_id/requests` | 3 | Webhook request history |
| GET | `/v2/teams/:team_id/webhooks` | 3 | List team webhooks |

Note: webhooks use `/v2/` prefix.

## Rate Limits

Leaky bucket algorithm.

429 responses include `Retry-After` (seconds) header.

| Tier | Starter | Pro | Org/Enterprise |
|------|---------|-----|----------------|
| 1 | 10/min | 15/min | 20/min |
| 2 | 25/min | 50/min | 100/min |
| 3 | 50/min | 100/min | 150/min |

Best practices:
- Batch node requests using `?ids=` instead of individual calls
- Use `?depth=` to limit response size
- Cache responses
- Respect `Retry-After` on 429 errors
- Use webhooks instead of polling

## Node Types

DOCUMENT, CANVAS, FRAME, GROUP, SECTION, COMPONENT, COMPONENT_SET, INSTANCE, VECTOR, BOOLEAN_OPERATION, STAR, LINE, ELLIPSE, POLYGON, RECTANGLE, TEXT, SLICE, TABLE, TABLE_CELL, STICKY, SHAPE_WITH_TEXT, CONNECTOR, EMBED, LINK_UNFURL, WIDGET, CODE_BLOCK, STAMP, HIGHLIGHT, WASHI_TAPE, MEDIA, SLIDE, TRANSFORM_GROUP, TEXT_PATH

## Document Tree Hierarchy

```
DOCUMENT (root)
  +-- CANVAS (page)
       +-- FRAME, GROUP, SECTION, COMPONENT, ...
            +-- child nodes (TEXT, RECTANGLE, INSTANCE, ...)
```
