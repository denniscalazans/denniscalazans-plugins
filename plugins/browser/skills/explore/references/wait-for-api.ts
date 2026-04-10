/**
 * API wait utility for Playwright flow files.
 *
 * Waits for a matching API response and parses the JSON body.
 *
 * Copy into your project's Playwright helpers directory.
 *
 * IMPORTANT: Register the listener BEFORE triggering the navigation or action
 * that causes the API call. If the response completes before the listener is
 * registered, it will be missed and the call will time out.
 *
 * CORRECT:
 *   const apiPromise = waitForApi(page, '/api/data');
 *   await page.goto(url);  // triggers the API call
 *   await apiPromise;       // now safe to await
 *
 * WRONG:
 *   await page.goto(url);  // response may already be done
 *   await waitForApi(page, '/api/data');  // listener misses it → timeout
 *
 * ALTERNATIVE: For verification purposes, prefer DOM markers over API
 * interception. Checking rendered content is more robust — it proves the
 * full pipeline works (API → response → rendering), not just the HTTP layer.
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
