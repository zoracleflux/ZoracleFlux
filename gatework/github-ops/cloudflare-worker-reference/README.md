# Cloudflare Worker reference adapter (not ZoracleFlux)

This tiny JavaScript adapter exists only to demonstrate and test the boundary
between static GitHub Pages and an externally hosted HTTP runtime. It exposes
`/healthz` and `/`; it does not execute the Python package, store users, accept
customer source, or implement an API.

Local test:

```powershell
node test.mjs
```

Deployment requires a Cloudflare account and Wrangler credentials. Do not add
the optional deployment workflow until an owner has reviewed the threat model,
secret policy, quotas, abuse controls and rollback plan.
