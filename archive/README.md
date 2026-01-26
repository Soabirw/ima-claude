# Archive

This directory contains deprecated content kept for reference only.

## Contents

### commands/fp/
The original `/fp:*` command system that has been superseded by Skills.

**Migration**: See `docs/MIGRATING-FROM-COMMANDS.md`

**Status**: Deprecated. Use Skills instead:
- `/fp:core` → `js-fp` skill
- `/fp:api` → `js-fp-api` skill
- `/fp:react` → `js-fp-react` skill
- `/fp:vue` → `js-fp-vue` skill
- `/fp:wordpress` → `php-fp-wordpress` skill

### commands/fp-legacy/
Even older command versions, kept for historical reference.

## Why Keep This?

1. **Reference**: See how patterns evolved
2. **Migration**: Help users moving from old commands
3. **Documentation**: Some detailed examples may be useful

## Do Not Use

These commands are NOT loaded by ima-claude. They exist only as reference material.

To use FP patterns, invoke the appropriate Skill:
```
"Use the js-fp skill to review this code"
"Apply js-fp-react patterns to this component"
```
