---
name: ds-keys
description: >
  Use before opening a PR that adds or modifies i18n translation keys in FFA.
  Use when running translation gap detection, DS key sync, or CSV import workflows.
  Triggers: "sync DS keys", "dictionary service gap", "translation import",
  "missing keys", "prepare translations for PR".
---

# Dictionary Service Key Sync

Detects translation keys missing from DS prod, infers translations, generates a ready-to-import CSV, and optionally pushes via API.

**When to invoke this skill:** Before opening a PR that adds new `i18n.*` translation keys.

---

## Phase 1 — Validate local JSON (no network)

1. Run `npm run i18n:validate` from the FFA repo root.

2. If it exits non-zero — **stop**. Fix missing/malformed/unused keys first.

3. Confirm both `public/i18n/en.json` and `public/i18n/sv.json` have all new keys filled in (not empty strings).

## Phase 2 — Detect DS gap (public GET, no auth)

1. Invoke the `ffa-translations` skill for project-specific conventions.

2. Run from the FFA repo root:
   ```
   npx tsx scripts/collect.ts
   ```
   (where `scripts/` is relative to this skill directory)

3. If output says "No gap" — all keys already in DS prod. PR is ready. **Stop.**

4. If gap found — script writes `.dictionary-service/import-YYYY-MM-DD.csv` and prints the missing keys.

## Phase 3 — Infer translations (LLM reasoning)

For each gap key, read the existing `en.json` and `sv.json` to:

- Identify the domain prefix (e.g. `siteDetails`, `sections`, `vocabulary`)
- Find semantic neighbors — same domain prefix, same component type (label, button, snackbar, dialog title/message)
- Apply established vocabulary:
  - "trakt" = site, "avdelning" = section, "partner" = partner
  - "ta bort" = delete/remove, "avbryt" = cancel, "bekräfta" = confirm
  - Labels: no trailing period; sentences: period at end
  - Buttons: imperative verb ("Ta bort X", "Avbryt")
- Produce a completed 4-column CSV row for each key

Display the completed CSV to the developer for review.

## Phase 4 — Developer review (required human step)

Print:
```
Review the import CSV: .dictionary-service/import-YYYY-MM-DD.csv
   Edit Swedish values if domain terminology needs adjustment.
   en-CA / en_UK are set to match en — update if regional variants differ.
```

Ask: **"Do the translations look correct? [y/N]"**

- If N: ask what to adjust and re-infer or pause for manual edit.
- If Y: proceed to Phase 5 (CSV upload) or Phase 6 (API push).

## Phase 5 — CSV upload (always available, primary path)

The generated CSV can always be uploaded manually to DS web UI:
```
1. Open https://dictionary-service.akelius.com
2. Select FFA → dev environment → Import
3. Upload .dictionary-service/import-YYYY-MM-DD.csv
4. Migrate: dev → prod
5. Re-run: npx tsx scripts/collect.ts  (should say "No gap")
```

## Phase 6 — API push (optional, only if developer requests it)

Only proceed here if the developer explicitly says "push via API".

### Prerequisites
- `DS_WRITE_TOKEN` must be set in the current terminal session.
- If not set, print the recovery instructions from `client.ts` and stop.

### Push steps

```typescript
import { importCsv, getMigrationDiff, migrateEnv } from './scripts/client';
import fs from 'fs';

// 1. Push CSV to DS dev
const csvContent = fs.readFileSync('.dictionary-service/import-YYYY-MM-DD.csv', 'utf8');
await importCsv(csvContent, 'dev');  // PATCH only — safe upsert

// 2. Preview migration diff
const diff = await getMigrationDiff('dev', 'prod');
console.log('New keys to migrate:', Object.keys(diff.newTranslations));

// 3. Require explicit confirmation
// Ask developer: type "yes" to migrate dev → prod
```

**Require the developer to type `"yes"` to confirm migration.** Do not proceed on Enter alone.

```typescript
// 4. Migrate only the new keys (selective, not bulk)
const keysToMigrate = Object.keys(diff.newTranslations);
await migrateEnv('dev', 'prod', keysToMigrate);
```

### After push
Run `npx tsx scripts/collect.ts` — should print "No gap".

---

## Safety invariants (never violate)

| Rule | Why |
|------|-----|
| Never write to DS prod directly | DS prod = live for all end users |
| Always write to DS dev first | Safe draft zone |
| Never use PUT on `/translations/transfer` | Replaces ALL keys — no undo |
| Only PATCH for imports | Upsert-safe, no deletes |
| `appId = "FFA"` hardcoded | APIM key could touch other apps |
| `DS_WRITE_TOKEN` from `process.env` only | Never interpolate into shell strings |
| Preview diff before migrate | Developer must see what changes |
| Require "yes" typed | Prevent accidental migration |

---

## Scripts reference

| Script | Purpose | Auth |
|--------|---------|------|
| `scripts/collect.ts` | Gap detection + CSV generation | None (public GET) |
| `scripts/client.ts` | DS write API (push, migrate) | `DS_WRITE_TOKEN` |
