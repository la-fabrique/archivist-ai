import { createServer, type IncomingMessage, type ServerResponse } from "node:http";

function send(res: ServerResponse, status: number, body: string): void {
  res.writeHead(status, { "Content-Type": "text/plain; charset=utf-8" });
  res.end(body);
}

export type OAuthCallbackResult = { code: string; state: string | null };

/**
 * Démarre un serveur sur 127.0.0.1:port aléatoire ; fournit le port pour redirect_uri, puis une promesse du code OAuth.
 */
export function createOAuthServer(timeoutMs = 120_000): {
  port: Promise<number>;
  result: Promise<OAuthCallbackResult>;
} {
  let resolvePort!: (p: number) => void;
  let rejectResult!: (e: Error) => void;
  let resolveResult!: (v: OAuthCallbackResult) => void;

  const port = new Promise<number>((res) => {
    resolvePort = res;
  });

  const result = new Promise<OAuthCallbackResult>((res, rej) => {
    resolveResult = res;
    rejectResult = rej;
  });

  let settled = false;
  const safeReject = (err: Error): void => {
    if (settled) {
      return;
    }
    settled = true;
    clearTimeout(timer);
    try {
      server.close();
    } catch {
      /* ignore */
    }
    rejectResult(err);
  };

  const safeResolve = (value: OAuthCallbackResult): void => {
    if (settled) {
      return;
    }
    settled = true;
    clearTimeout(timer);
    try {
      server.close();
    } catch {
      /* ignore */
    }
    resolveResult(value);
  };

  const timer = setTimeout(() => {
    safeReject(new Error("OAuth timeout: aucun callback reçu"));
  }, timeoutMs);

  const server = createServer((req: IncomingMessage, res: ServerResponse) => {
    if (!req.url || req.method !== "GET") {
      send(res, 404, "Not found");
      return;
    }
    const addr = server.address();
    const listenP = typeof addr === "object" && addr ? addr.port : 0;
    let url: URL;
    try {
      url = new URL(req.url, `http://127.0.0.1:${listenP}`);
    } catch {
      send(res, 400, "Bad request");
      return;
    }
    if (url.pathname !== "/oauth2callback") {
      send(res, 404, "Not found");
      return;
    }
    const oerr = url.searchParams.get("error");
    if (oerr) {
      send(res, 400, `OAuth error: ${oerr}`);
      safeReject(new Error(`OAuth error: ${oerr}`));
      return;
    }
    const code = url.searchParams.get("code");
    if (!code) {
      send(res, 400, "Missing code");
      return;
    }
    const state = url.searchParams.get("state");
    send(res, 200, "Authentification réussie. Tu peux fermer cet onglet.");
    safeResolve({ code, state });
  });

  server.on("error", (e) => {
    safeReject(e instanceof Error ? e : new Error(String(e)));
  });

  server.listen(0, "127.0.0.1", () => {
    const addr = server.address();
    const listenPort = typeof addr === "object" && addr ? addr.port : 0;
    resolvePort(listenPort);
  });

  return { port, result };
}
