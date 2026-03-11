import type { DetectedPlatform, PlatformAdapter } from "./types";
import { ClaudeAdapter } from "../claude/adapter";
import { JunieAdapter } from "../junie/adapter";

const ADAPTERS: PlatformAdapter[] = [
  new ClaudeAdapter(),
  new JunieAdapter(),
];

export function detectPlatforms(): DetectedPlatform[] {
  return ADAPTERS.map((adapter) => {
    const detected = adapter.detect();
    const note = adapter.name === "claude" && detected
      ? "Recommended: install via plugin marketplace instead"
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
