// World Dispatch — 19 November 2026 news image entry.
// Copies entry.png (next to this script) into $MAKEFUN_OUTPUT_DIR (default /output).
// Node 22, no dependencies. Deterministic: no network, identical output every run.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const source = join(scriptDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, dest);

  // Robustness: verify the copy is byte-for-byte identical to the source.
  const srcBytes = readFileSync(source);
  const dstBytes = readFileSync(dest);
  if (srcBytes.length !== dstBytes.length) {
    throw new Error(
      `Size mismatch: source entry.png is ${srcBytes.length} bytes, ` +
        `copy at ${dest} is ${dstBytes.length} bytes.`,
    );
  }
  if (!srcBytes.equals(dstBytes)) {
    throw new Error(`Content mismatch: copy at ${dest} differs from source entry.png.`);
  }
  if (statSync(dest).size !== srcBytes.length) {
    throw new Error(`Stat size mismatch for ${dest}.`);
  }

  console.log(`Copied entry.png -> ${dest} (${srcBytes.length} bytes, verified)`);
} catch (err) {
  console.error(`ERROR: ${(err as Error).message}`);
  process.exit(1);
}
