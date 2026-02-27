# Migration Guide: Legacy → Plugin System

## What Changed

Prior to v2.0.0, ima-claude installed files directly into `~/.claude/` — skills, hooks, rules, and personalities were copied there and managed by a Bun install script.

Starting with v2.0.0, ima-claude is a **Claude Code native plugin**. Nothing is copied to `~/.claude/`. The plugin lives in its own directory (wherever you cloned the repo or wherever Claude Code stores installed plugins) and is loaded by Claude Code's plugin system at startup.

**Why it's better:**
- `git pull` + `/plugin marketplace update` to upgrade — no install script, no file conflicts
- Namespaced skills (`/ima-claude:task-master`) prevent collisions with other plugins
- Hooks are declared in `hooks.json` inside the plugin — no manual `settings.json` surgery
- Clean uninstall — remove the plugin, nothing left behind in `~/.claude/`

---

## Option A: Migrate to the Plugin (Recommended)

### Step 1: Preview what will be removed

```bash
git clone https://gitea.theflccc.org/IMA/ima-claude.git
cd ima-claude
bun run scripts/migrate-to-plugin.ts --dry-run
```

This shows every file that will be removed from `~/.claude/` without touching anything.

### Step 2: Remove legacy artifacts

```bash
bun run scripts/migrate-to-plugin.ts
```

Removes:
- All ima-claude skills from `~/.claude/skills/`
- All ima-claude hooks from `~/.claude/hooks/`
- ima-claude rules from `~/.claude/rules/`
- ima-claude personalities from `~/.claude/personalities/`
- ima-claude hook entries from `~/.claude/settings.json`
- `~/.claude/IMA_CLAUDE_INIT.md`

Your own custom skills, other plugins' hooks, and personal settings are untouched.

### Step 3: Install the plugin

Inside Claude Code:

```
/plugin install https://gitea.theflccc.org/IMA/ima-claude
```

### Step 4: Verify

```
/ima-claude:quickstart
```

If you see the cheat sheet, everything is working.

---

## Option B: Stay on Legacy

The last legacy release is tagged `v1.21.0-legacy`. It will not receive further updates, but it works exactly as it always did.

```bash
git clone https://gitea.theflccc.org/IMA/ima-claude.git
cd ima-claude
git checkout v1.21.0-legacy
bun run scripts/install.ts
```

To upgrade to the plugin later, follow Option A from that point.

---

## What Changes After Migration

### Skill invocation

| Before | After |
|--------|-------|
| `/task-master` | `/ima-claude:task-master` |
| `/quickstart` | `/ima-claude:quickstart` |
| `/save-session` | `/ima-claude:save-session` |
| (all skills) | prefix with `ima-claude:` |

Skills still auto-activate on context — the namespace only matters when you invoke them explicitly with `/`.

### Hook behavior

Hooks behave identically. The difference is where they live and how they're registered:

- **Legacy**: hook files in `~/.claude/hooks/`, entries manually merged into `~/.claude/settings.json`
- **Plugin**: hook files live inside the plugin, registered automatically via `hooks.json`

If you customized any hook scripts in `~/.claude/hooks/`, note those changes before running the migration script — they will be removed.

### Update workflow

| Before | After |
|--------|-------|
| `git pull && bun run scripts/install.ts` | `/plugin marketplace update` |

### Memory state

Nothing changes. Vestige, Qdrant, and Serena memories are stored outside ima-claude and are unaffected by the migration.

---

## Troubleshooting

**Skills not loading after migration**

Run `/ima-claude:quickstart` — if it doesn't respond, the plugin may not be enabled. Check:
```
/plugin list
```

**Hook warnings missing**

Hooks are loaded from the plugin's `hooks.json`. If you're not seeing expected warnings, confirm the plugin is enabled and restart Claude Code.

**Old `/task-master` (without namespace) not found**

The legacy unnamespaced skills are gone once you remove the legacy install. Update any scripts or habits to use `/ima-claude:task-master`.

**Settings.json still has old hook entries**

Run `bun run scripts/migrate-to-plugin.ts` again — it's idempotent and will clean any remaining entries.
