---
name: "mcp-memory"
description: "Memory MCP for persistent knowledge graph across sessions. Store project decisions, user preferences, architectural patterns, and important context. Use when information should persist beyond current conversation."
triggers:
  - "remember this"
  - "save this"
  - "note this"
  - "store this"
  - "for next time"
  - "don't forget"
  - "recall"
  - "what did we"
  - "what was"
  - "previously"
  - "last time"
  - "user preference"
  - "project decision"
  - "architectural decision"
---

# Memory MCP - Persistent Knowledge Graph

Use Memory MCP to store and retrieve information across sessions as a knowledge graph.

## Setup: Airis Gateway

Memory runs through the Airis MCP gateway.

**Tool access pattern**: `mcp__airis-mcp-gateway__airis-exec` with `tool: "memory:tool-name"`

## Available Tools

| Tool | Purpose |
|------|---------|
| `memory:create_entities` | Create new entities (things/concepts) |
| `memory:create_relations` | Link entities together |
| `memory:add_observations` | Add facts to existing entities |
| `memory:search_nodes` | Search the knowledge graph |
| `memory:open_nodes` | Get specific entities by name |
| `memory:read_graph` | Read entire knowledge graph |
| `memory:delete_entities` | Remove entities |
| `memory:delete_relations` | Remove relations |
| `memory:delete_observations` | Remove observations |

## When to Use

**Store (create/add):**
- Project architectural decisions
- User preferences and conventions
- Important code patterns specific to a project
- Configuration choices and rationale
- Team standards and agreements
- Bug fixes and their root causes (for reference)

**Retrieve (search/read):**
- "What did we decide about X?"
- "What's the user's preference for Y?"
- "How did we solve this before?"
- Session start: Load relevant project context

## Workflow

### 1. Load Server (if cold)

```
mcp__airis-mcp-gateway__airis-find
  server: "memory"
  query: "memory"
```

### 2. Create Entities

Entities are the nodes in your knowledge graph - things, concepts, decisions.

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:create_entities"
  arguments: {
    "entities": [
      {
        "name": "project-acme-api",
        "entityType": "project",
        "observations": [
          "Uses Node.js with Express",
          "PostgreSQL database",
          "REST API architecture chosen over GraphQL"
        ]
      },
      {
        "name": "user-eric",
        "entityType": "user",
        "observations": [
          "Prefers functional programming patterns",
          "Uses Quasar for Vue projects",
          "Wants minimal comments in code"
        ]
      }
    ]
  }
```

### 3. Create Relations

Relations connect entities - use active voice verbs.

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:create_relations"
  arguments: {
    "relations": [
      {
        "from": "user-eric",
        "to": "project-acme-api",
        "relationType": "owns"
      },
      {
        "from": "project-acme-api",
        "to": "decision-rest-over-graphql",
        "relationType": "uses"
      }
    ]
  }
```

### 4. Add Observations

Add new facts to existing entities.

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:add_observations"
  arguments: {
    "observations": [
      {
        "entityName": "project-acme-api",
        "contents": [
          "Added rate limiting on 2024-01-15",
          "Uses Redis for session storage"
        ]
      }
    ]
  }
```

### 5. Search Knowledge Graph

Find relevant entities by query.

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:search_nodes"
  arguments: {
    "query": "authentication"
  }
```

### 6. Get Specific Entities

Retrieve entities by name.

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:open_nodes"
  arguments: {
    "names": ["user-eric", "project-acme-api"]
  }
```

### 7. Read Full Graph

Get everything (use sparingly for large graphs).

```
mcp__airis-mcp-gateway__airis-exec
  tool: "memory:read_graph"
  arguments: {}
```

## Entity Types (Suggested)

| Type | Use For |
|------|---------|
| `project` | Projects, repos, codebases |
| `user` | User preferences, conventions |
| `decision` | Architectural/design decisions |
| `pattern` | Code patterns, conventions |
| `technology` | Tools, frameworks, libraries |
| `bug` | Notable bugs and their fixes |
| `standard` | Team/org standards |

## Naming Conventions

Use consistent, searchable names:
- `project-{name}` - Projects
- `user-{name}` - Users
- `decision-{topic}` - Decisions
- `pattern-{name}` - Patterns
- `tech-{name}` - Technologies

## Best Practices

1. **Be specific in observations** - "Uses JWT with 24h expiry" not "uses auth"
2. **Include rationale** - "Chose X because Y" helps future decisions
3. **Use consistent entity types** - Makes searching easier
4. **Create relations** - The graph structure is valuable
5. **Search before creating** - Avoid duplicates
6. **Update, don't duplicate** - Use `add_observations` for existing entities

## Example: Storing a Project Decision

```
# Create the decision entity
memory:create_entities
  entities: [{
    "name": "decision-api-versioning",
    "entityType": "decision",
    "observations": [
      "Decided to use URL path versioning (/v1/, /v2/)",
      "Rejected header versioning due to caching complexity",
      "Made on 2024-01-20 by Eric",
      "Applies to all REST endpoints"
    ]
  }]

# Link to project
memory:create_relations
  relations: [{
    "from": "project-acme-api",
    "to": "decision-api-versioning",
    "relationType": "follows"
  }]
```

## Example: Storing User Preferences

```
memory:create_entities
  entities: [{
    "name": "user-eric-code-style",
    "entityType": "preference",
    "observations": [
      "Prefer const over let when possible",
      "Use arrow functions for callbacks",
      "No semicolons (StandardJS style)",
      "Prefer early returns over nested if/else",
      "Minimal inline comments - code should be self-documenting"
    ]
  }]
```

## Example: Session Start - Load Context

```
# Search for relevant project context
memory:search_nodes
  query: "project-acme"

# Get user preferences
memory:open_nodes
  names: ["user-eric", "user-eric-code-style"]
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| Server cold | Use `airis-find server="memory"` first |
| Entity not found | Check spelling, use `search_nodes` to find |
| Duplicate entity | Use `add_observations` instead of create |
