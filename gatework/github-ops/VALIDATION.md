# Local validation record

Date: 2026-08-21. Workspace: Windows 11-style host. Spend: **$0.00**.
No GitHub token, cloud credential, endpoint, domain, or external service was
used.

## Tool versions

```text
Python 3.10.1
pytest 9.1.1
PyYAML 6.0.2
Node v22.12.0
Git 2.53.0.4
```

## Results

Commands were run from the preserved RC3 root unless noted:

```text
python -m pytest -q
=> 22 passed

python -m compileall -q src tests harness evaluation support
=> compileall=passed

python evaluation\run_evaluation.py
=> relation_passed=13, relation_total=13, mutation_score=1.0,
   false_failure_rate=0.0, network_calls=0, model_calls=0,
   cash_spend_usd=0.0, version=1.0.0rc2

python support\production\threat_tests.py
=> 5/5 checks passed

python harness\compatibility_contract.py
=> status=passed; native_clients=UNVERIFIED
```

Bundle checks:

```text
python -m py_compile scripts\github_backup_export.py
=> passed
python -m compileall -q scripts
=> compileall=passed
PyYAML safe_load of all 10 .yml/.yaml files
=> all parsed; GitHub's `on` key is intentionally interpreted as a boolean
   by YAML 1.1 parsers, but is valid workflow syntax for GitHub's parser
Local Git bundle export smoke test with --no-api
=> backup-export=passed; repository.bundle, manifest.json,
   API_EXPORT_SKIPPED.txt and SHA256SUMS.txt produced

Expanded free-option checks:

```text
node cloudflare-worker-reference\test.mjs
=> health adapter assertions passed
PyYAML safe_load of all .yml/.yaml files
=> 12 parsed
```

The Worker check is an in-process health-only adapter test. It is not a
Cloudflare deployment and does not execute ZoracleFlux.
```

## Hashes

`SHA256SUMS.txt` is generated after this report is complete. It covers every
bundle file except itself and this file's generated hash line is therefore
intentionally absent from the manifest if the report is edited later.

## Not proven

This local run cannot prove a real repository's Pages settings or URL, release
permissions, branch protection, environment reviewers, secret redaction,
OIDC trust, CodeQL/Dependabot service results, schedule delivery, artifact
retention, external backup restore, endpoint availability, DNS/TLS, provider
free-tier eligibility, alert delivery, an on-call rota, customer traffic,
privacy/legal approval, certification, or production spend. Those are explicit
deployment checklist gates.
