---
name: mcp-gitea
description: >-
  Gitea internal Git repository management — pull requests, issues, releases, branches,
  tags, wikis, and CI/CD actions via MCP server or tea CLI fallback. Use when: creating/
  reviewing PRs, managing issues, creating releases/tags, browsing repo contents, managing
  branches, wiki operations, or any Gitea-hosted repository operation. Triggers on: Gitea,
  internal repo, pull request, PR review, merge request, release, tag, branch, issue,
  milestone, wiki, actions, CI/CD, timetracking. NOT for GitHub repos — use mcp-github.
---

# Gitea - Internal Git Repository Management

Team's internal Git platform. Two integration approaches available — check MCP availability first.

- Gitea = primary for daily work (PRs, issues, releases)
- GitHub = FOSS publishing only → use `mcp-github`
- `gh` CLI = GitHub-only, does not work with Gitea

## Integration Approach: MCP vs tea CLI

**Check which is available before acting:**

```
MCP configured? → verify: mcp__gitea__get_me works without error
  → Yes: use mcp__gitea__* tools (structured, rich responses)
  → No:  use tea CLI via Bash (zero-setup if tea is already configured)
```

| | MCP Server | tea CLI |
|---|---|---|
| **Setup** | Install binary + configure settings.json | `tea login add` (one-time) |
| **Output** | Structured JSON | Text (parse with jq/grep if needed) |
| **Coverage** | Full API surface | Common ops (PR, issue, release, repo) |
| **Best for** | Agentic workflows, rich data reads | Quick ops, scripting, no MCP configured |

## Setup

### Option A — Gitea MCP Server

Install the [official Gitea MCP server](https://gitea.com/gitea/gitea-mcp), then add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "gitea": {
      "command": "gitea-mcp",
      "env": {
        "GITEA_URL": "https://your-gitea-instance",
        "GITEA_TOKEN": "your-token"
      }
    }
  }
}
```

Verify: `mcp__gitea__get_me` returns your user profile.

### Option B — tea CLI

```bash
# Check if configured
tea login list

# Add login if not configured
tea login add --url https://your-gitea-instance --token your-token

# Verify
tea repos list
```

---

## tea CLI Reference

Use when MCP is not configured. All commands run via Bash tool.

### Pull Requests

```bash
# List PRs
tea pr list --repo owner/repo --state open

# Create PR (after git push)
tea pr create --repo owner/repo \
  --title "feat: description" \
  --body "## Summary\n- what changed" \
  --head feature/branch --base main

# View PR
tea pr view <index> --repo owner/repo

# Review PR
tea pr review <index> --repo owner/repo --approve --comment "LGTM"
tea pr review <index> --repo owner/repo --reject --comment "See comments"

# Merge PR
tea pr merge <index> --repo owner/repo --style squash --delete-branch

# Add reviewers
tea pr edit <index> --repo owner/repo --reviewer username
```

### Issues

```bash
# List issues
tea issue list --repo owner/repo --state open

# Create issue
tea issue create --repo owner/repo \
  --title "Bug: description" \
  --body "## Steps\n1. ...\n\n## Expected\n...\n\n## Actual\n..."

# Comment on issue
tea comment create <index> --repo owner/repo --body "comment text"

# Close issue
tea issue close <index> --repo owner/repo
```

### Releases & Tags

```bash
# List releases
tea releases list --repo owner/repo

# Create release (tag must exist or will be created)
tea releases create --repo owner/repo \
  --tag v2.1.0 --title "v2.1.0 — Feature Name" \
  --note "## Changes\n- ...\n\n## Breaking Changes\n- none"

# List tags
tea tag list --repo owner/repo
```

### Repos & Branches

```bash
# List repos
tea repos list --owner org-name

# List branches
tea branch list --repo owner/repo

# Create branch (use git directly — tea doesn't wrap branch creation)
git checkout -b feature/branch && git push -u origin feature/branch
```

### Shorthand: omit `--repo` when inside a cloned repo

```bash
cd ~/projects/my-repo   # git remote must point to Gitea
tea pr list             # auto-detects owner/repo from remote
tea issue list --state open
```

---

## MCP Tool Catalog

*Use these when `mcp__gitea__get_me` succeeds.*

**Method-dispatch:** `pull_request_read`, `pull_request_write`, `pull_request_review_write`, `issue_read`, `issue_write` require a `method` param — omitting it causes a missing parameter error.

### Identity & Discovery

| Tool | Purpose | Key Params |
|------|---------|------------|
| `get_me` | Current authenticated user | *(none)* |
| `get_user_orgs` | User's organizations | *(none)* |
| `search_users` | Search users by name/email | `query` |
| `search_repos` | Search repositories | `query`, `owner` |
| `search_org_teams` | Find teams within an org | `org`, `query` |
| `list_my_repos` | List authenticated user's repos | `page`, `perPage` |
| `get_gitea_mcp_server_version` | Server version info | *(none)* |

### Repository Operations

| Tool | Purpose | Key Params |
|------|---------|------------|
| `create_repo` | Create repository | `owner`, `name`, `description`, `private` |
| `fork_repo` | Fork repository | `owner`, `repo`, `organization` |
| `get_file_contents` | Get file at path | `owner`, `repo`, `filepath`, `ref` |
| `get_dir_contents` | List directory | `owner`, `repo`, `filepath`, `ref` |
| `create_or_update_file` | Create or update file | `owner`, `repo`, `filepath`, `content`, `message`, `sha` (required for updates) |
| `delete_file` | Delete file | `owner`, `repo`, `filepath`, `message`, `sha` |

### Branches

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_branches` | List all branches | `owner`, `repo`, `page`, `perPage` |
| `create_branch` | Create branch | `owner`, `repo`, `new_branch_name`, `old_branch_name` |
| `delete_branch` | Delete branch | `owner`, `repo`, `branch` |

### Pull Requests

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_pull_requests` | List PRs with filtering | `owner`, `repo`, `state` (open/closed/all), `sort`, `milestone`, `page`, `perPage` |
| `pull_request_read` | Read PR data and reviews | `method` (get/get_diff/get_reviews/get_review/get_review_comments), `owner`, `repo`, `index`; `review_id` for get_review/get_review_comments |
| `pull_request_write` | Create, update, merge PR; manage reviewers | `method` (create/update/merge/add_reviewers/remove_reviewers), `owner`, `repo`; `index` required except for create |
| `pull_request_review_write` | Submit, delete, or dismiss review | `method` (create/submit/delete/dismiss), `owner`, `repo`, `index`; `review_id` required for submit/delete/dismiss |

**`pull_request_write` methods:**
- `create`: `title` (req), `head` (req), `base` (req), `body`
- `update`: `index` (req), `title`, `body`, `state`, `assignee`, `assignees`, `milestone`, `base`, `allow_maintainer_edit`
- `merge`: `index` (req), `merge_style` (merge/rebase/rebase-merge/squash/fast-forward-only), `message`, `delete_branch`, `title`
- `add_reviewers` / `remove_reviewers`: `index` (req), `reviewers` (string[]), `team_reviewers` (string[])

**`pull_request_review_write` methods:**
- `create`: `body`, `commit_id`, `comments` (inline array with `path`, `body`, `old_line_num`, `new_line_num`), `state`
- `submit`: `review_id` (req), `body`, `state` (APPROVED/REQUEST_CHANGES/COMMENT/PENDING)
- `delete`: `review_id` (req)
- `dismiss`: `review_id` (req), `message`

### Issues

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_issues` | List issues with filtering | `owner`, `repo`, `state` (default "all"), `page`, `perPage` |
| `issue_read` | Get issue details, comments, or labels | `method` (get/get_comments/get_labels), `owner`, `repo`, `index` |
| `issue_write` | Create, update, comment, manage labels | `method` (create/update/add_comment/edit_comment/add_labels/remove_label/replace_labels/clear_labels), `owner`, `repo`; `index` required except for create |

**`issue_write` methods:**
- `create`: `title` (req), `body`, `assignees`, `labels` (number[]), `milestone`
- `update`: `index` (req), `title`, `body`, `state`, `assignees`, `milestone`
- `add_comment`: `index` (req), `body` (req)
- `edit_comment`: `index` (req), `commentID` (req), `body` (req)
- `add_labels` / `replace_labels`: `index` (req), `labels` (number[])
- `remove_label`: `index` (req), `label_id` (number)
- `clear_labels`: `index` (req)

### Labels

| Tool | Purpose | Key Params |
|------|---------|------------|
| `label_read` | Get label details | `owner`, `repo`, `id` |
| `label_write` | Create or update label | `owner`, `repo`, `name`, `color` |

### Milestones

| Tool | Purpose | Key Params |
|------|---------|------------|
| `milestone_read` | Get milestone details | `owner`, `repo`, `id` |
| `milestone_write` | Create or update milestone | `owner`, `repo`, `title`, `due_on`, `description` |

### Releases & Tags

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_releases` | List all releases | `owner`, `repo`, `page`, `perPage` |
| `get_release` | Get release by ID | `owner`, `repo`, `id` |
| `get_latest_release` | Get latest published release | `owner`, `repo` |
| `create_release` | Create release | `owner`, `repo`, `tag_name`, `name`, `body`, `draft`, `prerelease` |
| `delete_release` | Delete release | `owner`, `repo`, `id` |
| `list_tags` | List all tags | `owner`, `repo`, `page`, `perPage` |
| `get_tag` | Get tag by name | `owner`, `repo`, `tag` |
| `create_tag` | Create tag | `owner`, `repo`, `tag_name`, `message`, `target` |
| `delete_tag` | Delete tag | `owner`, `repo`, `tag` |

### Commits

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_commits` | List commits on branch | `owner`, `repo`, `sha`, `path`, `page`, `perPage` |

### Wiki

| Tool | Purpose | Key Params |
|------|---------|------------|
| `wiki_read` | Read wiki page | `owner`, `repo`, `pageName` |
| `wiki_write` | Create or update wiki page | `owner`, `repo`, `pageName`, `content`, `message` |

### CI/CD Actions

| Tool | Purpose | Key Params |
|------|---------|------------|
| `actions_config_read` | Read workflow/actions config | `owner`, `repo` |
| `actions_config_write` | Write workflow/actions config | `owner`, `repo`, `config` |
| `actions_run_read` | Read action run details/logs | `owner`, `repo`, `run_id` |
| `actions_run_write` | Trigger or manage action runs | `owner`, `repo`, `workflow_id`, `ref` |

### Time Tracking

| Tool | Purpose | Key Params |
|------|---------|------------|
| `timetracking_read` | Read time entries on issue | `owner`, `repo`, `index` |
| `timetracking_write` | Log time on issue | `owner`, `repo`, `index`, `time` (seconds) |

## Common Workflows

### Create a Pull Request

```
git push origin feature/my-branch

pull_request_write(
  method: "create",
  owner: "FLCCC", repo: "my-repo",
  title: "feat: add new feature",
  body: "## Summary\n- What changed\n\n## Test plan\n- [ ] Tested locally",
  head: "feature/my-branch", base: "main"
)
```

### Review a Pull Request

```
pull_request_read(method: "get", owner: "FLCCC", repo: "my-repo", index: 42)
pull_request_read(method: "get_reviews", owner: "FLCCC", repo: "my-repo", index: 42)

pull_request_review_write(
  method: "create",
  owner: "FLCCC", repo: "my-repo", index: 42,
  state: "APPROVED", body: "LGTM — clean implementation"
)
pull_request_review_write(
  method: "submit",
  owner: "FLCCC", repo: "my-repo", index: 42,
  review_id: <id from create>, state: "APPROVED"
)
```

### Merge a Pull Request

```
pull_request_write(
  method: "merge",
  owner: "FLCCC", repo: "my-repo", index: 42,
  merge_style: "squash", delete_branch: true
)
```

### Create a Release

```
get_latest_release(owner: "FLCCC", repo: "my-repo")

create_tag(owner: "FLCCC", repo: "my-repo", tag_name: "v2.1.0", message: "Release v2.1.0", target: "main")

create_release(
  owner: "FLCCC", repo: "my-repo",
  tag_name: "v2.1.0", name: "v2.1.0 — Feature Name",
  body: "## Changes\n- ...\n\n## Breaking Changes\n- none",
  draft: false, prerelease: false
)
```

### Manage Issues

```
issue_write(method: "create", owner: "FLCCC", repo: "my-repo",
  title: "Bug: description", body: "## Steps\n1. ...\n\n## Expected\n...\n\n## Actual\n...")

issue_write(method: "add_comment", owner: "FLCCC", repo: "my-repo", index: 15,
  body: "Confirmed — reproduced on v2.9.1.")

list_issues(owner: "FLCCC", repo: "my-repo", state: "open", perPage: 20)
```

### Browse Repo Contents

```
get_dir_contents(owner: "FLCCC", repo: "my-repo", filepath: "src/", ref: "main")
get_file_contents(owner: "FLCCC", repo: "my-repo", filepath: "package.json", ref: "main")
```

## Decision Logic

```
Gitea-hosted repo? (git remote -v shows gitea.* or internal hostname)
  → No, github.com: mcp__github__* or gh CLI
  → Local git ops (commit, diff, log, stash, rebase, push, pull): git CLI directly
  → Yes, Gitea:
      MCP configured? (mcp__gitea__get_me succeeds)
        → Yes: use mcp__gitea__* tools below
        → No:  use tea CLI via Bash (see tea CLI Reference above)

Operation → MCP tool → tea CLI equivalent
  Creating PR           → pull_request_write(method: "create")       → tea pr create
  Reading PR/diff       → pull_request_read(method: "get|get_diff")  → tea pr view <n>
  Reviewing PR          → pull_request_review_write(create→submit)   → tea pr review <n>
  Merging PR            → pull_request_write(method: "merge")        → tea pr merge <n>
  Issue triage          → issue_write / list_issues                  → tea issue list
  Adding comment        → issue_write(method: "add_comment")         → tea comment create
  Cutting release       → create_tag → create_release                → tea releases create
  Browsing files        → get_file_contents / get_dir_contents       → tea repo list / git show
  Editing file via MCP  → create_or_update_file (need sha first)     → Edit tool + git commit
  Branch management     → create_branch / delete_branch              → git checkout -b / git push
  CI/CD status          → actions_run_read                           → (no tea equivalent — check Gitea UI)
  Team docs             → wiki_write / wiki_read                     → (no tea equivalent)
  Time logging          → timetracking_write                         → (no tea equivalent)
```

## Token-Saving Strategies

- **Paginate:** set `perPage` to what you need — defaults can return 30+ items
- **Filter state:** `state: "open"` on PRs/issues; skip closed unless historical review
- **Target refs:** always pass `ref: "main"` to avoid ambiguity; use `perPage: 10` on commits
- **Cache in session:** owner/org names, repo names, label IDs, milestone IDs — these don't change
- **Read before file write:** `create_or_update_file` requires current `sha` — call `get_file_contents` first or get a 409 conflict

## When NOT to Use Gitea MCP

| Situation | Use Instead |
|-----------|-------------|
| MCP not configured | `tea` CLI via Bash (see tea CLI Reference above) |
| GitHub-hosted repo (github.com) | `mcp__github__*` or `gh` CLI |
| Local git operations (commit, diff, stash, rebase, cherry-pick) | `git` CLI |
| Pushing/pulling code | `git push` / `git pull` |
| GitHub Actions (github.com CI) | `gh` CLI |
| Cloning a repo | `git clone` |
