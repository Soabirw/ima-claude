import { join, dirname } from "path";
import { homedir } from "os";
import { existsSync, readdirSync, statSync, readFileSync, writeFileSync, copyFileSync } from "fs";
import { fileURLToPath } from "url";

import type { PlatformAdapter, InstallItem, InstallPreview } from "../shared/types";
import { ensureDir, copyDirRecursive, log, SKILLS_TO_INSTALL, HOOKS_TO_INSTALL, HOOKS_CONFIG, VERSION } from "../../scripts/utils";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const COPILOT_DIR = join(homedir(), ".copilot");
const COPILOT_SKILLS_DIR = join(COPILOT_DIR, "skills");
const COPILOT_AGENTS_DIR = join(COPILOT_DIR, "agents");
const COPILOT_HOOKS_DIR = join(COPILOT_DIR, "hooks");
const COPILOT_GUIDELINES_FILE = join(COPILOT_DIR, "copilot-instructions.md");

// Claude Code → GitHub Copilot tool name mapping
const TOOL_MAP: Record<string, string> = {
  Bash: "run_terminal_command",
  Read: "read_file",
  Edit: "edit_file",
  Write: "write_file",
  Glob: "find_files",
  Grep: "search_code",
  LS: "list_directory",
  WebSearch: "web_search",
  WebFetch: "fetch_url",
  ExitPlanMode: "ExitPlanMode",
};

// Claude Code → GitHub Copilot hook event mapping
const EVENT_MAP: Record<string, string> = {
  PreToolUse: "preToolUse",
  PostToolUse: "postToolUse",
  UserPromptSubmit: "userPromptSubmitted",
  SessionStart: "sessionStart",
};

// Simple single-line YAML parser — same as Gemini/Junie adapters.
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

function transformAgentForCopilot(content: string): string {
  const { frontmatter, body } = parseFrontmatter(content);

  // Drop permissionMode (Copilot has no equivalent)
  // Drop model (Copilot uses its own model selection)
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
  // Copilot:  python3 ~/.copilot/hooks/hooks-translator.py ~/.copilot/hooks/some_hook.py
  const hooksDir = COPILOT_HOOKS_DIR;
  const translatorPath = join(hooksDir, "hooks-translator.py");

  // Extract the script filename (and any trailing args) from the original command
  const match = command.match(/python3\s+.*\/([^/\s]+\.py)(\s.*)?$/);
  if (!match) return command;

  const scriptName = match[1];
  const trailingArgs = match[2] ?? "";
  return `python3 ${translatorPath} ${join(hooksDir, scriptName)}${trailingArgs}`;
}

function generateCopilotHooksConfig(): Record<string, unknown> {
  const copilotHooks: Record<string, unknown[]> = {};

  for (const [claudeEvent, hookEntries] of Object.entries(HOOKS_CONFIG.hooks)) {
    const copilotEvent = EVENT_MAP[claudeEvent] ?? claudeEvent;

    // Flatten: Claude groups multiple hooks under one matcher,
    // Copilot uses one flat entry per hook command
    const flatEntries: Record<string, unknown>[] = [];

    for (const entry of hookEntries as Array<{ matcher?: string; hooks: Array<{ type: string; command: string }> }>) {
      const translatedMatcher = entry.matcher ? translateMatcher(entry.matcher) : undefined;

      for (const hook of entry.hooks) {
        const flatEntry: Record<string, unknown> = {};
        if (translatedMatcher) {
          flatEntry.matcher = translatedMatcher;
        }
        flatEntry.type = hook.type;
        flatEntry.bash = translateHookCommand(hook.command);
        flatEntries.push(flatEntry);
      }
    }

    copilotHooks[copilotEvent] = flatEntries;
  }

  return { version: 1, hooks: copilotHooks };
}

function generateCopilotInstructionsMd(): string {
  return `# ima-claude: AI Coding Agent Guidelines

> Generated by ima-claude v${VERSION} for GitHub Copilot.
> Source: https://github.com/Soabirw/ima-claude

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

Delegate to named agents — they enforce tools and permissions automatically.

| Agent | Use For |
|---|---|
| \`explorer\` | File discovery, codebase exploration |
| \`implementer\` | Feature dev, bug fixes, refactoring |
| \`reviewer\` | Code review, security audit, FP checks |
| \`wp-developer\` | WordPress plugins, themes, WP-CLI, forms |
| \`memory\` | Memory search, storage, consolidation |

---

## Code Navigation (Serena)

When Serena MCP is available, **prefer Serena over read_file/search_code for code investigation.** 40-70% token savings.

| Instead of | Use |
|---|---|
| Read file to understand structure | Serena get_symbols_overview |
| search_code for class/function definition | Serena find_symbol |
| search_code for callers/references | Serena find_referencing_symbols |

Use read_file only when you need the actual implementation body of a known, specific symbol.

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

export class GhCopilotAdapter implements PlatformAdapter {
  readonly name = "gh-copilot";
  readonly displayName = "GitHub Copilot";
  readonly configDir = COPILOT_DIR;

  detect(): boolean {
    return existsSync(COPILOT_DIR);
  }

  preview(sourceDir: string): InstallPreview {
    const skillItems: InstallItem[] = SKILLS_TO_INSTALL.map((skill) => ({
      name: skill,
      category: "skill" as const,
      destPath: join(COPILOT_SKILLS_DIR, skill),
      exists: existsSync(join(COPILOT_SKILLS_DIR, skill)),
    })).filter((item) => existsSync(join(sourceDir, "skills", item.name)));

    const agentsDir = join(sourceDir, "agents");
    const agentItems: InstallItem[] = existsSync(agentsDir)
      ? readdirSync(agentsDir)
          .filter((f) => f.endsWith(".md"))
          .map((file) => ({
            name: file.replace(/\.md$/, ""),
            category: "agent" as const,
            destPath: join(COPILOT_AGENTS_DIR, file.replace(/\.md$/, ".agent.md")),
            exists: existsSync(join(COPILOT_AGENTS_DIR, file.replace(/\.md$/, ".agent.md"))),
          }))
      : [];

    const hookItems: InstallItem[] = HOOKS_TO_INSTALL.map((file) => ({
      name: file,
      category: "hook" as const,
      destPath: join(COPILOT_HOOKS_DIR, file),
      exists: existsSync(join(COPILOT_HOOKS_DIR, file)),
    }));

    // Include the translator shim and generated hooks.json
    const translatorItem: InstallItem = {
      name: "hooks-translator.py",
      category: "hook",
      destPath: join(COPILOT_HOOKS_DIR, "hooks-translator.py"),
      exists: existsSync(join(COPILOT_HOOKS_DIR, "hooks-translator.py")),
    };

    const guidelineItem: InstallItem = {
      name: "copilot-instructions.md",
      category: "guideline",
      destPath: COPILOT_GUIDELINES_FILE,
      exists: existsSync(COPILOT_GUIDELINES_FILE),
    };

    return {
      platform: this.name,
      targetDir: COPILOT_DIR,
      items: [...skillItems, ...agentItems, ...hookItems, translatorItem, guidelineItem],
    };
  }

  installSkills(sourceDir: string, exclude?: string[]): void {
    ensureDir(COPILOT_SKILLS_DIR);
    const skills = exclude?.length
      ? SKILLS_TO_INSTALL.filter((s) => !exclude.includes(s))
      : SKILLS_TO_INSTALL;
    for (const skill of skills) {
      const src = join(sourceDir, skill);
      if (existsSync(src) && statSync(src).isDirectory()) {
        copyDirRecursive(src, join(COPILOT_SKILLS_DIR, skill));
        log.step(`skill: ${skill}`);
      }
    }
  }

  installAgents(sourceDir: string, exclude?: string[]): void {
    ensureDir(COPILOT_AGENTS_DIR);
    const entries = readdirSync(sourceDir)
      .filter((f) => f.endsWith(".md"))
      .filter((f) => !exclude?.includes(f.replace(/\.md$/, "")));
    for (const file of entries) {
      const content = readFileSync(join(sourceDir, file), "utf8");
      const transformed = transformAgentForCopilot(content);
      // Copilot uses .agent.md extension
      const destFile = file.replace(/\.md$/, ".agent.md");
      writeFileSync(join(COPILOT_AGENTS_DIR, destFile), transformed);
      log.step(`agent: ${destFile}`);
    }
  }

  installGuidelines(_pluginRoot: string): void {
    ensureDir(COPILOT_DIR);
    writeFileSync(COPILOT_GUIDELINES_FILE, generateCopilotInstructionsMd());
    log.step(`guidelines: ${COPILOT_GUIDELINES_FILE}`);
  }

  installHooks(sourceDir: string, exclude?: string[]): void {
    ensureDir(COPILOT_HOOKS_DIR);

    // Copy hook scripts
    const hooks = exclude?.length
      ? HOOKS_TO_INSTALL.filter((f) => !exclude.includes(f))
      : HOOKS_TO_INSTALL;
    for (const file of hooks) {
      const src = join(sourceDir, file);
      if (existsSync(src)) {
        copyFileSync(src, join(COPILOT_HOOKS_DIR, file));
        log.step(`hook: ${file}`);
      }
    }

    // Copy the translator shim from the platform directory
    const shimSrc = join(__dirname, "hooks-translator.py");
    if (!existsSync(shimSrc)) {
      throw new Error(`hooks-translator.py not found at ${shimSrc} — packaging error`);
    }
    copyFileSync(shimSrc, join(COPILOT_HOOKS_DIR, "hooks-translator.py"));
    log.step("hook: hooks-translator.py (shim)");

    // Generate Copilot-specific hooks.json
    const hooksConfig = generateCopilotHooksConfig();
    const hooksConfigPath = join(COPILOT_HOOKS_DIR, "hooks.json");
    mergeCopilotHooksConfig(hooksConfigPath, hooksConfig);
    log.step("hook: hooks.json (generated for GitHub Copilot)");
  }

  postInstall(): void {
    log.info("GitHub Copilot install complete. Verify:");
    log.info(`  Skills:     ${COPILOT_SKILLS_DIR}`);
    log.info(`  Agents:     ${COPILOT_AGENTS_DIR}`);
    log.info(`  Hooks:      ${COPILOT_HOOKS_DIR}`);
    log.info(`  Guidelines: ${COPILOT_GUIDELINES_FILE}`);
  }
}

function mergeCopilotHooksConfig(
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

  // Start with version from new config
  existing.version = (newConfig as Record<string, unknown>).version ?? 1;

  if (!existing.hooks) {
    existing.hooks = {};
  }
  const existingHooks = existing.hooks as Record<string, unknown[]>;
  const incomingHooks = (newConfig as Record<string, unknown>).hooks as Record<string, Array<{ matcher?: string }>>;

  // Merge each event type: remove old ima-claude entries, then add new ones.
  // User hooks (without hooks-translator.py in the command) are preserved.
  for (const [event, entries] of Object.entries(incomingHooks)) {
    if (!existingHooks[event]) {
      existingHooks[event] = entries;
      continue;
    }

    // Strip all old ima-claude entries (identified by hooks-translator.py in the bash command)
    const userHooks = (existingHooks[event] as Array<{ bash?: string }>).filter(
      (h) => !h.bash?.includes("hooks-translator.py")
    );

    // Append new ima-claude entries
    existingHooks[event] = [...userHooks, ...entries];
  }

  writeFileSync(configPath, JSON.stringify(existing, null, 2) + "\n");
}
