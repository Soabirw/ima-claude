---
name: mcp-serena
description: "Use Serena MCP for ALL code navigation and investigation — it saves 40-70% tokens vs reading files. Use INSTEAD of Read/Grep when exploring code structure: get_symbols_overview (structure without reading), find_symbol (locate any class/method/function), find_referencing_symbols (all callers). Triggers on: where is X used, find references, what calls X, rename X, refactor X, show X usage, track down X, what does class X look like, find the function, look up the method, explore this file, understand this code, how is X implemented. With PHPStorm+Serena: works across PHP, TypeScript, JS, Vue, Python."
---

# Serena MCP - Code Symbol Operations

Use Serena FIRST for all code investigation — before Read/Grep/Glob. Reading entire files wastes 40-70% token budget. Serena gives precise symbol-level access: structure without content, bodies only when needed, references without scanning every file.

Tools available as `mcp__serena__*` (direct access, not through gateway).

## Tools

| Tool | Purpose |
|------|---------|
| `jet_brains_find_symbol` | Find symbols by name path pattern |
| `jet_brains_find_referencing_symbols` | Find all references to a symbol |
| `rename_symbol` | Rename symbol across entire codebase |
| `jet_brains_get_symbols_overview` | Get top-level symbols in a file |
| `search_for_pattern` | Regex pattern search (preferred for Vue) |
| `list_dir` | List directory contents |

## Symbol Discovery

```
mcp__serena__jet_brains_find_symbol
  name_path_pattern: "UserService"
  include_body: false
  depth: 1
```

- `depth: 1` — see methods/properties
- `include_body: true` — only when implementation needed
- `relative_path` — narrow search scope

```
mcp__serena__jet_brains_find_referencing_symbols
  name_path: "UserService/getUserData"
  relative_path: "src/services/user.ts"
  include_info: true
```

```
mcp__serena__jet_brains_get_symbols_overview
  relative_path: "src/services/user.ts"
  depth: 1
```

## Symbol Modification

```
mcp__serena__rename_symbol
  name_path: "getUserData"
  relative_path: "src/services/user.ts"
  new_name: "fetchUserData"
```

Updates all references automatically.

## Gitignore Handling

Known issue: complex `.gitignore` negation patterns block Serena (GitHub #600). Example: `plugins/` ignored + `!plugins/custom/` re-included — Serena may still skip it.

Workarounds:

```
# list_dir — use skip_ignored_files: false
mcp__serena__list_dir
  relative_path: "plugins"
  recursive: true
  skip_ignored_files: false

# search_for_pattern — target folder directly
mcp__serena__search_for_pattern
  substring_pattern: "functionName"
  relative_path: "plugins/custom"
  context_lines_before: 2
  context_lines_after: 2

# Or use explicit glob
mcp__serena__search_for_pattern
  substring_pattern: "functionName"
  paths_include_glob: "**/plugins/**"
```

## Vue 3 / Quasar Projects

TypeScript LSP doesn't fully understand Vue 3 `<script setup>`. For `.vue` files and `src/composables/`, use pattern search:

```
mcp__serena__search_for_pattern
  substring_pattern: "import.*useAuth|from.*useAuth"
  paths_include_glob: "**/*.vue"
  context_lines_before: 2
  context_lines_after: 2
```

```
IF .vue file OR src/composables/:
    → search_for_pattern
ELSE IF .ts/.js files:
    → find_symbol, find_referencing_symbols
```

## Decision Logic

```
IF find/understand code symbols:
    → find_symbol, find_referencing_symbols
ELSE IF rename/refactor:
    → rename_symbol
ELSE IF text pattern search:
    → search_for_pattern
ELSE IF gitignore-negated folder:
    → relative_path directly OR skip_ignored_files: false
ELSE IF full file content needed:
    → native Read tool
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| Symbol not found | Broader name_path_pattern, check spelling |
| Vue SFC issues | Switch to search_for_pattern |
| Gitignore blocking | Use relative_path or skip_ignored_files: false |
| Rename failed | Check if symbol is in external dependency |
| Too many results | Add relative_path to narrow scope |

## Fall Back to Read/Grep Only For

- Non-code files: markdown, JSON, YAML, config (LSP doesn't index these)
- Serena unavailable or returning errors
- Full file content after overview identified what to read

Never use Grep for code searches — use `search_for_pattern` or `find_symbol`.

## Quick Reference

| Request | Tool |
|---------|------|
| "Where is UserService used?" | `find_referencing_symbols(name_path: "UserService")` |
| "Rename getUserData to fetchUser" | `rename_symbol(name_path: "getUserData", new_name: "fetchUser")` |
| "What methods does AuthService have?" | `find_symbol(name_path: "AuthService", depth: 1)` |
| "Find useAuth in Vue files" | `search_for_pattern(pattern: "useAuth", glob: "**/*.vue")` |
| "Search in plugins folder" | `search_for_pattern(relative_path: "plugins/custom")` |
| "List plugins directory" | `list_dir(relative_path: "plugins", skip_ignored_files: false)` |
| "Show me user.ts" | Native Read |
