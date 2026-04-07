# Atlassian Direct API — Bulk Operations

MCP gap: no batch/bulk endpoints. Use these patterns for multi-issue operations.

See [direct-api-auth.md](direct-api-auth.md) for auth setup.

All examples use Gateway (Bearer) auth.

---

### Bulk Edit Issues (Jira v3)

**API:** `POST /rest/api/3/issue/bulk`
**When:** Updating the same fields on many issues at once.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "issueUpdates": [
      {
        "issueIdOrKey": "PROJ-101",
        "fields": {"priority": {"name": "High"}, "labels": ["urgent"]}
      },
      {
        "issueIdOrKey": "PROJ-102",
        "fields": {"priority": {"name": "High"}, "labels": ["urgent"]}
      }
    ]
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/bulk" \
  | jq '.errors'
```

#### Notes
- Max ~50 issues per request (Atlassian soft limit)
- Response includes per-issue errors — check `.errors` for partial failures
- Each issue can have different field updates
- This endpoint may not be available on all Jira Cloud plans

---

### Bulk Transition (Loop Pattern)

**When:** Moving many issues through a workflow step (e.g., close all done issues).

This uses the MCP `transitionJiraIssue` in a loop. No direct bulk transition API exists.

**Pattern:**
1. Find issues with JQL via MCP `searchJiraIssuesUsingJql`
2. Get transitions for one representative issue via MCP `getTransitionsForJiraIssue`
3. Loop `transitionJiraIssue` for each issue

```
# Step 1: Find issues
searchJiraIssuesUsingJql
  cloudId: "<cloudId>"
  jql: "project = PROJ AND status = 'In Review'"
  maxResults: 50
  fields: ["summary", "status"]

# Step 2: Get transition ID (same for all issues in the same workflow)
getTransitionsForJiraIssue
  cloudId: "<cloudId>"
  issueIdOrKey: "PROJ-101"  # any issue from the results

# Step 3: Transition each issue
# Repeat for each issue key from Step 1:
transitionJiraIssue
  cloudId: "<cloudId>"
  issueIdOrKey: "PROJ-101"
  transition: {"id": "<transitionId>"}
```

#### Notes
- Rate limit: ~100 requests/minute for Jira Cloud
- For large batches (50+ issues), add a brief delay between calls
- If issues span different workflows, group by issue type and get transitions per group

---

### Paginated JQL Fetch

**When:** Fetching more results than the default page size (50).

Use MCP `searchJiraIssuesUsingJql` with pagination:

```
# Page 1
searchJiraIssuesUsingJql
  cloudId: "<cloudId>"
  jql: "project = PROJ AND status != Done"
  maxResults: 50
  startAt: 0
  fields: ["summary", "status"]

# Page 2
searchJiraIssuesUsingJql
  cloudId: "<cloudId>"
  jql: "project = PROJ AND status != Done"
  maxResults: 50
  startAt: 50
  fields: ["summary", "status"]
```

Or via direct API for more control:

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jql": "project = PROJ AND status != Done ORDER BY created DESC",
    "maxResults": 100,
    "startAt": 0,
    "fields": ["summary", "status", "assignee"]
  }' \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/search" \
  | jq '{total: .total, count: (.issues | length), issues: [.issues[] | {key, summary: .fields.summary, status: .fields.status.name}]}'
```

#### Notes
- MCP `searchJiraIssuesUsingJql` max is typically 50 per page
- Direct API `POST /search` supports up to 100 per page
- Check `.total` in response to know when to stop paginating
- Use `POST` (not `GET`) for the search endpoint — JQL strings can exceed URL length limits

---

### Bulk Add Labels

**When:** Tagging many issues with the same label.

```bash
# For each issue, use the update operations syntax
for KEY in PROJ-101 PROJ-102 PROJ-103; do
  curl -s -X PUT \
    -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"update": {"labels": [{"add": "reviewed"}]}}' \
    "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/$KEY"
  echo "Labeled: $KEY"
done
```

#### Notes
- Uses Jira's `update` operations (add/remove/set) — more precise than replacing the entire `fields.labels` array
- Same pattern works for `components`, `fixVersions`, and other array fields
