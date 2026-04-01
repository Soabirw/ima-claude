---
name: "wp-ddev"
description: "Run WordPress WP-CLI commands in DDEV environments. Database queries, plugin management, user ops, themes, cache, cron. Zero config from any DDEV project dir. Supply chain isolated package management. Triggers on: ddev wp, ddev setup, ddev import, wp plugin, wp db, wp user, wp option, wp-cli, DDEV."
---

# WordPress WP-DDEV

Execute WP-CLI commands in DDEV WordPress environments. Zero configuration — just be in a DDEV project directory.

## Quick Start

**Prerequisites**: Docker + DDEV v1.25+ installed.

```bash
# Start your DDEV project
ddev start

# Run WP-CLI commands directly
ddev wp plugin list
ddev wp user list
ddev wp db query "SELECT * FROM wp_posts LIMIT 5"

# View project info (URLs, ports, credentials)
ddev describe
```

## How It Works

1. DDEV auto-detects `.ddev/config.yaml` in project directory
2. WP-CLI runs inside the web container with correct PHP, MySQL, and WordPress paths
3. No environment pollution — host session stays clean
4. No UUIDs, no socket paths, no wrapper scripts

## Common Commands

### Database Operations
`ddev wp db query <sql>` · `ddev wp db export [file]` · `ddev wp db import <file>` · `ddev wp search-replace <old> <new>`
```bash
ddev wp db query "SELECT * FROM wp_users"
ddev wp db export dump.sql
ddev wp db import dump.sql
ddev wp search-replace 'old.com' 'new.com' --dry-run
ddev wp search-replace 'old.com' 'new.com' --all-tables
```

### Plugin Management
`ddev wp plugin list` · `ddev wp plugin activate <plugin>` · `ddev wp plugin deactivate <plugin>` · `ddev wp plugin install <plugin> [--activate]`
```bash
ddev wp plugin list
ddev wp plugin list --status=active --format=json
ddev wp plugin activate my-plugin
ddev wp plugin deactivate my-plugin
ddev wp plugin install contact-form-7 --activate
ddev wp plugin is-installed woocommerce && echo "yes"
```

### User Operations
`ddev wp user list` · `ddev wp user create <login> <email> [--role=<role>]` · `ddev wp user update <user> [--field=value]`
```bash
ddev wp user list
ddev wp user list --role=administrator --format=table
ddev wp user create testuser test@example.com --role=editor
ddev wp user update 1 --display_name="Admin User"
ddev wp user add-role 2 editor
```

### Theme Operations
`ddev wp theme list` · `ddev wp theme activate <theme>` · `ddev wp theme status <theme>`
```bash
ddev wp theme list
ddev wp theme activate twentytwentyfour
ddev wp theme status flavor
```

### Cache & Transients
`ddev wp cache flush` · `ddev wp transient delete --all` · `ddev wp transient get <key>`
```bash
ddev wp cache flush
ddev wp transient delete --all
ddev wp transient get my_transient_key
ddev wp transient list --format=table
```

### Options
`ddev wp option get <key>` · `ddev wp option update <key> <value>` · `ddev wp option list [--search=<pattern>]`
```bash
ddev wp option get siteurl
ddev wp option update blogname "New Site Name"
ddev wp option list --search="woocommerce_*" --format=table
ddev wp option delete my_old_option
```

### Post & Content
`ddev wp post list [--post_type=<type>]` · `ddev wp post create` · `ddev wp post update <id>` · `ddev wp post delete <id>`
```bash
ddev wp post list --post_type=page --format=table
ddev wp post list --post_status=draft --fields=ID,post_title
ddev wp post create --post_type=post --post_title="Test" --post_status=publish
ddev wp post update 42 --post_title="Updated Title"
ddev wp post delete 42 --force
ddev wp post meta get 42 _thumbnail_id
ddev wp post meta update 42 custom_field "new value"
```

### Taxonomy & Terms
`ddev wp term list <taxonomy>` · `ddev wp term create <taxonomy> <term>` · `ddev wp term update <taxonomy> <term-id>`
```bash
ddev wp term list category --format=table
ddev wp term create category "New Category" --slug=new-category
ddev wp term update category 5 --name="Renamed"
ddev wp term delete category 5
```

### Menu
`ddev wp menu list` · `ddev wp menu item list <menu>` · `ddev wp menu item add-post <menu> <post-id>`
```bash
ddev wp menu list --format=table
ddev wp menu item list primary-menu
ddev wp menu item add-post primary-menu 42
ddev wp menu item add-custom primary-menu "Link" https://example.com
```

### Rewrite Rules
`ddev wp rewrite flush` · `ddev wp rewrite list` · `ddev wp rewrite structure <structure>`
```bash
ddev wp rewrite flush
ddev wp rewrite list --format=csv
ddev wp rewrite structure '/%postname%/'
```

### Scaffold
`ddev wp scaffold plugin <slug>` · `ddev wp scaffold child-theme <slug>` · `ddev wp scaffold post-type <slug>`
```bash
ddev wp scaffold plugin my-plugin --plugin_name="My Plugin"
ddev wp scaffold post-type product --plugin=my-plugin
ddev wp scaffold taxonomy genre --post_types=product --plugin=my-plugin
ddev wp scaffold child-theme flavor-child --parent_theme=flavor
```

### Eval & Shell
`ddev wp eval <code>` · `ddev wp eval-file <file>`
```bash
ddev wp eval "echo home_url();"
ddev wp eval "var_dump(wp_get_current_user());"
ddev wp eval "echo get_option('active_plugins') | print_r;"
ddev wp eval-file test-script.php
```

## DDEV Project Commands

```bash
# Lifecycle
ddev start            # Start containers
ddev stop             # Stop (preserves database)
ddev restart          # Restart after config changes

# Information
ddev describe         # URLs, ports, DB credentials, PHP version
ddev list             # All DDEV projects on this machine

# Shell & Exec
ddev ssh              # Interactive shell in web container
ddev exec ls -la      # Run any command in web container

# Logs
ddev logs             # Web server logs
ddev logs -s db       # Database server logs

# Launch
ddev launch           # Open site in browser
ddev launch wp-admin/ # Open WP admin
```

## IMA Addon Commands

Commands provided by the `ima-ddev-wordpress` addon:

```bash
# First-time bootstrap (idempotent — safe to re-run)
ddev setup

# Import wp-content assets from WPE site archive
ddev import-assets ~/path/to/extracted-archive

# Import database dump
ddev import-db --file=~/path/to/dump.sql

# Update the addon
ddev add-on update ima-ddev-wordpress
```

## Supply Chain Security

Always use `ddev npm`, `ddev composer` instead of bare host commands. Container isolation prevents compromised dependencies from accessing host SSH keys, env vars, and other projects.

| Instead of | Use | Why |
|---|---|---|
| `npm install` | `ddev npm install` | Container-isolated |
| `composer install` | `ddev composer install` | Container-isolated |
| `npm run composer:dev` | `ddev npm run composer:dev` | Container-isolated |

**Exception:** `npm run deploy` stays on host — needs SSH access for WP Engine push.

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

The 12 categories above cover ~90% of daily dev usage. For everything else:

```bash
ddev wp help
ddev wp help plugin
ddev wp help post list
```

See [`references/wp-cli-reference.md`](references/wp-cli-reference.md) for a comprehensive reference and [`references/ddev-commands.md`](references/ddev-commands.md) for DDEV-specific commands.

## Daily Workflow

```bash
# Start your day
ddev start

# Develop — code changes auto-reflected via bind mounts
# Test
ddev wp plugin activate my-plugin
ddev wp cache flush
ddev launch

# Stop when done
ddev stop
```

## Integration

**With php-fp-wordpress**: Test plugins during development, verify security functions, check database operations.

**With js-fp-wordpress**: Test script enqueuing, verify AJAX endpoints, check jQuery availability.

```bash
# Develop plugin with php-fp-wordpress patterns, test with DDEV
ddev wp plugin activate my-new-plugin
ddev wp eval "var_dump(current_user_can('edit_posts'));"
```

## Quality Gates

Before running destructive commands:
- ✅ Correct project: `ddev describe` to verify you're in the right DDEV project
- ✅ Backup if needed: `ddev export-db --file=backup.sql.gz` for database modifications
- ✅ Containers running: `ddev start` (DDEV will tell you if already running)
