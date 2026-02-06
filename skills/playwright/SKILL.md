---
name: "playwright"
description: "End-to-end testing and QA automation with Playwright + TypeScript. Test strategy, locators, fixtures, POM, assertions, network mocking, visual regression, accessibility, and CI/CD. Use when: writing E2E tests, creating page objects, setting up test fixtures, mocking API responses, visual regression testing, accessibility audits, configuring Playwright projects, debugging flaky tests, or when user mentions Playwright, E2E, end-to-end, browser testing, test automation, QA automation, getByRole, locator, toBeVisible, toHaveScreenshot, or page.route."
---

# Playwright + QA Automation

E2E testing with Playwright and TypeScript. Combines QA strategy (what/why to test) with Playwright implementation (how to test).

## QA Strategy Layer

### Test Pyramid for E2E

E2E tests are expensive. Use them strategically:

- **Test critical user journeys** — login, checkout, signup, core workflows
- **Don't duplicate unit test coverage** — if business logic is tested in unit tests, don't re-test it through the UI
- **Test integration points** — where frontend meets backend, where data flows between systems
- **Test what users actually do** — real workflows, not implementation details

### What Makes a Good E2E Test

```typescript
// GOOD: Tests a real user journey with meaningful assertions
test('user completes checkout flow', async ({ page }) => {
  await page.goto('/products')
  await page.getByRole('button', { name: 'Add to cart' }).first().click()
  await page.getByRole('link', { name: 'Cart' }).click()
  await page.getByRole('button', { name: 'Checkout' }).click()
  await expect(page.getByText('Order confirmed')).toBeVisible()
})

// BAD: Tests implementation details, brittle selectors
test('checkout works', async ({ page }) => {
  await page.goto('/products')
  await page.click('#product-123 > .btn-primary')  // brittle
  await page.waitForTimeout(2000)  // never do this
  expect(await page.locator('.cart-count').innerText()).toBe('1')  // manual assertion
})
```

### Test Independence

Each test must be self-contained:
- Set up its own data (via API calls, not UI when possible)
- Clean up after itself (or use fresh browser contexts — Playwright's default)
- Never depend on another test's state or execution order

## Locator Strategy

**Priority order** (most resilient to least):

| Priority | Locator | Example | Why |
|----------|---------|---------|-----|
| 1 | Role | `getByRole('button', { name: 'Submit' })` | Semantic, accessible |
| 2 | Label | `getByLabel('Email address')` | User-facing text |
| 3 | Placeholder | `getByPlaceholder('Enter email')` | User-facing text |
| 4 | Text | `getByText('Welcome back')` | User-visible content |
| 5 | Test ID | `getByTestId('submit-btn')` | Stable, explicit contract |
| 6 | CSS/XPath | `locator('.btn-primary')` | Last resort only |

```typescript
// Prefer semantic locators
await page.getByRole('button', { name: 'Save changes' }).click()
await page.getByLabel('Email').fill('user@example.com')

// Use test IDs when no semantic option exists
await page.getByTestId('chart-container').isVisible()

// Scoped locators for disambiguation
const dialog = page.getByRole('dialog')
await dialog.getByRole('button', { name: 'Confirm' }).click()

// Filter locators for lists
await page.getByRole('listitem').filter({ hasText: 'Product A' }).click()
```

## Assertions

**Always use web-first assertions** — they auto-wait and retry.

```typescript
// CORRECT: Web-first assertions (auto-wait + retry)
await expect(page.getByText('Success')).toBeVisible()
await expect(page.getByRole('heading')).toHaveText('Dashboard')
await expect(page).toHaveURL(/\/dashboard/)
await expect(page).toHaveTitle('My App - Dashboard')

// WRONG: Manual assertions (race conditions, flaky)
expect(await page.getByText('Success').isVisible()).toBe(true)
const text = await page.locator('h1').innerText()
expect(text).toBe('Dashboard')
```

### Key Assertions

```typescript
// Visibility
await expect(locator).toBeVisible()
await expect(locator).toBeHidden()

// Text content
await expect(locator).toHaveText('exact text')
await expect(locator).toContainText('partial')

// Input state
await expect(locator).toHaveValue('test@example.com')
await expect(locator).toBeChecked()
await expect(locator).toBeDisabled()

// Count
await expect(page.getByRole('listitem')).toHaveCount(3)

// Page-level
await expect(page).toHaveURL(/dashboard/)
await expect(page).toHaveTitle(/Dashboard/)
```

## Page Object Model

Encapsulate page interactions in classes. Tests read like user stories.

```typescript
// pages/LoginPage.ts
import { type Page, type Locator, expect } from '@playwright/test'

export class LoginPage {
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(private readonly page: Page) {
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }
}
```

### Register Page Objects as Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

type Fixtures = {
  loginPage: LoginPage
  dashboardPage: DashboardPage
}

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page))
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page))
  },
})

export { expect } from '@playwright/test'
```

```typescript
// tests/login.spec.ts
import { test, expect } from '../fixtures'

test('successful login redirects to dashboard', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto()
  await loginPage.login('user@example.com', 'password123')
  await expect(dashboardPage.heading).toBeVisible()
})

test('invalid credentials show error', async ({ loginPage }) => {
  await loginPage.goto()
  await loginPage.login('user@example.com', 'wrong')
  await loginPage.expectError('Invalid credentials')
})
```

## Custom Fixtures

Fixtures provide reusable setup/teardown. Use them instead of beforeEach/afterEach.

```typescript
// fixtures.ts — authenticated user fixture
export const test = base.extend<{
  authenticatedPage: Page
}>({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth/user.json'  // pre-saved auth state
    })
    const page = await context.newPage()
    await use(page)
    await context.close()
  },
})
```

### Save Auth State (Global Setup)

```typescript
// global-setup.ts
import { chromium, type FullConfig } from '@playwright/test'

export default async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.goto('/login')
  await page.getByLabel('Email').fill(process.env.TEST_USER!)
  await page.getByLabel('Password').fill(process.env.TEST_PASSWORD!)
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.waitForURL('/dashboard')
  await page.context().storageState({ path: 'auth/user.json' })
  await browser.close()
}
```

## Project Structure

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── checkout/
│   │   └── purchase-flow.spec.ts
│   └── dashboard/
│       └── widgets.spec.ts
├── pages/
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── CheckoutPage.ts
├── components/
│   ├── Modal.ts
│   ├── DataTable.ts
│   └── Navigation.ts
├── fixtures.ts
├── global-setup.ts
└── playwright.config.ts
```

**Guidelines**:
- One page object per page/major section
- Shared components (modals, tables, nav) get their own classes in `components/`
- Tests grouped by feature area
- Single `fixtures.ts` exports the extended `test` object

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'blob' : 'html',
  globalSetup: './tests/global-setup.ts',

  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## Network Mocking (Quick Reference)

```typescript
// Mock an API endpoint
await page.route('**/api/users', route => route.fulfill({
  status: 200,
  contentType: 'application/json',
  body: JSON.stringify([{ id: 1, name: 'Test User' }]),
}))

// Modify a real response
await page.route('**/api/products', async route => {
  const response = await route.fetch()
  const json = await response.json()
  json.push({ id: 999, name: 'Test Product' })
  await route.fulfill({ response, json })
})

// Block resources (speed up tests)
await page.route('**/*.{png,jpg,gif}', route => route.abort())

// Add auth headers
await page.route('**/api/**', route => {
  route.continue({
    headers: { ...route.request().headers(), Authorization: 'Bearer test-token' },
  })
})
```

For advanced mocking patterns (HAR recording, API-first setup, error simulation), see [references/network-mocking.md](references/network-mocking.md).

## Visual Regression (Quick Reference)

```typescript
// Full page screenshot comparison
await expect(page).toHaveScreenshot()

// Element-level comparison
await expect(page.getByTestId('chart')).toHaveScreenshot('chart.png')

// With tolerance for minor rendering differences
await expect(page).toHaveScreenshot({ maxDiffPixelRatio: 0.01 })

// Update baselines: npx playwright test --update-snapshots
```

For deterministic screenshots, animation handling, and CI considerations, see [references/visual-regression.md](references/visual-regression.md).

## Debugging

```bash
# Run with UI mode (interactive debugging)
npx playwright test --ui

# Run with headed browser
npx playwright test --headed

# Run with step-by-step trace viewer
npx playwright test --trace on

# Debug a specific test
npx playwright test -g "login" --debug

# View last test report
npx playwright show-report
```

```typescript
// Pause execution for manual inspection
await page.pause()

// Slow down actions for visual debugging
// In config: use: { launchOptions: { slowMo: 500 } }
```

## Anti-Patterns

```typescript
// NEVER: Hard-coded waits
await page.waitForTimeout(3000)  // Use auto-waiting instead

// NEVER: Brittle CSS selectors
await page.click('#app > div:nth-child(2) > button.btn-primary')

// NEVER: Manual assertions without retry
const text = await page.locator('.status').innerText()
expect(text).toBe('Ready')  // Race condition — use web-first assertions

// NEVER: Testing third-party dependencies
await page.goto('https://external-service.com/verify')  // Mock it instead

// NEVER: Shared mutable state between tests
let sharedUser  // Each test gets its own state via fixtures

// NEVER: Skipping cleanup
// Use fixtures — they handle teardown automatically
```

## Linting

Use `eslint-plugin-playwright` to catch common mistakes:

```bash
npm install -D eslint-plugin-playwright
```

Key rules it catches:
- Missing `await` on async Playwright calls
- Using `page.waitForTimeout` (prefer auto-waiting)
- Manual assertions instead of web-first assertions
- Using forbidden selectors (nth-child, etc.)

## Reference Files

### Network Mocking Patterns
**File**: [references/network-mocking.md](references/network-mocking.md)
**When**: Mocking APIs, HAR recording, intercepting requests, simulating errors, API-first test setup

### Visual Regression Testing
**File**: [references/visual-regression.md](references/visual-regression.md)
**When**: Screenshot comparisons, deterministic rendering, CI screenshot strategies, animation handling

### Accessibility Testing
**File**: [references/accessibility-testing.md](references/accessibility-testing.md)
**When**: WCAG compliance audits, axe-core integration, accessibility fixtures, automated a11y checks

### CI/CD Integration
**File**: [references/ci-cd.md](references/ci-cd.md)
**When**: GitHub Actions setup, sharding, parallelism, artifact management, Docker, reporting strategies
