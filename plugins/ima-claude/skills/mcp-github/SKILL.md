---
name: mcp-github
description: >-
  GitHub MCP for FOSS and public repository management — pull requests, issues, code
  review, repository search, and GitHub API operations. Use when: working with GitHub-hosted
  repos, creating PRs for open source, managing GitHub issues, searching public repos, or
  any github.com operation. Triggers on: GitHub, github.com, open source, FOSS, public repo,
  gh pr, gh issue, upstream PR. NOT for internal repos — use mcp-gitea for Gitea-hosted repos.
  Falls back to gh CLI when MCP tools unavailable.
---

# GitHub MCP - FOSS & Public Repository Management

Use GitHub MCP tools for GitHub-hosted repositories. Falls back to `gh` CLI when MCP tools unavailable.

## Setup

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_yourtoken
```

Server: `api.githubcopilot.com`. Tools prefixed `mcp__github__*`, dynamically served — exact names may vary. On "tool not found", fall back to `gh` CLI.

## Tool Catalog

**Repository**

| Tool | Purpose |
|------|---------|
| `mcp__github__search_repositories` | Find public repos by query |
| `mcp__github__get_repository` | Repo metadata (stars, forks, topics) |
| `mcp__github__list_repository_contents` | List files/dirs |
| `mcp__github__get_file_contents` | Read file from any branch/commit |
| `mcp__github__create_repository` | Create new GitHub repo |
| `mcp__github__fork_repository` | Fork repo to your account |

**Pull Requests**

| Tool | Purpose |
|------|---------|
| `mcp__github__list_pull_requests` | List PRs (state, label, author filters) |
| `mcp__github__get_pull_request` | PR details + diff metadata |
| `mcp__github__create_pull_request` | Open new PR |
| `mcp__github__update_pull_request` | Edit title, body, labels, assignees |
| `mcp__github__merge_pull_request` | Merge (merge/squash/rebase) |
| `mcp__github__list_pull_request_reviews` | Review status |
| `mcp__github__create_pull_request_review` | Submit review (approve/request changes/comment) |
| `mcp__github__list_pull_request_comments` | Inline code comments |

**Issues**

| Tool | Purpose |
|------|---------|
| `mcp__github__list_issues` | List issues with filters |
| `mcp__github__get_issue` | Issue details and comments |
| `mcp__github__create_issue` | Open new issue |
| `mcp__github__update_issue` | Edit title, body, state, assignees, labels |
| `mcp__github__list_issue_comments` | All comments on an issue |
| `mcp__github__add_issue_comment` | Post comment |

**Code & Users**

| Tool | Purpose |
|------|---------|
| `mcp__github__search_code` | Search code across GitHub |
| `mcp__github__create_or_update_file` | Commit file change via API |
| `mcp__github__get_user` | GitHub user profile |
| `mcp__github__search_users` | Find GitHub users |

## `gh` CLI Fallback

| Operation | Command |
|-----------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| List PRs | `gh pr list` |
| View PR | `gh pr view 123` |
| Merge PR | `gh pr merge 123 --squash` |
| Create issue | `gh issue create --title "..." --body "..."` |
| List issues | `gh issue list` |
| Close issue | `gh issue close 123` |
| View repo | `gh repo view owner/name` |
| Fork repo | `gh repo fork owner/name` |
| Search repos | `gh search repos "query"` |
| Search code | `gh search code "query" --repo owner/name` |
| View file | `gh api repos/owner/name/contents/path` |

## Decision Logic

```
git remote -v

No remote → git CLI only
Remote = github.com → mcp__github__* (fallback: gh CLI)
Remote = gitea.* / internal → mcp__gitea__* (see mcp-gitea skill)
Unknown → ask user

Local git ops (commit, diff, stash) → git CLI always
```

## Common Workflows

```
# Create PR
mcp__github__create_pull_request
  owner: "FLCCC"  repo: "ima-claude"
  title: "feat: add mcp-github skill"
  body: "## Summary\n..."
  head: "feat/mcp-github-skill"  base: "main"

# Create issue
mcp__github__create_issue
  owner: "FLCCC"  repo: "ima-claude"
  title: "Bug: skill not loading"
  body: "Steps to reproduce..."
  labels: ["bug"]

# Close issue
mcp__github__add_issue_comment
  owner: "FLCCC"  repo: "ima-claude"
  issue_number: 42  body: "Fixed in v2.11.0"
mcp__github__update_issue
  owner: "FLCCC"  repo: "ima-claude"
  issue_number: 42  state: "closed"

# Review PR
mcp__github__create_pull_request_review
  owner: "FLCCC"  repo: "ima-claude"
  pull_number: 15  event: "APPROVE"  body: "LGTM"
```

## When NOT to Use

- Internal Gitea repos → use `mcp-gitea`
- Local git operations → use `git` CLI
- Reading local files → use Read tool
- GitHub Actions config → edit locally and push
