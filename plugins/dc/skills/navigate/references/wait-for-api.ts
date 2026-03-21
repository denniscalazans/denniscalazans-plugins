/**
 * API wait utility for Playwright flow files.
 *
 * Waits for a matching API response and parses the JSON body.
 *
 * Copy into your project's Playwright helpers directory.
 */

import { type Page } from '@playwright/test';

/**
 * Waits for an API response matching a URL pattern and HTTP method.
 *
 * Returns the parsed JSON body, or null for empty responses (e.g., 204 No Content).
 */
export async function waitForApi(
  page: Page,
  urlPattern: string,
  method: string = 'GET',
  timeout: number = 10_000,
): Promise<unknown> {
  const response = await page.waitForResponse(
    (res) => res.url().includes(urlPattern) && res.request().method() === method && res.ok(),
    { timeout },
  );
  const text = await response.text();
  return text ? JSON.parse(text) : null;
}
