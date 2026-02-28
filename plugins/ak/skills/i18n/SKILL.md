---
name: ffa-translations
description: >
  FFA-specific translation workflow: key naming, 4-language CSV format,
  Swedish domain vocabulary, and pre-PR DS sync using /dictionary-service-keys command.
  Load when adding or editing i18n keys in the Forest Flow frontend.
---

# FFA Translation Conventions

## Key Format

```
{domain}.{feature}.{element}.{descriptor}   ← 3 to 7 segments
```

**In JSON files** (`public/i18n/en.json`, `sv.json`): NO `i18n.` prefix
```json
{ "siteDetails.softDelete.dialog.title": "delete site" }
```

**In templates / TypeScript**: WITH `i18n.` prefix
```html
{{ 'i18n.siteDetails.softDelete.dialog.title' | translate }}
```

The prefix is added at runtime by `TranslationsLoaderService.prepareKeys()`.

## Common Patterns by Element Type

| Element | Key pattern | Example key |
|---------|------------|-------------|
| Button label | `{domain}.button.{action}.text` | `siteDetails.button.downloadShapeFile.text` |
| Snackbar | `{domain}.snackbar.{action}.text` | `createSite.snackbar.siteCreatedSuccessfully.text` |
| Dialog title | `{domain}.{feature}.dialog.title` | `siteDetails.softDelete.dialog.title` |
| Dialog message | `{domain}.{feature}.dialog.message` | `siteDetails.softDelete.dialog.message` |
| Confirmation title | `{domain}.confirmation.{action}.title` | `siteDetails.confirmation.cancelSite.title` |
| Confirmation message | `{domain}.confirmation.{action}.message` | `siteDetails.confirmation.cancelSite.message` |
| Column header | `{domain}.column.{field}` | `history.column.changedBy` |
| Shared term | `vocabulary.{term}` | `vocabulary.cancel` |

## Swedish Domain Vocabulary

Core FFA terms (use consistently — these are established in the corpus):

| English | Swedish |
|---------|---------|
| site / trakt | trakt |
| section / avdelning | avdelning |
| partner | partner |
| cancel (action) | avbryt |
| delete / remove | ta bort |
| confirm | bekräfta |
| create | skapa |
| load | läsa in / ladda |
| add | lägg till |
| status | status |
| history | historik |
| attribute | attribut |
| changed by | ändrad av |
| changed at | ändrad den |
| new value | nytt värde |
| old value | gammalt värde |
| download | ladda ner |
| upload | ladda upp |
| budget year | budgetår |
| municipality | kommun |
| county | länsstyrelsebeteckning |
| property | fastighet |
| operation | åtgärd |

## Swedish Formatting Rules

- **Labels and button text**: no trailing period (`"ta bort trakt"`, not `"Ta bort trakt."`)
- **Sentences in dialogs/confirmations**: end with period; may include line breaks with `\n\n`
- **Delete/remove pattern**: `"Ta bort X"` (title case on "Ta")
- **Success snackbars**: typically lowercase, no period (`"du har skapat en ny trakt"`)
- **Error snackbars**: sentence with period (`"Det gick inte att skapa trakten. Försök igen."`)
- **Cancellation pattern**: `"borttag"` (noun) for cancelled status; `"ta bort"` for the action

## Real Examples (from corpus)

```
siteDetails.button.downloadSiteDirective.text
  en: "download site directive"
  sv: "ladda ner traktdirektiv"

siteDetails.confirmation.cancelSite.title
  en: "cancel site"
  sv: "ta bort trakt"

siteDetails.confirmation.cancelSite.message
  en: "Canceling a site will also cancel all associated sections.\n\nTo reallocate sections,\nplease remove them before canceling the site."
  sv: "Borttag av denna trakt innebär att alla tillhörande avdelningar också tas bort.\n\nOm du vill omfördela avdelningar till en annan trakt,\nta då bort dem innan du bekräftar borttag av trakten."

createSite.snackbar.siteCreatedSuccessfully.text
  en: "site created successfully"
  sv: "du har skapat en ny trakt"

sections.snackbar.statusUpdatedSuccessfully.text
  en: "section status updated"
  sv: "status uppdaterad"

history.column.changedBy
  en: "changed by"
  sv: "ändrad av"
```

## 4-Language CSV Format

FFA uses 4 locale columns. `en-CA` and `en_UK` default to same as `en` unless regional variants differ (British: "cancelling" vs American: "canceling").

```csv
"key";"en";"en-CA";"en_UK";"sv"
"siteDetails.softDelete.dialog.title";"delete site";"delete site";"delete site";"ta bort trakt"
```

Rules:
- Separator: `;` (semicolon, NOT comma)
- All fields: wrapped in double quotes `"`
- Internal quotes: escaped by doubling `""`
- Multiline values: literal `\n` inside the quoted field (valid CSV)

## Workflow for Adding New Keys

### Step 1: Add to local JSON (always do this first)
Update BOTH files:
- `public/i18n/en.json` — English value (no `i18n.` prefix in key)
- `public/i18n/sv.json` — Swedish value

### Step 2: Validate locally
```bash
npm run i18n:validate
```
Must exit 0 before proceeding.

### Step 3: Sync to DS (before opening PR)
DS prod must have all keys before PR is merged.
```
/ak:ds-sync-keys
```
This skill:
1. Runs `collect.ts` to detect gap vs DS prod
2. Infers translations using the vocabulary above
3. Generates `.dictionary-service/import-YYYY-MM-DD.csv` (gitignored)
4. Developer reviews and uploads to DS UI, or pushes via API

### Key Rule
**DS prod must have all keys before the PR is merged.** FFA reads from DS prod in all environments (test/stage/prod). Missing keys fall back to local JSON — but local JSON is only deployed with a new release, not updated on its own.

## Scripts Reference

| Script | Auth | What it does |
|--------|------|--------------|
| `../ds-sync-keys/scripts/collect.ts` | None | Gap detection + CSV generation |
| `../ds-sync-keys/scripts/client.ts` | `DS_WRITE_TOKEN` | DS write API (pushKey, importCsv, migrateEnv) |

Run from FFA repo root using the script path from the `ds-sync-keys` sibling skill.

## Snackbar Translations Note

Snackbar keys (e.g. `siteDetails.snackbar.softDeleteSite.text`) are served by the Dictionary Service only — they are NOT in the local JSON fallback files. Do not search `public/i18n/` for them.

## Validate Before Every PR

1. `npm run i18n:validate` — checks missing/unused/malformed keys
2. `/ak:ds-sync-keys` — detects DS gap and generates import CSV
3. After uploading CSV to DS: re-run `collect.ts` from the `ds-sync-keys` sibling skill to confirm gap is closed
