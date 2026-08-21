import handler from "./src/index.js";

const request = (path, init) =>
  handler.fetch(new Request(`https://example.invalid${path}`, init));

const health = await request("/healthz");
const payload = await health.json();
if (health.status !== 200 || payload.status !== "ok" || payload.customer_data) {
  throw new Error("health response assertion failed");
}

const method = await request("/healthz", { method: "POST" });
if (method.status !== 405) throw new Error("method assertion failed");

const missing = await request("/missing");
if (missing.status !== 404) throw new Error("404 assertion failed");

console.log("health adapter assertions passed");
