# Local pilot mode

This is a disposable, self-hosted developer preview. Run:

```powershell
zoracleflux pilot --database .zoracleflux\pilot.sqlite3 --runs 3 --json
```

The command runs synthetic packaged functions, writes only bounded relation
evidence to SQLite, and reports zero model/network calls. It does not accept
customer source, credentials, PII, or outbound destinations. Delete the SQLite
file to reset the pilot. This is not a customer interview, paid pilot,
production telemetry system, SLA, or proof of correctness.
