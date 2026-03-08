---
name: mcp-qdrant
description: "Qdrant MCP — the permanent library. Unlike Vestige (neural memory that fades), nothing stored here is ever forgotten. Use for all reference material: wiki articles, coding standards, architecture docs, code samples, PRDs, plans, meeting notes, research findings. Triggers on: 'store this', 'what do we know about', 'search knowledge', 'add to library', 'find in docs'. Triggers proactively when reference material is created, discussed, or finalized — feed the library without being asked. Search the library before starting any new work."
---

# Qdrant MCP - The Permanent Library

Our permanent reference library. Unlike Vestige (neural memory that fades if unused), nothing stored here is ever forgotten. This is where we feed our entire universe — wiki articles, coding standards, architecture docs, code samples, PRDs, plans, and research findings.

## Architecture: How This Fits

| System | Role | Lifecycle | Example |
|--------|------|-----------|---------|
| **Qdrant** | Permanent library — reference material, standards, PRDs, architecture docs, code samples | Persistent forever | "Our payment system uses Accept.js with ARB" |
| **Vestige** | Neural memory — decisions, preferences, patterns, bugs, learnings | Fades if unused (FSRS-6 decay) | "We chose JWT over sessions because..." |
| **Serena Memory** | Project workbench — session state, task progress | Project-scoped, survives git ops | "Currently on task 3/5" |

**Will it fade if we stop referencing it?** If no → Qdrant (permanent). If yes → Vestige (neural decay).

## Embedding Stack

| Component | Value |
|---|---|
| MCP server | `qdrant-mcp` (custom, at `~/dev/qdrant-mcp-server`) |
| Embedding model | `nomic-embed-text` via Ollama |
| Vector dimensions | 768 |
| Distance metric | Cosine |
| Vector type | Default (unnamed) |
| Default collection | `ima-knowledge` |

## Per-Project Collection

Projects can specify their Qdrant collection via a `.qdrant` file in the project root (YAML format, like `.serena`):

```yaml
# .qdrant — project-level config
collection: my-project-knowledge
```

**At session start**, check for a `.qdrant` file in the working directory. If found, read its `collection` value and pass it as `collection_name` on every `qdrant_store` and `qdrant_find` call for that session.

If no `.qdrant` file is found, omit `collection_name` — the server defaults to `ima-knowledge` (from the `COLLECTION_NAME` env var).

## MCP Tools

MCP server name: `qdrant-memory`. Tool prefix: `mcp__qdrant-memory__`.

| Tool | Purpose | Parameters |
|------|---------|------------|
| `qdrant_store` | Store text with auto-embedding | `information` (required), `collection_name`, `metadata` |
| `qdrant_find` | Semantic search across stored knowledge | `query` (required), `collection_name`, `limit` |

## Storing Knowledge

```
mcp__qdrant-memory__qdrant_store
  information: "The IMA donation system uses Authorize.net Accept.js for payment
    processing. Guest donations use charge-then-profile for ARB recurring."
  metadata: {"source": "donation-system-prd", "type": "architecture", "date": "2026-02-21"}
```

To target a specific collection explicitly:

```
mcp__qdrant-memory__qdrant_store
  collection_name: "other-project-knowledge"
  information: "..."
```

### What to Store

Anything that should never be forgotten — reference material for our permanent library.

| Content Type | Metadata `type` |
|---|---|
| PRDs / Feature Specs | `prd` |
| Architecture decisions & diagrams | `architecture` |
| Integration guides | `integration` |
| Domain knowledge | `domain` |
| Requirements / meeting notes | `requirements` |
| Coding standards & conventions | `standard` |
| Useful code samples | `sample` |

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
mcp__qdrant-memory__qdrant_find
  query: "how does guest recurring donation work"
```

**Broad**: `"payment processing"` — discover what's available
**Specific**: `"Authorize.net ARB guest checkout"` — find exact knowledge
**Problem-oriented**: `"SSO authentication between WordPress and Discourse"` — find solutions

## Proactive Behavior

### Feed the Library When:

- A wiki article, PRD, or spec is created or discussed → store it
- Architecture is documented or diagrammed → store it
- A coding standard or convention is established → store it
- A useful code sample is written → store it
- Research is completed on a topic → store the findings
- A Compound Engineering solution is finalized → store it
- Integration is documented → store it
- Meeting notes capture decisions or context → store them
- User says "add this to knowledge base" or "store this"

### Search the Library When:

- Starting implementation of any feature → check if prior art exists
- Debugging an integration → search for architecture context
- User asks "how does X work" → check library before guessing
- Planning new work → search for related PRDs or standards
- Before making architectural decisions → search for existing conventions

## Ingestion: Claude Web → Qdrant

When user shares content from Claude Web Projects:

1. User pastes document content
2. For short docs (<2000 words): store as single entry
3. For long docs: chunk by section with shared `source` metadata
4. Confirm: "Stored [title] in knowledge base ([N] chunks)"

## Decision Logic

**Will it fade if we stop referencing it?** If no → store here. Qdrant is the permanent library.

```
IF reference material that should never be forgotten
   (wiki, standards, PRDs, architecture docs, code samples, plans):
    → Qdrant qdrant_store (permanent library)
ELSE IF knowledge that should strengthen with use, fade if unused
   (preferences, decisions, patterns, bugs):
    → Vestige smart_ingest (neural memory)
ELSE IF session state or project progress:
    → Serena write_memory (project workbench)

Searching:
IF need reference docs, architecture context, prior art:
    → Qdrant qdrant_find
IF need user preferences or past decisions:
    → Vestige search
IF starting any new work:
    → Search BOTH Qdrant and Vestige
```

## Metadata Conventions

| Key | Values | Purpose |
|-----|--------|---------|
| `source` | Document name (kebab-case) | Group chunks from same doc |
| `type` | `prd`, `architecture`, `integration`, `domain`, `requirements`, `standard`, `sample` | Categorize |
| `date` | `YYYY-MM-DD` | When stored |

## Error Recovery

| Issue | Resolution |
|-------|------------|
| No results | Broaden query terms |
| Irrelevant results | Use more specific key terms |
| Qdrant not responding | `docker ps \| grep qdrant` — restart if needed |
| Ollama not responding | `ollama list` — ensure it's running with `nomic-embed-text` |
| Duplicate content | Search before storing to verify novelty |

## When NOT to Use

- Knowledge that should fade if unused (preferences, decisions, patterns) → Vestige (neural memory)
- Session state or task progress → Serena memory (project workbench)
- Code symbol search → Serena or Grep
- Current web info → Tavily
- Library API docs → Context7

## Setup

```bash
# 1. Start Qdrant with persistent storage
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# 2. Install Ollama and pull embedding model
ollama pull nomic-embed-text

# 3. Install custom MCP server
cd ~/dev/qdrant-mcp-server && pip install -e .

# 4. Add to Claude Code (in ~/.claude.json mcpServers)
# "qdrant-memory": {
#   "type": "stdio",
#   "command": "qdrant-mcp",
#   "args": [],
#   "env": {
#     "QDRANT_URL": "http://localhost:6333",
#     "COLLECTION_NAME": "ima-knowledge",
#     "OLLAMA_URL": "http://localhost:11434",
#     "EMBEDDING_MODEL": "nomic-embed-text"
#   }
# }

# 5. Verify
curl http://localhost:6333/health
```

**Persistence**: `-v qdrant_storage:/qdrant/storage` preserves data across restarts.
**Embeddings**: Ollama with `nomic-embed-text` (768d). All data stays on your machine.

### Per-Project Setup

Add a `.qdrant` file to any project root to use a project-specific collection:

```yaml
# .qdrant
collection: my-project-knowledge
```

This keeps project knowledge isolated from the global `ima-knowledge` collection. The collection is created automatically on first store.
