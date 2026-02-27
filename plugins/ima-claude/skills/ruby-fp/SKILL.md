---
name: "ruby-fp"
description: "Functional Ruby patterns - Enumerable as FP toolkit, lambdas, freeze, functional core/imperative shell"
---

# Ruby FP

Ruby is OOP-first, but its FP toolkit is excellent. The goal is **functional core, imperative shell** — pure methods for logic, OOP shell only where the framework demands it.

## When to Use This Skill

- Writing standalone Ruby scripts
- Building Ruby utilities or service objects
- Refactoring procedural Ruby toward composable units
- Any Ruby code where framework conventions don't dictate the pattern

## Core Philosophy

> Ruby's Enumerable is a functional toolkit hiding inside an OOP language.

The architect's lens applied to Ruby:
- **Pure methods** for logic (no instance variable mutation in calculation methods)
- **Enumerable over explicit loops** — `map/select/reduce` not `each` + accumulator
- **Lambdas** for first-class functions (strict arity, `lambda?` is true, `return` is scoped)
- **freeze** for value objects and constants
- **Functional core** isolated from I/O, database, external state

Ruby will never be Haskell. Don't fight the language — compose with it.

## Enumerable: The FP Toolkit

These are your primary tools. Prefer them over `each` + mutation.

```ruby
users = [
  { name: 'Alice', age: 30, active: true },
  { name: 'Bob',   age: 17, active: false },
  { name: 'Carol', age: 25, active: true }
]

# select — filter
adults = users.select { |u| u[:age] >= 18 }

# map — transform
names = users.map { |u| u[:name] }

# reduce — accumulate
total_age = users.reduce(0) { |sum, u| sum + u[:age] }

# filter_map — select + transform in one pass (Ruby 2.7+, preferred)
active_names = users.filter_map { |u| u[:name] if u[:active] }

# flat_map — map + flatten
tags = posts.flat_map { |p| p[:tags] }

# each_with_object — build a hash/array without external mutation
index = users.each_with_object({}) { |u, h| h[u[:name]] = u[:age] }

# group_by — partition
by_status = users.group_by { |u| u[:active] ? :active : :inactive }

# Chaining — functional pipeline
result = users
  .select { |u| u[:active] }
  .map { |u| u.merge(display_name: u[:name].upcase) }
  .sort_by { |u| u[:age] }
```

**Rule**: If you find yourself writing `results = []; collection.each { |x| results << x if ... }`, reach for `filter_map` instead.

## Lambdas vs Procs

Use `lambda` (or `->`) for reusable, composable functions. Avoid bare `proc` for logic units.

```ruby
# Lambda — strict arity, scoped return, first-class function
validate_age = ->(age) { age.is_a?(Integer) && age >= 0 && age <= 150 }
normalize_email = ->(email) { email.to_s.strip.downcase }

# Compose with >> (Ruby 2.6+)
process_user = normalize_email >> method(:save_user)

# Use as argument (higher-order functions)
def transform_all(items, transformer)
  items.map(&transformer)
end

transform_all(emails, normalize_email)

# Method references — convert instance/class methods to callables
validator = method(:validate_age)
emails.map(&method(:normalize_email))
```

**Lambda vs Proc differences that matter:**
| | Lambda | Proc |
|-|--------|------|
| Arity | Strict (raises ArgumentError) | Loose (fills nil) |
| `return` | Exits lambda only | Exits enclosing method |
| Use for | Reusable functions, composition | Blocks, iterators |

## Immutability with freeze

```ruby
# Freeze constants
VALID_STATUSES = %w[active inactive pending].freeze
DEFAULT_CONFIG = { timeout: 30, retries: 3 }.freeze

# Value object pattern — frozen struct
UserRecord = Data.define(:name, :email, :age)  # Ruby 3.2+
user = UserRecord.new(name: 'Alice', email: 'alice@example.com', age: 30)
# user is immutable — no setters

# For older Ruby, use Struct with freeze
Config = Struct.new(:host, :port, :timeout).new('localhost', 5432, 30).freeze
```

**Rule**: Any hash/array used as a constant gets `.freeze`. Value objects use `Data.define` (Ruby 3.2+) or frozen `Struct`.

## Functional Core / Imperative Shell

The central pattern. Separate pure logic from I/O and external state.

```ruby
# PURE CORE — no I/O, no DB, fully testable, no side effects
module UserLogic
  def self.validate(attrs)
    errors = []
    errors << "Name required" if attrs[:name].to_s.strip.empty?
    errors << "Invalid email" unless attrs[:email].to_s.include?('@')
    errors << "Age must be 18+" if attrs[:age].to_i < 18
    errors
  end

  def self.normalize(attrs)
    attrs.merge(
      name: attrs[:name].to_s.strip,
      email: attrs[:email].to_s.strip.downcase
    )
  end

  def self.prepare_for_save(raw_attrs)
    normalized = normalize(raw_attrs)
    errors = validate(normalized)
    errors.empty? ? { ok: true, attrs: normalized } : { ok: false, errors: errors }
  end
end

# IMPERATIVE SHELL — orchestrates I/O, calls pure core
def create_user(raw_params)
  result = UserLogic.prepare_for_save(raw_params)
  return { success: false, errors: result[:errors] } unless result[:ok]

  user = User.create!(result[:attrs])  # database side effect here only
  { success: true, user: user }
end
```

## Pure Method Guidelines

A method is pure when:
1. Same inputs always return same output
2. No mutation of instance variables during computation
3. No I/O (logging, DB, network) inside the calculation

```ruby
# BAD — mutates state during calculation
def calculate_totals
  @subtotal = @items.sum { |i| i[:price] * i[:qty] }
  @tax = @subtotal * 0.08
  @total = @subtotal + @tax
end

# GOOD — returns new values, no mutation
def self.calculate_totals(items, tax_rate: 0.08)
  subtotal = items.sum { |i| i[:price] * i[:qty] }
  tax = subtotal * tax_rate
  { subtotal: subtotal, tax: tax, total: subtotal + tax }
end
```

## Composition Patterns

```ruby
# Method chaining on custom objects — return self or new instance
class Pipeline
  def initialize(steps = [])
    @steps = steps.freeze
  end

  def add(step)
    Pipeline.new(@steps + [step])  # returns new instance, immutable
  end

  def call(input)
    @steps.reduce(input) { |data, step| step.call(data) }
  end
end

# Lambda composition with >>
sanitize  = ->(s) { s.strip.downcase }
validate  = ->(s) { raise "empty" if s.empty?; s }
normalize = sanitize >> validate

# Callable objects (duck-typed lambdas)
class Validator
  def call(value)
    value.is_a?(String) && !value.empty?
  end
end

validators = [Validator.new, ->(v) { v.length < 255 }]
valid = validators.all? { |v| v.call(input) }
```

## Anti-Patterns to Avoid

```ruby
# BAD — accumulator mutation inside each
result = []
items.each { |item| result << transform(item) if item[:active] }
# GOOD
result = items.filter_map { |item| transform(item) if item[:active] }

# BAD — output parameter mutation
def process(items, output)
  items.each { |i| output << i * 2 }
end
# GOOD — return new value
def process(items)
  items.map { |i| i * 2 }
end

# BAD — complex logic inside a class with side effects mixed in
def calculate_and_save
  total = @items.sum(&:price)
  @total = total          # side effect
  DB.save(total)          # side effect
  total
end
# GOOD — separate concerns
total = calculate_total(@items)  # pure
update_total(total)              # side effect isolated

# BAD — bare proc for reusable function
adder = proc { |a, b| a + b }  # loose arity, weird return behavior
# GOOD
adder = ->(a, b) { a + b }
```

## When to Use Classes

OOP is fine for: stateful objects that model real entities (User, Order, Connection), framework integration (ActiveRecord models, controllers), objects that encapsulate a lifecycle.

Use modules with class methods (or plain lambdas/methods) for: pure logic, utilities, transformations, validators.

```ruby
# Module for pure logic — no instances needed
module PriceCalculator
  def self.discount(price, tier)
    rates = { bronze: 0.05, silver: 0.10, gold: 0.20 }.freeze
    price * (1 - rates.fetch(tier, 0))
  end
end

# Class for stateful lifecycle
class ImportJob
  def initialize(source_db, config)
    @source_db = source_db
    @config = config
  end

  def run
    records = fetch_records        # I/O
    processed = process(records)   # pure
    persist(processed)             # I/O
  end

  private

  def process(records)
    records
      .select { |r| valid?(r) }
      .map { |r| transform(r) }
  end
end
```

## Security Notes for Standalone Scripts

- **Never interpolate external input into shell commands** — use `Open3.capture3` with array args, not `system("cmd #{input}")`
- **Never interpolate input into SQL** — use parameterized queries or the driver's escape method
- **ENV for credentials** — never hardcode; raise if missing: `ENV.fetch('DB_PASSWORD')`

```ruby
# BAD — shell injection
system("convert #{filename} output.png")

# GOOD — array form, no shell expansion
require 'open3'
stdout, stderr, status = Open3.capture3('convert', filename, 'output.png')

# BAD — hardcoded credential
client = Mysql2::Client.new(password: 'secret123')

# GOOD — fail loudly if not set
client = Mysql2::Client.new(password: ENV.fetch('MYSQL_PASSWORD'))
```

## Quick Reference: When to Reach for What

| Need | Use |
|------|-----|
| Transform a collection | `map` |
| Filter a collection | `select` / `reject` |
| Transform + filter in one pass | `filter_map` |
| Accumulate to a single value | `reduce` / `inject` |
| Build a hash from a collection | `each_with_object` / `to_h` |
| Group by a property | `group_by` |
| Reusable function | `lambda` / `->` |
| Compose functions | `>>` operator |
| Immutable constant | `.freeze` |
| Immutable value object | `Data.define` (Ruby 3.2+) or frozen `Struct` |
| Pure logic module | `module Foo; def self.method...` |

## When to Load Reference Files

### FP Patterns Deep Dive
**File**: [`references/patterns.md`](references/patterns.md)
**Load when**: Need advanced composition, lazy enumerables, currying, memoization
**Contains**: Lazy evaluation, `Comparable`/`Enumerable` mixin, memoization patterns, full pipeline example

### Security Examples
**File**: [`references/security.md`](references/security.md)
**Load when**: Working with external input, SQL, shell commands, file operations
**Contains**: SQL parameterization, shell safety, input validation, ENV credential management
