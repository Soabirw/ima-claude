---
name: discourse-admin
description: "Discourse admin API for site settings, configuration export/import, categories, groups, and custom user fields. Use when: managing Discourse site configuration, deploying config to staging/production, exporting settings, bulk-updating site settings, managing groups or user fields via API. Triggers on: discourse admin, discourse settings, discourse config, site settings, config-as-code, discourse deploy, discourse staging."
---

# Discourse Admin API

Manage Discourse site configuration programmatically via the REST API. Export settings, apply environment configs, manage groups and user fields — without clicking through the admin UI.

## When to Use This Skill

- Exporting or importing Discourse site settings
- Deploying configuration to staging or production environments
- Bulk-updating site settings via API
- Managing groups, categories, or custom user fields programmatically
- Config-as-code workflows for Discourse

**Not this skill**: For Discourse *plugin development* (Ruby/Rails/Ember), use the `discourse` skill instead.

## Quick Start

**Prerequisites**: Configure environments in `~/.claude/discourse-environments.json`:
```json
{
  "local": {
    "url": "http://localhost:4200",
    "api_key": "your-local-api-key",
    "api_username": "system"
  },
  "staging": {
    "url": "https://staging.community.example.com",
    "api_key": "staging-key",
    "api_username": "system"
  }
}
```

**Run commands**:
```bash
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py export
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py import base.json staging-overlay.json
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py diff config.json
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py get title
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py set disable_emails yes
python3 ~/.claude/skills/discourse-admin/scripts/discourse-admin.py envs
```

## Environment Resolution

Resolved via priority chain (same pattern as `wp-local`):

1. `--env` flag on command line
2. `$DISCOURSE_ENV` environment variable
3. `.discourse-env` file in project root or parents
4. Falls back to `"local"`

```bash
# Explicit env
python3 discourse-admin.py --env staging export

# Env var (set in Kitty terminal config)
export DISCOURSE_ENV=staging
python3 discourse-admin.py export

# Project file
echo "staging" > .discourse-env
python3 discourse-admin.py export
```

**Credentials** stored in `~/.claude/discourse-environments.json` (not in repo, not in env vars).
API keys are managed at `/admin/api/keys` in each Discourse instance.

## Config-as-Code Workflow

### Step 1: Export Non-Default Settings

```bash
python3 discourse-admin.py export discourse-base.json
```

Exports only settings where value differs from default — typically 50-100 settings, not 500+.

### Step 2: Create Environment Overlays

```
config/
  discourse-base.json          # Non-default settings from local
  discourse-staging.json       # Staging overrides
  discourse-production.json    # Production overrides
```

**Staging overlay example** (`discourse-staging.json`):
```json
{
  "title": "[STAGING] Community Forum",
  "site_description": "Staging environment — do not use for real discussions",
  "disable_emails": "yes",
  "notification_email": "noreply-staging@example.com",
  "discourse_connect_provider_secrets": "staging.example.com|staging-secret-here"
}
```

### Step 3: Preview Changes (Dry Run)

```bash
# Show what would change
python3 discourse-admin.py --env staging import base.json staging.json --dry-run

# Compare remote vs desired
python3 discourse-admin.py --env staging diff base.json
```

### Step 4: Apply Config

```bash
python3 discourse-admin.py --env staging import discourse-base.json discourse-staging.json
```

Uses bulk_update endpoint (single request). Falls back to individual updates if bulk fails.

## Site Settings API

The primary endpoint for config-as-code. ~500+ settings covering email, SSO, branding, security, etc.

### Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/admin/site_settings.json` | List all settings |
| GET | `/admin/site_settings/category/{slug}.json` | Filter by category |
| PUT | `/admin/site_settings/{name}.json` | Update single setting |
| PUT | `/admin/site_settings/bulk_update.json` | Update multiple (undocumented, source-verified) |

**Setting categories:** `required`, `basic`, `users`, `email`, `login`, `security`, `onboarding`, `spam`, `rate_limits`, `developer`, `embedding`, `legal`, `branding`, `uncategorized`

## When to Load Reference Files

### Full API Reference
**File**: `references/api-endpoints.md`
**Load when**: You need exact parameters, response formats, or edge cases for any admin endpoint (groups, categories, users, user fields, site texts, API keys).

### Known Gotchas
**File**: `references/gotchas.md`
**Load when**: Hitting unexpected behavior, 404s, or working with a specific Discourse version. Contains breaking changes across versions and endpoint migration history.

### Staging Defaults
**File**: `references/staging-defaults.md`
**Load when**: Setting up a new staging environment. Contains recommended safe defaults and a pre-deploy checklist.

## Common Staging Settings

| Setting | Staging Value | Why |
|---------|--------------|-----|
| `disable_emails` | `yes` | Prevent sending real emails |
| `title` | `[STAGING] ...` | Visual distinction |
| `notification_email` | staging address | Don't spam real inbox |
| `discourse_connect_provider_secrets` | staging domains | SSO only for staging WP sites |
| `enable_local_logins` | `true` | Allow direct login for testing |
| `min_password_length` | `6` | Easier test accounts |
| `invite_only` | `true` | Prevent public signups |

## Rate Limiting

- Admin API rate limits are site-setting driven (not hardcoded)
- Two independent limiters: IP-based (`max_reqs_per_ip_mode`) and API-key-based (`max_admin_api_reqs_per_minute`, default 60)
- max=0 means BLOCK ALL (not unlimited) — use high numbers like 6000
- Must flush Redis rate limit keys after changing rate limit config

## Quick Reference (Manual curl)

```bash
# List all settings
curl -s -H "Api-Key: $KEY" -H "Api-Username: system" "$URL/admin/site_settings.json"

# Get email settings only
curl -s -H "Api-Key: $KEY" -H "Api-Username: system" "$URL/admin/site_settings/category/email.json"

# Update a single setting
curl -s -X PUT -H "Api-Key: $KEY" -H "Api-Username: system" \
  -H "Content-Type: application/json" \
  -d '{"disable_emails": "yes"}' \
  "$URL/admin/site_settings/disable_emails.json"

# List groups
curl -s -H "Api-Key: $KEY" -H "Api-Username: system" "$URL/groups.json"

# List custom user fields
curl -s -H "Api-Key: $KEY" -H "Api-Username: system" "$URL/admin/config/user_fields.json"

# List categories
curl -s -H "Api-Key: $KEY" -H "Api-Username: system" "$URL/categories.json"
```
