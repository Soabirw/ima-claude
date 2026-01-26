---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite]
description: "Diagnose and resolve issues through functional programming analysis, focusing on purity, performance, and composition problems"
---

# /fp:troubleshoot - Functional Programming Issue Diagnosis

## Purpose
Systematically diagnose and resolve issues in functional programming code, focusing on purity violations, performance bottlenecks, composition problems, and anti-pattern detection.

## Usage
```
/fp:troubleshoot [issue] [--type performance|purity|composition|pattern] [--lang javascript|php|python|rust] [--trace]
```

## Arguments
- `issue` - Description of the problem, error message, or performance concern
- `--type` - Issue category (performance, purity, composition, pattern)
- `--lang` - Target language for language-specific debugging
- `--trace` - Enable detailed analysis and debugging output
- `--benchmark` - Include performance measurements and comparisons
- `--fix` - Automatically apply safe FP transformations
- `--examples` - Provide before/after transformation examples

## FP Troubleshooting Framework

### 1. Performance Issue Diagnosis

#### Hot Path Configuration Access Detection
```javascript
// PROBLEM: Performance degradation in data processing
function slowProcessor(records, config) {
    return records.map(record => {
        // Configuration accessed per record - O(records × config)
        const rules = config.validation.rules
        const transforms = config.processing.transforms
        return processRecord(record, rules, transforms)
    })
}

// DIAGNOSIS: Configuration access in hot path
// IMPACT: O(records × configuration_size) complexity
// SOLUTION: Pre-compile configuration outside the loop
```

#### Memory Leak Detection in Closures
```javascript
// PROBLEM: Memory usage growing over time
function createProcessors(configs) {
    return configs.map(config => {
        const heavyData = loadLargeDataset(config) // ← Retained in closure
        return (record) => processWithHeavyData(record, heavyData)
    })
}

// DIAGNOSIS: Closures retaining large objects
// IMPACT: Memory grows linearly with processor count
// SOLUTION: Use WeakMap or external caching strategy
```

### 2. Purity Issue Diagnosis

#### Side Effect Detection
```javascript
// PROBLEM: Unpredictable behavior and testing difficulties
function processUser(user) {
    console.log(`Processing ${user.name}`) // ← Side effect
    user.processed = true                  // ← Mutation
    user.timestamp = Date.now()            // ← Non-deterministic
    return saveToDatabase(user)            // ← Side effect
}

// DIAGNOSIS: Multiple purity violations
// IMPACT: Untestable, unpredictable, hard to debug
// SOLUTION: Extract pure business logic
```

#### Mutation Detection and Resolution
```php
// PROBLEM: Data corruption in concurrent processing
function updateUserStats(array &$users): array {
    foreach ($users as &$user) {
        $user['score'] += calculateBonus($user); // ← Mutation
        $user['rank'] = determineRank($user);    // ← Mutation
    }
    return $users;
}

// DIAGNOSIS: In-place mutations causing race conditions
// IMPACT: Data corruption in concurrent environments
// SOLUTION: Return new array with updated values
```

### 3. Composition Issue Diagnosis

#### Composition Complexity Problems
```javascript
// PROBLEM: Deep nesting and error handling complexity
function validateAndSaveUser(userData) {
    try {
        if (validateEmail(userData.email)) {
            if (validatePassword(userData.password)) {
                if (validateAge(userData.age)) {
                    const user = transformUser(userData)
                    return saveUser(user)
                } else {
                    throw new Error('Invalid age')
                }
            } else {
                throw new Error('Invalid password')
            }
        } else {
            throw new Error('Invalid email')
        }
    } catch (error) {
        logError(error)
        throw error
    }
}

// DIAGNOSIS: Callback hell in validation chain
// IMPACT: Hard to maintain, test, and extend
// SOLUTION: Function composition with early returns
```

#### Error Handling in Composition
```python
# PROBLEM: Exceptions breaking composition flow
def process_data_pipeline(data):
    try:
        validated = validate_data(data)
        transformed = transform_data(validated)
        enriched = enrich_data(transformed)
        return save_data(enriched)
    except ValidationError as e:
        # Different error types need different handling
        log_validation_error(e)
        return None
    except TransformError as e:
        log_transform_error(e)
        return None

# DIAGNOSIS: Exception handling scattered across pipeline
# IMPACT: Complex error recovery and unclear flow
# SOLUTION: Result/Either pattern for error composition
```

### 4. Anti-Pattern Detection

#### Over-Engineering Detection
```javascript
// PROBLEM: Complex utility creation for simple operations
class FunctionalPipelineBuilder {
    constructor() {
        this.operations = []
    }
    
    pipe(fn) {
        this.operations.push(fn)
        return this
    }
    
    execute(input) {
        return this.operations.reduce((acc, op) => op(acc), input)
    }
}

// DIAGNOSIS: Over-engineered utility for simple composition
// IMPACT: Unnecessary complexity, performance overhead
// SOLUTION: Use native language features
```

#### Utility Anti-Pattern Resolution
```javascript
// PROBLEM: Performance degradation from FP utilities
const pipe = (...fns) => (input) => fns.reduce((acc, fn) => fn(acc), input)

const processUser = pipe(
    validateUser,
    sanitizeUser,
    enrichUser,
    saveUser
)

// DIAGNOSIS: Utility overhead for simple composition
// IMPACT: Function call overhead, stack depth, debugging complexity
// SOLUTION: Direct composition or early returns
```

## SuperClaude Integration

**Enhanced SC:Troubleshoot**: Routes to `/sc:troubleshoot` with FP diagnostic seeding

**FP Diagnostic Enhancement**:
```yaml
fp_troubleshooting_seeding:
  performance_diagnostics:
    - "Scan for configuration access in hot paths"
    - "Detect O(n²) complexity patterns"
    - "Identify closure memory retention issues"
    - "Find pre-compilation opportunities"
    
  purity_diagnostics:
    - "Identify side effects and mutations"
    - "Detect non-deterministic behavior"
    - "Find testing and debugging difficulties"
    - "Suggest pure function extraction"
    
  composition_diagnostics:
    - "Detect deep nesting and callback hell"
    - "Find error handling complexity"
    - "Identify composition opportunities"
    - "Suggest early return patterns"
    
  anti_pattern_diagnostics:
    - "Detect over-engineering and utility creation"
    - "Find complex abstractions for simple problems"
    - "Identify performance overhead from utilities"
    - "Suggest native language alternatives"
```

## Diagnostic Workflow

### 1. Issue Classification Phase
- **Performance Issues**: Slow execution, memory leaks, scalability problems
- **Purity Issues**: Side effects, mutations, non-deterministic behavior
- **Composition Issues**: Complex nesting, error handling, flow control
- **Anti-Pattern Issues**: Over-engineering, utility creation, complex abstractions

### 2. Analysis Phase
- **Code Scanning**: Identify patterns and anti-patterns
- **Performance Profiling**: Measure execution time and memory usage
- **Purity Analysis**: Detect side effects and mutations
- **Composition Analysis**: Map data flow and error paths

### 3. Root Cause Identification Phase
- **Hot Path Analysis**: Find expensive operations in loops
- **Side Effect Mapping**: Trace impure operations and their impact
- **Complexity Assessment**: Measure cognitive and computational complexity
- **Pattern Recognition**: Identify known FP anti-patterns

### 4. Solution Generation Phase
- **Optimization Strategies**: Pre-compilation, caching, memoization
- **Purity Transformations**: Extract pure functions, isolate side effects
- **Composition Refactoring**: Simplify control flow, improve error handling
- **Anti-Pattern Resolution**: Replace complex utilities with simple patterns

## Diagnostic Examples

### Performance Issue Resolution
```javascript
// BEFORE: Slow performance (O(records × fields))
function processRecords(records, schema) {
    return records.map(record => {
        return schema.fields.reduce((obj, field) => {
            obj[field.name] = transformField(record[field.name], field.type)
            return obj
        }, {})
    })
}

// DIAGNOSIS: Configuration access in hot path
// PERFORMANCE IMPACT: 8.2s for 100K records

// AFTER: Hot path optimization (O(records + fields))
function createOptimizedProcessor(schema) {
    // Pre-compile field processors
    const fieldProcessors = schema.fields.map(field => 
        record => transformField(record[field.name], field.type)
    )
    
    return records => records.map(record => {
        const result = {}
        fieldProcessors.forEach((processor, index) => {
            result[schema.fields[index].name] = processor(record)
        })
        return result
    })
}

// PERFORMANCE IMPROVEMENT: 320ms for 100K records (25.6x faster)
```

### Purity Issue Resolution
```php
// BEFORE: Impure function with side effects
function processUser(array $user): array {
    error_log("Processing user: " . $user['name']); // Side effect
    $user['processed'] = true;                      // Mutation
    $user['timestamp'] = time();                    // Non-deterministic
    
    return $user;
}

// DIAGNOSIS: Multiple purity violations affecting testability

// AFTER: Pure function extraction
function processUserData(array $user, int $timestamp): array {
    return array_merge($user, [
        'processed' => true,
        'timestamp' => $timestamp
    ]);
}

function processUserWithEffects(array $user): array {
    error_log("Processing user: " . $user['name']); // Side effect isolated
    return processUserData($user, time());
}

// BENEFITS: Testable pure logic, isolated side effects
```

### Composition Issue Resolution
```python
# BEFORE: Complex nested validation
def validate_and_save_user(user_data):
    try:
        if validate_email(user_data.get('email')):
            if validate_password(user_data.get('password')):
                if validate_age(user_data.get('age')):
                    transformed = transform_user(user_data)
                    return save_user(transformed)
                else:
                    raise ValidationError('Invalid age')
            else:
                raise ValidationError('Invalid password')
        else:
            raise ValidationError('Invalid email')
    except Exception as e:
        log_error(e)
        raise

# DIAGNOSIS: Deep nesting, complex error handling

# AFTER: Early return composition
def validate_and_save_user(user_data):
    # Sequential validation with early returns
    email_result = validate_email(user_data.get('email'))
    if not email_result.valid:
        return email_result
    
    password_result = validate_password(user_data.get('password'))
    if not password_result.valid:
        return password_result
    
    age_result = validate_age(user_data.get('age'))
    if not age_result.valid:
        return age_result
    
    # All validations passed
    transformed = transform_user(user_data)
    return save_user(transformed)

# BENEFITS: Clear flow, simple error handling, maintainable
```

## Cross-Language Troubleshooting

### JavaScript Issues
- **Closure Memory Leaks**: WeakMap usage, proper cleanup
- **Async Composition**: Promise chains vs async/await patterns
- **V8 Optimizations**: Hidden classes, inline caches, deoptimization

### PHP Issues  
- **Array Processing**: array_map vs foreach performance
- **Closure Performance**: 'use' clause optimization
- **OpCache Considerations**: Function compilation and caching

### Python Issues
- **Generator vs List**: Memory efficiency in data processing
- **Decorator Performance**: Overhead in function wrapping
- **GIL Impact**: Threading vs multiprocessing for CPU-bound tasks

### Rust Issues
- **Borrow Checker**: Ownership patterns in functional code
- **Zero-Cost Abstractions**: Iterator chain optimization
- **Memory Safety**: Lifetime management in closures

## Quality Gates

- **Issue Resolution**: "Is the root cause correctly identified and addressed?"
- **Performance Improvement**: "Are performance claims validated with benchmarks?"
- **Purity Restoration**: "Are side effects properly isolated or eliminated?"
- **Simplicity Enhancement**: "Is the solution simpler and more maintainable?"
- **Cross-Language Applicability**: "Do solutions apply appropriately across languages?"

## Usage Examples

### Diagnose Performance Issue
```
/fp:troubleshoot "Processing 100K records takes 8 seconds" --type performance --benchmark
```

### Fix Purity Violations
```
/fp:troubleshoot "Function is hard to test due to side effects" --type purity --fix --examples
```

### Resolve Composition Complexity
```
/fp:troubleshoot "Validation logic is nested 6 levels deep" --type composition --examples
```

### Detect Anti-Patterns
```
/fp:troubleshoot "Created pipe() utility but performance decreased" --type pattern --fix
```

### Language-Specific Issues
```
/fp:troubleshoot "PHP array processing slower than expected" --lang php --trace --benchmark
```