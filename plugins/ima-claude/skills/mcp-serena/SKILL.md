---
name: mcp-serena
description: "Use Serena MCP for ALL code navigation and investigation — it saves 40-70% tokens vs reading files. Use INSTEAD of Read/Grep when exploring code structure: get_symbols_overview (structure without reading), find_symbol (locate any class/method/function), find_referencing_symbols (all callers). Triggers on: where is X used, find references, what calls X, rename X, refactor X, show X usage, track down X, what does class X look like, find the function, look up the method, explore this file, understand this code, how is X implemented. With PHPStorm+Serena: works across PHP, TypeScript, JS, Vue, Python."
---

# Serena MCP - Code Symbol Operations

Use Serena for code symbol discovery and modification instead of reading entire files.

## Setup: Direct Access

Serena runs directly (not through Airis gateway). Tools are available as `mcp__serena__*`.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__serena__jet_brains_find_symbol` | Find symbols by name path pattern |
| `mcp__serena__jet_brains_find_referencing_symbols` | Find all references to a symbol |
| `mcp__serena__rename_symbol` | Rename symbol across entire codebase |
| `mcp__serena__jet_brains_get_symbols_overview` | Get top-level symbols in a file |
| `mcp__serena__search_for_pattern` | Regex pattern search (better for Vue) |
| `mcp__serena__list_dir` | List directory contents |

## Workflow: Symbol Discovery

### Find a Symbol

```
mcp__serena__jet_brains_find_symbol
  name_path_pattern: "UserService"
  include_body: false
  depth: 1
```

- Use `depth: 1` to see methods/properties
- Use `include_body: true` only when you need implementation details
- Use `relative_path` to narrow search scope

### Find All References

```
mcp__serena__jet_brains_find_referencing_symbols
  name_path: "UserService/getUserData"
  relative_path: "src/services/user.ts"
  include_info: true
```

### Get File Overview

```
mcp__serena__jet_brains_get_symbols_overview
  relative_path: "src/services/user.ts"
  depth: 1
```

Better than reading entire file when you just need structure.

## Workflow: Symbol Modification

### Rename Symbol

```
mcp__serena__rename_symbol
  name_path: "getUserData"
  relative_path: "src/services/user.ts"
  new_name: "fetchUserData"
```

Automatically updates all references across the codebase.

## Gitignore Handling (Important)

**Known Issue**: Serena has problems with complex `.gitignore` negation patterns (GitHub Issue #600).

Example problem:
```gitignore
plugins/           # Ignored
!plugins/custom/   # Re-included (but Serena may still ignore it)
```

Serena's `is_ignored_path()` returns `True` early, bypassing negation logic.

### Workarounds

**For `list_dir`** - use `skip_ignored_files: false`:
```
mcp__serena__list_dir
  relative_path: "plugins"
  recursive: true
  skip_ignored_files: false
```

**For `search_for_pattern`** - target folder directly with `relative_path`:
```
mcp__serena__search_for_pattern
  substring_pattern: "functionName"
  relative_path: "plugins/custom"
  context_lines_before: 2
  context_lines_after: 2
```

**Alternative** - use explicit glob to include:
```
mcp__serena__search_for_pattern
  substring_pattern: "functionName"
  paths_include_glob: "**/plugins/**"
```

## Vue 3 / Quasar Projects

**Important**: TypeScript LSP doesn't fully understand Vue 3 `<script setup>` syntax.

For `.vue` files and `src/composables/`, prefer pattern search:

```
mcp__serena__search_for_pattern
  substring_pattern: "import.*useAuth|from.*useAuth"
  paths_include_glob: "**/*.vue"
  context_lines_before: 2
  context_lines_after: 2
```

**Decision Logic for Vue**:
```
IF target is .vue file OR src/composables/:
    → Use search_for_pattern (more reliable)
ELSE IF pure .ts/.js files:
    → Use LSP tools (find_symbol, find_referencing_symbols)
```

## Decision Logic

```
IF need to find/understand code symbols:
    → Use find_symbol, find_referencing_symbols
ELSE IF need to rename/refactor symbol:
    → Use rename_symbol (handles dependencies automatically)
ELSE IF simple text pattern search:
    → Use search_for_pattern
ELSE IF searching in gitignore-negated folder:
    → Use relative_path to target directly OR skip_ignored_files: false
ELSE IF reading full file needed:
    → Use native Read tool
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| Symbol not found | Try broader name_path_pattern, check spelling |
| Vue SFC issues | Switch to search_for_pattern |
| Gitignore blocking folder | Use relative_path directly or skip_ignored_files: false |
| Rename failed | Check if symbol is in external dependency |
| Too many results | Add relative_path to narrow scope |

## When NOT to Use

- Simple text searches (use Grep)
- Reading configuration files (use Read)
- Operations on non-code files (markdown, json, yaml)
- When you need file content, not symbol info

## Examples

| User Request | Action |
|--------------|--------|
| "Where is UserService used?" | find_referencing_symbols(name_path: "UserService") |
| "Rename getUserData to fetchUser" | rename_symbol(name_path: "getUserData", new_name: "fetchUser") |
| "What methods does AuthService have?" | find_symbol(name_path: "AuthService", depth: 1) |
| "Find useAuth usage in Vue files" | search_for_pattern(pattern: "useAuth", glob: "**/*.vue") |
| "Search in plugins folder" | search_for_pattern(relative_path: "plugins/custom") |
| "List plugins directory" | list_dir(relative_path: "plugins", skip_ignored_files: false) |
| "Show me the user.ts file" | Native Read (full file needed) |
