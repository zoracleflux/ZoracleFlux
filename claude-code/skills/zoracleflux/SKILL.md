---
name: zoracleflux
description: Run ZoracleFlux bounded offline behavioral checks and report JSON evidence. Use when a user asks to validate supported Python relations or inspect deterministic check results.
---

Run `zoracleflux check --json` from the repository root. Show the literal JSON
and treat a nonzero exit status as a failed gate. This command is local-only:
do not send source, output, credentials, or prompts to a model or network.

If `zoracleflux` is not on PATH, stop and give the setup steps in the
ZoracleFlux support report; do not substitute an invented result. Do not claim
that Claude Code itself was executed unless the user has installed it and its
version is observed.
