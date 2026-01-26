# ⚠️ Functional Programming Commands (DEPRECATED - Migrating to Agent Skills)

**Status**: These commands are being phased out in favor of Agent Skills.

**Migration Path**: See `~/.claude/skills/SKILLS-USER-GUIDE.md`

**Timeline**:
- ✅ **Now**: Skills available, commands streamlined with deprecation notices
- ⏳ **Week 2**: Commands archived to `commands/fp-legacy/`
- ⏳ **Month 1**: Full migration complete

**Why Agent Skills?**
- ✅ **Auto-discovery**: No manual `/fp:*` commands needed
- ✅ **Progressive disclosure**: Only loads what's needed (400-600 lines vs 1200+)
- ✅ **80% less duplication**: Shared cores, domain-specific patterns
- ✅ **Always available**: Persistent across all sessions
- ✅ **Language-specific**: `js-fp` for JavaScript, `php-fp` for PHP (WordPress!)

**Available Skills**:
- `js-fp` - JavaScript FP core
- `js-fp-api` - Node.js/API
- `js-fp-react` - React
- `js-fp-vue` - Vue.js
- `php-fp` - PHP FP core
- `php-fp-wordpress` - WordPress

---

# Functional Programming Command System (Legacy - Lazy-Load Architecture)

A context-efficient functional programming command system using **lazy-load architecture** to provide complete FP guidance without overwhelming the context window. Features shared core principles, lean domain-specific commands, and de-prioritized performance obsession.

## Overview (Streamlined)

The `/fp:` command system provides **domain-specific FP orchestration** and **cross-cutting patterns**:

- **`/fp:core`**: Universal FP principles (referenced by other commands)
- **Domain Commands**: `api`, `react`, `vue`, `wordpress` - with deprecation notices pointing to Skills
- **Orchestration**: `implement`, `workflow`, `design`, `cleanup` - cross-cutting patterns
- **Utilities**: `document`, `explain`, `troubleshoot` - specialized assistance
- **Anti-Over-Engineering**: Simplicity-first approach (PRIMARY FOCUS)
- **Evidence-Based**: Only add complexity when measured and justified

**Note**: Router system (lean/think variants) removed - obsoleted by Skills + Sonnet 4.5.

## Available Commands (14 streamlined)

### Core & Foundation
- **`/fp:core`** - Universal FP principles and patterns

### Domain-Specific (with Skills migration)
- **`/fp:api`** - Node.js/API patterns → migrating to `js-fp-api` skill
- **`/fp:react`** - React patterns → migrating to `js-fp-react` skill
- **`/fp:vue`** - Vue.js patterns → migrating to `js-fp-vue` skill
- **`/fp:wordpress`** - WordPress patterns → migrating to `php-fp-wordpress` skill

### Orchestration & Cross-Cutting
- **`/fp:implement`** - Feature implementation orchestration
- **`/fp:workflow`** - PRD to implementation workflows
- **`/fp:design`** - Architecture and API design
- **`/fp:cleanup`** - Code cleanup and technical debt reduction

### Utilities & Assistance
- **`/fp:document`** - Documentation generation
- **`/fp:explain`** - Educational explanations
- **`/fp:troubleshoot`** - Problem diagnosis and fixing

### Integration
- **`/fp:sc-coordination`** - SuperClaude persona coordination patterns

## Command Structure

### Lazy-Load Architecture

```
/fp:core                 # Universal FP principles (standalone or referenced)
├── Anti-Over-Engineering (PRIMARY)
├── Purity & Side Effects
├── Composition Patterns  
├── Dependency Injection
├── Native Language Patterns
├── Evidence-Based Optimization
└── Comprehensive Testing

/fp:[domain]             # Intelligent wrappers - smart routing (NEW)
├── /fp:api             # Routes api-lean ↔ api-think based on complexity
├── /fp:react           # Routes react-lean ↔ react-think based on complexity
├── /fp:vue             # Routes vue-lean ↔ vue-think based on complexity
├── /fp:analyze         # Routes analyze-lean ↔ analyze-think based on complexity
├── /fp:optimize        # Routes optimize-lean ↔ optimize-think based on complexity
├── /fp:improve         # Routes improve-lean ↔ improve-think based on complexity
├── /fp:test            # Routes test-lean ↔ test-think based on complexity
└── /fp:purify          # Routes purify-lean ↔ purify-think based on complexity

/fp:[domain]-lean        # Lean, domain-specific commands  
├── /fp:api-lean        # API patterns + core reference
├── /fp:react-lean      # React patterns + core reference (optimized)
├── /fp:vue-lean        # Vue.js patterns + core reference
├── /fp:test-lean       # FP testing patterns + core reference
├── /fp:purify-lean     # Code purification + core reference
├── /fp:improve-lean    # Code improvement + core reference
├── /fp:analyze-lean    # Analysis patterns + core reference
└── /fp:optimize-lean   # Evidence-based optimization + core reference

/fp:[domain]-think       # Comprehensive analysis with automatic --think mode
├── /fp:analyze-think   # Deep FP analysis with reasoning
├── /fp:optimize-think  # Performance optimization with detailed analysis  
├── /fp:improve-think   # Code improvement with comprehensive reasoning
├── /fp:test-think      # Test generation with deep coverage analysis
├── /fp:purify-think    # Code purification with transformation reasoning
├── /fp:api-think       # API generation with architectural analysis
├── /fp:vue-think       # Vue.js components with composition strategy analysis
└── /fp:react-think     # React components with hook strategy analysis
```

### Core Command (Universal)

| Command | Purpose | Usage |
|---------|---------|-------|
| `/fp:core` | Complete FP principles foundation | Standalone or referenced by personas |

### Intelligent Wrappers (Smart Routing) ⭐

**Recommended**: Use these familiar commands for automatic routing to the optimal approach.

| Wrapper Command | Auto-Routes Between | Benefits |
|----------------|-------------------|----------|
| `/fp:api` | `api-lean` ↔ `api-think` | Smart complexity detection, familiar interface |
| `/fp:react` | `react-lean` ↔ `react-think` | Automatic React pattern selection, user-friendly |
| `/fp:vue` | `vue-lean` ↔ `vue-think` | Intelligent Vue.js approach, transparent routing |
| `/fp:analyze` | `analyze-lean` ↔ `analyze-think` | Context-aware analysis depth, optimal results |
| `/fp:optimize` | `optimize-lean` ↔ `optimize-think` | Smart performance analysis, reliability bias |
| `/fp:improve` | `improve-lean` ↔ `improve-think` | Intelligent refactoring depth, comprehensive default |
| `/fp:test` | `test-lean` ↔ `test-think` | Context-aware testing strategy, thorough coverage |
| `/fp:purify` | `purify-lean` ↔ `purify-think` | Adaptive purification analysis, transformation clarity |

**Key Benefits**: Transparent routing decisions, override controls, reliability bias toward comprehensive analysis, continuous improvement through user feedback.

### Lean Commands (Domain-Specific)

| Command | Purpose | Core Reference |
|---------|---------|----------------|
| `/fp:api-lean` | Reference-quality APIs with FP | `/fp:core --focus patterns` |
| `/fp:react-lean` | Pure React components with hooks (optimized) | `/fp:core --focus composition` |
| `/fp:vue-lean` | Pure Vue.js components with composables (NEW) | `/fp:core --focus composition` |
| `/fp:test-lean` | Comprehensive FP testing patterns (NEW) | `/fp:core --focus testing` |
| `/fp:purify-lean` | Code purification and conversion (NEW) | `/fp:core --focus purity` |
| `/fp:improve-lean` | Systematic code improvement (NEW) | `/fp:core --focus improvement` |
| `/fp:analyze-lean` | FP-focused code analysis | `/fp:core --focus principles` |
| `/fp:optimize-lean` | Evidence-based optimization | `/fp:core --focus evidence-based` |

### Think Commands (Comprehensive Analysis)

**Purpose**: Detailed analysis and generation with automatic `--think` mode reasoning by default.

| Think Command | Purpose | Key Features |
|--------------|---------|--------------|
| `/fp:analyze-think` | Comprehensive FP code analysis | Deep reasoning, pattern recognition, cross-pattern comparisons |
| `/fp:optimize-think` | Performance optimization with analysis | Detailed performance impact analysis, benchmarking |
| `/fp:improve-think` | Code improvement with reasoning | Comprehensive architectural assessment, quality analysis |
| `/fp:test-think` | Test generation with deep analysis | Coverage reasoning, edge case analysis, testing strategy |
| `/fp:purify-think` | Code purification with reasoning | Detailed purity analysis, transformation explanations |
| `/fp:api-think` | API generation with architecture analysis | Security assessment, performance analysis, error handling strategy |
| `/fp:vue-think` | Vue.js components with reasoning | Architectural assessment, composition strategy analysis |
| `/fp:react-think` | React components with reasoning | Hook strategy analysis, state management evaluation |

**Usage Strategy**:
- Use think commands when you need comprehensive analysis and detailed explanations
- Automatically includes `--think` level reasoning without manual flag
- Provides architectural assessment and cross-pattern comparisons
- Ideal for learning, complex projects, and detailed understanding

## Quick Start

### ⚡ Intelligent Wrapper Usage (Recommended)

**Smart routing to the right approach** - just use familiar commands:

```bash
# 🧠 Smart API generation - auto-routes to optimal approach
/fp:api user-authentication     # → Likely routes to api-think (complex)
/fp:api basic-crud             # → Likely routes to api-lean (simple)

# 🎯 Smart React components - context-aware routing  
/fp:react UserDashboard        # → Likely routes to react-think (complex)
/fp:react Button --quick       # → Routes to react-lean (efficiency keyword)

# 🔍 Smart code analysis - intelligent depth selection
/fp:analyze legacy-system      # → Routes to analyze-think (complexity)
/fp:analyze simple function    # → Routes to analyze-lean (clear scope)

# ⚡ Smart optimization - automatic complexity detection
/fp:optimize performance-bottleneck  # → Routes to optimize-think (complexity)

# 🛡️ Force specific approach when needed
/fp:api user-service --force-think   # → Forces comprehensive analysis
/fp:react Button --force-lean        # → Forces efficient approach

# 📚 Get complete FP foundation anytime
/fp:core --focus principles --examples
```

### 🎛️ Direct Command Usage (Advanced)

For explicit control when you know exactly what you want:

```bash
# Lean commands - efficient, focused with core references
/fp:api-lean user-endpoints --with-core
/fp:react-lean UserCard --type component --with-core
/fp:analyze-lean service-layer.js --focus simple --with-core

# Think commands - comprehensive analysis with detailed reasoning
/fp:api-think complex-auth --architectural-analysis
/fp:react-think Dashboard --performance-analysis
/fp:analyze-think system-architecture --deep-reasoning
```

### Legacy Usage (Still Works)

```bash
# Original commands maintain backward compatibility
/fp:api user-addresses --method POST --pattern crud
/fp:react UserCard --type component --pattern pure
/fp:analyze database-layer.js --focus patterns

# But lean commands are preferred for context efficiency
/fp:api-lean user-addresses --method POST
/fp:react-lean UserCard --type component
/fp:analyze-lean database-layer.js --focus simple --with-core
```

## Core FP Principles

**Complete Foundation**: See `/fp:core` for comprehensive FP principles including:

### ⚠️ PRIMARY FOCUS: Anti-Over-Engineering and Simplicity

**"Simple solutions > Complex abstractions | Evidence > assumptions | MVP > Enterprise patterns"**

- **Anti-Utility Creation**: No pipe/compose/curry utilities - use native patterns
- **Context-Appropriate Complexity**: CLI script ≠ production service ≠ big data
- **Evidence-Based Optimization**: Measure first, optimize only when needed
- **Simplicity-First**: Choose simple solution over complex abstraction

### Universal FP Patterns (Brief Overview)

**Complete guidance available in `/fp:core`**:
- **Purity**: Functions without side effects, 100% testable
- **Composition**: Native function calls over inheritance  
- **Dependency Injection**: Explicit parameters over global state
- **Native Patterns**: Language idioms over FP utilities

### 1. Performance Through Purity (Native JavaScript Patterns)

```javascript
// Pure functions enable aggressive optimization - NO pipe() utility needed
const createOptimizedProcessor = (config) => {
    // Pre-compile expensive operations (Configuration Pre-Compilation pattern)
    const processors = config.fields.map(compileFieldProcessor)
    
    // Return optimized function - use native function calls
    return (record) => processors.map(p => p(record))
}
```

### 2. Composition Over Inheritance (Native Language Style)

```javascript
// Build complex behavior from simple functions - NO pipe() utility
const validateUser = (userData) => {
    const requiredCheck = validateRequired(['email', 'name'])(userData)
    if (!requiredCheck.valid) return requiredCheck
    
    const emailCheck = validateEmail(userData)
    if (!emailCheck.valid) return emailCheck
    
    return validateNameLength(userData)
}

// Alternative: Use JavaScript-native chaining where appropriate
const validateUserFunctional = (userData) => 
    validateRequired(['email', 'name'])(userData) &&
    validateEmail(userData) &&
    validateNameLength(userData)
```

### 3. Configuration Pre-Compilation (Hot Path Optimization)

```javascript
// Extract expensive setup from hot paths
// Before: O(records × fields) - slow
records.map(record => 
    schema.fields.map(field => transform(record, field)) // ← repeated config access
)

// After: O(records + fields) - fast  
const processor = createProcessor(schema) // ← setup once
records.map(processor) // ← linear execution
```

### 4. React-Specific FP Patterns

```javascript
// Pure component with custom hook pattern
const useUserLogic = (userData, config) => {
  const displayData = useMemo(() => ({
    ...userData,
    displayName: userData.name.trim()
  }), [userData, config])
  
  const handleAction = useCallback((action) => ({
    type: 'USER_ACTION', 
    payload: { userId: userData.id, action }
  }), [userData.id])
  
  return { displayData, handleAction }
}

const UserCard = memo(({ userData, config, onAction }) => {
  const { displayData, handleAction } = useUserLogic(userData, config)
  
  const handleClick = useCallback(() => {
    const action = handleAction('view')
    onAction?.(action)
  }, [handleAction, onAction])
  
  return (
    <div onClick={handleClick}>
      <h3>{displayData.displayName}</h3>
      {config.showEmail && <p>{displayData.email}</p>}
    </div>
  )
})
```

### 5. Comprehensive Edge-Case Testing

```javascript
// Pure functions enable systematic testing
describe('validateEmail', () => {
    // Test all JavaScript data types - only practical with pure functions
    [null, undefined, true, [], {}, 123, 'invalid'].forEach(input => {
        it(`handles ${typeof input} gracefully`, () => {
            expect(() => validateEmail(input)).not.toThrow()
        })
    })
})
```

## JavaScript-Focused Language Support

### Modern JavaScript Features
- ES2024+ syntax and features
- Closures for Hot Path Optimization patterns
- Arrow functions and async/await
- WeakMap caching optimization
- Array methods and native iteration

### React Integration
- Pure functional components with hooks
- HOC patterns for dependency injection
- Performance optimization with memoization
- Compound component architectures
- Context-based state management

### Node.js Backend Patterns
- Pure business logic functions
- Configuration pre-compilation for APIs
- Functional error handling patterns
- Stream processing with functional composition

## Performance Benchmarks

### Expected Hot Path Optimization Improvements

| Dataset | Traditional | FP Optimized | Improvement |
|---------|-------------|--------------|-------------|
| 1K records, 12 fields | 45ms | 8ms | 5.6x |
| 10K records, 24 fields | 890ms | 65ms | 13.7x |
| 100K records, 24 fields | 8.2s | 320ms | 25.6x |

### Key Optimization Patterns

1. **Pre-Compilation**: Move configuration costs to setup time
2. **Closure Caching**: Use function scope for expensive lookups
3. **Function Factories**: Generate optimized functions at initialization
4. **Linear Scaling**: Transform O(n²) algorithms to O(n+m)

## Integration with SuperClaude

### Automatic FP Seeding

When FP commands delegate to SuperClaude personas, they automatically inject:

```yaml
fp_principles:
  decision_framework:
    - "Can this be pure?"
    - "Can this be pre-compiled?"
    - "Can this be composed?"
    - "Can this be simplified?"
    
  constraints:
    - "Prefer composition over inheritance"
    - "Extract configuration from hot paths" 
    - "Choose simple solutions over clever ones"
    - "Test comprehensively with edge cases"
```

### Anti-Over-Engineering & Anti-Utility Creation

FP commands apply STRICT simplicity filters to prevent utility anti-patterns:

**PROHIBITED PATTERNS**:
- ❌ **Creating pipe() utilities** → Use native function calls and early returns
- ❌ **Creating compose() utilities** → Use native function composition or direct calls  
- ❌ **Creating curry() utilities** → Use native closures and function factories
- ❌ **Creating custom monads** → Use native error handling and conditionals
- ❌ **FP utility libraries** → Use native language patterns

**PREFERRED APPROACHES**:
- ✅ **Native Function Calls** → Direct function invocation with proper error handling
- ✅ **JavaScript Idioms** → Array methods, conditional operators, native async patterns
- ✅ **Simple Composition** → Function factories and closure patterns without utilities
- ✅ **Performance First** → Choose patterns that work WITH JavaScript, not against it

**SuperClaude Integration Filters**:
- **Complex Abstractions** → Suggest direct function approach
- **Utility Creation** → Block FP utility generation, suggest native patterns
- **Deep Hierarchies** → Recommend simple function composition  
- **Clever Solutions** → Prioritize readable, performant alternatives
- **Framework Creation** → Use simple implementation first

## Enhanced Command System

### React Component Generation

```bash
# Generate pure component with custom hook
/fp:react UserProfile --type component --pattern pure --test comprehensive

# Generate HOC for service injection
/fp:react withAuthService --type hoc --di explicit

# Generate compound component
/fp:react Modal --pattern compound --perf optimize
```

### Performance Optimization Workflows

```bash
# Generate step-by-step performance optimization
/fp:workflow data-processing --focus performance --strategy performance-first

# Benchmark existing vs FP patterns
/fp:benchmark current-implementation.js --compare-with-fp --scale 10000
```

### Documentation and Testing

```bash
# Generate FP-focused documentation
/fp:document validation-service.js --type api --performance --edge-cases

# Generate comprehensive pure function tests
/fp:test user-validation.js --edge-cases --performance
```

## File Organization (New Lazy-Load Architecture)

```
~/.claude/commands/fp/
├── README.md              # This file (updated for lazy-load)
├── lazy-load-index.md     # Guide to new architecture
├── core.md                # /fp:core - Universal FP principles
├── api-lean.md            # /fp:api-lean - API patterns + core reference
├── react-lean.md          # /fp:react-lean - React patterns + core reference
├── analyze-lean.md        # /fp:analyze-lean - Analysis + core reference
├── optimize-lean.md       # /fp:optimize-lean - Evidence-based optimization
├── sc-coordination.md     # SuperClaude integration
└── [legacy commands]      # Original commands (backward compatibility)
    ├── analyze.md         # Legacy /fp:analyze
    ├── api.md             # Legacy /fp:api
    ├── react.md           # Legacy /fp:react
    └── [other legacy files]
```

## Key Benefits

### Context Efficiency
- **80% reduction** in repeated FP principles across commands
- **Lazy loading** - reference complete context only when needed
- **Shared foundation** - single source of truth for core principles
- **Domain focus** - lean commands concentrate on specific patterns

### De-Prioritized Performance Obsession  
- **Simplicity-first** approach prevents over-engineering
- **Evidence-based optimization** only when measured performance problems
- **MVP principles** prioritized over premature optimization
- **Context-appropriate** complexity matching actual needs

### Standalone Utility
- **`/fp:core`** works independently for specific FP guidance
- **Individual concepts** can be referenced without full system
- **Cross-language examples** for consistent FP patterns
- **Educational resource** for learning FP principles

## Migration Guide

- **New commands preferred** - use lean commands for better context efficiency  
- **Legacy compatibility** - original commands still work
- **Gradual adoption** - mix old and new commands as needed
- **Reference core** - use `/fp:core` when you need complete FP foundation

## Quality Gates

Every FP command applies these validation checks:

- **Anti-Utility**: "Are we avoiding FP utility creation and using native JavaScript patterns?"
- **Simplicity**: "Is this the simplest approach that meets requirements?"
- **Language Respect**: "Are we working WITH JavaScript's strengths, not against them?"
- **Purity**: "Are side effects minimized and isolated using native patterns?"  
- **Composition**: "Can this be built from simple, composable functions without utilities?"
- **Testability**: "Can this be tested easily with all edge cases?"
- **Performance**: "Are expensive operations pre-compiled where beneficial WITHOUT utility overhead?"

## Reference Examples

### Configuration Pre-Compilation Example

```javascript
// Before: O(n²) complexity with repeated config access
const processItems = (items, config) => {
  return items.map(item => {
    return config.transforms.reduce((result, transform) => {
      return applyTransform(result, transform.type, transform.options)
    }, item)
  })
}

// After: O(n+m) with pre-compiled transforms
const createProcessor = (config) => {
  const compiledTransforms = config.transforms.map(t => 
    createCompiledTransform(t.type, t.options)
  )
  
  return (items) => items.map(item =>
    compiledTransforms.reduce((result, transform) => 
      transform(result), item
    )
  )
}

// Usage: 5-15x performance improvement
const processor = createProcessor(config) // Setup once
const result = processor(items) // Fast execution
```

### React FP Pattern Example

```javascript
// Reference-quality React component following FP principles
import { memo, useCallback, useMemo } from 'react'
import { createClassMap } from './fp-react-utils'

// Pre-compiled class map for performance
const cardClasses = createClassMap('card', {
  default: 'bg-white border border-gray-200',
  elevated: 'bg-white shadow-lg border-0',
  outlined: 'bg-transparent border-2 border-gray-300'
})

// Pure custom hook containing all business logic
const useCardLogic = (data, config) => {
  const displayData = useMemo(() => ({
    ...data,
    formattedDate: formatDate(data.createdAt),
    truncatedContent: truncate(data.content, config.maxLength)
  }), [data, config.maxLength])
  
  const handleAction = useCallback((actionType) => ({
    type: 'CARD_ACTION',
    payload: { id: data.id, action: actionType }
  }), [data.id])
  
  return { displayData, handleAction }
}

// Pure presentational component
const Card = memo(({ data, config, onAction }) => {
  const { displayData, handleAction } = useCardLogic(data, config)
  
  const handleClick = useCallback(() => {
    const action = handleAction('view')
    onAction?.(action)
  }, [handleAction, onAction])
  
  return (
    <div 
      className={cardClasses(config.variant)}
      onClick={handleClick}
    >
      <h3>{displayData.title}</h3>
      <p>{displayData.truncatedContent}</p>
      <time>{displayData.formattedDate}</time>
    </div>
  )
})

Card.displayName = 'Card'
export { Card }
```

## Success Metrics

### Performance Targets
- **Bundle Size**: <5KB per component (gzipped)
- **Execution Time**: 5-25x improvement for hot path optimizations
- **Memory Usage**: Efficient closure and WeakMap utilization
- **Re-render**: Minimal through proper memoization

### Code Quality
- **Test Coverage**: 100% line coverage for pure functions
- **Type Safety**: Full TypeScript integration
- **Maintainability**: Simple, readable code over clever abstractions
- **Performance**: Measurable improvements with benchmarks

### Developer Experience
- **Predictable Patterns**: Consistent FP approaches
- **Easy Testing**: 100% mockable through dependency injection
- **Clear Documentation**: Comprehensive examples and usage guides
- **Simple Maintenance**: Easy to understand and modify

## Contributing and Extension

### Adding New FP Commands

1. Create command file in fp/ directory
2. Follow the YAML frontmatter format with `allowed-tools` and `description`
3. Include comprehensive JavaScript examples
4. Add SuperClaude integration patterns if applicable
5. Include quality gates and anti-over-engineering checks

### Command File Template

```markdown
---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, TodoWrite]
description: "Brief description of command purpose"
---

# /fp:command-name - Command Title

## Purpose
Clear statement of what this command accomplishes

## Usage
```
/fp:command-name [args] [--flags]
```

## FP Principles Applied
- Specific FP patterns this command implements

## JavaScript Examples
- Comprehensive implementation examples

## Quality Gates
- Validation checks applied
```

## Resources

The FP command system transforms JavaScript development by making functional programming accessible, preventing over-engineering, and delivering measurable performance improvements through proven patterns.

**Philosophy**: *"Pure functions, native JavaScript patterns, performance consciousness, and anti-over-engineering for reference-quality code."*