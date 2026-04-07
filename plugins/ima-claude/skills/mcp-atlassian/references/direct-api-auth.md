# Atlassian Direct REST API — Authentication

When the bundled MCP tools don't cover an operation, use `curl` via Bash with these auth patterns.

## ENV Variables

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `ATLASSIAN_CLOUD_ID` | Yes (gateway) | Cloud instance ID | `a1b2c3d4-e5f6-...` |
| `ATLASSIAN_BEARER_TOKEN` | Yes (gateway) | Service account token (`ATSTT...`) | `ATSTT...` |
| `ATLASSIAN_DOMAIN` | Yes (basic) | Site domain | `yoursite.atlassian.net` |
| `ATLASSIAN_EMAIL` | Yes (basic) | Account email | `you@company.com` |
| `ATLASSIAN_API_TOKEN` | Yes (basic) | Personal API token | `abc123...` |

**Choose one auth method.** Gateway (Bearer) is preferred for service accounts. Basic is the fallback for personal tokens.

## Base URLs

### Jira REST API v3

| Auth Method | Base URL |
|-------------|----------|
| Gateway (Bearer) | `https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3` |
| Direct (Basic) | `https://$ATLASSIAN_DOMAIN/rest/api/3` |

### Jira Agile API v1

| Auth Method | Base URL |
|-------------|----------|
| Gateway (Bearer) | `https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/agile/1.0` |
| Direct (Basic) | `https://$ATLASSIAN_DOMAIN/rest/agile/1.0` |

### Confluence REST API

| Auth Method | Base URL |
|-------------|----------|
| Gateway (Bearer) | `https://api.atlassian.com/ex/confluence/$ATLASSIAN_CLOUD_ID/wiki/rest/api` |
| Direct (Basic) | `https://$ATLASSIAN_DOMAIN/wiki/rest/api` |

### Confluence v2 API

| Auth Method | Base URL |
|-------------|----------|
| Gateway (Bearer) | `https://api.atlassian.com/ex/confluence/$ATLASSIAN_CLOUD_ID/wiki/api/v2` |
| Direct (Basic) | `https://$ATLASSIAN_DOMAIN/wiki/api/v2` |

## Reusable Header Blocks

### Gateway (Bearer) — copy into any curl

```bash
-H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json"
```

### Direct (Basic) — copy into any curl

```bash
-H "Authorization: Basic $(echo -n "$ATLASSIAN_EMAIL:$ATLASSIAN_API_TOKEN" | base64)" \
-H "Content-Type: application/json" \
-H "Accept: application/json"
```

## Verify Your Setup

Run this before any direct API session. Should return your display name.

```bash
# Gateway auth
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/ex/jira/$ATLASSIAN_CLOUD_ID/rest/api/3/myself" \
  | jq '.displayName'

# Basic auth
curl -s \
  -H "Authorization: Basic $(echo -n "$ATLASSIAN_EMAIL:$ATLASSIAN_API_TOKEN" | base64)" \
  "https://$ATLASSIAN_DOMAIN/rest/api/3/myself" \
  | jq '.displayName'
```

## Getting the Cloud ID

The MCP's `getAccessibleAtlassianResources` returns the `cloudId`. You can also get it via:

```bash
curl -s \
  -H "Authorization: Bearer $ATLASSIAN_BEARER_TOKEN" \
  "https://api.atlassian.com/oauth/token/accessible-resources" \
  | jq '.[0].id'
```

Store it: `export ATLASSIAN_CLOUD_ID="<value>"`

## Error Patterns

| Status | Meaning | Fix |
|--------|---------|-----|
| 401 | Bad credentials | Check token/email/apiToken values |
| 403 | Missing scope or permission | Token needs the right OAuth scopes or project access |
| 404 | Wrong base URL or resource not found | Check gateway vs direct URL, verify resource exists |
| 429 | Rate limited | Wait and retry; Jira Cloud allows ~100 req/min |
