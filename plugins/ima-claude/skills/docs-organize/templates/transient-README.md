# Transient Documentation

Ephemeral local-only documents for active planning and investigation.

**⚠️ Files here are git-ignored and will NOT be committed.**

## Purpose

Use transient/ for:
- **Phase planning** before implementation starts
- **Investigation logs** during debugging
- **Spike results** from technical exploration
- **Collaborative notes** during pairing sessions
- **Temporary checklists** for one-time tasks

## Organization Suggestions

```
transient/
├── planning/              # Upcoming phase/feature planning
├── investigations/        # Debug sessions, root cause analysis
├── spikes/               # Technical explorations, POCs
└── notes/                # Miscellaneous working notes
```

## Workflow

### Creating Transient Docs
1. Create file in appropriate subfolder
2. Include date in filename: `YYYY-MM-DD-topic.md`
3. Work locally, iterate freely

### Moving to Active
When a transient doc becomes stable:
1. Clean up content for permanence
2. Move to appropriate `active/` section
3. Delete original transient file
4. Update navigation links

### Cleanup
- Review transient/ monthly
- Delete completed investigation logs
- Archive useful findings to `active/` or `archive/`

## Example: Investigation Log

```markdown
# 2025-01-20 - API Performance Investigation

## Symptoms
- API response times >2s on listing endpoint
- Database queries showing N+1 pattern

## Investigation Steps
1. Added timing logs to endpoint
2. Identified 47 individual queries per request
3. Found missing `update_meta_cache()` call

## Resolution
- Added batch meta loading
- Response time reduced to 150ms

## Outcome
→ Move findings to `active/operations/TROUBLESHOOTING.md`
→ Delete this investigation log
```

## Git Behavior

This folder contains a `.gitignore` that excludes all `*.md` files.

**To force-add a file** (rare, for intentional commits):
```bash
git add -f docs/transient/important-file.md
```

---

**Last Updated**: YYYY-MM-DD
