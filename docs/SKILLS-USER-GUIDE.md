# Agent Skills User Guide

Complete guide for using Agent Skills with Claude Code for functional programming in JavaScript.

## What Are Agent Skills?

Agent Skills are **organized folders of instructions, scripts, and resources** that Claude can discover and load dynamically. Think of them as specialized expertise modules that enhance Claude's capabilities for specific tasks.

**Key Benefits**:
- **Progressive Disclosure**: Claude loads only what's needed (metadata → SKILL.md → additional files)
- **Context Efficiency**: 80% reduction in repeated content vs. old command system
- **Persistent**: Skills remain available across all Claude Code sessions
- **Discoverable**: Claude automatically finds and uses appropriate skills

## Available Skills

### **`js-fp`** - JavaScript Functional Programming (Foundation)

**When Claude loads this**: Any FP-related request, need for core FP principles, anti-over-engineering guidance.

**What it provides**:
- Anti-over-engineering enforcement (PRIMARY)
- Core FP patterns (purity, composition, DI, immutability)
- Critical anti-patterns (NO pipe/compose/curry utilities)
- Testing essentials
- Performance patterns (evidence-based)

**Example requests**:
```
"Help me write pure functions for data validation"
"How do I avoid over-engineering this feature?"
"Show me FP testing patterns"
```

### **`js-fp-api`** - Node.js/API Development

**When Claude loads this**: Building REST APIs, Node.js backends, need security-first SQL, middleware patterns.

**What it provides**:
- Security-first SQL (parameterized queries, MANDATORY)
- Middleware dependency injection
- Self-contained route pattern (300-500 lines max)
- Pure business logic separation
- CRUD examples with security

**Example requests**:
```
"Create a REST API endpoint for users with security"
"How do I structure my Node.js API with FP principles?"
"Show me secure SQL query patterns"
```

### **`js-fp-vue`** - Vue.js Development

**When Claude loads this**: Building Vue.js components, need composables, wrapper patterns, Vue 3 Composition API.

**What it provides**:
- Pure component with composable pattern
- Wrapper pattern for side effects
- Composable factory pattern (performance)
- Anti-patterns (Pinia/Vuex over-usage, reactive over-engineering)
- State management (composables > stores)

**Example requests**:
```
"Create a Vue component with pure business logic"
"How do I handle external API calls in Vue with FP?"
"Show me composable patterns for state management"
```

### **`js-fp-react`** - React Development

**When Claude loads this**: Building React components, need custom hooks, HOC patterns, React 16.8+ with hooks.

**What it provides**:
- Pure component with custom hook pattern
- HOC for dependency injection
- Compound component pattern
- Appropriate memoization (not obsessive)
- Anti-patterns (premature optimization, context over-usage)

**Example requests**:
```
"Create a React component with custom hooks"
"How do I inject dependencies in React with FP?"
"Show me compound component patterns"
```

### **`js-fp-wordpress`** - WordPress/Bootstrap JavaScript

**When Claude loads this**: Building WordPress plugin/theme JavaScript, need jQuery vs Vanilla JS guidance, integrating with Gravity Forms or ACF.

**What it provides**:
- jQuery vs Vanilla JS decision matrix (context-specific)
- Pure business logic separation in browser JS
- WordPress/GF/ACF jQuery event integration
- AJAX patterns (jQuery and fetch)
- Ecosystem-native patterns (jQuery IS native in WordPress)
- Anti-patterns (mixing approaches, fighting the ecosystem)

**Example requests**:
```
"Should I use jQuery or vanilla JS in WordPress?"
"Create a form handler that integrates with Gravity Forms"
"How do I separate business logic from DOM operations in WordPress JS?"
"Show me AJAX patterns for WordPress with pure functions"
```

### **`php-fp`** - PHP Functional Programming (Foundation)

**When Claude loads this**: PHP development, need for PHP-specific FP patterns, strict types enforcement, native PHP patterns.

**What it provides**:
- PHP-specific FP patterns (different from JavaScript)
- Strict types enforcement (`declare(strict_types=1)`)
- Native PHP patterns (array functions, arrow functions, match expressions)
- Configuration pre-compilation for performance (O(n²) → O(n+m))
- Result type pattern for error handling
- PHPUnit testing patterns

**Example requests**:
```
"Help me write pure PHP functions with strict types"
"How do I optimize PHP code with FP patterns?"
"Show me PHP FP testing with PHPUnit"
"Pre-compile configuration for better performance"
```

### **`php-fp-wordpress`** - WordPress Development

**When Claude loads this**: Building WordPress plugins/themes, need security-first PHP practices, WordPress hooks with FP.

**What it provides**:
- 5 mandatory security practices (capability checks, nonces, sanitization, escaping, prepared SQL)
- Pure business logic + WordPress wrapper pattern (PHP-based)
- Plugin complexity patterns (simple/medium/complex)
- Security-first development with PHP FP principles
- Testing strategy for WordPress with PHPUnit

**Example requests**:
```
"Create a WordPress plugin with PHP FP principles"
"How do I secure my WordPress plugin with pure functions?"
"Show me pure PHP functions with WordPress hooks"
```

## How Skills Work (Progressive Disclosure)

Skills use a **3-level progressive disclosure** system:

### Level 1: Metadata (Always Loaded)

```yaml
---
name: "JavaScript FP - Node.js API"
description: "FP API patterns for Node.js with security-first SQL"
---
```

Claude sees this metadata and decides if the skill is relevant to your request.

### Level 2: SKILL.md (Loaded When Relevant)

The main skill file (~400-600 lines) with:
- Error-preventing essentials
- Critical patterns
- Quick examples
- Anti-patterns
- References to additional content

### Level 3: Additional Files (Loaded When Needed)

- `core-principles.md` - Deep dive into WHY
- `*-patterns.md` - Advanced patterns and strategies
- `examples/` - Complete working code examples
- `tests/` - Comprehensive test suites

**Example flow**:
```
You: "Create a secure API endpoint for users"

Claude:
1. Reads metadata → "js-fp-api" looks relevant
2. Loads SKILL.md → Gets security-first SQL patterns, route structure
3. Creates endpoint using loaded patterns
4. (Optional) Loads security-sql.md if needs deeper security patterns
```

## Using Skills Effectively

### Simple Requests (Level 2 Only)

**Good for**: Straightforward implementations, standard patterns.

```
"Create a CRUD endpoint for products"
→ Claude loads: js-fp-api/SKILL.md (~450 lines)
→ Result: Secure endpoint with proper patterns
```

### Complex Requests (Level 2 + 3)

**Good for**: Architecture decisions, learning, optimization.

```
"Explain FP principles and show me how to architect a complex API"
→ Claude loads: js-fp/SKILL.md + core-principles.md + js-fp-api/SKILL.md
→ Result: Comprehensive understanding with architectural guidance
```

### Learning Mode (All Levels)

**Good for**: Understanding patterns, seeing examples, training.

```
"Show me working examples of pure React components with tests"
→ Claude loads: js-fp-react/SKILL.md + examples/ + tests/
→ Result: Complete working examples with explanations
```

## Best Practices

### ✅ DO

**Be specific about your needs**:
```
Good: "Create a Vue composable for user authentication with FP principles"
Better: "Create a Vue composable that handles user auth, keeping side effects in wrapper"
```

**Ask for explanations when learning**:
```
"Why should I avoid pipe() utilities in JavaScript?"
"Explain the wrapper pattern for Vue components"
```

**Reference skills directly when needed**:
```
"Use js-fp-api patterns to create a secure endpoint"
"Apply js-fp-wordpress security practices"
```

### ❌ DON'T

**Be vague**:
```
Bad: "Help me code"
Good: "Create a React component using custom hooks with FP principles"
```

**Assume Claude knows your context without stating it**:
```
Bad: "Make it secure"
Good: "Add WordPress security practices (nonce, capability check, sanitization)"
```

**Over-specify if you don't need to**:
```
Unnecessary: "Load js-fp core principles, then load js-fp-api patterns, then..."
Better: "Create an API endpoint with FP principles" (Claude handles loading)
```

## Common Workflows

### Building a New Feature

1. **Start with the domain skill**:
   ```
   "Create a [React/Vue/API/WordPress] component for [feature]"
   ```

2. **Claude automatically**:
   - Loads relevant skill
   - Applies FP principles
   - Uses domain-specific patterns
   - Prevents common mistakes

3. **Refine as needed**:
   ```
   "Add comprehensive tests"
   "Optimize performance with evidence"
   "Explain the patterns you used"
   ```

### Learning FP Patterns

1. **Ask for explanations**:
   ```
   "Explain pure functions and show examples"
   ```

2. **Request working examples**:
   ```
   "Show me a complete working example of [pattern]"
   ```

3. **Ask for comparisons**:
   ```
   "Compare OOP vs FP for [scenario]"
   "Show me the wrong way vs the right way"
   ```

### Code Review

1. **Request analysis**:
   ```
   "Review this code for FP principles and security"
   ```

2. **Claude checks against**:
   - Anti-over-engineering filters
   - Security practices
   - FP patterns
   - Domain-specific anti-patterns

3. **Get improvement suggestions**:
   ```
   "How can I improve this to be more functional?"
   ```

## Skill Combinations

Skills work together! Claude automatically combines them when needed.

### FP Core + Domain Skill

```
"Create a React component following FP principles"
→ Loads: js-fp (core) + js-fp-react (domain)
→ Result: Component with pure functions, proper DI, comprehensive tests
```

### Multiple Domain Skills

```
"Create a full-stack feature with Vue frontend and Node.js API"
→ Loads: js-fp + js-fp-vue + js-fp-api
→ Result: Consistent FP patterns across frontend and backend
```

## Troubleshooting

### "Claude isn't using the skills"

**Check**:
- Are you being specific enough? "Create a Vue component" vs "Help me code"
- Is the skill relevant? WordPress patterns won't load for React requests

### "Claude loads too much context"

**Solution**:
- Be more specific: "Quick example" vs "Explain everything"
- Skills are optimized for efficiency - if context is high, the task is genuinely complex

### "I want to see what Claude loaded"

**Use the `--show-skills` flag**:
```
"Create a Vue component --show-skills"
```

**Output includes**:
- 📚 Skills Considered: Which skill metadata was scanned
- 📖 Skills Loaded: Which SKILL.md files were read (with line counts)
- 📑 Additional Context: Any deep-dive files accessed (Level 3)
- 🤖 Agent Delegation: Strategy decisions and agent launches (when agents used)
- 📦 Agent Results: Individual agent outcomes and synthesis (when agents used)
- 💬 Pattern Attribution: Code comments linking patterns to their skill sources
- 📊 Summary: Total context loaded and efficiency metrics vs old command system

**Or use the output style for always-on visibility**:
```
/output-style "Skills & Agents Transparency"
```
This enables transparency for all subsequent requests until you switch back with `/output-style default`

**Or ask manually**:
```
"What skills did you use for this?"
"Show me which patterns you applied"
```

## Skill Updates

Skills are version-controlled and improve over time:

- **Current location**: `~/.claude/skills/`
- **Version control**: Git branch `feature/skills-migration`
- **Updates**: Pull latest from repository

## Comparing to Old Command System

| Aspect | Old Commands | New Skills |
|--------|--------------|------------|
| Discovery | Manual `/fp:*` commands | Automatic discovery |
| Context | Full command loaded | Progressive disclosure |
| Persistence | Per-session | Cross-session |
| Examples | Inline only | Separate example files |
| Learning | Integrated in command | Separate deep-dive files |
| Token efficiency | 80% repeated content | Minimal duplication |

## Quick Reference

### Skill Names

**JavaScript Skills:**
- `js-fp` - JavaScript FP core principles
- `js-fp-api` - Node.js/API
- `js-fp-vue` - Vue.js
- `js-fp-react` - React

**PHP Skills:**
- `php-fp` - PHP FP core principles
- `php-fp-wordpress` - WordPress

### Skill Loading Triggers
- **Automatic**: Claude decides based on your request
- **Explicit**: "Use js-fp-api patterns"
- **Learning**: "Explain [concept] from js-fp core"

### Transparency & Visibility

**Per-Request Visibility** (Flag):
```bash
"Create a component --show-skills"
```
Shows skills + agent tracking for this request only

**Always-On Visibility** (Output Style):
```bash
/output-style "Skills & Agents Transparency"
```
Enables visibility for all requests until you switch back

**Return to Default**:
```bash
/output-style default
```

### Getting Help
- Ask Claude: "What skills are available?"
- Ask Claude: "How do I use [skill-name] skill?"
- Read this guide: `skills/SKILLS-USER-GUIDE.md`

## Skills Visibility with `--show-skills`

### Example Output

**Request**: `"Create a secure API endpoint for users --show-skills"`

**Claude's Response**:

```
📚 Skills Considered (Metadata Scan):
  ✓ js-fp-api - "FP API patterns for Node.js with security-first SQL"
  ✓ js-fp - "JavaScript FP core principles"
  ✗ js-fp-react - Not relevant (backend request)
  ✗ js-fp-vue - Not relevant (backend request)

📖 Skills Loaded (Level 2):
  → js-fp-api/SKILL.md (452 lines)
  → js-fp/SKILL.md (380 lines)

[... implementation with pattern attribution ...]

// Pattern from: js-fp-api/SKILL.md (security-first SQL)
const users = await db.query(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);

// Pattern from: js-fp/SKILL.md (pure validation function)
const validateUser = (data) => {
  // validation logic
};

📊 Skills Summary:
  ✅ Task completed

  Skills Used:
    - js-fp-api: Security patterns, route structure, error handling
    - js-fp: Pure function validation, anti-over-engineering

  Context Efficiency:
    - Loaded: 832 lines across 2 skills
    - Old command system equivalent: ~4,200 lines
    - Token reduction: 80% more efficient
```

**With Agent Delegation**: `"Analyze codebase for security issues --show-skills --delegate"`

```
📚 Skills Considered (Metadata Scan):
  ✓ js-fp - "JavaScript FP core principles"
  ✓ php-fp-wordpress - "WordPress security-first practices"

📖 Skills Loaded (Level 2):
  → js-fp/SKILL.md (380 lines)
  → php-fp-wordpress/SKILL.md (510 lines)

🤖 Agent Delegation Analysis:
  Complexity Score: 0.75
  Parallelizable Operations: 8 files across 3 directories
  Estimated Token Requirement: 18K

  Strategy: parallel_dirs
  Reason: >7 directories with independent security concerns

🚀 Launching Agents:
  Agent 1: security-engineer - Analyze /src security
    Prompt: "Security audit focusing on input validation and SQL injection"
    Tools: Read, Grep, Sequential

  Agent 2: security-engineer - Analyze /api security
    Prompt: "Security audit focusing on authentication and authorization"
    Tools: Read, Grep, Sequential

  Agent 3: security-engineer - Analyze /admin security
    Prompt: "Security audit focusing on capability checks and nonces"
    Tools: Read, Grep, Sequential

[... agents execute in parallel ...]

📦 Agent Results:

  Agent 1 (security-engineer) - /src:
    Status: ✅ Completed
    Key Findings:
      - 3 SQL injection vulnerabilities (missing parameterization)
      - 2 XSS risks (unescaped output)
    Files Affected: 5

  Agent 2 (security-engineer) - /api:
    Status: ✅ Completed
    Key Findings:
      - 1 missing authentication check
      - 2 weak authorization patterns
    Files Affected: 3

  Agent 3 (security-engineer) - /admin:
    Status: ✅ Completed
    Key Findings:
      - 4 missing capability checks
      - 3 missing nonce verifications
    Files Affected: 6

  Synthesis:
    Total: 15 security issues across 14 files
    Priority: 3 critical (SQL injection), 12 high (auth/authz)
    Pattern: Consistent security practice gaps across all modules

  Performance:
    - Total agents: 3
    - Parallel efficiency: 65% time saved vs sequential
    - Token distribution: 6K / 5.8K / 6.2K

📊 Skills Summary:
  ✅ Analysis completed

  Skills Used:
    - js-fp: Security patterns, pure validation
    - php-fp-wordpress: 5 mandatory security practices

  Agent Coordination:
    - Agents launched: 3 security-engineer specialists
    - Files analyzed: 14 total
    - Parallel efficiency: 65% faster than sequential

  Context Efficiency:
    - Loaded: 890 lines across 2 skills
    - Agent coordination: 18K tokens distributed across 3 agents
    - Total efficiency: 70% improvement vs monolithic analysis
```

## Advanced Usage

### Requesting Specific Files

```
"Show me the advanced patterns from js-fp-react"
→ Loads: js-fp-react/hooks-advanced.md
```

### Combining Multiple Skills

```
"Create an API that follows both js-fp-api and js-fp-wordpress security patterns"
→ Loads: Both skills, applies both security approaches
```

### Performance Optimization

```
"Optimize this using js-fp performance patterns"
→ Loads: js-fp/performance-patterns.md
```

## Summary

**Skills = Specialized Expertise Modules**

- **Automatic**: Claude finds and loads relevant skills
- **Efficient**: Progressive disclosure (only loads what's needed)
- **Comprehensive**: Core principles + domain patterns + examples
- **Practical**: Real-world patterns that prevent errors

**Just describe what you want to build, and Claude will use the appropriate skills to help you!**
