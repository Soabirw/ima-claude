---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, TodoWrite, Task]
description: "Implement features using functional programming patterns with SuperClaude persona integration"
---

# /fp:implement - Functional Programming Implementation

## Purpose
Implement features using functional programming patterns while preventing over-engineering through FP constraints and decision frameworks.

## Usage
```
/fp:implement [feature] [--type component|api|service|function] [--lang javascript|php|python|rust] [--hot-path] [--benchmark]
```

## Arguments
- `feature` - Feature or functionality to implement
- `--type` - Implementation type (component, api, service, function, validator)  
- `--lang` - Target implementation language
- `--hot-path` - Apply hot path performance patterns specifically
- `--benchmark` - Generate performance benchmarks vs traditional approaches
- `--with-tests` - Include comprehensive edge-case testing

## FP Implementation Framework

### ⚠️ CRITICAL: Anti-Utility Creation Guidelines

**NEVER CREATE**: pipe(), compose(), curry(), or other FP utilities. Use native language patterns instead.

**SPIRIT-BASED APPROACH**:
- Pure functions using native syntax
- Composition through native function calls and early returns
- Dependency injection through parameters
- Performance optimization through native language features

### Pre-Implementation Analysis
1. **Purity Assessment**: Can this be implemented as pure functions using native patterns?
2. **Native Composition**: Can this be built using native function calls and language idioms?
3. **Pre-Compilation Potential**: Are there expensive operations that can be pre-compiled using closures?
4. **Performance Patterns**: Does this leverage native language performance characteristics?
5. **Anti-Utility Check**: Are we avoiding FP utility creation and working WITH the language?

### Core FP Implementation Patterns

#### 1. Function Factory Pattern
```javascript
// Create customized functions instead of classes
export const createValidator = (rules) => (value) => 
    rules.every(rule => rule(value))

// Usage: Configuration happens once, execution is optimized
const validateEmail = createValidator([
    val => typeof val === 'string',
    val => val.includes('@'),
    val => val.length > 5
])
```

#### 2. Hot Path Configuration Pre-Compilation Pattern  
```javascript
// Extract configuration from hot paths
export const createRecordMapper = (schema) => {
    // Pre-compile field transformers (cached in closure)
    const transformers = schema.fields.reduce((acc, field) => {
        acc[field.name] = field.formatter || (val => val)
        return acc
    }, {})
    
    // Return optimized mapper
    return (record) => {
        const entity = {}
        Object.keys(transformers).forEach(name => {
            entity[name] = transformers[name](record[`${schema.prefix}_${name}`])
        })
        return entity
    }
}
```

#### 3. Native Error Handling (Railway-Oriented Spirit)
```javascript
// Keep business logic on happy path using native error handling - NO pipe() utility
export const processUser = async (userData, ctx) => {
    try {
        // Native function composition with early returns
        const validatedUser = validateUserData(userData)
        if (!validatedUser.valid) {
            return { success: false, error: validatedUser.error }
        }
        
        const savedUser = await saveUser(validatedUser.data, ctx)
        if (!savedUser) {
            return { success: false, error: 'Failed to save user' }
        }
        
        const authToken = await generateToken(savedUser, ctx)
        return { success: true, user: savedUser, token: authToken }
    } catch (error) {
        return { success: false, error: error.message }
    }
}

// Alternative: Use native async/await with Result pattern (no custom monads)
export const processUserWithResults = async (userData, ctx) => {
    const validationResult = validateUserData(userData)
    if (!validationResult.success) return validationResult
    
    const saveResult = await saveUser(validationResult.data, ctx)
    if (!saveResult.success) return saveResult
    
    const tokenResult = await generateToken(saveResult.data, ctx)
    return tokenResult.success 
        ? { success: true, user: saveResult.data, token: tokenResult.data }
        : tokenResult
}
```

## SuperClaude Integration

**Automatic Delegation**:
- Routes to `/sc:implement` with FP principle injection
- Coordinates with `/sc:build` for build system integration
- Integrates with `/sc:test` for comprehensive testing approaches

**FP Seeding for SuperClaude Personas**:
```yaml
fp_seeding:
  anti_patterns:
    - "NEVER create pipe(), compose(), curry() or FP utilities"
    - "NEVER force pure FP patterns that fight the language"
    - "NEVER create custom monads or complex abstractions"
    
  principles:
    - "Use native language patterns to express FP principles"
    - "Prefer pure functions with native syntax"
    - "Use function factories for reusable logic with closures"  
    - "Extract configuration from execution paths using native features"
    - "Apply comprehensive edge-case testing"
    
  constraints:
    - "Respect language native capabilities and performance characteristics"
    - "Avoid side effects in business logic using native error handling"
    - "Pre-compile expensive operations using closures, not utilities"
    - "Choose native composition over utility-based composition"
    - "Test all data types systematically"
```

## Execution Flow

1. **Analyze Feature Requirements**: Apply FP lens to understand implementation approach
2. **Seed SC:Implement**: Inject hot path performance patterns and FP constraints
3. **Generate Implementation**: Create code using functional patterns
4. **Performance Review**: Identify pre-compilation opportunities  
5. **Comprehensive Testing**: Generate edge-case test coverage
6. **Simplicity Validation**: Ensure solution isn't over-engineered

## Language-Specific Implementations

### JavaScript Implementation  
```javascript
// Modern JavaScript with native functional patterns - NO utilities
export const createApiHandler = (config) => {
    // Pre-compile validation and transformation logic using native closures
    const validators = compileValidators(config.validation)
    const transformers = compileTransformers(config.transforms)
    
    return async (request, context) => {
        // Native composition with early returns
        const validationResult = validators(request.body)
        if (!validationResult.valid) {
            return { success: false, error: validationResult.error }
        }
        
        const transformationResult = transformers(validationResult.data)
        if (!transformationResult.valid) {
            return { success: false, error: transformationResult.error }
        }
        
        try {
            const result = await processData(transformationResult.data, context)
            return { success: true, data: result }
        } catch (error) {
            return { success: false, error: error.message }
        }
    }
}
```

### PHP Implementation
```php
// Modern PHP functional patterns
function createApiHandler(array $config): Closure {
    // Pre-compile logic using closure variables
    $validators = compileValidators($config['validation']);
    $transformers = compileTransformers($config['transforms']);
    
    return function(array $request, array $context) use ($validators, $transformers) {
        $validatedData = $validators($request['body']);
        $transformedData = $transformers($validatedData);
        $result = processData($transformedData, $context);
        return ['success' => true, 'data' => $result];
    };
}
```

### Python Implementation
```python
from functools import partial, lru_cache
from typing import Callable, Dict, Any

def create_api_handler(config: Dict[str, Any]) -> Callable:
    # Pre-compile logic with decorators and closures
    validators = compile_validators(config['validation'])
    transformers = compile_transformers(config['transforms'])
    
    @lru_cache(maxsize=None)
    def handler(request_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = validators(request_data)
        transformed_data = transformers(validated_data)
        result = process_data(transformed_data, context)
        return {'success': True, 'data': result}
    
    return handler
```

### Rust Implementation
```rust
// Zero-cost abstractions with compile-time optimization
use std::sync::Arc;

pub fn create_api_handler<T>(config: Config) -> impl Fn(Request, Context) -> Result<T, Error> 
where 
    T: Clone + Send + 'static,
{
    // Compile-time configuration capture
    let validators = compile_validators(config.validation);
    let transformers = compile_transformers(config.transforms);
    
    move |request: Request, context: Context| -> Result<T, Error> {
        let validated_data = validators(request.body)?;
        let transformed_data = transformers(validated_data)?;
        let result = process_data(transformed_data, context)?;
        Ok(result)
    }
}
```

## Performance Benchmarking

When `--benchmark` flag is used, automatically generate:

```javascript
// Benchmark template for validation
function benchmarkImplementation() {
    const testData = generateTestData(10000)
    
    console.time('Traditional Approach')
    const result1 = testData.map(traditionalImplementation)
    console.timeEnd('Traditional Approach')
    
    console.time('FP Approach - Setup')
    const fpImplementation = createFpImplementation(config)
    console.timeEnd('FP Approach - Setup')
    
    console.time('FP Approach - Execution')
    const result2 = testData.map(fpImplementation)  
    console.timeEnd('FP Approach - Execution')
    
    // Validate equivalence
    assert.deepEqual(result1, result2)
    return { traditional: result1.length, fp: result2.length, improvement: 'X% faster' }
}
```

## Comprehensive Testing Strategy

Automatically generate test coverage for:

```javascript
describe('FP Implementation', () => {
    describe('valid inputs', () => {
        // Test expected use cases
    })
    
    describe('all data types', () => {
        // Test against ALL language data types - only practical with pure functions
        const invalidTypes = [null, undefined, NaN, true, false, [], {}, 'string', 123]
        invalidTypes.forEach(type => {
            it(`should handle ${typeof type} gracefully`, () => {
                expect(() => fpFunction(type)).not.toThrow()
            })
        })
    })
    
    describe('edge cases', () => {
        // Boundary values, empty inputs, extreme values
    })
    
    describe('composition', () => {
        // Test function combinations
    })
})
```

## Quality Gates

- **Anti-Utility Check**: Are we avoiding FP utility creation and using native patterns?
- **Language Respect**: Are we working WITH the language's strengths, not against them?
- **Purity Check**: Are side effects minimized and isolated using native error handling?
- **Performance Check**: Are expensive operations pre-compiled using native features?  
- **Simplicity Check**: Is this the simplest approach that meets requirements?
- **Testability Check**: Can this be comprehensively tested with all data types?
- **Native Composition Check**: Can this be combined with other functions using language idioms?
