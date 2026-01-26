import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync, readFileSync, writeFileSync, unlinkSync, chmodSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";

export const CLAUDE_DIR = join(homedir(), ".claude");
export const SKILLS_DIR = join(CLAUDE_DIR, "skills");
export const HOOKS_DIR = join(CLAUDE_DIR, "hooks");
export const SETTINGS_FILE = join(CLAUDE_DIR, "settings.json");
export const VERSION = "1.2.0";

export const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  cyan: "\x1b[36m",
};

export const log = {
  info: (msg: string) => console.log(`${colors.cyan}ℹ${colors.reset} ${msg}`),
  success: (msg: string) => console.log(`${colors.green}✅${colors.reset} ${msg}`),
  warn: (msg: string) => console.log(`${colors.yellow}⚠️${colors.reset} ${msg}`),
  error: (msg: string) => console.error(`${colors.red}❌${colors.reset} ${msg}`),
  step: (msg: string) => console.log(`${colors.blue}→${colors.reset} ${msg}`),
};

export function ensureDir(dir: string): void {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

export function copyDirRecursive(src: string, dest: string): void {
  ensureDir(dest);
  const entries = readdirSync(src);

  for (const entry of entries) {
    const srcPath = join(src, entry);
    const destPath = join(dest, entry);
    const stat = statSync(srcPath);

    if (stat.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      // Remove existing file first (handles read-only files)
      if (existsSync(destPath)) {
        try {
          unlinkSync(destPath);
        } catch {
          // If unlink fails, try to make it writable first
          chmodSync(destPath, 0o644);
          unlinkSync(destPath);
        }
      }
      copyFileSync(srcPath, destPath);
    }
  }
}

export function checkClaudeCode(): boolean {
  return existsSync(CLAUDE_DIR);
}

export function checkSuperClaude(): boolean {
  // Check for SuperClaude by looking for COMMANDS.md
  return existsSync(join(CLAUDE_DIR, "COMMANDS.md"));
}

/**
 * Check if ima-claude is already installed by looking for our skills
 */
export function isImaClaudeInstalled(): boolean {
  // Check for at least one of our core skills
  const coreSkills = ["js-fp", "php-fp", "architect"];
  return coreSkills.some(skill =>
    existsSync(join(SKILLS_DIR, skill, "SKILL.md"))
  );
}

export function backupDir(dir: string, backupName: string): string {
  const backupPath = join(dirname(dir), backupName);
  if (existsSync(dir)) {
    copyDirRecursive(dir, backupPath);
  }
  return backupPath;
}

export function getInstalledSkills(): string[] {
  if (!existsSync(SKILLS_DIR)) {
    return [];
  }
  return readdirSync(SKILLS_DIR).filter((name) => {
    const skillPath = join(SKILLS_DIR, name);
    return statSync(skillPath).isDirectory() && existsSync(join(skillPath, "SKILL.md"));
  });
}

export function readVersion(skillDir: string): string | null {
  const skillMd = join(skillDir, "SKILL.md");
  if (!existsSync(skillMd)) return null;

  try {
    const content = readFileSync(skillMd, "utf8");
    const match = content.match(/version:\s*["']?([^"'\n]+)["']?/);
    return match ? match[1] : null;
  } catch {
    return null;
  }
}

export function promptYesNo(question: string): boolean {
  const rl = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise<boolean>((resolve) => {
    rl.question(`${question} [y/N] `, (answer: string) => {
      rl.close();
      resolve(answer.toLowerCase() === "y" || answer.toLowerCase() === "yes");
    });
  }) as unknown as boolean;
}

export const SKILLS_TO_INSTALL = [
  "js-fp",
  "js-fp-api",
  "js-fp-react",
  "js-fp-vue",
  "js-fp-wordpress",
  "php-fp",
  "php-fp-wordpress",
  "quasar-fp",
  "architect",
  "docs-organize",
  "skill-analyzer",
  "skill-creator",
];

export const PERSONALITIES_TO_INSTALL = [
  "enable-40k.md",
  "enable-templars.md",
];

export const HOOKS_TO_INSTALL = [
  "enforce_rg_over_grep.py",
  "tavily_extract_advanced.py",
  "webfetch_to_tavily.py",
  "websearch_to_tavily.py",
];

// Hook configuration to merge into settings.json
export const HOOKS_CONFIG = {
  hooks: {
    preToolUse: [
      {
        matcher: "Bash",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/enforce_rg_over_grep.py` }
        ]
      },
      {
        matcher: "mcp__tavily__tavily-extract",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/tavily_extract_advanced.py` }
        ]
      },
      {
        matcher: "WebFetch",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/webfetch_to_tavily.py` }
        ]
      },
      {
        matcher: "WebSearch",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/websearch_to_tavily.py` }
        ]
      }
    ]
  }
};

/**
 * Merge ima-claude hooks config into existing settings.json
 * Preserves existing settings, adds/updates hooks section
 */
export function mergeHooksIntoSettings(): { merged: boolean; created: boolean } {
  let settings: Record<string, unknown> = {};
  let created = false;

  // Read existing settings if present
  if (existsSync(SETTINGS_FILE)) {
    try {
      const content = readFileSync(SETTINGS_FILE, "utf8");
      settings = JSON.parse(content);
    } catch {
      // If parse fails, start fresh but preserve the file
      settings = {};
    }
  } else {
    created = true;
  }

  // Merge hooks config
  // If hooks.preToolUse exists, merge arrays (avoid duplicates by matcher)
  if (settings.hooks && (settings.hooks as Record<string, unknown>).preToolUse) {
    const existingHooks = (settings.hooks as Record<string, unknown>).preToolUse as Array<{ matcher: string }>;
    const newHooks = HOOKS_CONFIG.hooks.preToolUse;

    for (const newHook of newHooks) {
      const existingIndex = existingHooks.findIndex(h => h.matcher === newHook.matcher);
      if (existingIndex >= 0) {
        // Replace existing hook with same matcher
        existingHooks[existingIndex] = newHook;
      } else {
        // Add new hook
        existingHooks.push(newHook);
      }
    }
  } else {
    // No existing hooks, just add ours
    settings.hooks = HOOKS_CONFIG.hooks;
  }

  // Write back
  writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2) + "\n");

  return { merged: true, created };
}
