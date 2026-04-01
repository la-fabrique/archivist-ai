import { describe, it, expect } from "vitest";
import { orderedReferencePaths } from "../src/sync/path-order.js";

describe("orderedReferencePaths", () => {
  it("orders shallower paths before deeper ones", () => {
    const input = ["a/b/c.txt", "a/x.txt", "root.txt", "a/b/d.txt"];
    expect(orderedReferencePaths(input)).toEqual([
      "root.txt",
      "a/x.txt",
      "a/b/c.txt",
      "a/b/d.txt",
    ]);
  });
});
