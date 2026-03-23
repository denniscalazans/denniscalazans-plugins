/**
 * Unit tests for export-auth utility functions.
 *
 * Tests the pure logic for session discovery, parsing, validation,
 * and path construction used by the export-auth.ts CLI script.
 *
 * Run with: npx tsx --test export-auth-utils.spec.ts
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import {
  findSessionFile,
  parseSessionFile,
  buildAuthOutputPath,
  validateInput,
  validateStorageState,
} from './export-auth-utils';


const FIXTURES_DIR = join(tmpdir(), `export-auth-test-${process.pid}`);


describe('validateInput', () => {
  it('accepts alphanumeric names with hyphens and underscores', () => {
    assert.doesNotThrow(() => validateInput('my-app', 'admin_01'));
  });

  it('rejects app name with path traversal', () => {
    assert.throws(
      () => validateInput('../etc', 'admin'),
      /Invalid app name/,
    );
  });

  it('rejects role name with path traversal', () => {
    assert.throws(
      () => validateInput('my-app', '../../passwd'),
      /Invalid role name/,
    );
  });

  it('rejects app name with slashes', () => {
    assert.throws(
      () => validateInput('my/app', 'admin'),
      /Invalid app name/,
    );
  });

  it('rejects empty app name', () => {
    assert.throws(
      () => validateInput('', 'admin'),
      /Invalid app name/,
    );
  });

  it('rejects empty role name', () => {
    assert.throws(
      () => validateInput('my-app', ''),
      /Invalid role name/,
    );
  });
});


describe('findSessionFile', () => {
  beforeEach(() => {
    mkdirSync(join(FIXTURES_DIR, 'hash1'), { recursive: true });
    mkdirSync(join(FIXTURES_DIR, 'hash2'), { recursive: true });
  });

  afterEach(() => {
    rmSync(FIXTURES_DIR, { recursive: true, force: true });
  });

  it('returns null when no session file matches', () => {
    const result = findSessionFile(FIXTURES_DIR, 'my-app', 'admin');
    assert.equal(result, null);
  });

  it('returns the path when exactly one match exists', () => {
    const sessionPath = join(FIXTURES_DIR, 'hash1', 'my-app-admin.session');
    writeFileSync(sessionPath, JSON.stringify({ name: 'my-app-admin' }));

    const result = findSessionFile(FIXTURES_DIR, 'my-app', 'admin');
    assert.equal(result, sessionPath);
  });

  it('picks the cwd match when multiple exist', () => {
    const cwd = '/Users/test/project-a';

    const session1 = join(FIXTURES_DIR, 'hash1', 'my-app-admin.session');
    writeFileSync(session1, JSON.stringify({
      name: 'my-app-admin',
      workspaceDir: '/Users/test/project-b',
    }));

    const session2 = join(FIXTURES_DIR, 'hash2', 'my-app-admin.session');
    writeFileSync(session2, JSON.stringify({
      name: 'my-app-admin',
      workspaceDir: cwd,
    }));

    const result = findSessionFile(FIXTURES_DIR, 'my-app', 'admin', cwd);
    assert.equal(result, session2);
  });

  it('returns the first match when no cwd match exists among multiple', () => {
    const session1 = join(FIXTURES_DIR, 'hash1', 'my-app-admin.session');
    writeFileSync(session1, JSON.stringify({ name: 'my-app-admin' }));

    const session2 = join(FIXTURES_DIR, 'hash2', 'my-app-admin.session');
    writeFileSync(session2, JSON.stringify({ name: 'my-app-admin' }));

    const result = findSessionFile(FIXTURES_DIR, 'my-app', 'admin', '/some/other/path');
    assert.ok(result === session1 || result === session2);
  });
});


describe('parseSessionFile', () => {
  beforeEach(() => {
    mkdirSync(FIXTURES_DIR, { recursive: true });
  });

  afterEach(() => {
    rmSync(FIXTURES_DIR, { recursive: true, force: true });
  });

  it('extracts userDataDir, cdpPort, and socketPath', () => {
    const sessionPath = join(FIXTURES_DIR, 'test.session');
    writeFileSync(sessionPath, JSON.stringify({
      name: 'my-app-admin',
      browser: { userDataDir: '/path/to/ud-my-app-admin-chrome' },
      cdpPort: 64230,
      socketPath: '/tmp/my-app-admin.sock',
    }));

    const result = parseSessionFile(sessionPath);
    assert.equal(result.userDataDir, '/path/to/ud-my-app-admin-chrome');
    assert.equal(result.cdpPort, 64230);
    assert.equal(result.socketPath, '/tmp/my-app-admin.sock');
  });

  it('throws on malformed JSON', () => {
    const sessionPath = join(FIXTURES_DIR, 'bad.session');
    writeFileSync(sessionPath, 'not json at all');

    assert.throws(
      () => parseSessionFile(sessionPath),
      /Failed to parse session file/,
    );
  });

  it('throws when userDataDir is missing', () => {
    const sessionPath = join(FIXTURES_DIR, 'incomplete.session');
    writeFileSync(sessionPath, JSON.stringify({
      name: 'my-app-admin',
      cdpPort: 64230,
    }));

    assert.throws(
      () => parseSessionFile(sessionPath),
      /userDataDir not found/,
    );
  });
});


describe('buildAuthOutputPath', () => {
  it('constructs the correct path', () => {
    const result = buildAuthOutputPath('my-app', 'admin');
    assert.equal(result, '.agents.tmp/.auth/my-app-admin.json');
  });

  it('handles underscores and hyphens in names', () => {
    const result = buildAuthOutputPath('my_app', 'super-admin');
    assert.equal(result, '.agents.tmp/.auth/my_app-super-admin.json');
  });
});


describe('validateStorageState', () => {
  it('returns valid for state with cookies', () => {
    const state = {
      cookies: [{ name: 'session', value: 'abc', domain: 'localhost' }],
      origins: [],
    };
    const result = validateStorageState(state);
    assert.equal(result.valid, true);
  });

  it('returns valid for state with origins (localStorage)', () => {
    const state = {
      cookies: [],
      origins: [{ origin: 'http://localhost', localStorage: [{ name: 'token', value: 'xyz' }] }],
    };
    const result = validateStorageState(state);
    assert.equal(result.valid, true);
  });

  it('returns invalid for empty state', () => {
    const state = { cookies: [], origins: [] };
    const result = validateStorageState(state);
    assert.equal(result.valid, false);
    assert.ok(result.reason?.includes('empty'));
  });

  it('returns invalid for null input', () => {
    const result = validateStorageState(null);
    assert.equal(result.valid, false);
  });

  it('returns invalid for undefined input', () => {
    const result = validateStorageState(undefined);
    assert.equal(result.valid, false);
  });
});
