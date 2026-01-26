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

## ⚠️ CRITICAL: Security-First SQL (MANDATORY)

**Rule**: NEVER use string concatenation for SQL. ALWAYS use parameterized queries.

```javascript
// ❌ NEVER: SQL injection vulnerability
const domain = req.query.domain
const sql = `SELECT * FROM events WHERE domain LIKE '%${domain}%'` // DANGER!

// ✅ ALWAYS: Parameterized queries
const buildDomainFilter = (domain) => {
  const validation = validateDomain(domain)
  if (!validation.valid) throw new Error(validation.error)

  if (validation.domain === 'all') return { sql: '', params: {} }

  // Zero string concatenation
  return {
    sql: 'AND from_address LIKE @domain_pattern',
    params: { domain_pattern: `%${validation.domain}%` }
  }
}

// Usage
const { sql, params } = buildDomainFilter(req.query.domain)
const query = `SELECT * FROM events WHERE 1=1 ${sql}`
const results = await db.queryWithParams(query, params)
```

### SQL Builder Pattern

All SQL builders return `{sql, params}`:

```javascript
// Shared filter builders
export const buildDomainFilter = (domain) => {
  const validation = validateDomain(domain)
  if (!validation.valid) throw new Error(validation.error)

  if (validation.domain === 'all') return { sql: '', params: {} }

  return {
    sql: 'AND from_address LIKE @domain_pattern',
    params: { domain_pattern: `%${validation.domain}%` }
  }
}

export const buildTimeFilter = (startDate, endDate) => {
  return {
    sql: 'AND created_at BETWEEN @start_date AND @end_date',
    params: { start_date: startDate, end_date: endDate }
  }
}

// Combine filters safely
const domain = buildDomainFilter(req.query.domain)
const time = buildTimeFilter(req.query.start, req.query.end)

const query = {
  sql: `SELECT * FROM events WHERE 1=1 ${domain.sql} ${time.sql}`,
  params: { ...domain.params, ...time.params }
}
```

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
import { validateDomain, validateTimeRange } from '../../shared/validators.js'
import { buildDomainFilter, buildTimeFilter } from '../../shared/filters.js'

const route = new Hono()

// ───── Route-scoped validation (closures) ─────
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
  const filters = buildDomainFilter(domain)  // {sql, params}

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

## Middleware Dependency Injection Pattern

### Function Factory for O(1) Performance

```javascript
// middleware/bigquery.js
const createBigQueryAPI = (client, projectId) => ({
  query: (q) => client.query(projectId, q),
  queryWithParams: (q, p) => client.queryWithParams(projectId, q, p)
})

export const bigQueryMiddleware = async (c, next) => {
  const client = new BigQueryRestClient(c.env)
  await client.init()
  c.bq = createBigQueryAPI(client, c.env.BIGQUERY_PROJECT_ID)
  await next()
}

// Usage in routes: await c.bq.queryWithParams(sql, params)
```

### Standard Middleware Pattern

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

// middleware/auth.js
export const authMiddleware = async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')

  if (!token) {
    return c.json({ error: 'Unauthorized' }, 401)
  }

  try {
    c.user = await verifyToken(token, c.env.JWT_SECRET)
    await next()
  } catch (error) {
    return c.json({ error: 'Invalid token' }, 401)
  }
}
```

## Validation Patterns

### Domain Whitelisting

```javascript
// shared/validators.js
const ALLOWED_DOMAINS = ['example.com', 'test.com', 'all']

export const validateDomain = (domain) => {
  if (!domain) {
    return { valid: false, error: 'Domain is required' }
  }

  const normalized = domain.toLowerCase().trim()

  if (!ALLOWED_DOMAINS.includes(normalized)) {
    return { valid: false, error: 'Domain not allowed' }
  }

  return { valid: true, domain: normalized }
}

export const validateTimeRange = (start, end) => {
  const startDate = new Date(start)
  const endDate = new Date(end)

  if (isNaN(startDate.getTime())) {
    return { valid: false, error: 'Invalid start date' }
  }

  if (isNaN(endDate.getTime())) {
    return { valid: false, error: 'Invalid end date' }
  }

  if (startDate > endDate) {
    return { valid: false, error: 'Start date must be before end date' }
  }

  return { valid: true, start: startDate.toISOString(), end: endDate.toISOString() }
}
```

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

export const groupOrdersByDate = (orders) =>
  orders.reduce((groups, order) => {
    const date = order.createdAt.split('T')[0]
    if (!groups[date]) groups[date] = []
    groups[date].push(order)
    return groups
  }, {})
```

## Anti-Patterns (REJECT)

```javascript
// ❌ Routes >500 lines → Split to business/
// ❌ Service layer files → Keep in-route or business/
// ❌ String concatenation SQL → Use {sql, params}
// ❌ Manual client init → Use middleware DI
// ❌ Validation files used by <3 routes → Keep in-route
// ❌ Abstraction layers → Direct implementation
// ❌ Complex error handling frameworks → Simple try/catch
// ❌ Over-engineered logging → Simple logger DI
```

## Testing Strategy

### Pure Business Logic Tests

```javascript
// business/calculations.test.js
import { calculateTotalRevenue, calculateAverageOrderValue } from '../calculations.js'

describe('calculateTotalRevenue', () => {
  it('sums order totals', () => {
    const orders = [
      { total: 100 },
      { total: 200 },
      { total: 50 }
    ]
    expect(calculateTotalRevenue(orders)).toBe(350)
  })

  it('handles empty array', () => {
    expect(calculateTotalRevenue([])).toBe(0)
  })
})
```

### Route Integration Tests

```javascript
// routes/orders/orders.test.js
import { describe, it, expect, beforeEach } from 'vitest'
import app from '../../index.js'

describe('GET /orders', () => {
  let mockDb

  beforeEach(() => {
    mockDb = {
      queryWithParams: jest.fn().mockResolvedValue([
        { id: 1, total: 100 },
        { id: 2, total: 200 }
      ])
    }
  })

  it('returns orders successfully', async () => {
    const res = await app.request('/orders', {
      method: 'GET'
    }, {
      db: mockDb  // Inject mock
    })

    expect(res.status).toBe(200)
    const json = await res.json()
    expect(json.success).toBe(true)
    expect(json.data).toHaveLength(2)
  })

  it('validates required parameters', async () => {
    const res = await app.request('/orders?domain=invalid', {
      method: 'GET'
    }, {
      db: mockDb
    })

    expect(res.status).toBe(400)
    const json = await res.json()
    expect(json.success).toBe(false)
  })
})
```

## Complete API Example

```javascript
// routes/users/users.js
import { Hono } from 'hono'
import { validateEmail, validateRequired } from '../../shared/validators.js'

const route = new Hono()

// ───── Validation ─────
const validateUserInput = (data) => {
  const errors = []

  if (!validateRequired(data.email)) {
    errors.push('Email is required')
  } else if (!validateEmail(data.email)) {
    errors.push('Invalid email format')
  }

  if (!validateRequired(data.name)) {
    errors.push('Name is required')
  }

  return errors.length > 0
    ? { valid: false, errors }
    : { valid: true, data }
}

// ───── Pure business logic ─────
const prepareUserForStorage = (userData, hasher) => ({
  email: userData.email.toLowerCase(),
  name: userData.name.trim(),
  password: hasher.hash(userData.password),
  createdAt: new Date().toISOString()
})

// ───── GET all users ─────
route.get('/', async (c) => {
  try {
    const users = await c.db.query('SELECT id, email, name, created_at FROM users')
    return c.json({ success: true, data: users })
  } catch (error) {
    c.logger.error('Failed to fetch users', error)
    return c.json({ success: false, error: 'Internal error' }, 500)
  }
})

// ───── POST create user ─────
route.post('/', async (c) => {
  try {
    const body = await c.req.json()
    const validation = validateUserInput(body)

    if (!validation.valid) {
      return c.json({ success: false, errors: validation.errors }, 400)
    }

    const userToSave = prepareUserForStorage(validation.data, c.hasher)

    const { sql, params } = {
      sql: 'INSERT INTO users (email, name, password, created_at) VALUES (@email, @name, @password, @created_at) RETURNING id, email, name, created_at',
      params: userToSave
    }

    const [user] = await c.db.queryWithParams(sql, params)

    c.logger.info('User created', { userId: user.id })
    return c.json({ success: true, data: user }, 201)
  } catch (error) {
    c.logger.error('Failed to create user', error)
    return c.json({ success: false, error: 'Internal error' }, 500)
  }
})

export default route
```

## Quality Gates

Before implementing any API endpoint:

1. ✅ **Security-first SQL**: Using `{sql, params}` pattern?
2. ✅ **Route size**: Can route be <500 lines?
3. ✅ **Validation**: Route-scoped closures or shared (3+ routes)?
4. ✅ **Middleware DI**: Using `c.db`, `c.bq`, `c.logger`?
5. ✅ **Pure business logic**: Extracted if reusable (3+ routes)?
6. ✅ **Testing**: Can inject mocks for all dependencies?
7. ✅ **FP principles**: Pure functions, explicit dependencies?

## Performance Considerations

### Configuration Pre-Compilation

```javascript
// For routes that process large datasets
const createDataProcessor = (config) => {
  // Pre-compile validators
  const validators = config.fields.map(field => ({
    name: field.name,
    validate: compileValidator(field.type)
  }))

  return (data) => {
    const errors = []
    for (const validator of validators) {
      if (!validator.validate(data[validator.name])) {
        errors.push(`Invalid ${validator.name}`)
      }
    }
    return errors.length > 0 ? { valid: false, errors } : { valid: true, data }
  }
}

// Setup once
const validateOrder = createDataProcessor(orderSchema)

// Use many times
route.post('/orders', async (c) => {
  const validation = validateOrder(await c.req.json())
  // ...
})
```

## When to Load Additional Content

### Security Deep-Dive
**File**: `security-sql.md`
**When**: Building complex queries, need advanced patterns, training team
**Contains**: Advanced SQL security, complex query patterns, injection prevention

### Middleware Patterns
**File**: `middleware-patterns.md`
**When**: Building custom middleware, advanced DI patterns
**Contains**: Advanced middleware patterns, error handling, request lifecycle

### Validation Strategies
**File**: `validation-patterns.md`
**When**: Complex validation logic, custom validators
**Contains**: Advanced validation patterns, error accumulation, async validation

### Working Examples
**Directory**: `examples/`
**When**: Need complete working API examples
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
