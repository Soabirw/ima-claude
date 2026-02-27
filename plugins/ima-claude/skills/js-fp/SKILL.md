---
name: "js-fp"
description: "Core FP principles with anti-over-engineering focus - Simple > Complex | Evidence > Assumptions"
---

# JavaScript Functional Programming

Core functional programming principles for JavaScript with anti-over-engineering enforcement. This skill provides error-preventing essentials and references to deep-dive content.

## When to Use This Skill

- Implementing pure, testable functions
- Need FP architectural guidance
- Preventing over-engineering and custom FP utility creation
- Comprehensive testing strategies
- Evidence-based performance optimization

## ⚠️ CRITICAL: Anti-Over-Engineering (PRIMARY FOCUS)

**Core Principle**: "Simple > Complex | Evidence > Assumptions"

> **Clarification**: This skill prevents CREATING custom FP utility functions (pipe, compose, curry) to make JavaScript "feel" like Haskell. Using established libraries (lodash, date-fns, etc.) is perfectly fine. FP is a mindset—pure functions, immutability, composition—not a rigid API signature.

### Don't Create Custom FP Utilities

```javascript
// ❌ DON'T CREATE: pipe() utility
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x)

// ✅ INSTEAD: Native function calls with early returns
const validateUser = (userData) => {
  const requiredCheck = validateRequired(['email', 'name'])(userData)
  if (!requiredCheck.valid) return requiredCheck

  const emailCheck = validateEmail(userData)
  if (!emailCheck.valid) return emailCheck

  return validateNameLength(userData)
}

// ❌ DON'T CREATE: compose() utility
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x)

// ✅ INSTEAD: Direct function calls
const processData = (raw) => {
  const normalized = normalize(raw)
  const validated = validate(normalized)
  return transform(validated)
}

// ❌ DON'T CREATE: curry() utility
const curry = (fn) => (...args) => args.length >= fn.length
  ? fn(...args)
  : (...more) => curry(fn)(...args, ...more)

// ✅ INSTEAD: Native closures and function factories
const createValidator = (rules) => (value) => {
  const errors = rules.filter(rule => !rule.validator(value))
  return errors.length === 0 ? { valid: true } : { valid: false, errors }
}

// ❌ DON'T CREATE: Custom monads
class Maybe { /* complex monad implementation */ }

// ✅ INSTEAD: Native error handling and conditionals
const getUser = async (id) => {
  try {
    const user = await fetchUser(id)
    return { success: true, data: user }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

### Context-Appropriate Complexity

```javascript
// CLI Script: Simple and direct
const processFile = (filePath) => {
  const data = readFileSync(filePath, 'utf8')
  const lines = data.split('\n').filter(line => line.trim())
  return lines.map(line => line.toUpperCase())
}

// Production Service: Appropriate error handling
const processFile = async (filePath, logger) => {
  try {
    const data = await readFile(filePath, 'utf8')
    const lines = data.split('\n').filter(line => line.trim())
    logger.info('File processed', { filePath, lineCount: lines.length })
    return { success: true, data: lines.map(line => line.toUpperCase()) }
  } catch (error) {
    logger.error('File processing failed', { filePath, error })
    return { success: false, error: error.message }
  }
}

// Big Data System: Performance optimization with evidence
const createFileProcessor = (config) => {
  // Pre-compile expensive transformations
  const transformers = config.transforms.map(compileTransformer)

  return async (filePath, logger) => {
    const stream = createReadStream(filePath)
    return processStream(stream, transformers, logger)
  }
}
```

## Core FP Patterns (Error-Preventing Essentials)

### 1. Purity and Side Effect Isolation

**Rule**: Separate business logic from side effects.

```javascript
// ❌ Impure - side effects mixed with logic
function calculateTotal(items) {
  console.log('Processing items') // Side effect
  total += items.reduce((sum, item) => sum + item.price, 0) // Mutation
  return total
}

// ✅ Pure business logic
const calculateTotal = (items) =>
  items.reduce((sum, item) => sum + item.price, 0)

// ✅ Side effects isolated
const logAndCalculate = (items, logger) => {
  const total = calculateTotal(items) // Pure calculation
  logger.log(`Total: ${total}`) // Side effect isolated
  return total
}
```

**Benefits**:
- 100% testable with all edge cases
- Predictable behavior and debugging
- Safe for parallel execution
- Enables optimization through memoization

### 2. Composition Over Inheritance

**Rule**: Build complex behavior from simple functions.

```javascript
// ❌ Class hierarchy approach
class BaseValidator {
  validate() { throw new Error('Not implemented') }
}
class EmailValidator extends BaseValidator {
  validate(value) { /* email logic */ }
}

// ✅ Function composition (no utilities needed)
const validateRequired = (value) => value != null && value !== ''
const validateEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
const validateLength = (min, max) => (value) =>
  value.length >= min && value.length <= max

// Simple composition without pipe() utility
const validateUserEmail = (email) => {
  if (!validateRequired(email)) return { valid: false, error: 'Required' }
  if (!validateEmail(email)) return { valid: false, error: 'Invalid email' }
  if (!validateLength(5, 100)(email)) return { valid: false, error: 'Length' }
  return { valid: true }
}
```

### 3. Dependency Injection Through Parameters

**Rule**: Pass dependencies explicitly, avoid global state.

```javascript
// ❌ Hidden dependencies, hard to test
function saveUser(userData) {
  const hashedPassword = bcrypt.hash(userData.password) // Hidden
  return database.save({ ...userData, password: hashedPassword }) // Hidden
}

// ✅ Explicit dependencies, fully testable
const saveUser = async (userData, hasher, database) => {
  const hashedPassword = await hasher.hash(userData.password)
  return database.save({ ...userData, password: hashedPassword })
}

// ✅ Function factory for repeated use
const createUserService = (hasher, database) => ({
  saveUser: (userData) => saveUser(userData, hasher, database),
  findUser: (id) => database.findById(id)
})
```

### 4. Immutability Patterns

**Rule**: Avoid mutations, create new objects/arrays.

```javascript
// ❌ Mutation approach
function updateUserSettings(user, settings) {
  user.settings = { ...user.settings, ...settings } // Mutates user
  user.updatedAt = new Date()
  return user
}

// ✅ Immutable approach
const updateUserSettings = (user, settings) => ({
  ...user,
  settings: { ...user.settings, ...settings },
  updatedAt: new Date()
})

// ✅ Array operations without mutation
const addItem = (items, newItem) => [...items, newItem]
const removeItem = (items, id) => items.filter(item => item.id !== id)
const updateItem = (items, id, updates) =>
  items.map(item => item.id === id ? { ...item, ...updates } : item)
```

## Testing Essentials (Enabled by Purity)

**Philosophy**: Pure functions enable testing all edge cases systematically.

```javascript
// Traditional testing (limited coverage)
describe('calculateDiscount', () => {
  it('should calculate 10% discount', () => {
    expect(calculateDiscount(100, 0.1)).toBe(10)
  })
})

// FP comprehensive testing (all edge cases)
describe('calculateDiscount - FP Comprehensive', () => {
  describe('valid inputs', () => {
    const testCases = [
      [100, 0.1, 10],
      [50, 0.2, 10],
      [0, 0.1, 0]
    ]

    testCases.forEach(([price, rate, expected]) => {
      it(`${rate*100}% discount on ${price} = ${expected}`, () => {
        expect(calculateDiscount(price, rate)).toBe(expected)
      })
    })
  })

  describe('all data types - systematic edge cases', () => {
    const invalidTypes = [null, undefined, NaN, true, [], {}, '100']

    invalidTypes.forEach(input => {
      it(`handles ${typeof input} gracefully`, () => {
        expect(() => calculateDiscount(input, 0.1)).not.toThrow()
        expect(calculateDiscount(input, 0.1)).toBe(0)
      })
    })
  })
})
```

## Performance Patterns (Evidence-Based)

**⚠️ IMPORTANT**: Optimize only when needed with evidence.

### Configuration Pre-Compilation (When Actually Needed)

**Use When**: Processing large datasets (>10K items) with repeated configuration access.

```javascript
// Problem: O(records × fields) complexity
function processRecords(records, schema) {
  return records.map(record => {
    return schema.fields.reduce((obj, field) => { // ← Repeated config access
      obj[field.name] = transformField(record[field.name], field.type)
      return obj
    }, {})
  })
}

// Solution: O(records + fields) - pre-compile configuration
function createRecordProcessor(schema) {
  // Setup once - extract expensive configuration
  const fieldProcessors = schema.fields.map(field =>
    value => transformField(value, field.type)
  )

  return record => fieldProcessors.reduce((obj, processor, i) => {
    obj[schema.fields[i].name] = processor(record[schema.fields[i].name])
    return obj
  }, {})
}

// Usage: Configuration cost paid once
const processor = createRecordProcessor(schema) // Setup phase
const results = records.map(processor) // Linear execution
```

### Function Factories for Reusable Logic

```javascript
// Create specialized functions instead of generic ones
const createValidator = (rules) => (value) => {
  const errors = []
  for (const rule of rules) {
    if (!rule.validator(value)) {
      errors.push(rule.message)
    }
  }
  return errors.length === 0 ? { valid: true } : { valid: false, errors }
}

// Usage: Configure once, use many times
const validateEmail = createValidator([
  { validator: v => typeof v === 'string', message: 'Must be string' },
  { validator: v => v.includes('@'), message: 'Must contain @' },
  { validator: v => v.length > 5, message: 'Too short' }
])
```

## Language-Specific Idioms

### Native JavaScript Patterns

```javascript
// Native array methods over loops
const processUsers = (users) =>
  users
    .filter(user => user.active)
    .map(user => ({ ...user, displayName: `${user.firstName} ${user.lastName}` }))
    .sort((a, b) => a.lastName.localeCompare(b.lastName))

// Native async/await over callbacks
const fetchUserData = async (userId, fetcher) => {
  try {
    const user = await fetcher.getUser(userId)
    const preferences = await fetcher.getPreferences(userId)
    return { ...user, preferences }
  } catch (error) {
    return { error: error.message }
  }
}

// WeakMap for performance when appropriate
const createMemoized = () => {
  const cache = new WeakMap()
  return (obj, computeFn) => {
    if (cache.has(obj)) return cache.get(obj)
    const result = computeFn(obj)
    cache.set(obj, result)
    return result
  }
}
```

## Quality Gates (Pre-Implementation Checklist)

1. **"Can this be pure?"** → Separate business logic from side effects
2. **"Can this use native patterns?"** → Avoid creating custom FP utilities, use language features
3. **"Can this be simplified?"** → Choose simple solution over complex abstraction
4. **"Is this complexity justified?"** → Evidence-based complexity decisions
5. **"Is this testable?"** → Pure functions enable comprehensive testing
6. **"Is this context-appropriate?"** → CLI script ≠ production service ≠ big data system

## When to Load Additional Content

### Deep Principles and Explanations
**File**: `core-principles.md` (~800 lines)
**When**: Learning mode, explaining WHY, architectural decisions
**Contains**: Complete FP philosophy, detailed pattern explanations, cross-pattern comparisons

### Comprehensive Anti-Patterns
**File**: `anti-patterns.md` (~400 lines)
**When**: Code review, preventing specific mistakes, team training
**Contains**: Exhaustive anti-patterns, common mistakes, migration strategies

### Testing Methodology
**File**: `testing-patterns.md` (~500 lines)
**When**: Building test suites, improving coverage, edge case analysis
**Contains**: Full testing strategies, edge case patterns, property-based testing

### Performance Deep-Dive
**File**: `performance-patterns.md` (~400 lines)
**When**: Performance issues identified, optimization needed, benchmarking
**Contains**: Detailed optimization strategies, profiling techniques, benchmarking patterns

### Working Examples
**Directory**: `examples/`
**When**: Learning implementation, need working code, integration examples
**Contains**: Complete working examples with tests

## Integration with Domain Skills

This core skill provides the foundation for domain-specific skills:

- **js-fp-api**: Node.js API patterns with FP principles
- **js-fp-react**: React component patterns with FP principles
- **js-fp-vue**: Vue.js component patterns with FP principles
- **js-fp-wordpress**: WordPress patterns with FP principles

Each domain skill references this core and adds domain-specific patterns.

## Common Use Cases

### Data Validation
```javascript
const createValidationRules = (schema) => {
  const rules = schema.map(rule => ({
    field: rule.field,
    validator: compileValidator(rule.type, rule.options),
    message: rule.message
  }))

  return (data) => {
    const errors = []
    for (const rule of rules) {
      if (!rule.validator(data[rule.field])) {
        errors.push({ field: rule.field, message: rule.message })
      }
    }
    return errors.length === 0 ? { valid: true } : { valid: false, errors }
  }
}
```

### Data Transformation
```javascript
// Pipeline without utilities - native chaining
const processUserData = (rawData) => {
  const normalized = normalizeUserData(rawData)
  if (!normalized.valid) return normalized

  const validated = validateUserData(normalized.data)
  if (!validated.valid) return validated

  const enhanced = enhanceWithDefaults(validated.data)
  return { valid: true, data: enhanced }
}
```

## Success Metrics

### Code Quality
- **Simplicity**: Readable, maintainable code over clever solutions
- **Testability**: 100% testable pure functions with edge case coverage
- **Native Integration**: Uses language features effectively
- **Context-Appropriate**: Matches complexity to actual requirements

### Performance (When Needed)
- **Evidence-Based**: Optimizations backed by measurements
- **Appropriate Scale**: Simple solutions for small/medium data
- **Native Optimization**: Leverages language/runtime optimizations
- **Avoid Over-Engineering**: No complex monitoring for simple apps

### Maintainability
- **Predictable Patterns**: Consistent FP approaches
- **Easy Testing**: Comprehensive test coverage enabled by purity
- **Simple Maintenance**: Easy to understand and modify
- **Documentation**: Clear examples and usage patterns

## Philosophy

*"Pure functions, native language patterns, appropriate complexity, and comprehensive testing for maintainable, predictable code that respects the language and solves real problems simply."*
