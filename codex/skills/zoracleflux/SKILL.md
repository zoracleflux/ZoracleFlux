---
name: zoracleflux
description: Run ZoracleFlux bounded offline behavioral checks and report JSON evidence. Use when a user asks to validate supported Python relations or inspect deterministic check results.
---

From the repository root, run `zoracleflux check --json` and show its literal
JSON output. Treat a nonzero exit status as a failed gate. The command is
offline-only and makes zero model calls; never add a source path, credentials,
network destination, or guessed result.

If the command is unavailable, report the exact setup command from the
ZoracleFlux support report. Do not claim Codex native execution unless a local
Codex binary and version were actually observed.
