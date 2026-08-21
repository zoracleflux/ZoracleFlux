# Local verification record

Recorded 2026-08-21 on Windows 10 (`Windows-10-10.0.26200-SP0`) from the
preserved `final-release-candidate`. These are local observations, not hosted
production evidence.

## Exact commands and observed results

The unabridged stdout/stderr for each command is stored under `raw\` and
integrity-listed in `SHA256SUMS.txt`. The excerpts below summarize the same
files without reproducing UUIDs and timing noise.

```text
py -3.10 --version
Python 3.10.1

py -3.10 -c "import sqlite3; print(sqlite3.sqlite_version)"
3.35.5

py -3.10 -m pip --version
pip 24.3.1 from C:\Users\ziada\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)

py -3.10 -m pip show pytest setuptools wheel | Select-String '^(Name|Version):'
Name: pytest
Version: 8.4.2
Name: setuptools
Version: 75.8.0
Name: wheel
Version: 0.45.1

py -3.10 -m compileall -q .\support\production
(exit 0; no output)

py -3.10 .\support\production\threat_tests.py
{"checks": {"audit_allowlist": "pass", "backup_path_traversal_rejected": "pass", "health_missing_db_is_safe": "pass", "metrics_no_network": "pass", "overlay_static_boundary": "pass"}, "schema_version": 1, "status": "passed"}

py -3.10 -m pytest
......................                                                   [100%]
22 passed in 2.20s

zoracleflux doctor --json
{"command":"doctor","message":"Deterministic local path is available; optional model/provider adapters are disabled.","model_calls":0,"network_calls":0,"offline_default":true,"platform":"Windows-10-10.0.26200-SP0","python":"3.10.1","schema_version":"1","status":"passed","version":"1.0.0rc2"}

zoracleflux check --json
{"counts":{"failed":0,"passed":13,"total":13},"evidence":"bounded deterministic cases; not a proof","model_calls":0,"network":false,"status":"passed","version":"1.0.0rc2"}

zoracleflux pilot --runs 2 --json
{"cash_spend_usd":0.0,"database":".zoracleflux\\pilot.sqlite3","runs":"2 synthetic runs, 13/13 relations each","status":"passed","version":"1.0.0rc2"}

py -3.10 .\evaluation\run_evaluation.py
{"cash_spend_usd":0.0,"false_failure_rate":0.0,"heldout_static_declarations":0,"mode":"offline-deterministic","model_calls":0,"mutation_killed":5,"mutation_score":1.0,"mutation_total":5,"network_calls":0,"relation_passed":13,"relation_total":13,"unknown_tag_negative_fixture_present":true,"version":"1.0.0rc2"}

py -3.10 .\support\production\backup.py backup --db .\.zoracleflux\pilot.sqlite3 --out .\support\production\evidence\backup
{"cash_usd":"0.00","file":"pilot.sqlite3","sha256":"f0a35392b83a99ed3c12fdd180efe8e024aadb2e1aa5b12c689d4b172d49a0f8","sqlite_integrity":true}

py -3.10 .\support\production\backup.py restore --backup-dir .\support\production\evidence\backup --target .\support\production\evidence\restored-latest.sqlite3
{"restored":"support\\production\\evidence\\restored-latest.sqlite3","sha256":"f0a35392b83a99ed3c12fdd180efe8e024aadb2e1aa5b12c689d4b172d49a0f8","sqlite_integrity":true}

docker --version
PowerShell: The term 'docker' is not recognized; Compose validation/build was not available.
```

The exact native command errors are preserved in
`raw\docker-version.txt` and `raw\docker-compose-version.txt` (and hashed in
`SHA256SUMS.txt`); therefore the Compose path is documented but not claimed as
executed on this workstation.

The raw files (including `backup.json`, `restore.json`, and
`restore-health.json`) are the exact captured outputs; JSON output is otherwise
non-deterministic in timestamps, UUIDs, and elapsed milliseconds. The backup
SHA-256 in full is
`f0a35392b83a99ed3c12fdd180efe8e024aadb2e1aa5b12c689d4b172d49a0f8`.

## Release and bundle hashes

```text
dist\zoracleflux-1.0.0rc2-py3-none-any.whl
67142421933973cbc91890eafcb9a6c8345bcc9f578671359a7d9c96ffdc7d8b
dist\zoracleflux-1.0.0rc2.tar.gz
b27f6ce1335c808db2c9181715af198962ea99f17ddeeb8d694f87b50618d33e6
```

`ARTIFACT_MANIFEST.sha256` and the release candidate's `SBOM.json` remain the
source of truth for release contents. This support overlay is not signed.

## Cost and claim boundary

Incremental cash spend: **$0.00**. No production credentials, public hosting,
domain, paid API, managed secret service, customer data, legal advice,
certification audit, SLA, or uptime measurement was used. Local CPU, storage,
workstation power, and founder time are not a funded production operation.
Deferred costs and dependencies are itemized in `..\GATE_B_REGISTER.csv`.
