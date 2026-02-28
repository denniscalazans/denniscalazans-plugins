/**
 * Unit tests for recording utility functions.
 *
 * These test the pure logic extracted from the CDP screencast recording template:
 * interpolation math, timestamp formatting, framerate computation, and ffmpeg command construction.
 *
 * Run with: npx tsx --test recording-utils.spec.ts
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  easeInOutCubic,
  interpolate,
  formatTimestamp,
  computeEffectiveFps,
  buildGifArgs,
  buildMp4Args,
} from './recording-utils';

describe('easeInOutCubic', () => {
  it('returns 0 at the start', () => {
    assert.equal(easeInOutCubic(0), 0);
  });

  it('returns 1 at the end', () => {
    assert.equal(easeInOutCubic(1), 1);
  });

  it('returns 0.5 at the midpoint', () => {
    assert.equal(easeInOutCubic(0.5), 0.5);
  });

  it('eases in slowly at the beginning (value < ratio)', () => {
    const ratio = 0.2;
    const eased = easeInOutCubic(ratio);
    assert.ok(eased < ratio, `Expected ${eased} < ${ratio}`);
  });

  it('eases out slowly at the end (value > ratio)', () => {
    const ratio = 0.8;
    const eased = easeInOutCubic(ratio);
    assert.ok(eased > ratio, `Expected ${eased} > ${ratio}`);
  });

  it('is monotonically increasing', () => {
    let prev = 0;
    for (let i = 1; i <= 100; i++) {
      const current = easeInOutCubic(i / 100);
      assert.ok(current >= prev, `Expected ${current} >= ${prev} at step ${i}`);
      prev = current;
    }
  });
});

describe('interpolate', () => {
  it('returns the start value when eased is 0', () => {
    assert.equal(interpolate(100, 500, 0), 100);
  });

  it('returns the end value when eased is 1', () => {
    assert.equal(interpolate(100, 500, 1), 500);
  });

  it('returns the midpoint when eased is 0.5', () => {
    assert.equal(interpolate(0, 200, 0.5), 100);
  });

  it('handles negative coordinates', () => {
    assert.equal(interpolate(-100, 100, 0.5), 0);
  });

  it('handles reverse direction (from > to)', () => {
    assert.equal(interpolate(500, 100, 1), 100);
  });
});

describe('formatTimestamp', () => {
  it('produces exactly 14 digits', () => {
    const result = formatTimestamp(new Date('2026-02-27T16:03:09.123Z'));
    assert.equal(result.length, 14);
  });

  it('contains only digits', () => {
    const result = formatTimestamp(new Date('2026-02-27T16:03:09.123Z'));
    assert.match(result, /^\d{14}$/);
  });

  it('formats correctly as YYYYMMDDHHmmss', () => {
    const result = formatTimestamp(new Date('2026-02-27T16:03:09.123Z'));
    assert.equal(result, '20260227160309');
  });

  it('handles midnight correctly', () => {
    const result = formatTimestamp(new Date('2026-01-01T00:00:00.000Z'));
    assert.equal(result, '20260101000000');
  });
});

describe('computeEffectiveFps', () => {
  it('computes correct fps for typical recording', () => {
    // 150 frames over 5 seconds = 30 fps
    const fps = computeEffectiveFps(150, 5000);
    assert.equal(fps, 30);
  });

  it('returns 15 as fallback when duration is zero', () => {
    assert.equal(computeEffectiveFps(10, 0), 15);
  });

  it('returns 15 as fallback when duration is negative', () => {
    assert.equal(computeEffectiveFps(10, -100), 15);
  });

  it('handles single-second recording', () => {
    // 20 frames over 1 second = 20 fps
    const fps = computeEffectiveFps(20, 1000);
    assert.equal(fps, 20);
  });

  it('returns fractional fps for slow capture rates', () => {
    // 5 frames over 2 seconds = 2.5 fps
    const fps = computeEffectiveFps(5, 2000);
    assert.equal(fps, 2.5);
  });
});

describe('buildGifArgs', () => {
  const args = buildGifArgs('22', '/frames/frame_%05d.png', '/output.gif');

  it('includes framerate as input flag', () => {
    const idx = args.indexOf('-framerate');
    assert.ok(idx >= 0, 'Missing -framerate flag');
    assert.equal(args[idx + 1], '22');
  });

  it('includes the frame pattern as input', () => {
    const idx = args.indexOf('-i');
    assert.equal(args[idx + 1], '/frames/frame_%05d.png');
  });

  it('includes the output path', () => {
    assert.ok(args.includes('/output.gif'));
  });

  it('uses fps=6 for output', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('fps=6'), 'Missing fps=6');
  });

  it('scales to viewport width (default 1440)', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('scale=1440'), 'Missing scale=1440');
  });

  it('scales to custom viewport width', () => {
    const customArgs = buildGifArgs('22', '/frames/frame_%05d.png', '/output.gif', 1920);
    const vfArg = customArgs[customArgs.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('scale=1920'), 'Missing scale=1920');
  });

  it('includes hqdn3d denoising filter with correct values', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('hqdn3d=2:2:1:1'), 'Missing hqdn3d=2:2:1:1');
  });

  it('includes palettegen with stats_mode=diff', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('stats_mode=diff'), 'Missing stats_mode=diff');
  });

  it('includes paletteuse with bayer dithering', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('dither=bayer'), 'Missing bayer dithering');
  });

  it('overwrites output with -y', () => {
    assert.ok(args.includes('-y'));
  });
});

describe('buildMp4Args', () => {
  const args = buildMp4Args('22', '/frames/frame_%05d.png', '/output.mp4');

  it('includes framerate as input flag', () => {
    const idx = args.indexOf('-framerate');
    assert.ok(idx >= 0, 'Missing -framerate flag');
    assert.equal(args[idx + 1], '22');
  });

  it('includes the frame pattern as input', () => {
    const idx = args.indexOf('-i');
    assert.equal(args[idx + 1], '/frames/frame_%05d.png');
  });

  it('includes the output path', () => {
    assert.ok(args.includes('/output.mp4'));
  });

  it('uses libx264 codec', () => {
    assert.equal(args[args.indexOf('-c:v') + 1], 'libx264');
  });

  it('uses CRF 22', () => {
    assert.equal(args[args.indexOf('-crf') + 1], '22');
  });

  it('uses tune animation', () => {
    assert.equal(args[args.indexOf('-tune') + 1], 'animation');
  });

  it('uses yuv420p pixel format for compatibility', () => {
    assert.equal(args[args.indexOf('-pix_fmt') + 1], 'yuv420p');
  });

  it('disables audio with -an', () => {
    assert.ok(args.includes('-an'));
  });

  it('uses fps=12 for output', () => {
    const vfArg = args[args.indexOf('-vf') + 1];
    assert.ok(vfArg.includes('fps=12'), 'Missing fps=12');
  });

  it('overwrites output with -y', () => {
    assert.ok(args.includes('-y'));
  });
});
