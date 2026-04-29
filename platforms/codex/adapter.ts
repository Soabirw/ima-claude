import { join, dirname } from "path";
import { homedir } from "os";
import { existsSync, readdirSync, statSync, readFileSync, writeFileSync, copyFileSync } from "fs";
import { fileURLToPath } from "url";

import type { PlatformAdapter, InstallItem, InstallPreview } from "../shared/types";
import { ensureDir, copyDirRecursive, log, SKILLS_TO_INSTALL, HOOKS_TO_INSTALL, HOOKS_CONFIG, VERSION } from "../../scripts/utils";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Honour CODEX_HOME if set; otherwise default to ~/.codex
const CODEX_DIR = process.env.CODEX_HOME ?? join(homedir(), ".codex");
const CODEX_SKILLS_DIR = join(CODEX_DIR, "skills");
const CODEX_AGENTS_DIR = join(CODEX_DIR, "agents");
const CODEX_HOOKS_DIR = join(CODEX_DIR, "hooks");
const CODEX_HOOKS_CONFIG = join(CODEX_DIR, "hooks.json");
const CODEX_GUIDELINES_FILE = join(CODEX_DIR, "AGENTS.md");
const CODEX_CONFIG_TOML = join(CODEX_DIR, "config.toml");

// Claude Code → Codex CLI tool name mapping
// Based on developers.openai.com/codex docs. "shell" is well-attested; the rest
// are best-known canonical names. Update here if a Codex release renames any.
const TOOL_MAP: Record<string, string> = {
  Bash: "shell",
  Read: "read",
  Edit: "edit",
  Write: "write",
  Glob: "glob",
  Grep: "grep",
  LS: "list",
  WebSearch: "web_search",
  WebFetch: "fetch",
  ExitPlanMode: "ExitPlanMode",
};

// Claude Code → Codex CLI hook event mapping
// Codex uses Claude Code's exact event names natively, so this is identity.
// Kept as a constant so future divergences are a single-point edit.
const EVENT_MAP: Record<string, string> = {
  PreToolUse: "PreToolUse",
  PostToolUse: "PostToolUse",
  UserPromptSubmit: "UserPromptSubmit",
  SessionStart: "SessionStart",
};

// Simple single-line YAML parser — same shape as Junie/Gemini/Copilot adapters.
function parseFrontmatter(content: string): { frontmatter: Record<string, string>; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) return { frontmatter: {}, body: content };

  const frontmatter: Record<string, string> = {};
  for (const line of match[1].split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    const value = line.slice(colonIdx + 1).trim();
    if (key) frontmatter[key] = value;
  }

  return { frontmatter, body: match[2] };
}

function serializeFrontmatter(frontmatter: Record<string, string>, body: string): string {
  const lines = Object.entries(frontmatter).map(([k, v]) => `${k}: ${v}`);
  return `---\n${lines.join("\n")}\n---\n${body}`;
}

function mapToolName(claudeName: string): string {
  return TOOL_MAP[claudeName] ?? claudeName;
}

function transformAgentForCodex(content: string): string {
  const { frontmatter, body } = parseFrontmatter(content);

  // Drop permissionMode (Codex uses global approval_policy / sandbox_mode)
  // Drop model (Codex uses its own model selection)
  const { permissionMode: _perm, model: _model, ...kept } = frontmatter;

  // Map tool names in the tools field if present
  if (kept.tools) {
    const mapped = kept.tools
      .split(",")
      .map((t) => t.trim())
      .map(mapToolName)
      .join(", ");
    kept.tools = mapped;
  }

  return serializeFrontmatter(kept, body);
}

function translateMatcher(matcher: string): string {
  // MCP tool matchers pass through unchanged; only map built-in Claude tool names
  return TOOL_MAP[matcher] ?? matcher;
}

function translateHookCommand(command: string): string {
  // Rewrite hook commands to route through the translator shim
  // Original: python3 ~/.claude/hooks/some_hook.py
  // Codex:    python3 ~/.codex/hooks/hooks-translator.py ~/.codex/hooks/some_hook.py
  const translatorPath = join(CODEX_HOOKS_DIR, "hooks-translator.py");

  const match = command.match(/python3\s+.*\/([^/\s]+\.py)(\s.*)?$/);
  if (!match) return command;

  const scriptName = match[1];
  const trailingArgs = match[2] ?? "";
  return `python3 ${translatorPath} ${join(CODEX_HOOKS_DIR, scriptName)}${trailingArgs}`;
}

function generateCodexHooksConfig(): Record<string, unknown> {
  const codexHooks: Record<string, unknown[]> = {};

  for (const [claudeEvent, hookEntries] of Object.entries(HOOKS_CONFIG.hooks)) {
    const codexEvent = EVENT_MAP[claudeEvent] ?? claudeEvent;

    codexHooks[codexEvent] = (hookEntries as Array<{ matcher?: string; hooks: Array<{ type: string; command: string }> }>).map(
      (entry) => {
        const translated: Record<string, unknown> = {};

        if (entry.matcher) {
          translated.matcher = translateMatcher(entry.matcher);
        }

        translated.hooks = entry.hooks.map((h) => ({
          type: h.type,
          command: translateHookCommand(h.command),
        }));

        return translated;
      }
    );
  }

  return { hooks: codexHooks };
}

function generateCodexAgentsMd(): string {
  return `# ima-claude: AI Coding Agent Guidelines

> Generated by ima-claude v${VERSION} for OpenAI Codex CLI.
> Source: https://github.com/Soabirw/ima-claude

This file is auto-loaded by Codex at session start (\`AGENTS.md\` convention).
Per-directory \`AGENTS.md\` files in your project tree merge on top of this one,
with closer-to-cwd files taking precedence.

## Default Persona: The Practitioner

A 25-year software development veteran. FP-first, composition-minded, anti-over-engineering.
Uses "we" not "I" — collaborative, humble, light-hearted. "Slow is smooth, smooth is fast."

**Philosophy**: Simple > Complex | Evidence > Assumptions | Native > Utilities | MVP > Enterprise

---

## Memory Routing

| Store what | Where | Why |
|---|---|---|
| Decisions, preferences, patterns, bugs | Vestige \`smart_ingest\` | Fades naturally if not referenced |
| Reference material (docs, standards, PRDs) | Qdrant \`qdrant-store\` | Permanent library |
| Session state, task progress | Serena \`write_memory\` | Project-scoped workbench |
| Future reminders | Vestige \`intention\` | Surfaces at next session |

At session start, check memory before asking questions:
- Vestige: search for user preferences and project context
- Vestige: check for pending reminders/intentions
- Serena: list memories if in a Serena-activated project

Auto-store: "I prefer..." → Vestige preference. "Let's go with X because..." → Vestige decision. "The reason this failed..." → Vestige bug.

After completing work: store outcome in Vestige, reference material in Qdrant, session state in Serena.

---

## Orchestrator Protocol

You are the Orchestrator. Plan and delegate. Do NOT implement directly.
- Non-trivial work → task-planner (decompose) → task-runner (delegate)
- Trivial = single file, < 5 lines, no judgment calls

---

## Available Agents

Codex does not yet support a formal named-subagent dispatcher. Treat the agents
listed below as documented delegation patterns: when the work matches, scope a
session (or a per-directory \`AGENTS.md\` overlay) to that agent's persona.
Reference copies of each agent's full system prompt live in \`~/.codex/agents/\`.

| Agent | Use For |
|---|---|
| \`explorer\` | File discovery, codebase exploration |
| \`implementer\` | Feature dev, bug fixes, refactoring |
| \`reviewer\` | Code review, security audit, FP checks |
| \`tester\` | Test creation, TDD, debugging test failures |
| \`wp-developer\` | WordPress plugins, themes, WP-CLI, forms |
| \`memory\` | Memory search, storage, consolidation |

---

## Code Navigation (Serena)

When Serena MCP is available, **prefer Serena over read/grep for code investigation.** 40-70% token savings.

| Instead of | Use |
|---|---|
| Read file to understand structure | Serena get_symbols_overview |
| grep for class/function definition | Serena find_symbol |
| grep for callers/references | Serena find_referencing_symbols |

Use the read tool only when you need the actual implementation body of a known, specific symbol.

---

## Complex Reasoning

Use sequential thinking before acting on:
- Debugging / root cause analysis / "why is this failing"
- Trade-off evaluation / "which approach"
- Architectural decisions / design choices
- Multi-step investigations where approach may change

---

## MCP Tool Routing

| Signal | Preferred Tool |
|---|---|
| "latest", "2025/2026", "what's new" | Tavily search |
| Library/framework API question | Context7 |
| URL content extraction | Tavily extract (use advanced for complex pages) |

Before web tools: check internal knowledge → Context7 → then Tavily.
Before external lookups: check Vestige memory first.

To register MCP servers in Codex, add \`[mcp_servers.<name>]\` tables to
\`~/.codex/config.toml\`. STDIO transport is the documented default.

---

## Search Preference

Always prefer \`rg\` (ripgrep) over grep/find. Faster, respects .gitignore, recursive by default.

---

## Security

- Verify nonce usage and input sanitization in WordPress PHP code
- Never concatenate user input directly into SQL — use parameterized queries
- Check for XSS, CSRF, and OWASP top 10 vulnerabilities in written code

---

## Code Style

- Don't create custom FP utility functions (pipe, compose, curry) — use language-native patterns or established libraries
- In WordPress JavaScript context, use jQuery patterns when jQuery is already loaded
- Prefer Bootstrap utility classes over custom CSS overrides
- Run \`composer dump-autoload\` after creating new PHP files

---

## Documentation

Follow the three-tier documentation system:
- **Active** — Living docs, kept current (README, API docs, architecture)
- **Archive** — Historical reference, rarely updated (decisions, post-mortems)
- **Transient** — Ephemeral, git-ignored (session notes, scratch)
`;
}

export class CodexAdapter implements PlatformAdapter {
  readonly name = "codex";
  readonly displayName = "OpenAI Codex CLI";
  readonly configDir = CODEX_DIR;

  detect(): boolean {
    return existsSync(CODEX_DIR);
  }

  preview(sourceDir: string): InstallPreview {
    const skillItems: InstallItem[] = SKILLS_TO_INSTALL.map((skill) => ({
      name: skill,
      category: "skill" as const,
      destPath: join(CODEX_SKILLS_DIR, skill),
      exists: existsSync(join(CODEX_SKILLS_DIR, skill)),
    })).filter((item) => existsSync(join(sourceDir, "skills", item.name)));

    const agentsDir = join(sourceDir, "agents");
    const agentItems: InstallItem[] = existsSync(agentsDir)
      ? readdirSync(agentsDir)
          .filter((f) => f.endsWith(".md"))
          .map((file) => ({
            name: file.replace(/\.md$/, ""),
            category: "agent" as const,
            destPath: join(CODEX_AGENTS_DIR, file),
            exists: existsSync(join(CODEX_AGENTS_DIR, file)),
          }))
      : [];

    const hookItems: InstallItem[] = HOOKS_TO_INSTALL.map((file) => ({
      name: file,
      category: "hook" as const,
      destPath: join(CODEX_HOOKS_DIR, file),
      exists: existsSync(join(CODEX_HOOKS_DIR, file)),
    }));

    const translatorItem: InstallItem = {
      name: "hooks-translator.py",
      category: "hook",
      destPath: join(CODEX_HOOKS_DIR, "hooks-translator.py"),
      exists: existsSync(join(CODEX_HOOKS_DIR, "hooks-translator.py")),
    };

    const guidelineItem: InstallItem = {
      name: "AGENTS.md",
      category: "guideline",
      destPath: CODEX_GUIDELINES_FILE,
      exists: existsSync(CODEX_GUIDELINES_FILE),
    };

    return {
      platform: this.name,
      targetDir: CODEX_DIR,
      items: [...skillItems, ...agentItems, ...hookItems, translatorItem, guidelineItem],
    };
  }

  installSkills(sourceDir: string, exclude?: string[]): void {
    ensureDir(CODEX_SKILLS_DIR);
    const skills = exclude?.length
      ? SKILLS_TO_INSTALL.filter((s) => !exclude.includes(s))
      : SKILLS_TO_INSTALL;
    for (const skill of skills) {
      const src = join(sourceDir, skill);
      if (existsSync(src) && statSync(src).isDirectory()) {
        copyDirRecursive(src, join(CODEX_SKILLS_DIR, skill));
        log.step(`skill: ${skill}`);
      }
    }
  }

  installAgents(sourceDir: string, exclude?: string[]): void {
    ensureDir(CODEX_AGENTS_DIR);
    const entries = readdirSync(sourceDir)
      .filter((f) => f.endsWith(".md"))
      .filter((f) => !exclude?.includes(f.replace(/\.md$/, "")));
    for (const file of entries) {
      const content = readFileSync(join(sourceDir, file), "utf8");
      const transformed = transformAgentForCodex(content);
      writeFileSync(join(CODEX_AGENTS_DIR, file), transformed);
      log.step(`agent: ${file}`);
    }
  }

  installGuidelines(_pluginRoot: string): void {
    ensureDir(CODEX_DIR);
    writeFileSync(CODEX_GUIDELINES_FILE, generateCodexAgentsMd());
    log.step(`guidelines: ${CODEX_GUIDELINES_FILE}`);
  }

  installHooks(sourceDir: string, exclude?: string[]): void {
    ensureDir(CODEX_HOOKS_DIR);

    const hooks = exclude?.length
      ? HOOKS_TO_INSTALL.filter((f) => !exclude.includes(f))
      : HOOKS_TO_INSTALL;
    for (const file of hooks) {
      const src = join(sourceDir, file);
      if (existsSync(src)) {
        copyFileSync(src, join(CODEX_HOOKS_DIR, file));
        log.step(`hook: ${file}`);
      }
    }

    const shimSrc = join(__dirname, "hooks-translator.py");
    if (!existsSync(shimSrc)) {
      throw new Error(`hooks-translator.py not found at ${shimSrc} — packaging error`);
    }
    copyFileSync(shimSrc, join(CODEX_HOOKS_DIR, "hooks-translator.py"));
    log.step("hook: hooks-translator.py (shim)");

    const hooksConfig = generateCodexHooksConfig();
    mergeCodexHooksConfig(CODEX_HOOKS_CONFIG, hooksConfig);
    log.step("hook: hooks.json (generated for Codex CLI)");
  }

  postInstall(): void {
    log.info("OpenAI Codex CLI install complete. Verify:");
    log.info(`  Skills:     ${CODEX_SKILLS_DIR}`);
    log.info(`  Agents:     ${CODEX_AGENTS_DIR}`);
    log.info(`  Hooks:      ${CODEX_HOOKS_DIR}`);
    log.info(`  Hooks cfg:  ${CODEX_HOOKS_CONFIG}`);
    log.info(`  Guidelines: ${CODEX_GUIDELINES_FILE}`);
    log.info("");
    log.info("MCP servers are not auto-configured. To register them, add");
    log.info(`  [mcp_servers.<name>] command = "..." args = [...]`);
    log.info(`tables to ${CODEX_CONFIG_TOML} (STDIO transport).`);
    log.info("");
    log.info("If a hook silently fails to fire, the Codex tool name may have changed —");
    log.info("update TOOL_MAP in platforms/codex/adapter.ts and reinstall.");
  }
}

function mergeCodexHooksConfig(
  configPath: string,
  newConfig: Record<string, unknown>
): void {
  let existing: Record<string, unknown> = {};

  if (existsSync(configPath)) {
    try {
      const content = readFileSync(configPath, "utf8");
      existing = JSON.parse(content);
    } catch {
      existing = {};
    }
  }

  if (!existing.hooks) {
    existing.hooks = {};
  }
  const existingHooks = existing.hooks as Record<string, unknown[]>;
  const incomingHooks = (newConfig as Record<string, unknown>).hooks as Record<
    string,
    Array<{ matcher?: string; hooks: Array<{ command: string }> }>
  >;

  // Merge each event: strip prior ima-claude entries (identified by hooks-translator.py
  // substring in any nested command), then append the new entries. User hooks survive.
  for (const [event, entries] of Object.entries(incomingHooks)) {
    if (!existingHooks[event]) {
      existingHooks[event] = entries;
      continue;
    }

    const userEntries = (
      existingHooks[event] as Array<{ matcher?: string; hooks?: Array<{ command?: string }> }>
    ).filter(
      (entry) =>
        !entry.hooks?.some((h) => h.command?.includes("hooks-translator.py"))
    );

    existingHooks[event] = [...userEntries, ...entries];
  }

  writeFileSync(configPath, JSON.stringify(existing, null, 2) + "\n");
}
