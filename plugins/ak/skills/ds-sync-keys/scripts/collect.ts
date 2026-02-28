#!/usr/bin/env npx tsx
/**
 * collect.ts — Dictionary Service gap computation
 *
 * Reads local en.json + sv.json, fetches DS prod keys (no auth),
 * computes the gap, and writes a ready-to-import CSV.
 *
 * Usage (from FFA repo root):
 *   npx tsx <path-to-plugin>/ak/skills/ds-sync-keys/scripts/collect.ts
 *   npx tsx <path-to-plugin>/ak/skills/ds-sync-keys/scripts/collect.ts --output=.dictionary-service/pending-import.csv
 */

import fs from 'fs';
import * as https from 'https';
import * as path from 'path';

const DS_BASE = 'https://dictionary-service.akelius.com';
const APP_ID = 'FFA' as const;

type TranslationList = Record<string, Record<string, string>>;

// ─── HTTP helpers ────────────────────────────────────────────────────────────

function fetchJson(url: string): Promise<unknown> {
  return new Promise((resolve, reject) => {
    https
      .get(url, (res) => {
        if (!res.statusCode || res.statusCode < 200 || res.statusCode > 299) {
          reject(new Error(`HTTP ${res.statusCode} fetching ${url}`));
          return;
        }
        let body = '';
        res.on('data', (chunk: Buffer) => {
          body += chunk;
        });
        res.on('end', () => {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            reject(new Error(`JSON parse error from ${url}: ${e}`));
          }
        });
      })
      .on('error', reject);
  });
}

// ─── CSV helpers ─────────────────────────────────────────────────────────────

/** Wrap a field value in double quotes, escaping internal double quotes. */
export function csvField(value: string): string {
  return `"${value.replace(/"/g, '""')}"`;
}

export function buildCsvRow(key: string, en: string, sv: string): string {
  return [
    csvField(key),
    csvField(en),
    csvField(en), // en-CA = same as en (unless regional variant needed)
    csvField(en), // en_UK = same as en (unless regional variant needed)
    csvField(sv),
  ].join(';');
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const cwd = process.cwd();

  // Validate we're in the FFA repo root
  const enPath = path.join(cwd, 'public/i18n/en.json');
  const svPath = path.join(cwd, 'public/i18n/sv.json');

  if (!fs.existsSync(enPath)) {
    console.error(`❌ Not found: ${enPath}`);
    console.error('   Run this script from the FFA repo root (where public/i18n/ lives).');
    process.exit(1);
  }

  // Parse local translation files
  const enJson: Record<string, string> = JSON.parse(fs.readFileSync(enPath, 'utf8'));
  const svJson: Record<string, string> = fs.existsSync(svPath)
    ? JSON.parse(fs.readFileSync(svPath, 'utf8'))
    : {};

  const localKeyCount = Object.keys(enJson).length;
  console.log(`📖 Local keys (en.json): ${localKeyCount}`);

  // Fetch DS prod translations (public endpoint — no auth required)
  const url = `${DS_BASE}/api/v3/applications/${APP_ID}/env/prod/translations`;
  console.log(`🌐 Fetching DS prod translations...`);

  let dsProdTranslations: TranslationList;
  try {
    dsProdTranslations = (await fetchJson(url)) as TranslationList;
  } catch (e) {
    console.error(`❌ Failed to fetch DS prod: ${e instanceof Error ? e.message : String(e)}`);
    console.error('   Check VPN/connectivity to dictionary-service.akelius.com');
    process.exit(1);
  }

  const dsProdKeys = new Set(Object.keys(dsProdTranslations));
  console.log(`🌍 DS prod keys: ${dsProdKeys.size}`);

  // Compute gap: keys in local JSON not yet in DS prod
  const gapKeys = Object.keys(enJson).filter((k) => !dsProdKeys.has(k));

  if (gapKeys.length === 0) {
    console.log('\n✅ No gap — all local keys are already in DS prod.');
    console.log('   Your PR can be opened: no DS import needed.');
    return;
  }

  console.log(`\n📋 Gap: ${gapKeys.length} key(s) not in DS prod:\n`);
  gapKeys.forEach((k) => console.log(`   • ${k}`));

  // Build import CSV
  const csvLines: string[] = ['"key";"en";"en-CA";"en_UK";"sv"'];
  for (const key of gapKeys) {
    const en = enJson[key] ?? '';
    const sv = svJson[key] ?? '';
    csvLines.push(buildCsvRow(key, en, sv));
  }
  const csvContent = csvLines.join('\n');

  // Determine output path
  const outputFlag = process.argv.find((a) => a.startsWith('--output='));
  let outputPath: string;
  if (outputFlag) {
    outputPath = path.resolve(cwd, outputFlag.split('=')[1]);
  } else {
    const date = new Date().toISOString().split('T')[0];
    const outputDir = path.join(cwd, '.dictionary-service');
    fs.mkdirSync(outputDir, { recursive: true });
    outputPath = path.join(outputDir, `import-${date}.csv`);
  }

  fs.writeFileSync(outputPath, csvContent, 'utf8');

  console.log(`\n✅ Import CSV written: ${outputPath}`);
  console.log(`   ${gapKeys.length} key(s) ready to import`);
  console.log('\nNext steps:');
  console.log('  1. Review: open ' + outputPath);
  console.log(
    '  2. Upload to DS: https://dictionary-service.akelius.com → FFA → dev env → Import CSV',
  );
  console.log('  3. Migrate: dev → prod in DS UI');
  console.log('  4. Re-run this script to confirm gap is closed before opening your PR.');
}

// Guard: only run when executed directly (not when imported in tests)
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((e) => {
    console.error('Fatal:', e);
    process.exit(1);
  });
}
