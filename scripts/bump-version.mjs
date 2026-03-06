#!/usr/bin/env node

/**
 * Manual version bump script for major/minor releases.
 *
 * Usage:
 *   node scripts/bump-version.mjs --version 2.0.0
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PLUGIN_JSON = resolve(__dirname, '../plugins/dc/.claude-plugin/plugin.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);
const versionIndex = args.indexOf('--version');

if (versionIndex === -1 || !args[versionIndex + 1]) {
  console.error('Usage: node scripts/bump-version.mjs --version <X.Y.Z>');
  process.exit(1);
}

const newVersion = args[versionIndex + 1];

// -- Validate semver format ---------------------------------------------------

const SEMVER_RE = /^\d+\.\d+\.\d+$/;

if (!SEMVER_RE.test(newVersion)) {
  console.error(`Invalid semver: "${newVersion}". Expected format: X.Y.Z (e.g. 2.0.0)`);
  process.exit(1);
}

// -- Update plugin.json -------------------------------------------------------

const pkg = JSON.parse(readFileSync(PLUGIN_JSON, 'utf8'));
const oldVersion = pkg.version;
pkg.version = newVersion;
writeFileSync(PLUGIN_JSON, JSON.stringify(pkg, null, 2) + '\n');

console.log(`Updated plugins/dc/.claude-plugin/plugin.json: ${oldVersion} -> ${newVersion}`);
