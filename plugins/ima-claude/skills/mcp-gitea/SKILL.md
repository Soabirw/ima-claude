---
name: mcp-gitea
description: >-
  Gitea MCP for internal Git repository management — pull requests, issues, releases,
  branches, tags, wikis, and CI/CD actions. Use when: creating/reviewing PRs, managing
  issues, creating releases/tags, browsing repo contents, managing branches, wiki
  operations, or any Gitea-hosted repository operation. Triggers on: Gitea, internal
  repo, pull request, PR review, merge request, release, tag, branch, issue, milestone,
  wiki, actions, CI/CD, timetracking. NOT for GitHub repos — use mcp-github for those.
---

# Gitea MCP - Internal Git Repository Management

The team's internal Git platform. All tools prefixed `mcp__gitea__`.

Gitea is the **primary** tool for daily development work (PRs, issues, releases).
GitHub is FOSS publishing only — use `mcp-github` for GitHub operations.
The `gh` CLI is GitHub-only; it does not work with Gitea.

**Method-dispatch pattern:** Several tools (`pull_request_read`, `pull_request_write`, `pull_request_review_write`, `issue_read`, `issue_write`) use a required `method` parameter to select the operation. Always include `method` — omitting it causes a missing parameter error.

## Tool Catalog

### Identity & Discovery

| Tool | Purpose | Key Params |
|------|---------|------------|
| `get_me` | Current authenticated user | *(none)* |
| `get_user_orgs` | User's organizations | *(none)* |
| `search_users` | Search users by name/email | `query` |
| `search_repos` | Search repositories across Gitea | `query`, `owner` |
| `search_org_teams` | Find teams within an org | `org`, `query` |
| `list_my_repos` | List authenticated user's repos | `page`, `perPage` |
| `get_gitea_mcp_server_version` | Server version info | *(none)* |

### Repository Operations

| Tool | Purpose | Key Params |
|------|---------|------------|
| `create_repo` | Create a new repository | `owner`, `name`, `description`, `private` |
| `fork_repo` | Fork an existing repository | `owner`, `repo`, `organization` |
| `get_file_contents` | Get file contents at a path | `owner`, `repo`, `filepath`, `ref` |
| `get_dir_contents` | List directory contents | `owner`, `repo`, `filepath`, `ref` |
| `create_or_update_file` | Create or update a file | `owner`, `repo`, `filepath`, `content`, `message`, `sha` (required for updates) |
| `delete_file` | Delete a file | `owner`, `repo`, `filepath`, `message`, `sha` |

### Branches

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_branches` | List all branches | `owner`, `repo`, `page`, `perPage` |
| `create_branch` | Create a new branch | `owner`, `repo`, `new_branch_name`, `old_branch_name` |
| `delete_branch` | Delete a branch | `owner`, `repo`, `branch` |

### Pull Requests

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_pull_requests` | List PRs with filtering | `owner`, `repo`, `state` (open/closed/all), `sort`, `milestone`, `page`, `perPage` |
| `pull_request_read` | Read PR data and reviews | `method` (get/get_diff/get_reviews/get_review/get_review_comments), `owner`, `repo`, `index`; `review_id` for get_review/get_review_comments |
| `pull_request_write` | Create, update, merge PR; manage reviewers | `method` (create/update/merge/add_reviewers/remove_reviewers), `owner`, `repo`; `index` required except for create |
| `pull_request_review_write` | Submit, delete, or dismiss a PR review | `method` (create/submit/delete/dismiss), `owner`, `repo`, `index`; `review_id` required for submit/delete/dismiss |

**`pull_request_write` method details:**
- `create`: `title` (req), `head` (req), `base` (req), `body`
- `update`: `index` (req), `title`, `body`, `state`, `assignee`, `assignees`, `milestone`, `base`, `allow_maintainer_edit`
- `merge`: `index` (req), `merge_style` (merge/rebase/rebase-merge/squash/fast-forward-only), `message`, `delete_branch`, `title`
- `add_reviewers` / `remove_reviewers`: `index` (req), `reviewers` (string[]), `team_reviewers` (string[])

**`pull_request_review_write` method details:**
- `create`: `body`, `commit_id`, `comments` (inline array with `path`, `body`, `old_line_num`, `new_line_num`), `state`
- `submit`: `review_id` (req), `body`, `state` (APPROVED/REQUEST_CHANGES/COMMENT/PENDING)
- `delete`: `review_id` (req)
- `dismiss`: `review_id` (req), `message`

### Issues

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_issues` | List issues with filtering | `owner`, `repo`, `state` (default "all"), `page`, `perPage` |
| `issue_read` | Get issue details, comments, or labels | `method` (get/get_comments/get_labels), `owner`, `repo`, `index` |
| `issue_write` | Create, update, comment, or manage labels | `method` (create/update/add_comment/edit_comment/add_labels/remove_label/replace_labels/clear_labels), `owner`, `repo`; `index` required except for create |

**`issue_write` method details:**
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
| `label_write` | Create or update a label | `owner`, `repo`, `name`, `color` |

### Milestones

| Tool | Purpose | Key Params |
|------|---------|------------|
| `milestone_read` | Get milestone details | `owner`, `repo`, `id` |
| `milestone_write` | Create or update a milestone | `owner`, `repo`, `title`, `due_on`, `description` |

### Releases & Tags

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_releases` | List all releases | `owner`, `repo`, `page`, `perPage` |
| `get_release` | Get release by ID | `owner`, `repo`, `id` |
| `get_latest_release` | Get the latest published release | `owner`, `repo` |
| `create_release` | Create a new release | `owner`, `repo`, `tag_name`, `name`, `body`, `draft`, `prerelease` |
| `delete_release` | Delete a release | `owner`, `repo`, `id` |
| `list_tags` | List all tags | `owner`, `repo`, `page`, `perPage` |
| `get_tag` | Get tag by name | `owner`, `repo`, `tag` |
| `create_tag` | Create a new tag | `owner`, `repo`, `tag_name`, `message`, `target` |
| `delete_tag` | Delete a tag | `owner`, `repo`, `tag` |

### Commits

| Tool | Purpose | Key Params |
|------|---------|------------|
| `list_commits` | List commits on a branch | `owner`, `repo`, `sha`, `path`, `page`, `perPage` |

### Wiki

| Tool | Purpose | Key Params |
|------|---------|------------|
| `wiki_read` | Read a wiki page | `owner`, `repo`, `pageName` |
| `wiki_write` | Create or update a wiki page | `owner`, `repo`, `pageName`, `content`, `message` |

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
| `timetracking_read` | Read time entries on an issue | `owner`, `repo`, `index` |
| `timetracking_write` | Log time on an issue | `owner`, `repo`, `index`, `time` (seconds) |

## Common Workflows

### Create a Pull Request

```
1. Ensure your feature branch is pushed:
   git push origin feature/my-branch

2. pull_request_write(
     method: "create",
     owner: "FLCCC",
     repo: "my-repo",
     title: "feat: add new feature",
     body: "## Summary\n- What changed\n- Why it changed\n\n## Test plan\n- [ ] Tested locally",
     head: "feature/my-branch",
     base: "main"
   )
```

### Review a Pull Request

```
1. pull_request_read(method: "get", owner: "FLCCC", repo: "my-repo", index: 42)
   → Review title, description, and diff summary

2. pull_request_read(method: "get_reviews", owner: "FLCCC", repo: "my-repo", index: 42)
   → Check existing reviews

3. pull_request_review_write(
     method: "create",
     owner: "FLCCC",
     repo: "my-repo",
     index: 42,
     state: "APPROVED",
     body: "LGTM — clean implementation, tests look solid"
   )
   → Then submit it:
   pull_request_review_write(
     method: "submit",
     owner: "FLCCC",
     repo: "my-repo",
     index: 42,
     review_id: <id from create response>,
     state: "APPROVED"
   )
```

### Merge a Pull Request

```
pull_request_write(
  method: "merge",
  owner: "FLCCC",
  repo: "my-repo",
  index: 42,
  merge_style: "squash",
  delete_branch: true
)
```

### Create a Release

```
1. get_latest_release(owner: "FLCCC", repo: "my-repo")
   → Note current version for bump reference

2. create_tag(
     owner: "FLCCC",
     repo: "my-repo",
     tag_name: "v2.1.0",
     message: "Release v2.1.0",
     target: "main"
   )

3. create_release(
     owner: "FLCCC",
     repo: "my-repo",
     tag_name: "v2.1.0",
     name: "v2.1.0 — Feature Name",
     body: "## Changes\n- ...\n\n## Breaking Changes\n- none",
     draft: false,
     prerelease: false
   )
```

### Manage Issues

```
# Create an issue
issue_write(
  method: "create",
  owner: "FLCCC",
  repo: "my-repo",
  title: "Bug: description of problem",
  body: "## Steps to reproduce\n1. ...\n\n## Expected\n...\n\n## Actual\n..."
)

# Update an existing issue
issue_write(
  method: "update",
  owner: "FLCCC",
  repo: "my-repo",
  index: 15,
  body: "<updated body>"
)

# Add a comment
issue_write(
  method: "add_comment",
  owner: "FLCCC",
  repo: "my-repo",
  index: 15,
  body: "Confirmed — reproduced on v2.9.1."
)

# Filter open issues
list_issues(
  owner: "FLCCC",
  repo: "my-repo",
  state: "open",
  perPage: 20
)
```

### Browse Repo Contents

```
# List files in a directory
get_dir_contents(owner: "FLCCC", repo: "my-repo", filepath: "src/", ref: "main")

# Read a specific file
get_file_contents(owner: "FLCCC", repo: "my-repo", filepath: "package.json", ref: "main")
```

## Decision Logic

```
Is this a Gitea-hosted repo?
(check: git remote -v shows gitea.* or internal hostname)
  → Yes: Use mcp__gitea__* tools  ← PRIMARY for daily work

  → No: Is it GitHub-hosted? (github.com in remote URL)
      → Yes: Use mcp__github__* tools (see mcp-github skill)
             or gh CLI for GitHub-specific operations

For local-only git operations (commit, diff, log, stash, rebase):
  → Always use git CLI directly — no MCP needed for local ops

Operation decision tree:
  Creating a PR                → pull_request_write(method: "create")
  Reading PR details/diff      → pull_request_read(method: "get" | "get_diff")
  Reviewing a PR               → pull_request_review_write(method: "create" then "submit")
  Merging a PR                 → pull_request_write(method: "merge")
  Issue triage/tracking        → issue_write(method: "create" | "update") / list_issues
  Adding a comment             → issue_write(method: "add_comment")
  Cutting a release            → create_tag → create_release
  Browsing file contents       → get_file_contents / get_dir_contents
  Editing a file via MCP       → create_or_update_file (need sha for updates)
  Branch management            → create_branch / delete_branch
  CI/CD pipeline status        → actions_run_read
  Team documentation           → wiki_write / wiki_read
  Time logging                 → timetracking_write
```

## Token-Saving Strategies

### 1. Paginate Large Lists

```
list_issues(owner: "FLCCC", repo: "my-repo", perPage: 15, page: 1)
# Default can return 30+ items. Set perPage to what you actually need.
```

### 2. Filter by State

```
list_pull_requests(owner: "FLCCC", repo: "my-repo", state: "open")    # "open" | "closed" | "all"
list_issues(owner: "FLCCC", repo: "my-repo", state: "open")           # Skip closed unless historical review
```

### 3. Target Specific Refs

```
get_file_contents(ref: "main")                              # Avoid default branch ambiguity
list_commits(sha: "feature-branch", perPage: 10, page: 1)  # Last 10 commits only
```

### 4. Avoid Redundant Discovery

Cache within a session (these don't change):
- Owner/org names from `get_me` or `get_user_orgs`
- Repo names once confirmed via `search_repos`
- Label IDs once fetched via `label_read`
- Milestone IDs once fetched via `milestone_read`

### 5. Read Before Write (Files)

`create_or_update_file` requires the current file `sha` for updates. Always call
`get_file_contents` first to extract the `sha` — skipping this causes a 409 conflict error.

## When NOT to Use Gitea MCP

| Situation | Use Instead |
|-----------|-------------|
| GitHub-hosted repo (github.com) | `mcp__github__*` tools or `gh` CLI |
| Local git operations (commit, diff, stash, rebase, cherry-pick) | `git` CLI directly |
| Pushing/pulling code | `git push` / `git pull` (git CLI) |
| GitHub Actions (github.com CI) | `gh` CLI |
| Cloning a repo | `git clone` (git CLI) |
