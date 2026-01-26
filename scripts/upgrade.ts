#!/usr/bin/env bun

/**
 * Upgrade script - now delegates to install.ts
 *
 * The install script automatically detects existing installations
 * and runs in upgrade mode (no backup, overwrites files).
 *
 * Use `bun scripts/install.ts --reinstall` for a fresh install with backup.
 */

import { spawn } from "bun";
import { dirname, join } from "path";

const scriptDir = dirname(import.meta.path);
const installScript = join(scriptDir, "install.ts");

const proc = spawn(["bun", installScript], {
  stdio: ["inherit", "inherit", "inherit"],
});

const exitCode = await proc.exited;
process.exit(exitCode);
