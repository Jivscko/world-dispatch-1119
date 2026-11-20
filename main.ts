// World Dispatch — 19 November 2026 (Thursday) news image entry.
// Copies entry.png from this script's directory into MAKEFUN_OUTPUT_DIR
// (default /output), creating it if needed, then verifies the copy is
// byte-identical to the source. Node 22, zero dependencies, no network.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(src, dst);

  const a = readFileSync(src);
  const b = readFileSync(dst);
  if (a.length !== b.length || !a.equals(b)) {
    throw new Error(
      `copy verification failed: ${dst} (${b.length} bytes) differs from source (${a.length} bytes)`,
    );
  }

  console.log(`OK: entry.png -> ${dst} (${a.length} bytes, byte-identical)`);
} catch (err) {
  console.error(`ERROR: ${(err as Error).message}`);
  process.exit(1);
}
