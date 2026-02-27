---
name: "rails"
description: "Ruby on Rails conventions + security - strong parameters, ActiveRecord safety, CSRF, auth, secrets management"
---

# Rails

Convention-over-configuration development on the happy path, with security non-negotiables that prevent the most common Rails vulnerabilities.

## When to Use This Skill

- Building Rails controllers, models, services
- Reviewing Rails code for security or structure
- Adding features to an existing Rails application
- Discourse plugin development (see also `discourse` skill)

## Core Philosophy

Rails has opinions. Work with them, not against them. The framework gives you:
- SQL injection protection via ActiveRecord (use it)
- CSRF protection by default (don't disable it)
- XSS protection via ERB auto-escaping (use `<%= %>`)
- Mass assignment protection via Strong Parameters (permit explicitly)

**Functional core still applies in Rails.** Business logic in service modules/plain Ruby objects. Keep models and controllers thin.

**Foundation**: Reference `../ruby-fp/SKILL.md` for Ruby FP core principles.

## The 5 Non-Negotiable Security Practices

| Practice | Prevents | Rule |
|----------|----------|------|
| **Strong Parameters** | Mass assignment | `params.require(:model).permit(:field, ...)` on ALL controller actions |
| **Parameterized Queries** | SQL injection | ActiveRecord methods or `?`/named placeholders — NEVER string interpolation |
| **CSRF Protection** | CSRF | Never disable `protect_from_forgery`; use `form_with` helpers |
| **Before Actions (Auth)** | Unauthorized access | `before_action :authenticate_user!` or equivalent on ALL sensitive actions |
| **Secrets via Credentials** | Credential exposure | Rails credentials or ENV — never hardcode secrets in source |

### Quick Reference: The Five in Code

```ruby
# 1. Strong Parameters
def user_params
  params.require(:user).permit(:name, :email, :bio)
  # Never: params[:user]  or  params.permit!
end

# 2. Parameterized Queries — ActiveRecord keeps you safe
User.where(email: params[:email])                          # safe
User.where("email = ?", params[:email])                    # safe
User.where("email = :email", email: params[:email])        # safe
User.where("email = '#{params[:email]}'")                  # NEVER — SQL injection

# 3. CSRF — keep default, use form helpers
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception  # default — keep it
end
# form_with and form_for automatically include the token

# 4. Before action auth
class PostsController < ApplicationController
  before_action :authenticate_user!          # Devise
  before_action :require_admin, only: [:destroy]

  private
  def require_admin
    redirect_to root_path unless current_user&.admin?
  end
end

# 5. Credentials — never hardcode
# config/credentials.yml.enc (encrypted)
# Access: Rails.application.credentials.stripe[:secret_key]
# ENV fallback: ENV.fetch('STRIPE_SECRET_KEY')
```

## ActiveRecord Safety

```ruby
# SAFE — all these use parameterization internally
User.find(params[:id])                     # auto-cast to integer
User.find_by(email: params[:email])
User.where(status: params[:status])
User.where("created_at > ?", 1.week.ago)

# SAFE — sanitize_sql_like for LIKE patterns
query = ActiveRecord::Base.sanitize_sql_like(params[:search])
User.where("name LIKE ?", "%#{query}%")

# UNSAFE — never do these
User.where("id = #{params[:id]}")          # SQL injection
User.where("name LIKE '%#{params[:q]}%'")  # SQL injection
User.find_by("email = '#{email}'")         # SQL injection

# Raw SQL when needed — use sanitize or bind params
User.find_by_sql(["SELECT * FROM users WHERE token = ?", token])
ActiveRecord::Base.connection.execute(
  ActiveRecord::Base.sanitize_sql(["UPDATE users SET x = ? WHERE id = ?", val, id])
)
```

## Mass Assignment

```ruby
# BAD — never permit all, never skip permit
User.new(params[:user])           # bypasses strong params
User.update(params.permit!)       # permits everything — dangerous

# GOOD — explicit whitelist
def user_params
  params.require(:user).permit(:name, :email, :bio)
end

# Nested params
def post_params
  params.require(:post).permit(:title, :body, tags: [], author: [:name, :email])
end

# Never permit sensitive fields
# role, admin, password_digest, confirmed_at — set these explicitly in code
def promote_to_admin
  @user.update!(role: 'admin')  # explicit, not from params
end
```

## XSS in Views

```ruby
# ERB auto-escaping — always use <%= %> for user content
<%= user.name %>           # safe — HTML-escaped
<%== user.name %>          # UNSAFE — raw output, HTML injection risk
<%= raw user.name %>       # UNSAFE — same as above
<%= user.name.html_safe %> # UNSAFE — marking untrusted content safe

# When you need to render HTML you control
<%= sanitize user.bio, tags: %w[b i em strong p] %>

# JavaScript context — never interpolate directly
<script>var name = "<%= user.name %>"</script>  # UNSAFE — XSS via JS
# GOOD
<script>var data = <%= user.to_json.html_safe %></script>  # if you control the data
# BEST — pass via data attributes
<div data-user-name="<%= user.name %>"></div>
```

## Authentication & Authorization Pattern

```ruby
# Authentication — Devise is the Rails default
# Before action guards all sensitive routes
class ApplicationController < ActionController::Base
  before_action :authenticate_user!

  # Override to allow public actions
  skip_before_action :authenticate_user!, only: [:index, :show]
end

# Authorization — policy objects (Pundit pattern or manual)
class PostPolicy
  def initialize(user, post)
    @user = user
    @post = post
  end

  def update?
    @user.admin? || @post.user_id == @user.id
  end
end

# In controller
def update
  @post = Post.find(params[:id])
  policy = PostPolicy.new(current_user, @post)
  return head :forbidden unless policy.update?
  # ... update logic
end

# NEVER rely on hidden fields or client-side checks alone
# Always enforce auth server-side
```

## Secrets Management

```ruby
# config/credentials.yml.enc (encrypted, safe to commit)
# Edit with: rails credentials:edit
# Access:
Rails.application.credentials.database[:password]
Rails.application.credentials.dig(:aws, :access_key_id)

# ENV for 12-factor apps (Heroku, Docker, etc.)
# Always use fetch to fail loudly if missing
DB_PASSWORD = ENV.fetch('DB_PASSWORD')  # raises KeyError if missing
DB_PASSWORD = ENV.fetch('DB_PASSWORD') { raise "DB_PASSWORD not set" }

# Never in source code
config.secret_key_base = "abc123hardcoded"  # NEVER
```

## Controller Pattern

```ruby
class UsersController < ApplicationController
  before_action :authenticate_user!
  before_action :set_user, only: [:show, :update, :destroy]
  before_action :authorize_user!, only: [:update, :destroy]

  def show
    render json: @user.as_json(only: [:id, :name, :email])
  end

  def update
    if @user.update(user_params)
      render json: @user
    else
      render json: { errors: @user.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def set_user
    @user = User.find(params[:id])
  end

  def authorize_user!
    head :forbidden unless current_user.admin? || @user == current_user
  end

  def user_params
    params.require(:user).permit(:name, :email, :bio)
  end
end
```

## Model: Thin, Validated, No Business Logic

```ruby
class User < ApplicationRecord
  # Validations
  validates :email, presence: true, uniqueness: { case_sensitive: false },
                    format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true, length: { maximum: 100 }

  # Scopes — declarative query building
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc) }
  scope :admins, -> { where(role: 'admin') }

  # Callbacks — use sparingly, only for model lifecycle concerns
  before_save :normalize_email

  # Associations
  has_many :posts, dependent: :destroy
  belongs_to :organization

  private

  def normalize_email
    self.email = email.to_s.strip.downcase
  end
end

# Business logic lives in service objects, NOT the model
# UserRegistrationService, UserImportService, etc.
```

## Service Objects (Functional Core in Rails)

```ruby
# app/services/user_registration_service.rb
class UserRegistrationService
  Result = Data.define(:success, :user, :errors)

  def self.call(attrs)
    new(attrs).call
  end

  def initialize(attrs)
    @attrs = attrs
  end

  def call
    user = User.new(normalized_attrs)
    if user.save
      send_welcome_email(user)
      Result.new(success: true, user: user, errors: [])
    else
      Result.new(success: false, user: nil, errors: user.errors.full_messages)
    end
  end

  private

  def normalized_attrs
    @attrs.slice(:name, :email, :password).merge(
      email: @attrs[:email].to_s.strip.downcase,
      name: @attrs[:name].to_s.strip
    )
  end

  def send_welcome_email(user)
    WelcomeMailer.with(user: user).welcome_email.deliver_later
  end
end

# Usage in controller
result = UserRegistrationService.call(user_params)
```

## File Organization

```
app/
├── controllers/
│   └── users_controller.rb      # Thin — delegate to services
├── models/
│   └── user.rb                  # Validations, scopes, associations only
├── services/
│   └── user_registration_service.rb  # Business logic
├── policies/
│   └── user_policy.rb           # Authorization rules
└── views/
    └── users/                   # Only <%= %> — never <%== %>
config/
└── credentials.yml.enc          # Secrets (encrypted)
```

## Security Checklist

- [ ] Strong Parameters on all mutating actions
- [ ] No string interpolation in SQL queries
- [ ] `protect_from_forgery` enabled (default — don't remove)
- [ ] `before_action` auth guard on all sensitive routes
- [ ] No secrets in source code — credentials or ENV.fetch
- [ ] ERB uses `<%= %>` not `<%== %>` for user content
- [ ] `sanitize` used when rendering user-supplied HTML
- [ ] Dependency audit: `bundle exec bundler-audit check --update`

## When to Load Reference Files

### Security Deep Dive
**File**: [`references/security.md`](references/security.md)
**Load when**: Need vulnerable vs. safe comparisons, injection examples, CSRF details
**Contains**: Full attack examples, all Rails security helpers, CSP configuration

### ActiveRecord Patterns
**File**: [`references/activerecord.md`](references/activerecord.md)
**Load when**: Complex queries, raw SQL needs, migration patterns, performance
**Contains**: Query interface, raw SQL safety, N+1 prevention, index strategy

### Testing Strategy
**File**: [`references/testing.md`](references/testing.md)
**Load when**: Writing request specs, model specs, service object tests
**Contains**: RSpec patterns, factory patterns, security test examples

---

**Evidence Base**: OWASP Top 10 (2021), Rails Security Guide, RailsFactory/Corgea security research (2024–2025).
