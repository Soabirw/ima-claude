#!/usr/bin/env bun

import { existsSync, readdirSync, readFileSync, statSync } from "fs";
import { join, dirname } from "path";
import {
  CLAUDE_DIR,
  SKILLS_DIR,
  VERSION,
  log,
  colors,
  ensureDir,
  copyDirRecursive,
  checkClaudeCode,
  SKILLS_TO_INSTALL,
} from "./utils";

interface SkillStatus {
  name: string;
  installed: boolean;
  hasLocalChanges: boolean;
  action: "update" | "skip" | "new";
}

function getFileHash(path: string): string {
  if (!existsSync(path)) return "";
  try {
    const content = readFileSync(path, "utf8");
    // Simple hash for comparison
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return hash.toString(16);
  } catch {
    return "";
  }
}

function checkLocalChanges(skillName: string, sourceDir: string): boolean {
  const installedDir = join(SKILLS_DIR, skillName);
  const sourceSkillDir = join(sourceDir, skillName);

  if (!existsSync(installedDir)) return false;

  // Compare SKILL.md files
  const installedSkill = join(installedDir, "SKILL.md");
  const sourceSkill = join(sourceSkillDir, "SKILL.md");

  if (!existsSync(sourceSkill)) return false;

  // If hashes are different, there might be local changes
  // This is a simple heuristic - could be improved with git-style tracking
  const installedHash = getFileHash(installedSkill);
  const sourceHash = getFileHash(sourceSkill);

  return installedHash !== sourceHash;
}

async function main() {
  console.log(`\n${colors.bright}🔄 Upgrading ima-claude to v${VERSION}${colors.reset}\n`);

  // Check prerequisites
  if (!checkClaudeCode()) {
    log.error("~/.claude not found. Run install first.");
    process.exit(1);
  }

  if (!existsSync(SKILLS_DIR)) {
    log.error("Skills directory not found. Run install first.");
    console.log("   Try: bun run install.ts");
    process.exit(1);
  }

  // Get script directory
  const scriptDir = dirname(import.meta.dir);
  const skillsSource = join(scriptDir, "skills");

  if (!existsSync(skillsSource)) {
    log.error(`Skills source not found at: ${skillsSource}`);
    process.exit(1);
  }

  // Analyze skills
  log.step("Analyzing installed skills...");
  const statuses: SkillStatus[] = [];

  for (const skill of SKILLS_TO_INSTALL) {
    const installed = existsSync(join(SKILLS_DIR, skill));
    const hasLocalChanges = installed && checkLocalChanges(skill, skillsSource);

    statuses.push({
      name: skill,
      installed,
      hasLocalChanges,
      action: !installed ? "new" : hasLocalChanges ? "skip" : "update",
    });
  }

  // Display status
  console.log("");
  console.log("   Skill Status:");
  for (const status of statuses) {
    const icon =
      status.action === "new"
        ? `${colors.green}+${colors.reset}`
        : status.action === "skip"
        ? `${colors.yellow}~${colors.reset}`
        : `${colors.blue}↻${colors.reset}`;
    const note =
      status.action === "new"
        ? "(new)"
        : status.action === "skip"
        ? "(local changes, skipping)"
        : "(update)";
    console.log(`   ${icon} ${status.name} ${colors.cyan}${note}${colors.reset}`);
  }
  console.log("");

  // Check for skills with local changes
  const skipped = statuses.filter((s) => s.action === "skip");
  if (skipped.length > 0) {
    log.warn(`${skipped.length} skill(s) have local modifications and will be skipped`);
    console.log("   To force update, backup and reinstall:");
    console.log(`   ${colors.cyan}mv ~/.claude/skills/SKILL_NAME ~/.claude/skills/SKILL_NAME.backup${colors.reset}`);
    console.log(`   ${colors.cyan}bun run upgrade.ts${colors.reset}`);
    console.log("");
  }

  // Perform upgrades
  const toUpgrade = statuses.filter((s) => s.action !== "skip");

  if (toUpgrade.length === 0) {
    log.success("All skills are up to date!");
    return;
  }

  log.step(`Upgrading ${toUpgrade.length} skills...`);

  for (const status of toUpgrade) {
    const src = join(skillsSource, status.name);
    const dest = join(SKILLS_DIR, status.name);

    if (!existsSync(src)) {
      log.warn(`Source not found for ${status.name} (skipping)`);
      continue;
    }

    copyDirRecursive(src, dest);
    const icon = status.action === "new" ? "+" : "↻";
    console.log(`   ${colors.green}${icon}${colors.reset} ${status.name}`);
  }

  // Update .skill files
  log.step("Updating .skill files...");
  const skillFiles = readdirSync(skillsSource).filter((f) => f.endsWith(".skill"));
  for (const file of skillFiles) {
    const src = join(skillsSource, file);
    const dest = join(SKILLS_DIR, file);
    const fs = await import("fs");
    fs.copyFileSync(src, dest);
    console.log(`   ${colors.green}↻${colors.reset} ${file}`);
  }

  // Summary
  console.log(`\n${colors.bright}✅ Upgrade complete!${colors.reset}\n`);

  const newCount = statuses.filter((s) => s.action === "new").length;
  const updateCount = statuses.filter((s) => s.action === "update").length;
  const skipCount = skipped.length;

  console.log(`   New:     ${newCount} skills`);
  console.log(`   Updated: ${updateCount} skills`);
  console.log(`   Skipped: ${skipCount} skills (local changes preserved)`);
  console.log("");
}

main().catch((err) => {
  log.error(`Upgrade failed: ${err.message}`);
  process.exit(1);
});
