---
name: navigate
description: >
  Use when the user wants to generate replayable Playwright .flow.ts files for browser navigation, verify
  UI behavior through exploratory testing, create a navigation baseline for a task, or build a disposable
  flow that can later be promoted to a committed E2E test.
  Framework-agnostic — works with any web application that has a dev server.
  Triggers: "navigate", "flow file", "verify UI", "browser flow", "playwright flow", "explore the app",
  "disposable test", "exploratory test".
---

# Navigate — Exploratory Flow Files

Generate replayable Playwright `.flow.ts` files that verify UI behavior with a single command.

Flow files are **disposable** — used for exploration, screenshots, and investigation.
They are not committed to git.
When a flow proves valuable, promote it to a committed E2E test.


## Quick Start

```
/navigate create a record and verify it appears in the listing
/navigate open the details page and check the sidebar
/navigate fill the form and submit, then verify the success message
```


## Prerequisites

1. **Dev server running** — the app must be accessible at a known URL.
2. **Authentication** — if the app requires login, use `dc:browser-login` to create a persistent session first.
3. **Playwright installed** — `@playwright/test` in the project's dev dependencies.


## Two-Track Architecture

This skill creates **Track 2 (exploratory)** files.
Track 1 (committed CI tests) lives in the project's `e2e/` directory.

| | Track 1 — Committed Tests | Track 2 — Navigate Flows |
|---|---|---|
| Files | `e2e/*.spec.ts` | `.agents.tmp/**/*.flow.ts` |
| Config | `playwright.config.ts` | `.claude/skills/navigate/playwright.config.ts` |
| Git | Committed, reviewed | Gitignored, disposable |
| Purpose | CI regression, permanent | Exploration, screenshots, investigation |
| Promotion | N/A | Promote proven flows to Track 1 |

The boundary matters: never mix exploratory flows into committed tests, and never commit `.agents.tmp/` files.


## File Output Rules

All flow artifacts go into self-contained per-flow directories.

```
.agents.tmp/<ticket>/playwright/<flow-name>/
  <flow-name>.flow.ts       <- the flow file
  screenshots/               <- flow-specific screenshots
.agents.tmp/_playwright-artifacts/    <- Playwright traces/retries (global)
```

**Constraints:**
- ALWAYS write to `.agents.tmp/<ticket>/playwright/<flow-name>/`
- NEVER write to `/tmp`, repo root, or any committed directory
- NEVER generate Playwright config files — use the project's permanent config
- If no ticket is provided, use `scratch` as the ticket name


## Four-Phase Workflow

### Phase 1: PLAN

1. **Parse** the flow description to identify:
   - Target route or URL
   - User actions (click, fill, select, navigate)
   - Expected outcomes (page visible, data loaded, element appears)

2. **Discover selectors** by reading the project's templates or components:
   - Check for `data-test-id` attributes (preferred locator strategy)
   - Read `.claude/skills/navigate/registry/pages.json` if it exists — auto-maintained registry of known testIds per route

3. **Identify gaps** — elements that need interaction but lack stable selectors.
   Propose `data-test-id` additions where needed.


### Phase 2: GENERATE

Write the `.flow.ts` file.

**Flow file template:**

```typescript
import { test as base, type Page } from '@playwright/test';

const FLOW_DIR = '.agents.tmp/<ticket>/playwright/<flow-name>';
const SCREENSHOTS_DIR = `${FLOW_DIR}/screenshots`;

// Simple test fixture — adapt auth as needed for your project.
const test = base;

test('<flow description>', async ({ page }) => {
  await page.goto('<route>');

  // ... interactions ...

  // Take a screenshot at a key moment.
  await page.screenshot({
    path: `${SCREENSHOTS_DIR}/01-step-name.png`,
    animations: 'disabled',
  });
});
```

If the project provides `createFlowTest()` from a helpers bundle, use it for authentication:

```typescript
import { createFlowTest, screenshot } from '../../.claude/skills/navigate/helpers/flow-helpers';

const test = createFlowTest('<session-name>');

test('my flow', async ({ page }) => {
  await page.goto('/dashboard');
  await screenshot(page, '01-dashboard', { outputDir: SCREENSHOTS_DIR });
});
```


### Phase 3: HEAL

If the flow fails:
1. Read the error output carefully
2. Classify the failure: selector, timing, auth, navigation, or data
3. Fix the root cause (not symptoms — never add `waitForTimeout`)
4. Re-run until it passes

Use the `dc:playwright-healer` agent if available for automated debugging.


### Phase 4: IMPROVE

After a passing flow:
1. Add screenshots at key decision points
2. Verify assertions match expected behavior
3. Consider promoting stable flows to committed tests (Track 1)


## Page Registry (Auto-Learning)

If the project implements `updatePageRegistry()`, a `pages.json` file is auto-maintained at `.claude/skills/navigate/registry/pages.json`.

After every flow run, it scrapes `data-test-id` attributes from the current page and adds them to the registry.

**Read this file before writing any flow** — it tells you what testIds exist on each route without running the app.


## Running Flows

```bash
npx playwright test --config .claude/skills/navigate/playwright.config.ts <path-to-flow-file>
```

When a specific file is passed, Playwright ignores `testMatch` and `testDir` from the config — only `use`, `timeout`, and `outputDir` settings apply.


## Screenshot Guidelines

- Default to viewport screenshots (`fullPage: false`)
- Scroll target elements into view before screenshots: `await element.scrollIntoViewIfNeeded()`
- Only use `fullPage: true` when explicitly asked
- Disable CSS animations: `animations: 'disabled'`


## Reference Files

This skill includes two TypeScript reference utilities in `references/`:

- **`screenshot.ts`** — viewport screenshots with animation disabling and auto-mkdir
- **`wait-for-api.ts`** — wait for a matching API response by URL pattern + HTTP method, parse JSON body

Copy these into your project's Playwright helpers directory and import as needed.


## Integration with Other Skills

- **dc:browser-login** — authenticate before running flows that require login
- **dc:record** — record flows as MP4/GIF for PR evidence
- **dc:op** — inject credentials securely via 1Password


## Banned Patterns

See `dc/skills/record/references/playwright-antipatterns.md` for the full list.

Key rules:
- **Never** use `waitForTimeout` — masks real timing issues
- **Never** use `waitForLoadState('networkidle')` — unreliable with live content
- **Never** use inflated timeouts — find and fix the actual cause
- **Prefer** `expect(locator).toBeVisible()` over manual boolean checks
- **Use** `Promise.all([waitForResponse, action])` for mutation operations
