/**
 * Pure utility functions for the CDP screencast recording template.
 *
 * Extracted so they can be unit tested independently of Playwright.
 */

/**
 * Ease-in-out cubic function for natural-feeling mouse movement.
 *
 * Returns values between 0 and 1.
 * Slow at start, fast in the middle, slow at end.
 */
export function easeInOutCubic(ratio: number): number {
  return ratio < 0.5
    ? 4 * ratio * ratio * ratio
    : 1 - Math.pow(-2 * ratio + 2, 3) / 2;
}

/**
 * Linear interpolation between two values using an eased ratio.
 */
export function interpolate(from: number, to: number, eased: number): number {
  return from + (to - from) * eased;
}

/**
 * Format a Date as a 14-digit timestamp string: YYYYMMDDHHmmss.
 */
export function formatTimestamp(date: Date): string {
  return date.toISOString().replace(/[-:T.]/g, '').slice(0, 14);
}

/**
 * Compute effective frames per second from wall-clock timestamps.
 *
 * CDP screencast delivers frames at variable rates depending on browser activity.
 * Using the actual wall-clock duration ensures playback matches real-time.
 *
 * Returns 15 as fallback if duration is zero (e.g., single frame).
 */
export function computeEffectiveFps(totalFrames: number, durationMs: number): number {
  if (durationMs <= 0) return 15;
  return totalFrames / (durationMs / 1000);
}

/**
 * Build ffmpeg arguments for GIF conversion from PNG frames.
 *
 * Settings: 6 fps, scaled to viewport width (1440px), denoised (hqdn3d),
 * palette-optimized with bayer dithering.
 *
 * The denoise step (hqdn3d) removes compression artifacts before palette generation.
 * This is the technique used by the KAP screen recording app — it reduces GIF sizes
 * because GIF's LZW compression works better on clean pixel data.
 */
export function buildGifArgs(
  inputFps: string,
  framePattern: string,
  outputPath: string,
  viewportWidth = 1440,
): string[] {
  return [
    '-framerate', inputFps,
    '-i', framePattern,
    '-vf', `fps=6,scale=${viewportWidth}:-1:flags=lanczos,hqdn3d=2:2:1:1,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4`,
    '-y', outputPath,
  ];
}

/**
 * Build ffmpeg arguments for MP4 conversion from PNG frames.
 *
 * Settings: 12 fps output, H.264, CRF 22, animation-tuned, yuv420p for compatibility, no audio.
 *
 * CRF 22 keeps text crisp (CRF 26+ makes text blurry at Retina resolution).
 * `-tune animation` optimizes for screen content: longer GOPs, better sharp edges.
 * `-pix_fmt yuv420p` ensures GitHub and browser compatibility.
 */
export function buildMp4Args(
  inputFps: string,
  framePattern: string,
  outputPath: string,
): string[] {
  return [
    '-framerate', inputFps,
    '-i', framePattern,
    '-vf', 'fps=12',
    '-c:v', 'libx264',
    '-crf', '22',
    '-preset', 'slow',
    '-tune', 'animation',
    '-pix_fmt', 'yuv420p',
    '-an',
    '-y', outputPath,
  ];
}
