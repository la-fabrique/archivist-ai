import { writeFileSync, mkdtempSync, unlinkSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect } from "vitest";
import { createHash } from "node:crypto";
import { fileMd5Hex } from "../src/sync/content-hash.js";

describe("fileMd5Hex", () => {
  it("matches md5 of file contents", () => {
    const root = mkdtempSync(join(tmpdir(), "hash-"));
    const file = join(root, "hello.txt");
    writeFileSync(file, "hello");
    const expected = createHash("md5").update("hello").digest("hex");
    try {
      expect(fileMd5Hex(file)).toBe(expected);
    } finally {
      unlinkSync(file);
    }
  });
});
