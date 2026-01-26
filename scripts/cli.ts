#!/usr/bin/env bun

import { colors, VERSION } from "./utils";

const args = process.argv.slice(2);
const command = args[0];

function showHelp() {
  console.log(`
${colors.bright}ima-claude v${VERSION}${colors.reset}
IMA's Claude Code Skills - FP patterns, architecture guidance, and team standards.

${colors.cyan}Usage:${colors.reset}
  ima-claude <command>

${colors.cyan}Commands:${colors.reset}
  install     Install ima-claude skills to ~/.claude
  upgrade     Upgrade installed skills to latest version
  help        Show this help message

${colors.cyan}Examples:${colors.reset}
  bunx ima-claude install
  bunx ima-claude upgrade

${colors.cyan}More Info:${colors.reset}
  https://github.com/your-org/ima-claude
`);
}

async function main() {
  switch (command) {
    case "install":
      await import("./install");
      break;
    case "upgrade":
      await import("./upgrade");
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
