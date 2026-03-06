---
name: "unit-testing"
description: "Test workflow orchestration — decision tree routing to domain skills (phpunit-wp, playwright, js-fp, php-fp). TDD, test strategy, mock decisions, quality checklists. Triggers on: unit test, write tests, TDD, test coverage, mock, test strategy."
---

# Unit Testing - Orchestration Skill

**"Test pure core, not impure shell. FP makes testing easy."**

This skill orchestrates test workflows by routing to the right domain skills. It does NOT duplicate domain-specific testing patterns — it coordinates them.

## Core Philosophy

Pure functions are trivially testable. If something is hard to test, the problem is the code design, not the test setup.

1. **Extract pure logic** — separate decisions from effects
2. **Test behavior, not implementation** — what it does, not how
3. **Bottom-heavy pyramid** — many unit tests, few integration, fewer E2E
4. **Minimal mocking** — mock boundaries (DB, network, filesystem), not your own code

## Decision Tree: Which Skills to Use

```
What are you testing?
├── WordPress PHP plugin/theme?
│   → phpunit-wp (primary) + php-fp + php-fp-wordpress
│   → References: php-fp/references/testing-patterns.md
│                  php-fp-wordpress/references/testing-strategy.md
│
├── General PHP (non-WordPress)?
│   → php-fp (primary)
│   → References: php-fp/references/testing-patterns.md
│
├── JavaScript/TypeScript?
│   ├── React components?
│   │   → js-fp-react + js-fp
│   ├── Vue components?
│   │   → js-fp-vue + js-fp
│   │   → References: js-fp-vue/references/testing.md
│   └── General JS/TS?
│       → js-fp (primary)
│       → References: js-fp/references/testing-patterns.md
│
├── End-to-end / browser tests?
│   → playwright (primary)
│
└── Unknown / mixed?
    → Start with functional-programmer principles
    → Route to domain skill once context is clear
```

**Always apply:** `functional-programmer` principles (pure functions, composition, immutability).

## Workflow: Adding Tests to Existing Code

### Step 1: Analyze

- Read the code under test
- Identify pure functions vs impure boundaries
- Map dependencies: what does this code touch? (DB, filesystem, network, global state)

### Step 2: Classify

| Code Type | Test Type | Speed | Mocking |
|-----------|-----------|-------|---------|
| Pure function (no side effects) | Unit test | Fast (<10ms) | None |
| Function with injected deps | Unit test | Fast | Stub the deps |
| WordPress hook/filter callback | Unit or integration | Medium | Mock WP functions |
| API endpoint handler | Integration test | Medium | Mock external services |
| Full user workflow | E2E test | Slow | None (real browser) |

### Step 3: Structure

Follow project conventions for test file location:
- PHP: `tests/Unit/`, `tests/Integration/` (mirror `src/` structure)
- JS/TS: colocated `*.test.ts` or `__tests__/` directory
- E2E: `tests/e2e/` or `e2e/`

### Step 4: Write

Apply the domain skill's patterns. General principles:

```
Arrange → Act → Assert (one behavior per test)
```

- **Test name = behavior description**: `it('returns empty array when no items match filter')`
- **One assertion per concept** (multiple `expect` calls are fine if they verify one behavior)
- **No logic in tests**: no conditionals, no loops, no try/catch
- **Test data is minimal**: only include fields relevant to the behavior under test

### Step 5: Verify

- Run the test suite: `composer test`, `npm test`, `npx vitest`, etc.
- All tests pass (green)
- No skipped or pending tests without a documented reason
- Coverage meets project floor (if configured)

## Workflow: TDD (Test-Driven Development)

### Red-Green-Refactor

```
1. RED    — Write a failing test for the next behavior
2. GREEN  — Write the minimum code to make it pass
3. REFACTOR — Clean up while keeping tests green
```

### TDD with Pure Functions (Ideal Case)

Pure functions + TDD = fast feedback loops. No setup, no teardown, no mocking.

```
Test: add(2, 3) === 5
Code: const add = (a, b) => a + b
Done.
```

### TDD for Impure Boundaries

When TDD hits an impure boundary (DB, network, filesystem):

1. **Define the interface** — what does the boundary need to provide?
2. **Stub the boundary** — test against the interface, not the implementation
3. **Wire up later** — connect the real implementation after the pure logic is tested

### When TDD Slows You Down

TDD is a tool, not a religion. Skip it when:
- Exploring/prototyping (you'll throw the code away)
- The implementation is trivial and obvious
- You're writing glue code with no logic

See `references/tdd-workflow.md` for detailed mechanics.

## Mock Decision Tree

```
Is the dependency hard to test?
├── No (pure function, simple data) → Don't mock. Test directly.
├── Yes, but I own the code
│   ├── Can I extract pure logic? → Extract it. Test the pure part.
│   └── Can I inject the dependency? → Inject it. Pass a stub.
└── Yes, external service (DB, API, filesystem, time)
    → Mock it. Use the simplest mock type that works.
```

### Mock Types (Simplest First)

| Type | What it does | When to use |
|------|-------------|-------------|
| **Stub** | Returns canned data | Most cases. Default choice. |
| **Spy** | Records calls for verification | When you need to verify a call was made |
| **Fake** | Working simplified implementation | Complex interfaces (in-memory DB) |
| **Full mock** | Strict expectations on calls | Almost never. Couples tests to implementation. |

See `references/mock-patterns.md` for language-specific examples and anti-patterns.

## Test Quality Checklist

Before considering tests "done":

- [ ] Tests verify behavior, not implementation
- [ ] Each test has a descriptive name explaining the scenario
- [ ] No test depends on another test's state (isolation)
- [ ] No flaky signals: no timers, no real network, no filesystem in unit tests
- [ ] Pure functions tested without mocking
- [ ] Mocks used only at impure boundaries
- [ ] Edge cases covered: empty input, null/undefined, boundary values
- [ ] Error paths tested (not just happy path)
- [ ] Test runs fast (unit suite < 10s for most projects)

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Testing implementation details | Breaks on refactor | Test behavior/output instead |
| Mocking everything | Tests prove nothing | Extract pure logic, mock only boundaries |
| Giant test setup | Hard to understand | Simplify code under test or use factories |
| Copy-paste test bodies | Maintenance nightmare | Use parameterized/table-driven tests |
| Testing framework behavior | Wastes time | Trust the framework |
| 100% coverage target | Diminishing returns | Set a floor, not a ceiling |
| `sleep()` in tests | Flaky, slow | Use deterministic waits or fix the design |

## Integration: Domain Skill Reference

| Context | Primary Skill | Reference Files |
|---------|--------------|-----------------|
| WordPress PHP | `phpunit-wp` | `php-fp/references/testing-patterns.md`, `php-fp-wordpress/references/testing-strategy.md` |
| General PHP | `php-fp` | `php-fp/references/testing-patterns.md` |
| JavaScript/TypeScript | `js-fp` | `js-fp/references/testing-patterns.md` |
| Vue.js | `js-fp-vue` | `js-fp-vue/references/testing.md` |
| React | `js-fp-react` | `js-fp/references/testing-patterns.md` |
| E2E / Browser | `playwright` | (self-contained skill) |

## The Final Word

*"If it's hard to test, it's hard to use. Testability is a design signal, not a chore. Extract the pure, inject the impure, and the tests write themselves."*
