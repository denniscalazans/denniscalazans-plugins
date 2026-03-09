---
name: record-video
description: 'Use when the user asks to record a video, screen recording, demo, GIF, or screencast of a web application flow. Also use when the user mentions recording browser interactions, creating PR evidence videos, or capturing UI workflows. Triggers: "record a video", "make a recording", "screen record", "film a demo", "capture a screencast", "PR evidence video", "record this flow", "record a GIF", "make a demo GIF", "capture my changes".'
---

# Record Video — CDP Screencast with Retina Cursor

Generate and run Playwright scripts that capture Retina-quality browser recordings with a visible red-dot cursor, then produce MP4 or GIF for GitHub PRs.

## How it works

Playwright's `recordVideo` uses VP8 at hardcoded 1Mbps — blurry and not configurable.

This skill uses CDP `Page.startScreencast` to capture PNG frames at native Retina resolution (2880x1800 for a 1440x900 viewport with `deviceScaleFactor: 2`).

A DOM-level red dot cursor follows mousemove events and flashes yellow on click — without it, recordings show things happening with no visible interaction.

A keep-rendering script forces Chrome to render during idle periods, ensuring continuous frame capture even during `waitForTimeout` pauses.

Frames are stitched into MP4 with ffmpeg using wall-clock timestamps for correct playback speed.

## Quick start

1. Read `references/recording-template.ts` (relative to the skill directory) — this is the full working template
2. Copy it into the project root as `record-<ticket>.ts`
3. Set `BASE_URL` and `TICKET` constants
4. Replace the `REPLACE FLOW STEPS BELOW` section with the user's flow
5. Run: `npx tsx record-<ticket>.ts` (append `--gif` to also generate a GIF)
6. Report the MP4 path with file size

## Determining the ticket and base URL

**Ticket:** Extract from the current branch name (e.g., `feat/ffa-475-...` → `ffa-475`) or from the conversation context.

**Base URL:** Check the project for common patterns:
- Angular Nx: look for `serve` target in `project.json` — the port is defined there
- Default fallback: `http://localhost:4200`

## Template helpers

The template provides these helpers — use them instead of raw Playwright calls to get smooth cursor movement:

```typescript
// Move cursor to element center and click
await clickElement(page, 'text=Sites');

// Move cursor to input, click, type text
await fillField(page, 'input[placeholder="Search"]', 'Stockholm');

// Move cursor to arbitrary coordinates
await smoothMove(page, 640, 360);

// Scroll (no cursor movement needed)
await page.mouse.wheel(0, 300);

// Wait for content to render
await page.waitForTimeout(1000);

// Wait for navigation
await page.waitForURL('**/sites/**');
```

## Writing flow steps

Translate the user's description into a sequence of helper calls.

**Pacing matters** — add `waitForTimeout(500-1000)` between interactions so the viewer can follow what's happening.

**Wait for elements** — the `clickElement` and `fillField` helpers already call `waitFor()` internally.

**After navigation** — use `waitForURL` or `waitForSelector` before interacting with new page content.

Example flow for "record creating a new site":
```typescript
await clickElement(page, 'text=Sites');
await page.waitForURL('**/sites');
await page.waitForTimeout(800);

await clickElement(page, 'button:has-text("Create")');
await page.waitForTimeout(500);

await fillField(page, '[formControlName="name"]', 'Skog Stockholm Nord');
await fillField(page, '[formControlName="county"]', 'Stockholm');

await clickElement(page, 'button:has-text("Save")');
await page.waitForTimeout(1500);
```

## Output

**Default (MP4 only):**
- `.videos/<ticket>.mp4` — 12 fps, H.264, CRF 22, Retina quality (~60-200 KB)

**With `--gif` flag:**
- `.videos/<ticket>.gif` — 6 fps, viewport-width, denoised, palette-optimized (~80-150 KB)

Both formats render inline on GitHub PRs.

The `.videos/` directory should be gitignored.

## Prerequisites

- Dev server running at the configured `BASE_URL`
- Playwright browsers: `npx playwright install chromium`
- ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)

## Key technical details

**CDP screencast vs recordVideo:** CDP gives PNG frames at configurable resolution.

Playwright's recordVideo hardcodes VP8 params (`-b:v 1M -deadline realtime -speed 8`) with no public API to change them.

**Retina rendering:** `deviceScaleFactor: 2` tells Chrome to render at 2x regardless of physical display.

A 1440x900 viewport produces 2880x1800 frames — 4x more pixels than CSS resolution.

**Keep-rendering trick:** CDP screencast only captures when Chrome actually renders.

During idle (`waitForTimeout`), nothing renders and frame capture stops.

The injected script toggles a 1px element's `translateX` via `requestAnimationFrame`, forcing Chrome to composite every frame.

**Wall-clock framerate:** CDP delivers frames at variable rates.

The template tracks `Date.now()` on first and last frames, computes `effectiveFps = totalFrames / durationSeconds`, and passes this to ffmpeg so playback duration matches recording time.

**GIF optimization (KAP technique):** `hqdn3d` denoises before palette generation.

This removes compression artifacts that inflate GIF sizes — the key insight from KAP's recording pipeline.

**MP4 settings:** `-tune animation` optimizes for screen content with sharp text edges and flat color areas.

CRF 22 keeps text crisp (CRF 26+ makes text blurry at Retina resolution).

## Authentication

If the app requires login:
- Pre-authenticate the dev server session before recording
- Or use the `auth0-login` skill first if available

## Common Mistakes

| Don't | Do |
|-------|-----|
| Use `page.click()` directly | Use `clickElement(page, selector)` for visible cursor movement |
| Skip `waitForTimeout` between steps | Add 500–1000ms pauses so viewers can follow the flow |
| Set CRF above 25 | Use CRF 22 to keep text crisp at Retina resolution |
| Forget to start the dev server | Verify the dev server is running at `BASE_URL` before executing |
| Use Playwright's `recordVideo` option | Omit it entirely — CDP screencast replaces it |
| Interact with new page content immediately after navigation | Use `waitForURL` or `waitForSelector` first |

## Running tests

The template utility functions (interpolation, timestamp, framerate computation, ffmpeg args) are unit tested.

Run: `npx tsx --test references/recording-utils.spec.ts` (from the skill directory)
