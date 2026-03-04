import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync, readFileSync, writeFileSync, unlinkSync, chmodSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";

export const CLAUDE_DIR = join(homedir(), ".claude");
export const SKILLS_DIR = join(CLAUDE_DIR, "skills");
export const HOOKS_DIR = join(CLAUDE_DIR, "hooks");
export const COMMANDS_DIR = join(CLAUDE_DIR, "commands");
export const RULES_DIR = join(CLAUDE_DIR, "rules");
export const SETTINGS_FILE = join(CLAUDE_DIR, "settings.json");
export const VERSION = "2.5.0";

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
  // Foundational skills
  "functional-programmer",
  "task-master",
  "task-planner",
  "task-runner",
  // FP implementation skills
  "js-fp",
  "js-fp-api",
  "js-fp-react",
  "js-fp-vue",
  "js-fp-wordpress",
  "php-fp",
  "php-fp-wordpress",
  "quasar-fp",
  "jquery",
  // Payment & API skills
  "php-authnet",
  // Domain expert skills
  "architect",
  "docs-organize",
  "wp-local",
  "rg",
  "ima-forms-expert",
  "ima-brand",
  "ima-bootstrap",
  "jira-checkpoint",
  // Testing skills
  "playwright",
  // Discourse skills
  "discourse",
  "discourse-admin",
  "ember-discourse",
  // Integration skills
  "compound-bridge",
  // MCP integration skills
  "mcp-atlassian",
  "mcp-tavily",
  "mcp-context7",
  "mcp-serena",
  "mcp-sequential",
  "mcp-memory",
  "mcp-vestige",
  "mcp-qdrant",
  // Quick reference
  "quickstart",
  "scorecard",
  // Session management skills
  "save-session",
  "resume-session",
  // Meta skills
  "skill-analyzer",
  "skill-creator",
];

export const PERSONALITIES_TO_INSTALL = [
  "enable-40k.md",
  "enable-templars.md",
];

export const HOOKS_TO_INSTALL = [
  // Tool redirection hooks
  "enforce_rg_over_grep.py",
  "tavily_extract_advanced.py",
  "webfetch_to_tavily.py",
  "websearch_to_tavily.py",
  // Prompt coaching
  "prompt_coach.py",
  "prompt_coach_system.md",
  "prompt_coach_digest.md",
  // Memory system hooks
  "memory_bootstrap.py",
  "memory_store_reminder.py",
  "vestige_before_external.py",
  // Workflow hooks
  "task_master_after_plan.py",
  "task_master_before_impl.py",
  "jira_issue_fetch.py",
  // Security hooks
  "wp_security_check.py",
  "sql_injection_check.py",
  // Atlassian prerequisite hooks
  "atlassian_prereqs.py",
  // Serena hooks
  "serena_project_check.py",
  "serena_over_grep.py",
  "serena_over_read.py",
  // Sequential Thinking hooks
  "sequential_thinking_check.py",
  // Code quality hooks
  "fp_utility_check.py",
  "jquery_in_wordpress.py",
  "bootstrap_utility_check.py",
  "composer_autoload_check.py",
  "docs_organization.py",
];

export const COMMANDS_TO_INSTALL = [
  // Commands moved to skills in v1.6.0
  // - save-session (now a skill using Serena MCP)
  // - resume-session (now a skill using Serena MCP)
];

export const RULES_TO_INSTALL = [
  "memory-after-work.md",
];

// Serena JetBrains tools that need WP project path check
const SERENA_JETBRAINS_TOOLS = [
  "mcp__serena__jet_brains_find_symbol",
  "mcp__serena__jet_brains_find_referencing_symbols",
  "mcp__serena__jet_brains_get_symbols_overview",
  "mcp__serena__jet_brains_type_hierarchy",
];

// Atlassian tools that need prereq checks (H3/H4/M5)
const ATLASSIAN_TOOLS_WITH_PREREQS = [
  "mcp__claude_ai_Atlassian__getJiraIssue",
  "mcp__claude_ai_Atlassian__editJiraIssue",
  "mcp__claude_ai_Atlassian__createJiraIssue",
  "mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql",
  "mcp__claude_ai_Atlassian__transitionJiraIssue",
  "mcp__claude_ai_Atlassian__addCommentToJiraIssue",
  "mcp__claude_ai_Atlassian__getConfluencePage",
  "mcp__claude_ai_Atlassian__createConfluencePage",
  "mcp__claude_ai_Atlassian__updateConfluencePage",
  "mcp__claude_ai_Atlassian__searchConfluenceUsingCql",
  "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources",
  "mcp__claude_ai_Atlassian__getTransitionsForJiraIssue",
];

// Hook configuration to merge into settings.json
export const HOOKS_CONFIG = {
  hooks: {
    PreToolUse: [
      {
        matcher: "Bash",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/enforce_rg_over_grep.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` }
        ]
      },
      {
        matcher: "Read",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/serena_over_read.py` }
        ]
      },
      {
        matcher: "Edit",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` }
        ]
      },
      {
        matcher: "Write",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` }
        ]
      },
      {
        matcher: "Glob",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` }
        ]
      },
      {
        matcher: "Grep",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_bootstrap.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/serena_over_grep.py` }
        ]
      },
      {
        matcher: "mcp__tavily__tavily-extract",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/tavily_extract_advanced.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/vestige_before_external.py` }
        ]
      },
      {
        matcher: "mcp__tavily__tavily_search",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/vestige_before_external.py` }
        ]
      },
      {
        matcher: "mcp__tavily__tavily_research",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/vestige_before_external.py` }
        ]
      },
      {
        matcher: "mcp__context7__resolve-library-id",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/vestige_before_external.py` }
        ]
      },
      {
        matcher: "mcp__context7__query-docs",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/vestige_before_external.py` }
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
      },
      // Serena WP project path checks
      ...SERENA_JETBRAINS_TOOLS.map(tool => ({
        matcher: tool,
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/serena_project_check.py` }
        ]
      })),
      // Atlassian prerequisite checks
      ...ATLASSIAN_TOOLS_WITH_PREREQS.map(tool => ({
        matcher: tool,
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/atlassian_prereqs.py` }
        ]
      }))
    ],
    PostToolUse: [
      {
        matcher: "Edit",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_store_reminder.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/wp_security_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/sql_injection_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/fp_utility_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/jquery_in_wordpress.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/bootstrap_utility_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/composer_autoload_check.py` }
        ]
      },
      {
        matcher: "Write",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/memory_store_reminder.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/wp_security_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/sql_injection_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/fp_utility_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/jquery_in_wordpress.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/bootstrap_utility_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/composer_autoload_check.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/docs_organization.py` }
        ]
      },
      {
        matcher: "ExitPlanMode",
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/task_master_after_plan.py` }
        ]
      }
    ],
    UserPromptSubmit: [
      {
        hooks: [
          { type: "command", command: `python3 ${HOOKS_DIR}/prompt_coach.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/jira_issue_fetch.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/task_master_before_impl.py` },
          { type: "command", command: `python3 ${HOOKS_DIR}/sequential_thinking_check.py` }
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

  // Initialize hooks object if not present
  if (!settings.hooks) {
    settings.hooks = {};
  }
  const settingsHooks = settings.hooks as Record<string, unknown>;

  // Merge PreToolUse hooks (match by matcher field)
  if (settingsHooks.PreToolUse) {
    const existingHooks = settingsHooks.PreToolUse as Array<{ matcher: string }>;
    const newHooks = HOOKS_CONFIG.hooks.PreToolUse;

    for (const newHook of newHooks) {
      const existingIndex = existingHooks.findIndex(h => h.matcher === newHook.matcher);
      if (existingIndex >= 0) {
        existingHooks[existingIndex] = newHook;
      } else {
        existingHooks.push(newHook);
      }
    }
  } else {
    settingsHooks.PreToolUse = HOOKS_CONFIG.hooks.PreToolUse;
  }

  // Merge PostToolUse hooks (match by matcher field)
  if (settingsHooks.PostToolUse) {
    const existingHooks = settingsHooks.PostToolUse as Array<{ matcher: string }>;
    const newHooks = HOOKS_CONFIG.hooks.PostToolUse;

    for (const newHook of newHooks) {
      const existingIndex = existingHooks.findIndex(h => h.matcher === newHook.matcher);
      if (existingIndex >= 0) {
        existingHooks[existingIndex] = newHook;
      } else {
        existingHooks.push(newHook);
      }
    }
  } else {
    settingsHooks.PostToolUse = HOOKS_CONFIG.hooks.PostToolUse;
  }

  // Merge UserPromptSubmit hooks (replace entire array since no matcher field)
  settingsHooks.UserPromptSubmit = HOOKS_CONFIG.hooks.UserPromptSubmit;

  // Write back
  writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2) + "\n");

  return { merged: true, created };
}
