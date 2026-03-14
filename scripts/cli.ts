#!/usr/bin/env node

import { VERSION, colors, log, promptYesNo } from "./utils";
import { detectPlatforms, getAdapter } from "../platforms/shared/detector";
import { installForPlatform } from "../platforms/shared/installer";
import type { PlatformAdapter } from "../platforms/shared/types";

const args = process.argv.slice(2);
const command = args[0];

function showHelp() {
  console.log(`
${colors.bright}ima-claude v${VERSION}${colors.reset}
IMA's AI coding agent skills - FP patterns, architecture guidance, and team standards.

${colors.cyan}Usage:${colors.reset}
  ima-claude <command> [options]

${colors.cyan}Commands:${colors.reset}
  install             Interactive install (auto-detects platforms)
  install --target X  Install for specific platform (claude, junie, gemini, gh-copilot)
  upgrade             Upgrade installed skills to latest version
  detect              Show detected platforms
  help                Show this help message

${colors.cyan}Examples:${colors.reset}
  npx ima-claude install
  npx ima-claude install --target junie
  npx ima-claude detect

${colors.cyan}More Info:${colors.reset}
  https://github.com/Soabirw/ima-claude
`);
}

function showDetected() {
  const platforms = detectPlatforms();

  console.log(`\n${colors.bright}Detected AI Coding Agents${colors.reset}\n`);
  for (const { adapter, detected, note } of platforms) {
    const icon = detected ? `${colors.green}+${colors.reset}` : `${colors.red}-${colors.reset}`;
    const status = detected ? "found" : "not detected";
    console.log(`  ${icon} ${adapter.displayName} (${status})`);
    if (note && detected) {
      console.log(`    ${colors.yellow}${note}${colors.reset}`);
    }
  }
  console.log("");
}

async function interactiveInstall() {
  console.log(`\n${colors.bright}ima-claude v${VERSION} — Multi-Platform Installer${colors.reset}`);
  console.log("Detecting installed AI coding agents...\n");

  const platforms = detectPlatforms();
  const detected = platforms.filter((p) => p.detected);
  const notDetected = platforms.filter((p) => !p.detected);

  for (const { adapter, note } of detected) {
    console.log(`  ${colors.green}+${colors.reset} ${adapter.displayName}`);
    if (adapter.name === "claude" && note) {
      console.log(
        `    ${colors.yellow}Tip:${colors.reset} For Claude Code, the plugin marketplace is recommended:`
      );
      console.log(
        `    ${colors.cyan}/plugin marketplace add Soabirw/ima-claude${colors.reset}`
      );
      console.log(
        `    ${colors.cyan}/plugin install ima-claude${colors.reset}`
      );
    }
  }
  for (const { adapter } of notDetected) {
    console.log(`  ${colors.red}-${colors.reset} ${adapter.displayName} (not detected)`);
  }

  if (detected.length === 0) {
    console.log(
      `\n${colors.yellow}No supported platforms detected.${colors.reset}`
    );
    console.log("Install Claude Code, Junie CLI, Gemini CLI, or GitHub Copilot first, then run this installer again.\n");
    return;
  }

  console.log("");

  const toInstall: PlatformAdapter[] = [];

  for (const { adapter } of detected) {
    if (adapter.name === "claude") {
      const proceed = await promptYesNo(
        `Install for ${adapter.displayName}? (Plugin marketplace is preferred)`,
        false
      );
      if (proceed) toInstall.push(adapter);
    } else {
      const proceed = await promptYesNo(
        `Install for ${adapter.displayName}?`,
        true
      );
      if (proceed) toInstall.push(adapter);
    }
  }

  if (toInstall.length === 0) {
    console.log("\nNo platforms selected. Exiting.\n");
    return;
  }

  for (const adapter of toInstall) {
    await installForPlatform(adapter);
  }
}

async function targetedInstall(targetName: string) {
  const adapter = getAdapter(targetName);
  if (!adapter) {
    log.error(`Unknown target: ${targetName}`);
    console.log("Available targets: claude, junie, gemini, gh-copilot");
    process.exit(1);
  }

  if (!adapter.detect()) {
    log.warn(
      `${adapter.displayName} not detected at ${adapter.configDir}`
    );
    const proceed = await promptYesNo("Install anyway?", false);
    if (!proceed) {
      console.log("Exiting.\n");
      return;
    }
  }

  if (adapter.name === "claude") {
    console.log(
      `\n${colors.yellow}Tip:${colors.reset} For Claude Code, the plugin marketplace is recommended:`
    );
    console.log(
      `  ${colors.cyan}/plugin marketplace add Soabirw/ima-claude${colors.reset}`
    );
    console.log(
      `  ${colors.cyan}/plugin install ima-claude${colors.reset}\n`
    );
    const proceed = await promptYesNo("Continue with direct install?", false);
    if (!proceed) return;
  }

  await installForPlatform(adapter);
}

async function main() {
  switch (command) {
    case "install": {
      const targetIdx = args.indexOf("--target");
      if (targetIdx !== -1 && args[targetIdx + 1]) {
        await targetedInstall(args[targetIdx + 1]);
      } else {
        await interactiveInstall();
      }
      break;
    }
    case "detect":
      showDetected();
      break;
    case "upgrade":
      console.log("Upgrade runs the same as install — detecting and updating.\n");
      await interactiveInstall();
      break;
    case "help":
    case "--help":
    case "-h":
    case undefined:
      showHelp();
      break;
    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
