#!/usr/bin/env bun

import { existsSync, copyFileSync, readdirSync, chmodSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import {
  CLAUDE_DIR,
  SKILLS_DIR,
  HOOKS_DIR,
  COMMANDS_DIR,
  VERSION,
  log,
  colors,
  ensureDir,
  copyDirRecursive,
  checkClaudeCode,
  checkSuperClaude,
  isImaClaudeInstalled,
  mergeHooksIntoSettings,
  SKILLS_TO_INSTALL,
  PERSONALITIES_TO_INSTALL,
  HOOKS_TO_INSTALL,
  COMMANDS_TO_INSTALL,
} from "./utils";

const args = process.argv.slice(2);
const reinstall = args.includes("--reinstall");

async function main() {
  const isUpgrade = isImaClaudeInstalled() && !reinstall;
  const action = isUpgrade ? "Upgrading" : "Installing";
  const emoji = isUpgrade ? "🔄" : "🚀";

  console.log(`\n${colors.bright}${emoji} ${action} ima-claude v${VERSION}${colors.reset}\n`);

  // Step 1: Check for Claude Code
  if (!checkClaudeCode()) {
    log.error("~/.claude not found. Install Claude Code first.");
    console.log("   Visit: https://claude.ai/code\n");
    process.exit(1);
  }
  log.success("Claude Code detected");

  // Step 2: Check for SuperClaude (optional) - only on fresh install
  if (!isUpgrade) {
    const hasSuperClaude = checkSuperClaude();
    if (hasSuperClaude) {
      log.success("SuperClaude detected - skills will integrate with personas");
    } else {
      log.warn("SuperClaude not detected");
      console.log("   ima-claude works best with SuperClaude installed.");
      console.log("   Visit: https://github.com/SuperClaude-Org/SuperClaude_Framework\n");
      console.log("   Continuing with standalone installation...\n");
    }
  }

  // Step 3: Get script directory (where ima-claude source is)
  const scriptDir = dirname(import.meta.dir);
  const skillsSource = join(scriptDir, "skills");
  const personalitiesSource = join(scriptDir, "personalities");

  if (!existsSync(skillsSource)) {
    log.error(`Skills source not found at: ${skillsSource}`);
    log.error("Make sure you're running from the ima-claude directory");
    process.exit(1);
  }

  // Step 4: Backup on --reinstall only
  if (reinstall && existsSync(SKILLS_DIR)) {
    const existingSkills = readdirSync(SKILLS_DIR);
    const conflictingSkills = SKILLS_TO_INSTALL.filter((s) =>
      existingSkills.includes(s)
    );

    if (conflictingSkills.length > 0) {
      const backupName = `skills.backup.${Date.now()}`;
      const backupPath = join(CLAUDE_DIR, backupName);
      log.step(`Backing up existing skills to ${backupName}`);

      for (const skill of conflictingSkills) {
        const srcSkill = join(SKILLS_DIR, skill);
        const destSkill = join(backupPath, skill);
        ensureDir(dirname(destSkill));
        copyDirRecursive(srcSkill, destSkill);
      }
      log.success(`Backed up ${conflictingSkills.length} existing skills`);
    }
  }

  // Step 5: Ensure skills directory exists
  ensureDir(SKILLS_DIR);

  // Step 6: Install/upgrade skills
  const skillVerb = isUpgrade ? "Upgrading" : "Installing";
  const skillSymbol = isUpgrade ? "↻" : "✓";
  log.step(`${skillVerb} skills...`);
  let installedCount = 0;

  for (const skill of SKILLS_TO_INSTALL) {
    const src = join(skillsSource, skill);
    const dest = join(SKILLS_DIR, skill);

    if (!existsSync(src)) {
      log.warn(`Skill not found: ${skill} (skipping)`);
      continue;
    }

    copyDirRecursive(src, dest);
    console.log(`   ${colors.green}${skillSymbol}${colors.reset} ${skill}`);
    installedCount++;
  }

  log.success(`${isUpgrade ? "Upgraded" : "Installed"} ${installedCount} skills`);

  // Step 7: Install .skill files (if any)
  const skillFiles = readdirSync(skillsSource).filter((f) => f.endsWith(".skill"));
  if (skillFiles.length > 0) {
    log.step(`${skillVerb} .skill files...`);
    for (const file of skillFiles) {
      const dest = join(SKILLS_DIR, file);
      // Handle read-only files
      if (existsSync(dest)) {
        try { chmodSync(dest, 0o644); } catch {}
      }
      copyFileSync(join(skillsSource, file), dest);
      console.log(`   ${colors.green}${skillSymbol}${colors.reset} ${file}`);
    }
  }

  // Step 8: Install personalities
  if (existsSync(personalitiesSource)) {
    const personalitiesDir = join(CLAUDE_DIR, "personalities");
    ensureDir(personalitiesDir);

    log.step(`${skillVerb} personalities...`);
    for (const file of PERSONALITIES_TO_INSTALL) {
      const src = join(personalitiesSource, file);
      const dest = join(personalitiesDir, file);
      if (existsSync(src)) {
        // Handle read-only files
        if (existsSync(dest)) {
          try { chmodSync(dest, 0o644); } catch {}
        }
        copyFileSync(src, dest);
        console.log(`   ${colors.green}${skillSymbol}${colors.reset} ${file}`);
      }
    }
    // Copy README
    const readmeSrc = join(personalitiesSource, "README.md");
    if (existsSync(readmeSrc)) {
      const readmeDest = join(personalitiesDir, "README.md");
      if (existsSync(readmeDest)) {
        try { chmodSync(readmeDest, 0o644); } catch {}
      }
      copyFileSync(readmeSrc, readmeDest);
    }
  }

  // Step 9: Install hooks
  const hooksSource = join(scriptDir, "hooks");
  if (existsSync(hooksSource)) {
    ensureDir(HOOKS_DIR);

    log.step(`${skillVerb} hooks...`);
    let hooksInstalled = 0;

    for (const hook of HOOKS_TO_INSTALL) {
      const src = join(hooksSource, hook);
      const dest = join(HOOKS_DIR, hook);

      if (existsSync(src)) {
        // Handle read-only files
        if (existsSync(dest)) {
          try { chmodSync(dest, 0o644); } catch {}
        }
        copyFileSync(src, dest);
        chmodSync(dest, 0o755);
        console.log(`   ${colors.green}${skillSymbol}${colors.reset} ${hook}`);
        hooksInstalled++;
      }
    }

    // Copy hooks README
    const hooksReadme = join(hooksSource, "README.md");
    if (existsSync(hooksReadme)) {
      const dest = join(HOOKS_DIR, "README.md");
      if (existsSync(dest)) {
        try { chmodSync(dest, 0o644); } catch {}
      }
      copyFileSync(hooksReadme, dest);
    }

    log.success(`${isUpgrade ? "Upgraded" : "Installed"} ${hooksInstalled} hooks`);

    // Step 10: Configure hooks in settings.json
    log.step("Configuring hooks in settings.json...");
    const { created } = mergeHooksIntoSettings();
    if (created) {
      log.success("Created settings.json with hook configuration");
    } else {
      log.success("Merged hook configuration into settings.json");
    }
  }

  // Step 11: Install commands
  const commandsSource = join(scriptDir, "commands");
  if (existsSync(commandsSource)) {
    ensureDir(COMMANDS_DIR);

    log.step(`${skillVerb} commands...`);
    let commandsInstalled = 0;

    for (const cmd of COMMANDS_TO_INSTALL) {
      const src = join(commandsSource, cmd);
      const dest = join(COMMANDS_DIR, cmd);

      if (existsSync(src)) {
        // Handle read-only files
        if (existsSync(dest)) {
          try { chmodSync(dest, 0o644); } catch {}
        }
        copyFileSync(src, dest);
        console.log(`   ${colors.green}${skillSymbol}${colors.reset} ${cmd}`);
        commandsInstalled++;
      }
    }

    log.success(`${isUpgrade ? "Upgraded" : "Installed"} ${commandsInstalled} commands`);
  }

  // Step 12: Install IMA_CLAUDE_INIT.md (bootstrap file)
  const initFile = join(scriptDir, "IMA_CLAUDE_INIT.md");
  if (existsSync(initFile)) {
    const dest = join(CLAUDE_DIR, "IMA_CLAUDE_INIT.md");
    log.step(`${skillVerb} IMA_CLAUDE_INIT.md...`);
    if (existsSync(dest)) {
      try { chmodSync(dest, 0o644); } catch {}
    }
    copyFileSync(initFile, dest);
    console.log(`   ${colors.green}${skillSymbol}${colors.reset} IMA_CLAUDE_INIT.md`);
    log.success("Bootstrap file installed");
  }

  // Step 13: Create local-skills template directory (only on fresh install)
  const localSkillsDir = join(SKILLS_DIR, ".local");
  if (!existsSync(localSkillsDir)) {
    ensureDir(localSkillsDir);
    const placeholderContent = `# Local Skills

Place your private/project-specific skills here.
This directory is gitignored by ima-claude.

## Creating a Local Skill

1. Create a new directory: \`my-project-skill/\`
2. Add a SKILL.md file with frontmatter
3. The skill will auto-discover

Example:
\`\`\`
my-project-skill/
├── SKILL.md
└── references/
    └── api-patterns.md
\`\`\`
`;
    writeFileSync(join(localSkillsDir, "README.md"), placeholderContent);
    log.success("Created .local directory for private skills");
  }

  // Summary
  const doneEmoji = isUpgrade ? "🔄" : "✅";
  const doneVerb = isUpgrade ? "upgraded" : "installed";
  console.log(`\n${colors.bright}${doneEmoji} ima-claude ${doneVerb} successfully!${colors.reset}\n`);
  console.log(`   Skills:        ${SKILLS_DIR}/`);
  console.log(`   Personalities: ${CLAUDE_DIR}/personalities/`);
  console.log(`   Hooks:         ${HOOKS_DIR}/`);
  console.log(`   Commands:      ${COMMANDS_DIR}/`);
  console.log("");

  if (!isUpgrade) {
    console.log("   Quick Start:");
    console.log(`   ${colors.cyan}"Use the js-fp skill to review this code"${colors.reset}`);
    console.log(`   ${colors.cyan}"Apply architect patterns to this design"${colors.reset}`);
    console.log(`   ${colors.cyan}/save-session${colors.reset} - Save session state`);
    console.log(`   ${colors.cyan}/resume-session${colors.reset} - Resume saved session`);
    console.log("");

    if (!checkSuperClaude()) {
      console.log(`   ${colors.yellow}Tip: Install SuperClaude for enhanced features${colors.reset}`);
      console.log("");
    }
  }
}

main().catch((err) => {
  log.error(`Installation failed: ${err.message}`);
  process.exit(1);
});
