---
allowed-tools: [Read, Grep, Glob, Write, Edit, TodoWrite, Task]
description: "Apply functional composition principles to system design with SuperClaude integration"
---

# /fp:design - Functional Programming Guided Design

## Purpose
Apply functional programming composition principles to system design using native language patterns, preventing over-engineering through simplicity constraints and anti-utility creation guidelines.

## Usage
```
/fp:design [domain] [--focus security|performance|api] [--lang javascript|php|python|rust] [--simple]
```

## Arguments
- `domain` - System domain to design (auth, api, ui, data-processing)
- `--focus` - Primary design focus (security, performance, api, ui)
- `--lang` - Target implementation language for FP patterns
- `--simple` - Apply aggressive simplicity constraints
- `--with-sc-[persona]` - Collaborate with specific SuperClaude persona

## ⚠️ CRITICAL: Anti-Utility Design Guidelines

**NEVER DESIGN SYSTEMS THAT REQUIRE FP UTILITIES**:
- ❌ **Systems requiring pipe() utilities** → Design for native function calls
- ❌ **Architectures needing compose() utilities** → Use native composition patterns
- ❌ **Designs dependent on curry() utilities** → Use native closures and function factories
- ❌ **Custom monad-based architectures** → Use native error handling patterns

**SPIRIT-BASED DESIGN PRINCIPLES**:
- ✅ **Native Composition**: Design systems that use language-native function composition
- ✅ **Pure Function Boundaries**: Separate pure logic from side effects using native patterns
- ✅ **Performance-First**: Design for optimal performance using native language features
- ✅ **Language Respect**: Architecture should work WITH the language, not against it

## FP Principle Injection

Before executing, inject these principles into any activated SuperClaude personas:

### Core FP Design Principles
- **Native Composition Over Utilities**: Design for native language composition, NOT pipe/compose utilities
- **Pure Function Boundaries**: Separate pure functions from side effects using native error handling
- **Pre-Compilation Planning**: Plan for expensive operations to be pre-compiled using native closures
- **Testability by Design**: Optimize architecture for comprehensive edge-case testing without utility dependencies

### Decision Framework
1. **Can this system be composed using native language patterns?**
2. **Are we avoiding FP utility creation and respecting language capabilities?**
3. **Where can pure functions be isolated from side effects using native patterns?**  
4. **What expensive operations can be pre-compiled into native closures?**
5. **How can this design optimize for comprehensive testing without utility overhead?**

### Anti-Over-Engineering & Anti-Utility Constraints  
- **NEVER create FP utilities** - use native language composition patterns
- Prefer simple native composition over complex abstractions
- Choose direct function calls over utility-based indirection  
- Optimize for readability, maintainability, and language-native performance
- Test design assumptions with concrete examples that avoid utility dependencies

## Execution Flow

1. **Analyze Requirements**: Apply FP lens to understand composition opportunities
2. **Seed SuperClaude Personas**: Inject FP principles into /sc:design or related personas
3. **Execute Design**: Run design process with FP oversight and constraints
4. **Simplicity Review**: Filter recommendations for over-engineering patterns
5. **Testability Validation**: Ensure design supports comprehensive functional testing
6. **Cross-Language Guidance**: Provide equivalent patterns for target languages

## SuperClaude Integration

**Automatic Delegation**: 
- Routes to `/sc:design` with FP principle injection
- Coordinates with `/sc:architect` for system-level FP patterns
- Integrates with `/sc:security` using FP purity requirements for security boundaries

**Collaboration Patterns**:
```
/fp:design user-auth --focus security
→ Seeds /sc:design + /sc:security with FP principles
→ Design emerges with pure function security boundaries
→ FP review prevents over-engineering
```

## Output Focus

- **Function Composition Architecture**: System built from composable functions
- **Pure Function Boundaries**: Clear separation of pure vs side-effect functions  
- **Pre-Compilation Strategies**: Setup-time optimizations identified
- **Comprehensive Testing Approaches**: Testing strategies for functional architecture
- **Simple, Maintainable Solutions**: Complexity minimized through FP constraints

## Cross-Language Pattern Examples

### JavaScript
```javascript
// Native function composition architecture - NO pipe utility
const createAuthSystem = (config) => ({
    authenticate: async (credentials) => {
        const validationResult = validateCredentials(credentials)
        if (!validationResult.valid) return validationResult
        
        const userResult = await checkUser(validationResult.data)
        if (!userResult.valid) return userResult
        
        return generateToken(userResult.data)
    },
    authorize: async (token) => {
        const extractResult = extractToken(token)
        if (!extractResult.valid) return extractResult
        
        const validationResult = await validateToken(extractResult.data)
        if (!validationResult.valid) return validationResult
        
        return checkPermissions(validationResult.data)
    }
})
```

### Python  
```python
# Native functional composition with Python - NO pipe utility
def create_auth_system(config):
    def authenticate(credentials):
        validation_result = validate_credentials(credentials)
        if not validation_result['valid']:
            return validation_result
            
        user_result = check_user(validation_result['data'])
        if not user_result['valid']:
            return user_result
            
        return generate_token(user_result['data'])
    
    def authorize(token):
        extract_result = extract_token(token)
        if not extract_result['valid']:
            return extract_result
            
        validation_result = validate_token(extract_result['data'])
        if not validation_result['valid']:
            return validation_result
            
        return check_permissions(validation_result['data'])
    
    return {
        'authenticate': authenticate,
        'authorize': authorize
    }
```

### PHP
```php
// Native PHP functional composition - NO pipe utility
function createAuthSystem(array $config): array {
    return [
        'authenticate' => function($credentials) {
            $validationResult = validateCredentials($credentials);
            if (!$validationResult['valid']) return $validationResult;
            
            $userResult = checkUser($validationResult['data']);
            if (!$userResult['valid']) return $userResult;
            
            return generateToken($userResult['data']);
        },
        'authorize' => function($token) {
            $extractResult = extractToken($token);
            if (!$extractResult['valid']) return $extractResult;
            
            $validationResult = validateToken($extractResult['data']);
            if (!$validationResult['valid']) return $validationResult;
            
            return checkPermissions($validationResult['data']);
        }
    ];
}
```

### Rust
```rust
// Native Rust zero-cost functional composition - uses native Result chaining
pub fn create_auth_system(config: Config) -> AuthSystem {
    AuthSystem {
        authenticate: |creds| -> Result<Token, AuthError> {
            let validated = validate_credentials(creds)?;
            let user = check_user(validated)?;
            let token = generate_token(user)?;
            Ok(token)
        },
        authorize: |token| -> Result<Permissions, AuthError> {
            let extracted = extract_token(token)?;
            let validated = validate_token(extracted)?;
            let permissions = check_permissions(validated)?;
            Ok(permissions)
        },
    }
}
```

## Quality Gates

- **Anti-Utility Check**: "Are we avoiding FP utility creation and using native patterns?"
- **Language Respect**: "Does this design work WITH the language's strengths?"
- **Simplicity Check**: "Would a junior developer understand this in 6 months?"
- **Native Testability Check**: "Can this be tested easily with all edge cases without utility dependencies?"
- **Native Purity Check**: "Are side effects minimized and isolated using native error handling?"
- **Native Composition Check**: "Is complex behavior composed from simple functions using language idioms?"