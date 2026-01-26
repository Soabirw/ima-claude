---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Grep, TodoWrite, Task]
description: "FP patterns for React with hooks and HOCs (DEPRECATED - see Agent Skills)"
---

# ⚠️ DEPRECATED: This command has been replaced by Agent Skills

**Old**: `/fp:react`, `/fp:react-lean`, `/fp:react-think`
**New**: Skills automatically loaded - just describe what you need!

**Migration**: See `~/.claude/skills/SKILLS-USER-GUIDE.md`

**Why Skills are better:**
- ✅ **Auto-discovery**: No manual commands needed
- ✅ **Progressive disclosure**: Loads 460 lines vs 1200+ for think variant
- ✅ **80% less duplication**: Shared FP core, React-specific patterns
- ✅ **Always available**: Persistent across all sessions

**Example Migration:**
```
Before: /fp:react-lean UserCard --hooks --memo
After:  "Create a React component with custom hooks and appropriate memoization"
```

**New Skill Location**: `~/.claude/skills/js-fp-react/SKILL.md`

---

# /fp:react - Functional Programming React Patterns

**Note**: This command remains available during transition. New projects should use Agent Skills.

## Purpose

React 16.8+ component development using functional programming principles with custom hooks, HOCs for dependency injection, and appropriate memoization.

## Usage

```
/fp:react [component-name] [--hooks] [--hoc] [--compound] [--memo]
```

## Arguments

- `component-name` - React component to generate
- `--hooks` - Generate with custom hooks pattern (default)
- `--hoc` - Include HOC for dependency injection
- `--compound` - Use compound component pattern
- `--memo` - Add memoization (when appropriate)

## Core Philosophy

**Foundation**: Builds on `/fp:core` principles for purity, composition, and testing.

**Pure components** with **business logic in custom hooks**, **HOCs for dependency injection**, and **appropriate memoization** (not obsessive).

## Pure Component with Custom Hook Pattern

**Rule**: Separate business logic (custom hooks) from presentation (components).

```typescript
import { memo, useMemo, useCallback } from 'react'

interface UserData {
  id: string
  name: string
  email: string
}

interface UserConfig {
  showEmail: boolean
  variant: 'compact' | 'detailed'
}

// ───── Custom hook with pure business logic ─────
const useUserLogic = (userData: UserData, config: UserConfig) => {
  // Pure computation - no side effects
  const displayData = useMemo(() => ({
    ...userData,
    displayName: userData.name.trim(),
    shouldShowEmail: config.showEmail && userData.email
  }), [userData, config])

  // Pre-compiled handlers
  const handleAction = useCallback((action: string) => ({
    type: 'USER_ACTION',
    payload: { userId: userData.id, action }
  }), [userData.id])

  return { displayData, handleAction }
}

// ───── Pure component with memo ─────
const UserCard = memo<UserCardProps>(({ userData, config, onAction }) => {
  const { displayData, handleAction } = useUserLogic(userData, config)

  const handleClick = useCallback(() => {
    const action = handleAction('view')
    onAction?.(action)
  }, [handleAction, onAction])

  return (
    <div className={`user-card user-card--${config.variant}`}>
      <h3>{displayData.displayName}</h3>
      {displayData.shouldShowEmail && <p>{displayData.email}</p>}
      <button onClick={handleClick}>View</button>
    </div>
  )
})

UserCard.displayName = 'UserCard'
```

## HOC for Dependency Injection Pattern

**Rule**: Inject dependencies via HOCs for testability.

```typescript
// ───── Service interfaces ─────
interface ServiceDependencies {
  userService: {
    getUser: (id: string) => Promise<UserData>
    updateUser: (id: string, data: Partial<UserData>) => Promise<UserData>
  }
  logger: {
    info: (message: string, meta?: any) => void
    error: (message: string, meta?: any) => void
  }
}

// ───── HOC factory ─────
export const withUserService = <P extends object>(
  WrappedComponent: React.ComponentType<P & ServiceDependencies>
) => {
  const WithUserServiceComponent = (props: P) => {
    // Service injection - can be mocked for testing
    const services: ServiceDependencies = {
      userService: useUserService(),
      logger: useLogger()
    }

    return <WrappedComponent {...props} {...services} />
  }

  WithUserServiceComponent.displayName =
    `withUserService(${WrappedComponent.displayName || WrappedComponent.name})`

  return WithUserServiceComponent
}

// ───── Pure component with injected dependencies ─────
const UserProfile = ({
  userId,
  userService,
  logger
}: { userId: string } & ServiceDependencies) => {
  const [user, setUser] = useState<UserData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadUser = async () => {
      try {
        const userData = await userService.getUser(userId)
        setUser(userData)
        logger.info('User loaded', { userId })
      } catch (error) {
        logger.error('Failed to load user', { userId, error })
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [userId, userService, logger])

  if (loading) return <div>Loading...</div>
  if (!user) return <div>User not found</div>

  return <UserCard userData={user} config={{ showEmail: true, variant: 'detailed' }} />
}

// ───── Enhanced component with service injection ─────
export const UserProfileWithServices = withUserService(UserProfile)
```

## Compound Component Pattern

**Rule**: Use composition for flexible, reusable component APIs.

```typescript
import { createContext, useContext, useState, useEffect } from 'react'

// ───── Context for compound component ─────
interface ModalContextValue {
  isOpen: boolean
  onClose: () => void
}

const ModalContext = createContext<ModalContextValue | null>(null)

const useModalContext = () => {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error('Modal components must be used within Modal')
  }
  return context
}

// ───── Main compound component ─────
const Modal = ({ isOpen, onClose, children }: {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}) => {
  // Keyboard handling (side effect isolated)
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      return () => document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <ModalContext.Provider value={{ isOpen, onClose }}>
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          {children}
        </div>
      </div>
    </ModalContext.Provider>
  )
}

// ───── Compound component parts ─────
Modal.Header = ({ children }: { children: React.ReactNode }) => {
  const { onClose } = useModalContext()

  return (
    <div className="modal-header">
      {children}
      <button onClick={onClose} aria-label="Close">×</button>
    </div>
  )
}

Modal.Body = ({ children }: { children: React.ReactNode }) => (
  <div className="modal-body">{children}</div>
)

Modal.Footer = ({ children }: { children: React.ReactNode }) => (
  <div className="modal-footer">{children}</div>
)

// ───── Usage - composition over configuration ─────
const UserEditModal = ({ isOpen, onClose, user }: {
  isOpen: boolean
  onClose: () => void
  user: UserData
}) => (
  <Modal isOpen={isOpen} onClose={onClose}>
    <Modal.Header>Edit User: {user.name}</Modal.Header>
    <Modal.Body>
      <UserEditForm user={user} />
    </Modal.Body>
    <Modal.Footer>
      <button onClick={onClose}>Cancel</button>
      <button type="submit" form="user-edit-form">Save</button>
    </Modal.Footer>
  </Modal>
)
```

## Performance Optimization (MVP-First)

**⚠️ IMPORTANT**: Optimize only when needed with evidence.

```typescript
// ✅ Good - memo for expensive renders
const ExpensiveComponent = memo(({ data }: { data: LargeDataSet }) => {
  // Expensive rendering logic
  return <ComplexVisualization data={data} />
})

// ✅ Good - useMemo for expensive computations
const useExpensiveComputation = (largeDataSet: LargeDataSet) => {
  const result = useMemo(() => {
    return performExpensiveCalculation(largeDataSet) // Only when actually expensive
  }, [largeDataSet])

  return result
}

// ✅ Good - useCallback to prevent prop changes
const Parent = () => {
  const [count, setCount] = useState(0)

  const handleClick = useCallback(() => {
    setCount(c => c + 1)
  }, [])

  return <MemoizedChild onCount={handleClick} />
}

// ❌ Avoid - unnecessary optimization
const SimpleComponent = memo(({ text }: { text: string }) => <p>{text}</p>) // Not needed

// ❌ Avoid - over-using useMemo
const DisplayName = ({ first, last }: { first: string; last: string }) => {
  const fullName = useMemo(() => `${first} ${last}`, [first, last]) // Overkill
  return <p>{fullName}</p>
}

// ✅ Better - direct computation for simple operations
const DisplayName = ({ first, last }: { first: string; last: string }) => {
  const fullName = `${first} ${last}` // Simple, no memo needed
  return <p>{fullName}</p>
}
```

## Testing React FP Components

### Test Custom Hooks

```typescript
// __tests__/useUserLogic.test.ts
import { renderHook } from '@testing-library/react-hooks'
import { useUserLogic } from '../useUserLogic'

describe('useUserLogic', () => {
  it('processes user data correctly', () => {
    const { result } = renderHook(() =>
      useUserLogic(
        { id: '1', name: '  John  ', email: 'john@test.com' },
        { showEmail: true, variant: 'compact' }
      )
    )

    expect(result.current.displayData.displayName).toBe('John')
    expect(result.current.displayData.email).toBe('john@test.com')
  })

  it('hides email when config.showEmail is false', () => {
    const { result } = renderHook(() =>
      useUserLogic(
        { id: '1', name: 'John', email: 'john@test.com' },
        { showEmail: false, variant: 'compact' }
      )
    )

    expect(result.current.displayData.shouldShowEmail).toBe(false)
  })
})
```

### Test Components with React Testing Library

```typescript
// __tests__/UserCard.test.tsx
import { render, screen, userEvent } from '@testing-library/react'
import UserCard from '../UserCard'

describe('UserCard', () => {
  it('renders user data correctly', () => {
    render(
      <UserCard
        userData={{ id: '1', name: 'John', email: 'john@test.com' }}
        config={{ showEmail: true, variant: 'compact' }}
        onAction={jest.fn()}
      />
    )

    expect(screen.getByText('John')).toBeInTheDocument()
    expect(screen.getByText('john@test.com')).toBeInTheDocument()
  })

  it('calls onAction when button clicked', async () => {
    const onAction = jest.fn()
    render(
      <UserCard
        userData={{ id: '1', name: 'John', email: 'john@test.com' }}
        config={{ showEmail: true, variant: 'compact' }}
        onAction={onAction}
      />
    )

    await userEvent.click(screen.getByRole('button'))
    expect(onAction).toHaveBeenCalled()
  })
})
```

## Anti-Patterns (AVOID)

### ❌ Overusing Context

```typescript
// ❌ Context for local state
const UserContext = createContext<UserData | null>(null)

// ✅ Props for local state (simpler)
<UserCard userData={user} />
```

### ❌ Premature Memoization

```typescript
// ❌ Memoizing everything
const Component = () => {
  const a = useMemo(() => 1 + 1, []) // Overkill
  const b = useMemo(() => 'hello', []) // Overkill
  const c = useCallback(() => {}, []) // Overkill when passed to non-memoized children
}

// ✅ Memoize only when needed
const Component = () => {
  const a = 2 // Simple calculation
  const b = 'hello' // Simple value
  const c = () => {} // Only memo if passed to memoized child
}
```

## Complete Component Example

```typescript
// ProductCard.tsx
import { memo, useMemo, useCallback } from 'react'

interface Product {
  id: string
  name: string
  price: number
  inStock: boolean
}

// ───── Custom hook ─────
const useProductLogic = (product: Product) => {
  const displayData = useMemo(() => ({
    ...product,
    formattedPrice: `$${product.price.toFixed(2)}`,
    availability: product.inStock ? 'In Stock' : 'Out of Stock'
  }), [product])

  const cssClasses = useMemo(() => ({
    card: `product-card ${product.inStock ? 'in-stock' : 'out-of-stock'}`,
    price: `product-price ${product.inStock ? 'available' : 'unavailable'}`
  }), [product.inStock])

  return { displayData, cssClasses }
}

// ───── Component ─────
interface ProductCardProps {
  product: Product
  onAddToCart: (productId: string) => void
}

const ProductCard = memo<ProductCardProps>(({ product, onAddToCart }) => {
  const { displayData, cssClasses } = useProductLogic(product)

  const handleAddToCart = useCallback(() => {
    if (product.inStock) {
      onAddToCart(product.id)
    }
  }, [product.inStock, product.id, onAddToCart])

  return (
    <div className={cssClasses.card}>
      <h3>{displayData.name}</h3>
      <p className={cssClasses.price}>{displayData.formattedPrice}</p>
      <p className="availability">{displayData.availability}</p>
      <button onClick={handleAddToCart} disabled={!product.inStock}>
        Add to Cart
      </button>
    </div>
  )
})

ProductCard.displayName = 'ProductCard'

export { ProductCard }
```

## Quality Gates

Before implementing any React component:

1. ✅ **Pure custom hook**: Business logic separated from presentation?
2. ✅ **HOC for DI**: Dependencies injected via HOC when appropriate?
3. ✅ **Appropriate memoization**: Using memo/useMemo/useCallback only when needed?
4. ✅ **Compound components**: Using composition for flexible APIs?
5. ✅ **Testability**: Can inject mocks for all dependencies?
6. ✅ **FP principles**: Pure functions, immutable updates?

## Foundation Reference

**Core FP Principles**: `/fp:core`
- Purity and side effect isolation
- Composition patterns
- Dependency injection
- Immutability
- Testing strategies

## Success Metrics

- **Testability**: 100% testable custom hooks
- **Performance**: Appropriate memoization, sub-100ms renders
- **Maintainability**: Clear separation of concerns
- **Code Quality**: Simple, readable component logic
- **Bundle Size**: Tree-shakeable, minimal overhead

## Philosophy

*"Pure component architecture through custom hooks, HOCs for dependency injection, and appropriate memoization - optimize for testability and simplicity over premature optimization."*

## Migration to Agent Skills

**When ready to migrate:**

1. Remove this command file: `rm commands/fp/react*.md`
2. Skills automatically available at: `~/.claude/skills/js-fp-react/SKILL.md`
3. Just describe what you need - no commands required!

**Example**: "Create a React component with custom hooks for user authentication and proper dependency injection"
