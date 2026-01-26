---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Grep, TodoWrite, Task]
description: "FP API patterns for Node.js with security-first SQL (DEPRECATED - see Agent Skills)"
---

# ⚠️ DEPRECATED: This command has been replaced by Agent Skills

**Old**: `/fp:api`, `/fp:api-lean`, `/fp:api-think`
**New**: Skills automatically loaded - just describe what you need!

**Migration**: See `~/.claude/skills/SKILLS-USER-GUIDE.md`

**Why Skills are better:**
- ✅ **Auto-discovery**: No manual commands, Claude finds the right skill
- ✅ **Progressive disclosure**: Only loads what's needed (400-600 lines vs 1200+ lines)
- ✅ **80% less duplication**: Shared core principles, domain-specific patterns
- ✅ **Always available**: Persistent across all sessions

**Example Migration:**
```
Before: /fp:api-lean user-endpoint --method POST
After:  "Create a Node.js API endpoint for users with security-first SQL"
```

**New Skill Location**: `~/.claude/skills/js-fp-api/SKILL.md`

---

# /fp:api - Functional Programming API Patterns (Node.js)

**Note**: This command remains available during transition. New projects should use Agent Skills.

## Purpose

Security-first Node.js API development with functional programming patterns emphasizing pure business logic, middleware dependency injection, and self-contained routes.

## Usage

```
/fp:api [endpoint-name] [--method GET|POST|PUT|DELETE] [--security strict] [--di explicit]
```

## Arguments

- `endpoint-name` - API endpoint to generate
- `--method` - HTTP method (GET, POST, PUT, DELETE)
- `--security` - Security level: strict (default), standard
- `--di` - Dependency injection: explicit (default), auto
- `--test` - Generate tests: comprehensive, unit

## Core Philosophy

**Foundation**: Builds on `/fp:core` principles. Reference for purity, composition, dependency injection, and testing patterns.

**Security practices prevent vulnerabilities, not architectural patterns.** Hybrid approach: **pure functions for business logic** + **middleware with explicit dependencies** + **MANDATORY parameterized SQL**.

## ⚠️ CRITICAL: Security-First SQL (MANDATORY)

**Evidence**: 89% of SQL injection vulnerabilities stem from string concatenation. Parameterized queries prevent 99%+ of SQL injection attacks.

### ✅ ALWAYS: Parameterized Query Builders

```javascript
// Pure function - returns query config
const buildUserFilter = (filters) => {
  const conditions = []
  const params = {}

  if (filters.status) {
    conditions.push('status = @status')
    params.status = filters.status
  }

  if (filters.role) {
    conditions.push('role = @role')
    params.role = filters.role
  }

  return {
    sql: conditions.length > 0
      ? `WHERE ${conditions.join(' AND ')}`
      : '',
    params
  }
}

// Usage in route
const { sql, params } = buildUserFilter({ status: 'active', role: req.query.role })
const users = await db.query(`SELECT * FROM users ${sql}`, params)
```

### ❌ NEVER: String Concatenation

```javascript
// ❌ SQL INJECTION VULNERABILITY
const sql = `SELECT * FROM users WHERE role = '${req.query.role}'`
const users = await db.query(sql) // Attacker can inject: ' OR '1'='1
```

## Middleware Dependency Injection Pattern

**Rule**: Inject dependencies via middleware for testability.

```javascript
// ─────── Service Configuration ───────
const createUserService = (db) => ({
  async getUser(id) {
    return db.query('SELECT * FROM users WHERE id = @id', { id })
  },

  async createUser(data) {
    const result = await db.query(
      'INSERT INTO users (email, name) VALUES (@email, @name)',
      { email: data.email, name: data.name }
    )
    return result.insertId
  }
})

// ─────── Middleware for DI ───────
const withUserService = (dependencies) => (req, res, next) => {
  req.services = {
    user: dependencies.userService
  }
  next()
}

// ─────── Route Handler (Pure Logic) ───────
const handleGetUser = async (req, res) => {
  const userId = parseInt(req.params.id, 10)

  if (!userId || userId <= 0) {
    return res.status(400).json({ error: 'Invalid user ID' })
  }

  try {
    const user = await req.services.user.getUser(userId)

    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }

    res.json(user)
  } catch (error) {
    req.log.error({ error, userId }, 'Failed to get user')
    res.status(500).json({ error: 'Internal server error' })
  }
}

// ─────── Express Setup ───────
const app = express()

// Inject dependencies
const userService = createUserService(db)
app.use(withUserService({ userService }))

// Mount routes
app.get('/users/:id', handleGetUser)
```

## Self-Contained Route Pattern

**Rule**: Each route file contains all related logic (300-500 lines max).

```javascript
// routes/users.js

// ─────── Pure Business Logic ───────
const validateUserData = (data) => {
  const errors = []

  if (!data.email || !data.email.includes('@')) {
    errors.push('Valid email required')
  }

  if (!data.name || data.name.length < 2) {
    errors.push('Name must be at least 2 characters')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

const buildUserFilter = (filters) => {
  const conditions = []
  const params = {}

  if (filters.status) {
    conditions.push('status = @status')
    params.status = filters.status
  }

  if (filters.search) {
    conditions.push('(name LIKE @search OR email LIKE @search)')
    params.search = `%${filters.search}%`
  }

  return {
    sql: conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '',
    params
  }
}

// ─────── Route Handlers ───────
const handlers = {
  async list(req, res) {
    const { sql, params } = buildUserFilter(req.query)

    try {
      const users = await req.services.user.list(sql, params)
      res.json({ users, count: users.length })
    } catch (error) {
      req.log.error({ error }, 'Failed to list users')
      res.status(500).json({ error: 'Internal server error' })
    }
  },

  async create(req, res) {
    const validation = validateUserData(req.body)

    if (!validation.valid) {
      return res.status(400).json({ errors: validation.errors })
    }

    try {
      const userId = await req.services.user.create(req.body)
      const user = await req.services.user.getUser(userId)
      res.status(201).json(user)
    } catch (error) {
      req.log.error({ error, data: req.body }, 'Failed to create user')
      res.status(500).json({ error: 'Internal server error' })
    }
  }
}

// ─────── Router Setup ───────
const createUserRouter = () => {
  const router = express.Router()
  router.get('/', handlers.list)
  router.post('/', handlers.create)
  return router
}

module.exports = { createUserRouter, validateUserData, buildUserFilter }
```

## Testing Strategy

### Unit Tests (Pure Functions - No Dependencies)

```javascript
// __tests__/users.test.js
const { validateUserData, buildUserFilter } = require('../routes/users')

describe('validateUserData', () => {
  it('validates correct user data', () => {
    const result = validateUserData({
      email: 'test@example.com',
      name: 'John Doe'
    })

    expect(result.valid).toBe(true)
    expect(result.errors).toHaveLength(0)
  })

  it('rejects invalid email', () => {
    const result = validateUserData({
      email: 'invalid',
      name: 'John Doe'
    })

    expect(result.valid).toBe(false)
    expect(result.errors).toContain('Valid email required')
  })
})

describe('buildUserFilter', () => {
  it('builds filter with status', () => {
    const { sql, params } = buildUserFilter({ status: 'active' })

    expect(sql).toContain('WHERE status = @status')
    expect(params.status).toBe('active')
  })

  it('builds filter with search', () => {
    const { sql, params } = buildUserFilter({ search: 'john' })

    expect(sql).toContain('LIKE @search')
    expect(params.search).toBe('%john%')
  })
})
```

### Integration Tests (With Services)

```javascript
// __tests__/users.integration.test.js
const request = require('supertest')
const { createApp } = require('../app')

describe('GET /users', () => {
  let app

  beforeAll(() => {
    const mockUserService = {
      list: jest.fn().mockResolvedValue([
        { id: 1, email: 'test@example.com', name: 'Test User' }
      ])
    }

    app = createApp({ userService: mockUserService })
  })

  it('returns list of users', async () => {
    const response = await request(app)
      .get('/users')
      .expect(200)

    expect(response.body.users).toHaveLength(1)
    expect(response.body.users[0].email).toBe('test@example.com')
  })

  it('filters by status', async () => {
    await request(app)
      .get('/users?status=active')
      .expect(200)

    // Verify filter was called correctly
  })
})
```

## Anti-Patterns (AVOID)

### ❌ SQL String Concatenation

```javascript
// ❌ DANGEROUS
const users = await db.query(
  `SELECT * FROM users WHERE status = '${req.query.status}'`
)

// ✅ SAFE
const users = await db.query(
  'SELECT * FROM users WHERE status = @status',
  { status: req.query.status }
)
```

### ❌ God Routes

```javascript
// ❌ 2000-line route file with everything
// routes/api.js (2000 lines)

// ✅ Self-contained route files (300-500 lines each)
// routes/users.js (400 lines)
// routes/posts.js (350 lines)
```

### ❌ Hidden Dependencies

```javascript
// ❌ Global database access
app.get('/users', async (req, res) => {
  const users = await globalDb.query('SELECT * FROM users') // Where did this come from?
})

// ✅ Explicit dependency injection
app.use(withUserService({ userService }))
app.get('/users', async (req, res) => {
  const users = await req.services.user.list() // Clear dependency
})
```

## Complete CRUD Endpoint Example

```javascript
// routes/products.js

// ─────── Pure Functions ───────
const validateProduct = (data) => {
  const errors = []
  if (!data.name || data.name.length < 3) errors.push('Name required (3+ chars)')
  if (!data.price || data.price <= 0) errors.push('Valid price required')
  return { valid: errors.length === 0, errors }
}

const buildProductFilter = (filters) => {
  const conditions = []
  const params = {}

  if (filters.category) {
    conditions.push('category = @category')
    params.category = filters.category
  }

  if (filters.minPrice) {
    conditions.push('price >= @minPrice')
    params.minPrice = parseFloat(filters.minPrice)
  }

  return {
    sql: conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '',
    params
  }
}

// ─────── Service ───────
const createProductService = (db) => ({
  async list(filterSql, filterParams) {
    return db.query(`SELECT * FROM products ${filterSql} ORDER BY created_at DESC`, filterParams)
  },

  async get(id) {
    const [product] = await db.query('SELECT * FROM products WHERE id = @id', { id })
    return product
  },

  async create(data) {
    const result = await db.query(
      'INSERT INTO products (name, price, category) VALUES (@name, @price, @category)',
      { name: data.name, price: data.price, category: data.category }
    )
    return result.insertId
  },

  async update(id, data) {
    await db.query(
      'UPDATE products SET name = @name, price = @price WHERE id = @id',
      { id, name: data.name, price: data.price }
    )
  },

  async delete(id) {
    await db.query('DELETE FROM products WHERE id = @id', { id })
  }
})

// ─────── Handlers ───────
const createHandlers = () => ({
  async list(req, res) {
    const { sql, params } = buildProductFilter(req.query)
    const products = await req.services.product.list(sql, params)
    res.json({ products, count: products.length })
  },

  async get(req, res) {
    const product = await req.services.product.get(parseInt(req.params.id))
    if (!product) return res.status(404).json({ error: 'Product not found' })
    res.json(product)
  },

  async create(req, res) {
    const validation = validateProduct(req.body)
    if (!validation.valid) return res.status(400).json({ errors: validation.errors })

    const productId = await req.services.product.create(req.body)
    const product = await req.services.product.get(productId)
    res.status(201).json(product)
  },

  async update(req, res) {
    const validation = validateProduct(req.body)
    if (!validation.valid) return res.status(400).json({ errors: validation.errors })

    await req.services.product.update(parseInt(req.params.id), req.body)
    const product = await req.services.product.get(parseInt(req.params.id))
    res.json(product)
  },

  async delete(req, res) {
    await req.services.product.delete(parseInt(req.params.id))
    res.status(204).end()
  }
})

// ─────── Router ───────
const createProductRouter = () => {
  const router = express.Router()
  const handlers = createHandlers()

  router.get('/', handlers.list)
  router.get('/:id', handlers.get)
  router.post('/', handlers.create)
  router.put('/:id', handlers.update)
  router.delete('/:id', handlers.delete)

  return router
}

module.exports = { createProductRouter, createProductService, validateProduct, buildProductFilter }
```

## Quality Gates

Before implementing any API endpoint:

1. ✅ **Security-first SQL**: All queries use parameterized queries?
2. ✅ **Middleware DI**: Dependencies injected explicitly?
3. ✅ **Self-contained routes**: Route file 300-500 lines max?
4. ✅ **Pure business logic**: Validation/filtering separated from side effects?
5. ✅ **Comprehensive tests**: Unit tests for pure functions, integration for routes?
6. ✅ **FP principles**: Pure functions, explicit dependencies, composition?

## Foundation Reference

**Core FP Principles**: `/fp:core`
- Purity and side effect isolation
- Composition patterns
- Dependency injection
- Immutability
- Testing strategies

## Success Metrics

- **Security**: Zero SQL injection vulnerabilities
- **Testability**: 95%+ coverage for business logic
- **Maintainability**: Self-contained routes under 500 lines
- **Performance**: Sub-200ms API response times
- **Code Quality**: Simple, readable route handlers

## Philosophy

*"Security practices prevent vulnerabilities, not architectural patterns. Write pure functions for business logic, inject dependencies explicitly through middleware, and use parameterized SQL queries exclusively."*

**Evidence Base**: OWASP Top 10 (SQL Injection #3), Node.js Security Best Practices, Express.js documentation, real-world API security audits.

## Migration to Agent Skills

**When ready to migrate:**

1. Remove this command file: `rm commands/fp/api*.md`
2. Skills automatically available at: `~/.claude/skills/js-fp-api/SKILL.md`
3. Just describe what you need - no commands required!

**Example**: "Create a secure Node.js API endpoint for user management with proper SQL parameterization"
