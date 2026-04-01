import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const cliPath = join(__dirname, "..", "dist", "cli.js");

let body = readFileSync(cliPath, "utf8");
if (!body.startsWith("#!/usr/bin/env node\n") && !body.startsWith("#!/usr/bin/env node\r\n")) {
  body = "#!/usr/bin/env node\n" + body;
  writeFileSync(cliPath, body, "utf8");
}
