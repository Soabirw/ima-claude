---
name: mcp-qdrant
description: "Qdrant MCP — the permanent library. Unlike Vestige (neural memory that fades), nothing stored here is ever forgotten. Use for all reference material: wiki articles, coding standards, architecture docs, code samples, PRDs, plans, meeting notes, research findings. Triggers on: 'store this', 'what do we know about', 'search knowledge', 'add to library', 'find in docs'. Triggers proactively when reference material is created, discussed, or finalized — feed the library without being asked. Search the library before starting any new work."
---

# Qdrant MCP — Permanent Library

| System | Role | Lifecycle |
|--------|------|-----------|
| **Qdrant** | Permanent library — standards, PRDs, architecture, code samples | Persistent forever |
| **Vestige** | Neural memory — decisions, preferences, learnings | Fades if unused (FSRS-6) |
| **Serena Memory** | Project workbench — session state, task progress | Project-scoped |

**Decision rule**: Will it fade if unused? No → Qdrant. Yes → Vestige.

## Embedding Stack

| Component | Ollama (default) | fastembed |
|-----------|-----------------|-----------|
| Embedding model | `nomic-embed-text` | `BAAI/bge-small-en-v1.5` |
| Vector dimensions | 768 | 384 |
| Distance metric | Cosine | Cosine |
| Dependency | Ollama running locally | `pip install qdrant-mcp[fastembed]` |
| Default collection | `ima-knowledge` | `ima-knowledge` |

Collections can't be shared across providers (different vector dimensions). Switching providers requires collection rebuild.

## Per-Project Collection

Add `.qdrant` to project root (YAML):

```yaml
collection: my-project-knowledge
```

At session start, check for `.qdrant`. If found, pass `collection_name` on every `qdrant_store` and `qdrant_find` call. If absent, omit `collection_name` — server defaults to `ima-knowledge`.

## MCP Tools

Server: `qdrant-memory`. Prefix: `mcp__qdrant-memory__`.

| Tool | Purpose | Parameters |
|------|---------|------------|
| `qdrant_store` | Store text with auto-embedding | `information` (required), `collection_name`, `metadata` |
| `qdrant_find` | Semantic search | `query` (required), `collection_name`, `limit` |

## Storing

```
mcp__qdrant-memory__qdrant_store
  information: "The IMA donation system uses Authorize.net Accept.js for payment
    processing. Guest donations use charge-then-profile for ARB recurring."
  metadata: {"source": "donation-system-prd", "type": "architecture", "date": "2026-02-21"}
```

### What to Store

| Content Type | `type` metadata |
|---|---|
| PRDs / Feature Specs | `prd` |
| Architecture decisions | `architecture` |
| Integration guides | `integration` |
| Domain knowledge | `domain` |
| Requirements / meeting notes | `requirements` |
| Coding standards | `standard` |
| Code samples | `sample` |

### Chunking (docs >2000 words)

Store by section; include document title in each chunk:

```
Store: "Donation System PRD - Overview: [content]"
  metadata: {"source": "donation-prd", "type": "prd", "section": "overview"}
```

## Searching

```
mcp__qdrant-memory__qdrant_find
  query: "how does guest recurring donation work"
```

- Broad: `"payment processing"` — discover available knowledge
- Specific: `"Authorize.net ARB guest checkout"` — targeted lookup
- Problem-oriented: `"SSO between WordPress and Discourse"` — find solutions

## Proactive Behavior

**Feed library when:**
- Wiki article, PRD, or spec created/discussed
- Architecture documented or diagrammed
- Coding standard established
- Useful code sample written
- Research completed
- Integration documented
- Meeting notes capture decisions
- User says "store this" or "add to knowledge base"

**Search library when:**
- Starting any feature implementation
- Debugging an integration
- User asks "how does X work"
- Planning new work or making architectural decisions

## Decision Logic

```
IF reference material that should never be forgotten
   (wiki, standards, PRDs, architecture, code samples):
    → qdrant_store (permanent)
ELSE IF knowledge that strengthens with use, fades if unused:
    → Vestige smart_ingest
ELSE IF session state or project progress:
    → Serena write_memory

Searching:
IF need reference docs, architecture context, prior art:
    → qdrant_find
IF need preferences or past decisions:
    → Vestige search
IF starting new work:
    → Search BOTH
```

## Metadata Conventions

| Key | Values | Purpose |
|-----|--------|---------|
| `source` | kebab-case document name | Group chunks from same doc |
| `type` | `prd`, `architecture`, `integration`, `domain`, `requirements`, `standard`, `sample` | Categorize |
| `date` | `YYYY-MM-DD` | When stored |

## Error Recovery

| Issue | Resolution |
|-------|------------|
| No results | Broaden query terms |
| Irrelevant results | Use more specific key terms |
| Qdrant not responding | `docker ps \| grep qdrant` — restart if needed |
| Ollama not responding | `ollama list` — ensure running with `nomic-embed-text` |
| fastembed not installed | `pip install qdrant-mcp[fastembed]` |
| Switched providers, bad results | Different vector dimensions — rebuild collection |
| Duplicate content | Search before storing to verify novelty |

## When NOT to Use

- Fading knowledge (preferences, decisions) → Vestige
- Session state / task progress → Serena memory
- Code symbol search → Serena or Grep
- Current web info → Tavily
- Library API docs → Context7

## Setup

```bash
# 1. Start Qdrant
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# 2a. Ollama (default)
ollama pull nomic-embed-text

# 2b. fastembed (CPU-only)
# pip install qdrant-mcp[fastembed]

# 3. Install MCP server
cd ~/dev/qdrant-mcp-server && pip install -e .

# 4. Add to ~/.claude.json mcpServers:
# "qdrant-memory": {
#   "type": "stdio",
#   "command": "qdrant-mcp",
#   "env": {
#     "QDRANT_URL": "http://localhost:6333",
#     "COLLECTION_NAME": "ima-knowledge",
#     "EMBEDDING_PROVIDER": "ollama",
#     "OLLAMA_URL": "http://localhost:11434",
#     "EMBEDDING_MODEL": "nomic-embed-text"
#   }
# }

# 5. Verify
curl http://localhost:6333/health
```
