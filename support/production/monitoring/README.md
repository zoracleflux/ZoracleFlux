# Monitoring overlay

`metrics.py` writes Prometheus exposition text to a file; no HTTP listener or
telemetry transport is included. `prometheus.yml` is an illustrative operator
starting point only and is not a working hosted scrape target until an
owner-approved local collector is added. Do not expose the audit log or metrics
file publicly.

