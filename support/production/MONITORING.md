# Local monitoring and audit

`healthcheck.py` emits one JSON object and exits nonzero on package or SQLite
integrity failure. `metrics.py` converts valid local audit JSONL into Prometheus
text for a local scraper or a file collector; it does not listen on a port and
does not send telemetry. The release candidate's own `.zoracleflux/audit.jsonl`
contains bounded event metadata only.

Suggested zero-cash loop:

```powershell
.\support\production\healthcheck.py --root . --db .\.zoracleflux\pilot.sqlite3
.\support\production\metrics.py --audit .\.zoracleflux\audit.jsonl --output .\support\production\evidence\metrics.prom
```

For Gate B, define alert thresholds, clock synchronization, retention,
tamper-evident forwarding, paging ownership, and a tested dashboard. Do not
turn local metrics into an availability or SLA claim.

