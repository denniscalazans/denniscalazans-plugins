import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  parseVersion,
  isHigher,
  stripPreRelease,
  computeReleaseVersion,
  type SemVer,
} from './versioning.js';


describe('parseVersion', () => {
  it('parses a simple semver string', () => {
    const v = parseVersion('2.1.0');
    assert.deepStrictEqual(v, { major: 2, minor: 1, patch: 0, preRelease: undefined });
  });

  it('parses a version with pre-release suffix', () => {
    const v = parseVersion('2.1.1-pr.19');
    assert.deepStrictEqual(v, { major: 2, minor: 1, patch: 1, preRelease: 'pr.19' });
  });

  it('parses version 1.0.0', () => {
    const v = parseVersion('1.0.0');
    assert.deepStrictEqual(v, { major: 1, minor: 0, patch: 0, preRelease: undefined });
  });
});


describe('isHigher', () => {
  it('returns true when major is higher', () => {
    assert.strictEqual(isHigher(parseVersion('3.0.0'), parseVersion('2.9.9')), true);
  });

  it('returns true when minor is higher', () => {
    assert.strictEqual(isHigher(parseVersion('2.2.0'), parseVersion('2.1.9')), true);
  });

  it('returns true when patch is higher', () => {
    assert.strictEqual(isHigher(parseVersion('2.1.1'), parseVersion('2.1.0')), true);
  });

  it('returns false when equal', () => {
    assert.strictEqual(isHigher(parseVersion('2.1.0'), parseVersion('2.1.0')), false);
  });

  it('returns false when lower', () => {
    assert.strictEqual(isHigher(parseVersion('1.0.0'), parseVersion('2.0.0')), false);
  });

  it('ignores pre-release suffix for comparison', () => {
    assert.strictEqual(isHigher(parseVersion('2.1.1-pr.5'), parseVersion('2.1.0')), true);
  });
});


describe('stripPreRelease', () => {
  it('removes pre-release suffix', () => {
    assert.strictEqual(stripPreRelease('2.1.1-pr.19'), '2.1.1');
  });

  it('returns unchanged version when no suffix', () => {
    assert.strictEqual(stripPreRelease('2.1.0'), '2.1.0');
  });

  it('handles complex pre-release suffixes', () => {
    assert.strictEqual(stripPreRelease('1.0.0-beta.1.rc.2'), '1.0.0');
  });
});


describe('computeReleaseVersion', () => {
  it('strips pre-release when tag does not exist', () => {
    const tagExists = (_tag: string) => false;
    const result = computeReleaseVersion('dc', '2.1.1-pr.19', tagExists);
    assert.deepStrictEqual(result, { version: '2.1.1', tag: 'dc-v2.1.1', autoBumped: false });
  });

  it('returns base version when no pre-release and tag does not exist', () => {
    const tagExists = (_tag: string) => false;
    const result = computeReleaseVersion('dc', '2.1.0', tagExists);
    assert.deepStrictEqual(result, { version: '2.1.0', tag: 'dc-v2.1.0', autoBumped: false });
  });

  it('auto-bumps patch when tag already exists (race condition)', () => {
    const tagExists = (tag: string) => tag === 'dc-v2.1.0';
    const result = computeReleaseVersion('dc', '2.1.0', tagExists);
    assert.deepStrictEqual(result, { version: '2.1.1', tag: 'dc-v2.1.1', autoBumped: true });
  });

  it('auto-bumps patch when stripped pre-release tag exists', () => {
    const tagExists = (tag: string) => tag === 'dc-v2.1.1';
    const result = computeReleaseVersion('dc', '2.1.1-pr.19', tagExists);
    assert.deepStrictEqual(result, { version: '2.1.2', tag: 'dc-v2.1.2', autoBumped: true });
  });

  it('scans past multiple existing tags to find next available patch', () => {
    const tagExists = (tag: string) => tag === 'dc-v2.1.0' || tag === 'dc-v2.1.1';
    const result = computeReleaseVersion('dc', '2.1.0', tagExists);
    assert.deepStrictEqual(result, { version: '2.1.2', tag: 'dc-v2.1.2', autoBumped: true });
  });

  it('returns skip when all patch slots are taken', () => {
    const tagExists = (_tag: string) => true;
    const result = computeReleaseVersion('dc', '2.1.0', tagExists);
    assert.strictEqual(result, null);
  });

  it('works with code-quality plugin prefix', () => {
    const tagExists = (_tag: string) => false;
    const result = computeReleaseVersion('code-quality', '1.1.3', tagExists);
    assert.deepStrictEqual(result, { version: '1.1.3', tag: 'code-quality-v1.1.3', autoBumped: false });
  });
});
