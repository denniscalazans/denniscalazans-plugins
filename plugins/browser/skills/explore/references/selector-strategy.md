# Selector Strategy

When translating agent-browser interactions to Playwright locators, use the most stable selector available.


## Verification Strategy — DOM markers > API interception

When verifying that a page loaded data correctly, prefer DOM markers over API response interception.

**DOM markers** verify the full rendering pipeline:
  API request → response → JSON parsing → store update → template rendering

**API interception** only verifies the HTTP layer:
  API request → response

Use DOM markers when:
- A `[data-test-id]` marker exists that only appears after data loads
- You want to verify the user-visible result, not implementation details

Use API interception only when:
- You need to assert on the response body content
- You need to verify specific HTTP headers (e.g., request ID)
- No DOM marker exists for the loaded state


## Priority Order (Most Stable to Least Stable)

### 1. data-test-id / data-testid

Translation-proof, purpose-built for automation.  
Survives refactors, design changes, and language switches.

```typescript
page.locator('[data-test-id="site-name-input"]')
page.locator('[data-testid="submit-button"]')
```


### 2. id attribute

Stable if the app uses meaningful IDs.  
Angular Material generates IDs like `mat-input-0` — these are positional, not semantic.  
Prefer semantic IDs when available.

```typescript
page.locator('#username')
page.locator('#mat-input-0')  // positional — less stable
```


### 3. name attribute + tag

Common on form elements.  
Stable across translations and UI changes.

```typescript
page.locator('input[name="username"]')
page.locator('button[name="action"]')
```


### 4. formcontrolname (Angular-specific)

Angular reactive forms bind inputs to form controls.  
Stable within the Angular app, but meaningless outside Angular.

```typescript
page.locator('[formcontrolname="siteName"]')
page.locator('[formcontrolname="executionQuarter"]')
```


### 5. Structural CSS

Position-based selectors.  
Stable as long as the DOM structure doesn't change.

```typescript
page.locator('mat-row:first-child mat-checkbox')
page.locator('table tr:nth-child(2) td:first-child')
```


### 6. Role + accessible name (Last Resort)

Fragile with translations — the accessible name comes from visible text.  
Use only when no other selector is available.

```typescript
page.getByRole('button', { name: 'Continue' })
page.getByRole('textbox', { name: 'Email address' })
```


## Discovering Selectors

### From the interaction log

The interaction logger hook captures element metadata at interaction time:
```jsonl
{"cmd":"click","ref":"@e2","element":{"tag":"BUTTON","id":"","testId":"","name":"action","selector":"button[name='action']"}}
```

Use the `selector` field from the log entry.


### Via agent-browser eval

When the log doesn't have sufficient metadata, discover selectors at runtime:

```bash
agent-browser eval 'JSON.stringify(Array.from(document.querySelectorAll("[data-test-id],[data-testid],[data-cy]")).map(el => ({id: el.getAttribute("data-test-id") || el.getAttribute("data-testid"), tag: el.tagName})))'
```


### Suggesting test ID additions

When codebase access is available and an element lacks stable selectors:
1. Identify the component template that renders the element
2. Suggest adding `data-test-id="<descriptive-name>"` to the element
3. Follow the project's existing test ID convention (check for `data-test-id` vs `data-testid` vs `data-cy`)
