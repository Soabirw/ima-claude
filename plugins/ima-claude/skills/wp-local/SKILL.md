---
name: "wp-local"
description: "Run WordPress WP-CLI commands in Flywheel Local WP environments. Use for database queries, plugin management, user operations, theme operations, cache clearing, cron jobs. Auto-configures environment without affecting main Claude session. Triggers on: wp plugin, wp db, wp user, wp option, wp-cli, Local WP, Flywheel."
---

# WordPress WP-Local

Execute WP-CLI commands in Flywheel Local WP environments without disrupting Claude Code's main session.

## Quick Start

**Prerequisites**:
- **Recommended**: Use Kitty terminal with `$WP_LOCAL_SITE` configured (see Configuration)
- **Alternative**: Create `.wp-local` file in project root: `echo "19efkkzWB" > .wp-local`

**Run wp commands**:
```bash
bash ~/.claude/skills/wp-local/scripts/wp-local.sh plugin list
bash ~/.claude/skills/wp-local/scripts/wp-local.sh db query "SELECT * FROM wp_posts LIMIT 5"
bash ~/.claude/skills/wp-local/scripts/wp-local.sh user list
```

**With shell alias** (recommended, see Configuration):
```bash
wpl plugin list
wpl db query "SELECT * FROM wp_users"
```

**Verify configuration**:
```bash
echo $WP_LOCAL_SITE  # Should show UUID like: -hJRW0lQL
```

## How It Works

1. **Kitty integration**: `$WP_LOCAL_SITE` env var set by Kitty config (or `.wp-local` file fallback)
2. **Isolated execution**: Each wp command runs in subprocess with Local WP environment sourced
3. **Clean main session**: Claude Code tab environment unaffected (MCPs work normally)
4. **Friendly names**: Optional mapping via `~/.claude/wp-local-sites.json`

**Priority order:**
1. `$WP_LOCAL_SITE` environment variable (Kitty terminal integration)
2. `.wp-local` file (project-specific override)
3. Error if neither configured

## Common Commands

### Database Operations
```bash
wpl db query "SELECT * FROM wp_users"
wpl db export dump.sql
wpl search-replace 'old.com' 'new.com'
```

### Plugin Management
```bash
wpl plugin list
wpl plugin activate my-plugin
wpl plugin install contact-form-7 --activate
```

### User Operations
```bash
wpl user list
wpl user create testuser test@example.com --role=editor
```

### Theme Operations
```bash
wpl theme list
wpl theme activate twentytwentyfour
```

### Cache & Transients
```bash
wpl cache flush
wpl transient delete --all
```

### Options
```bash
wpl option get siteurl
wpl option update blogname "New Site Name"
```

## Configuration

See [`references/configuration.md`](references/configuration.md) for:
- **Recommended**: Kitty terminal integration with `$WP_LOCAL_SITE`
- **Alternative**: Creating `.wp-local` file for project-specific override
- Finding site UUIDs
- Setting up friendly name mapping
- Shell alias setup
- Troubleshooting

**Quick Kitty Config**:
Modify Claude Code tab in `/home/eric/kitty/configs/[site].conf`:
```conf
launch bash -c "export WP_LOCAL_SITE='UUID'; exec bash"
```

## Integration

**With php-fp-wordpress**:
- Test plugins during development
- Verify security functions
- Check database operations

**With js-fp-wordpress**:
- Test script enqueuing
- Verify AJAX endpoints
- Check jQuery availability

Example workflow:
```bash
# 1. Develop plugin with php-fp-wordpress patterns
# 2. Test with wp-local
wpl plugin activate my-new-plugin
wpl eval "var_dump(current_user_can('edit_posts'));"
```

## Why This Approach?

**Problem**: Local WP environment breaks MCP servers when sourced in main session.

**Solution**: Bash subprocess isolation:
- Main session stays clean → MCPs work
- Each wp command gets proper environment → wp works
- No persistent environment pollution
- Simple, native Unix pattern

## Quality Gates

Before running destructive commands:
- ✅ Correct site (.wp-local points to intended site)
- ✅ Backup if needed (database modifications)
- ✅ Site running (Local WP app)
