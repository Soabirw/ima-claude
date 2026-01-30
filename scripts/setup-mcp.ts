#!/usr/bin/env bun

import { existsSync, readFileSync } from "fs";
import { spawnSync } from "child_process";
import { colors, log, checkClaudeCode } from "./utils";

// MCP Server Definitions
const MCP_SERVERS = {
  tavily: {
    name: "Tavily",
    description: "Web research and current information (requires API key)",
    command: "npx",
    args: ["-y", "tavily-mcp@latest"],
    requiresApiKey: true,
    apiKeyVar: "TAVILY_API_KEY",
    apiKeyInstructions: "Get your API key at https://tavily.com",
    recommended: true,
  },
  context7: {
    name: "Context7",
    description: "Official library documentation lookup",
    command: "npx",
    args: ["-y", "@upstash/context7-mcp@latest"],
    requiresApiKey: false,
    recommended: true,
  },
  memory: {
    name: "Memory",
    description: "Knowledge graph for persistent project context",
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-memory@latest"],
    requiresApiKey: false,
    recommended: true,
  },
  "sequential-thinking": {
    name: "Sequential Thinking",
    description: "Structured reasoning for complex problems",
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-sequential-thinking@latest"],
    requiresApiKey: false,
    recommended: false,
  },
  fetch: {
    name: "Fetch",
    description: "Web page fetching (may be redundant with native tools)",
    command: "uvx",
    args: ["mcp-server-fetch"],
    requiresApiKey: false,
    recommended: false,
  },
  "chrome-devtools": {
    name: "Chrome DevTools",
    description: "Chrome debugging for web development",
    command: "npx",
    args: ["-y", "chrome-devtools-mcp@latest"],
    requiresApiKey: false,
    recommended: false,
  },
};

interface InstalledServer {
  command: string;
  args: string[];
  env?: Record<string, string>;
}

function getInstalledServers(): Record<string, InstalledServer> {
  const claudeJsonPath = `${process.env.HOME}/.claude.json`;
  if (!existsSync(claudeJsonPath)) {
    return {};
  }

  try {
    const config = JSON.parse(readFileSync(claudeJsonPath, "utf8"));
    return config.mcpServers || {};
  } catch {
    return {};
  }
}

function checkAirisRunning(): boolean {
  const result = spawnSync("docker", ["ps", "--filter", "name=airis-mcp-gateway", "--format", "{{.Names}}"], {
    encoding: "utf8",
  });
  return result.stdout.trim().includes("airis-mcp-gateway");
}

function prompt(question: string): Promise<string> {
  return new Promise((resolve) => {
    process.stdout.write(question);
    process.stdin.once("data", (data) => {
      resolve(data.toString().trim());
    });
  });
}

async function promptYesNo(question: string, defaultYes = true): Promise<boolean> {
  const suffix = defaultYes ? "[Y/n]" : "[y/N]";
  const answer = await prompt(`${question} ${suffix} `);
  if (!answer) return defaultYes;
  return answer.toLowerCase() === "y" || answer.toLowerCase() === "yes";
}

async function promptApiKey(serverKey: string): Promise<string | null> {
  const server = MCP_SERVERS[serverKey];
  console.log(`\n${colors.cyan}ℹ${colors.reset} ${server.name} requires an API key`);
  console.log(`   ${server.apiKeyInstructions}\n`);

  // Check if key exists in Airis .env
  const airisEnvPath = `${process.env.HOME}/ai/airis-mcp-gateway/.env`;
  if (existsSync(airisEnvPath)) {
    try {
      const envContent = readFileSync(airisEnvPath, "utf8");
      const match = envContent.match(new RegExp(`${server.apiKeyVar}=(.+)`));
      if (match) {
        const existingKey = match[1].trim();
        const useExisting = await promptYesNo(
          `Found ${server.apiKeyVar} in Airis .env. Use this key?`,
          true
        );
        if (useExisting) {
          return existingKey;
        }
      }
    } catch {}
  }

  const key = await prompt(`Enter ${server.apiKeyVar} (or press Enter to skip): `);
  return key || null;
}

function addMcpServer(
  serverKey: string,
  apiKey?: string
): { success: boolean; message: string } {
  const server = MCP_SERVERS[serverKey];
  const args = ["mcp", "add", "--scope", "user"];

  if (apiKey) {
    args.push("-e", `${server.apiKeyVar}=${apiKey}`);
    args.push("--");
  }

  args.push(serverKey);
  args.push("--");
  args.push(server.command);
  args.push(...server.args);

  const result = spawnSync("claude", args, { encoding: "utf8" });

  if (result.status === 0) {
    return { success: true, message: result.stdout };
  } else {
    return { success: false, message: result.stderr || result.stdout };
  }
}

function removeMcpServer(serverKey: string): { success: boolean; message: string } {
  const result = spawnSync("claude", ["mcp", "remove", serverKey], { encoding: "utf8" });

  if (result.status === 0) {
    return { success: true, message: "Removed successfully" };
  } else {
    return { success: false, message: result.stderr || result.stdout };
  }
}

async function selectServers(): Promise<string[]> {
  console.log(`\n${colors.bright}Select MCP Servers to Install${colors.reset}\n`);
  console.log("Recommended servers are pre-selected. Enter 'all' for all servers.");
  console.log("Enter server numbers separated by spaces (e.g., '1 2 3'), or press Enter for recommended.\n");

  const serverKeys = Object.keys(MCP_SERVERS);
  serverKeys.forEach((key, index) => {
    const server = MCP_SERVERS[key];
    const recommended = server.recommended ? `${colors.green}(Recommended)${colors.reset}` : "";
    const apiKey = server.requiresApiKey ? `${colors.yellow}[API Key Required]${colors.reset}` : "";
    console.log(`   ${index + 1}. ${server.name} - ${server.description} ${recommended} ${apiKey}`);
  });

  const answer = await prompt("\nSelection: ");

  if (!answer || answer.toLowerCase() === "recommended") {
    return serverKeys.filter((key) => MCP_SERVERS[key].recommended);
  }

  if (answer.toLowerCase() === "all") {
    return serverKeys;
  }

  const selected: string[] = [];
  const numbers = answer.split(/\s+/).filter(Boolean);

  for (const num of numbers) {
    const index = parseInt(num, 10) - 1;
    if (index >= 0 && index < serverKeys.length) {
      selected.push(serverKeys[index]);
    }
  }

  return selected;
}

async function main() {
  console.log(`\n${colors.bright}🔌 MCP Server Setup${colors.reset}\n`);

  // Check for Claude Code
  if (!checkClaudeCode()) {
    log.error("~/.claude not found. Install Claude Code first.");
    console.log("   Visit: https://claude.ai/code\n");
    process.exit(1);
  }

  // Check installed servers
  const installed = getInstalledServers();
  const installedKeys = Object.keys(installed);

  if (installedKeys.length > 0) {
    console.log(`${colors.cyan}Currently installed MCP servers:${colors.reset}`);
    installedKeys.forEach((key) => {
      if (key === "airis-mcp-gateway") {
        console.log(`   ${colors.yellow}⚠${colors.reset}  ${key} (Airis Gateway - can be removed)`);
      } else {
        console.log(`   ${colors.green}✓${colors.reset} ${key}`);
      }
    });
    console.log("");
  }

  // Check if Airis is running
  const airisRunning = checkAirisRunning();
  if (airisRunning) {
    console.log(`${colors.yellow}⚠${colors.reset}  Airis MCP Gateway is currently running in Docker\n`);
  }

  // Main menu
  console.log("What would you like to do?");
  console.log("   1. Install/Update MCP servers");
  console.log("   2. Remove Airis Gateway");
  console.log("   3. List installed servers");
  console.log("   4. Exit\n");

  const choice = await prompt("Selection [1]: ");

  switch (choice || "1") {
    case "1":
      await installServers(installed);
      break;
    case "2":
      await removeAiris(installed, airisRunning);
      break;
    case "3":
      await listServers();
      break;
    case "4":
      console.log("\nExiting...\n");
      process.exit(0);
    default:
      log.error("Invalid choice");
      process.exit(1);
  }
}

async function installServers(installed: Record<string, InstalledServer>) {
  const selectedKeys = await selectServers();

  if (selectedKeys.length === 0) {
    log.warn("No servers selected. Exiting.");
    process.exit(0);
  }

  console.log(`\n${colors.cyan}Installing ${selectedKeys.length} server(s)...${colors.reset}\n`);

  for (const key of selectedKeys) {
    const server = MCP_SERVERS[key];
    process.stdout.write(`   Installing ${server.name}... `);

    let apiKey: string | undefined;
    if (server.requiresApiKey) {
      console.log(""); // New line for API key prompt
      apiKey = (await promptApiKey(key)) || undefined;
      if (!apiKey) {
        console.log(`   ${colors.yellow}⊘${colors.reset} Skipped ${server.name} (no API key)\n`);
        continue;
      }
      process.stdout.write(`   Installing ${server.name} with API key... `);
    }

    const result = addMcpServer(key, apiKey);

    if (result.success) {
      console.log(`${colors.green}✓${colors.reset}`);

      // Add API key to ~/.bashrc if provided
      if (apiKey && server.apiKeyVar) {
        const bashrcPath = `${process.env.HOME}/.bashrc`;
        if (existsSync(bashrcPath)) {
          const bashrc = readFileSync(bashrcPath, "utf8");
          if (!bashrc.includes(server.apiKeyVar)) {
            const { appendFileSync } = await import("fs");
            appendFileSync(
              bashrcPath,
              `\n# ${server.name} API Key for MCP\nexport ${server.apiKeyVar}=${apiKey}\n`
            );
            console.log(`      Added ${server.apiKeyVar} to ~/.bashrc`);
          }
        }
      }
    } else {
      console.log(`${colors.red}✗${colors.reset}`);
      console.log(`      ${result.message}`);
    }
  }

  console.log(`\n${colors.green}✅ MCP server setup complete!${colors.reset}\n`);
  console.log(`Run ${colors.cyan}claude mcp list${colors.reset} to verify installation.\n`);
}

async function removeAiris(installed: Record<string, InstalledServer>, airisRunning: boolean) {
  if (!installed["airis-mcp-gateway"]) {
    log.warn("Airis Gateway is not configured in ~/.claude.json");
    if (airisRunning) {
      console.log("\nHowever, Airis is still running in Docker.");
      const stopIt = await promptYesNo("Stop Airis Docker containers?", true);
      if (stopIt) {
        console.log("\nStopping Airis Docker containers...");
        const result = spawnSync("docker", ["stop", "airis-mcp-gateway", "airis-serena", "airis-mcp-gateway-core"], {
          encoding: "utf8",
        });
        if (result.status === 0) {
          log.success("Airis Docker containers stopped");
          console.log("\nTo prevent auto-start, remove from docker-compose or disable auto-start.");
        } else {
          log.error("Failed to stop containers. Stop manually with: docker stop airis-mcp-gateway");
        }
      }
    }
    console.log("");
    process.exit(0);
  }

  console.log(`\n${colors.yellow}⚠${colors.reset}  This will remove Airis Gateway from ~/.claude.json\n`);
  const confirm = await promptYesNo("Continue?", false);

  if (!confirm) {
    console.log("\nCancelled.\n");
    process.exit(0);
  }

  console.log("\nRemoving Airis Gateway...");
  const result = removeMcpServer("airis-mcp-gateway");

  if (result.success) {
    log.success("Airis Gateway removed from configuration");

    if (airisRunning) {
      console.log("");
      const stopIt = await promptYesNo("Stop Airis Docker containers?", true);
      if (stopIt) {
        console.log("\nStopping Airis Docker containers...");
        const stopResult = spawnSync("docker", ["stop", "airis-mcp-gateway", "airis-serena", "airis-mcp-gateway-core"], {
          encoding: "utf8",
        });
        if (stopResult.status === 0) {
          log.success("Airis Docker containers stopped");
          console.log("\nTo prevent auto-start, remove from docker-compose or disable auto-start.");
        } else {
          log.error("Failed to stop containers. Stop manually with: docker stop airis-mcp-gateway");
        }
      }
    }
  } else {
    log.error(`Failed to remove: ${result.message}`);
  }

  console.log("");
}

async function listServers() {
  console.log("\nChecking MCP server health...\n");
  const result = spawnSync("claude", ["mcp", "list"], { encoding: "utf8" });
  console.log(result.stdout);
  process.exit(0);
}

main().catch((err) => {
  log.error(`Setup failed: ${err.message}`);
  process.exit(1);
});
