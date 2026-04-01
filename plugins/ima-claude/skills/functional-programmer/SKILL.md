---
name: "functional-programmer"
description: "Functional programming principles and philosophy - pure functions, immutability, composition, side effect isolation, declarative style. Trigger when: discussing FP concepts, transitioning from OOP, explaining why FP matters, architectural mindset shifts. This skill covers principles ONLY - see js-fp, php-fp, etc. for implementation patterns."
---

# Functional Programming: Principles and Philosophy

This skill provides the conceptual foundation for functional programming. It covers the WHY, not the HOW. For language-specific implementation patterns, see:
- **js-fp** - JavaScript FP patterns
- **php-fp** - PHP FP patterns
- **js-fp-react**, **js-fp-vue** - Framework-specific FP patterns

## The Core Insight

Functional programming is not a set of utility functions. It's not `pipe()`, `compose()`, or `curry()`. It's a way of thinking about problems that makes code predictable, testable, and maintainable.

**FP is a mindset, not an API signature.**

## The Seven Pillars

### 1. Pure Functions

**Principle**: A function should return the same output for the same input, every time, with no side effects.

**Why it matters:**
- Predictability: No surprises, no hidden state changes
- Testability: Test any function with any input, no mocking required
- Parallelization: Pure functions can run concurrently without coordination
- Debugging: When something breaks, you know exactly where to look

**The litmus test:** Can you call this function 1000 times with the same arguments and always get the same result without affecting anything else? If yes, it's pure.

### 2. Immutability

**Principle**: Data, once created, never changes. To "modify" data, create new data.

**Why it matters:**
- No aliasing bugs: When two variables point to the same data, neither can corrupt the other
- Time-travel debugging: Every state is preserved, you can inspect any point in time
- Concurrency safety: No locks needed when data can't change
- Predictable state: You always know what data looks like at any point

**The key insight:** Mutation is the source of countless bugs. Race conditions, stale references, unexpected side effects - all stem from shared mutable state. Immutability eliminates these entire categories of bugs.

### 3. Function Composition

**Principle**: Complex behavior emerges from combining simple functions.

**Why it matters:**
- Reusability: Small functions combine in countless ways
- Testability: Test each piece independently, trust the composition
- Readability: The code structure matches the mental model
- Maintainability: Change one piece without affecting others

**The mental model:** Think of functions as LEGO bricks. Each brick is simple and does one thing. Complex structures come from how you connect them, not from making bigger bricks.

### 4. First-Class Functions

**Principle**: Functions are values. Pass them around, return them, store them.

**Why it matters:**
- Abstraction power: Higher-order functions enable powerful patterns
- Flexibility: Behavior becomes data you can manipulate
- DRY: Common patterns extracted into reusable higher-order functions
- Customization: Inject behavior without inheritance hierarchies

**The unlock:** When functions become values, you can write functions that operate on functions. This is where FP's real power emerges - abstracting over behavior, not just data.

### 5. Referential Transparency

**Principle**: An expression can be replaced with its value without changing program behavior.

**Why it matters:**
- Reasoning: You can understand code by substituting values
- Refactoring: Move code freely, confident behavior won't change
- Caching: Memoize any referentially transparent computation
- Optimization: Compilers can reorder and optimize freely

**The test:** If you can replace a function call with its return value everywhere in your code and nothing changes, the function is referentially transparent.

### 6. Side Effect Isolation

**Principle**: Push side effects to the edges of your system. Keep the core pure.

**Why it matters:**
- The bulk of your code becomes testable without mocks
- Side effects are explicit and contained
- Business logic stays decoupled from infrastructure
- Easier to swap implementations (databases, APIs, etc.)

**The architecture:** Your system has an impure shell that handles I/O (databases, APIs, user input, logging) and a pure core that handles all business logic. The shell calls the core, never vice versa.

**The ratio to aim for:** 80% pure core, 20% impure shell. If your ratio is inverted, you're spreading side effects throughout your code.

### 7. Declarative Style

**Principle**: Describe WHAT you want, not HOW to get it.

**Why it matters:**
- Intent clarity: Code expresses business logic, not mechanics
- Less boilerplate: The runtime handles the implementation details
- Optimization freedom: Declarative code can be optimized freely
- Reduced bugs: Fewer moving parts means fewer places for bugs to hide

**The shift:** Imperative code is a sequence of instructions. Declarative code is a description of the desired outcome. The runtime figures out the steps.

## The Journey from OOP

### Why Classical Inheritance Fails

**The fragile base class problem:** Change a base class, break all descendants in unpredictable ways.

**The gorilla-banana problem:** You want a banana, but you get a gorilla holding the banana and the entire jungle. Class hierarchies bring unwanted dependencies.

**The diamond problem:** Multiple inheritance creates ambiguity. Single inheritance creates awkward hierarchies where things don't quite fit.

**Deep hierarchies:** Every level of inheritance is another level of complexity to understand. Five levels deep, and nobody knows what's actually happening.

### Composition Over Inheritance

Instead of "is-a" relationships (inheritance), use "has-a" relationships (composition).

Instead of extending behavior through class hierarchies, compose behavior through functions.

**The key difference:**
- Inheritance: Behavior locked in at definition time, tightly coupled
- Composition: Behavior assembled at runtime, loosely coupled

### What OOP Got Right

Object-oriented programming contributed valuable ideas:
- Encapsulation (hiding implementation details)
- Polymorphism (same interface, different behavior)

FP embraces these - through closures for encapsulation and first-class functions for polymorphism. The mistake was coupling these ideas to class hierarchies and inheritance.

## Anti-Over-Engineering

### Don't Create Custom FP Utilities

The biggest trap for newcomers to FP: building a personal utility library of `pipe()`, `compose()`, `curry()`, and custom monads.

**Why it's harmful:**
- Every team member must learn your utilities
- Debugging through abstraction layers
- Maintenance burden for no business value
- Makes code less portable

**The right approach:** Use established libraries (lodash, Ramda, etc.) when appropriate, or just use the language's native patterns. FP principles work without special utilities.

### The Abstraction Cost

Every abstraction has a cost:
- Learning curve for new team members
- Debugging complexity
- Maintenance burden
- Mental overhead when reading code

**The question to ask:** Does this abstraction pay for itself? Will I use it enough to justify the cost? Would a junior developer understand it?

### File Size as a Smell

Keep files under 500 lines. This isn't an arbitrary limit — it's a smell detector. A file approaching 500 lines almost certainly has multiple responsibilities that should be separated.

**When a file grows too large:**
- Split by responsibility, not by arbitrary line count
- A 300-line file with two unrelated concerns is worse than a 480-line file with one
- The goal is cohesion: each file should have a single, clear reason to exist

**Why this matters:**
- Readability: Developers can hold one file's purpose in their head
- Testability: Smaller, focused files are easier to test in isolation
- Navigation: Finding what you need is faster in a well-structured codebase
- Review: Code review quality drops sharply beyond 500 lines

### Context-Appropriate Complexity

A CLI script has different needs than a production API.

A weekend project has different needs than enterprise software.

**Match complexity to context:**
- Simple problem? Simple solution.
- Complex problem? Complex solution.
- Simple problem + complex solution = over-engineering.

## The Practical Application

### Pure Core, Impure Shell

Structure your code in two layers:

**The Pure Core (business logic):**
- All calculations
- All transformations
- All validations
- All business rules

**The Impure Shell (I/O):**
- Database operations
- API calls
- User input/output
- Logging
- File system access

The shell calls the core, passes data in, gets results out. The core never reaches out to the shell.

### Explicit Dependencies

Functions should receive everything they need as parameters.

No reaching into global state. No hidden dependencies. Everything visible in the function signature.

**Why this matters:** You can understand what a function does by reading its signature. You can test it by passing in test data. You can reuse it in any context.

### Result Types Over Exceptions

Return structured results instead of throwing exceptions.

**Why this is better:**
- Error handling is explicit in the type system
- No hidden control flow
- Caller must acknowledge potential failure
- Easier to test error paths

## The Mindset Shift

### Think in Transformations

Stop thinking: "How do I modify this data?"
Start thinking: "What new data do I create from this data?"

### Think in Pipelines

Stop thinking: "How do I imperatively process this step by step?"
Start thinking: "What transformations does this data flow through?"

### Think in Declarations

Stop thinking: "What steps do I need to perform?"
Start thinking: "What is the relationship between input and output?"

### Think in Boundaries

Stop thinking: "How do I make this class do everything?"
Start thinking: "Where does pure logic end and side effects begin?"

## Integration with Tech-Specific Skills

This skill provides the conceptual foundation. For implementation:

| Principle | Implementation Skill |
|-----------|---------------------|
| Pure functions in JavaScript | js-fp |
| Immutability in React | js-fp-react |
| Composition in Vue | js-fp-vue |
| Side effect isolation in Node | js-fp-api |
| FP patterns in PHP | php-fp |
| FP in WordPress | php-fp-wordpress |

## Summary: The FP Mindset

1. **Functions are the unit of abstraction** - Not classes, not modules, functions
2. **Data flows, it doesn't change** - Transform, don't mutate
3. **Side effects are dangerous** - Isolate and control them
4. **Composition beats inheritance** - Small pieces combined > large hierarchies
5. **Explicit beats implicit** - Dependencies, data flow, error handling
6. **Simple beats clever** - Boring, readable code wins
7. **Evidence beats assumptions** - Add complexity only when needed

## The Final Word

*"Functional programming is not about using fancy utilities or writing point-free code. It's about writing code that's honest about what it does, predictable in its behavior, and simple in its structure. The functions are pure, the data is immutable, the dependencies are explicit, and the side effects are contained. Everything else is just syntax."*
