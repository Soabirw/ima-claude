import { homedir } from "os";
import { join, resolve, dirname } from "path";
import { existsSync } from "fs";
import { fileURLToPath } from "url";

export interface InstallItem {
  name: string;
  category: "skill" | "agent" | "hook" | "guideline";
  destPath: string;
  exists: boolean;
}

export interface InstallPreview {
  platform: string;
  targetDir: string;
  items: InstallItem[];
}

export interface InstallFilter {
  excludeSkills?: string[];
  excludeAgents?: string[];
  excludeHooks?: string[];
  skipGuidelines?: boolean;
}

export interface PlatformAdapter {
  readonly name: string;
  readonly displayName: string;
  readonly configDir: string;

  detect(): boolean;
  preview(sourceDir: string): InstallPreview;
  installSkills(sourceDir: string, exclude?: string[]): void;
  installAgents(sourceDir: string, exclude?: string[]): void;
  installGuidelines(pluginRoot: string): void;
  installHooks?(sourceDir: string, exclude?: string[]): void;
  configureMcp?(): Promise<void>;
  postInstall?(): void;
}

export interface DetectedPlatform {
  adapter: PlatformAdapter;
  detected: boolean;
  note?: string;
}

export interface InstallOptions {
  targets?: string[];
  verbose?: boolean;
  skipMcp?: boolean;
}

export function findPackageRoot(): string {
  let dir: string;
  try {
    dir = dirname(fileURLToPath(import.meta.url));
  } catch {
    dir = typeof __dirname !== "undefined" ? __dirname : resolve(".");
  }

  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, "package.json"))) return dir;
    const parent = join(dir, "..");
    if (parent === dir) break;
    dir = parent;
  }
  return process.cwd();
}

export const PLUGIN_SOURCE = join(
  findPackageRoot(),
  "plugins",
  "ima-claude"
);

export function platformConfigDir(platformDir: string): string {
  return join(homedir(), platformDir);
}
