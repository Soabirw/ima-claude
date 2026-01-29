---
name: "rg"
description: "Ripgrep (rg) - fast recursive search tool. Prefer over grep/find for code search. Respects .gitignore, searches recursively, supports regex. Use for file content search, file listing, pattern matching."
triggers:
  - "ripgrep"
  - "rg"
  - "search files"
  - "find in files"
  - "grep"
  - "search code"
  - "find pattern"
---

# Ripgrep (rg) - Preferred Search Tool

**Always use `rg` instead of `grep` or `find -name`** - it's faster, has better defaults, and respects `.gitignore`.

## Quick Reference

### Basic Search
```bash
# Search for pattern in current directory (recursive)
rg "pattern"

# Search specific file or directory
rg "pattern" src/
rg "pattern" file.ts

# Case-insensitive search
rg -i "pattern"

# Word boundary match (whole words only)
rg -w "function"

# Fixed string (not regex)
rg -F "exact.string.match"
```

### Output Control
```bash
# Show N lines of context (before and after)
rg -C 3 "pattern"

# Lines before (-B) or after (-A) only
rg -B 2 -A 5 "pattern"

# Count matches per file
rg -c "pattern"

# List files with matches only (no content)
rg -l "pattern"
rg --files-with-matches "pattern"

# List files WITHOUT matches
rg --files-without-match "pattern"

# Show only the matched text (not full line)
rg -o "pattern"
```

### File Filtering
```bash
# By file type (built-in types)
rg -t ts "pattern"       # TypeScript only
rg -t py "pattern"       # Python only
rg -t js "pattern"       # JavaScript only
rg -t rust "pattern"     # Rust only

# Exclude file type
rg -T js "pattern"       # Exclude JavaScript

# By glob pattern
rg -g "*.vue" "pattern"           # Only .vue files
rg -g "!*.test.ts" "pattern"      # Exclude test files
rg -g "src/**/*.ts" "pattern"     # TypeScript in src/

# Multiple globs
rg -g "*.ts" -g "*.vue" "pattern"
```

### List Files (No Search)
```bash
# List all files that would be searched
rg --files

# List files matching glob
rg --files -g "*.ts"

# List files in specific directory
rg --files src/components/
```

### Bypass Filters
```bash
# -u levels (unrestricted):
rg -u "pattern"      # Ignore .gitignore
rg -uu "pattern"     # + search hidden files
rg -uuu "pattern"    # + search binary files

# Specific overrides
rg --hidden "pattern"      # Include hidden files
rg --no-ignore "pattern"   # Ignore all ignore files
```

### Advanced Patterns
```bash
# Multiline search
rg -U "start.*\n.*end"

# PCRE2 regex (lookahead/lookbehind)
rg -P "(?<=prefix)pattern(?=suffix)"

# Replace in output (preview, doesn't modify files)
rg "old" -r "new"

# With capture groups
rg "fn (\w+)" -r "function $1"

# JSON output (for scripting)
rg --json "pattern"
```

## Common Recipes

### Find Function/Class Definitions
```bash
# JavaScript/TypeScript
rg "^(export )?(async )?(function|const|class) \w+"
rg "^export (default )?(function|class)"

# Python
rg "^(async )?def \w+|^class \w+"

# PHP
rg "^(public |private |protected )?(static )?(function) \w+"
```

### Find Imports/Requires
```bash
rg "^import .+ from"
rg "require\(['\"]"
```

### Find TODOs/FIXMEs
```bash
rg "TODO|FIXME|HACK|XXX" -g "!node_modules"
```

### Find Files by Extension
```bash
rg --files -g "*.tsx"              # All TSX files
rg --files -g "*.{ts,tsx}"         # TS and TSX
rg --files -g "!*.test.*"          # Exclude test files
```

### Search and Replace Preview
```bash
# See what would change (doesn't modify files)
rg "oldFunction" -r "newFunction" --passthru
```

## vs grep/find

| Task | grep/find (avoid) | rg (prefer) |
|------|-------------------|-------------|
| Search text | `grep -r "pattern" .` | `rg "pattern"` |
| Find files | `find . -name "*.ts"` | `rg --files -g "*.ts"` |
| Case insensitive | `grep -ri "pattern" .` | `rg -i "pattern"` |
| Whole word | `grep -rw "word" .` | `rg -w "word"` |
| Show context | `grep -r -C 3 "pattern" .` | `rg -C 3 "pattern"` |
| List files only | `grep -rl "pattern" .` | `rg -l "pattern"` |

## Key Advantages

1. **Speed**: 2-10x faster than grep on large codebases
2. **Smart defaults**: Respects `.gitignore`, skips binary/hidden files
3. **Recursive by default**: No `-r` flag needed
4. **Better regex**: Rust regex engine, optional PCRE2
5. **Built-in file types**: `-t ts`, `-t py`, etc.
6. **Colored output**: Easy to read in terminal

## Configuration

Create `~/.ripgreprc` for persistent settings:
```shell
# Smart case (case-insensitive unless uppercase used)
--smart-case

# Max line length for display
--max-columns=150
--max-columns-preview

# Include hidden files by default
# --hidden

# Custom file type
--type-add
web:*.{html,css,js,ts,vue}
```

Set the config file path:
```bash
export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"
```

## Type List

View all built-in types:
```bash
rg --type-list
```

Common types: `ts`, `js`, `py`, `rust`, `go`, `java`, `php`, `ruby`, `css`, `html`, `json`, `yaml`, `md`, `sh`
