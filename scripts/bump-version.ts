#!/usr/bin/env npx tsx

/**
 * Manual version bump script for major/minor releases.
 *
 * Usage:
 *   npx tsx scripts/bump-version.ts --version 2.0.0
 *   npx tsx scripts/bump-version.ts --version 1.1.0 --plugin code-quality
 *   npx tsx scripts/bump-version.ts --version 3.0.0 --plugin dc
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const MARKETPLACE_JSON = resolve(__dirname, '../.claude-plugin/marketplace.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);
const versionIndex = args.indexOf('--version');

if (versionIndex === -1 || !args[versionIndex + 1]) {
  console.error('Usage: npx tsx scripts/bump-version.ts --version <X.Y.Z> [--plugin <name>]');
  process.exit(1);
}

const newVersion = args[versionIndex + 1];

const pluginIndex = args.indexOf('--plugin');
const pluginName = pluginIndex !== -1 && args[pluginIndex + 1]
  ? args[pluginIndex + 1]
  : 'dc';

// -- Validate semver format ---------------------------------------------------

const SEMVER_RE = /^\d+\.\d+\.\d+$/;

if (!SEMVER_RE.test(newVersion)) {
  console.error(`Invalid semver: "${newVersion}". Expected format: X.Y.Z (e.g. 2.0.0)`);
  process.exit(1);
}

// -- Resolve plugin path from marketplace.json --------------------------------

interface MarketplacePlugin {
  name: string;
  source: string;
}

interface Marketplace {
  plugins?: MarketplacePlugin[];
}

const marketplace: Marketplace = JSON.parse(readFileSync(MARKETPLACE_JSON, 'utf8'));
const pluginEntry = (marketplace.plugins ?? []).find(p => p.name === pluginName);

if (!pluginEntry) {
  const available = (marketplace.plugins ?? []).map(p => p.name).join(', ');
  console.error(`Plugin "${pluginName}" not found in marketplace.json. Available: ${available}`);
  process.exit(1);
  throw new Error('unreachable');
}

const sourcePath = pluginEntry.source.replace(/^\.\//, '');
const PLUGIN_JSON = resolve(__dirname, '..', sourcePath, '.claude-plugin/plugin.json');

// -- Update plugin.json -------------------------------------------------------

const pkg = JSON.parse(readFileSync(PLUGIN_JSON, 'utf8'));
const oldVersion: string = pkg.version;
pkg.version = newVersion;
writeFileSync(PLUGIN_JSON, JSON.stringify(pkg, null, 2) + '\n');

console.log(`Updated ${sourcePath}/.claude-plugin/plugin.json: ${oldVersion} -> ${newVersion}`);
