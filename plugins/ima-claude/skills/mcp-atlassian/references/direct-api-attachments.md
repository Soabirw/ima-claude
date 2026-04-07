# Atlassian Direct API — Attachments

MCP gap: no attachment download or upload. Use these curl recipes.

See [direct-api-auth.md](direct-api-auth.md) for auth setup.

All examples use Gateway (Bearer) auth. Substitute Basic auth headers if needed.

---

### List Attachments on a Jira Issue

**API:** `GET /rest/api/3/issue/{issueKey}?fields=attachment`
**When:** Need to see what files are attached before downloading.

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123?fields=attachment" \
  | jq '.fields.attachment[] | {id, filename, mimeType, size, content}'
```

**Tip:** You can also use MCP `getJiraIssue` with `fields: ["attachment"]` — the `content` URL in the response is what you need for download.

#### Response Shape

```json
{
  "id": "10001",
  "filename": "mockup.png",
  "mimeType": "image/png",
  "size": 245678,
  "content": "https://yoursite.atlassian.net/rest/api/3/attachment/content/10001"
}
```

---

### Download a Single Attachment

**API:** `GET` the `content` URL from the attachment metadata
**When:** Need the actual binary file (image, PDF, document).

```bash
# Get the download URL from attachment metadata
ATTACHMENT_URL=$(curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123?fields=attachment" \
  | jq -r '.fields.attachment[] | select(.filename == "mockup.png") | .content')

# Download the file
curl -s -L \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -o "mockup.png" \
  "$ATTACHMENT_URL"
```

#### Notes
- The `-L` flag follows redirects — Atlassian may redirect to a CDN URL
- For Gateway auth, the `content` URL may use the direct domain. The Bearer token works with both
- To download ALL attachments from an issue, pipe through a loop:

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123?fields=attachment" \
  | jq -r '.fields.attachment[] | "\(.content)\t\(.filename)"' \
  | while IFS=$'\t' read -r url fname; do
      curl -s -L -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" -o "$fname" "$url"
      echo "Downloaded: $fname"
    done
```

---

### Upload Attachment to a Jira Issue

**API:** `POST /rest/api/3/issue/{issueKey}/attachments`
**When:** Attaching generated files, screenshots, or documents to an issue.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/file.pdf" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/issue/PROJ-123/attachments" \
  | jq '.[0] | {id, filename, size}'
```

#### Notes
- **Do NOT set `Content-Type: application/json`** — this is `multipart/form-data` (curl sets it automatically with `-F`)
- `X-Atlassian-Token: no-check` is required (XSRF protection bypass for attachments)
- Response is an array of attachment objects (one per file)
- Multiple files: use multiple `-F "file=@path"` flags

---

### Upload Attachment to a Confluence Page

**API:** `POST /wiki/rest/api/content/{pageId}/child/attachment`
**When:** Attaching files to Confluence pages.

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/diagram.png" \
  "https://api.atlassian.com/ex/confluence/$ATLASSIAN_CLOUD_ID/wiki/rest/api/content/12345/child/attachment" \
  | jq '.results[0] | {id: .id, title: .title}'
```

#### Notes
- Use the **Confluence v1 API** (not v2) for attachment uploads
- Page ID is numeric — get it from MCP `getConfluencePage` or `searchConfluenceUsingCql`
- To update an existing attachment, use `PUT` with the same endpoint and filename
