---
allowed-tools: [Read, Grep, Glob, Bash, Edit, MultiEdit]
description: "Clean up code using FP principles, removing impurities, optimizing compositions, and eliminating anti-patterns"
---

# /fp:cleanup - Functional Programming Code Cleanup

## Purpose
Systematically clean up code using functional programming principles, removing impurities, optimizing compositions, eliminating anti-patterns, and applying simplicity constraints.

## Usage
```
/fp:cleanup [target] [--type purity|performance|patterns|all] [--level safe|moderate|aggressive] [--lang javascript|php|python|rust]
```

## Arguments
- `target` - Files, directories, or specific functions to clean up
- `--type` - Cleanup focus (purity, performance, patterns, all)
- `--level` - Cleanup intensity (safe, moderate, aggressive)
- `--lang` - Target language for language-specific optimizations
- `--dry-run` - Preview changes without applying them
- `--benchmark` - Measure performance before/after cleanup
- `--preserve-behavior` - Ensure identical input/output behavior

## FP Cleanup Framework

### 1. Purity Cleanup

#### Side Effect Isolation
```javascript
// BEFORE: Side effects mixed with business logic
function processOrder(order) {
    console.log(`Processing order ${order.id}`) // ← Side effect
    const validatedOrder = validateOrder(order)
    if (!validatedOrder.valid) {
        console.error('Invalid order:', validatedOrder.errors) // ← Side effect
        return null
    }
    
    order.processed = true // ← Mutation
    order.processedAt = Date.now() // ← Non-deterministic
    
    database.save(order) // ← Side effect
    return order
}

// AFTER: Pure business logic with isolated effects
function processOrderData(order, timestamp) {
    const validatedOrder = validateOrder(order)
    if (!validatedOrder.valid) {
        return { success: false, errors: validatedOrder.errors }
    }
    
    return {
        success: true,
        data: {
            ...order,
            processed: true,
            processedAt: timestamp
        }
    }
}

function processOrderWithEffects(order) {
    console.log(`Processing order ${order.id}`)
    const result = processOrderData(order, Date.now())
    
    if (!result.success) {
        console.error('Invalid order:', result.errors)
        return null
    }
    
    database.save(result.data)
    return result.data
}

// CLEANUP BENEFITS:
// - Pure business logic is testable
// - Side effects are isolated and explicit
// - Function behavior is predictable
```

#### Mutation Elimination
```php
// BEFORE: In-place mutations
function updateUserScores(array &$users): void {
    foreach ($users as &$user) {
        $user['score'] += calculateBonus($user);
        $user['level'] = determineLevelFromScore($user['score']);
        $user['achievements'] = updateAchievements($user);
    }
}

// AFTER: Immutable transformations
function updateUserScores(array $users): array {
    return array_map(function (array $user): array {
        $newScore = $user['score'] + calculateBonus($user);
        return array_merge($user, [
            'score' => $newScore,
            'level' => determineLevelFromScore($newScore),
            'achievements' => updateAchievements($user)
        ]);
    }, $users);
}

// CLEANUP BENEFITS:
// - No side effects on input data
// - Safe for concurrent processing
// - Clear input/output contracts
```

### 2. Performance Cleanup

#### Hot Path Configuration Access Optimization
```python
# BEFORE: Configuration access in hot path
def process_records(records, config):
    return [
        transform_record(record, config['rules'], config['transforms'])
        for record in records  # ← Config accessed per record
    ]

# AFTER: Pre-compiled configuration
def create_optimized_processor(config):
    # Pre-compile expensive operations
    compiled_rules = [compile_rule(rule) for rule in config['rules']]
    compiled_transforms = [compile_transform(t) for t in config['transforms']]
    
    def process_records(records):
        return [
            transform_record(record, compiled_rules, compiled_transforms)
            for record in records
        ]
    
    return process_records

# CLEANUP BENEFITS:
# - O(records × config) → O(records + config)
# - 10-25x performance improvement typical
# - Reduced memory allocation per record
```

#### Closure Memory Optimization
```javascript
// BEFORE: Memory leak through closure retention
function createProcessors(configs) {
    return configs.map(config => {
        const heavyData = loadExpensiveData(config) // ← Retained indefinitely
        const metadata = generateMetadata(config)   // ← Also retained
        
        return function(input) {
            return processWithData(input, heavyData, metadata)
        }
    })
}

// AFTER: Optimized closure with cleanup
function createProcessors(configs) {
    const processorsMap = new WeakMap()
    
    return configs.map(config => {
        const heavyData = loadExpensiveData(config)
        const metadata = generateMetadata(config)
        
        const processor = function(input) {
            return processWithData(input, heavyData, metadata)
        }
        
        // Enable garbage collection when config is released
        processorsMap.set(config, { heavyData, metadata })
        return processor
    })
}

// CLEANUP BENEFITS:
// - Enables garbage collection of heavy data
// - Reduces memory footprint
// - Prevents memory leaks in long-running processes
```

### 3. Pattern Cleanup

#### Anti-Utility Pattern Elimination
```rust
// BEFORE: Over-engineered utility functions
struct PipelineBuilder<T> {
    operations: Vec<Box<dyn Fn(T) -> T>>,
}

impl<T> PipelineBuilder<T> {
    fn new() -> Self {
        Self { operations: Vec::new() }
    }
    
    fn pipe<F>(mut self, operation: F) -> Self 
    where F: Fn(T) -> T + 'static {
        self.operations.push(Box::new(operation));
        self
    }
    
    fn execute(&self, input: T) -> T {
        self.operations.iter().fold(input, |acc, op| op(acc))
    }
}

// AFTER: Simple native composition
fn process_user(user: User) -> Result<User, ProcessingError> {
    let validated = validate_user(user)?;
    let sanitized = sanitize_user(validated)?;
    let enriched = enrich_user(sanitized)?;
    Ok(enriched)
}

// CLEANUP BENEFITS:
// - No runtime overhead from utilities
// - Clear error propagation with ?
// - Native language patterns
// - Easier debugging and profiling
```

#### Composition Simplification
```javascript
// BEFORE: Complex nested composition
function processUserData(userData) {
    return validateUser(userData)
        .then(validatedData => {
            return sanitizeUser(validatedData)
                .then(sanitizedData => {
                    return enrichUser(sanitizedData)
                        .then(enrichedData => {
                            return transformUser(enrichedData)
                                .then(transformedData => {
                                    return saveUser(transformedData)
                                })
                        })
                })
        })
        .catch(error => {
            logError(error)
            throw error
        })
}

// AFTER: Clean async/await composition
async function processUserData(userData) {
    try {
        const validated = await validateUser(userData)
        const sanitized = await sanitizeUser(validated)
        const enriched = await enrichUser(sanitized)
        const transformed = await transformUser(enriched)
        return await saveUser(transformed)
    } catch (error) {
        logError(error)
        throw error
    }
}

// CLEANUP BENEFITS:
// - Linear flow instead of nested callbacks
// - Clear error handling
// - Easier to debug and maintain
```

### 4. Anti-Over-Engineering Cleanup

#### Complex Abstraction Simplification
```php
// BEFORE: Over-engineered validation system
abstract class AbstractValidatorFactory {
    abstract public function createValidator(string $type): ValidatorInterface;
}

class EmailValidatorFactory extends AbstractValidatorFactory {
    public function createValidator(string $type): ValidatorInterface {
        switch ($type) {
            case 'strict':
                return new StrictEmailValidator(
                    new RegexValidationEngine(
                        new ConfigurablePatternProvider()
                    )
                );
            case 'lenient':
                return new LenientEmailValidator(
                    new BasicValidationEngine()
                );
            default:
                throw new InvalidValidatorTypeException($type);
        }
    }
}

// AFTER: Simple function-based approach
function validateEmail(string $email, bool $strict = false): array {
    $email = trim($email);
    
    if ($strict) {
        $pattern = '/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/';
    } else {
        $pattern = '/^[^\s@]+@[^\s@]+\.[^\s@]+$/';
    }
    
    if (!preg_match($pattern, $email)) {
        return ['valid' => false, 'error' => 'Invalid email format'];
    }
    
    return ['valid' => true, 'email' => $email];
}

// CLEANUP BENEFITS:
// - 50+ lines reduced to 15 lines
// - No complex inheritance hierarchy
// - Direct and testable
// - Performance improvement (no object overhead)
```

## SuperClaude Integration

**Enhanced SC:Cleanup**: Routes to `/sc:cleanup` with FP cleanup seeding

**FP Cleanup Enhancement**:
```yaml
fp_cleanup_seeding:
  purity_cleanup:
    - "Isolate side effects from business logic"
    - "Eliminate in-place mutations"
    - "Extract non-deterministic behavior"
    - "Create pure function boundaries"
    
  performance_cleanup:
    - "Move configuration access out of hot paths"
    - "Optimize closure memory usage"
    - "Pre-compile expensive operations"
    - "Eliminate redundant calculations"
    
  pattern_cleanup:
    - "Remove over-engineered utility functions"
    - "Simplify complex compositions"
    - "Use native language patterns"
    - "Reduce abstraction layers"
    
  simplicity_cleanup:
    - "Apply KISS principle throughout"
    - "Eliminate unnecessary complexity"
    - "Prefer direct solutions over abstractions"
    - "Reduce cognitive overhead"
```

## Cleanup Levels

### Safe Level (`--level safe`)
- Only applies transformations that are guaranteed behavior-preserving
- Focuses on obvious improvements with minimal risk
- Includes: Dead code removal, obvious purity extractions, simple optimizations
- Conservative approach for production systems

### Moderate Level (`--level moderate`)
- Applies transformations with high confidence of correctness
- Includes structural improvements and pattern optimizations
- May require testing to verify behavior preservation
- Balanced approach for most projects

### Aggressive Level (`--level aggressive`)
- Applies comprehensive FP transformations
- May change function signatures and interfaces
- Requires thorough testing and review
- Maximum improvement potential with higher risk

## Cleanup Workflow

### 1. Analysis Phase
- **Code Scanning**: Identify cleanup opportunities using Grep and Glob
- **Pattern Detection**: Find anti-patterns, impurities, and performance issues
- **Impact Assessment**: Evaluate cleanup potential and risk levels
- **Priority Ranking**: Order cleanup operations by impact and safety

### 2. Planning Phase
- **Cleanup Strategy**: Select appropriate cleanup level and focus areas
- **Dependency Analysis**: Identify interconnected changes required
- **Risk Assessment**: Evaluate potential impact on system behavior
- **Testing Strategy**: Plan validation approach for cleanup changes

### 3. Execution Phase
- **Systematic Cleanup**: Apply transformations in dependency order
- **Behavior Preservation**: Maintain identical input/output contracts
- **Performance Monitoring**: Track improvements with benchmarks
- **Quality Validation**: Verify code quality improvements

### 4. Validation Phase
- **Behavior Testing**: Ensure identical functionality after cleanup
- **Performance Testing**: Measure and document improvements
- **Code Quality Assessment**: Verify maintainability improvements
- **Documentation Update**: Record cleanup changes and benefits

## Cross-Language Cleanup Strategies

### JavaScript Cleanup
- **Closure Optimization**: WeakMap usage, proper cleanup patterns
- **Promise Chain Simplification**: async/await over nested .then()
- **V8 Optimization**: Hidden class preservation, deoptimization avoidance
- **Memory Management**: Event listener cleanup, reference management

### PHP Cleanup
- **Array Processing**: array_map vs foreach performance optimization
- **Closure Performance**: Minimize 'use' clause overhead
- **Type Safety**: Add type hints for performance and reliability
- **OpCache Optimization**: Function structure for better caching

### Python Cleanup
- **List Comprehensions**: Generator expressions for memory efficiency
- **Function Decoration**: Minimize decorator overhead
- **Iterator Usage**: Lazy evaluation over eager computation
- **Type Hints**: MyPy-compatible type annotations

### Rust Cleanup
- **Ownership Optimization**: Minimize cloning, use references
- **Iterator Chains**: Zero-cost abstraction optimization
- **Error Handling**: Result<T,E> pattern consistency
- **Memory Safety**: Lifetime optimization in closures

## Quality Gates

- **Behavior Preservation**: "Does the cleaned code maintain identical behavior?"
- **Performance Improvement**: "Are performance gains measurable and significant?"
- **Simplicity Enhancement**: "Is the code simpler and more maintainable?"
- **Purity Achievement**: "Are side effects properly isolated or eliminated?"
- **Pattern Appropriateness**: "Are FP patterns appropriate for the language and context?"

## Usage Examples

### Clean Up Impure Functions
```
/fp:cleanup src/services/user-service.js --type purity --level safe --dry-run
```

### Performance-Focused Cleanup
```
/fp:cleanup data-processor.php --type performance --benchmark --level moderate
```

### Remove Anti-Patterns
```
/fp:cleanup src/utils/ --type patterns --level aggressive --preserve-behavior
```

### Comprehensive Cleanup
```
/fp:cleanup src/ --type all --level moderate --lang javascript --benchmark
```

### Language-Specific Cleanup
```
/fp:cleanup validation.py --lang python --type purity --level safe --dry-run
```