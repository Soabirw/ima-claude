# Atlassian Direct API — Sprint & Board Management

MCP gap: no Scrum/Kanban board or sprint tools. The Agile API uses a different base path.

See [direct-api-auth.md](direct-api-auth.md) for auth setup.

All examples use Gateway (Bearer) auth. The Agile API base is:
```
https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0
```

---

### List Boards

**API:** `GET /rest/agile/1.0/board`
**When:** Finding the board ID for a project.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/board?projectKeyOrId=PROJ" \
  | jq '.values[] | {id, name, type}'
```

#### Notes
- Filter by project with `projectKeyOrId` param
- `type` is `scrum` or `kanban`
- Board ID is needed for all subsequent sprint operations

---

### Get Active Sprint

**API:** `GET /rest/agile/1.0/board/{boardId}/sprint?state=active`
**When:** Finding the current sprint to add issues to.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/board/42/sprint?state=active" \
  | jq '.values[] | {id, name, state, startDate, endDate}'
```

#### Notes
- `state` filter accepts: `future`, `active`, `closed`
- Multiple states: `state=active,future`
- Only Scrum boards have sprints — Kanban boards return empty

---

### Get Issues in a Sprint

**API:** `GET /rest/agile/1.0/sprint/{sprintId}/issue`
**When:** Reviewing what's in a sprint.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/sprint/100/issue?fields=summary,status,assignee" \
  | jq '.issues[] | {key, summary: .fields.summary, status: .fields.status.name}'
```

#### Notes
- Use `fields` param to limit response size (same as Jira REST API v3)
- Supports `jql` param for additional filtering within the sprint
- Paginated: use `startAt` and `maxResults` for large sprints

---

### Move Issues to a Sprint

**API:** `POST /rest/agile/1.0/sprint/{sprintId}/issue`
**When:** Adding issues to a sprint (sprint planning).

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issues": ["PROJ-101", "PROJ-102", "PROJ-103"]}' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/sprint/100/issue"
```

#### Notes
- Accepts issue keys or issue IDs
- Issues are moved from their current sprint (or backlog) to the target sprint
- No response body on success (HTTP 204)
- To move to backlog: use `POST /rest/agile/1.0/backlog/issue` with same body

---

### Create a Sprint

**API:** `POST /rest/agile/1.0/sprint`
**When:** Setting up a new sprint.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sprint 42",
    "originBoardId": 42,
    "startDate": "2026-04-06T09:00:00.000Z",
    "endDate": "2026-04-20T17:00:00.000Z",
    "goal": "Complete auth migration"
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/sprint" \
  | jq '{id, name, state}'
```

#### Notes
- `originBoardId` is required — use the board ID from "List Boards"
- Dates are ISO 8601
- Sprint starts in `future` state

---

### Start or Close a Sprint

**API:** `PUT /rest/agile/1.0/sprint/{sprintId}`
**When:** Starting a planned sprint or closing a completed one.

```bash
# Start a sprint
curl -s -X PUT \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "active"}' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/sprint/100"

# Close a sprint (must specify where incomplete issues go)
curl -s -X PUT \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "closed"}' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/sprint/100"
```

#### Notes
- Only one sprint can be `active` per board at a time
- When closing, incomplete issues move to the backlog by default
- To move incomplete issues to a specific sprint, close the sprint via the Jira UI (API doesn't support the move-to-sprint parameter natively)

---

### Move Issues to Backlog

**API:** `POST /rest/agile/1.0/backlog/issue`
**When:** Removing issues from a sprint without deleting them.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issues": ["PROJ-101", "PROJ-102"]}' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0/backlog/issue"
```
