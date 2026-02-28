---
name: dictionary-service-awareness
description: >
  Use when working with Dictionary Service API: translation key imports, env migrations, auth setup, or endpoint contracts.
  Use when checking safe write patterns, banned operations, or DS URL for Akelius Angular apps.
  Triggers: DS API, PATCH translations, migration-diff, DS_WRITE_TOKEN, 401 Unauthorized.
---

# Dictionary Service — API Awareness

## Service URL

```
https://dictionary-service.akelius.com
```

(Not the APIM gateway URL in the OpenAPI spec — FFA calls the live DS directly.)

## Environment Model

DS uses logical namespaces for the same application, not separate deployments:

| Env | Purpose |
|-----|---------|
| `dev` | Safe draft zone — all automated writes go here |
| `test` | QA environment |
| `stage` | Pre-production |
| `prod` | **Live for all end users** — never write directly |

FFA applications in all deployed environments (test, stage, prod) **all read from DS `prod`**.

## Endpoint Contracts

### Read (no auth required)
```
GET /api/v3/applications/{appId}/env/{env}/translations
→ { [key: string]: { [lnCode: string]: string } }
```
Fetch all keys for an app+env. Public endpoint. Used by `collect.ts`.

```
GET /api/v3/applications/{appId}/env/{env}/translations/ln/{lnCode}
→ { [key: string]: string }
```
Fetch all keys for a single language. Also public. Used by `npm run i18n:download-fallback`.

### Write (auth required)
```
PATCH /api/v3/applications/{appId}/env/{env}/translations/{key}
Body: { "translation": { "en": "...", "sv": "..." }, "data": {} }
```
Upsert a single key. Safe — adds/updates only, never deletes.

```
PATCH /api/v3/applications/{appId}/env/{env}/translations/transfer
Body: CSV content (text/plain or application/csv)
```
Bulk upsert from CSV. Safe — adds/updates only, never deletes.

### Migration
```
PATCH /api/v3/applications/{appId}/env/{fromEnv}/migration-diff
Body: { "targetEnv": "prod", "keys": ["key1", "key2"] }
→ { newTranslations: {...}, updatedTranslations: { old: {...}, new: {...} }, lnCodes: [...] }
```
Preview only — no changes applied.

```
PATCH /api/v3/applications/{appId}/env/{fromEnv}/migrate
Body: { "targetEnv": "prod", "migrateApplicationSettings": false, "keys": ["key1"] }
```
Selective migration of specific keys. Use PATCH (not PUT) and always pass `keys`.

## Banned Operations

| Operation | Why banned |
|-----------|-----------|
| `PUT /translations/transfer` | Replaces ALL keys in an env — no undo |
| Writing directly to `prod` | Live for all end users; one bad call blanks all UI text |
| Migrating without diff preview | Developer must see what changes before confirming |
| Accepting `appId` as a parameter | APIM key grants write access to ALL Akelius apps |

## Auth

**Mechanism:** Bearer JWT (Auth0), ~24h expiry.

**How to get a token:**
1. Open `https://dictionary-service.akelius.com` and log in
2. DevTools → Network tab → click any API request → copy the `Authorization` header value
3. `export DS_WRITE_TOKEN="<value>"`

**Storage rules:**
- Acceptable: `export DS_WRITE_TOKEN="..."` in the current terminal session only
- Never: add to `~/.zshrc` (expires in 24h, would contain stale creds)
- Never: pass as a CLI argument (appears in `ps aux`)
- Script access: `process.env['DS_WRITE_TOKEN']` — never string-interpolated

**401 Unauthorized:** Token expired. Get a fresh one from DS web UI DevTools.

## Safe Write Pattern (always follow)

```
1. Write to DS dev  (PATCH — upsert-only)
2. Preview diff     (PATCH /migration-diff — read-only)
3. Confirm with developer (type "yes" to proceed)
4. Migrate dev → prod  (PATCH /migrate with explicit keys array)
5. Verify gap is closed (GET /translations — collect.ts)
```

## CSV Format (Akelius standard)

Each app configures its own supported languages. The CSV header must match exactly.

```csv
"key";"lang1";"lang2";"lang3"
"some.key";"value in lang1";"value in lang2";"value in lang3"
```

- Separator: `;` (semicolon)
- All fields: double-quoted
- Internal double quotes: escaped by doubling (`""`)
- Multiline values: literal newlines inside the double-quoted field (valid CSV)

App-specific locale columns (e.g. FFA's `en;en-CA;en_UK;sv`) are defined per-app.

## Scripts

| Script | Auth | Purpose |
|--------|------|---------|
| `../ds-sync-keys/scripts/collect.ts` | None | Gap detection + CSV generation |
| `../ds-sync-keys/scripts/client.ts` | `DS_WRITE_TOKEN` | Typed write API (pushKey, importCsv, migrateEnv) |

Scripts are bundled in the `ds-sync-keys` sibling skill.
