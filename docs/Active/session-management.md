# Session Management (MCP-Based)

Lean save/resume system using Serena MCP memories (no file path confusion).

## Commands

### `/save-session`
Saves current session state to Serena MCP memory `session-state`.

**What gets saved:**
- Current Task (1-2 sentences)
- Modified Files (list)
- Decisions Made (bullets)
- Technical Context (code/patterns/dependencies)
- Outstanding Items (checklist)
- Resume Hint (what to do first)

**What gets excluded:**
- Conversation history
- Code snippets (files have the code)
- Completed work
- Research dead-ends

### `/resume-session`
Restores session from Serena MCP memory and presents status summary.

**Behavior:**
- Reads memory
- Shows status summary
- Waits for user direction
- Does NOT auto-start work

## Technical Implementation

**Storage:** Serena MCP `write_memory/read_memory`
- Memory name: `session-state`
- Project-specific
- Cross-session persistent
- No file path confusion (Serena handles storage)

**Format:** Structured markdown (same as old file-based approach)

## Advantages Over File-Based

1. **No path confusion** - Serena handles storage location
2. **Project-bound** - Memory tied to project context
3. **Cross-session** - Survives Claude restarts
4. **Lean** - Single checkpoint, not a massive project load
5. **Simple** - No `.claude` directory creation, no absolute path resolution

## Requirements

**Serena MCP** is required for session management. The skills use Serena's file-based memory storage which is designed for document persistence (unlike Memory MCP which is optimized for knowledge graphs).

If Serena is not installed, the skills will inform you and provide installation guidance.

## Migration from Old Commands

Old commands in `~/.claude/commands/`:
- `save-session.md` - tried to write `.claude/session.md`
- `resume-session.md` - tried to read `.claude/session.md`
- `save-session-lean.md` - same approach

**Issues:**
- Claude confused about working directory
- File write failures
- Path resolution problems

**Solution:**
- Convert to Skills
- Use Serena MCP instead of files
- Let Serena handle storage
