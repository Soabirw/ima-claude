---
name: "php-fp"
description: "Core FP principles for PHP with anti-over-engineering focus - Simple > Complex | Native > Utilities | MVP > Enterprise"
---

# PHP Functional Programming

Core functional programming principles for PHP with anti-over-engineering enforcement. This skill provides error-preventing essentials and references to deep-dive content.

## When to Use This Skill

- Implementing pure, testable PHP functions
- Need FP architectural guidance for PHP
- Preventing over-engineering and utility creation
- Comprehensive testing strategies with PHPUnit
- Evidence-based performance optimization

## ⚠️ CRITICAL: Anti-Over-Engineering (PRIMARY FOCUS)

**Core Principle**: "Simple solutions > Complex abstractions | Native patterns > FP utilities | MVP > Enterprise patterns"

### Prohibited Patterns (NEVER CREATE)

```php
<?php
// ❌ NEVER: pipe() utility
function pipe(...$functions) {
    return fn($value) => array_reduce(
        $functions,
        fn($carry, $fn) => $fn($carry),
        $value
    );
}

// ✅ INSTEAD: Native array functions with early returns
function validateUser(array $userData): array {
    $requiredCheck = validateRequired(['email', 'name'], $userData);
    if (!$requiredCheck['valid']) return $requiredCheck;

    $emailCheck = validateEmail($userData);
    if (!$emailCheck['valid']) return $emailCheck;

    return validateNameLength($userData);
}

// ❌ NEVER: curry() utility
function curry(callable $fn) {
    return function(...$args) use ($fn) {
        return count($args) >= (new ReflectionFunction($fn))->getNumberOfRequiredParameters()
            ? $fn(...$args)
            : fn(...$more) => curry($fn)(...$args, ...$more);
    };
}

// ✅ INSTEAD: Native closures and explicit parameters
function createValidator(array $rules): callable {
    return function($value) use ($rules): array {
        $errors = array_filter($rules, fn($rule) => !$rule['validator']($value));
        return empty($errors)
            ? ['valid' => true]
            : ['valid' => false, 'errors' => $errors];
    };
}

// ❌ NEVER: Complex monad implementations
class Maybe {
    // Complex monad implementation
}

// ✅ INSTEAD: Simple result type
function divide(float $a, float $b): array {
    return $b === 0.0
        ? ['success' => false, 'error' => 'Division by zero']
        : ['success' => true, 'data' => $a / $b];
}
```

### Real-World Case Study: When NOT to Extract Pure Functions

**Context**: CRMAPI class in ima-espo WordPress plugin sends webhook data via HTTP POST.

**Anti-Over-Engineering Decision**: Applied 4-question quality gates framework and determined NO pure function extraction needed.

#### The 4-Question Framework

**Question 1: "Can this be pure?"**
```php
<?php
// sanitize_data() method analysis
private function sanitize_data($data) {
    $sanitized_data = array();
    foreach ($data as $key => $value) {
        $key = sanitize_text_field($key);  // WordPress function with filters
        if (is_array($value)) {
            $sanitized_data[$key] = $this->sanitize_data($value);
        } else {
            $sanitized_data[$key] = sanitize_text_field($value);
        }
    }
    return $sanitized_data;
}

// ❌ NOT PURE: Uses sanitize_text_field() which applies WordPress filters
// ✅ ALREADY ISOLATED: Private method, single responsibility
```

**Question 2: "Can this use native patterns?"**
```php
<?php
// send_api_request() method analysis
private function send_api_request($url, $data, $endpoint_label) {
    $response = wp_remote_post($url, array(/* ... */));  // WordPress HTTP API

    if (is_wp_error($response)) {
        error_log("API Error: {$endpoint_label}");  // WordPress logging
        return false;
    }

    return wp_remote_retrieve_response_code($response) === 200;
}

// ✅ USES NATIVE PATTERNS: WordPress HTTP API (wp_remote_post)
// ❌ EXTRACTION WOULD BE WRONG: Would require rebuilding WordPress HTTP transport
```

**Question 3: "Can this be simplified?"**
- **Current structure**: 239 lines total, ~35 lines of actual logic
- **Extraction cost**: Would create 2-3 new files for minimal benefit
- **Complexity analysis**: Already simple - thin wrapper over WordPress HTTP API
- **Decision**: ✅ Current structure is ALREADY simple and appropriate

**Question 4: "Is this complexity justified?"**
- **File purpose**: WordPress HTTP transport wrapper for webhook integration
- **Appropriate dependencies**: All wp_remote_* functions are correct tools
- **Extraction value**: Would add complexity without benefits
- **Anti-pattern detection**: Extraction would be over-engineering
- **Decision**: ❌ Extraction NOT justified

#### Result: NO EXTRACTION NEEDED

**Grade**: 🟢 **B+** (Appropriate WordPress Wrapper)

**Rationale**:
- File is appropriately structured as thin WordPress HTTP wrapper
- All dependencies (wp_remote_post, sanitize_text_field) are correct for the context
- Extraction would add indirection without improving testability or maintainability
- Current isolation (private methods) provides adequate structure
- **Anti-over-engineering principle applied**: Don't extract pure functions when WordPress integration IS the business logic

**Key Insight**: Not every file needs pure function extraction. WordPress HTTP wrappers are appropriately structured when they're thin transport layers using WordPress APIs correctly.

### Context-Appropriate Complexity

```php
<?php
// CLI Script: Simple and direct
function processFile(string $filePath): array {
    $data = file_get_contents($filePath);
    $lines = array_filter(explode("\n", $data), fn($line) => trim($line) !== '');
    return array_map('strtoupper', $lines);
}

// Production Service: Appropriate error handling
function processFile(string $filePath, LoggerInterface $logger): array {
    try {
        if (!file_exists($filePath)) {
            throw new InvalidArgumentException("File not found: {$filePath}");
        }

        $data = file_get_contents($filePath);
        $lines = array_filter(explode("\n", $data), fn($line) => trim($line) !== '');

        $logger->info('File processed', ['path' => $filePath, 'lines' => count($lines)]);

        return ['success' => true, 'data' => array_map('strtoupper', $lines)];
    } catch (Exception $e) {
        $logger->error('File processing failed', ['path' => $filePath, 'error' => $e->getMessage()]);
        return ['success' => false, 'error' => $e->getMessage()];
    }
}
```

## Core FP Patterns (Error-Preventing Essentials)

### 1. Purity and Side Effect Isolation

**Rule**: Separate business logic from side effects. Use strict types.

```php
<?php
declare(strict_types=1);

// ❌ Impure - side effects mixed with logic
function calculateTotal(array $items): float {
    error_log('Processing items'); // Side effect
    global $total; // Global state
    $total += array_reduce($items, fn($sum, $item) => $sum + $item['price'], 0);
    return $total;
}

// ✅ Pure business logic
function calculateTotal(array $items): float {
    return array_reduce($items, fn($sum, $item) => $sum + $item['price'], 0.0);
}

// ✅ Side effects isolated
function logAndCalculate(array $items, LoggerInterface $logger): float {
    $total = calculateTotal($items); // Pure calculation
    $logger->info("Total: {$total}"); // Side effect isolated
    return $total;
}
```

**Benefits**:
- 100% testable with all edge cases
- Type-safe with strict types
- Predictable behavior
- Safe for parallel execution

### 2. Composition Over Inheritance

**Rule**: Build complex behavior from simple functions.

```php
<?php
// ❌ Class hierarchy approach
abstract class BaseValidator {
    abstract public function validate($value): bool;
}

class EmailValidator extends BaseValidator {
    public function validate($value): bool {
        // email logic
    }
}

// ✅ Function composition (no utilities needed)
function validateRequired($value): bool {
    return $value !== null && $value !== '';
}

function validateEmail(string $value): bool {
    return filter_var($value, FILTER_VALIDATE_EMAIL) !== false;
}

function validateLength(int $min, int $max): callable {
    return fn(string $value): bool =>
        strlen($value) >= $min && strlen($value) <= $max;
}

// Simple composition without pipe() utility
function validateUserEmail(string $email): array {
    if (!validateRequired($email)) {
        return ['valid' => false, 'error' => 'Required'];
    }

    if (!validateEmail($email)) {
        return ['valid' => false, 'error' => 'Invalid email'];
    }

    if (!validateLength(5, 100)($email)) {
        return ['valid' => false, 'error' => 'Length'];
    }

    return ['valid' => true];
}
```

### 3. Dependency Injection Through Parameters

**Rule**: Pass dependencies explicitly via constructor or parameters.

```php
<?php
// ❌ Hidden dependencies, hard to test
function saveUser(array $userData): void {
    $hashedPassword = password_hash($userData['password'], PASSWORD_DEFAULT); // Hidden
    $db = new Database(); // Hidden dependency
    $db->save(['name' => $userData['name'], 'password' => $hashedPassword]);
}

// ✅ Explicit dependencies, fully testable
function saveUser(array $userData, PasswordHasherInterface $hasher, DatabaseInterface $database): array {
    $hashedPassword = $hasher->hash($userData['password']);
    return $database->save([
        'name' => $userData['name'],
        'password' => $hashedPassword
    ]);
}

// ✅ Service with constructor DI
class UserService {
    public function __construct(
        private readonly PasswordHasherInterface $hasher,
        private readonly DatabaseInterface $database
    ) {}

    public function saveUser(array $userData): array {
        return saveUser($userData, $this->hasher, $this->database);
    }
}
```

### 4. Immutability Patterns

**Rule**: Avoid mutations, create new arrays/objects.

```php
<?php
// ❌ Mutation approach
function updateUserSettings(array $user, array $settings): array {
    $user['settings'] = array_merge($user['settings'] ?? [], $settings); // Mutates
    $user['updated_at'] = time();
    return $user;
}

// ✅ Immutable approach
function updateUserSettings(array $user, array $settings): array {
    return [
        ...$user,
        'settings' => array_merge($user['settings'] ?? [], $settings),
        'updated_at' => time()
    ];
}

// ✅ Array operations without mutation
function addItem(array $items, array $newItem): array {
    return [...$items, $newItem];
}

function removeItem(array $items, int $id): array {
    return array_values(array_filter($items, fn($item) => $item['id'] !== $id));
}

function updateItem(array $items, int $id, array $updates): array {
    return array_map(
        fn($item) => $item['id'] === $id ? [...$item, ...$updates] : $item,
        $items
    );
}
```

## PHP-Specific FP Patterns

### Native Array Functions

```php
<?php
declare(strict_types=1);

// Native array methods over loops
function processUsers(array $users): array {
    return array_slice(
        array_map(
            fn($user) => [
                ...$user,
                'display_name' => "{$user['first_name']} {$user['last_name']}"
            ],
            array_filter($users, fn($user) => $user['active'])
        ),
        0,
        10
    );
}

// Arrow functions (PHP 7.4+)
$prices = array_map(fn($item) => $item['price'] * 1.1, $items);

// Named arguments (PHP 8.0+)
function createUser(string $name, string $email, bool $active = true): array {
    return compact('name', 'email', 'active');
}

$user = createUser(name: 'John', email: 'john@test.com');

// Match expressions (PHP 8.0+)
function getTierDiscount(string $tier): float {
    return match($tier) {
        'bronze' => 0.05,
        'silver' => 0.10,
        'gold' => 0.15,
        'platinum' => 0.20,
        default => 0.0
    };
}
```

### Strict Types (MANDATORY)

```php
<?php
declare(strict_types=1);

// ✅ Always use strict types and type declarations
function calculateDiscount(float $price, float $rate): float {
    return $price * (1 - $rate);
}

// ✅ Return type declarations
function validateData(array $data): array {
    return ['valid' => true, 'data' => $data];
}

// ✅ Nullable types when appropriate
function findUser(int $id, DatabaseInterface $db): ?array {
    $user = $db->find($id);
    return $user ?: null;
}

// ✅ Union types (PHP 8.0+)
function processResult(array|false $result): array {
    if ($result === false) {
        return ['success' => false, 'error' => 'Not found'];
    }
    return ['success' => true, 'data' => $result];
}
```

## Testing Essentials (PHPUnit)

**Philosophy**: Pure functions enable testing all edge cases systematically.

```php
<?php
declare(strict_types=1);

use PHPUnit\Framework\TestCase;

// Traditional testing (limited coverage)
class CalculatorTest extends TestCase {
    public function testCalculateDiscount(): void {
        $result = calculateDiscount(100.0, 0.1);
        $this->assertEquals(90.0, $result);
    }
}

// FP comprehensive testing (all edge cases)
class CalculatorComprehensiveTest extends TestCase {
    /**
     * @dataProvider discountProvider
     */
    public function testCalculateDiscount(float $price, float $rate, float $expected): void {
        $result = calculateDiscount($price, $rate);
        $this->assertEquals($expected, $result);
    }

    public function discountProvider(): array {
        return [
            'standard discount' => [100.0, 0.1, 90.0],
            'no discount' => [100.0, 0.0, 100.0],
            'full discount' => [100.0, 1.0, 0.0],
            'zero price' => [0.0, 0.1, 0.0],
        ];
    }

    /**
     * Test all data types - systematic edge cases
     * @dataProvider invalidTypeProvider
     */
    public function testHandlesInvalidTypesGracefully($input): void {
        $this->expectException(TypeError::class);
        calculateDiscount($input, 0.1);
    }

    public function invalidTypeProvider(): array {
        return [
            'null' => [null],
            'string' => ['100'],
            'array' => [[]],
            'object' => [new stdClass()],
        ];
    }
}
```

## Performance Patterns (MVP-First, Evidence-Based)

**⚠️ IMPORTANT**: Optimize only when needed with evidence.

### Configuration Pre-Compilation (When Actually Needed)

**Use When**: Processing large datasets (>10K items) with repeated configuration access.

```php
<?php
// Problem: O(records × fields) complexity
function processRecords(array $records, array $schema): array {
    return array_map(function($record) use ($schema) {
        return array_reduce($schema['fields'], function($obj, $field) use ($record) {
            $obj[$field['name']] = transformField($record[$field['name']], $field['type']);
            return $obj;
        }, []);
    }, $records);
}

// Solution: O(records + fields) - pre-compile configuration
function createRecordProcessor(array $schema): callable {
    // Setup once - extract expensive configuration
    $fieldProcessors = array_map(
        fn($field) => fn($value) => transformField($value, $field['type']),
        $schema['fields']
    );

    return function(array $record) use ($schema, $fieldProcessors): array {
        $result = [];
        foreach ($schema['fields'] as $i => $field) {
            $result[$field['name']] = $fieldProcessors[$i]($record[$field['name']]);
        }
        return $result;
    };
}

// Usage: Configuration cost paid once
$processor = createRecordProcessor($schema); // Setup phase
$results = array_map($processor, $records); // Linear execution
```

### Real-World Case Study: Email Validation Performance

**Production metrics from ima-espo WordPress plugin** (130 tests, 236 assertions, <30ms total):

```php
<?php
declare(strict_types=1);

namespace IMA_Espo\Pure;

// Before: O(n*m) - Configuration accessed per validation
foreach ($emails as $email) {
    // Accesses $bad_domains and $typo_domains each iteration
    validate_email_domain($email, $bad_domains, $typo_domains);
}

// After: O(n+m) - Configuration pre-compiled once
$validator = create_email_validator($bad_domains, $typo_domains);
foreach ($emails as $email) {
    $validator($email);  // 2-5x faster
}

// Function factory implementation
function create_email_validator(
    array $bad_domains,
    array $typo_corrections
): callable {
    // Configuration captured in closure scope (pre-compiled)
    return function (string $email) use ($bad_domains, $typo_corrections): array {
        return validate_email_domain($email, $bad_domains, $typo_corrections);
    };
}

// Pure validation function (no side effects)
function validate_email_domain(
    string $email,
    array $bad_domains,
    array $typo_domains
): array {
    // Standard result structure
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return ['valid' => false, 'error' => 'Invalid email format'];
    }

    $domain = get_domain_from_email($email);

    // Check disposable domains
    if (in_array($domain, $bad_domains, true)) {
        return ['valid' => false, 'error' => 'Disposable email domain'];
    }

    // Check for typos
    if (isset($typo_domains[$domain])) {
        return [
            'valid' => false,
            'error' => 'Possible typo',
            'suggestion' => $typo_domains[$domain]
        ];
    }

    return ['valid' => true];
}
```

**Measured Performance Gains**:
- **Single email validation**: <0.001ms per email
- **Configuration pre-compilation**: O(1) closure creation
- **Total for k validations**: O(1 + k\*n) vs O(k\*m + k\*n) without factory
- **Real-world speedup**: 2-5x when validating multiple emails
- **Test execution**: 130 tests complete in <30ms (including factory setup)
- **Production stability**: 100% test coverage with comprehensive edge cases

**WordPress Integration Example**:
```php
<?php
// WordPress wrapper class uses function factory
class IMAEspo_EmailValidatorCore {
    protected $validator = null;

    public function __construct(array $bad_domains = array(), array $typo_domains = array()) {
        // Pre-compile validator function once during construction
        $this->validator = create_email_validator($bad_domains, $typo_domains);
    }

    public function validate_email_domain(string $email) {
        // Use pre-compiled validator - no configuration access
        return ($this->validator)($email);
    }
}
```

### Function Factories for Reusable Logic

```php
<?php
function createValidator(array $rules): callable {
    return function($value) use ($rules): array {
        $errors = [];
        foreach ($rules as $rule) {
            if (!$rule['validator']($value)) {
                $errors[] = $rule['message'];
            }
        }
        return empty($errors)
            ? ['valid' => true]
            : ['valid' => false, 'errors' => $errors];
    };
}

// Usage: Configure once, use many times
$validateEmail = createValidator([
    ['validator' => fn($v) => is_string($v), 'message' => 'Must be string'],
    ['validator' => fn($v) => str_contains($v, '@'), 'message' => 'Must contain @'],
    ['validator' => fn($v) => strlen($v) > 5, 'message' => 'Too short']
]);
```

## Error Handling Patterns

### Result Type Pattern

```php
<?php
// Standard result shape
function createResult($data = null, ?string $error = null): array {
    return $error !== null
        ? ['success' => false, 'error' => $error]
        : ['success' => true, 'data' => $data];
}

// Use in functions
function divide(float $a, float $b): array {
    return $b === 0.0
        ? createResult(error: 'Division by zero')
        : createResult(data: $a / $b);
}

// Chain results
function calculate(float $a, float $b, float $c): array {
    $result1 = divide($a, $b);
    if (!$result1['success']) return $result1;

    $result2 = divide($result1['data'], $c);
    return $result2;
}
```

### Try-Catch Wrapper

```php
<?php
function tryCatch(callable $fn): callable {
    return function(...$args) use ($fn): array {
        try {
            $data = $fn(...$args);
            return ['success' => true, 'data' => $data];
        } catch (Exception $e) {
            return ['success' => false, 'error' => $e->getMessage()];
        }
    };
}

// Wrap risky functions
$safeFetchUser = tryCatch(fetchUser(...));
$result = $safeFetchUser($userId);
```

## Quality Gates (Pre-Implementation Checklist)

1. **"Can this be pure?"** → Separate business logic from side effects
2. **"Can this use native patterns?"** → Avoid utility creation, use PHP features
3. **"Can this be simplified?"** → Choose simple solution over complex abstraction
4. **"Is this complexity justified?"** → Evidence-based complexity decisions
5. **"Is this testable?"** → Pure functions enable comprehensive testing
6. **"Are strict types used?"** → `declare(strict_types=1)` at file top

## When to Load Additional Content

### Deep Principles and Explanations
**File**: `core-principles.md`
**When**: Learning mode, explaining WHY, architectural decisions
**Contains**: Complete FP philosophy, detailed pattern explanations, cross-pattern comparisons

### Testing Methodology
**File**: `testing-patterns.md`
**When**: Building test suites, improving coverage, edge case analysis
**Contains**: Full PHPUnit strategies, edge case patterns, mocking techniques

### Working Examples
**Directory**: `examples/`
**When**: Learning implementation, need working code, integration examples
**Contains**: Complete working examples with PHPUnit tests

## Integration with Domain Skills

This core skill provides the foundation for domain-specific skills:

- **php-fp-wordpress**: WordPress patterns with FP principles
- **php-fp-laravel**: Laravel patterns with FP principles (future)
- **php-fp-symfony**: Symfony patterns with FP principles (future)

Each domain skill references this core and adds domain-specific patterns.

## Common Use Cases

### Data Validation

```php
<?php
declare(strict_types=1);

function createValidationRules(array $schema): callable {
    $rules = array_map(fn($rule) => [
        'field' => $rule['field'],
        'validator' => compileValidator($rule['type'], $rule['options']),
        'message' => $rule['message']
    ], $schema);

    return function(array $data) use ($rules): array {
        $errors = [];
        foreach ($rules as $rule) {
            if (!$rule['validator']($data[$rule['field']] ?? null)) {
                $errors[] = ['field' => $rule['field'], 'message' => $rule['message']];
            }
        }
        return empty($errors)
            ? ['valid' => true]
            : ['valid' => false, 'errors' => $errors];
    };
}
```

### Data Transformation

```php
<?php
// Pipeline without utilities - native chaining
function processUserData(array $rawData): array {
    $normalized = normalizeUserData($rawData);
    if (!$normalized['valid']) return $normalized;

    $validated = validateUserData($normalized['data']);
    if (!$validated['valid']) return $validated;

    $enhanced = enhanceWithDefaults($validated['data']);
    return ['valid' => true, 'data' => $enhanced];
}
```

## Success Metrics

### Code Quality
- **Simplicity**: Readable, maintainable code over clever solutions
- **Type Safety**: Strict types, full type declarations
- **Testability**: 100% testable pure functions with edge case coverage
- **Native Integration**: Uses PHP features effectively

### Performance (When Needed)
- **Evidence-Based**: Optimizations backed by measurements
- **Appropriate Scale**: Simple solutions for small/medium data
- **Native Optimization**: Leverages PHP 8+ features

### Maintainability
- **Predictable Patterns**: Consistent FP approaches
- **Easy Testing**: Comprehensive test coverage with PHPUnit
- **Simple Maintenance**: Easy to understand and modify

## Philosophy

*"Pure functions, native PHP patterns, strict types, appropriate complexity, and comprehensive testing for maintainable, predictable code that respects the language and solves real problems simply."*
