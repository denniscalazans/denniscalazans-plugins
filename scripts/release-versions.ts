#!/usr/bin/env npx tsx

/**
 * Release changed plugins: strip pre-release suffixes, create tags, and GitHub releases.
 *
 * For each changed plugin, strips any pre-release suffix from the version,
 * creates a git tag <name>-v<version>, and a GitHub Release.
 *
 * Usage:
 *   npx tsx scripts/release-versions.ts --base HEAD~1
 *
 * Requires GH_TOKEN environment variable for `gh release create`.
 */

import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { computeReleaseVersion } from './lib/versioning.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const MARKETPLACE_JSON = resolve(ROOT, '.claude-plugin/marketplace.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);
const baseIndex = args.indexOf('--base');
const baseRef = baseIndex !== -1 ? args[baseIndex + 1] : undefined;

if (!baseRef) {
  console.error('Usage: npx tsx scripts/release-versions.ts --base <git-ref>');
  process.exit(1);
}

// -- Helper: run a command and return trimmed stdout --------------------------

function run(cmd: string, cmdArgs: string[], opts: Record<string, unknown> = {}): string {
  return execFileSync(cmd, cmdArgs, { cwd: ROOT, encoding: 'utf8', ...opts }).trim();
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
    const diff = run('git', ['diff', '--name-only', `${baseRef}...HEAD`, '--', sourcePath]);
    if (diff.length > 0) {
      changed.push({ name: plugin.name, path: sourcePath });
    }
  } catch {
    // Skip if diff fails
  }
}

if (changed.length === 0) {
  console.log('No plugins changed, skipping release');
  process.exit(0);
}

// -- Process each changed plugin ----------------------------------------------

let needsCommit = false;

interface TagToCreate {
  tagName: string;
  name: string;
}

const tagsToCreate: TagToCreate[] = [];

function tagExists(tag: string): boolean {
  try {
    run('git', ['rev-parse', tag]);
    return true;
  } catch {
    return false;
  }
}

for (const { name, path } of changed) {
  const pluginJsonPath = `${path}/.claude-plugin/plugin.json`;
  const pluginJsonAbsolute = resolve(ROOT, pluginJsonPath);

  const pkg = JSON.parse(readFileSync(pluginJsonAbsolute, 'utf8'));
  const version: string = pkg.version;

  const result = computeReleaseVersion(name, version, tagExists);

  if (result === null) {
    console.log(`Plugin ${name}: tag already exists, skipping`);
    continue;
  }

  if (result.autoBumped) {
    console.log(`Plugin ${name}: existing tag found, auto-bumping to ${result.version}`);
  }

  // Update plugin.json if version changed
  if (version !== result.version) {
    pkg.version = result.version;
    writeFileSync(pluginJsonAbsolute, JSON.stringify(pkg, null, 2) + '\n');
    run('git', ['add', pluginJsonPath]);
    needsCommit = true;
  }

  tagsToCreate.push({ tagName: result.tag, name });
  console.log(`Plugin ${name}: will release as ${result.tag}`);
}

// -- Commit version cleanups --------------------------------------------------

if (needsCommit) {
  run('git', ['config', 'user.name', 'github-actions[bot]']);
  run('git', ['config', 'user.email', 'github-actions[bot]@users.noreply.github.com']);
  run('git', ['commit', '-m', 'chore: release versions [skip ci]']);
  run('git', ['push']);
}

// -- Create tags and GitHub releases ------------------------------------------

for (const { tagName, name } of tagsToCreate) {
  run('git', ['tag', tagName]);
  run('git', ['push', 'origin', tagName]);

  // Find previous tag for this plugin to scope the changelog.
  // First try plugin-prefixed tags, then fall back to old v* tags.
  let prevTag = '';

  try {
    const pluginTags = run('git', ['tag', '--list', `${name}-v*`, '--sort=-v:refname']);
    const tagList = pluginTags.split('\n').filter(Boolean);
    // The first tag is the one we just created; the second is the previous one
    if (tagList.length >= 2) {
      prevTag = tagList[1];
    }
  } catch {
    // No plugin-prefixed tags found
  }

  if (!prevTag || prevTag === tagName) {
    // Fall back to latest v* tag (backward compat with old dc tags)
    try {
      const oldTags = run('git', ['tag', '--list', 'v*', '--sort=-v:refname']);
      const oldTagList = oldTags.split('\n').filter(Boolean);
      if (oldTagList.length > 0) {
        prevTag = oldTagList[0];
      }
    } catch {
      // No old tags either
    }
  }

  // Create GitHub Release
  const releaseArgs = ['release', 'create', tagName, '--title', tagName, '--generate-notes'];
  if (prevTag) {
    releaseArgs.push('--notes-start-tag', prevTag);
  }

  try {
    run('gh', releaseArgs);
    console.log(`Created release ${tagName}`);
  } catch (err) {
    console.error(`Failed to create release ${tagName}: ${(err as Error).message}`);
  }
}
