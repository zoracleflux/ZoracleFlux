# Zero-cost options research

Reviewed 2026-08-21 against the linked vendor pages. “Free” means the
published free plan at review time; it is not a promise that terms, availability
or eligibility will never change. No account was created and no live ZoracleFlux
endpoint was fabricated.

## Public hosting and runtime

| Option | Published free allowance | What it can do | Exact boundary |
|---|---|---|---|
| GitHub Pages | Public static site; published site up to 1 GB, 10-minute deployment timeout, soft 100 GB/month bandwidth and soft 10 builds/hour (custom Actions publisher avoids the build-rate limit). | Documentation, static status page, release links. | Static only. No Python process, API, database, auth, queue or worker. |
| GitHub Actions | Standard hosted runners are free for public repositories. | CI, release packaging, exports, scheduled probes. | Ephemeral jobs; schedules can be delayed/disabled. Not an API host or SLA. |
| Cloudflare Workers Free | 100,000 requests/day, 10 ms CPU/invocation, 128 MB memory, 50 subrequests/request, 6 simultaneous outgoing connections, 5 Cron Triggers/account, workers.dev endpoint available after account setup. | A small JavaScript/TypeScript HTTP API or adapter. | Not a Python runtime. 10 ms is a hard constraint for non-trivial logic. “Free plan” is quota-based, not a forever contract; account/terms still apply. |
| Cloudflare Pages Functions Free | Functions share the Workers Free 100,000/day quota; static asset requests are free and unlimited. | JS/TS edge functions beside a static Pages site. | Same Workers limits; still not a Python/ZoracleFlux runtime. |

The bundle includes a **health-only Cloudflare Worker adapter** to test the
runtime boundary locally. It is deliberately not called ZoracleFlux and does
not execute the Python package. A real API requires a separately designed
adapter, identity model, data model, abuse controls and endpoint.

## Managed secrets and identity

| Option | Published free allowance | Good use | Boundary |
|---|---|---|---|
| GitHub environment secrets | Available for public repositories on GitHub Free; required reviewers and branch/tag restrictions are available. | Small public-repo deployment token, protected by `production`. | Anyone with repository write access can read repository secrets. It is not an HSM or independent vault. |
| GitHub OIDC | Short-lived JWT; no long-lived cloud secret in GitHub after a cloud trust policy is configured. | AWS/Azure/GCP/Vault role federation for backup/deploy. | A cloud account, trust policy, billing/eligibility and least-privilege role are unavoidable. OIDC itself stores no data. |
| Cloudflare Worker secrets | Encrypted per-Worker secrets, hidden in the dashboard/Wrangler. | Runtime API keys after a Worker exists. | Requires a Cloudflare account; deployment generally needs a Cloudflare API token or vendor integration. No native Cloudflare OIDC claim is assumed here. |
| Infisical Cloud Free | $0 forever; 5 identities, unlimited projects, 3 environments, 10 secret syncs. | A small external secret manager with machine identity. | No versioning/PITR, RBAC, audit retention, rotation, approvals, or SLA on Free; cloud account and trust token still needed. Self-hosted core is free software but hosting is not free. |

The strongest zero-cost default is **no application secret at all** for the
offline pilot, then environment secrets for a public-repository pilot. For
production, prefer GitHub OIDC to a cloud role; do not treat a static token in
GitHub as equivalent.

## Backups and recovery

| Option | Published free allowance | Evidence | Boundary |
|---|---|---|---|
| GitHub Actions artifact | Per-artifact retention can be set but cannot exceed repository/org/enterprise policy; upload-artifact returns a SHA-256 digest. | The included export workflow creates a Git bundle plus API JSON and hashes. | Retention is finite; artifact storage is not an off-site DR guarantee. It does not export secrets, environments, variables, all settings, or a complete Discussions/Projects backup. |
| GitHub mirror repository | Git can clone/push all refs and tags to a second repository. | `git clone --mirror`/`git push --mirror` is documented. | A mirror duplicates code/refs, not settings, secrets, Actions logs, issues, projects or cloud data. A second public repo may disclose source. |
| Cloudflare R2 Standard | 10 GB-month storage, 1M Class A and 10M Class B operations/month free; Internet egress free. | Suitable target for encrypted bundle exports. | Billing account/provider terms and an access token are required; overage is billed ($0.015/GB-month, $4.50/M A, $0.36/M B). Encryption, immutability and restore policy remain owner work. |
| Cloudflare D1 Free | 10 databases/account, 500 MB/database, 5 GB/account, 7-day Time Travel, 50 queries/Worker invocation. | Small metadata store only. | Single-threaded database, 500 MB/5 GB caps and 7-day recovery are not a backup strategy for customer data. |

R2 is the strongest practical free off-site target for small exports, but only
after a human creates the account, bucket, access policy, encryption/retention
policy and restore test. Keep the GitHub artifact as a short-lived staging
copy, not the only backup.

## Monitoring, uptime evidence and on-call

| Option | Published free allowance | What it proves | What it does not prove |
|---|---|---|---|
| GitHub scheduled probe | No external account; Actions is free in public repos. | A best-effort `curl` result in a workflow run. | Continuous monitoring, precise interval, delivery, or paging; schedules can be delayed and inactive repositories can lose schedules. |
| UptimeRobot Free | $0, no card; 50 monitors, 5-minute interval, HTTP/port/ping/API/keyword/SSL/DNS options, basic status pages, five integrations; no notification seats. | Independent external checks and basic public status. | Five-minute detection and limited integrations are not a staffed on-call. |
| Better Stack free personal tier | 10 monitors/heartbeats, 1 status page, Slack/email alerts, 3 GB logs/traces/metrics class allowances with short retention as published. | Useful hobby/personal monitoring and status. | The responder/on-call scheduling and phone/SMS capability is not the free personal guarantee; paid responder pricing is listed separately. |
| PagerDuty Free | Up to 5 users, 1 on-call schedule, 1 escalation policy, 100 international phone/SMS notifications/month, API and integrations. | A genuine free on-call product with a human rota if configured. | It still requires five real people or fewer, a real monitor integration, phone/email delivery and a person who responds. No response evidence exists here. |

Use GitHub Issues/Projects for incident records and PagerDuty Free for a small
human rota when a real endpoint exists. A runbook, an email notification, or a
failed Actions run is not an active on-call service.

## Security and supply chain

* Dependabot version/security PRs and dependency graph are available for public
  repositories.
* CodeQL code scanning uses Actions and is free for public repositories; private
  repositories require the applicable Code Security license.
* OpenSSF Scorecard Action is free for public repositories. Publishing results
  uses `id-token: write` to bind the result to GitHub OIDC; it is a heuristic,
  not a certification.
* GitHub Releases allow up to 1,000 assets/release and each asset under 2 GiB;
  no total release size or bandwidth limit is documented.

## References

* GitHub Pages limits: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>
* GitHub Actions billing: <https://docs.github.com/en/actions/concepts/billing-and-usage>
* GitHub OIDC: <https://docs.github.com/en/actions/concepts/security/openid-connect>
* Environments: <https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments>
* Artifacts: <https://docs.github.com/en/actions/tutorials/store-and-share-data>
* Releases: <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>
* Cloudflare Workers limits: <https://developers.cloudflare.com/workers/platform/limits/>
* Cloudflare Workers pricing: <https://developers.cloudflare.com/workers/platform/pricing/>
* Pages Functions pricing: <https://developers.cloudflare.com/pages/functions/pricing/>
* Cloudflare secrets: <https://developers.cloudflare.com/workers/configuration/secrets/>
* Cloudflare D1 limits: <https://developers.cloudflare.com/d1/platform/limits/>
* Cloudflare R2 pricing: <https://developers.cloudflare.com/r2/pricing/>
* Infisical pricing: <https://infisical.com/pricing>
* UptimeRobot pricing: <https://uptimerobot.com/pricing/>
* Better Stack pricing: <https://betterstack.com/pricing>
* PagerDuty pricing: <https://www.pagerduty.com/pricing/incident-management/>
* Scorecard Action: <https://github.com/ossf/scorecard-action>
