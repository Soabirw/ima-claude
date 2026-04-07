# Atlassian Direct API — Miscellaneous Operations

MCP gaps: comment edit/delete, watchers, components, versions, page deletion.

See [direct-api-auth.md](direct-api-auth.md) for auth setup.

All examples use Gateway (Bearer) auth.

---

## Comments

### Edit a Jira Comment

**API:** `PUT /rest/api/3/issue/{issueKey}/comment/{commentId}`
**When:** Correcting or updating an existing comment.

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Updated comment text"}]
        }
      ]
    }
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/comment/10042"
```

#### Notes
- Comment body must be ADF (not Markdown) for the v3 API
- Get comment IDs from `getJiraIssue` with `fields: ["comment"]`
- Only the comment author or an admin can edit

### Delete a Jira Comment

**API:** `DELETE /rest/api/3/issue/{issueKey}/comment/{commentId}`
**When:** Removing erroneous or sensitive comments.

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/comment/10042"
```

#### Notes
- Returns HTTP 204 on success (no body)
- Only the comment author or an admin can delete

---

## Watchers

### Get Watchers

**API:** `GET /rest/api/3/issue/{issueKey}/watchers`
**When:** Checking who is watching an issue.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/watchers" \
  | jq '.watchers[] | {accountId, displayName}'
```

### Add a Watcher

**API:** `POST /rest/api/3/issue/{issueKey}/watchers`
**When:** Subscribing someone to issue notifications.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '"5b10a2844c20165700ede21g"' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/watchers"
```

#### Notes
- Body is a **raw JSON string** (the accountId in quotes), not an object
- Get `accountId` from MCP `lookupJiraAccountId`

### Remove a Watcher

**API:** `DELETE /rest/api/3/issue/{issueKey}/watchers?accountId={accountId}`
**When:** Unsubscribing someone from issue notifications.

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/watchers?accountId=5b10a2844c20165700ede21g"
```

---

## Components

### List Project Components

**API:** `GET /rest/api/3/project/{projectKey}/components`
**When:** Finding component IDs for issue creation or filtering.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/project/PROJ/components" \
  | jq '.[] | {id, name, lead: .lead.displayName}'
```

### Create a Component

**API:** `POST /rest/api/3/component`
**When:** Adding a new component to a project.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Authentication",
    "project": "PROJ",
    "description": "Auth and identity management",
    "leadAccountId": "5b10a2844c20165700ede21g"
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/component" \
  | jq '{id, name}'
```

---

## Versions (Releases)

### List Project Versions

**API:** `GET /rest/api/3/project/{projectKey}/versions`
**When:** Finding version IDs for fix-version assignment.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/project/PROJ/versions" \
  | jq '.[] | {id, name, released, releaseDate}'
```

### Create a Version

**API:** `POST /rest/api/3/version`
**When:** Setting up a new release version.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "v2.1.0",
    "projectId": 10001,
    "description": "Q2 release",
    "releaseDate": "2026-06-30",
    "released": false
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/version" \
  | jq '{id, name}'
```

#### Notes
- Uses numeric `projectId`, not project key — get it from `getVisibleJiraProjects`

---

## Confluence Page Deletion

### Delete a Confluence Page

**API:** `DELETE /wiki/api/v2/pages/{pageId}`
**When:** Removing outdated or draft Confluence pages.

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/confluence/$ATLASSIAN_CLOUD_ID/wiki/api/v2/pages/12345"
```

#### Notes
- Uses Confluence **v2 API** (not v1)
- Returns HTTP 204 on success
- Page is moved to trash first (recoverable for 30 days)
- Get page ID from MCP `getConfluencePage` or `searchConfluenceUsingCql`
- Child pages become orphans — reassign or delete them first
