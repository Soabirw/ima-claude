---
name: "discourse"
description: "Discourse plugin development - plugin.rb, after_initialize, admin routes, Guardian auth, security patterns"
---

# Discourse Plugin Development

Discourse plugins are Rails engines with conventions. Work with the framework — its plugin API, Guardian authorization system, and event hooks exist for good reason.

## When to Use This Skill

- Building or modifying Discourse plugins
- Adding admin UI to a Discourse plugin
- Implementing authentication hooks or user lifecycle extensions
- Migrating data into Discourse (import scripts)
- Reviewing Discourse plugin security

## Core Philosophy

> Discourse plugins are Rails. Discourse adds its own authorization layer (Guardian). Respect both.

- **`after_initialize`** is where plugin logic wires into Discourse
- **Guardian** is the authorization layer — every action checks it
- **Plugin API** hooks (`register_*`, `add_*`) are the extension points — don't monkey-patch core
- **StaffConstraint** protects admin routes — use it, never roll your own
- **RuboCop** is enforced — Discourse ships lint rules

**Foundation**: Reference `../rails/SKILL.md` for Rails security practices and `../ruby-fp/SKILL.md` for Ruby patterns.

## Plugin Structure

```
my-plugin/
├── plugin.rb               # Manifest + bootstrap (required)
├── about.json              # Metadata for admin panel
├── app/
│   ├── controllers/
│   │   └── admin/
│   │       └── my_plugin_controller.rb
│   ├── models/
│   │   └── my_plugin_record.rb
│   └── serializers/
│       └── my_plugin_serializer.rb
├── config/
│   ├── locales/
│   │   └── server.en.yml
│   └── settings.yml        # Site settings
├── db/
│   └── migrate/
│       └── 20250101000000_create_my_plugin.rb
├── assets/
│   └── javascripts/
│       └── admin/          # Ember components for admin UI
├── lib/
│   └── my_plugin/          # Pure logic (no Discourse deps)
└── spec/
    └── plugin_helper.rb
```

## plugin.rb: Manifest + Bootstrap

```ruby
# frozen_string_literal: true

# name: my-plugin
# about: Brief plugin description
# version: 1.0.0
# authors: Your Name
# url: https://github.com/yourorg/my-plugin

# Autoloading — define module first, then require engine
module ::MyPlugin
  PLUGIN_NAME = "my-plugin"
end

require_relative "lib/my_plugin/engine"

# All wiring happens inside after_initialize
after_initialize do
  # Register settings, hooks, extensions here
  # This runs after Discourse core is fully loaded
end
```

## after_initialize: The Plugin Entry Point

```ruby
after_initialize do
  # Extend models — use class_eval in after_initialize, not top-level monkey-patches
  User.class_eval do
    has_one :my_plugin_profile, dependent: :destroy
  end

  # Register custom fields
  register_post_custom_field_type('wp_original_id', :integer)
  register_topic_custom_field_type('imported_from', :string)

  # Wire into Discourse events (preferred over overriding methods)
  on(:user_created) do |user|
    MyPlugin::UserSetup.call(user)
  end

  on(:post_created) do |post, opts, user|
    MyPlugin::PostSync.call(post, user)
  end

  # Add serializer extensions
  add_to_serializer(:user, :wp_user_id) do
    object.custom_fields['wp_user_id']
  end
end
```

## Admin Routes + Controller

Every admin route needs `StaffConstraint` — never expose admin actions without it.

```ruby
# In plugin.rb — register the admin nav link
add_admin_route 'my_plugin.title', 'my-plugin'

# Wire the route
Discourse::Application.routes.append do
  get '/admin/plugins/my-plugin' => 'admin/my_plugin#index',
      constraints: StaffConstraint.new
  post '/admin/plugins/my-plugin/action' => 'admin/my_plugin#action',
      constraints: StaffConstraint.new
end
```

```ruby
# app/controllers/admin/my_plugin_controller.rb
# frozen_string_literal: true

class ::Admin::MyPluginController < ::Admin::AdminController
  # Admin::AdminController already requires:
  # - User is logged in
  # - User is staff (moderator or admin)
  # For admin-only actions, add:
  before_action :ensure_admin, only: [:dangerous_action]

  def index
    render json: {
      stats: MyPlugin::Stats.summary,
      settings: SiteSetting.my_plugin_enabled
    }
  end

  def action
    # Strong parameters for any mutating action
    attrs = params.require(:my_plugin).permit(:field_one, :field_two)
    result = MyPlugin::SomeService.call(attrs.to_h.symbolize_keys)

    if result.success?
      render json: { success: true, data: result.data }
    else
      render json: { success: false, errors: result.errors }, status: :unprocessable_entity
    end
  end
end
```

## Guardian: Authorization Layer

Guardian is Discourse's authorization system. Always check it for user-facing actions.

```ruby
# Check permissions before acting
def update_post
  post = Post.find(params[:id])

  # guardian.can_edit_post? checks ownership, trust level, staff status
  unless guardian.can_edit_post?(post)
    return render json: failed_json, status: :forbidden
  end

  post.update!(body: params[:body])
  render json: PostSerializer.new(post, scope: guardian).as_json
end

# Extending Guardian for plugin-specific permissions
# In after_initialize:
module ::Guardian::MyPluginExtensions
  def can_use_my_feature?
    authenticated? && (is_staff? || user.trust_level >= 2)
  end
end

Guardian.prepend(::Guardian::MyPluginExtensions)
```

## Security Non-Negotiables

### 1. Never Raw SQL with Interpolation — Use ActiveRecord or Named Params

```ruby
# BAD — SQL injection
User.where("username = '#{params[:username]}'")
DB.query("SELECT * FROM users WHERE id = #{user_id}")

# GOOD — ActiveRecord parameterization
User.where(username: params[:username])
User.where("created_at > ?", params[:since])

# GOOD — Discourse DB helper with named bind params (always use this for raw SQL)
DB.query("SELECT * FROM users WHERE id = :id", id: user_id.to_i)
DB.query("UPDATE users SET flag = TRUE WHERE id = :id", id: user_id.to_i)
```

### 2. Staff-Only Admin Routes

```ruby
# ALWAYS use StaffConstraint on admin routes
get '/admin/plugins/my-plugin' => 'admin/my_plugin#index',
    constraints: StaffConstraint.new

# Admin::AdminController gives you these checks automatically:
# - ensure_logged_in
# - ensure_staff
# For admin-only (not just moderator), add ensure_admin
```

### 3. No Sensitive Data in Logs

```ruby
# BAD — logs hash values, tokens, passwords
Rails.logger.warn("[MyPlugin] Processing hash: #{user_hash}")
Rails.logger.info("[MyPlugin] Token: #{token}")

# GOOD — log what happened, not the sensitive value
Rails.logger.info("[MyPlugin] Processing user #{user.id}")
Rails.logger.warn("[MyPlugin] Auth failed for user #{user.id}")
```

### 4. Custom Fields — Validate Types

```ruby
# Register field types to prevent type confusion
register_user_custom_field_type('my_plugin_id', :integer)
register_post_custom_field_type('source_url', :string)

# Whitelist custom fields for API/serializer exposure
DiscoursePluginRegistry.serialized_current_user_fields << 'my_plugin_id'

# Access safely — always coerce type
user_id = (user.custom_fields['my_plugin_id'].to_i rescue nil)
```

### 5. Rate Limiting on Sensitive Endpoints

```ruby
# For endpoints that test credentials or perform expensive operations
RateLimiter.new(current_user, "my_plugin_sensitive_action", 5, 1.minute).performed!
# Raises RateLimiter::LimitExceeded if over limit
```

## Site Settings

```yaml
# config/settings.yml
plugins:
  my_plugin_enabled:
    default: false
    client: false  # server-side only unless UI needs it
  my_plugin_max_items:
    default: 100
    min: 1
    max: 1000
    type: integer
```

```ruby
# Access in code
SiteSetting.my_plugin_enabled
SiteSetting.my_plugin_max_items

# Guard features
return unless SiteSetting.my_plugin_enabled
```

## Migrations

```ruby
# db/migrate/20250101000000_create_my_plugin_records.rb
# frozen_string_literal: true

class CreateMyPluginRecords < ActiveRecord::Migration[7.0]
  def change
    create_table :my_plugin_records do |t|
      t.integer :user_id, null: false
      t.string :source_id, null: false
      t.text :data
      t.timestamps
    end

    add_index :my_plugin_records, :user_id
    add_index :my_plugin_records, :source_id, unique: true
    add_foreign_key :my_plugin_records, :users
  end
end
```

## Import Script Pattern (Standalone Ruby)

Import scripts inherit from `ImportScripts::Base` and run outside the Rails request cycle.

```ruby
# frozen_string_literal: true

require_relative "base"

class ImportScripts::MyImport < ImportScripts::Base
  def initialize
    super
    @client = Mysql2::Client.new(
      host: ENV.fetch('SOURCE_DB_HOST'),
      username: ENV.fetch('SOURCE_DB_USER'),
      password: ENV.fetch('SOURCE_DB_PASSWORD'),
      database: ENV.fetch('SOURCE_DB_NAME')
    )
  end

  def perform
    import_users
    import_categories
    import_posts
  end

  private

  def import_users
    puts "Importing users..."

    # Parameterized query — never interpolate
    users = @client.query(
      "SELECT id, email, username, display_name FROM wp_users WHERE user_status = 0",
      as: :hash
    )

    create_users(users) do |user|
      {
        id: user['id'],
        email: user['email'],
        username: normalize_username(user['username']),
        name: user['display_name']
      }
    end
  end

  def normalize_username(raw)
    # Pure function — transform only, no side effects
    raw.to_s.strip.downcase.gsub(/[^a-z0-9_]/, '_').truncate(20)
  end
end

ImportScripts::MyImport.new.perform
```

## Testing

```ruby
# spec/plugin_helper.rb — loads Discourse test env
require 'rails_helper'

# spec/requests/admin/my_plugin_spec.rb
RSpec.describe Admin::MyPluginController do
  fab!(:admin) { Fabricate(:admin) }
  fab!(:user)  { Fabricate(:user) }

  before { sign_in(admin) }

  describe "GET #index" do
    it "returns success for admin" do
      get "/admin/plugins/my-plugin.json"
      expect(response.status).to eq(200)
    end
  end

  describe "authorization" do
    it "rejects non-staff" do
      sign_in(user)
      get "/admin/plugins/my-plugin.json"
      expect(response.status).to eq(404)  # Discourse returns 404 for staff routes
    end
  end
end

# Pure logic specs — no Discourse dependencies
RSpec.describe MyPlugin::UserSetup do
  describe ".call" do
    it "normalizes username" do
      expect(described_class.normalize("John Doe!")).to eq("john_doe_")
    end
  end
end
```

## Security Checklist

- [ ] `StaffConstraint.new` on all admin routes
- [ ] Inherited from `Admin::AdminController` for admin endpoints
- [ ] Strong parameters on all mutating endpoints
- [ ] No string interpolation in SQL — use ActiveRecord or `DB.query` with `:named` params
- [ ] `guardian.can_*?` checked before user-facing mutations
- [ ] No sensitive values (tokens, hashes, passwords) in log output
- [ ] Rate limiting on credential-testing or expensive endpoints
- [ ] Custom field types registered (`register_*_custom_field_type`)
- [ ] Site settings used for feature flags, not hardcoded booleans

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Monkey-patching Discourse classes | Use `class_eval` / `prepend` in `after_initialize` |
| Direct DB string interpolation | `DB.query("... WHERE id = :id", id: val)` |
| Checking `current_user.staff?` in controller | Inherit `Admin::AdminController` instead |
| Logging `user.password_hash` for debugging | Log `user.id` only |
| `params[:field]` without strong params | Always `params.require().permit()` |
| Hardcoded credentials in plugin.rb | `ENV.fetch('KEY')` or Rails credentials |

## When to Load Reference Files

### Security Examples
**File**: [`references/security.md`](references/security.md)
**Load when**: Implementing auth hooks, custom Guardian checks, SQL safety in import scripts
**Contains**: Guardian extension patterns, DB.query vs ActiveRecord, rate limiting, log hygiene

### Admin UI (Ember)
**File**: [`references/admin-ui.md`](references/admin-ui.md)
**Load when**: Building admin panel Ember components
**Contains**: Route setup, Ember component patterns, REST adapter, admin nav

### Import Scripts
**File**: [`references/import-scripts.md`](references/import-scripts.md)
**Load when**: Writing data migration scripts
**Contains**: ImportScripts::Base lifecycle, batching, lookup maps, resume/idempotency

---

**Evidence Base**: Discourse Developer Docs, Discourse GitHub (discourse-solved, discourse-data-explorer), Discourse CVE history (2024–2026), Rails Security Guide.
