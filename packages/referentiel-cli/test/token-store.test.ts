import { mkdtempSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  saveTokens,
  loadTokens,
  getTokensPath,
} from "../src/auth/token-store.js";

describe("token-store", () => {
  let prevXdg: string | undefined;
  let configBase: string;

  beforeEach(() => {
    prevXdg = process.env.XDG_CONFIG_HOME;
    configBase = mkdtempSync(join(tmpdir(), "xdg-"));
    process.env.XDG_CONFIG_HOME = configBase;
  });

  afterEach(() => {
    if (prevXdg === undefined) {
      delete process.env.XDG_CONFIG_HOME;
    } else {
      process.env.XDG_CONFIG_HOME = prevXdg;
    }
  });

  it("writes and reads refresh token", () => {
    const tokens = {
      refresh_token: "fake-refresh",
      token_type: "Bearer",
      expiry_date: 0,
    };
    saveTokens(tokens);
    const path = getTokensPath();
    expect(existsSync(path)).toBe(true);
    const loaded = loadTokens();
    expect(loaded?.refresh_token).toBe("fake-refresh");
    const raw = readFileSync(path, "utf8");
    expect(JSON.parse(raw).refresh_token).toBe("fake-refresh");
  });
});
