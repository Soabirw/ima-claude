---
name: "js-fp-vue"
description: "FP patterns for Vue.js with composables, wrappers, and pure components - references js-fp core"
---

# JavaScript FP - Vue.js

Functional programming patterns for Vue.js components with composables, wrapper patterns, and pure component architecture.

## When to Use This Skill

- Building Vue.js 3+ components
- Need pure, testable component logic
- Implementing composables with FP principles
- Wrapper patterns for external dependencies
- Performance optimization without over-engineering

## Core Philosophy

**Pure components** with **business logic in composables**, **wrapper pattern for side effects**, and **simple state management** (composables > stores for 95% of use cases).

**Foundation**: This skill builds on `js-fp` core principles. Reference `../js-fp/SKILL.md` for purity, composition, dependency injection, and testing patterns.

## Pure Component with Composable Pattern

**Rule**: Separate business logic (composables) from presentation (components).

```vue
<script setup lang="ts">
/**
 * Business logic in composables, presentation in component
 * - Zero side effects in component
 * - All logic in composables
 * - 100% testable through dependency injection
 */

import { computed, readonly, toRef } from 'vue'

interface UserData {
  id: string
  name: string
  email: string
}

interface UserConfig {
  showEmail: boolean
  variant: 'compact' | 'detailed'
}

// ───── Composable with pure business logic ─────
const useUserLogic = (
  userData: Readonly<Ref<UserData>>,
  config: Readonly<Ref<UserConfig>>
) => {
  // Pure computation - no side effects
  const displayData = computed(() => {
    const user = userData.value
    const cfg = config.value

    return {
      ...user,
      displayName: user.name.trim(),
      ...(cfg.showEmail ? {} : { email: undefined })
    }
  })

  // Pre-compiled CSS for performance
  const cssClasses = computed(() => ({
    card: `user-card user-card--${config.value.variant}`,
    name: `user-card__name user-card__name--${config.value.variant}`
  }))

  return { displayData, cssClasses }
}

// ───── Component props ─────
const props = defineProps<{
  userData: UserData
  config: UserConfig
}>()

// ───── Use composable ─────
const { displayData, cssClasses } = useUserLogic(
  readonly(toRef(props, 'userData')),
  readonly(toRef(props, 'config'))
)
</script>

<template>
  <div :class="cssClasses.card">
    <h3 :class="cssClasses.name">{{ displayData.displayName }}</h3>
    <p v-if="config.showEmail && displayData.email">{{ displayData.email }}</p>
  </div>
</template>
```

## Wrapper Pattern for External Dependencies

**Rule**: Isolate side effects in wrapper layer, keep inner component pure.

```vue
<!-- UserDisplayPure.vue - Pure Inner Component -->
<script setup lang="ts">
const props = defineProps<{
  user: UserData
}>()

const emit = defineEmits<{
  update: [user: UserData]
}>()

const handleUpdate = (updates: Partial<UserData>) => {
  const updatedUser = { ...props.user, ...updates }
  emit('update', updatedUser)
}
</script>

<template>
  <div class="user-display">
    <h3>{{ user.name }}</h3>
    <button @click="handleUpdate({ name: 'Updated' })">Update</button>
  </div>
</template>

<!-- UserDisplayWrapper.vue - Wrapper with Side Effects -->
<script setup lang="ts">
import { ref } from 'vue'
import UserDisplayPure from './UserDisplayPure.vue'

const props = defineProps<{
  userId: string
}>()

// Side effect: External API call
const user = ref<UserData | null>(null)
const loading = ref(true)
const error = ref<Error | null>(null)

const fetchUser = async () => {
  try {
    loading.value = true
    user.value = await userApi.getUser(props.userId)
  } catch (e) {
    error.value = e as Error
  } finally {
    loading.value = false
  }
}

// Side effect isolated to wrapper
const handleUpdate = async (updatedUser: UserData) => {
  await userApi.updateUser(updatedUser)
  await fetchUser() // Refresh
}

// Initial load
fetchUser()
</script>

<template>
  <UserDisplayPure
    v-if="user && !loading"
    :user="user"
    @update="handleUpdate"
  />
  <div v-else-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
</template>
```

## Composable Factory Pattern

**Rule**: Pre-compile expensive configurations for performance.

```typescript
// composables/useUserFactory.ts

// Factory creates optimized composable
const createUserComposable = (defaultConfig: UserConfig) => {
  // Pre-compile static configuration (hot path optimization)
  const compiledClasses = {
    compact: {
      card: 'user-card user-card--compact',
      name: 'user-card__name user-card__name--compact'
    },
    detailed: {
      card: 'user-card user-card--detailed',
      name: 'user-card__name user-card__name--detailed'
    }
  }

  return (userData: Readonly<Ref<UserData>>, config?: Partial<UserConfig>) => {
    const mergedConfig = { ...defaultConfig, ...config }

    const displayData = computed(() => ({
      ...userData.value,
      displayName: userData.value.name.trim()
    }))

    // O(1) lookup instead of string concatenation
    const cssClasses = computed(() => compiledClasses[mergedConfig.variant])

    return { displayData, cssClasses }
  }
}

// Usage: Pre-compile for different contexts
export const useCompactUser = createUserComposable({
  showEmail: false,
  variant: 'compact'
})

export const useDetailedUser = createUserComposable({
  showEmail: true,
  variant: 'detailed'
})
```

## State Management (Composables > Stores)

**Rule**: Use composables for 95% of state management. Only use Pinia/Vuex for truly global state.

```typescript
// composables/useUserState.ts

export const useUserState = () => {
  const users = ref<UserData[]>([])
  const loading = ref(false)

  // Pure functions for state transitions
  const addUser = (user: UserData) => {
    users.value = [...users.value, user] // Immutable
  }

  const updateUser = (userId: string, updates: Partial<UserData>) => {
    users.value = users.value.map(user =>
      user.id === userId ? { ...user, ...updates } : user
    ) // Immutable
  }

  const removeUser = (userId: string) => {
    users.value = users.value.filter(user => user.id !== userId) // Immutable
  }

  // Side effect isolated
  const fetchUsers = async () => {
    loading.value = true
    try {
      users.value = await userApi.getUsers()
    } finally {
      loading.value = false
    }
  }

  return {
    users: readonly(users),
    loading: readonly(loading),
    addUser,
    updateUser,
    removeUser,
    fetchUsers
  }
}

// Usage in component
const { users, addUser, fetchUsers } = useUserState()
```

## Anti-Patterns (AVOID)

### ❌ Pinia/Vuex Over-Usage

```typescript
// ❌ Complex store for simple state
const useUserStore = defineStore('users', {
  state: () => ({ users: [], loading: false }),
  actions: {
    async fetchUsers() { /* complex async logic */ }
  }
})

// ✅ Simple composable (covers 95% of use cases)
const useUsers = () => {
  const users = ref<UserData[]>([])
  const loading = ref(false)

  const fetchUsers = async () => {
    loading.value = true
    users.value = await userApi.getUsers()
    loading.value = false
  }

  return { users: readonly(users), loading: readonly(loading), fetchUsers }
}
```

### ❌ Reactive Over-Engineering

```typescript
// ❌ Unnecessary reactive complexity
const user = reactive({
  profile: reactive({
    settings: reactive({
      theme: 'dark'
    })
  })
})

// ✅ Simple ref with computed when needed
const userSettings = ref({ theme: 'dark', notifications: true })
const isDarkTheme = computed(() => userSettings.value.theme === 'dark')
```

### ❌ Watch Over-Usage

```typescript
// ❌ Watch for derived state
const fullName = ref('')
watch([firstName, lastName], () => {
  fullName.value = `${firstName.value} ${lastName.value}`
})

// ✅ Computed for derived state
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
```

## Vue 3 Composition API Best Practices

### Reactive vs. Ref

```typescript
// Use ref for primitives and simple objects
const count = ref(0)
const user = ref<UserData>({ id: '1', name: 'Alice', email: 'alice@test.com' })

// Use reactive sparingly (only for complex nested objects)
const state = reactive({
  users: [],
  filters: { search: '', minAge: 0 }
})

// Prefer computed over watch
const filteredUsers = computed(() =>
  state.users.filter(u => u.name.includes(state.filters.search))
)
```

### Lifecycle Hooks

```typescript
import { onMounted, onUnmounted } from 'vue'

// Side effects in lifecycle hooks
onMounted(() => {
  fetchData()
  const interval = setInterval(refreshData, 60000)

  onUnmounted(() => {
    clearInterval(interval)
  })
})
```

## Testing Vue FP Components

### Test Pure Composables

```typescript
// composables/__tests__/useUserLogic.test.ts
import { ref } from 'vue'
import { useUserLogic } from '../useUserLogic'

describe('useUserLogic', () => {
  it('computes display data correctly', () => {
    const userData = ref({
      id: '1',
      name: ' John ',
      email: 'john@test.com'
    })
    const config = ref({
      showEmail: true,
      variant: 'compact' as const
    })

    const { displayData } = useUserLogic(userData, config)

    expect(displayData.value).toEqual({
      id: '1',
      name: ' John ',
      email: 'john@test.com',
      displayName: 'John' // Trimmed
    })
  })

  it('hides email when config.showEmail is false', () => {
    const userData = ref({
      id: '1',
      name: 'John',
      email: 'john@test.com'
    })
    const config = ref({
      showEmail: false,
      variant: 'compact' as const
    })

    const { displayData } = useUserLogic(userData, config)

    expect(displayData.value.email).toBeUndefined()
  })
})
```

### Test Components with Vue Test Utils

```typescript
// components/__tests__/UserCard.test.ts
import { mount } from '@vue/test-utils'
import UserCard from '../UserCard.vue'

describe('UserCard', () => {
  it('renders user data correctly', () => {
    const wrapper = mount(UserCard, {
      props: {
        userData: { id: '1', name: 'John', email: 'john@test.com' },
        config: { showEmail: true, variant: 'compact' }
      }
    })

    expect(wrapper.find('.user-card__name').text()).toBe('John')
    expect(wrapper.find('p').text()).toBe('john@test.com')
  })

  it('hides email when config.showEmail is false', () => {
    const wrapper = mount(UserCard, {
      props: {
        userData: { id: '1', name: 'John', email: 'john@test.com' },
        config: { showEmail: false, variant: 'compact' }
      }
    })

    expect(wrapper.find('p').exists()).toBe(false)
  })
})
```

## Complete Component Example

```vue
<!-- ProductCard.vue -->
<script setup lang="ts">
import { computed, readonly, toRef } from 'vue'

interface Product {
  id: string
  name: string
  price: number
  inStock: boolean
}

// ───── Pure composable ─────
const useProductLogic = (product: Readonly<Ref<Product>>) => {
  const displayData = computed(() => ({
    ...product.value,
    formattedPrice: `$${product.value.price.toFixed(2)}`,
    availability: product.value.inStock ? 'In Stock' : 'Out of Stock'
  }))

  const cssClasses = computed(() => ({
    card: `product-card ${product.value.inStock ? 'in-stock' : 'out-of-stock'}`,
    price: `product-price ${product.value.inStock ? 'available' : 'unavailable'}`
  }))

  return { displayData, cssClasses }
}

// ───── Component setup ─────
const props = defineProps<{
  product: Product
}>()

const emit = defineEmits<{
  addToCart: [productId: string]
}>()

const { displayData, cssClasses } = useProductLogic(
  readonly(toRef(props, 'product'))
)

const handleAddToCart = () => {
  if (props.product.inStock) {
    emit('addToCart', props.product.id)
  }
}
</script>

<template>
  <div :class="cssClasses.card">
    <h3>{{ displayData.name }}</h3>
    <p :class="cssClasses.price">{{ displayData.formattedPrice }}</p>
    <p class="availability">{{ displayData.availability }}</p>
    <button
      @click="handleAddToCart"
      :disabled="!product.inStock"
    >
      Add to Cart
    </button>
  </div>
</template>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
}

.product-card.in-stock {
  border-color: #28a745;
}

.product-card.out-of-stock {
  opacity: 0.6;
}

.product-price.unavailable {
  text-decoration: line-through;
}
</style>
```

## Quality Gates

Before implementing any Vue component:

1. ✅ **Pure composable**: Business logic separated from presentation?
2. ✅ **Wrapper pattern**: Side effects isolated to wrapper component?
3. ✅ **Reactive optimization**: Using computed over watch?
4. ✅ **State management**: Using composables instead of store (unless truly global)?
5. ✅ **Testability**: Can inject mocks for all dependencies?
6. ✅ **FP principles**: Pure functions, immutable updates?
7. ✅ **Performance**: Pre-compiled configurations when appropriate?

## When to Load Additional Content

### Composables Advanced
**File**: `composables-advanced.md`
**When**: Complex composable patterns, advanced composition
**Contains**: Advanced composable patterns, lifecycle integration, provide/inject

### Reactivity Patterns
**File**: `reactivity-patterns.md`
**When**: Performance optimization, reactivity issues
**Contains**: Deep reactivity patterns, performance optimization, memory management

### Working Examples
**Directory**: `examples/`
**When**: Need complete working component examples
**Contains**: Full component examples, composables, wrappers, tests

## Foundation Reference

**Core FP Principles**: `../js-fp/SKILL.md`
- Purity and side effect isolation
- Composition patterns
- Dependency injection
- Immutability
- Testing strategies

**Deep Dive**: `../js-fp/core-principles.md` for complete FP philosophy

## Success Metrics

- **Testability**: 100% testable composables
- **Performance**: Pre-compiled configurations, reactive optimization
- **Maintainability**: Clear separation of concerns
- **Code Quality**: Simple, readable component logic
- **Bundle Size**: Minimal overhead, tree-shakeable composables

## Philosophy

*"Pure component architecture through composables, wrapper patterns for side effects, and simple state management - optimize for testability and simplicity over clever reactivity."*
