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

Use GitHub MCP tools for GitHub-hosted repositories. Falls back to the `gh` CLI when MCP tools aren't available.

## Setup

Requires `GITHUB_PERSONAL_ACCESS_TOKEN` in your environment:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_yourtoken
```

The GitHub MCP server is HTTP-based at `api.githubcopilot.com`. Tools are prefixed `mcp__github__*` and are **dynamically served** — exact tool names may vary. If a tool call fails with "tool not found", fall back to the `gh` CLI table below.

## Tool Catalog

GitHub MCP tools map to GitHub REST API operations. Expected tools by category:

**Repository**

| Tool (expected) | Purpose |
|-----------------|---------|
| `mcp__github__search_repositories` | Find public repos by query |
| `mcp__github__get_repository` | Get repo metadata (stars, forks, topics) |
| `mcp__github__list_repository_contents` | List files/dirs in a repo |
| `mcp__github__get_file_contents` | Read a file from any branch/commit |
| `mcp__github__create_repository` | Create a new GitHub repo |
| `mcp__github__fork_repository` | Fork a repo to your account |

**Pull Requests**

| Tool (expected) | Purpose |
|-----------------|---------|
| `mcp__github__list_pull_requests` | List PRs with filters (state, label, author) |
| `mcp__github__get_pull_request` | Get PR details including diff metadata |
| `mcp__github__create_pull_request` | Open a new PR |
| `mcp__github__update_pull_request` | Edit title, body, labels, assignees |
| `mcp__github__merge_pull_request` | Merge a PR (merge, squash, or rebase) |
| `mcp__github__list_pull_request_reviews` | Get review status |
| `mcp__github__create_pull_request_review` | Submit a review (approve, request changes, comment) |
| `mcp__github__list_pull_request_comments` | List inline code comments |

**Issues**

| Tool (expected) | Purpose |
|-----------------|---------|
| `mcp__github__list_issues` | List issues with filters |
| `mcp__github__get_issue` | Get issue details and comments |
| `mcp__github__create_issue` | Open a new issue |
| `mcp__github__update_issue` | Edit title, body, state, assignees, labels |
| `mcp__github__list_issue_comments` | Get all comments on an issue |
| `mcp__github__add_issue_comment` | Post a comment on an issue |

**Code & Files**

| Tool (expected) | Purpose |
|-----------------|---------|
| `mcp__github__search_code` | Search code across GitHub repos |
| `mcp__github__create_or_update_file` | Commit a file change via API |

**Users & Orgs**

| Tool (expected) | Purpose |
|-----------------|---------|
| `mcp__github__get_user` | Get GitHub user profile |
| `mcp__github__search_users` | Find GitHub users |

## `gh` CLI Fallback

When MCP tools aren't available or sufficient, use the `gh` CLI:

| Operation | `gh` Command |
|-----------|-------------|
| Create PR | `gh pr create --title "..." --body "..."` |
| List PRs | `gh pr list` |
| View PR | `gh pr view 123` |
| Merge PR | `gh pr merge 123 --squash` |
| Create issue | `gh issue create --title "..." --body "..."` |
| List issues | `gh issue list` |
| Close issue | `gh issue close 123` |
| View repo | `gh repo view owner/name` |
| Fork repo | `gh repo fork owner/name` |
| Clone fork | `gh repo clone owner/name` |
| Search repos | `gh search repos "query"` |
| Search code | `gh search code "query" --repo owner/name` |
| View file | `gh api repos/owner/name/contents/path` |

## Decision Logic

```
Check git remote: git remote -v

No remote configured?
  → Local-only repo. Use git CLI directly.

Does the remote point to github.com?
  → Yes: Use mcp__github__* tools
      → MCP tools not available or responding?
        → Use gh CLI as fallback
  → No: Does it point to gitea.* / internal hostname?
      → Yes: Use mcp__gitea__* tools (see mcp-gitea skill)
      → Unknown: Check with the user

For local-only git operations (commit, diff, log, stash, branch):
  → Always use git CLI directly — no MCP needed
```

## Common Workflows

### Create a PR for a FOSS Project

```
1. Confirm the remote is github.com:
   git remote -v

2. Create the PR:
   mcp__github__create_pull_request
     owner: "FLCCC"
     repo:  "ima-claude"
     title: "feat: add mcp-github skill"
     body:  "## Summary\n..."
     head:  "feat/mcp-github-skill"
     base:  "main"
```

### Manage Issues

```
# Open a bug report
mcp__github__create_issue
  owner: "FLCCC"
  repo:  "ima-claude"
  title: "Bug: skill not loading"
  body:  "Steps to reproduce..."
  labels: ["bug"]

# Close with a comment
mcp__github__add_issue_comment
  owner: "FLCCC"
  repo:  "ima-claude"
  issue_number: 42
  body: "Fixed in v2.11.0"

mcp__github__update_issue
  owner: "FLCCC"
  repo:  "ima-claude"
  issue_number: 42
  state: "closed"
```

### Search Public Repos

```
mcp__github__search_repositories
  query: "claude code skills mcp"
  sort: "stars"

# Or via gh CLI:
gh search repos "claude mcp skills" --sort stars --limit 10
```

### Review a PR

```
mcp__github__get_pull_request
  owner: "FLCCC"
  repo:  "ima-claude"
  pull_number: 15

mcp__github__create_pull_request_review
  owner: "FLCCC"
  repo:  "ima-claude"
  pull_number: 15
  event: "APPROVE"
  body: "LGTM"
```

## When NOT to Use

- Internal Gitea repos — use `mcp-gitea` skill instead
- Local git operations (commit, diff, stash) — use `git` CLI directly
- Reading local files — use the Read tool, not the GitHub API
- GitHub Actions configuration — edit files locally and push

## Notes

- GitHub MCP tools are **dynamically served** — exact names may differ. If a tool call fails with "tool not found", fall back to `gh` CLI.
- The `gh` CLI is reliable and covers the majority of GitHub operations. MCP adds value for structured responses (search, bulk operations, code review workflows).
- Always confirm the target remote (`git remote -v`) before deciding which tool to use.
