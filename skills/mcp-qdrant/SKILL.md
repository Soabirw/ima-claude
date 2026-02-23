---
name: mcp-qdrant
description: "Qdrant MCP for persistent knowledge base with semantic search. Use as a local RAG system for PRDs, architecture docs, integration plans, and domain knowledge that persists across sessions. Triggers on: 'store this in knowledge base', 'what do we know about', 'search knowledge', 'add to RAG', 'find in docs', or when Claude needs context that might already be stored. Also triggers proactively when PRDs, architecture decisions, or integration plans are created — store them automatically. Complements Vestige (preferences/decisions) with document-scale knowledge retrieval."
---

# Qdrant MCP - Persistent Knowledge Base

Local RAG system for document-scale knowledge. Stores and retrieves PRDs, architecture docs, plans, and domain knowledge via semantic search.

## Architecture: How This Fits

| System | Scope | Example |
|--------|-------|---------|
| **Qdrant** | Document knowledge (PRDs, plans, guides) | "Our payment system uses Accept.js with ARB" |
| **Vestige** | Atomic decisions, preferences, patterns | "We chose JWT over sessions because..." |
| **Serena Memory** | Session state checkpoints (ephemeral) | "Currently on task 3/5" |

**Rule of thumb**: Document or large knowledge chunk → Qdrant. Single decision or preference → Vestige.

## MCP Tools

Tool prefix depends on MCP server name (default: `qdrant-memory`).

| Tool | Purpose |
|------|---------|
| `qdrant-store` | Store text with auto-embedding |
| `qdrant-find` | Semantic search across stored knowledge |

## Storing Knowledge

```
mcp__qdrant-memory__qdrant-store
  information: "The IMA donation system uses Authorize.net Accept.js for payment
    processing. Guest donations use charge-then-profile for ARB recurring."
  metadata: {"source": "donation-system-prd", "type": "architecture", "date": "2026-02-21"}
```

### What to Store

| Content Type | Metadata `type` |
|---|---|
| PRDs / Feature Specs | `prd` |
| Architecture decisions | `architecture` |
| Integration guides | `integration` |
| Domain knowledge | `domain` |
| Requirements / meeting notes | `requirements` |

### Chunking Large Documents

For documents over ~2000 words, store by section:

```
Store: "Donation System PRD - Overview: [content]"
  metadata: {"source": "donation-prd", "type": "prd", "section": "overview"}

Store: "Donation System PRD - Payment Flow: [content]"
  metadata: {"source": "donation-prd", "type": "prd", "section": "payment-flow"}
```

Include the document title in each chunk so search results have context.

## Searching Knowledge

```
mcp__qdrant-memory__qdrant-find
  query: "how does guest recurring donation work"
```

**Broad**: `"payment processing"` — discover what's available
**Specific**: `"Authorize.net ARB guest checkout"` — find exact knowledge
**Problem-oriented**: `"SSO authentication between WordPress and Discourse"` — find solutions

## Proactive Behavior

### Store Automatically When:

- PRD or feature spec is created/discussed
- Architecture plan is finalized
- Integration is documented
- Complex research is completed
- User says "add this to knowledge base"

### Search Automatically When:

- Starting implementation of a feature
- Debugging an integration
- User asks "how does X work"
- Planning new work that may have prior context

## Ingestion: Claude Web → Qdrant

When user shares content from Claude Web Projects:

1. User pastes document content
2. For short docs (<2000 words): store as single entry
3. For long docs: chunk by section with shared `source` metadata
4. Confirm: "Stored [title] in knowledge base ([N] chunks)"

## Decision Logic

```
IF document-scale knowledge (PRD, plan, guide, spec):
    → Qdrant
ELSE IF atomic preference/decision/pattern:
    → Vestige
ELSE IF session progress:
    → Serena memory

IF need context before starting work:
    → Search Qdrant first, then Vestige
ELSE IF need user preference:
    → Search Vestige
ELSE IF need related documents:
    → Search Qdrant
```

## Metadata Conventions

| Key | Values | Purpose |
|-----|--------|---------|
| `source` | Document name (kebab-case) | Group chunks from same doc |
| `type` | `prd`, `architecture`, `integration`, `domain`, `requirements` | Categorize |
| `date` | `YYYY-MM-DD` | When stored |

## Error Recovery

| Issue | Resolution |
|-------|------------|
| No results | Broaden query terms |
| Irrelevant results | Use more specific key terms |
| Qdrant not responding | `docker ps \| grep qdrant` — restart if needed |
| Duplicate content | Search before storing to verify novelty |

## When NOT to Use

- Single preferences or decisions → Vestige
- Session state → Serena memory
- Code symbol search → Serena or Grep
- Current web info → Tavily
- Library API docs → Context7

## Setup

```bash
# Start Qdrant with persistent storage
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# Add to Claude Code (global)
claude mcp add --transport stdio --scope user qdrant-memory \
  --env QDRANT_URL="http://localhost:6333" \
  --env COLLECTION_NAME="ima-knowledge" \
  -- uvx mcp-server-qdrant

# Verify
curl http://localhost:6333/health
```

**Persistence**: `-v qdrant_storage:/qdrant/storage` preserves data across restarts.
**Embeddings**: FastEmbed (local, no API keys). All data stays on your machine.
