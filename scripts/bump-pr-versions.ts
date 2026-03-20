#!/usr/bin/env npx tsx

/**
 * Bump versions for changed plugins in a PR context.
 *
 * For each changed plugin, computes a pre-release version X.Y.(Z+1)-pr.N
 * based on the main branch version. Skips plugins that are already at the
 * correct version or have been manually bumped higher.
 *
 * Usage:
 *   npx tsx scripts/bump-pr-versions.ts --base origin/main --pr 12
 *
 * Outputs space-separated list of bumped plugin names to stdout (for commit message).
 * Exits with code 0 even if no plugins were bumped.
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { parseVersion, isHigher, computePrVersion } from './lib/versioning.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const MARKETPLACE_JSON = resolve(ROOT, '.claude-plugin/marketplace.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);

function getArg(name: string): string | undefined {
  const idx = args.indexOf(name);
  return idx !== -1 ? args[idx + 1] : undefined;
}

const baseRef = getArg('--base');
const prNumber = getArg('--pr');

if (!baseRef || !prNumber) {
  console.error('Usage: npx tsx scripts/bump-pr-versions.ts --base <git-ref> --pr <number>');
  process.exit(1);
}

// -- Discover changed plugins -------------------------------------------------

interface MarketplacePlugin {
  name: string;
  source: string;
}

interface Marketplace {
  plugins?: MarketplacePlugin[];
}

const marketplace: Marketplace = JSON.parse(readFileSync(MARKETPLACE_JSON, 'utf8'));
const plugins = marketplace.plugins ?? [];

interface ChangedPlugin {
  name: string;
  path: string;
}

const changed: ChangedPlugin[] = [];

for (const plugin of plugins) {
  const sourcePath = plugin.source.replace(/^\.\//, '');
  try {
    const diff = execFileSync(
      'git', ['diff', '--name-only', `${baseRef}...HEAD`, '--', sourcePath],
      { cwd: ROOT, encoding: 'utf8' },
    ).trim();
    if (diff.length > 0) {
      changed.push({ name: plugin.name, path: sourcePath });
    }
  } catch {
    // Skip if diff fails (e.g. base ref doesn't exist)
  }
}

if (changed.length === 0) {
  console.log('No plugins changed, skipping version bump');
  process.exit(0);
}

// -- Bump versions ------------------------------------------------------------

const bumped: string[] = [];

for (const { name, path } of changed) {
  const pluginJsonPath = `${path}/.claude-plugin/plugin.json`;
  const pluginJsonAbsolute = resolve(ROOT, pluginJsonPath);

  // Get version from main branch
  let mainVersionStr = '1.0.0';
  try {
    const mainContent = execFileSync(
      'git', ['show', `${baseRef}:${pluginJsonPath}`],
      { cwd: ROOT, encoding: 'utf8' },
    );
    mainVersionStr = JSON.parse(mainContent).version;
  } catch {
    // File doesn't exist on main yet — use default 1.0.0
  }

  const mainVersion = parseVersion(mainVersionStr);
  const prVersion = computePrVersion(mainVersionStr, Number(prNumber));

  // Read current version on PR branch
  const currentPkg = JSON.parse(readFileSync(pluginJsonAbsolute, 'utf8'));
  const current: string = currentPkg.version;

  // Skip if already at desired version
  if (current === prVersion) {
    console.log(`Plugin ${name}: already at ${prVersion}, skipping`);
    continue;
  }

  // Skip if PR branch has a manual bump higher than main
  const currentParsed = parseVersion(current);
  if (isHigher(currentParsed, mainVersion)) {
    console.log(`Plugin ${name}: version ${current} is higher than main ${mainVersionStr}, skipping`);
    continue;
  }

  // Update plugin.json
  currentPkg.version = prVersion;
  writeFileSync(pluginJsonAbsolute, JSON.stringify(currentPkg, null, 2) + '\n');
  console.log(`Plugin ${name}: bumped to ${prVersion}`);

  // Stage the file
  execFileSync('git', ['add', pluginJsonPath], { cwd: ROOT });
  bumped.push(name);
}

// -- Output bumped names for commit message -----------------------------------

if (bumped.length > 0) {
  // Write to a file so the workflow can read it
  writeFileSync(resolve(ROOT, '.bumped-plugins'), bumped.join(', '));
}
