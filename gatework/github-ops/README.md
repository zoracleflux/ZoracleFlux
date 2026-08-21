# ZoracleFlux GitHub operations bundle

This is a ready-to-copy operations overlay for the preserved RC3 at
`artifacts\zoracleflux\final-release-candidate-rc3`. It targets a public
GitHub repository and deliberately separates static GitHub-hosted surfaces from
the ZoracleFlux runtime.

## What is included

* CI and release gates for the Python package, hashes, and GitHub Releases.
* GitHub Pages static documentation deployment (no server-side code).
* Least-privilege permissions, Dependabot, dependency review, and CodeQL.
* A scheduled repository export and artifact retention plan.
* A scheduled HTTP probe for an already-hosted endpoint.
* Incident and bug issue forms, a PR gate checklist, and an on-call runbook.
* A local, offline self-hosted pilot procedure.
* A current free-tier comparison and a health-only Cloudflare Worker boundary
  adapter; the adapter is not the ZoracleFlux runtime.

Copy the contents of this directory into the repository root, preserving
`.github`, `scripts`, and `site`. Do not copy anything back into RC3; RC3 is
evidence-preserved and remains unchanged.

## Runtime boundary

GitHub Pages serves static files. GitHub Actions runs finite jobs. Neither is
an API host, a durable worker, a database, an ingress, a secret manager, or an
on-call service. The included Pages site is documentation only. A public
ZoracleFlux API requires externally hosted compute, TLS/DNS, identity and
tenant isolation, managed secrets, backups, monitoring, and an owner. A $0
external deployment is not promised: provider free tiers, quotas, sleep
behavior, and terms change. The $0 path that can be proven here is the local
self-hosted pilot in `LOCAL_SELF_HOSTED_PILOT.md`.

## Apply

1. Copy this overlay into a real public repository containing RC3.
2. Configure Pages to use **GitHub Actions** and create the `github-pages`
   environment. GitHub Free environments/protection rules are available for
   public repositories only.
3. Protect `main`: require the `CI / test` and `Security / codeql` checks,
   require review, dismiss stale approvals, and restrict tag creation/release
   permissions to maintainers.
4. Set repository variable `HEALTHCHECK_URL` only after a real HTTPS endpoint
   exists. Do not put credentials in that URL.
5. If off-site backups are required, configure an external object store and an
   OIDC trust policy restricted to this repository and the backup workflow.
6. Run the checklist and record real repository, endpoint, domain, cloud and
   on-call evidence. Until then, status is **pilot-ready, not production
   ready**.

See `RESEARCH.md`, `FREE_OPTIONS_RESEARCH.md`,
`FREE_REFERENCE_ARCHITECTURE.md`, `DEPLOYMENT_CHECKLIST.md`, and `RUNBOOK.md`.
