---
name: "espocrm"
description: >-
  EspoCRM skill family router. Detects intent (API calls, extension development,
  UI customization) and routes to the appropriate child skill. Provides shared
  context: v9.x target, entity-based REST architecture, Salesforce mental model
  mapping. Use when: any EspoCRM work, CRM integration, CRM API, EspoCRM
  customization. Triggers on: EspoCRM, Espo, CRM API, CRM integration, CRM
  entity, CRM webhook, CRM hook.
---

# EspoCRM - Skill Family Router

Routes EspoCRM work to the right child skill based on intent.

**Target version**: v9.x (9.0+)
**Architecture**: Entity-based REST API, PHP backend, Backbone.js frontend

## Decision Tree

```
What are you doing with EspoCRM?
├── REST API calls (external integration)?
│   → espocrm-api (primary) + php-fp or js-fp-api
│   → Auth, CRUD, filtering, webhooks, mass ops
│
├── PHP extension development (hooks, services, custom entities)?
│   → espocrm-extensions (Phase 2) + php-fp
│   → ORM, hooks, services, DI, custom controllers, modules
│
├── Frontend/UI customization (views, fields, layouts)?
│   → espocrm-ui (Phase 3)
│   → Backbone views, Espo.Ajax, Handlebars templates
│
└── Not sure / mixed?
    → Start with espocrm-api for data access
    → Route to extension/UI skill once scope is clear
```

## Shared Context

### Entity-Based Model
EspoCRM organizes data as **Entity Types** (Account, Contact, Lead, Opportunity, custom types). Every entity type gets automatic REST endpoints. Custom entities created via Entity Manager are immediately API-accessible.

### Salesforce Mental Model
For developers familiar with Salesforce, this mapping accelerates onboarding:

| Salesforce | EspoCRM |
|---|---|
| sObject | Entity Type |
| Connected App + OAuth | API User + API Key |
| SOQL | WHERE JSON filters + select/orderBy params |
| SOSL | Text filter on list endpoint |
| Apex Trigger | PHP Hook (beforeSave, afterSave) |
| Apex REST endpoint | Custom API Action (Controller + routes.json) |
| LWC / Visualforce | Custom Views (JS, extending base views) |
| Platform Events / CDC | Webhooks ({Entity}.create, .update, .delete) |
| Bulk API 2.0 | No equivalent (loop individual calls or use Import) |
| Governor Limits | None (self-hosted, you manage resources) |
| AppExchange | EspoCRM Extensions marketplace |

### Key Differences from Salesforce
- **No SOQL** — queries use structured JSON WHERE filters (verbose but explicit)
- **No Bulk API** — mass operations exist (massUpdate, massDelete) but no batch create
- **No Composite API** — one request per operation
- **No governor limits** — self-hosted, manage at server/proxy level
- **Simpler auth** — API Key in one header vs. multi-step OAuth
- **Metadata is JSON files** — no deployment steps, changes take effect on cache clear

### Documentation Lookup
Use Context7 for live EspoCRM docs: `resolve-library-id("espocrm")` resolves to `/espocrm/documentation`.

## Child Skill Status

| Skill | Status | Covers |
|---|---|---|
| `espocrm-api` | Active | REST API, auth, CRUD, filtering, webhooks, mass ops |
| `espocrm-extensions` | Planned | PHP hooks, services, ORM, custom entities, modules |
| `espocrm-ui` | Planned | JS views, fields, Espo.Ajax, Backbone, Handlebars |
