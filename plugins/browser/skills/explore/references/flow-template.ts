/**
 * Flow file template — generates replayable Playwright flows on agent-browser's Chrome.
 *
 * Connects to agent-browser via connectOverCDP (same authenticated session).
 * No auth export/import needed — same cookies, same localStorage.
 *
 * Usage:
 *   npx tsx <flow-name>.flow.ts
 *   FLOW_ROLE=partner FLOW_APP=ffa npx tsx <flow-name>.flow.ts
 *
 * Prerequisites:
 *   - agent-browser running with an authenticated session
 *   - Playwright: project dev dependency or npx fallback
 */

import { chromium, expect } from 'playwright';
import { execFileSync } from 'child_process';
import * as fs from 'fs';

// --- CONFIGURATION (agent fills these in) ---
const FLOW_DIR = '.agents.tmp/<ticket>/playwright/<flow-name>';
const SCREENSHOTS_DIR = `${FLOW_DIR}/screenshots`;

// Role-agnostic: set FLOW_ROLE and FLOW_APP to run as different users.
const role = process.env.FLOW_ROLE || 'default';
const app = process.env.FLOW_APP || 'app';

// Input validation (path traversal prevention).
if (!/^[a-zA-Z0-9_-]+$/.test(role)) throw new Error(`Invalid FLOW_ROLE: ${role}`);
if (!/^[a-zA-Z0-9_-]+$/.test(app)) throw new Error(`Invalid FLOW_APP: ${app}`);

async function main(): Promise<void> {
  // Connect to agent-browser's Chrome.
  const cdpUrl = execFileSync('agent-browser', ['get', 'cdp-url']).toString().trim();
  const browser = await chromium.connectOverCDP(cdpUrl);

  const contexts = browser.contexts();
  if (contexts.length === 0) throw new Error('No browser contexts. Is agent-browser running?');

  const page = contexts[0].pages()[0];
  if (!page) throw new Error('No pages in agent-browser context.');

  fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

  // ---------------------------------------------------------------
  // REPLACE FLOW STEPS BELOW
  // ---------------------------------------------------------------
  //
  // The agent replaces this section with the user's requested flow.
  //
  // Available:
  //   await page.goto('http://localhost:4488/sites');
  //   await page.locator('[data-test-id="create-button"]').click();
  //   await page.locator('input[name="siteName"]').fill('Test Site');
  //   await expect(page.locator('h1')).toContainText('Created');
  //
  //   // Screenshots:
  //   await page.screenshot({
  //     path: `${SCREENSHOTS_DIR}/01-step-name.png`,
  //     animations: 'disabled',
  //   });
  //
  // ---------------------------------------------------------------

  // Disconnect (don't close — agent-browser owns Chrome).
  await browser.close();
  console.log('Flow complete. Agent-browser session preserved.');
}

main().catch((err) => {
  console.error('Flow failed:', err);
  process.exit(1);
});
