import { join } from "path";
import { existsSync, copyFileSync, readdirSync, statSync } from "fs";

import type { PlatformAdapter, InstallItem, InstallPreview } from "../shared/types";
import {
  CLAUDE_DIR,
  ensureDir,
  copyDirRecursive,
  mergeHooksIntoSettings,
  SKILLS_TO_INSTALL,
  HOOKS_TO_INSTALL,
  SKILLS_DIR,
  HOOKS_DIR,
  log,
} from "../../scripts/utils";

const AGENTS_DIR = join(CLAUDE_DIR, "agents");

export class ClaudeAdapter implements PlatformAdapter {
  readonly name = "claude";
  readonly displayName = "Claude Code";
  readonly configDir = CLAUDE_DIR;

  detect(): boolean {
    return existsSync(CLAUDE_DIR);
  }

  preview(sourceDir: string): InstallPreview {
    const skillItems: InstallItem[] = SKILLS_TO_INSTALL.map((skill) => ({
      name: skill,
      category: "skill",
      destPath: join(SKILLS_DIR, skill),
      exists: existsSync(join(SKILLS_DIR, skill)),
    }));

    const agentsSourceDir = join(sourceDir, "agents");
    const agentItems: InstallItem[] = existsSync(agentsSourceDir)
      ? readdirSync(agentsSourceDir)
          .filter((f) => f.endsWith(".md"))
          .map((file) => ({
            name: file.replace(/\.md$/, ""),
            category: "agent",
            destPath: join(AGENTS_DIR, file),
            exists: existsSync(join(AGENTS_DIR, file)),
          }))
      : [];

    const hooksSourceDir = join(sourceDir, "hooks");
    const hookItems: InstallItem[] = HOOKS_TO_INSTALL.map((file) => ({
      name: file,
      category: "hook",
      destPath: join(HOOKS_DIR, file),
      exists: existsSync(join(HOOKS_DIR, file)),
    }));

    return {
      platform: this.name,
      targetDir: CLAUDE_DIR,
      items: [...skillItems, ...agentItems, ...hookItems],
    };
  }

  installSkills(sourceDir: string, exclude?: string[]): void {
    ensureDir(SKILLS_DIR);
    const skills = exclude?.length
      ? SKILLS_TO_INSTALL.filter((s) => !exclude.includes(s))
      : SKILLS_TO_INSTALL;
    for (const skill of skills) {
      const src = join(sourceDir, skill);
      if (existsSync(src) && statSync(src).isDirectory()) {
        copyDirRecursive(src, join(SKILLS_DIR, skill));
        log.step(`skill: ${skill}`);
      }
    }
  }

  installAgents(sourceDir: string, exclude?: string[]): void {
    ensureDir(AGENTS_DIR);
    const entries = readdirSync(sourceDir).filter((f) => f.endsWith(".md"));
    const filtered = exclude?.length
      ? entries.filter((f) => !exclude.includes(f.replace(/\.md$/, "")))
      : entries;
    for (const file of filtered) {
      copyFileSync(join(sourceDir, file), join(AGENTS_DIR, file));
      log.step(`agent: ${file}`);
    }
  }

  installGuidelines(_pluginRoot: string): void {
    // No-op — guidelines come from the plugin system via CLAUDE.md injection
  }

  installHooks(sourceDir: string, exclude?: string[]): void {
    ensureDir(HOOKS_DIR);
    const hooks = exclude?.length
      ? HOOKS_TO_INSTALL.filter((f) => !exclude.includes(f))
      : HOOKS_TO_INSTALL;
    for (const file of hooks) {
      const src = join(sourceDir, file);
      if (existsSync(src)) {
        copyFileSync(src, join(HOOKS_DIR, file));
        log.step(`hook: ${file}`);
      }
    }
    const { created } = mergeHooksIntoSettings();
    log.info(created ? "Created ~/.claude/settings.json with hooks" : "Merged hooks into ~/.claude/settings.json");
  }

  postInstall(): void {
    log.warn("Note: Direct install is not the recommended approach for Claude Code.");
    log.info("Prefer the plugin system instead:");
    log.info("  /plugin marketplace add Soabirw/ima-claude");
    log.info("  /plugin install ima-claude");
  }
}
