---
allowed-tools: [Read, Grep, Glob, Write, Edit]
description: "Create FP-focused documentation emphasizing pure functions, composition patterns, and performance characteristics"
---

# /fp:document - Functional Programming Documentation

## Purpose
Generate comprehensive documentation for functional programming code, emphasizing pure function contracts, composition patterns, performance characteristics, and cross-language equivalents.

## Usage
```
/fp:document [target] [--type inline|external|api|patterns] [--style brief|detailed] [--lang javascript|php|python|rust]
```

## Arguments
- `target` - Specific file, function, or component to document
- `--type` - Documentation type (inline, external, api, patterns)
- `--style` - Documentation style (brief, detailed)
- `--lang` - Primary language for examples and patterns
- `--cross-lang` - Include equivalent patterns in other languages
- `--performance` - Include performance characteristics and benchmarks
- `--examples` - Generate comprehensive usage examples
- `--edge-cases` - Document edge case handling

## FP Documentation Framework

### 1. Pure Function Documentation Template
```javascript
/**
 * Creates optimized user data processor with pre-compiled validation rules
 * 
 * @pure - This function is pure and deterministic
 * @performance - O(1) setup, O(users) execution vs O(users × rules) naive approach
 * @pattern - Function factory with configuration pre-compilation
 * 
 * @param {Object} config - Validation configuration
 * @param {Array} config.rules - Validation rules to pre-compile
 * @param {Object} config.transforms - Field transformations
 * 
 * @returns {Function} Optimized processor function (users: Array) => ProcessedUser[]
 * 
 * @example
 * const processor = createUserProcessor({
 *   rules: [validateEmail, validateAge],
 *   transforms: { email: lowercase, name: trim }
 * })
 * 
 * const validUsers = processor(userData) // O(users) execution
 * 
 * @edge-cases
 * - Empty config.rules array: returns identity processor
 * - Null/undefined users: returns empty array
 * - Invalid user objects: skips with error logging
 * 
 * @cross-language
 * - PHP: Uses array_map with closure and 'use' clause
 * - Python: Uses functools.partial with lambda composition
 * - Rust: Uses closure with move semantics and Vec operations
 */
```

### 2. Composition Pattern Documentation
```markdown
## Function Composition: User Validation Pipeline

### Pattern Overview
Sequential validation with early returns, avoiding deep nesting and providing clear error paths.

### Architecture
```text
Input Data → validateRequired → validateEmail → validatePassword → Output
     ↓            ↓                ↓                ↓              ↓
   Invalid    Missing Fields    Invalid Email    Weak Password   Valid User
```

### Performance Characteristics
- **Time Complexity**: O(n) where n = validation rules
- **Space Complexity**: O(1) with early returns
- **Hot Path Optimization**: Pre-compile regex patterns and validation rules

### Cross-Language Implementations
- **JavaScript**: Early returns with Result pattern
- **PHP**: Null coalescing with validation chains  
- **Python**: Exception handling with validation decorators
- **Rust**: Result<T,E> with ? operator for error propagation
```

### 3. Hot Path Performance Documentation
```markdown
## Performance Analysis: Data Processing Pipeline

### Before: O(records × fields) Anti-Pattern
```javascript
// ❌ Configuration accessed per record
function processRecords(records, schema) {
    return records.map(record => {
        return schema.fields.reduce((obj, field) => {
            obj[field.name] = transformField(record[field.name], field.type)
            return obj
        }, {})
    })
}
```

### After: O(records + fields) Optimization
```javascript
// ✅ Configuration pre-compiled
function createOptimizedProcessor(schema) {
    const fieldProcessors = schema.fields.map(field => 
        record => ({ [field.name]: transformField(record[field.name], field.type) })
    )
    
    return records => records.map(record => 
        fieldProcessors.reduce((obj, processor) => ({ ...obj, ...processor(record) }), {})
    )
}
```

### Performance Impact
| Records | Fields | Before | After | Improvement |
|---------|--------|--------|-------|-------------|
| 1,000   | 12     | 45ms   | 8ms   | 5.6x        |
| 10,000  | 24     | 890ms  | 65ms  | 13.7x       |
| 100,000 | 24     | 8.2s   | 320ms | 25.6x       |
```

## Documentation Types

### Inline Documentation (`--type inline`)
Adds comprehensive JSDoc/PHPDoc comments with FP-specific annotations:
- `@pure` - Marks pure functions
- `@pattern` - Identifies FP pattern used
- `@performance` - Documents complexity and optimizations
- `@edge-cases` - Lists edge case handling
- `@cross-language` - Notes equivalent patterns

### External Documentation (`--type external`)
Creates standalone markdown documentation with:
- Function contracts and type signatures
- Composition patterns and data flow diagrams
- Performance characteristics and benchmarks
- Cross-language implementation examples
- Comprehensive testing strategies

### API Documentation (`--type api`)
Generates FP-focused API documentation with:
- Pure function guarantees and side effect isolation
- Input/output contracts with immutability constraints
- Performance budgets and complexity analysis
- Error handling patterns and recovery strategies
- Usage examples with performance implications

### Pattern Documentation (`--type patterns`)
Documents FP architectural patterns:
- Function factory implementations
- Composition strategies and error handling
- Hot path optimization techniques
- Cross-language pattern translations
- Anti-pattern warnings and alternatives

## SuperClaude Integration

**Enhanced SC:Document**: Routes to `/sc:document` with FP documentation seeding

**FP Documentation Enhancement**:
```yaml
fp_documentation_seeding:
  function_analysis:
    - "Identify pure vs impure functions"
    - "Document side effects and mitigation strategies"
    - "Specify input/output contracts and immutability"
    - "Include comprehensive edge case coverage"
    
  performance_documentation:
    - "Document complexity characteristics (Big O)"
    - "Include hot path optimization opportunities"
    - "Provide before/after performance comparisons"
    - "Specify configuration pre-compilation benefits"
    
  composition_patterns:
    - "Document function composition strategies"
    - "Show error handling in composition pipelines"
    - "Include data flow diagrams and architecture"
    - "Provide testability and maintenance benefits"
    
  cross_language_coverage:
    - "Include equivalent patterns in other languages"
    - "Document language-specific optimization techniques"
    - "Show idiomatic implementations per language"
    - "Provide performance characteristics per language"
```

## Generated Documentation Examples

### Pure Function Documentation
```javascript
/**
 * Pure email validation with comprehensive edge case handling
 * 
 * @pure - No side effects, deterministic output
 * @performance - O(1) time complexity, minimal memory allocation
 * @pattern - Simple validation with Result-like return
 * 
 * @param {*} email - Email input of any type
 * @returns {{valid: boolean, error?: string, normalized?: string}}
 * 
 * @example
 * validateEmail('user@example.com') // {valid: true, normalized: 'user@example.com'}
 * validateEmail('INVALID')          // {valid: false, error: 'Invalid email format'}
 * validateEmail(null)               // {valid: false, error: 'Email is required'}
 * 
 * @edge-cases
 * - null/undefined: Returns {valid: false, error: 'Email is required'}
 * - non-string types: Converts to string before validation
 * - empty string: Returns {valid: false, error: 'Email is required'}
 * - whitespace: Trims and validates normalized version
 * 
 * @testing-strategy
 * Pure function enables comprehensive testing:
 * - All JavaScript data types: null, undefined, boolean, number, object, array
 * - Boundary cases: empty strings, whitespace variations
 * - Format variations: valid formats, invalid formats, edge cases
 * - Performance testing: large input strings, memory usage validation
 */
function validateEmail(email) {
    if (email == null || email === '') {
        return { valid: false, error: 'Email is required' }
    }
    
    const normalized = String(email).trim().toLowerCase()
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    
    if (!emailRegex.test(normalized)) {
        return { valid: false, error: 'Invalid email format' }
    }
    
    return { valid: true, normalized }
}
```

### Hot Path Optimization Documentation
```markdown
# Data Processor Performance Optimization

## Problem: Configuration Access in Hot Path
The original implementation accesses configuration data during record processing, creating O(records × configuration) complexity.

## Solution: Configuration Pre-Compilation
Pre-compile expensive operations during setup phase, achieving O(setup + records) complexity.

## Implementation

### Before: Inefficient Pattern
```php
function processRecords(array $records, array $config): array {
    return array_map(function ($record) use ($config) {
        // Configuration accessed per record - SLOW
        return processWithConfig($record, $config);
    }, $records);
}
```

### After: Pre-Compilation Pattern
```php
function createOptimizedProcessor(array $config): callable {
    // Pre-compile expensive operations - FAST
    $compiledRules = array_map('compileRule', $config['rules']);
    $compiledTransforms = array_map('compileTransform', $config['transforms']);
    
    return function (array $records) use ($compiledRules, $compiledTransforms): array {
        return array_map(function ($record) use ($compiledRules, $compiledTransforms) {
            return applyCompiledRules($record, $compiledRules, $compiledTransforms);
        }, $records);
    };
}
```

## Performance Benchmarks
| Dataset Size | Before | After | Improvement |
|-------------|--------|-------|-------------|
| 1K records  | 45ms   | 8ms   | 5.6x faster |
| 10K records | 890ms  | 65ms  | 13.7x faster|
| 100K records| 8.2s   | 320ms | 25.6x faster|

## Memory Usage
- **Before**: O(records × config_size) memory allocation
- **After**: O(records + compiled_config) memory allocation
- **Improvement**: Reduces memory pressure by 60-80% for large datasets
```

### Cross-Language Pattern Documentation
```markdown
# Cross-Language Function Factory Pattern

## JavaScript Implementation
```javascript
const createValidator = (rules) => {
    const compiledRules = rules.map(compileRule)
    return (data) => compiledRules.every(rule => rule(data))
}
```

## PHP Implementation  
```php
function createValidator(array $rules): callable {
    $compiledRules = array_map('compileRule', $rules);
    return function ($data) use ($compiledRules): bool {
        return array_reduce($compiledRules, 
            fn($valid, $rule) => $valid && $rule($data), 
            true
        );
    };
}
```

## Python Implementation
```python
def create_validator(rules):
    compiled_rules = [compile_rule(rule) for rule in rules]
    return lambda data: all(rule(data) for rule in compiled_rules)
```

## Rust Implementation
```rust
fn create_validator<T>(rules: Vec<Rule<T>>) -> impl Fn(&T) -> bool {
    let compiled_rules: Vec<_> = rules.into_iter().map(compile_rule).collect();
    move |data| compiled_rules.iter().all(|rule| rule(data))
}
```

## Performance Characteristics
| Language   | Setup Time | Execution Time | Memory Usage |
|------------|------------|----------------|--------------|
| JavaScript | ~2ms       | ~0.1ms/call    | ~50KB        |
| PHP        | ~3ms       | ~0.15ms/call   | ~45KB        |
| Python     | ~5ms       | ~0.2ms/call    | ~60KB        |
| Rust       | ~1ms       | ~0.05ms/call   | ~30KB        |
```

## Quality Gates

- **FP Accuracy**: "Are FP principles correctly documented?"
- **Performance Claims**: "Are performance characteristics backed by evidence?"
- **Cross-Language Correctness**: "Are language-specific patterns idiomatic?"
- **Edge Case Coverage**: "Are all edge cases documented with examples?"
- **Testing Strategy**: "Is comprehensive testing approach provided?"
- **Maintenance Value**: "Does documentation aid long-term maintenance?"

## Usage Examples

### Document Pure Function with Performance Focus
```
/fp:document src/validators/email.js --type inline --performance --edge-cases
```

### Create External Pattern Documentation
```
/fp:document src/processors/ --type patterns --cross-lang --examples
```

### Generate API Documentation with FP Focus
```
/fp:document user-service.js --type api --style detailed --performance
```

### Document Cross-Language Implementation
```
/fp:document validation-logic.js --cross-lang --lang python --examples
```