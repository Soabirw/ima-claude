---
name: "js-fp-api"
description: "FP API patterns for Node.js with security-first SQL and middleware DI - references js-fp core"
---

# JavaScript FP - Node.js API

Functional programming patterns for Node.js APIs with security-first SQL, middleware dependency injection, and self-contained routes.

## When to Use This Skill

- Building REST APIs with Node.js
- Need security-first SQL patterns
- Implementing middleware-based dependency injection
- Self-contained route architecture
- Testing API endpoints comprehensively

## Core Philosophy

**Self-contained routes** (300-500 lines max) with **security-first SQL**, **middleware DI**, and **pure business logic separation** when genuinely reusable (3+ routes).

**Foundation**: This skill builds on `js-fp` core principles. Reference `../js-fp/SKILL.md` for purity, composition, dependency injection, and testing patterns.

## CRITICAL: Security-First SQL (MANDATORY)

**Rule**: NEVER use string concatenation for SQL. ALWAYS use parameterized queries.

```javascript
// NEVER: SQL injection vulnerability
const sql = `SELECT * FROM events WHERE domain LIKE '%${domain}%'` // DANGER!

// ALWAYS: Parameterized queries returning {sql, params}
const buildDomainFilter = (domain) => {
  const validation = validateDomain(domain)
  if (!validation.valid) throw new Error(validation.error)
  if (validation.domain === 'all') return { sql: '', params: {} }

  return {
    sql: 'AND from_address LIKE @domain_pattern',
    params: { domain_pattern: `%${validation.domain}%` }
  }
}
```

**Deep Dive**: See `references/security-sql.md` for advanced SQL patterns, triple-layer curry, and domain whitelisting.

## Mandatory Architecture

### File Structure

```
/api/
├── middleware/          # DI only (database.js, auth.js)
├── shared/             # ONLY if 3+ routes use it
│   ├── validators.js   # Domain whitelisting, validation
│   ├── filters.js      # SQL builders returning {sql, params}
│   └── constants.js    # Static config
├── business/           # Pure functions ONLY (calculations, transformations)
└── routes/
    ├── [domain]/       # Logical grouping
    │   ├── index.js    # Route orchestrator
    │   └── [endpoint].js # 300-500 lines MAX
    └── [simple].js     # Standalone endpoints
```

### Self-Contained Route Pattern (ENFORCE)

```javascript
import { Hono } from 'hono'
import { validateDomain } from '../../shared/validators.js'
import { buildDomainFilter } from '../../shared/filters.js'

const route = new Hono()

// ───── Route-scoped validation ─────
const validateRequest = (ctx) => {
  const domain = ctx.req.query('domain')
  const validation = validateDomain(domain)
  if (!validation.valid) {
    const error = new Error(validation.error)
    error.status = 400
    throw error
  }
  return { domain: validation.domain }
}

// ───── Security-first SQL building ─────
const buildQuery = (env, { domain }) => {
  const table = getTableReference(env)('events')
  const filters = buildDomainFilter(domain)

  return {
    sql: `SELECT * FROM ${table} WHERE 1=1 ${filters.sql}`,
    params: filters.params
  }
}

// ───── Business logic (keep in-route if <50 lines) ─────
const processData = (raw) => raw.map(r => ({
  ...r,
  timestamp: r.timestamp + 'Z'
}))

// ───── Clean orchestration ─────
route.get('/', async (c) => {
  try {
    const params = validateRequest(c)
    const { sql, params: qp } = buildQuery(c.env, params)
    const raw = await c.db.queryWithParams(sql, qp)  // Middleware-injected
    return c.json({ success: true, data: processData(raw) })
  } catch (error) {
    return c.json({ success: false, error: error.message }, error.status || 500)
  }
})

export default route
```

## Middleware Dependency Injection

Inject dependencies via middleware context, not per-request instantiation.

```javascript
// middleware/database.js
export const databaseMiddleware = async (c, next) => {
  const db = createDatabaseClient(c.env.DATABASE_URL)
  c.db = {
    query: (sql) => db.query(sql),
    queryWithParams: (sql, params) => db.query(sql, params),
    transaction: (fn) => db.transaction(fn)
  }
  await next()
}

// Usage in routes: await c.db.queryWithParams(sql, params)
```

**Deep Dive**: See `references/middleware-patterns.md` for function factories, auth middleware, and testing patterns.

## When to Extract to business/

**Extract ONLY if**:
- Function is genuinely reusable (3+ routes use it)
- Pure calculation/transformation
- No side effects
- 100% testable

```javascript
// business/calculations.js
export const calculateTotalRevenue = (orders) =>
  orders.reduce((sum, order) => sum + order.total, 0)

export const calculateAverageOrderValue = (orders) => {
  if (orders.length === 0) return 0
  return calculateTotalRevenue(orders) / orders.length
}
```

## Anti-Patterns (REJECT)

```javascript
// Routes >500 lines → Split to business/
// Service layer files → Keep in-route or business/
// String concatenation SQL → Use {sql, params}
// Manual client init → Use middleware DI
// Validation files used by <3 routes → Keep in-route
// Abstraction layers → Direct implementation
// Complex error handling frameworks → Simple try/catch
// Over-engineered logging → Simple logger DI
```

## Testing Strategy

### Pure Business Logic Tests

```javascript
import { calculateTotalRevenue } from '../calculations.js'

describe('calculateTotalRevenue', () => {
  it('sums order totals', () => {
    const orders = [{ total: 100 }, { total: 200 }, { total: 50 }]
    expect(calculateTotalRevenue(orders)).toBe(350)
  })

  it('handles empty array', () => {
    expect(calculateTotalRevenue([])).toBe(0)
  })
})
```

### Route Integration Tests

```javascript
describe('GET /orders', () => {
  const mockDb = {
    queryWithParams: jest.fn().mockResolvedValue([{ id: 1, total: 100 }])
  }

  it('returns orders successfully', async () => {
    const res = await app.request('/orders', { method: 'GET' }, { db: mockDb })
    expect(res.status).toBe(200)
  })

  it('validates required parameters', async () => {
    const res = await app.request('/orders?domain=invalid', { method: 'GET' }, { db: mockDb })
    expect(res.status).toBe(400)
  })
})
```

**Deep Dive**: See `references/middleware-patterns.md` for comprehensive testing patterns.

## Quality Gates

Before implementing any API endpoint:

1. **Security-first SQL**: Using `{sql, params}` pattern?
2. **Route size**: Can route be <500 lines?
3. **Validation**: Route-scoped closures or shared (3+ routes)?
4. **Middleware DI**: Using `c.db`, `c.bq`, `c.logger`?
5. **Pure business logic**: Extracted if reusable (3+ routes)?
6. **Testing**: Can inject mocks for all dependencies?
7. **FP principles**: Pure functions, explicit dependencies?

## When to Load Reference Files

### Security Deep-Dive
**File**: `references/security-sql.md`
**Load When**:
- Building complex multi-filter queries
- Implementing triple-layer curry pattern
- Training team on SQL security
- Debugging injection vulnerabilities
**Contains**: Parameterized queries, SQL builders, domain whitelisting, security checklist

### Middleware Patterns
**File**: `references/middleware-patterns.md`
**Load When**:
- Building custom middleware
- Implementing function factories for O(1) performance
- Setting up auth middleware
- Writing comprehensive integration tests
**Contains**: Context-based DI, function factories, auth patterns, testing with mocks

### Validation Strategies
**File**: `references/validation-patterns.md`
**Load When**:
- Implementing complex validation logic
- Building composable validators
- Deciding where to place validation code
- Implementing error accumulation
**Contains**: validateAll utility, composition patterns, result objects, when to extract

### Working Examples
**Directory**: `examples/`
**Load When**: Need complete working API examples
**Contains**: Full CRUD endpoints, authentication, authorization, testing

## Foundation Reference

**Core FP Principles**: `../js-fp/SKILL.md`
- Purity and side effect isolation
- Composition patterns
- Dependency injection
- Immutability
- Testing strategies

**Deep Dive**: `../js-fp/core-principles.md` for complete FP philosophy

## Success Metrics

- **Security**: Zero SQL injection vulnerabilities
- **Testability**: 95%+ coverage for pure functions
- **Maintainability**: Routes under 500 lines
- **Performance**: Sub-200ms response times
- **Code Quality**: Clear, self-documenting code

## Philosophy

*"Self-contained routes with security-first SQL and minimal abstraction - optimize for readability and security over clever architecture."*
