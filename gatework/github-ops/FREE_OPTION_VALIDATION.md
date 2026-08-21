# Free-option validation record

Date: 2026-08-21. No GitHub, Cloudflare, UptimeRobot, Better Stack or
PagerDuty account was used. No live ZoracleFlux endpoint was created.

## What was tested locally

```text
python -m pytest -q
=> 22 passed (preserved RC3)

python -m compileall -q scripts
=> passed

PyYAML safe_load of all bundle YAML files
=> 12 parsed

Local Git repository + scripts\github_backup_export.py --no-api
=> repository.bundle, manifest.json, API_EXPORT_SKIPPED.txt and
   SHA256SUMS.txt created; hashes verified

node cloudflare-worker-reference\test.mjs
=> health adapter assertions passed
```

The Worker test is an in-process Node test, not a Cloudflare deployment. It
proves only deterministic HTTP handler behavior.

## What was verified from current official terms

The official pricing/limits pages were fetched on 2026-08-21 and their
published values are recorded in `FREE_OPTIONS_RESEARCH.md`. The pages were
reachable, but page reachability is not a service-account or quota test.

```text
Cloudflare Workers Free: 100,000 requests/day, 10 ms CPU, 128 MB,
  50 subrequests/request, 5 Cron Triggers/account.
Cloudflare R2 Standard free: 10 GB-month, 1M Class A, 10M Class B,
  free Internet egress.
Cloudflare D1 Free: 10 databases/account, 500 MB/database, 5 GB/account,
  7-day Time Travel.
UptimeRobot Free: 50 monitors, 5-minute interval, $0/no card.
PagerDuty Free: up to 5 users, 1 schedule, 1 escalation policy,
  100 international phone/SMS notifications/month.
Infisical Free: 5 identities, 3 environments, 10 syncs, $0 forever.
```

Local `Invoke-WebRequest -Method Head` probe:

```text
10/10 official GitHub, Cloudflare, UptimeRobot, Better Stack, PagerDuty and
Infisical pricing/limits URLs returned HTTP 200.
```

## Explicit non-tests

No account signup, payment method, cloud trust policy, API token, custom
domain, DNS/TLS issuance, Worker deployment, R2 upload, external monitor,
PagerDuty notification, human acknowledgement, incident response, restore
from off-site storage, or provider SLA was tested. These are deployment gates,
not facts inferred from documentation.
