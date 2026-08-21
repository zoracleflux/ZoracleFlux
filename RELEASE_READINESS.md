# Release readiness — 1.0.0rc4 gate integration

**Status:** zero-cash self-hosted pilot-ready; not funded production-ready.

The preserved RC3 package payload (`1.0.0rc2`) still passes clean install,
22 tests, 13/13 bounded evaluation, mutation score 1.0, offline pilot,
production-shaped threat checks, Claude/Codex fallback contracts and local
Antigravity MCP checks. RC4 adds validated compliance, GitHub-ops and Sigstore
organization-trust gatework without claiming their external effects.

Compliance: 20 files, 17 controls, 15 evidence mappings, 17 pathways, 10
templates and 24 hash checks. GitHub-ops: 30 files, 12 YAML parsed, syntax,
backup/export, adapter tests and 10/10 URL probes reported pass. Sigstore:
policy/workflow/verifier validation passes and OpenSSH fallback 4/4; zero
Sigstore bundles because no GitHub OIDC run occurred.

Remaining blockers: authenticated native Claude/Codex/Antigravity runtime,
organization-authenticated release identity, live GitHub repository governance
and workflow runs, OIDC/Fulcio/Rekor evidence, real endpoint/uptime/on-call,
customer validation, legal/DPA approval, independent security review,
certification, managed secrets, funded operations and SLA evidence. Synthetic
uptime is explicitly non-production evidence.
