# Playwright Anti-Patterns Reference

Read this at the start of every test-writing session.
It takes two minutes and prevents the most expensive mistakes.

---

## 1. Banned Patterns

These patterns make tests slow, flaky, or both.
Never use them.
If you see them in existing code, do not copy them.

### `page.waitForTimeout()` — the cardinal sin

`waitForTimeout` adds a fixed delay even when the app is ready in 50ms.
Multiply this across dozens of tests and the suite becomes unusable.

```typescript
// BANNED — arbitrary sleep
await page.getByTestId('save-button').click();
await page.waitForTimeout(2000); // NO
await expect(page.getByText('Saved')).toBeVisible();

// CORRECT — the assertion itself retries until ready
await page.getByTestId('save-button').click();
await expect(page.getByText('Saved')).toBeVisible();
```

### `page.waitForSelector()` — redundant with actions

Playwright actions already auto-wait for elements to be actionable.
Adding `waitForSelector` before a click or assertion is pure noise.

```typescript
// BANNED — double-waiting for no reason
await page.waitForSelector('[data-test-id="submit-button"]');
await page.getByTestId('submit-button').click();

// CORRECT — just act; Playwright waits automatically
await page.getByTestId('submit-button').click();
```

```typescript
// BANNED — waiting before an assertion
await page.waitForSelector('h1');
await expect(page.getByRole('heading')).toBeVisible();

// CORRECT — the expect IS the wait
await expect(page.getByRole('heading')).toBeVisible();
```

### `waitForApi` after navigation — race condition

`waitForResponse` only catches responses that arrive AFTER the listener is registered.
With cached auth sessions, responses can complete in <100ms — before the listener is ready.

```typescript
// BANNED — listener registered after navigation
await page.goto(url);
await waitForApi(page, '/api/data'); // misses fast responses → timeout

// CORRECT — listener registered before navigation
const apiPromise = waitForApi(page, '/api/data');
await page.goto(url);
await apiPromise;

// BETTER — skip API interception entirely, verify via DOM
await page.goto(url);
await page.locator('[data-test-id="data-loaded"]').waitFor({ state: 'attached' });
```


### `page.waitForLoadState('networkidle')` — SPA killer

Single-page applications with websockets, polling, or analytics never reach
`networkidle` — this either hangs forever or wastes hundreds of milliseconds.

```typescript
// BANNED — hangs on SPAs
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');

// CORRECT — wait for the meaningful content instead
await page.goto('/dashboard');
await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
```

### Inflated timeouts — hiding bugs

A per-assertion timeout of 30 seconds is a symptom, not a solution.
If the app is genuinely slow, fix the app or set the timeout at the config level with documentation explaining why.

```typescript
// BANNED — hides the real problem
await expect(page.getByText('Report ready')).toBeVisible({ timeout: 30_000 });

// CORRECT — use the config default; investigate why the element is slow
await expect(page.getByText('Report ready')).toBeVisible();
```

### `waitForResponse` overuse — synchronizing on every call

Most assertions auto-retry until the expected state appears.
`waitForResponse` is only needed when you must verify a mutation's HTTP status
or capture the response body for downstream assertions.

```typescript
// BANNED — unnecessary synchronization
await page.getByRole('button', { name: 'Load more' }).click();
await page.waitForResponse('**/api/products*'); // unnecessary
await expect(page.getByRole('listitem')).toHaveCount(20);

// CORRECT — the count assertion retries until products appear
await page.getByRole('button', { name: 'Load more' }).click();
await expect(page.getByRole('listitem')).toHaveCount(20);
```

When `waitForResponse` IS acceptable — verifying a mutation result:

```typescript
// ACCEPTABLE — need to confirm the HTTP status of a side-effecting call
const [response] = await Promise.all([
  page.waitForResponse(
    (r) => r.url().includes('/api/orders') && r.request().method() === 'POST',
    { timeout: 60_000 },
  ),
  page.getByTestId('place-order-button').click(),
]);
expect(response.status()).toBe(201);
```

The critical rule: start listening BEFORE the action fires, not after.
Registering the listener after the click creates a race condition where the
response can arrive before the listener is attached.

```typescript
// WRONG — race condition
await page.getByTestId('create-button').click();
const response = await page.waitForResponse('**/api/items'); // may already be gone

// CORRECT — listener registered first via Promise.all
const [response] = await Promise.all([
  page.waitForResponse('**/api/items'),
  page.getByTestId('create-button').click(),
]);
```

---

## 2. Speed Rules

### API setup beats UI setup

Clicking through multiple screens to create test data wastes time on steps that
are not under test.
Seed preconditions via the API and navigate directly to the feature.

```typescript
// SLOW — five screens of setup before the real test begins
test('user can edit a product', async ({ page }) => {
  await page.goto('/products/new');
  await page.getByLabel('Name').fill('Widget');
  await page.getByLabel('Price').fill('29.99');
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByText('Created')).toBeVisible();
  // the actual test has not started yet
});

// FAST — arrange via API, test only what matters
test('user can edit a product', async ({ page, request }) => {
  const res = await request.post('/api/products', {
    data: { name: 'Widget', price: 29.99 },
  });
  const { id } = await res.json();

  await page.goto(`/products/${id}/edit`);
  await page.getByLabel('Price').fill('39.99');
  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('$39.99')).toBeVisible();
});
```

### Use `storageState` for auth, not UI login on every test

Logging in through the UI before every test adds seconds per run.
Capture the authenticated session once in global setup and reuse it.

```typescript
// SLOW — full login flow repeated for every test
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@my-app.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});

// FAST — reuse auth state captured once by global setup
test.use({ storageState: './auth/admin.json' });
```

### Use `Promise.all` for concurrent independent operations

When two operations do not depend on each other, run them in parallel.

```typescript
// SEQUENTIAL — unnecessary
await page.getByTestId('first-action').click();
await page.getByTestId('second-action').click();

// PARALLEL — when both can fire at the same time
await Promise.all([
  page.getByTestId('first-action').click(),
  page.getByTestId('second-action').click(),
]);
```

### Parallelize independent tests with `test.describe.configure`

If tests share no mutable state, run the describe block in parallel:

```typescript
test.describe('Product filters', () => {
  test.describe.configure({ mode: 'parallel' });

  test('filter by category', async ({ page }) => { /* ... */ });
  test('filter by price range', async ({ page }) => { /* ... */ });
  test('filter by rating', async ({ page }) => { /* ... */ });
});
```

### Assert final state, not intermediate loading

Waiting for a spinner to appear and then waiting for it to disappear is fragile
and slow.
Assert the content you actually want — Playwright retries until it appears.

```typescript
// BANNED — two waits for a loading artifact
await page.waitForSelector('.spinner');
await page.waitForSelector('.spinner', { state: 'hidden' });

// CORRECT — assert the content; the spinner is irrelevant
await expect(page.getByRole('table')).toBeVisible();
```

---

## 3. Assertion Best Practices

### Prefer `expect()` over manual boolean checks

`expect()` assertions auto-retry with configurable timeout.
Manual `isVisible()` / `count()` calls are snapshot checks — they do not retry,
so they fail on timing without any useful error message.

```typescript
// WRONG — snapshot, no retry
expect(await page.getByRole('dialog').isVisible()).toBe(false);

// CORRECT — retries until the element disappears
await expect(page.getByRole('dialog')).not.toBeVisible();
```

### Prefer specific assertions over existence checks

An assertion that checks content catches regressions a visibility check misses.

```typescript
// WEAK — only confirms the element exists
await expect(page.getByTestId('order-status')).toBeVisible();

// STRONG — confirms the correct value
await expect(page.getByTestId('order-status')).toHaveText('Confirmed');
```

### Assert negative states with `not.toBeVisible()`, not manual checks

```typescript
// WRONG — does not retry
expect(await page.getByRole('alert').isVisible()).toBe(false);

// CORRECT — retries until the condition is met
await expect(page.getByRole('alert')).not.toBeVisible();
```

### Assert navigation with `toHaveURL`

```typescript
// CORRECT — exact match
await expect(page).toHaveURL('/dashboard');

// CORRECT — regex for dynamic segments
await expect(page).toHaveURL(/\/products\/\d+/);
```

### Do not chain `.count()` as a truthiness guard

```typescript
// WRONG — count() is a snapshot; returns 0 if element not yet rendered
if ((await page.getByRole('row').count()) > 0) {
  // may run before rows appear
}

// CORRECT — assert the expected count and let Playwright retry
await expect(page.getByRole('row')).toHaveCount(5);
```
