---
name: mcp-atlassian
description: >-
  Atlassian MCP for Jira and Confluence operations (Claude's bundled integration).
  Token-efficient workflows for issue management, page creation, search, and user mentions.
  Use when: creating/editing Jira issues, searching with JQL/CQL, creating/updating Confluence
  pages, adding comments, transitioning issue status, looking up users, mentioning/tagging
  users in Jira or Confluence content, or any Atlassian Cloud operation. Triggers on: Jira,
  Confluence, JQL, CQL, sprint, epic, story, issue, wiki page, Atlassian, @mention in
  Jira/Confluence context. Provides 50-80% token savings over naive API usage through
  field filtering, pagination control, and format selection.
---

# Atlassian MCP - Jira & Confluence Integration

Claude's bundled Atlassian MCP. All tools prefixed `mcp__claude_ai_Atlassian__`.

## Bootstrap (Required First Call)

Every session MUST start with `getAccessibleAtlassianResources` to obtain the `cloudId`.
Nearly all other tools require it. Cache this value mentally for the session.

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

### Search (3 tools - choose wisely)

| Tool | Query Language | Scope | When to Use |
|------|---------------|-------|-------------|
| `search` | Natural language | Jira + Confluence | Default search. Always use unless JQL/CQL specifically needed |
| `searchJiraIssuesUsingJql` | JQL | Jira only | Structured queries: status, assignee, project, date ranges |
| `searchConfluenceUsingCql` | CQL | Confluence only | Structured queries: space, label, type, creator |

### Jira - Read

| Tool | Purpose | Token-Saving Tip |
|------|---------|------------------|
| `getJiraIssue` | Get issue details | Use `fields` param to request ONLY needed fields |
| `getVisibleJiraProjects` | List projects | Use `searchString` to filter |
| `getJiraProjectIssueTypesMetadata` | Issue types for a project | Call before `createJiraIssue` |
| `getJiraIssueTypeMetaWithFields` | Field metadata for issue type | Call before `editJiraIssue` to know valid fields |
| `getTransitionsForJiraIssue` | Available status transitions | MUST call before `transitionJiraIssue` |
| `getJiraIssueRemoteIssueLinks` | Remote links on an issue | |

### Jira - Write

| Tool | Content Format | Purpose |
|------|---------------|---------|
| `createJiraIssue` | **Markdown** (description) | Create issue. Has `assignee_account_id` param |
| `editJiraIssue` | **Raw fields object** | Update any fields. Use for ADF descriptions with mentions |
| `addCommentToJiraIssue` | **Markdown** | Add comment. Has `commentVisibility` for restricted comments |
| `transitionJiraIssue` | Transition object | Change status. Get transition IDs first |
| `addWorklogToJiraIssue` | Duration string | Log time: `"2h"`, `"30m"`, `"4d"` |

### Confluence - Read

| Tool | Purpose | Token-Saving Tip |
|------|---------|------------------|
| `getConfluencePage` | Get page by ID | Use `contentFormat: "markdown"` for smaller responses |
| `getConfluenceSpaces` | List spaces | Filter with `keys`, `type`, `labels` |
| `getPagesInConfluenceSpace` | Pages in a space | Filter with `title`, `status`, `sort` |
| `getConfluencePageDescendants` | Child pages | Use `depth` to limit |
| `getConfluencePageFooterComments` | Footer comments | |
| `getConfluencePageInlineComments` | Inline comments | Filter by `resolutionStatus` |

### Confluence - Write

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

## User Mentions (@tagging)

**This is the most error-prone area.** Follow these patterns exactly.

### Step 1: Always Look Up the accountId First

```
lookupJiraAccountId
  cloudId: "<your-cloud-id>"
  searchString: "john@example.com"   # or "John Doe" or partial "john"
```

Returns users with `accountId` values. This works for BOTH Jira and Confluence
(same Atlassian org user pool).

### Step 2: Choose the Right Mention Strategy

#### Confluence Pages (RELIABLE - use ADF)

Use `createConfluencePage` or `updateConfluencePage` with `contentFormat: "adf"`:

```json
{
  "cloudId": "<cloud-id>",
  "spaceId": "<space-id>",
  "title": "Page Title",
  "contentFormat": "adf",
  "body": "{\"version\":1,\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"Assigned to \"},{\"type\":\"mention\",\"attrs\":{\"id\":\"5b10a2844c20165700ede21g\",\"text\":\"@John Doe\"}},{\"type\":\"text\",\"text\":\" for review.\"}]}]}"
}
```

**Critical:** The `body` value MUST be a JSON **string** (result of JSON.stringify),
NOT a raw object. This is the #1 cause of failures.

ADF mention node structure:
```json
{
  "type": "mention",
  "attrs": {
    "id": "<accountId>",
    "text": "@Display Name"
  }
}
```

The mention node is **inline** - it MUST be inside a `paragraph.content` array,
never at the top-level `doc.content`.

#### Confluence Comments (Markdown only - no native mentions)

`createConfluenceFooterComment` and `createConfluenceInlineComment` accept only
Markdown. Real @mentions are not supported in Markdown mode. Workaround:
reference the user by name in plain text, or create/update the parent **page**
with ADF to include the mention there instead.

#### Jira Issue Description (RELIABLE - use editJiraIssue with ADF)

For mentions in descriptions, use `editJiraIssue` with the ADF description field:

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

**Note:** `createJiraIssue` takes Markdown for description. To create an issue
WITH mentions, create the issue first (Markdown description), then immediately
`editJiraIssue` to replace the description with ADF containing mentions.

#### Jira Comments (Markdown - limited mention support)

`addCommentToJiraIssue` accepts Markdown via `commentBody`. Real ADF mentions
are not directly available. Workaround: reference users by display name in the
Markdown text. If real @mentions in comments are critical, use a two-step
approach: add the comment, then use the Jira UI or a direct API call for the
mention.

### Mention Pitfalls Checklist

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `username` instead of `accountId` | Shows "unlicensed user" | Always use `lookupJiraAccountId` first |
| ADF body as object instead of string | "invalid request body" error | `JSON.stringify()` the ADF for Confluence |
| Mention at doc level, not in paragraph | Silent failure / no mention | Wrap in `{"type": "paragraph", "content": [...]}` |
| Missing `<ac:link>` wrapper (storage format) | Not rendered as mention | N/A for this MCP (uses ADF/Markdown, not storage format) |
| Wiki notation `[~accountId:xxx]` in Markdown | Raw text, not a mention | Use ADF via `editJiraIssue` instead |
| Using `@username` in Markdown | Plain text, not a real mention | Use ADF path for real mentions |

## Token-Saving Strategies

### 1. Filter Jira Fields

```
getJiraIssue
  fields: ["summary", "status", "assignee", "priority"]  # NOT the full issue
```

Never fetch all fields. Common useful subsets:
- **Quick status check:** `["summary", "status", "priority"]`
- **Assignment info:** `["summary", "assignee", "reporter"]`
- **Planning:** `["summary", "status", "priority", "issuetype", "parent"]`

### 2. Use Markdown for Confluence Reads

```
getConfluencePage
  contentFormat: "markdown"  # Much smaller than ADF
```

ADF responses can be 5-10x larger than Markdown equivalents.

### 3. Limit Search Results

```
searchJiraIssuesUsingJql
  maxResults: 10       # Default is 50, often excessive
  fields: ["summary", "status"]  # Minimal fields
```

### 4. Use Rovo Search for Discovery, JQL/CQL for Precision

- "Find issues about authentication" → `search` (natural language, cross-product)
- "All open bugs in PROJ assigned to me" → `searchJiraIssuesUsingJql` with JQL
- "Pages labeled 'architecture' in DEV space" → `searchConfluenceUsingCql` with CQL

### 5. Avoid Redundant Discovery Calls

Cache these within a session (they rarely change):
- `cloudId` from `getAccessibleAtlassianResources`
- Project keys from `getVisibleJiraProjects`
- Space IDs from `getConfluenceSpaces`
- Issue type IDs from `getJiraProjectIssueTypesMetadata`

## Common Workflows

### Create and Assign a Jira Issue

```
1. getAccessibleAtlassianResources → cloudId
2. lookupJiraAccountId(searchString: "jane@co.com") → accountId
3. createJiraIssue(
     projectKey: "PROJ",
     issueTypeName: "Task",
     summary: "Review Q4 report",
     description: "Review and approve the Q4 financial report",
     assignee_account_id: "<accountId>"
   )
```

### Transition a Jira Issue

```
1. getTransitionsForJiraIssue(issueIdOrKey: "PROJ-123") → find transition ID
2. transitionJiraIssue(
     issueIdOrKey: "PROJ-123",
     transition: { "id": "<transitionId>" }
   )
```

### Create a Confluence Page with User Mention

```
1. getAccessibleAtlassianResources → cloudId
2. lookupJiraAccountId(searchString: "john") → accountId
3. getConfluenceSpaces(keys: ["DEV"]) → spaceId
4. createConfluencePage(
     spaceId: "<spaceId>",
     title: "Meeting Notes",
     contentFormat: "adf",
     body: "<ADF JSON string with mention node>"
   )
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

## Decision Logic

```
Need to search across Jira AND Confluence?
  → search (Rovo, natural language)

Need structured Jira query (by project/status/assignee/date)?
  → searchJiraIssuesUsingJql (JQL)

Need structured Confluence query (by space/label/type)?
  → searchConfluenceUsingCql (CQL)

Need to @mention a user in content?
  → lookupJiraAccountId first, then:
    - Confluence page → ADF with mention node
    - Jira description → editJiraIssue with ADF fields
    - Jira/Confluence comment → Plain text name (Markdown limitation)

Need issue field metadata before editing?
  → getJiraIssueTypeMetaWithFields

Need to change issue status?
  → getTransitionsForJiraIssue THEN transitionJiraIssue

Creating a Confluence page?
  → Need spaceId (NOT space key). Get from getConfluenceSpaces
```

## What This MCP Does NOT Support

- Direct Atlassian storage format (XML) - uses Markdown or ADF only
- Confluence page permissions management
- Jira board/sprint management
- Jira custom field creation
- Attachment uploads
- Bulk operations
- Confluence page templates
