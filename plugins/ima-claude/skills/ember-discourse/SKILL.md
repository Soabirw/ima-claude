---
name: "ember-discourse"
description: "Ember/Glimmer component development for Discourse plugins - gjs, apiInitializer, plugin outlets, @tracked, @service, admin UI"
---

# Ember for Discourse Plugins

Discourse runs Ember Octane with Glimmer components. The plugin extension model is: `apiInitializer` → `renderInOutlet` → `.gjs` component. Everything else is either legacy or an internal Discourse concern.

## When to Use This Skill

- Adding frontend UI to a Discourse plugin
- Building admin panel components for a plugin
- Injecting content into Discourse's UI via plugin outlets
- Migrating old `decorateWidget` / raw handlebars to modern Glimmer

## Core Philosophy

> Glimmer components are close to pure functions: `(args, services) → template`. Minimize `@tracked` state. Prefer derived values over stored state.

FP lens applied to Ember:
- **Components** are view functions — args in, DOM out
- **`@tracked`** is isolated reactive state — use sparingly, only what truly changes
- **Derived values** via getters — no duplicate state, always in sync
- **Actions** are the imperative shell — side effects live in methods, not templates
- **Services** are dependency injection — inject, don't import singletons

**Foundation**: Reference `../discourse/SKILL.md` for the Ruby side of plugin development.

## The Modern Stack (use these)

| What | Modern | Deprecated / Avoid |
|------|--------|--------------------|
| File format | `.gjs` (Glimmer JS) | `.hbs` + `.js` pairs, `.hbr`, `.raw.hbs` |
| Entry point | `apiInitializer` | bare `withPluginApi` initializer export |
| Inject into UI | `api.renderInOutlet` | `registerConnectorClass`, `decorateWidget` |
| Component base | `@glimmer/component` | `@ember/component` (classic) |
| Reactive state | `@tracked` | `Ember.set()`, `this.set()` |
| Services | `@service` decorator | `Ember.inject.service()` |
| Event handling | `{{on "click" this.handler}}` | `{{action "handler"}}` |

## .gjs: The File Format

`.gjs` (Glimmer JS) combines the component class and template in one file. It's the current Discourse standard for new components.

```gjs
// assets/javascripts/discourse/components/my-component.gjs
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { action } from "@ember/object";
import { service } from "@ember/service";
import DButton from "discourse/components/d-button";

export default class MyComponent extends Component {
  @service currentUser;
  @service siteSettings;

  @tracked isExpanded = false;

  // Derived value — getter, not stored state
  get greeting() {
    return this.currentUser
      ? `Welcome back, ${this.currentUser.username}!`
      : "Welcome to our community!";
  }

  @action
  toggleExpanded() {
    this.isExpanded = !this.isExpanded;
  }

  <template>
    <div class="my-component">
      <p>{{this.greeting}}</p>

      <DButton
        @action={{this.toggleExpanded}}
        @label={{if this.isExpanded "collapse" "expand"}}
      />

      {{#if this.isExpanded}}
        <div class="my-component__body">
          {{yield}}
        </div>
      {{/if}}
    </div>
  </template>
}
```

### Template-only component (no JS needed)

```gjs
// When a component is purely presentational — no class required
<template>
  <div class="badge-card">
    <img src={{@badge.image_url}} alt={{@badge.name}} />
    <span>{{@badge.name}}</span>
  </div>
</template>
```

## apiInitializer: The Plugin Entry Point

Every plugin's JS starts here. One initializer file per plugin feature area.

```javascript
// assets/javascripts/discourse/initializers/my-plugin.js
import { apiInitializer } from "discourse/lib/api";
import MyBanner from "../components/my-banner";
import MyComponent from "../components/my-component";

export default apiInitializer((api) => {
  // Render into a plugin outlet
  api.renderInOutlet("discovery-list-container-top", MyBanner);

  // shouldRender on the component class controls conditional rendering
  api.renderInOutlet("topic-above-post-stream", MyComponent);
});
```

## Plugin Outlets: Where to Inject Content

Plugin outlets are pre-defined hooks in Discourse's templates. Use `api.renderInOutlet` to inject at them.

```gjs
// assets/javascripts/discourse/components/my-banner.gjs
import Component from "@glimmer/component";
import { service } from "@ember/service";

export default class MyBanner extends Component {
  @service currentUser;

  // Static method controls whether this component renders at all.
  // outletArgs contains context from where the outlet sits in the DOM.
  static shouldRender(outletArgs, helper) {
    return helper.siteSettings.my_plugin_enabled && helper.currentUser;
  }

  <template>
    <div class="my-banner">
      Welcome, {{this.currentUser.username}}!
    </div>
  </template>
}
```

### Post stream outlets (Glimmer post stream — current)

```gjs
import Component from "@glimmer/component";
import { apiInitializer } from "discourse/lib/api";

export default apiInitializer((api) => {
  api.renderAfterWrapperOutlet(
    "post-content-cooked-html",
    class extends Component {
      static shouldRender(args) {
        return args.post.wiki;  // args.post is the current post model
      }

      <template>
        <div class="wiki-notice">This post is a wiki</div>
      </template>
    }
  );
});
```

### Finding outlet names

Search Discourse core for `<PluginOutlet @name=`:
```bash
rg '<PluginOutlet @name=' app/assets/javascripts/discourse/
```

Common outlets: `discovery-list-container-top`, `topic-above-post-stream`,
`above-main-container`, `header-icons`, `user-profile-primary`,
`post-content-cooked-html`, `after-topic-list-area`.

## Glimmer Component Patterns

### Args vs State

```gjs
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class UserCard extends Component {
  // @tracked — only for state THIS component owns and mutates
  @tracked showDetails = false;

  // Derived from args — a getter, never @tracked
  get displayName() {
    return this.args.user.name || this.args.user.username;
  }

  get isStaff() {
    return this.args.user.staff;
  }

  <template>
    <div class="user-card {{if this.isStaff 'user-card--staff'}}">
      <h3>{{this.displayName}}</h3>
      {{#if this.showDetails}}
        <p>{{@user.bio_raw}}</p>
      {{/if}}
    </div>
  </template>
}
```

### Services — inject, don't import

```gjs
import Component from "@glimmer/component";
import { service } from "@ember/service";

export default class MyFeature extends Component {
  // Common Discourse services
  @service currentUser;       // logged-in user (null if anonymous)
  @service siteSettings;      // site configuration
  @service router;            // programmatic navigation
  @service store;             // Ember Data store
  @service session;           // session data
  @service modal;             // open modals
  @service toasts;            // toast notifications (Discourse 3.2+)

  get canUseFeature() {
    return this.currentUser?.trust_level >= 2
      && this.siteSettings.my_plugin_enabled;
  }

  <template>
    {{#if this.canUseFeature}}
      ...
    {{/if}}
  </template>
}
```

### Actions and events

```gjs
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { action } from "@ember/object";

export default class SearchBox extends Component {
  @tracked query = "";
  @tracked results = [];

  @action
  updateQuery(event) {
    this.query = event.target.value;
  }

  @action
  async search() {
    if (!this.query.trim()) return;
    // side effects belong in @action methods, not in getters or templates
    this.results = await this.args.onSearch(this.query);
  }

  <template>
    <input
      type="text"
      value={{this.query}}
      {{on "input" this.updateQuery}}
    />
    <button type="button" {{on "click" this.search}}>Search</button>
  </template>
}
```

## Admin UI Components

Admin components live in the `admin/` asset tree and use the same Glimmer patterns.

```
assets/javascripts/
├── discourse/
│   └── initializers/
│       └── my-plugin.js          # user-facing outlets
└── admin/
    ├── components/
    │   └── my-plugin-admin.gjs   # admin panel component
    └── routes/
        └── admin-plugins-my-plugin.js
```

```gjs
// assets/javascripts/admin/components/my-plugin-admin.gjs
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { ajax } from "discourse/lib/ajax";
import { popupAjaxError } from "discourse/lib/ajax-error";
import DButton from "discourse/components/d-button";
import LoadingSpinner from "discourse/components/loading-spinner";

export default class MyPluginAdmin extends Component {
  @service currentUser;

  @tracked stats = null;
  @tracked isLoading = false;

  @action
  async loadStats() {
    this.isLoading = true;
    try {
      const response = await ajax("/admin/plugins/my-plugin.json");
      this.stats = response.stats;
    } catch (error) {
      popupAjaxError(error);
    } finally {
      this.isLoading = false;
    }
  }

  <template>
    <div class="my-plugin-admin">
      <h2>My Plugin Admin</h2>

      {{#if this.isLoading}}
        <LoadingSpinner />
      {{else if this.stats}}
        <p>Total users: {{this.stats.total_users}}</p>
        <p>Pending: {{this.stats.pending}}</p>
      {{/if}}

      <DButton
        @action={{this.loadStats}}
        @label="my_plugin.admin.load_stats"
        @disabled={{this.isLoading}}
      />
    </div>
  </template>
}
```

## AJAX: Talking to the Plugin Backend

```javascript
import { ajax } from "discourse/lib/ajax";
import { popupAjaxError } from "discourse/lib/ajax-error";

// GET
const data = await ajax("/my-plugin/endpoint.json");

// POST — Discourse's ajax helper automatically includes the CSRF token
const result = await ajax("/my-plugin/action", {
  type: "POST",
  data: { user_id: userId, value: someValue }
});

// Always handle errors with popupAjaxError for consistent UX
try {
  await ajax("/my-plugin/action", { type: "DELETE" });
} catch (e) {
  popupAjaxError(e);
}
```

**Always use `discourse/lib/ajax`, never raw `fetch`.** The helper handles CSRF tokens, error formatting, and Discourse session state automatically.

## Security in Ember

### Client checks are UX only — backend enforces everything

```javascript
// Hiding/showing UI based on role is fine:
get showAdminTools() {
  return this.currentUser?.admin;
}

// But the BACKEND must enforce the same check on every request.
// Client-side auth is trivially bypassed in browser devtools.
// There is no such thing as client-side security.
```

### No raw HTML injection with user content

```handlebars
{{!-- Safe — Glimmer auto-escapes output --}}
{{user.bio}}

{{!-- Unsafe — raw output, skip escaping only for server-sanitized HTML --}}
{{! avoid triple-mustache with user-supplied content }}

{{!-- For server-sanitized post content, Discourse provides: --}}
<div>{{html-safe post.cooked}}</div>
```

### Content Security Policy

Discourse enforces CSP strictly. These patterns will break or be blocked:
- Inline `<script>` tags in plugin templates
- Dynamic code evaluation (`eval`, dynamic code strings)
- Modifying `innerHTML` directly — use Glimmer templates instead
- Importing from external CDNs — bundle or use Discourse's asset pipeline

## Deprecations to Actively Avoid

```javascript
// DEPRECATED — old connector class pattern (shows deprecation warning)
api.registerConnectorClass("outlet-name", "connector-name", {
  setupComponent(args, component) { ... }
});

// DEPRECATED — widget system (actively being removed in 2025/2026)
api.decorateWidget("post:after", (helper) => { ... });
api.createWidget("my-widget", { ... });

// DEPRECATED — raw handlebars files (.hbr, .raw.hbs)
// Breaks with the Glimmer topic list (enabled by default 2025)

// DEPRECATED — classic component base class
import Component from "@ember/component";  // use @glimmer/component instead

// DEPRECATED — Ember object mutation helpers
this.set("myProp", value);  // use @tracked + direct assignment: this.myProp = value
Ember.set(obj, "key", val); // same — direct assignment or @tracked
```

## File Naming and Location

```
assets/javascripts/discourse/
├── initializers/
│   └── my-plugin.js           # apiInitializer — one per feature area
├── components/
│   ├── my-feature.gjs         # kebab-case filenames
│   └── my-other-thing.gjs
└── lib/
    └── my-utils.js            # pure helpers, no Ember dependency

assets/javascripts/admin/
├── components/
│   └── admin-my-plugin.gjs    # admin components prefix with "admin-"
└── routes/
    └── admin-plugins-my-plugin.js
```

## Practical Checklist

- [ ] Using `.gjs` (not `.hbs`/`.js` pairs) for new components
- [ ] Entry point is `apiInitializer`, not a bare `withPluginApi` export
- [ ] Plugin outlets via `api.renderInOutlet` — not `decorateWidget`
- [ ] `@tracked` only for state the component owns — not derived values
- [ ] Derived values are getters, not `@tracked` properties
- [ ] Services injected via `@service` — not imported as singletons
- [ ] AJAX via `discourse/lib/ajax` — not raw `fetch`
- [ ] Errors handled with `popupAjaxError`
- [ ] No raw HTML output with user-supplied content
- [ ] Backend enforces all authorization — client checks are UI-only

## Quick Reference: Common Imports

```javascript
// Glimmer/Ember core
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { action } from "@ember/object";
import { service } from "@ember/service";

// Discourse plugin API
import { apiInitializer } from "discourse/lib/api";
import { ajax } from "discourse/lib/ajax";
import { popupAjaxError } from "discourse/lib/ajax-error";

// Discourse components
import DButton from "discourse/components/d-button";
import LoadingSpinner from "discourse/components/loading-spinner";
import DModal from "discourse/components/d-modal";

// i18n
import { i18n } from "discourse-i18n";   // current (replaces the old I18n.t())
```

## When to Load Reference Files

### Admin UI Patterns
**File**: [`references/admin-ui.md`](references/admin-ui.md)
**Load when**: Building admin routes, tables, forms, settings UI
**Contains**: Full admin route + component example, admin table patterns, settings form

### Plugin Outlet Reference
**File**: [`references/outlets.md`](references/outlets.md)
**Load when**: Need to find the right outlet or understand outletArgs context
**Contains**: Common outlet names, outletArgs by context, shouldRender patterns

---

**Evidence Base**: Discourse Developer Docs (2025), Discourse Meta dev posts (Glimmer post stream migration Q1 2025, topic list migration), Ember Octane Guides, Discourse CVE history.
