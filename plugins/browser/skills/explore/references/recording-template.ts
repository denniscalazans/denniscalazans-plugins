/**
 * CDP Screencast recording template — captures Retina-quality PNG frames.
 *
 * ADAPTED FOR UNIFIED PLUGIN: Connects to agent-browser's Chrome via connectOverCDP
 * instead of launching its own browser.  Agent-browser owns the session;
 * this template borrows it for recording, then disconnects.
 *
 * Uses Chrome DevTools Protocol's Page.startScreencast to capture each rendered frame
 * as a PNG at native device pixel ratio (2x = Retina).
 *
 * A keep-rendering script forces Chrome to render during idle periods,
 * ensuring continuous frame capture even during waitForTimeout pauses.
 *
 * Usage:
 *   npx tsx record-<ticket>.ts          # MP4 only (default)
 *   npx tsx record-<ticket>.ts --gif    # Also produce GIF
 *
 * Prerequisites:
 *   - agent-browser running with an authenticated session
 *   - ffmpeg installed: brew install ffmpeg
 *   - Playwright: project dev dependency or npx fallback
 */

import { chromium, Page, CDPSession } from 'playwright';
import * as path from 'path';
import * as fs from 'fs';
import { execFileSync } from 'child_process';

// --- CONFIGURATION (agent fills these in) ---
const BASE_URL = 'http://localhost:4200';
const TICKET = 'demo';
const SUMMARY = 'site-creation';
const VIDEO_DIR = path.resolve('.agents.tmp', 'recordings');
const FRAME_DIR = path.join(VIDEO_DIR, '_frames');
const FILE_STEM = [new Date().toISOString().slice(0, 10).replace(/-/g, ''), TICKET, SUMMARY].filter(Boolean).join('-');
const TRACE_PATH = path.join(VIDEO_DIR, `${FILE_STEM}-trace.zip`);
const PRODUCE_GIF = process.argv.includes('--gif');

// --- Viewport: 1440x900 at 2x = 2880x1800 Retina frames ---
const VIEWPORT_WIDTH = 1440;
const VIEWPORT_HEIGHT = 900;
const DEVICE_SCALE_FACTOR = 2;

// --- Cursor injection script (runs inside the browser) ---
const CURSOR_INIT_SCRIPT = `
  (function installCursor() {
    const CURSOR_SIZE = 20;
    const ID = '__playwright-cursor__';

    function createCursor() {
      if (document.getElementById(ID)) return;
      const cursor = document.createElement('div');
      cursor.id = ID;
      Object.assign(cursor.style, {
        width: CURSOR_SIZE + 'px',
        height: CURSOR_SIZE + 'px',
        borderRadius: '50%',
        backgroundColor: 'rgba(220, 40, 40, 0.85)',
        border: '2px solid rgba(255, 255, 255, 0.95)',
        position: 'fixed',
        top: '-50px',
        left: '-50px',
        zIndex: '2147483647',
        pointerEvents: 'none',
        transition: 'transform 0.08s ease-out, background-color 0.12s ease-out',
        transform: 'translate(-50%, -50%)',
        boxShadow: '0 0 6px rgba(0,0,0,0.4), 0 0 12px rgba(220,40,40,0.3)',
      });
      document.body.appendChild(cursor);
      return cursor;
    }

    function getCursor() {
      return document.getElementById(ID) || createCursor();
    }

    const observer = new MutationObserver(() => {
      if (!document.getElementById(ID) && document.body) createCursor();
    });

    function startObserving() {
      if (document.body) {
        createCursor();
        observer.observe(document.body, { childList: true, subtree: true });
      } else {
        requestAnimationFrame(startObserving);
      }
    }
    startObserving();

    document.addEventListener('mousemove', function(e) {
      const c = getCursor();
      if (c) { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; }
    }, { passive: true });

    document.addEventListener('mousedown', function() {
      const c = getCursor();
      if (c) {
        c.style.backgroundColor = 'rgba(255, 200, 0, 0.95)';
        c.style.transform = 'translate(-50%, -50%) scale(1.8)';
      }
    });

    document.addEventListener('mouseup', function() {
      const c = getCursor();
      if (c) {
        c.style.backgroundColor = 'rgba(220, 40, 40, 0.85)';
        c.style.transform = 'translate(-50%, -50%) scale(1)';
      }
    });
  })();
`;

// --- Force Chrome to keep rendering during idle periods ---
const KEEP_RENDERING_SCRIPT = `
  (function keepRendering() {
    if (document.getElementById('__keep-rendering__')) return;
    const el = document.createElement('div');
    el.id = '__keep-rendering__';
    el.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;pointer-events:none;z-index:-1;will-change:transform;';
    document.body.appendChild(el);
    let frame = 0;
    function tick() {
      frame++;
      el.style.transform = 'translateX(' + (frame % 2) + 'px)';
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  })();
`;

// --- CDP Screencast frame capture ---

let frameIndex = 0;
let firstFrameTime = 0;
let lastFrameTime = 0;

async function startScreencast(cdp: CDPSession): Promise<void> {
  frameIndex = 0;
  firstFrameTime = 0;
  lastFrameTime = 0;
  fs.mkdirSync(FRAME_DIR, { recursive: true });

  cdp.on('Page.screencastFrame', async (event: { data: string; sessionId: number; metadata: { timestamp: number } }) => {
    const buf = Buffer.from(event.data, 'base64');
    const fname = `frame_${String(frameIndex).padStart(5, '0')}.png`;
    fs.writeFileSync(path.join(FRAME_DIR, fname), buf);

    const now = Date.now();
    if (frameIndex === 0) firstFrameTime = now;
    lastFrameTime = now;
    frameIndex++;

    await cdp.send('Page.screencastFrameAck', { sessionId: event.sessionId });
  });

  await cdp.send('Page.startScreencast', {
    format: 'png',
    everyNthFrame: 1,
    maxWidth: VIEWPORT_WIDTH * DEVICE_SCALE_FACTOR,
    maxHeight: VIEWPORT_HEIGHT * DEVICE_SCALE_FACTOR,
  });
}

async function stopScreencast(cdp: CDPSession): Promise<{ totalFrames: number; durationMs: number; effectiveFps: number }> {
  await cdp.send('Page.stopScreencast');
  const durationMs = lastFrameTime - firstFrameTime;
  const effectiveFps = durationMs > 0 ? (frameIndex / (durationMs / 1000)) : 15;
  return { totalFrames: frameIndex, durationMs, effectiveFps };
}

// --- Cursor position tracker ---
let lastX = 0;
let lastY = 0;

async function smoothMove(
  page: Page, toX: number, toY: number, steps = 25, delayMs = 16,
): Promise<void> {
  const fromX = lastX;
  const fromY = lastY;
  for (let i = 1; i <= steps; i++) {
    const ratio = i / steps;
    const eased = ratio < 0.5
      ? 4 * ratio * ratio * ratio
      : 1 - Math.pow(-2 * ratio + 2, 3) / 2;
    const x = Math.round(fromX + (toX - fromX) * eased);
    const y = Math.round(fromY + (toY - fromY) * eased);
    await page.mouse.move(x, y);
    await page.waitForTimeout(delayMs);
  }
  lastX = toX;
  lastY = toY;
}

async function clickElement(page: Page, selector: string): Promise<void> {
  const el = page.locator(selector);
  await el.waitFor();
  const box = await el.boundingBox();
  if (!box) throw new Error(`Element not visible: ${selector}`);
  const cx = box.x + box.width / 2;
  const cy = box.y + box.height / 2;
  await smoothMove(page, cx, cy);
  await page.mouse.click(cx, cy);
  await page.waitForTimeout(500);
}

async function fillField(page: Page, selector: string, text: string): Promise<void> {
  const el = page.locator(selector);
  await el.waitFor();
  const box = await el.boundingBox();
  if (!box) throw new Error(`Element not visible: ${selector}`);
  await smoothMove(page, box.x + box.width / 2, box.y + box.height / 2);
  await el.click();
  await page.waitForTimeout(200);
  await el.fill(text);
  await page.waitForTimeout(800);
}

/**
 * Navigate to a URL and re-inject cursor + keep-rendering scripts.
 *
 * page.evaluate() injections do not survive navigation (unlike addInitScript).
 * This helper re-injects after every navigation.
 */
async function navigateAndInject(page: Page, url: string): Promise<void> {
  await page.goto(url, { waitUntil: 'load' });
  await page.evaluate(CURSOR_INIT_SCRIPT);
  await page.evaluate(KEEP_RENDERING_SCRIPT);
  await page.waitForTimeout(500);
}

async function main(): Promise<void> {
  if (!fs.existsSync(VIDEO_DIR)) fs.mkdirSync(VIDEO_DIR, { recursive: true });

  // --- Connect to agent-browser's Chrome via CDP ---
  const cdpUrl = execFileSync('agent-browser', ['get', 'cdp-url']).toString().trim();
  console.log(`Connecting to agent-browser Chrome: ${cdpUrl}`);
  const browser = await chromium.connectOverCDP(cdpUrl);

  const contexts = browser.contexts();
  if (contexts.length === 0) {
    console.error('No browser contexts found. Is agent-browser running?');
    process.exit(1);
  }

  const page = contexts[0].pages()[0];
  if (!page) {
    console.error('No pages found in agent-browser context.');
    process.exit(1);
  }

  // --- Set Retina viewport via CDP ---
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: VIEWPORT_WIDTH,
    height: VIEWPORT_HEIGHT,
    deviceScaleFactor: DEVICE_SCALE_FACTOR,
    mobile: false,
  });

  // --- Inject cursor and keep-rendering ---
  await page.evaluate(CURSOR_INIT_SCRIPT);
  await page.evaluate(KEEP_RENDERING_SCRIPT);
  await page.waitForTimeout(500);

  // --- Start screencast ---
  await startScreencast(cdp);

  // ---------------------------------------------------------------
  // REPLACE FLOW STEPS BELOW
  // ---------------------------------------------------------------
  //
  // The agent replaces this section with the user's requested flow.
  //
  // Available helpers:
  //   await clickElement(page, '[data-test-id="my-button"]');
  //   await fillField(page, 'input[name="search"]', 'Stockholm');
  //   await smoothMove(page, 640, 360);
  //   await page.mouse.wheel(0, 300);
  //   await page.waitForTimeout(1000);
  //   await navigateAndInject(page, 'http://localhost:4488/sites/create');
  //
  // IMPORTANT: Use navigateAndInject() instead of page.goto() to
  // re-inject cursor and keep-rendering scripts after navigation.
  //
  // ---------------------------------------------------------------

  await page.waitForTimeout(1000);

  // --- Stop screencast and get timing info ---
  const { totalFrames, durationMs, effectiveFps } = await stopScreencast(cdp);
  const durationSec = (durationMs / 1000).toFixed(1);
  console.log(`\nCaptured ${totalFrames} PNG frames over ${durationSec}s (effective ${effectiveFps.toFixed(1)} fps)`);

  // --- Reset viewport and disconnect ---
  await cdp.send('Emulation.clearDeviceMetricsOverride');
  await browser.close();
  console.log('Disconnected from agent-browser Chrome (session preserved).');

  // --- Stitch frames into MP4 (and optionally GIF) ---
  if (totalFrames === 0) {
    console.error('No frames captured!');
    process.exit(1);
  }

  const inputFps = String(Math.round(effectiveFps));
  console.log(`Using input framerate: ${inputFps} fps (matches wall-clock time)`);

  const mp4Path = path.join(VIDEO_DIR, `${FILE_STEM}.mp4`);
  const gifPath = path.join(VIDEO_DIR, `${FILE_STEM}.gif`);
  const framePattern = path.join(FRAME_DIR, 'frame_%05d.png');

  if (PRODUCE_GIF) {
    console.log(`Stitching to GIF (6 fps, scaled to ${VIEWPORT_WIDTH}px, denoised, palette-optimized)...`);
    execFileSync('ffmpeg', [
      '-framerate', inputFps,
      '-i', framePattern,
      '-vf', `fps=6,scale=${VIEWPORT_WIDTH}:-1:flags=lanczos,hqdn3d=2:2:1:1,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4`,
      '-y', gifPath,
    ], { stdio: 'pipe' });
  }

  console.log('Stitching to MP4 (12 fps, CRF 22, Retina)...');
  execFileSync('ffmpeg', [
    '-framerate', inputFps,
    '-i', framePattern,
    '-vf', 'fps=12',
    '-c:v', 'libx264',
    '-crf', '22',
    '-preset', 'slow',
    '-tune', 'animation',
    '-pix_fmt', 'yuv420p',
    '-an',
    '-y', mp4Path,
  ], { stdio: 'pipe' });

  // Clean up temp frames.
  const frames = fs.readdirSync(FRAME_DIR);
  for (const f of frames) fs.unlinkSync(path.join(FRAME_DIR, f));
  fs.rmdirSync(FRAME_DIR);

  const mp4Size = (fs.statSync(mp4Path).size / 1024).toFixed(1);
  console.log(`\nRecording outputs:`);
  console.log(`  MP4:   ${mp4Path}  (${mp4Size} KB)`);

  if (PRODUCE_GIF) {
    const gifSize = (fs.statSync(gifPath).size / 1024).toFixed(1);
    console.log(`  GIF:   ${gifPath}  (${gifSize} KB)`);
  }

  console.log(`\nDrag the MP4 into your PR description on GitHub.`);
}

main().catch((err) => {
  console.error('Recording failed:', err);
  process.exit(1);
});
