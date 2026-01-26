---
allowed-tools: [Read, Grep, Glob, Bash]
description: "Explain code through functional programming principles and patterns"
---

# /fp:explain - Functional Programming Explanation

## Purpose
Provide clear explanations of code functionality, concepts, or system behavior through a functional programming lens, emphasizing pure functions, composition, and performance patterns.

## Usage
```
/fp:explain [target] [--level basic|intermediate|advanced] [--focus patterns|performance|purity|composition] [--lang javascript|php|python|rust]
```

## Arguments
- `target` - Code file, function, concept, or pattern to explain
- `--level` - Explanation complexity (basic, intermediate, advanced)
- `--focus` - FP focus area (patterns, performance, purity, composition)
- `--lang` - Target language for FP-specific explanations
- `--examples` - Include practical FP transformation examples
- `--cross-lang` - Show equivalent patterns in other languages

## FP Explanation Framework

### 1. Functional Pattern Analysis
- **Pure Function Identification** - Distinguish pure from impure functions
- **Side Effect Mapping** - Identify and explain side effects impact
- **Composition Opportunities** - Show how functions can be composed
- **Hot Path Analysis** - Explain performance implications of FP patterns

### 2. Performance Perspective
- **Configuration Access Patterns** - Explain O(n²) vs O(n+m) optimizations
- **Function Factory Benefits** - Show pre-compilation advantages
- **Closure Optimization** - Explain scope-based performance gains
- **Memory Efficiency** - Discuss immutability vs mutation trade-offs

### 3. Cross-Language Translation
- **Pattern Equivalence** - Show how FP patterns work across languages
- **Language Idioms** - Explain native FP approaches per language
- **Performance Characteristics** - Language-specific optimization opportunities
- **Best Practices** - Language-specific FP recommendations

## Explanation Patterns

### Basic Level - Core Concepts
```javascript
// Example: Explaining pure function benefits
function impureExample(users) {
    console.log('Processing users...') // ← Side effect
    users.forEach(user => {
        user.processed = true // ← Mutation
    })
    return users.filter(u => u.active)
}

// FP Explanation:
// This function has side effects (console.log) and mutations (user.processed)
// This makes it hard to test, reason about, and optimize
```

### Intermediate Level - Performance Patterns
```javascript
// Example: Hot path optimization explanation
// Before: O(users × fields) - configuration accessed per user
function processUsers(users, schema) {
    return users.map(user => {
        return schema.fields.reduce((obj, field) => { // ← Expensive per user
            obj[field.name] = transformField(user[field.name], field.type)
            return obj
        }, {})
    })
}

// FP Explanation:
// The schema.fields access happens inside the user loop
// This creates O(users × fields) complexity
// FP solution: Pre-compile the field processors
```

### Advanced Level - Composition Architecture
```javascript
// Example: Function composition explanation
const processUserData = pipe(
    validateInput,
    sanitizeData, 
    enrichWithDefaults,
    transformFields,
    validateOutput
)

// FP Explanation:
// This composition creates a clear data flow pipeline
// Each function is pure and testable in isolation
// The composition is more maintainable than nested conditionals
// Error handling can be centralized at composition boundaries
```

## SuperClaude Integration

**Enhanced SC:Explain**: Routes to `/sc:explain` with FP analysis seeding

**FP Enhancement Framework**:
```yaml
fp_explanation_seeding:
  pure_function_analysis:
    - "Identify which functions are pure vs impure"
    - "Explain side effects and their implications"
    - "Show pure function testing advantages"
    - "Demonstrate predictable behavior benefits"
    
  performance_analysis:
    - "Identify hot path optimization opportunities"
    - "Explain configuration pre-compilation benefits"
    - "Show O(n²) to O(n+m) transformations"
    - "Demonstrate closure caching advantages"
    
  composition_patterns:
    - "Show how functions can be composed"
    - "Explain function factory patterns"
    - "Demonstrate error handling in compositions"
    - "Show cross-language equivalent patterns"
    
  simplicity_principles:
    - "Explain why simple solutions beat complex ones"
    - "Show how FP reduces cognitive complexity"
    - "Demonstrate testability improvements"
    - "Explain maintenance advantages"
```

## Explanation Focus Areas

### Patterns Focus (`--focus patterns`)
```javascript
// Explains common FP patterns and their benefits
const curriedValidation = (rules) => (data) => {
    // Explanation: Currying allows partial application
    // This enables reusable validators without repetition
    return rules.every(rule => rule(data))
}

// Usage explanation:
const userValidator = curriedValidation([validateEmail, validateAge])
const productValidator = curriedValidation([validateName, validatePrice])
```

### Performance Focus (`--focus performance`)
```javascript
// Explains performance implications and optimizations
// Slow approach - configuration in hot path
const slowProcessor = (records) => {
    const config = loadConfig() // ← Called for every record batch
    return records.map(record => processWithConfig(record, config))
}

// Fast approach - pre-compiled configuration  
const fastProcessor = (() => {
    const config = loadConfig() // ← Called once at setup
    return (records) => records.map(record => processWithConfig(record, config))
})()

// Explanation: Pre-compilation moves expensive operations out of hot paths
// This transforms O(batches × config_cost) to O(setup + batches)
```

### Purity Focus (`--focus purity`)
```javascript
// Explains pure function principles and benefits
function impure(data) {
    const timestamp = Date.now() // ← Non-deterministic
    data.processed = timestamp   // ← Mutation
    return data
}

function pure(data) {
    const timestamp = Date.now()
    return { ...data, processed: timestamp } // ← No mutation
}

// Explanation: Pure functions are predictable, testable, and composable
// They enable optimization opportunities and reduce bugs
```

### Composition Focus (`--focus composition`)
```javascript
// Explains function composition patterns
const validateUser = (userData) => {
    const emailValid = validateEmail(userData.email)
    if (!emailValid.valid) return emailValid
    
    const passwordValid = validatePassword(userData.password)
    if (!passwordValid.valid) return passwordValid
    
    return { valid: true, data: userData }
}

// Explanation: Sequential validation with early returns
// This avoids deep nesting and provides clear error paths
// Alternative: Use composition utilities where appropriate for the language
```

## Cross-Language Examples

### JavaScript Pattern
```javascript
const createProcessor = (config) => {
    const compiledRules = config.rules.map(compileRule)
    return (data) => compiledRules.reduce((result, rule) => rule(result), data)
}
```

### PHP Equivalent
```php
function createProcessor(array $config): callable {
    $compiledRules = array_map('compileRule', $config['rules']);
    return function (array $data) use ($compiledRules): array {
        return array_reduce($compiledRules, 
            fn($result, $rule) => $rule($result), 
            $data
        );
    };
}
```

### Python Equivalent  
```python
def create_processor(config):
    compiled_rules = [compile_rule(rule) for rule in config['rules']]
    def processor(data):
        return functools.reduce(lambda result, rule: rule(result), compiled_rules, data)
    return processor
```

### Rust Equivalent
```rust
fn create_processor<T>(config: &Config) -> impl Fn(T) -> T {
    let compiled_rules: Vec<_> = config.rules.iter().map(compile_rule).collect();
    move |data| compiled_rules.iter().fold(data, |acc, rule| rule(acc))
}
```

## Educational Workflow

### 1. Code Analysis Phase
- Read target code and identify key components
- Analyze function purity and side effects
- Map data flow and dependencies
- Identify optimization opportunities

### 2. FP Pattern Recognition Phase  
- Classify functions as pure/impure
- Identify composition opportunities
- Find hot path optimization potential
- Recognize anti-patterns and over-engineering

### 3. Explanation Generation Phase
- Structure explanation based on complexity level
- Provide relevant examples with before/after comparisons
- Include cross-language equivalents where helpful
- Add performance implications and testing benefits

### 4. Practical Application Phase
- Show transformation steps for imperative→functional conversion
- Provide comprehensive testing examples for pure functions
- Include performance benchmarking for optimization patterns
- Demonstrate real-world usage scenarios

## Quality Gates

- **Clarity Check**: "Is the explanation accessible to the target skill level?"
- **Accuracy Validation**: "Are all FP concepts explained correctly?"
- **Practical Value**: "Does the explanation provide actionable insights?"
- **Pattern Correctness**: "Are the recommended patterns appropriate for the language?"
- **Performance Accuracy**: "Are performance claims backed by evidence?"

## Usage Examples

### Explain Function Pattern
```
/fp:explain calculateUserMetrics --focus purity --examples
```

### Explain Performance Optimization
```
/fp:explain src/processors/data-transformer.js --focus performance --lang javascript
```

### Cross-Language Pattern Explanation
```
/fp:explain validation-logic.js --cross-lang --lang python
```

### Advanced Composition Explanation
```
/fp:explain --level advanced "How to compose validation functions without utilities" --examples
```

### Hot Path Performance Explanation
```
/fp:explain record-processor.php --focus performance --examples --lang php
```