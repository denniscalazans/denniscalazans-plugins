/**
 * Screenshot utility for Playwright flow files.
 *
 * Takes viewport screenshots with consistent naming, CSS animation disabling,
 * and automatic output directory creation.
 *
 * Copy into your project's Playwright helpers directory.
 */

import { type Page } from '@playwright/test';
import { existsSync, mkdirSync } from 'fs';

/**
 * Takes a viewport screenshot with consistent naming.
 *
 * Does NOT wait for networkidle — live content (maps, analytics, WebSockets)
 * prevents networkidle from ever settling.
 * If you need to wait for something, use a specific assertion before calling this.
 *
 * `outputDir` is required — pass the flow-specific screenshots directory.
 */
export async function screenshot(
  page: Page,
  name: string,
  { fullPage = false, outputDir }: { fullPage?: boolean; outputDir: string },
): Promise<void> {
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  const path = `${outputDir}/${name}.png`;
  await page.screenshot({ path, fullPage, animations: 'disabled' });
  console.log(`  screenshot: ${name}`);
}
