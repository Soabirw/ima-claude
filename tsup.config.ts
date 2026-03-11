import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["scripts/cli.ts"],
  format: ["esm"],
  target: "node18",
  outDir: "dist",
  clean: true,
  splitting: false,
  bundle: true,
});
