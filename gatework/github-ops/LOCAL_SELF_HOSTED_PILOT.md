# Local self-hosted pilot

This is the only runtime path proven by the preserved RC3 evidence. It is
offline-first, disposable, credential-free, and not an internet service.

```powershell
Set-Location C:\path\to\final-release-candidate-rc3
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements.lock
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\zoracleflux.exe doctor --json
.\.venv\Scripts\zoracleflux.exe check --json
.\.venv\Scripts\zoracleflux.exe pilot --database .zoracleflux\pilot.sqlite3 --runs 3 --json
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe evaluation\run_evaluation.py
```

Optional local production-shaped checks, if the support overlay is present:

```powershell
.\.venv\Scripts\python.exe support\production\threat_tests.py
.\.venv\Scripts\python.exe support\production\healthcheck.py --root . --db .zoracleflux\pilot.sqlite3
```

The pilot writes bounded SQLite/audit evidence and makes no model or network
calls. Delete `.zoracleflux\pilot.sqlite3` to reset it. Docker/Compose,
public ingress, authentication, tenant isolation, managed secrets,
off-host/encrypted backups, alerting and uptime are intentionally outside this
pilot.
