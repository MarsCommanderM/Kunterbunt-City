// P09-T09: Web-Build im echten Browser starten (Chromium headless, Software-WebGL) – lädt das Spiel ohne Fehler?
// Aufruf: NODE_PATH=$(npm root -g) node tools/dev/web_smoke.cjs export/web docs/tests/P09/web_start.png
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");   // global installiert: NODE_PATH=$(npm root -g)

(async () => {

const dir = path.resolve(process.argv[2] || "export/web");
const shot = process.argv[3] || "web_start.png";
const types = { ".html": "text/html", ".js": "application/javascript", ".wasm": "application/wasm", ".pck": "application/octet-stream",
  ".png": "image/png" };
const server = http.createServer((req, res) => {
  const f = path.join(dir, decodeURIComponent(req.url.split("?")[0]).replace(/^\/$/, "/index.html"));
  if (!f.startsWith(dir) || !fs.existsSync(f)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream",
    "Cross-Origin-Opener-Policy": "same-origin", "Cross-Origin-Embedder-Policy": "require-corp" });
  fs.createReadStream(f).pipe(res);
}).listen(8765);

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", headless: true,
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] }).catch(async () =>
  chromium.launch({ headless: true, args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] }));
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const errors = [];
const logs = [];
page.on("console", (m) => {
  logs.push(`${m.type()}: ${m.text()}`);
  const t = m.text();
  if (m.type() === "error" && !t.startsWith("WARNING") && !t.trim().startsWith("at:")) errors.push(t);   // Godot-Warnungen sind keine Fehler
});
page.on("pageerror", (e) => errors.push(String(e)));
const t0 = Date.now();
await page.goto("http://localhost:8765/index.html");
let started = false;
for (let i = 0; i < 90 && !started; i++) {
  await page.waitForTimeout(1000);
  started = logs.some((l) => l.includes("ItemDB:"));
}
await page.waitForTimeout(6000);
await page.screenshot({ path: shot });
// Durchspielen (wie ein Kind): Haut-Reiter → Hautfarbe → Fertig → Stadtkarte → Einkaufsstraße
const steps = [];
if (started && process.argv.includes("--play")) {
  const click = async (x, y, name, wait = 1500) => {
    await page.mouse.click(x, y); await page.waitForTimeout(wait);
    const f = shot.replace(/\.png$/, `_${steps.length + 1}_${name}.png`); await page.screenshot({ path: f }); steps.push(f);
  };
  await click(620, 140, "haut");
  await click(880, 245, "hautfarbe");
  await click(1150, 52, "fertig", 4000);
  await click(1115, 485, "einkaufsstrasse", 9000);
}
const result = { started, steps, seconds: Math.round((Date.now() - t0) / 1000), errors: errors.slice(0, 10),
  log: logs.filter((l) => l.includes("[INFO]") || l.includes("ERROR")).slice(0, 12) };
console.log(JSON.stringify(result, null, 1));
await browser.close();
server.close();
process.exit(started && errors.filter((e) => !e.includes("favicon")).length === 0 ? 0 : 1);
})();
