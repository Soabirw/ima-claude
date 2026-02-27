#!/usr/bin/env bun

/**
 * Migrate from legacy ima-claude install to Claude Code plugin system.
 *
 * 1. Removes ima-claude skills from ~/.claude/skills/
 * 2. Removes ima-claude hooks from ~/.claude/hooks/
 * 3. Removes ima-claude rules from ~/.claude/rules/
 * 4. Removes ima-claude personalities from ~/.claude/personalities/
 * 5. Cleans ima-claude hook entries from ~/.claude/settings.json
 * 6. Removes ~/.claude/IMA_CLAUDE_INIT.md
 * 7. Prints instructions to install as plugin
 */

import { existsSync, rmSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const CLAUDE_DIR = join(homedir(), ".claude");
const SKILLS_DIR = join(CLAUDE_DIR, "skills");
const HOOKS_DIR = join(CLAUDE_DIR, "hooks");
const RULES_DIR = join(CLAUDE_DIR, "rules");
const SETTINGS_FILE = join(CLAUDE_DIR, "settings.json");

const DRY_RUN = process.argv.includes("--dry-run");

const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  cyan: "\x1b[36m",
};

const log = {
  info: (msg: string) => console.log(`${colors.cyan}i${colors.reset} ${msg}`),
  success: (msg: string) => console.log(`${colors.green}v${colors.reset} ${msg}`),
  warn: (msg: string) => console.log(`${colors.yellow}!${colors.reset} ${msg}`),
  error: (msg: string) => console.error(`${colors.red}x${colors.reset} ${msg}`),
  step: (msg: string) => console.log(`${colors.blue}>${colors.reset} ${msg}`),
};

// All known ima-claude skills
const SKILLS = [
  "functional-programmer", "task-master", "task-planner", "task-runner",
  "js-fp", "js-fp-api", "js-fp-react", "js-fp-vue", "js-fp-wordpress",
  "php-fp", "php-fp-wordpress", "quasar-fp", "jquery", "php-authnet",
  "architect", "docs-organize", "wp-local", "rg", "ima-forms-expert",
  "ima-brand", "ima-bootstrap", "jira-checkpoint", "playwright",
  "compound-bridge", "mcp-atlassian", "mcp-tavily", "mcp-context7",
  "mcp-serena", "mcp-sequential", "mcp-memory", "mcp-vestige", "mcp-qdrant",
  "quickstart", "scorecard", "save-session", "resume-session",
  "skill-analyzer", "skill-creator", "phpunit-wp",
];

// All known ima-claude hook files
const HOOKS = [
  "enforce_rg_over_grep.py", "tavily_extract_advanced.py",
  "webfetch_to_tavily.py", "websearch_to_tavily.py",
  "prompt_coach.py", "prompt_coach_system.md", "prompt_coach_digest.md",
  "memory_bootstrap.py", "memory_store_reminder.py", "vestige_before_external.py",
  "task_master_after_plan.py", "task_master_before_impl.py", "jira_issue_fetch.py",
  "wp_security_check.py", "sql_injection_check.py",
  "atlassian_prereqs.py", "serena_project_check.py", "serena_over_grep.py",
  "fp_utility_check.py", "jquery_in_wordpress.py", "bootstrap_utility_check.py",
  "composer_autoload_check.py", "docs_organization.py",
];

const RULES = ["memory-after-work.md"];
const PERSONALITIES = ["enable-40k.md", "enable-templars.md"];

function remove(path: string, label: string): boolean {
  if (!existsSync(path)) return false;
  if (DRY_RUN) {
    log.step(`[dry-run] Would remove: ${label}`);
    return true;
  }
  try {
    rmSync(path, { recursive: true, force: true });
    return true;
  } catch (err) {
    log.warn(`Failed to remove ${label}: ${(err as Error).message}`);
    return false;
  }
}

function cleanSettingsHooks(): number {
  if (!existsSync(SETTINGS_FILE)) return 0;

  let settings: Record<string, unknown>;
  try {
    settings = JSON.parse(readFileSync(SETTINGS_FILE, "utf8"));
  } catch {
    return 0;
  }

  const hooks = settings.hooks as Record<string, unknown[]> | undefined;
  if (!hooks) return 0;

  const imaHookPath = `${HOOKS_DIR}/`;
  let removed = 0;

  for (const [event, matchers] of Object.entries(hooks)) {
    if (!Array.isArray(matchers)) continue;

    const filtered = matchers.filter((matcher: unknown) => {
      const m = matcher as Record<string, unknown>;
      const hookList = m.hooks as Array<Record<string, string>> | undefined;
      if (!hookList) return true;

      const cleaned = hookList.filter(h => !h.command?.includes(imaHookPath));
      if (cleaned.length === 0) {
        removed++;
        return false;
      }
      if (cleaned.length < hookList.length) {
        m.hooks = cleaned;
        removed += hookList.length - cleaned.length;
      }
      return true;
    });

    hooks[event] = filtered;
  }

  if (removed > 0 && !DRY_RUN) {
    writeFileSync(SETTINGS_FILE, JSON.stringify(settings, null, 2) + "\n");
  }

  return removed;
}

async function main() {
  console.log(`\n${colors.bright}ima-claude: Migrate to Plugin System${colors.reset}\n`);

  if (DRY_RUN) {
    log.info("Running in dry-run mode — no files will be modified\n");
  }

  if (!existsSync(CLAUDE_DIR)) {
    log.error("~/.claude not found. Nothing to migrate.");
    process.exit(1);
  }

  // 1. Remove ima-claude skills
  let skillsRemoved = 0;
  if (existsSync(SKILLS_DIR)) {
    log.step("Removing ima-claude skills...");
    for (const skill of SKILLS) {
      if (remove(join(SKILLS_DIR, skill), `skill: ${skill}`)) skillsRemoved++;
    }
    log.success(`Removed ${skillsRemoved} skills`);
  }

  // 2. Remove ima-claude hooks
  let hooksRemoved = 0;
  if (existsSync(HOOKS_DIR)) {
    log.step("Removing ima-claude hooks...");
    for (const hook of HOOKS) {
      if (remove(join(HOOKS_DIR, hook), `hook: ${hook}`)) hooksRemoved++;
    }
    log.success(`Removed ${hooksRemoved} hooks`);
  }

  // 3. Remove ima-claude rules
  let rulesRemoved = 0;
  if (existsSync(RULES_DIR)) {
    log.step("Removing ima-claude rules...");
    for (const rule of RULES) {
      if (remove(join(RULES_DIR, rule), `rule: ${rule}`)) rulesRemoved++;
    }
    log.success(`Removed ${rulesRemoved} rules`);
  }

  // 4. Remove personalities
  const personalitiesDir = join(CLAUDE_DIR, "personalities");
  let personalitiesRemoved = 0;
  if (existsSync(personalitiesDir)) {
    log.step("Removing ima-claude personalities...");
    for (const p of PERSONALITIES) {
      if (remove(join(personalitiesDir, p), `personality: ${p}`)) personalitiesRemoved++;
    }
    log.success(`Removed ${personalitiesRemoved} personalities`);
  }

  // 5. Clean hook entries from settings.json
  log.step("Cleaning hook entries from settings.json...");
  const hookEntriesRemoved = cleanSettingsHooks();
  if (hookEntriesRemoved > 0) {
    log.success(`Cleaned ${hookEntriesRemoved} hook entries from settings.json`);
  } else {
    log.info("No hook entries to clean");
  }

  // 6. Remove IMA_CLAUDE_INIT.md
  if (remove(join(CLAUDE_DIR, "IMA_CLAUDE_INIT.md"), "IMA_CLAUDE_INIT.md")) {
    log.success("Removed IMA_CLAUDE_INIT.md");
  }

  // Summary
  const total = skillsRemoved + hooksRemoved + rulesRemoved + personalitiesRemoved;
  console.log(`\n${colors.bright}Migration cleanup complete${colors.reset}`);
  console.log(`   Removed: ${total} files/directories + ${hookEntriesRemoved} settings entries\n`);

  console.log(`${colors.bright}Next steps:${colors.reset}`);
  console.log(`   1. Add the marketplace:`);
  console.log(`      ${colors.cyan}/plugin marketplace add your-org/ima-claude${colors.reset}`);
  console.log(`   2. Install the plugin:`);
  console.log(`      ${colors.cyan}/plugin install ima-claude${colors.reset}`);
  console.log(`   3. Verify skills load:`);
  console.log(`      ${colors.cyan}/ima-claude:quickstart${colors.reset}`);
  console.log("");

  if (DRY_RUN) {
    console.log(`${colors.yellow}This was a dry run. Run without --dry-run to apply changes.${colors.reset}\n`);
  }
}

main().catch((err) => {
  log.error(`Migration failed: ${err.message}`);
  process.exit(1);
});
