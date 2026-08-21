# ZoracleFlux hosted-production workstream

This directory is a **zero-cash, self-hosted, production-shaped pilot bundle** for
ZoracleFlux 1.0.0rc2. It does not create public hosting, a managed secret store,
customer processing, legal approval, certification, uptime evidence, or an SLA.
The release candidate is intentionally unchanged; use this directory as an
operator overlay.

## Deployable today

* Offline local execution with the release candidate's `doctor`, `check`, and
  synthetic `pilot` commands.
* Optional Docker Compose shape (`compose.yaml`) with a non-root, no-network
  pilot container and a persistent local SQLite volume. A Docker engine and a
  locally available base image are prerequisites; no public deployment is
  implied.
* Local JSONL audit review, Prometheus text metrics, SQLite backup/restore, and
  health checks using Python's standard library.
* Draft privacy, terms, security, SLA, certification, incident, and operator
  runbooks. Templates require owner/legal/customer completion.

## Not deployable/complete without Gate B

Public ingress, DNS/TLS, identity and tenant isolation, managed or HSM-backed
secrets, encrypted off-host backups, alert delivery, on-call coverage,
vulnerability monitoring, paid support, data-processing agreements, legal
approval, independent security review, SOC 2/ISO certification, and any
availability or response-time commitment. See `GATE_B_REGISTER.csv`.

## Local quickstart (PowerShell)

From the RC3 bundle root:

```powershell
Set-Location .\artifacts\zoracleflux\final-release-candidate-rc3
py -3.10 -m venv .venv
.\.venv\Scripts\python -m pip install --requirement requirements.lock
.\.venv\Scripts\python -m pip install .
zoracleflux doctor --json
zoracleflux check --json
zoracleflux pilot --runs 2 --json
.\support\production\healthcheck.py --root . --db .\.zoracleflux\pilot.sqlite3
.\support\production\metrics.py --audit .\.zoracleflux\audit.jsonl
.\support\production\threat_tests.py
.\support\production\backup.py backup --db .\.zoracleflux\pilot.sqlite3 --out .\support\production\evidence\backup
.\support\production\backup.py restore --backup-dir .\support\production\evidence\backup --target .\support\production\evidence\restored.sqlite3
```

`healthcheck.py`, `metrics.py`, `backup.py`, `audit_event.py`, and
`threat_tests.py` use only the Python standard library. They intentionally do
not read environment variables as secrets or make network calls.

## Compose pilot

```powershell
docker compose --file .\support\production\compose.yaml config
docker compose --file .\support\production\compose.yaml build
docker compose --file .\support\production\compose.yaml run --rm pilot
docker compose --file .\support\production\compose.yaml run --rm health
```

The Compose service is a bounded local pilot, not a hosted service. Network
access is disabled in the service definition, no credentials are mounted, and
the image is not signed. If the base image is not already cached, obtaining it
would require network access; that is a deferred operational dependency.

## Evidence and accounting

`evidence/LOCAL_CHECKS.md` records exact commands, observed versions, outputs,
and SHA-256 values from this workstream. `GATE_B_REGISTER.csv` records each
funding, legal, security, customer, and dependency gate. Incremental cash for
this bundle is **$0.00**; workstation time, power, and existing subscriptions
are not represented as zero-cost production capacity.


