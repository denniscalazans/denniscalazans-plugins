#!/usr/bin/env node

/**
 * Release changed plugins: strip pre-release suffixes, create tags, and GitHub releases.
 *
 * For each changed plugin, strips any pre-release suffix from the version,
 * creates a git tag <name>-v<version>, and a GitHub Release.
 *
 * Usage:
 *   node scripts/release-versions.mjs --base HEAD~1
 *
 * Requires GH_TOKEN environment variable for `gh release create`.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const MARKETPLACE_JSON = resolve(ROOT, '.claude-plugin/marketplace.json');

// -- Parse arguments ----------------------------------------------------------

const args = process.argv.slice(2);
const baseIndex = args.indexOf('--base');
const baseRef = baseIndex !== -1 ? args[baseIndex + 1] : undefined;

if (!baseRef) {
  console.error('Usage: node scripts/release-versions.mjs --base <git-ref>');
  process.exit(1);
}

// -- Helper: run a command and return trimmed stdout --------------------------

function run(cmd, cmdArgs, opts = {}) {
  return execFileSync(cmd, cmdArgs, { cwd: ROOT, encoding: 'utf8', ...opts }).trim();
}

// -- Discover changed plugins -------------------------------------------------

const marketplace = JSON.parse(readFileSync(MARKETPLACE_JSON, 'utf8'));
const plugins = marketplace.plugins || [];

const changed = [];

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
const tagsToCreate = [];

for (const { name, path } of changed) {
  const pluginJsonPath = `${path}/.claude-plugin/plugin.json`;
  const pluginJsonAbsolute = resolve(ROOT, pluginJsonPath);

  const pkg = JSON.parse(readFileSync(pluginJsonAbsolute, 'utf8'));
  const version = pkg.version;

  // Strip pre-release suffix (e.g. 1.0.1-pr.3 -> 1.0.1)
  let releaseVersion = version.replace(/-.*$/, '');
  let tagName = `${name}-v${releaseVersion}`;

  // If tag already exists, auto-bump patch.
  // This handles the race condition where a PR is merged before the
  // PR version-bump workflow pushes its commit back to the branch.
  let tagExists = false;
  try {
    run('git', ['rev-parse', tagName]);
    tagExists = true;
  } catch {
    // Tag doesn't exist — proceed with current version
  }

  if (tagExists) {
    const [major, minor, patch] = releaseVersion.split('.').map(Number);
    releaseVersion = `${major}.${minor}.${patch + 1}`;
    tagName = `${name}-v${releaseVersion}`;

    // Check the bumped tag too — skip only if both exist
    try {
      run('git', ['rev-parse', tagName]);
      console.log(`Plugin ${name}: tag ${tagName} already exists, skipping`);
      continue;
    } catch {
      // Good — bumped tag doesn't exist
    }

    console.log(`Plugin ${name}: tag ${name}-v${version.replace(/-.*$/, '')} exists, auto-bumping to ${releaseVersion}`);
  }

  // Update plugin.json if version changed
  if (version !== releaseVersion) {
    pkg.version = releaseVersion;
    writeFileSync(pluginJsonAbsolute, JSON.stringify(pkg, null, 2) + '\n');
    run('git', ['add', pluginJsonPath]);
    needsCommit = true;
  }

  tagsToCreate.push({ tagName, name });
  console.log(`Plugin ${name}: will release as ${tagName}`);
}

// -- Commit version cleanups --------------------------------------------------

if (needsCommit) {
  run('git', ['config', 'user.name', 'github-actions[bot]']);
  run('git', ['config', 'user.email', 'github-actions[bot]@users.noreply.github.com']);
  run('git', ['commit', '-m', 'chore: release versions']);
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
    console.error(`Failed to create release ${tagName}: ${err.message}`);
  }
}
