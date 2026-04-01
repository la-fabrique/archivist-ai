import { describe, it, expect } from "vitest";
import http from "node:http";
import { createOAuthServer } from "../src/auth/oauth-server.js";

function httpGet(url: string): Promise<void> {
  return new Promise((resolve, reject) => {
    http
      .get(url, (res) => {
        res.resume();
        res.on("end", () => resolve());
      })
      .on("error", reject);
  });
}

describe("createOAuthServer", () => {
  it("resolves with code on GET /oauth2callback", async () => {
    const { port: portP, result } = createOAuthServer(5000);
    const port = await portP;
    const done = result;
    await httpGet(`http://127.0.0.1:${port}/oauth2callback?code=abc&state=xyz`);
    await expect(done).resolves.toEqual({ code: "abc", state: "xyz" });
  });

  it("rejects on OAuth error param", async () => {
    const { port: portP, result } = createOAuthServer(5000);
    const port = await portP;
    const rejection = expect(result).rejects.toThrow(/OAuth error/);
    await httpGet(
      `http://127.0.0.1:${port}/oauth2callback?error=access_denied&error_description=nope`,
    );
    await rejection;
  });
});
