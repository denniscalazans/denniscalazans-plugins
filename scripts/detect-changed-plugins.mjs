#!/usr/bin/env node

/**
 * Detect which plugins have changed relative to a base git ref.
 *
 * Reads .claude-plugin/marketplace.json to discover all plugins,
 * then checks git diff for each plugin's source path.
 *
 * Usage:
 *   node scripts/detect-changed-plugins.mjs --base origin/main
 *   node scripts/detect-changed-plugins.mjs --base HEAD~1
 *
 * Outputs JSON array to stdout:
 *   [{"name":"code-quality","path":"plugins/code-quality"}]
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const MARKETPLACE_JSON = resolve(ROOT, '.claude-plugin/marketplace.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);
const baseIndex = args.indexOf('--base');

if (baseIndex === -1 || !args[baseIndex + 1]) {
  console.error('Usage: node scripts/detect-changed-plugins.mjs --base <git-ref>');
  process.exit(1);
}

const baseRef = args[baseIndex + 1];

// -- Read marketplace manifest ------------------------------------------------

const marketplace = JSON.parse(readFileSync(MARKETPLACE_JSON, 'utf8'));
const plugins = marketplace.plugins || [];

// -- Detect changed plugins ---------------------------------------------------

const changed = [];

for (const plugin of plugins) {
  // Normalize source path (strip leading ./)
  const sourcePath = plugin.source.replace(/^\.\//, '');

  try {
    // Uses three-dot diff range to compare changes on current branch vs base
    const diff = execFileSync(
      'git', ['diff', '--name-only', `${baseRef}...HEAD`, '--', sourcePath],
      { cwd: ROOT, encoding: 'utf8' }
    ).trim();

    if (diff.length > 0) {
      changed.push({ name: plugin.name, path: sourcePath });
    }
  } catch {
    // If the diff command fails (e.g., base ref doesn't exist), skip this plugin
  }
}

// -- Output -------------------------------------------------------------------

console.log(JSON.stringify(changed));
