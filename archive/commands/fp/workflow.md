---
allowed-tools: [Read, Write, Edit, Glob, Grep, TodoWrite, Task, mcp__sequential-thinking__sequentialthinking, mcp__context7__context7]
description: "Generate FP-focused implementation workflows emphasizing purity, composition, and performance optimization patterns"
complexity-threshold: 0.6
performance-profile: complex
personas: [functional, architect, analyzer, performance]
mcp-servers: [sequential, context7]
---

# /fp:workflow - Functional Programming Implementation Workflow

## Purpose
Generate comprehensive, step-by-step implementation workflows from requirements with functional programming principles, emphasizing pure functions, composition patterns, hot path optimizations, and anti-over-engineering constraints.

## Usage
```
/fp:workflow [prd-file|feature-description] [--lang javascript|php|python|rust] [--focus performance|purity|composition] [--strategy systematic|mvp|performance-first]
```

## Arguments
- `prd-file|feature-description` - Path to requirements or direct feature description
- `--lang` - Target language for FP-specific workflow patterns
- `--focus` - Primary FP focus (performance, purity, composition, simplicity)
- `--strategy` - Workflow approach (systematic, mvp, performance-first)
- `--cross-lang` - Include equivalent patterns in other languages
- `--benchmark` - Include performance measurement steps
- `--examples` - Generate detailed implementation examples

## FP Workflow Strategies

### Systematic Strategy (Default)
1. **Requirements Analysis** - FP pattern opportunities identification
2. **Pure Function Design** - Core business logic as pure functions
3. **Side Effect Architecture** - Isolation and management of impure operations
4. **Composition Planning** - Function composition and data flow design
5. **Performance Optimization** - Hot path analysis and pre-compilation
6. **Testing Strategy** - Comprehensive pure function testing approach

### MVP Strategy
1. **Core Function Identification** - Essential pure business logic
2. **Simple Composition** - Direct function calls over complex patterns
3. **Minimal Side Effects** - Only necessary impure operations
4. **Performance Baseline** - Simple implementation first
5. **Iteration Planning** - Progressive enhancement with FP patterns
6. **Evidence-Based Improvement** - Benchmark-driven optimization

### Performance-First Strategy
1. **Hot Path Identification** - Critical performance bottlenecks
2. **Configuration Pre-Compilation** - Setup-time optimization
3. **Pure Function Optimization** - Aggressive performance tuning
4. **Memory Optimization** - Closure and allocation efficiency
5. **Benchmark Integration** - Continuous performance validation
6. **Scalability Planning** - Growth-oriented optimization patterns

## FP Workflow Framework

### 1. Pure Function Architecture Phase

#### Core Business Logic Design
```yaml
pure_function_architecture:
  requirements_analysis:
    - "Identify core business rules and logic"
    - "Separate business logic from side effects"
    - "Map input/output contracts and data flow"
    - "Plan comprehensive edge case coverage"
    
  function_design:
    - "Design pure functions for business logic"
    - "Plan input validation and error handling"
    - "Define clear return value contracts"
    - "Enable comprehensive testing strategies"
    
  composition_planning:
    - "Plan function composition patterns"
    - "Design error propagation strategies"
    - "Map data transformation pipelines"
    - "Optimize for maintainability and clarity"
```

#### Implementation Workflow Example
```javascript
// Phase 1: Pure Business Logic
function validateUserData(userData) {
    // Pure function - no side effects, deterministic
    if (!userData.email || !validateEmailFormat(userData.email)) {
        return { valid: false, error: 'Invalid email' }
    }
    
    if (!userData.password || userData.password.length < 8) {
        return { valid: false, error: 'Password too short' }
    }
    
    return { valid: true, data: userData }
}

function processUserRegistration(userData, timestamp) {
    // Pure function with explicit dependencies
    const validation = validateUserData(userData)
    if (!validation.valid) {
        return validation
    }
    
    return {
        valid: true,
        user: {
            ...userData,
            id: generateUserId(userData.email),
            createdAt: timestamp,
            verified: false
        }
    }
}

// Phase 2: Side Effect Coordination
async function registerUserWithEffects(userData) {
    // Side effects coordinated separately from business logic
    const timestamp = Date.now()
    const result = processUserRegistration(userData, timestamp)
    
    if (!result.valid) {
        logValidationError(result.error, userData.email) // Side effect
        return result
    }
    
    const savedUser = await saveUser(result.user) // Side effect
    await sendVerificationEmail(savedUser.email)   // Side effect
    
    return { valid: true, user: savedUser }
}
```

### 2. Performance Optimization Phase

#### Hot Path Pattern Implementation
```yaml
performance_optimization:
  hot_path_analysis:
    - "Identify expensive operations in data processing loops"
    - "Find configuration access patterns in hot paths"
    - "Measure baseline performance with realistic data"
    - "Plan pre-compilation and caching strategies"
    
  optimization_implementation:
    - "Extract expensive operations to setup phase"
    - "Implement function factories for reusable logic"
    - "Apply closure caching for expensive lookups"
    - "Optimize memory allocation patterns"
    
  validation_strategy:
    - "Benchmark before/after performance improvements"
    - "Validate identical behavior preservation"
    - "Test with realistic data volumes"
    - "Monitor memory usage and garbage collection"
```

#### Performance Workflow Example
```php
// Phase 1: Performance Analysis
// BEFORE: O(records × fields) - configuration access in hot path
function processRecords(array $records, array $schema): array {
    return array_map(function ($record) use ($schema) {
        $result = [];
        foreach ($schema['fields'] as $field) { // ← Config access per record
            $result[$field['name']] = transformField(
                $record[$field['name']], 
                $field['type']
            );
        }
        return $result;
    }, $records);
}

// Phase 2: Hot Path Optimization
function createOptimizedProcessor(array $schema): callable {
    // Pre-compile field processors - O(fields) setup cost
    $fieldProcessors = [];
    foreach ($schema['fields'] as $field) {
        $fieldProcessors[] = createFieldProcessor($field);
    }
    
    // Return optimized processor - O(records) execution
    return function (array $records) use ($fieldProcessors): array {
        return array_map(function ($record) use ($fieldProcessors) {
            $result = [];
            foreach ($fieldProcessors as $processor) {
                $processed = $processor($record);
                $result[$processed['field']] = $processed['value'];
            }
            return $result;
        }, $records);
    };
}

// Phase 3: Performance Validation
function benchmarkProcessors(array $testRecords, array $schema): array {
    // Benchmark original implementation
    $startTime = microtime(true);
    $originalResult = processRecords($testRecords, $schema);
    $originalTime = microtime(true) - $startTime;
    
    // Benchmark optimized implementation
    $processor = createOptimizedProcessor($schema);
    $startTime = microtime(true);
    $optimizedResult = $processor($testRecords);
    $optimizedTime = microtime(true) - $startTime;
    
    return [
        'original_time' => $originalTime,
        'optimized_time' => $optimizedTime,
        'improvement' => $originalTime / $optimizedTime,
        'results_identical' => $originalResult === $optimizedResult
    ];
}
```

### 3. Anti-Over-Engineering Phase

#### Simplicity Constraints
```yaml
anti_over_engineering:
  pattern_evaluation:
    - "Prefer direct function calls over utility creation"
    - "Use native language features over FP utilities"
    - "Choose simple composition over complex abstractions"
    - "Apply MVP approach to FP pattern adoption"
    
  complexity_prevention:
    - "Avoid creating pipe(), compose(), curry() utilities"
    - "Use early returns over deep nesting"
    - "Prefer clear error handling over monadic patterns"
    - "Choose performance over pattern purity"
    
  validation_gates:
    - "Ensure solutions are simpler than problems"
    - "Validate that patterns improve maintainability"
    - "Confirm performance isn't sacrificed for pattern purity"
    - "Verify junior developers can understand and maintain"
```

#### Simplicity Workflow Example
```python
# Phase 1: Anti-Pattern Prevention
# AVOID: Over-engineered utility creation
def pipe(*functions):
    """DON'T CREATE - Use native patterns instead"""
    return lambda x: functools.reduce(lambda acc, f: f(acc), functions, x)

# Phase 2: Simple Native Patterns
def validate_user(user_data):
    """Simple validation with early returns"""
    if not user_data.get('email'):
        return {'valid': False, 'error': 'Email required'}
    
    if not validate_email_format(user_data['email']):
        return {'valid': False, 'error': 'Invalid email format'}
    
    if not user_data.get('password') or len(user_data['password']) < 8:
        return {'valid': False, 'error': 'Password too short'}
    
    return {'valid': True, 'data': user_data}

def process_user_registration(user_data, timestamp):
    """Simple composition with native language features"""
    validation = validate_user(user_data)
    if not validation['valid']:
        return validation
    
    sanitized = sanitize_user_data(validation['data'])
    enriched = enrich_user_data(sanitized, timestamp)
    
    return {'valid': True, 'user': enriched}

# Phase 3: Performance-Focused Implementation
def create_user_processor(config):
    """Function factory with pre-compiled configuration"""
    # Pre-compile expensive operations
    compiled_validations = [compile_validator(v) for v in config['validations']]
    compiled_sanitizers = [compile_sanitizer(s) for s in config['sanitizers']]
    
    def process_users(users):
        results = []
        for user in users:
            # Apply pre-compiled operations
            if not all(validator(user) for validator in compiled_validations):
                results.append({'valid': False, 'error': 'Validation failed'})
                continue
            
            sanitized = user
            for sanitizer in compiled_sanitizers:
                sanitized = sanitizer(sanitized)
            
            results.append({'valid': True, 'user': sanitized})
        
        return results
    
    return process_users
```

## SuperClaude Integration

**Enhanced SC:Workflow**: Routes to `/sc:workflow` with FP workflow seeding

**FP Workflow Enhancement**:
```yaml
fp_workflow_seeding:
  architectural_principles:
    - "Design for pure function boundaries"
    - "Isolate side effects to system edges"
    - "Plan composition patterns for maintainability"
    - "Optimize hot paths with pre-compilation"
    
  implementation_guidance:
    - "Start with simple direct solutions"
    - "Apply FP patterns only when they improve simplicity"
    - "Use native language features over utilities"
    - "Benchmark performance improvements"
    
  quality_assurance:
    - "Ensure comprehensive testing of pure functions"
    - "Validate behavior preservation in optimizations"
    - "Test all edge cases systematically"
    - "Monitor performance characteristics"
```

## Cross-Language Workflow Patterns

### JavaScript Workflow
```javascript
// 1. Pure function design with closures
const createValidator = (rules) => {
    const compiledRules = rules.map(compileRule)
    return (data) => compiledRules.every(rule => rule(data))
}

// 2. Performance optimization with WeakMap
const createCachedProcessor = (config) => {
    const cache = new WeakMap()
    const processor = createProcessor(config)
    
    return (input) => {
        if (cache.has(input)) return cache.get(input)
        const result = processor(input)
        cache.set(input, result)
        return result
    }
}
```

### PHP Workflow
```php
// 1. Function factories with use clauses
function createValidator(array $rules): callable {
    $compiledRules = array_map('compileRule', $rules);
    return function ($data) use ($compiledRules): bool {
        return array_reduce($compiledRules, 
            fn($valid, $rule) => $valid && $rule($data), 
            true
        );
    };
}

// 2. Performance with OpCache optimization
function createOptimizedProcessor(array $config): callable {
    $processors = array_map('compileProcessor', $config['processors']);
    return fn(array $data): array => array_reduce($processors, 
        fn($acc, $proc) => $proc($acc), 
        $data
    );
}
```

### Python Workflow
```python
# 1. Generator-based processing for memory efficiency
def create_data_processor(config):
    compiled_transforms = [compile_transform(t) for t in config['transforms']]
    
    def process_data_stream(data_stream):
        for item in data_stream:
            result = item
            for transform in compiled_transforms:
                result = transform(result)
            yield result
    
    return process_data_stream

# 2. functools.lru_cache for optimization
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(input_key):
    # Expensive pure computation
    return complex_calculation(input_key)
```

### Rust Workflow
```rust
// 1. Zero-cost abstractions with iterators
fn create_processor<T>(config: ProcessorConfig) -> impl Fn(Vec<T>) -> Vec<T> {
    let compiled_ops: Vec<_> = config.operations.into_iter()
        .map(|op| compile_operation(op))
        .collect();
    
    move |input| {
        input.into_iter()
            .map(|item| {
                compiled_ops.iter()
                    .fold(item, |acc, op| op(acc))
            })
            .collect()
    }
}

// 2. Memory-efficient processing with Result<T,E>
fn process_data_safely<T>(data: Vec<T>, processor: impl Fn(T) -> Result<T, ProcessError>) -> Result<Vec<T>, ProcessError> {
    data.into_iter()
        .map(processor)
        .collect()
}
```

## Quality Gates

- **Simplicity Validation**: "Are FP patterns simpler than alternative approaches?"
- **Performance Improvement**: "Do optimizations provide measurable benefits?"
- **Maintainability Enhancement**: "Does the workflow improve code maintainability?"
- **Testing Feasibility**: "Are pure functions comprehensively testable?"
- **Cross-Language Consistency**: "Do patterns translate appropriately across languages?"

## Usage Examples

### Generate FP-Focused Feature Workflow
```
/fp:workflow user-authentication-system --lang javascript --focus purity --strategy systematic
```

### Performance-Optimized Workflow
```
/fp:workflow data-processing-pipeline --focus performance --strategy performance-first --benchmark
```

### MVP Approach with FP Principles
```
/fp:workflow payment-validation --strategy mvp --lang php --examples
```

### Cross-Language Implementation Workflow
```
/fp:workflow validation-service --cross-lang --lang python --focus composition
```