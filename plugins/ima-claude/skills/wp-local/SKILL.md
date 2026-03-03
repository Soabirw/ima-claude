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
`wp db query <sql>` · `wp db export [file]` · `wp db import <file>` · `wp search-replace <old> <new> [table...]`
```bash
wpl db query "SELECT * FROM wp_users"
wpl db export dump.sql
wpl db import dump.sql
wpl search-replace 'old.com' 'new.com' --dry-run
wpl search-replace 'old.com' 'new.com' --all-tables
```

### Plugin Management
`wp plugin list` · `wp plugin activate <plugin>` · `wp plugin deactivate <plugin>` · `wp plugin install <plugin> [--activate]`
```bash
wpl plugin list
wpl plugin list --status=active --format=json
wpl plugin activate my-plugin
wpl plugin deactivate my-plugin
wpl plugin install contact-form-7 --activate
wpl plugin is-installed woocommerce && echo "yes"
```

### User Operations
`wp user list` · `wp user create <login> <email> [--role=<role>]` · `wp user update <user> [--field=value]`
```bash
wpl user list
wpl user list --role=administrator --format=table
wpl user create testuser test@example.com --role=editor
wpl user update 1 --display_name="Admin User"
wpl user add-role 2 editor
```

### Theme Operations
`wp theme list` · `wp theme activate <theme>` · `wp theme install <theme>`
```bash
wpl theme list
wpl theme activate twentytwentyfour
wpl theme status flavor
```

### Cache & Transients
`wp cache flush` · `wp transient delete --all` · `wp transient get <key>`
```bash
wpl cache flush
wpl transient delete --all
wpl transient get my_transient_key
wpl transient list --format=table
```

### Options
`wp option get <key>` · `wp option update <key> <value>` · `wp option list [--search=<pattern>]`
```bash
wpl option get siteurl
wpl option update blogname "New Site Name"
wpl option list --search="woocommerce_*" --format=table
wpl option delete my_old_option
```

### Post & Content
`wp post list [--post_type=<type>]` · `wp post create` · `wp post update <id>` · `wp post delete <id>`
```bash
wpl post list --post_type=page --format=table
wpl post list --post_status=draft --fields=ID,post_title
wpl post create --post_type=post --post_title="Test" --post_status=publish
wpl post update 42 --post_title="Updated Title"
wpl post delete 42 --force
wpl post meta get 42 _thumbnail_id
wpl post meta update 42 custom_field "new value"
```

### Taxonomy & Terms
`wp term list <taxonomy>` · `wp term create <taxonomy> <term>` · `wp term update <taxonomy> <term-id>`
```bash
wpl term list category --format=table
wpl term create category "New Category" --slug=new-category
wpl term update category 5 --name="Renamed"
wpl term delete category 5
```

### Menu
`wp menu list` · `wp menu item list <menu>` · `wp menu item add-post <menu> <post-id>`
```bash
wpl menu list --format=table
wpl menu item list primary-menu
wpl menu item add-post primary-menu 42
wpl menu item add-custom primary-menu "Link" https://example.com
```

### Rewrite Rules
`wp rewrite flush` · `wp rewrite list` · `wp rewrite structure <structure>`
```bash
wpl rewrite flush
wpl rewrite list --format=csv
wpl rewrite structure '/%postname%/'
```

### Scaffold
`wp scaffold plugin <slug>` · `wp scaffold child-theme <slug>` · `wp scaffold post-type <slug>`
```bash
wpl scaffold plugin my-plugin --plugin_name="My Plugin"
wpl scaffold post-type product --plugin=my-plugin
wpl scaffold taxonomy genre --post_types=product --plugin=my-plugin
wpl scaffold child-theme flavor-child --parent_theme=flavor
```

### Eval & Shell
`wp eval <code>` · `wp eval-file <file>` · `wp shell`
```bash
wpl eval "echo home_url();"
wpl eval "var_dump(wp_get_current_user());"
wpl eval "echo get_option('active_plugins') | print_r;"
wpl eval-file test-script.php
```

## Global Flags

These flags work with most WP-CLI commands:

| Flag | Description |
|---|---|
| `--format=<format>` | Output: `table`, `csv`, `json`, `yaml`, `count`, `ids` |
| `--fields=<fields>` | Comma-separated columns to display |
| `--quiet` | Suppress informational messages |
| `--skip-themes` | Skip loading themes (faster execution) |
| `--skip-plugins` | Skip loading all plugins (debug conflicts) |
| `--skip-plugins=<plugin>` | Skip loading specific plugin |
| `--debug` | Show debug output |
| `--user=<id\|login>` | Run command as specific user |

## Finding More Commands

The 12 categories above cover ~90% of daily local dev usage. For everything else:

```bash
# Browse all available commands
wpl help

# Get detailed help for a command group
wpl help plugin
wpl help post

# Get help for a specific subcommand
wpl help plugin install
wpl help post list
```

See [`references/wp-cli-reference.md`](references/wp-cli-reference.md) for a comprehensive reference covering 20+ command groups including core, cron, media, comment, role/cap, config, widget, sidebar, i18n, import/export, and more.

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
