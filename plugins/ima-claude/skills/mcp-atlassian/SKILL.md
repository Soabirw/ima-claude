---
name: mcp-atlassian
description: >-
  Hybrid Atlassian integration — MCP-first for Jira/Confluence operations,
  direct REST API (curl) for gaps the MCP doesn't cover.
  Use when: creating/editing Jira issues, searching with JQL/CQL, creating/updating Confluence
  pages, adding comments, transitioning issue status, looking up users, mentioning/tagging
  users in Jira or Confluence content, downloading/uploading attachments, sprint/board
  management, bulk operations, or any Atlassian Cloud operation. Triggers on: Jira,
  Confluence, JQL, CQL, sprint, epic, story, issue, wiki page, Atlassian, attachment,
  board, backlog, @mention in Jira/Confluence context.
---

# Atlassian Integration — Hybrid MCP + Direct API

MCP-first: use bundled tools (prefixed `mcp__claude_ai_Atlassian__`) for covered operations.
Direct REST API (curl via Bash) for gaps. See [Decision Logic](#decision-logic).

## Bootstrap (Required First Call)

Every session MUST start with `getAccessibleAtlassianResources` to obtain `cloudId`.
Nearly all other tools require it. Cache for the session.

```
getAccessibleAtlassianResources  → returns cloudId (UUID or site URL)
```

## Tool Catalog

### Discovery & Users

| Tool | Purpose | Key Params |
|------|---------|------------|
| `getAccessibleAtlassianResources` | Get cloudId (CALL FIRST) | *(none)* |
| `atlassianUserInfo` | Current authenticated user | *(none)* |
| `lookupJiraAccountId` | Find user accountId by name/email | `cloudId`, `searchString` |

### Search (choose wisely)

| Tool | Query Language | Scope | When to Use |
|------|---------------|-------|-------------|
| `search` | Natural language | Jira + Confluence | Default. Use unless JQL/CQL specifically needed |
| `searchJiraIssuesUsingJql` | JQL | Jira only | Structured: status, assignee, project, date ranges |
| `searchConfluenceUsingCql` | CQL | Confluence only | Structured: space, label, type, creator |

### Jira — Read

| Tool | Purpose | Token-Saving Tip |
|------|---------|------------------|
| `getJiraIssue` | Get issue details | Use `fields` param — request ONLY needed fields |
| `getVisibleJiraProjects` | List projects | Use `searchString` to filter |
| `getJiraProjectIssueTypesMetadata` | Issue types for project | Call before `createJiraIssue` |
| `getJiraIssueTypeMetaWithFields` | Field metadata for issue type | Call before `editJiraIssue` |
| `getTransitionsForJiraIssue` | Available status transitions | MUST call before `transitionJiraIssue` |
| `getJiraIssueRemoteIssueLinks` | Remote links on issue | |

### Jira — Write

| Tool | Content Format | Purpose |
|------|---------------|---------|
| `createJiraIssue` | **Markdown** (description) | Create issue. Has `assignee_account_id` param |
| `editJiraIssue` | **Raw fields object** | Update any fields. Use for ADF descriptions with mentions |
| `addCommentToJiraIssue` | **Markdown** | Add comment. Has `commentVisibility` for restricted comments |
| `transitionJiraIssue` | Transition object | Change status. Get transition IDs first |
| `addWorklogToJiraIssue` | Duration string | Log time: `"2h"`, `"30m"`, `"4d"` |

### Confluence — Read

| Tool | Purpose | Token-Saving Tip |
|------|---------|------------------|
| `getConfluencePage` | Get page by ID | Use `contentFormat: "markdown"` — much smaller than ADF |
| `getConfluenceSpaces` | List spaces | Filter with `keys`, `type`, `labels` |
| `getPagesInConfluenceSpace` | Pages in space | Filter with `title`, `status`, `sort` |
| `getConfluencePageDescendants` | Child pages | Use `depth` to limit |
| `getConfluencePageFooterComments` | Footer comments | |
| `getConfluencePageInlineComments` | Inline comments | Filter by `resolutionStatus` |

### Confluence — Write

| Tool | Content Format | Purpose |
|------|---------------|---------|
| `createConfluencePage` | **Markdown** or **ADF** | Create page. Requires `spaceId` (not space key!) |
| `updateConfluencePage` | **Markdown** or **ADF** | Replace entire page body |
| `createConfluenceFooterComment` | **Markdown only** | Comment on page |
| `createConfluenceInlineComment` | **Markdown only** | Comment on specific text selection |

### Cross-Product

| Tool | Purpose |
|------|---------|
| `search` | Rovo natural language search across Jira + Confluence |
| `fetch` | Get detail by ARI (Atlassian Resource Identifier). Read-only |

## Direct API — Gap Operations

Use `curl` via Bash only for operations not in the Tool Catalog above.

### Auth Setup

Two methods:
- **Gateway (Bearer)** — preferred for service accounts: `ATLASSIAN_CLOUD_ID` + `ATLASSIAN_BEARER_TOKEN`
- **Direct (Basic)** — fallback for personal tokens: `ATLASSIAN_DOMAIN` + `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN`

Verify auth before first direct call:
```bash
curl -s -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/myself" | jq '.displayName'
```

Full setup: [references/direct-api-auth.md](references/direct-api-auth.md)

### Gap Recipes

| Operation | Reference | Priority |
|-----------|-----------|----------|
| Attachment download/upload (Jira + Confluence) | [direct-api-attachments.md](references/direct-api-attachments.md) | P0 |
| Sprint/board management (Agile API) | [direct-api-sprints.md](references/direct-api-sprints.md) | P1 |
| Bulk operations (batch edit, bulk transition) | [direct-api-bulk.md](references/direct-api-bulk.md) | P1 |
| Comment edit/delete, watchers, components, versions, page deletion | [direct-api-misc.md](references/direct-api-misc.md) | P2 |

## Decision Logic

```
Can MCP tool handle it?             → MCP tool (always preferred)
Attachment download/upload?         → direct-api-attachments.md
Sprint or board operation?          → direct-api-sprints.md
Bulk operation (5+ issues)?         → direct-api-bulk.md
Edit/delete comment?                → direct-api-misc.md
Watchers, components, versions?     → direct-api-misc.md
Delete Confluence page?             → direct-api-misc.md

Search across Jira AND Confluence?  → search (Rovo, natural language)
Structured Jira query?              → searchJiraIssuesUsingJql (JQL)
Structured Confluence query?        → searchConfluenceUsingCql (CQL)

@mention in content?                → lookupJiraAccountId first, then:
  Confluence page                   → ADF with mention node
  Jira description                  → editJiraIssue with ADF fields
  Jira/Confluence comment           → plain text name (Markdown limitation)

Issue field metadata before editing? → getJiraIssueTypeMetaWithFields
Change issue status?                 → getTransitionsForJiraIssue THEN transitionJiraIssue
Creating Confluence page?            → need spaceId (NOT space key) from getConfluenceSpaces
```

## User Mentions (@tagging)

**Most error-prone area.** Follow exactly.

### Step 1: Look Up accountId

```
lookupJiraAccountId
  cloudId: "<your-cloud-id>"
  searchString: "john@example.com"   # or "John Doe" or partial "john"
```

Works for both Jira and Confluence (same org user pool).

### Step 2: Choose Mention Strategy

#### Confluence Pages — use ADF (reliable)

`createConfluencePage` / `updateConfluencePage` with `contentFormat: "adf"`:

```json
{
  "cloudId": "<cloud-id>",
  "spaceId": "<space-id>",
  "title": "Page Title",
  "contentFormat": "adf",
  "body": "{\"version\":1,\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Assigned to \"},{\"type\":\"mention\",\"attrs\":{\"id\":\"5b10a2844c20165700ede21g\",\"text\":\"@John Doe\"}},{\"type\":\"text\",\"text\":\" for review.\"}]}]}"
}
```

**Critical:** `body` MUST be a JSON **string** (result of JSON.stringify), NOT a raw object. This is the #1 cause of failures.

ADF mention node:
```json
{
  "type": "mention",
  "attrs": {
    "id": "<accountId>",
    "text": "@Display Name"
  }
}
```

Mention node is **inline** — MUST be inside `paragraph.content`, never at top-level `doc.content`.

#### Confluence Comments — no native mentions

`createConfluenceFooterComment` / `createConfluenceInlineComment` accept Markdown only. Real @mentions unsupported. Workaround: reference by name in plain text, or add the mention to the parent page via ADF instead.

#### Jira Description — use ADF (reliable)

Use `editJiraIssue` with ADF description:

```json
{
  "cloudId": "<cloud-id>",
  "issueIdOrKey": "PROJ-123",
  "fields": {
    "description": {
      "version": 1,
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Assigned to " },
            {
              "type": "mention",
              "attrs": {
                "id": "5b10a2844c20165700ede21g",
                "text": "@John Doe"
              }
            },
            { "type": "text", "text": " for review." }
          ]
        }
      ]
    }
  }
}
```

To create issue WITH mentions: create with `createJiraIssue` (Markdown), then immediately `editJiraIssue` to replace description with ADF.

#### Jira Comments — limited

`addCommentToJiraIssue` accepts Markdown only. Reference users by display name. For real @mentions in comments, use direct API after adding the comment.

### Mention Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `username` instead of `accountId` | Shows "unlicensed user" | Always use `lookupJiraAccountId` first |
| ADF body as object instead of string | "invalid request body" | `JSON.stringify()` the ADF for Confluence |
| Mention at doc level, not in paragraph | Silent failure / no mention | Wrap in `{"type": "paragraph", "content": [...]}` |
| Wiki notation `[~accountId:xxx]` in Markdown | Raw text, not mention | Use ADF via `editJiraIssue` instead |
| `@username` in Markdown | Plain text, not real mention | Use ADF path for real mentions |

## Token-Saving Strategies

**Filter Jira fields** — never fetch all:
```
getJiraIssue
  fields: ["summary", "status", "assignee", "priority"]
```

Common subsets:
- Quick status: `["summary", "status", "priority"]`
- Assignment: `["summary", "assignee", "reporter"]`
- Planning: `["summary", "status", "priority", "issuetype", "parent"]`

**Markdown for Confluence reads** — ADF is 5-10x larger:
```
getConfluencePage
  contentFormat: "markdown"
```

**Limit search results:**
```
searchJiraIssuesUsingJql
  maxResults: 10
  fields: ["summary", "status"]
```

**Cache within session** (rarely change):
- `cloudId` from `getAccessibleAtlassianResources`
- Project keys from `getVisibleJiraProjects`
- Space IDs from `getConfluenceSpaces`
- Issue type IDs from `getJiraProjectIssueTypesMetadata`

## Common Workflows

### Create and Assign Jira Issue
```
1. getAccessibleAtlassianResources → cloudId
2. lookupJiraAccountId(searchString: "jane@co.com") → accountId
3. createJiraIssue(projectKey: "PROJ", issueTypeName: "Task",
     summary: "Review Q4 report", assignee_account_id: "<accountId>")
```

### Transition Jira Issue
```
1. getTransitionsForJiraIssue(issueIdOrKey: "PROJ-123") → transition ID
2. transitionJiraIssue(issueIdOrKey: "PROJ-123", transition: {"id": "<transitionId>"})
```

### Create Confluence Page with Mention
```
1. getAccessibleAtlassianResources → cloudId
2. lookupJiraAccountId(searchString: "john") → accountId
3. getConfluenceSpaces(keys: ["DEV"]) → spaceId
4. createConfluencePage(spaceId, title, contentFormat: "adf", body: "<ADF JSON string>")
```

### Inline Comment on Specific Text
```
createConfluenceInlineComment(
  pageId: "<pageId>",
  body: "This section needs updating",
  inlineCommentProperties: {
    "textSelection": "exact text on page",
    "textSelectionMatchCount": 1,
    "textSelectionMatchIndex": 0
  }
)
```

### Download Attachments (Hybrid)
```
1. getJiraIssue(issueIdOrKey: "PROJ-123", fields: ["attachment"]) → content URL
2. curl -s -L -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
     -o "mockup.png" "<content-url>"
```
Full recipes: [references/direct-api-attachments.md](references/direct-api-attachments.md)

### Move Issues to Sprint (Direct API)
```
1. curl: GET /rest/agile/1.0/board?projectKeyOrId=PROJ → boardId
2. curl: GET /rest/agile/1.0/board/{boardId}/sprint?state=active → sprintId
3. curl: POST /rest/agile/1.0/sprint/{sprintId}/issue  body: {"issues": ["PROJ-101"]}
```
Full recipes: [references/direct-api-sprints.md](references/direct-api-sprints.md)

## Limitations

### Not Supported

- Atlassian storage format (XML) — MCP uses Markdown or ADF only
- Confluence page permissions management
- Jira custom field creation
- Confluence page templates
- Jira automation rules / webhooks

### Covered by Direct API

| Gap | Recipe |
|-----|--------|
| Attachment download/upload | [direct-api-attachments.md](references/direct-api-attachments.md) |
| Sprint/board management | [direct-api-sprints.md](references/direct-api-sprints.md) |
| Bulk operations | [direct-api-bulk.md](references/direct-api-bulk.md) |
| Comment edit/delete | [direct-api-misc.md](references/direct-api-misc.md) |
| Watchers | [direct-api-misc.md](references/direct-api-misc.md) |
| Components & versions | [direct-api-misc.md](references/direct-api-misc.md) |
| Confluence page deletion | [direct-api-misc.md](references/direct-api-misc.md) |
