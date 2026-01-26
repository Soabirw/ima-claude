---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Grep, TodoWrite, Task]
description: "Core functional programming principles and patterns - standalone or referenced by personas"
---

# /fp:core - Functional Programming Core Principles

## Purpose
Core functional programming principles, patterns, and anti-patterns that can be used standalone or referenced by AI personas when FP guidance is needed for specific tasks.

## Usage
```
/fp:core [--focus principles|patterns|anti-patterns|testing] [--lang javascript|php|python|rust] [--examples]
```

## Arguments  
- `--focus` - Specific area of FP guidance (principles, patterns, anti-patterns, testing)
- `--lang` - Language-specific examples and idioms
- `--examples` - Include comprehensive code examples
- `--standalone` - Use as complete FP reference without persona integration

## ⚠️ CRITICAL: Anti-Over-Engineering Foundation

**PRIMARY PRINCIPLE**: "Simple solutions > Complex abstractions | Native patterns > FP utilities | MVP > Enterprise patterns"

### Universal Anti-Patterns (NEVER CREATE)
- ❌ **pipe() utilities** → Use native function calls and early returns
- ❌ **compose() utilities** → Use direct function calls in sequence  
- ❌ **curry() utilities** → Use native closures and function factories
- ❌ **Custom monads** → Use native error handling patterns
- ❌ **FP utility libraries** → Use native language features
- ❌ **Complex performance monitoring** → Simple solutions for small data
- ❌ **Enterprise patterns for simple scripts** → Match complexity to need

### Preferred Native Patterns
- ✅ **Native function calls** → Zero overhead, JIT-optimizable
- ✅ **Language idioms** → Array methods, conditionals, native async
- ✅ **Simple composition** → Function factories without utilities
- ✅ **Evidence-based complexity** → Only add complexity when proven needed
- ✅ **Context-appropriate quality** → CLI script ≠ production service

## Core FP Principles

### 1. Purity and Side Effect Management

**Definition**: Functions that produce the same output for the same input without side effects.

```javascript
// ❌ Impure - has side effects
function calculateTotal(items) {
    console.log('Processing items') // Side effect
    total += items.reduce((sum, item) => sum + item.price, 0) // Mutation
    return total
}

// ✅ Pure - no side effects, testable, predictable
const calculateTotal = (items) => 
    items.reduce((sum, item) => sum + item.price, 0)

// ✅ Separate side effects from business logic
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

**Definition**: Build complex behavior from simple functions rather than class hierarchies.

```javascript
// ❌ Class hierarchy approach
class BaseValidator {
    validate() { throw new Error('Not implemented') }
}
class EmailValidator extends BaseValidator {
    validate(value) { /* email logic */ }
}

// ✅ Function composition approach  
const validateRequired = (value) => value != null && value !== ''
const validateEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
const validateLength = (min, max) => (value) => 
    value.length >= min && value.length <= max

// Simple composition without utilities
const validateUserEmail = (email) => {
    if (!validateRequired(email)) return { valid: false, error: 'Required' }
    if (!validateEmail(email)) return { valid: false, error: 'Invalid email' }
    if (!validateLength(5, 100)(email)) return { valid: false, error: 'Length' }
    return { valid: true }
}
```

### 3. Dependency Injection Through Parameters

**Definition**: Pass dependencies as parameters instead of using global state or complex DI frameworks.

```javascript
// ❌ Hidden dependencies, hard to test
function saveUser(userData) {
    const hashedPassword = bcrypt.hash(userData.password) // Hidden dependency
    return database.save({ ...userData, password: hashedPassword }) // Hidden dependency
}

// ✅ Explicit dependencies, fully testable
const saveUser = async (userData, hasher, database) => {
    const hashedPassword = await hasher.hash(userData.password)
    return database.save({ ...userData, password: hashedPassword })
}

// ✅ Function factory pattern for repeated use
const createUserService = (hasher, database) => ({
    saveUser: (userData) => saveUser(userData, hasher, database),
    findUser: (id) => database.findById(id)
})
```

### 4. Immutability Patterns

**Definition**: Avoid mutations, create new objects/arrays instead.

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

## Performance Patterns (MVP-First, Evidence-Based)

**⚠️ IMPORTANT**: Performance optimization should be:
- **Evidence-based**: Measure first, optimize only when needed
- **Context-appropriate**: Most apps are small data, don't need complex monitoring
- **MVP-first**: Simple solutions work for 90% of use cases
- **Nice-to-have enhancement**: Not primary focus unless dealing with big data

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

## Comprehensive Testing (Enabled by Purity)

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
            it(`should calculate ${rate*100}% discount on ${price}`, () => {
                expect(calculateDiscount(price, rate)).toBe(expected)
            })
        })
    })
    
    describe('all data types - systematic edge cases', () => {
        const invalidTypes = [null, undefined, NaN, true, [], {}, '100', 'invalid']
        
        invalidTypes.forEach(input => {
            it(`should handle ${typeof input} gracefully`, () => {
                expect(() => calculateDiscount(input, 0.1)).not.toThrow()
                expect(calculateDiscount(input, 0.1)).toBe(0) // or appropriate default
            })
        })
    })
})
```

## Language-Specific Idioms

### JavaScript/Node.js
```javascript
// Native array methods over loops
const processUsers = (users) => 
    users
        .filter(user => user.active)
        .map(user => ({ ...user, displayName: user.firstName + ' ' + user.lastName }))
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

### React-Specific Patterns  
```javascript
// Pure custom hook pattern
const useUserLogic = (userData, config) => {
    const displayData = useMemo(() => ({
        ...userData,
        displayName: userData.name.trim(),
        shouldShowEmail: config.showEmail && userData.email
    }), [userData, config])
    
    const handleAction = useCallback((action) => ({
        type: 'USER_ACTION', 
        payload: { userId: userData.id, action }
    }), [userData.id])
    
    return { displayData, handleAction }
}

// Pure component with memo
const UserCard = memo(({ userData, config, onAction }) => {
    const { displayData, handleAction } = useUserLogic(userData, config)
    
    const handleClick = useCallback(() => {
        const action = handleAction('view')
        onAction?.(action)
    }, [handleAction, onAction])
    
    return (
        <div onClick={handleClick}>
            <h3>{displayData.displayName}</h3>
            {displayData.shouldShowEmail && <p>{displayData.email}</p>}
        </div>
    )
})
```

## Quality Gates and Decision Framework

### Pre-Implementation Questions
1. **"Can this be pure?"** - Separate business logic from side effects
2. **"Can this use native patterns?"** - Avoid utility creation, use language features
3. **"Can this be simplified?"** - Choose simple solution over complex abstraction  
4. **"Is this complexity justified?"** - Evidence-based complexity decisions
5. **"Is this testable?"** - Pure functions enable comprehensive testing

### Validation Checklist
- ✅ **Anti-Utility**: No pipe/compose/curry utilities created
- ✅ **Purity**: Side effects minimized and isolated  
- ✅ **Simplicity**: Simplest solution that meets requirements
- ✅ **Native**: Works with language strengths, not against them
- ✅ **Context-Appropriate**: CLI script ≠ production service ≠ big data system
- ✅ **Testable**: Easy to test with comprehensive edge cases
- ✅ **Composable**: Can be built from simple functions without utilities

## Common Use Cases

### Data Validation
```javascript
// Function factory approach
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

### API Endpoint Logic
```javascript
// Pure business logic + dependency injection
const createUserHandler = (validator, hasher, database) => async (ctx) => {
    const validation = validator(ctx.request.body)
    if (!validation.valid) {
        return ctx.json({ errors: validation.errors }, 400)
    }
    
    try {
        const hashedPassword = await hasher.hash(validation.data.password)
        const user = await database.save({
            ...validation.data,
            password: hashedPassword,
            createdAt: new Date()
        })
        
        return ctx.json({ user: { ...user, password: undefined } }, 201)
    } catch (error) {
        return ctx.json({ error: 'Failed to create user' }, 500)
    }
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

## Integration with AI Personas

This core can be referenced by AI personas when they need FP guidance:

- **`--persona-functional`**: Uses full core reference for FP-focused tasks
- **`--persona-architect`**: References composition and design patterns
- **`--persona-backend`**: Uses dependency injection and API patterns  
- **`--persona-frontend`**: References React patterns and component design
- **`--persona-analyzer`**: Uses purity analysis and testing patterns
- **`--persona-performance`**: Uses evidence-based optimization patterns

## Philosophy

*"Pure functions, native language patterns, appropriate complexity, and comprehensive testing for maintainable, predictable code that respects the language and solves real problems simply."*