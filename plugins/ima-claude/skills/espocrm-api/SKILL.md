---
name: "espocrm-api"
description: >-
  EspoCRM v9.x REST API patterns — authentication (API Key, HMAC), CRUD operations,
  JSON WHERE filtering, relationship management, webhooks, mass operations, error
  handling, and performance. Official PHP client and Node.js patterns. Use when:
  calling EspoCRM API, building CRM integrations, querying CRM data, managing
  webhooks, bulk CRM operations. Triggers on: EspoCRM API, CRM endpoint, CRM
  query, CRM webhook, CRM filter, espo api, api/v1, X-Api-Key, HMAC auth,
  entity CRUD.
---

# EspoCRM REST API (v9.x)

Patterns for the EspoCRM REST API. External integrations, data pipelines, and automation.

**Base URL**: `https://{your-site}/api/v1/`
**Content-Type**: `application/json` (all requests)
**Parent skill**: `espocrm` (router — Salesforce mapping, shared context)
**Companion skills**: `php-fp` (PHP integrations), `js-fp-api` (Node integrations)
**Live docs**: Context7 `/espocrm/documentation`

---

## Authentication

Three methods, in order of recommendation:

### 1. API Key (Simple, Recommended for Dev/Internal)

Create an API User at Administration > API Users. Authentication method: "API Key". Assign a Role for scope.

```
X-Api-Key: {key_from_api_user_detail_view}
```

One header. Done. Use when transport is already secured (HTTPS, internal network).

### 2. HMAC (Production, Most Secure)

Create an API User with "HMAC" auth. Both API Key and Secret Key are generated. Secret never leaves your server.

```
X-Hmac-Authorization: base64(apiKey + ':' + hmacSha256(METHOD + ' /' + uri, secretKey))
```

Where `METHOD` is uppercase (GET, POST, PUT, DELETE) and `uri` is the path after `/api/v1/`.

```php
// PHP
$string = $method . ' /' . $uri;
$hash = hash_hmac('sha256', $string, $secretKey);
$header = base64_encode($apiKey . ':' . $hash);
// X-Hmac-Authorization: $header
```

```javascript
// Node.js
import { createHmac } from 'node:crypto';
const hash = createHmac('sha256', secretKey).update(`${method} /${uri}`).digest('hex');
const header = Buffer.from(`${apiKey}:${hash}`).toString('base64');
// X-Hmac-Authorization: header
```

### 3. Basic / Token Auth (Session-Based Only)

```
Espo-Authorization: base64(username + ':' + token)
```

Obtain token via `GET App/user` with initial credentials. Only for session flows (SPA, frontend). Never for server-to-server.

### Auth Decision

| Context | Method |
|---|---|
| Dev/testing, internal scripts | API Key |
| Production integrations | HMAC |
| Frontend SPA, session flows | Token auth |
| Never | Basic auth with plaintext password |

---

## CRUD Operations

All entity types share the same endpoint pattern. Replace `{Entity}` with the type name (Account, Contact, Lead, CMyCustomEntity, etc.).

### List Records
```
GET {Entity}
```
Returns `{"list": [...], "total": N}`. Total is `-1` if more records exist (pagination needed), `-2` if count disabled.

### Read One Record
```
GET {Entity}/{id}
```

### Create
```
POST {Entity}
{"name": "Acme Corp", "assignedUserId": "someUserId"}
```
Returns the created record with generated `id`. Use `X-Skip-Duplicate-Check: true` to bypass duplicate detection.

### Update (Partial)
```
PUT {Entity}/{id}
{"status": "Closed Won"}
```
Only send changed fields. Returns full updated record.

### Delete
```
DELETE {Entity}/{id}
```
Returns `true`.

### Endpoint Summary

| Operation | Method | Path |
|---|---|---|
| List | GET | `{Entity}` |
| Read | GET | `{Entity}/{id}` |
| Create | POST | `{Entity}` |
| Update | PUT | `{Entity}/{id}` |
| Delete | DELETE | `{Entity}/{id}` |
| List related | GET | `{Entity}/{id}/{link}` |
| Link | POST | `{Entity}/{id}/{link}` |
| Unlink | DELETE | `{Entity}/{id}/{link}` |
| Mass update | POST | `{Entity}/action/massUpdate` |
| Mass delete | POST | `{Entity}/action/massDelete` |
| Stream/notes | GET | `{Entity}/{id}/stream` |
| Webhook CRUD | POST/DELETE | `Webhook` / `Webhook/{id}` |
| Auth token | GET | `App/user` |
| Attachment up | POST | `Attachment` |
| Attachment down | GET | `Attachment/file/{id}` |
| OpenAPI spec | GET | `OpenApi` |

---

## Filtering & Search

Parameters go as query params or as a single JSON-encoded `searchParams` param.

### Core Parameters

| Param | Type | Purpose |
|---|---|---|
| `select` | string | Comma-separated fields: `id,name,status` |
| `maxSize` | int | Records per page (max 200, default varies) |
| `offset` | int | Pagination offset |
| `orderBy` | string | Sort field |
| `order` | string | `asc` or `desc` |
| `where` | array | Filter conditions (see below) |
| `primaryFilter` | string | Named server-side filter (`open`, `onlyMy`, etc.) |
| `boolFilterList` | array | Boolean toggles: `["onlyMy", "followed"]` |

v9.0+ aliases (WAF-safe): `attributeSelect` for `select`, `whereGroup` for `where`.

### WHERE Operators

Each filter is `{"type": "...", "attribute": "...", "value": "..."}`. Multiple items in the `where` array are implicitly ANDed. Use `{"type": "or", "value": [...]}` for OR logic.

**Operator categories**: equality (`equals`, `notEquals`), comparison (`greaterThan`, `lessThan`, `greaterThanOrEquals`, `lessThanOrEquals`), null (`isNull`, `isNotNull`), boolean (`isTrue`, `isFalse`), string (`contains`, `notContains`, `startsWith`, `endsWith`, `like`, `notLike`), set (`in`, `notIn`), relationship (`linkedWith`, `notLinkedWith`, `isLinked`, `isNotLinked`), date helpers (`today`, `past`, `future`, `lastSevenDays`, `currentMonth`, `lastMonth`, `currentYear`, `between`, `lastXDays`, `nextXDays`), logical (`or`, `and`).

Full operator reference with examples: `references/where-operators.md`

---

## Relationships

Link names are visible at Administration > Entity Manager > {Entity} > Relationships (4th column).

### List Related Records
```
GET Account/{id}/contacts?select=id,name,emailAddress&maxSize=50
```
Same search params as list endpoint.

### Link Records
```
POST Account/{id}/contacts
{"id": "contactId"}
```

Multiple at once:
```json
{"ids": ["id1", "id2", "id3"]}
```

Mass relate by filter:
```json
{"massRelate": true, "where": [{"type": "equals", "attribute": "status", "value": "Active"}]}
```

### Unlink Records
```
DELETE Account/{id}/contacts
{"id": "contactId"}
```

Multiple: `{"ids": ["id1", "id2"]}`.

---

## Webhooks

### Register
```
POST Webhook
{"event": "Contact.create", "url": "https://your-server.com/hook"}
```
Returns `{"id": "webhookId", "secretKey": "generatedKey"}`. Save both for signature verification.

### Event Types
- `{Entity}.create` — record created (all attributes in payload)
- `{Entity}.update` — record updated (only changed attributes)
- `{Entity}.delete` — record removed (ID only)
- `{Entity}.fieldUpdate.{field}` — specific field changed

### Payload Format
Always an array (even for single events):
```json
[{"id": "abc123", "name": "Updated Name", "status": "Active"}]
```

### Signature Verification
The `Signature` header contains: `base64(webhookId + ':' + hmacSha256(rawBody, secretKey))`.

```php
$expected = base64_encode($webhookId . ':' . hash_hmac('sha256', $rawBody, $secretKey));
$valid = hash_equals($expected, $_SERVER['HTTP_SIGNATURE']);
```

### Lifecycle
- Processed by scheduled job "Process Webhook Queue" (default: every 5 min)
- Failed deliveries are retried automatically
- Persistent failures deactivate the webhook
- Config: `webhookAllowedAddressList` in `data/config.php` for internal URLs

### Delete
```
DELETE Webhook/{id}
```

---

## Mass Operations

### Mass Update
```
POST Lead/action/massUpdate
```

By IDs:
```json
{"ids": ["id1", "id2"], "data": {"assignedUserId": "userId", "status": "In Process"}}
```

By filter:
```json
{"where": [{"type": "equals", "attribute": "status", "value": "New"}], "data": {"status": "Assigned"}}
```

### Mass Delete
```
POST Lead/action/massDelete
```
Same payload patterns — `ids` array or `where` filter.

### No Bulk Create
There is no native batch create endpoint. For bulk ingestion:
1. Loop individual POST requests with reasonable pacing
2. Use the built-in Import feature (Administration > Import) for CSV
3. Write a custom API action for batch processing if volume demands it

### Important
API Before-Save Scripts (Formula) are **not executed** during mass update operations.

---

## Error Handling

### Status Codes

| Code | Meaning | Action |
|---|---|---|
| 200 | Success | — |
| 400 | Bad Request | Check required fields, validation |
| 401 | Unauthorized | Check auth headers/credentials |
| 403 | Forbidden | Check API User role/ACL |
| 404 | Not Found | Record doesn't exist or no read access |
| 409 | Conflict | Duplicate detected or record locked |
| 500 | Server Error | Check `data/log` on server |

### Error Details
Error reason is in the `X-Status-Reason` response header (not always in the body).

### Duplicate Detection (409)
```json
{"reason": "Duplicate", "data": {"idList": ["existingId1"]}}
```
Bypass with `X-Skip-Duplicate-Check: true` header.

---

## Performance Best Practices

1. **Select only needed fields** — `?select=id,name,status` avoids loading all attributes
2. **Skip total count** — `X-No-Total: true` header skips the COUNT query on list requests
3. **Paginate** — use `offset` + `maxSize` (keep maxSize at 50-100)
4. **Use primary filters** — server-optimized named filters are faster than complex WHERE
5. **Minimal API User roles** — dedicated API users with only required scopes
6. **No native rate limiter** — implement at reverse proxy level (nginx, Apache) if needed
7. **OpenAPI spec** — `GET OpenApi` returns full schema for your instance including custom entities (v9.3+, admin only)

---

## Client Libraries

### PHP (Official — Preferred)

`composer require espocrm/php-espo-api-client`

Class: `Espo\ApiClient\Client`. Constructor takes base URL. Auth via `setApiKey()` or `setApiKey()` + `setSecretKey()` for HMAC. All requests through `$client->request(METHOD, path, params, payload)`.

### Node.js

No official npm package. Build a thin client around `fetch` with:
- Base URL + `/api/v1/` prefix
- `X-Api-Key` header (or compute HMAC per-request)
- `Content-Type: application/json`
- Search params as JSON-encoded `searchParams` query param
- Error extraction from `X-Status-Reason` header on non-2xx responses

---

## Field Types & API Representation

| Field Type | JSON Type | Example |
|---|---|---|
| varchar | string | `"name": "Test"` |
| text | string | `"description": "Long text"` |
| int | number | `"quantity": 5` |
| float | number | `"rate": 4.5` |
| boolean | boolean | `"isActive": true` |
| enum | string | `"status": "New"` |
| multiEnum | string[] | `"tags": ["A", "B"]` |
| date | string | `"closeDate": "2025-06-15"` |
| datetime | string (UTC) | `"createdAt": "2025-06-15 14:30:00"` |
| currency | number + string | `"amount": 1000, "amountCurrency": "USD"` |
| link | string (ID) | `"accountId": "someId"` |
| linkMultiple | string[] + object | `"teamsIds": ["id1"], "teamsNames": {"id1": "Sales"}` |
| email | string | `"emailAddress": "test@example.com"` |
| phone | string | `"phoneNumber": "+1234567890"` |
| address | multiple fields | `"billingAddressStreet": "123 Main", "billingAddressCity": "NYC"` |
| file | string (ID) | `"fileId": "attachmentId"` |

All datetime values are UTC. Date format: `YYYY-MM-DD`. Datetime: `YYYY-MM-DD HH:mm:ss`.
