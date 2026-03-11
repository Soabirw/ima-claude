import { join } from "path";
import type { PlatformAdapter, InstallFilter, InstallItem, InstallOptions } from "./types";
import { PLUGIN_SOURCE } from "./types";
import { colors, log, prompt, promptYesNo } from "../../scripts/utils";

function formatItemList(items: InstallItem[], category: string): string {
  const filtered = items.filter((i) => i.category === category);
  if (filtered.length === 0) return "";

  const overrideCount = filtered.filter((i) => i.exists).length;
  const overrideNote = overrideCount > 0
    ? ` ${colors.yellow}(${overrideCount} existing will be overwritten)${colors.reset}`
    : "";

  const names = filtered.map((i) => {
    const marker = i.exists ? `${colors.yellow}*${colors.reset}` : " ";
    return `${marker} ${i.name}`;
  });

  const label = category.charAt(0).toUpperCase() + category.slice(1) + "s";
  return `  ${colors.bright}${label} (${filtered.length})${colors.reset}${overrideNote}\n${names.map((n) => `    ${n}`).join("\n")}`;
}

function showPreview(adapter: PlatformAdapter, items: InstallItem[]): void {
  console.log(
    `\n${colors.bright}Install preview for ${adapter.displayName}${colors.reset}`
  );
  console.log(`  Target: ${adapter.configDir}\n`);

  const categories = ["skill", "agent", "hook", "guideline"] as const;
  for (const cat of categories) {
    const section = formatItemList(items, cat);
    if (section) console.log(section + "\n");
  }

  const existingCount = items.filter((i) => i.exists).length;
  if (existingCount > 0) {
    console.log(
      `  ${colors.yellow}*${colors.reset} = exists and will be overwritten (${existingCount} files)\n`
    );
  }
}

async function promptExclusions(items: InstallItem[]): Promise<InstallFilter> {
  const filter: InstallFilter = {};

  console.log(`${colors.cyan}Options:${colors.reset}`);
  console.log(`  [Enter]  Install all`);
  console.log(`  [e]      Exclude specific items`);
  console.log(`  [c]      Cancel\n`);

  const choice = await prompt("Selection: ");

  if (choice.toLowerCase() === "c") {
    return { excludeSkills: items.filter((i) => i.category === "skill").map((i) => i.name) };
  }

  if (choice.toLowerCase() !== "e") {
    return filter;
  }

  // Interactive exclusion
  const skills = items.filter((i) => i.category === "skill");
  const agents = items.filter((i) => i.category === "agent");
  const hooks = items.filter((i) => i.category === "hook");
  const guidelines = items.filter((i) => i.category === "guideline");

  if (skills.length > 0) {
    console.log(
      `\n${colors.bright}Skills${colors.reset} (${skills.length} total)`
    );
    console.log(
      `  Enter names to EXCLUDE (comma-separated), or press Enter to keep all:`
    );
    console.log(
      `  ${colors.cyan}Available:${colors.reset} ${skills.map((s) => s.name).join(", ")}\n`
    );
    const excluded = await prompt("  Exclude: ");
    if (excluded) {
      filter.excludeSkills = excluded.split(",").map((s) => s.trim()).filter(Boolean);
    }
  }

  if (agents.length > 0) {
    console.log(
      `\n${colors.bright}Agents${colors.reset} (${agents.length} total)`
    );
    console.log(
      `  Enter names to EXCLUDE (comma-separated), or press Enter to keep all:`
    );
    console.log(
      `  ${colors.cyan}Available:${colors.reset} ${agents.map((a) => a.name).join(", ")}\n`
    );
    const excluded = await prompt("  Exclude: ");
    if (excluded) {
      filter.excludeAgents = excluded.split(",").map((s) => s.trim()).filter(Boolean);
    }
  }

  if (hooks.length > 0) {
    console.log(
      `\n${colors.bright}Hooks${colors.reset} (${hooks.length} total)`
    );
    console.log(
      `  Enter names to EXCLUDE (comma-separated), or press Enter to keep all:`
    );
    console.log(
      `  ${colors.cyan}Available:${colors.reset} ${hooks.map((h) => h.name).join(", ")}\n`
    );
    const excluded = await prompt("  Exclude: ");
    if (excluded) {
      filter.excludeHooks = excluded.split(",").map((s) => s.trim()).filter(Boolean);
    }
  }

  if (guidelines.length > 0) {
    const skip = !(await promptYesNo("\n  Install guidelines?", true));
    filter.skipGuidelines = skip;
  }

  return filter;
}

export async function installForPlatform(
  adapter: PlatformAdapter,
  options: InstallOptions = {}
): Promise<void> {
  const skillsSource = join(PLUGIN_SOURCE, "skills");
  const agentsSource = join(PLUGIN_SOURCE, "agents");
  const hooksSource = join(PLUGIN_SOURCE, "hooks");

  // Preview
  const preview = adapter.preview(PLUGIN_SOURCE);
  showPreview(adapter, preview.items);

  // Exclusion selection
  const filter = await promptExclusions(preview.items);

  // Check if everything was cancelled
  const allSkills = preview.items.filter((i) => i.category === "skill");
  if (
    filter.excludeSkills &&
    filter.excludeSkills.length >= allSkills.length
  ) {
    console.log("\nInstallation cancelled.\n");
    return;
  }

  // Confirm
  const excludedCount =
    (filter.excludeSkills?.length ?? 0) +
    (filter.excludeAgents?.length ?? 0) +
    (filter.excludeHooks?.length ?? 0) +
    (filter.skipGuidelines ? 1 : 0);
  const totalItems = preview.items.length - excludedCount;

  const proceed = await promptYesNo(
    `\nInstall ${totalItems} items to ${adapter.configDir}?`
  );
  if (!proceed) {
    console.log("\nInstallation cancelled.\n");
    return;
  }

  console.log(
    `\n${colors.bright}Installing for ${adapter.displayName}${colors.reset}\n`
  );

  log.step(`Installing skills...`);
  adapter.installSkills(skillsSource, filter.excludeSkills);
  log.success(`Skills installed`);

  log.step(`Installing agents...`);
  adapter.installAgents(agentsSource, filter.excludeAgents);
  log.success(`Agents installed`);

  if (!filter.skipGuidelines) {
    log.step(`Installing guidelines...`);
    adapter.installGuidelines(PLUGIN_SOURCE);
    log.success(`Guidelines installed`);
  }

  if (adapter.installHooks) {
    log.step(`Installing hooks...`);
    adapter.installHooks(hooksSource, filter.excludeHooks);
    log.success(`Hooks installed`);
  }

  if (adapter.configureMcp && !options.skipMcp) {
    log.step(`Configuring MCP servers...`);
    await adapter.configureMcp();
    log.success(`MCP configured`);
  }

  if (adapter.postInstall) {
    adapter.postInstall();
  }

  console.log(
    `\n${colors.green}Done!${colors.reset} ${adapter.displayName} installation complete.\n`
  );
}
