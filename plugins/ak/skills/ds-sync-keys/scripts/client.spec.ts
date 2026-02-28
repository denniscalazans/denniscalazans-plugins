/**
 * client.spec.ts — unit tests for safety constraints in client.ts
 *
 * Run with: npx tsx --test client.spec.ts (from this directory)
 *
 * Tests the runtime safety guards that prevent destructive operations.
 * HTTPS calls are NOT mocked here (no external dependency) — they are
 * tested via runtime checks that throw before making any network call.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';

import { pushKey, importCsv, migrateEnv } from './client.ts';

const MOCK_TRANSLATIONS = { en: 'hello', sv: 'hej', 'en-CA': 'hello', en_UK: 'hello' };

// ─── env write guard ──────────────────────────────────────────────────────────
// pushKey/importCsv only accept env='dev'. The TypeScript type enforces this at
// compile time; the runtime guard catches JS callers or casts.

describe('env write guard (runtime)', () => {
  it('pushKey throws when env is forced to a non-dev value', async () => {
    await assert.rejects(
      // @ts-expect-error — testing the runtime guard, intentionally bypassing the type
      () => pushKey('test.key', MOCK_TRANSLATIONS, 'prod'),
      (err: Error) => {
        assert.ok(err.message.includes('Write blocked'), `expected "Write blocked" in: ${err.message}`);
        assert.ok(err.message.includes('prod'), `expected env name in: ${err.message}`);
        return true;
      },
    );
  });

  it('importCsv throws when env is forced to a non-dev value', async () => {
    await assert.rejects(
      // @ts-expect-error — intentional type bypass for runtime test
      () => importCsv('"key";"en"', 'stage'),
      /Write blocked/,
    );
  });
});

// ─── migrateEnv guard ─────────────────────────────────────────────────────────

describe('migrateEnv guards', () => {
  it('throws when keys array is empty', async () => {
    await assert.rejects(
      () => migrateEnv('dev', 'prod', []),
      /empty/,
    );
  });
});

// ─── DS_WRITE_TOKEN detection ─────────────────────────────────────────────────

describe('DS_WRITE_TOKEN missing', () => {
  let savedToken: string | undefined;

  beforeEach(() => {
    savedToken = process.env['DS_WRITE_TOKEN'];
    delete process.env['DS_WRITE_TOKEN'];
  });

  afterEach(() => {
    if (savedToken !== undefined) {
      process.env['DS_WRITE_TOKEN'] = savedToken;
    }
  });

  it('pushKey throws a descriptive error when token is not set', async () => {
    await assert.rejects(
      () => pushKey('test.key', MOCK_TRANSLATIONS),
      (err: Error) => {
        assert.ok(
          err.message.includes('DS_WRITE_TOKEN'),
          `expected "DS_WRITE_TOKEN" in error message, got: ${err.message}`,
        );
        return true;
      },
    );
  });

  it('importCsv throws when token is not set', async () => {
    await assert.rejects(
      () => importCsv('"key";"en"'),
      /DS_WRITE_TOKEN/,
    );
  });

  it('migrateEnv throws when token is not set', async () => {
    await assert.rejects(
      () => migrateEnv('dev', 'prod', ['some.key']),
      /DS_WRITE_TOKEN/,
    );
  });
});
