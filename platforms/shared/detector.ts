import type { DetectedPlatform, PlatformAdapter } from "./types";
import { ClaudeAdapter } from "../claude/adapter";
import { JunieAdapter } from "../junie/adapter";
import { GeminiAdapter } from "../gemini/adapter";
import { GhCopilotAdapter } from "../gh-copilot/adapter";
import { CodexAdapter } from "../codex/adapter";

const ADAPTERS: PlatformAdapter[] = [
  new ClaudeAdapter(),
  new JunieAdapter(),
  new GeminiAdapter(),
  new GhCopilotAdapter(),
  new CodexAdapter(),
];

export function detectPlatforms(): DetectedPlatform[] {
  return ADAPTERS.map((adapter) => {
    const detected = adapter.detect();
    const note = adapter.name === "claude" && detected
      ? "Recommended: install via plugin marketplace instead"
      : adapter.name === "gemini" && detected
        ? "Also available as a Gemini extension"
        : undefined;

    return { adapter, detected, note };
  });
}

export function getAdapter(name: string): PlatformAdapter | undefined {
  return ADAPTERS.find((a) => a.name === name);
}

export function getAllAdapters(): PlatformAdapter[] {
  return [...ADAPTERS];
}
