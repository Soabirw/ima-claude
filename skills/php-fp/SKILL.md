---
name: "php-fp"
description: "Core FP principles with anti-over-engineering focus - Simple > Complex | Evidence > Assumptions"
---

# PHP Functional Programming

Core functional programming principles for PHP with anti-over-engineering enforcement. This skill provides error-preventing essentials and references to deep-dive content.

## When to Use This Skill

- Implementing pure, testable PHP functions
- Need FP architectural guidance for PHP
- Preventing over-engineering and custom FP utility creation
- Comprehensive testing strategies with PHPUnit
- Evidence-based performance optimization

## CRITICAL: Anti-Over-Engineering (PRIMARY FOCUS)

**Core Principle**: "Simple > Complex | Evidence > Assumptions"

> **Clarification**: This skill prevents CREATING custom FP utility functions (pipe, compose, curry) to make PHP "feel" like Haskell. Using established libraries (Carbon, Collections, etc.) is perfectly fine. FP is a mindset—pure functions, immutability, composition—not a rigid API signature.

### Don't Create Custom FP Utilities

```php
<?php
// DON'T CREATE: pipe() utility
function pipe(...$functions) {
    return fn($value) => array_reduce($functions, fn($carry, $fn) => $fn($carry), $value);
}

// INSTEAD: Native early returns
function validateUser(array $userData): array {
    $requiredCheck = validateRequired(['email', 'name'], $userData);
    if (!$requiredCheck['valid']) return $requiredCheck;
    return validateEmail($userData);
}

// DON'T CREATE: curry() utility
// INSTEAD: Native closures
function createValidator(array $rules): callable {
    return fn($value): array => ['valid' => empty(array_filter($rules, fn($r) => !$r['validator']($value)))];
}

// DON'T CREATE: Complex monad implementations
// INSTEAD: Simple result arrays
function divide(float $a, float $b): array {
    return $b === 0.0 ? ['success' => false, 'error' => 'Division by zero'] : ['success' => true, 'data' => $a / $b];
}
```

### The 4-Question Quality Framework

Before extracting or abstracting, ask:

1. **"Can this be pure?"** - Separate business logic from side effects
2. **"Can this use native patterns?"** - Avoid creating custom FP utilities, use PHP features
3. **"Can this be simplified?"** - Choose simple solution over complex abstraction
4. **"Is this complexity justified?"** - Evidence-based complexity decisions

### When NOT to Extract: WordPress Example

**Context**: CRMAPI class sends webhook data via HTTP POST.

**Analysis**: Applied 4-question framework - NO pure function extraction needed.

- `sanitize_data()` uses `sanitize_text_field()` which applies WordPress filters - NOT PURE
- `send_api_request()` uses WordPress HTTP API - NATIVE PATTERNS ALREADY
- Current structure: 239 lines, ~35 lines of logic - ALREADY SIMPLE
- Extraction would add indirection without benefits - NOT JUSTIFIED

**Result**: Grade B+ (Appropriate WordPress Wrapper). Don't extract pure functions when WordPress integration IS the business logic.

### Context-Appropriate Complexity

```php
<?php
// CLI Script: Simple and direct
function processFile(string $filePath): array {
    $data = file_get_contents($filePath);
    return array_map('strtoupper', array_filter(explode("\n", $data), fn($l) => trim($l) !== ''));
}

// Production Service: Appropriate error handling
function processFile(string $filePath, LoggerInterface $logger): array {
    try {
        if (!file_exists($filePath)) throw new InvalidArgumentException("File not found: {$filePath}");
        $lines = array_filter(explode("\n", file_get_contents($filePath)), fn($l) => trim($l) !== '');
        $logger->info('File processed', ['path' => $filePath, 'lines' => count($lines)]);
        return ['success' => true, 'data' => array_map('strtoupper', $lines)];
    } catch (Exception $e) {
        $logger->error('File processing failed', ['path' => $filePath, 'error' => $e->getMessage()]);
        return ['success' => false, 'error' => $e->getMessage()];
    }
}
```

## Core FP Patterns (Quick Reference)

### 1. Purity and Side Effect Isolation

```php
<?php
declare(strict_types=1);

// PURE: business logic
function calculateTotal(array $items): float {
    return array_reduce($items, fn($sum, $item) => $sum + $item['price'], 0.0);
}

// ISOLATED: side effects separate
function logAndCalculate(array $items, LoggerInterface $logger): float {
    $total = calculateTotal($items);
    $logger->info("Total: {$total}");
    return $total;
}
```

### 2. Composition Over Inheritance

```php
<?php
// Simple validators that compose
function validateRequired($value): bool { return $value !== null && $value !== ''; }
function validateEmail(string $value): bool { return filter_var($value, FILTER_VALIDATE_EMAIL) !== false; }
function validateLength(int $min, int $max): callable {
    return fn(string $value): bool => strlen($value) >= $min && strlen($value) <= $max;
}

// Composition without utilities
function validateUserEmail(string $email): array {
    if (!validateRequired($email)) return ['valid' => false, 'error' => 'Required'];
    if (!validateEmail($email)) return ['valid' => false, 'error' => 'Invalid email'];
    if (!validateLength(5, 100)($email)) return ['valid' => false, 'error' => 'Length'];
    return ['valid' => true];
}
```

### 3. Dependency Injection

```php
<?php
// Explicit dependencies, fully testable
function saveUser(array $userData, PasswordHasherInterface $hasher, DatabaseInterface $db): array {
    return $db->save(['name' => $userData['name'], 'password' => $hasher->hash($userData['password'])]);
}

// Service with constructor DI
class UserService {
    public function __construct(
        private readonly PasswordHasherInterface $hasher,
        private readonly DatabaseInterface $db
    ) {}

    public function saveUser(array $userData): array {
        return saveUser($userData, $this->hasher, $this->db);
    }
}
```

### 4. Immutability

```php
<?php
// Always return new arrays
function updateUserSettings(array $user, array $settings): array {
    return [...$user, 'settings' => array_merge($user['settings'] ?? [], $settings), 'updated_at' => time()];
}

function addItem(array $items, array $newItem): array { return [...$items, $newItem]; }
function removeItem(array $items, int $id): array { return array_values(array_filter($items, fn($i) => $i['id'] !== $id)); }
function updateItem(array $items, int $id, array $updates): array {
    return array_map(fn($i) => $i['id'] === $id ? [...$i, ...$updates] : $i, $items);
}
```

## PHP-Specific Patterns

### Native Array Functions + Strict Types (MANDATORY)

```php
<?php
declare(strict_types=1);

// Native array methods over loops
function processUsers(array $users): array {
    return array_slice(
        array_map(fn($u) => [...$u, 'display_name' => "{$u['first_name']} {$u['last_name']}"],
            array_filter($users, fn($u) => $u['active'])),
        0, 10
    );
}

// Match expressions (PHP 8.0+)
function getTierDiscount(string $tier): float {
    return match($tier) {
        'bronze' => 0.05, 'silver' => 0.10, 'gold' => 0.15, 'platinum' => 0.20, default => 0.0
    };
}

// Union types (PHP 8.0+)
function processResult(array|false $result): array {
    return $result === false ? ['success' => false, 'error' => 'Not found'] : ['success' => true, 'data' => $result];
}
```

## Result Type Pattern

```php
<?php
// Standard result shape
function createResult($data = null, ?string $error = null): array {
    return $error !== null ? ['success' => false, 'error' => $error] : ['success' => true, 'data' => $data];
}

// Chain results with early return
function calculate(float $a, float $b, float $c): array {
    $r1 = divide($a, $b);
    if (!$r1['success']) return $r1;
    return divide($r1['data'], $c);
}
```

> **Deep dive**: See `references/core-principles.md` for complete Result Type patterns and error handling strategies.

## Testing Essentials

Pure functions enable testing ALL edge cases systematically.

```php
<?php
use PHPUnit\Framework\TestCase;

class CalculatorTest extends TestCase {
    /**
     * @dataProvider discountProvider
     */
    public function testCalculateDiscount(float $price, float $rate, float $expected): void {
        $this->assertEquals($expected, calculateDiscount($price, $rate));
    }

    public function discountProvider(): array {
        return [
            'standard' => [100.0, 0.1, 90.0],
            'zero' => [100.0, 0.0, 100.0],
            'full' => [100.0, 1.0, 0.0],
        ];
    }
}
```

> **Deep dive**: See `references/testing-patterns.md` for comprehensive PHPUnit strategies, edge case patterns, mocking, and test organization.

## Performance Patterns (Evidence-Based)

Optimize only when needed with evidence. Key pattern: **Configuration Pre-Compilation**.

```php
<?php
// Problem: O(records x config) - config accessed every iteration
// Solution: Pre-compile configuration once

function createRecordProcessor(array $schema): callable {
    // Setup once
    $fieldProcessors = array_map(fn($f) => fn($v) => transformField($v, $f['type']), $schema['fields']);

    return function(array $record) use ($schema, $fieldProcessors): array {
        $result = [];
        foreach ($schema['fields'] as $i => $field) {
            $result[$field['name']] = $fieldProcessors[$i]($record[$field['name']]);
        }
        return $result;
    };
}

$processor = createRecordProcessor($schema); // Setup phase
$results = array_map($processor, $records);  // Linear execution
```

**Real-world result**: Email validation in ima-espo achieved 2-5x speedup with function factory pattern. 130 tests, 236 assertions, <30ms total.

## Quality Gates Checklist

Before implementation:

1. **"Can this be pure?"** - Separate business logic from side effects
2. **"Can this use native patterns?"** - Avoid creating custom FP utilities
3. **"Can this be simplified?"** - Simple > complex
4. **"Is this complexity justified?"** - Evidence required
5. **"Is this testable?"** - Pure functions enable comprehensive testing
6. **"Are strict types used?"** - `declare(strict_types=1)` at file top

## When to Load Reference Files

### Deep Principles and Explanations
**File**: `references/core-principles.md`
**Load when**:
- Learning mode or explaining WHY behind patterns
- Making architectural decisions
- Need complete Result Type patterns
- Anti-pattern recognition details
- Cross-pattern comparisons

### Testing Methodology
**File**: `references/testing-patterns.md`
**Load when**:
- Building comprehensive test suites
- Improving test coverage
- Edge case analysis and boundary testing
- Setting up mocking strategies
- Performance testing pure functions

### Working Examples
**Directory**: `examples/`
**Load when**:
- Need complete working code
- Integration examples
- Learning implementation patterns

## Integration with Domain Skills

This core skill provides the foundation for:

- **php-fp-wordpress**: WordPress patterns with FP principles
- **php-fp-laravel**: Laravel patterns with FP principles (future)
- **php-fp-symfony**: Symfony patterns with FP principles (future)

Each domain skill references this core and adds domain-specific patterns.

## Philosophy

*"Pure functions, native PHP patterns, strict types, appropriate complexity, and comprehensive testing for maintainable, predictable code that respects the language and solves real problems simply."*
