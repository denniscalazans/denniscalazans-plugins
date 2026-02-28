# ds-sync-keys/scripts

Dictionary Service utility scripts. No `package.json` needed — run with `npx tsx`.

## Scripts

### `collect.ts` — gap detection

Reads local `en.json`/`sv.json`, fetches DS prod keys (no auth), and generates a ready-to-import CSV for any keys not yet in DS.

**Prerequisite:** Run from a project root that contains `public/i18n/en.json` and `public/i18n/sv.json`.

```bash
npx tsx ds-sync-keys/scripts/collect.ts
# Optional: custom output path
npx tsx ds-sync-keys/scripts/collect.ts --output=.dictionary-service/pending-import.csv
```

### `client.ts` — DS write API

Typed module for writing to Dictionary Service. Imported by orchestrating scripts or commands — not run directly.

> `APP_ID` is hardcoded to `"FFA"` — a personal pragmatic choice reflecting primary usage. The module can be adapted for other apps by parameterizing `appId`.

**Auth setup** (token expires ~24h):
```bash
# 1. Open https://dictionary-service.akelius.com, log in
# 2. DevTools → Network → any API request → copy Authorization header value
export DS_WRITE_TOKEN="<value>"
```

## Tests

Uses Node.js built-in `node:test` — no extra dependencies.

```bash
npx tsx ds-sync-keys/scripts/collect.spec.ts
npx tsx ds-sync-keys/scripts/client.spec.ts
```

Expected output: `# pass N  # fail 0`

## File overview

| File | Purpose |
|------|---------|
| `collect.ts` | Gap detection + CSV generation (no auth) |
| `client.ts` | DS write API module (requires `DS_WRITE_TOKEN`) |
| `collect.spec.ts` | Unit tests for pure functions in collect |
| `client.spec.ts` | Unit tests for safety guards in client |

## Related

- `../ds-guide/SKILL.md` — DS API reference
