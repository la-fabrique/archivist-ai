import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

export function fileMd5Hex(absolutePath: string): string {
  const buf = readFileSync(absolutePath);
  return createHash("md5").update(buf).digest("hex");
}
