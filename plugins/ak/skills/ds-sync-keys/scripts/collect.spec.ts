/**
 * collect.spec.ts — unit tests for pure functions in collect.ts
 *
 * Run with: npx tsx ~/.claude/scripts/dictionary-service/collect.spec.ts
 * (uses Node.js built-in test runner — no extra dependencies)
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { csvField, buildCsvRow } from './collect.ts';

// ─── csvField ────────────────────────────────────────────────────────────────

describe('csvField', () => {
  it('wraps a plain value in double quotes', () => {
    assert.equal(csvField('hello'), '"hello"');
  });

  it('handles an empty string', () => {
    assert.equal(csvField(''), '""');
  });

  it('escapes internal double quotes by doubling them', () => {
    assert.equal(csvField('say "hello"'), '"say ""hello"""');
  });

  it('preserves newlines (multiline CSV values)', () => {
    assert.equal(csvField('line1\nline2'), '"line1\nline2"');
  });

  it('preserves semicolons without escaping (semicolon is the column separator, not inside a field)', () => {
    assert.equal(csvField('a;b'), '"a;b"');
  });

  it('handles a value with both quotes and newlines', () => {
    const input = 'He said "yes"\nShe said "no"';
    const expected = '"He said ""yes""\nShe said ""no"""';
    assert.equal(csvField(input), expected);
  });
});

// ─── buildCsvRow ─────────────────────────────────────────────────────────────

describe('buildCsvRow', () => {
  it('produces 5 semicolon-separated columns', () => {
    // Can't naively split on ';' because values may contain ';'
    // Instead: verify the known simple case
    const row = buildCsvRow('test.key', 'hello', 'hej');
    assert.equal(row, '"test.key";"hello";"hello";"hello";"hej"');
  });

  it('column order is: key ; en ; en-CA ; en_UK ; sv', () => {
    const row = buildCsvRow('a.b.c', 'english', 'swedish');
    const parts = row.split(';');
    assert.equal(parts.length, 5);
    assert.equal(parts[0], '"a.b.c"');   // key
    assert.equal(parts[1], '"english"'); // en
    assert.equal(parts[2], '"english"'); // en-CA (same as en)
    assert.equal(parts[3], '"english"'); // en_UK (same as en)
    assert.equal(parts[4], '"swedish"'); // sv
  });

  it('en-CA and en_UK are the same as en (no regional variants by default)', () => {
    const row = buildCsvRow('x.y', 'cancel', 'avbryt');
    const parts = row.split(';');
    assert.equal(parts[1], parts[2], 'en should equal en-CA');
    assert.equal(parts[1], parts[3], 'en should equal en_UK');
  });

  it('escapes quotes in key and values', () => {
    const row = buildCsvRow('key.with."quotes"', 'value "with" quotes', 'värde');
    assert.ok(row.includes('""quotes""'), 'key quotes should be escaped');
    assert.ok(row.includes('""with""'), 'value quotes should be escaped');
  });

  it('handles multiline values (real FFA use case)', () => {
    const en = 'First line.\n\nSecond line.';
    const sv = 'Första raden.\n\nAndra raden.';
    const row = buildCsvRow('site.modal.body', en, sv);
    assert.ok(row.includes('\n'), 'multiline values should be preserved');
    assert.ok(row.startsWith('"site.modal.body"'), 'key should be first');
    assert.ok(row.endsWith(`"${sv}"`), 'sv should be last');
  });
});

// ─── Gap computation logic ───────────────────────────────────────────────────

describe('gap computation', () => {
  it('identifies keys in local JSON not present in DS', () => {
    const localKeys = { 'a.b': 'A', 'c.d': 'C', 'e.f': 'E' };
    const dsKeys = new Set(['a.b', 'c.d']);
    const gap = Object.keys(localKeys).filter((k) => !dsKeys.has(k));
    assert.deepEqual(gap, ['e.f']);
  });

  it('returns empty when all local keys are in DS', () => {
    const localKeys = { 'a.b': 'A', 'c.d': 'C' };
    const dsKeys = new Set(['a.b', 'c.d', 'extra.key']);
    const gap = Object.keys(localKeys).filter((k) => !dsKeys.has(k));
    assert.deepEqual(gap, []);
  });

  it('returns all keys when DS has none', () => {
    const localKeys = { 'a.b': 'A', 'c.d': 'C' };
    const dsKeys = new Set<string>();
    const gap = Object.keys(localKeys).filter((k) => !dsKeys.has(k));
    assert.equal(gap.length, 2);
  });
});
