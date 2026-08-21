# Antigravity adapter status

**First-class platform status:** verified. Antigravity IDE 1.107.0 (commit
`ecfbad74d93962fc8ca485d93ab9b4f3d4cb6cf8`) accepted `--add-mcp`; installed
schema compatibility and registration smoke passed.

**Native ZoracleFlux host call:** **UNVERIFIED HERE**, not unsupported. The
isolated host lacked account state and had no unauthenticated `tools/call`
entrypoint. The exact blocker, literal smoke output, tested stdio adapter, and
user-run authenticated verification steps are in `support\antigravity\REPORT.md`.
Use `support\antigravity\mcp_config.json` and the direct fallback
`zoracleflux check --json`.
