#!/usr/bin/env bun

/**
 * Backup critical ~/.claude content before a fresh start.
 *
 * Backs up:
 * - settings.json (MCP configs, model preferences)
 * - settings.local.json (permissions, output style)
 * - hooks/ (custom pre-tool-use hooks)
 * - todos/ (if active tasks exist)
 *
 * Warns about:
 * - .credentials.json (requires manual secure handling)
 *
 * Skips:
 * - projects/ (large, only for /resume, rarely used)
 * - debug/, cache/, file-history/ (regenerated)
 */

import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync, readFileSync } from "fs";
import { join, basename } from "path";
import {
  CLAUDE_DIR,
  log,
  colors,
  ensureDir,
  copyDirRecursive,
  checkClaudeCode,
} from "./utils";

const BACKUP_ITEMS = {
  critical: [
    "settings.json",
    "settings.local.json",
  ],
  directories: [
    "hooks",
  ],
  optional: [
    "todos",
  ],
  secure: [
    ".credentials.json",
  ],
  skip: [
    "projects",
    "debug",
    "cache",
    "file-history",
    "stats-cache.json",
    "history.jsonl",
    "skills",        // Managed by ima-claude
    "personalities", // Managed by ima-claude
  ],
};

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
}

function getDirSize(dir: string): number {
  if (!existsSync(dir)) return 0;

  let size = 0;
  const entries = readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      size += getDirSize(path);
    } else {
      size += statSync(path).size;
    }
  }

  return size;
}

async function main() {
  console.log(`\n${colors.bright}📦 ima-claude Backup Utility${colors.reset}\n`);

  // Check for Claude Code
  if (!checkClaudeCode()) {
    log.error("~/.claude not found. Nothing to backup.");
    process.exit(1);
  }

  // Create backup directory
  const timestamp = new Date().toISOString().split("T")[0].replace(/-/g, "");
  const backupDir = join(process.env.HOME || "~", `claude-backup-${timestamp}`);

  if (existsSync(backupDir)) {
    log.warn(`Backup directory already exists: ${backupDir}`);
    log.info("Using existing directory (will overwrite)");
  }

  ensureDir(backupDir);
  log.step(`Creating backup in: ${backupDir}`);
  console.log("");

  // Backup critical files
  log.step("Backing up critical configuration...");
  let backedUpFiles = 0;

  for (const file of BACKUP_ITEMS.critical) {
    const src = join(CLAUDE_DIR, file);
    const dest = join(backupDir, file);

    if (existsSync(src)) {
      copyFileSync(src, dest);
      const size = formatSize(statSync(src).size);
      console.log(`   ${colors.green}✓${colors.reset} ${file} (${size})`);
      backedUpFiles++;
    } else {
      console.log(`   ${colors.yellow}○${colors.reset} ${file} (not found)`);
    }
  }

  // Backup directories
  log.step("Backing up directories...");

  for (const dir of BACKUP_ITEMS.directories) {
    const src = join(CLAUDE_DIR, dir);
    const dest = join(backupDir, dir);

    if (existsSync(src)) {
      const size = formatSize(getDirSize(src));
      const fileCount = readdirSync(src).length;
      copyDirRecursive(src, dest);
      console.log(`   ${colors.green}✓${colors.reset} ${dir}/ (${fileCount} files, ${size})`);
      backedUpFiles++;
    } else {
      console.log(`   ${colors.yellow}○${colors.reset} ${dir}/ (not found)`);
    }
  }

  // Backup optional items (only if they have content)
  for (const dir of BACKUP_ITEMS.optional) {
    const src = join(CLAUDE_DIR, dir);
    const dest = join(backupDir, dir);

    if (existsSync(src)) {
      const entries = readdirSync(src);
      if (entries.length > 0) {
        const size = formatSize(getDirSize(src));
        copyDirRecursive(src, dest);
        console.log(`   ${colors.green}✓${colors.reset} ${dir}/ (${entries.length} items, ${size})`);
        backedUpFiles++;
      }
    }
  }

  // Warn about secure files
  console.log("");
  log.step("Checking secure files...");

  for (const file of BACKUP_ITEMS.secure) {
    const src = join(CLAUDE_DIR, file);

    if (existsSync(src)) {
      log.warn(`${file} exists - requires manual secure backup`);
      console.log(`   ${colors.yellow}→${colors.reset} Consider encrypting before storing`);
      console.log(`   ${colors.cyan}   gpg -c ${src}${colors.reset}`);
    }
  }

  // Report skipped items
  console.log("");
  log.step("Skipped (will regenerate or managed separately):");

  for (const item of BACKUP_ITEMS.skip) {
    const path = join(CLAUDE_DIR, item);
    if (existsSync(path)) {
      const isDir = statSync(path).isDirectory();
      const size = isDir ? formatSize(getDirSize(path)) : formatSize(statSync(path).size);
      console.log(`   ${colors.blue}○${colors.reset} ${item}${isDir ? "/" : ""} (${size})`);
    }
  }

  // Summary
  console.log(`\n${colors.bright}✅ Backup complete!${colors.reset}\n`);
  console.log(`   Location:    ${backupDir}`);
  console.log(`   Items:       ${backedUpFiles} backed up`);
  console.log(`   Total size:  ${formatSize(getDirSize(backupDir))}`);
  console.log("");

  // Fresh start instructions
  console.log(`${colors.bright}📋 Fresh Start Instructions:${colors.reset}`);
  console.log("");
  console.log("   1. Move old ~/.claude:");
  console.log(`      ${colors.cyan}mv ~/.claude ~/.claude.old-${timestamp}${colors.reset}`);
  console.log("");
  console.log("   2. Start Claude Code (creates fresh ~/.claude):");
  console.log(`      ${colors.cyan}claude${colors.reset}`);
  console.log("");
  console.log("   3. Install ima-claude:");
  console.log(`      ${colors.cyan}cd ~/dev/ima-claude && bun run scripts/install.ts${colors.reset}`);
  console.log("");
  console.log("   4. Restore backups:");
  console.log(`      ${colors.cyan}cp ${backupDir}/settings*.json ~/.claude/${colors.reset}`);
  console.log(`      ${colors.cyan}cp -r ${backupDir}/hooks/* ~/.claude/hooks/${colors.reset}`);
  console.log("");
  console.log("   5. (Optional) Restore credentials:");
  console.log(`      ${colors.cyan}cp ${backupDir}/.credentials.json ~/.claude/${colors.reset}`);
  console.log("");
}

main().catch((err) => {
  log.error(`Backup failed: ${err.message}`);
  process.exit(1);
});
