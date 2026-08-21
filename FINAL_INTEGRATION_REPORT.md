# ZoracleFlux RC3 final integration and claim audit

**Artifact:** `C:\Users\ziada\.copilot\chats\70b7f34f-e807-4a08-ae86-c1745773252f\artifacts\zoracleflux\final-release-candidate-rc3`

**Date:** 2026-08-21. **Cash:** `$0.00`. **Credentials:** none. **External
validation:** none. The prior `final-release-candidate` and all workstream
folders are preserved.

## Precise verdict

**ZERO-CASH SELF-HOSTED PILOT-READY — NOT FUNDED PRODUCTION-READY.** The
package payload is still `ZoracleFlux 1.0.0rc2`; RC3 is an isolated integration
bundle. No claim of 100%, public production readiness, customer validation,
certification, uptime, SLA, hosted deployment, or managed security is made.

## Integrated evidence

* Claude/Codex: `support\claude-codex` report integrated as `claude-code\`,
  `codex\`, and `harness\`. Direct CLI, plugin, skill, stdio MCP and negative
  contracts passed. Native clients were absent from PATH and remain **unverified**.
* Signing: `support\signing` copied to `signing\`. OpenSSH Ed25519 detached
  signatures cover wheel, sdist, SBOM and preserved manifest. Private key is
  absent/deleted. Sigstore/Fulcio/Rekor/OIDC was not executed.
* Production: production-shaped local overlay under `support\production\`,
  including non-root/read-only/no-network Compose shape, secrets guidance,
  audit JSONL, Prometheus text metrics, health, threat, backup/restore and
  Gate-B/legal/security/SLA templates. Docker was unavailable.
* Antigravity (release-blocking priority): platform and registration are
  verified; native authenticated tool call is explicitly **unverified here**.
  The exact blocker is absent account state in the isolated host and no
  unauthenticated CLI `tools/call` surface. Tested fallback is
  `zoracleflux check --json`; exact user-run steps are in
  `support\antigravity\REPORT.md`.

## Commands and literal final outputs

All commands below were run from the RC3 root in a fresh `.venv` (removed after
validation):

```text
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements.lock
.\.venv\Scripts\python.exe -m pip install .
```

Literal versions:

```text
Python 3.10.1
zoracleflux --version => 1.0.0rc2
pytest==9.1.1; setuptools==75.8.0; wheel==0.45.1
node --version => v22.12.0; npm.cmd --version => 10.9.0
claude --version => executable not found on PATH — UNAVAILABLE
codex --version => executable not found on PATH — UNAVAILABLE
```

Core checks:

```text
zoracleflux doctor --json
=> {"status":"passed","offline_default":true,"network_calls":0,"model_calls":0,"python":"3.10.1","version":"1.0.0rc2"}

zoracleflux check --json
=> {"counts":{"failed":0,"passed":13,"total":13},"model_calls":0,"network":false,"status":"passed","summary":"13/13 declared relations passed","version":"1.0.0rc2"}

zoracleflux pilot --runs 2 --json
=> {"cash_spend_usd":0.0,"runs":[{"passed":13,"relations":13,"status":"passed"},{"passed":13,"relations":13,"status":"passed"}],"status":"passed","version":"1.0.0rc2"}

python -m pytest -q
=> ...................... [100%]  (22 passed)

python evaluation\run_evaluation.py
=> {"cash_spend_usd":0.0,"false_failure_rate":0.0,"mutation_killed":5,"mutation_score":1.0,"mutation_total":5,"network_calls":0,"relation_passed":13,"relation_total":13,"unknown_tag_negative_fixture_present":true,"version":"1.0.0rc2"}
```

Adapter and local-security checks:

```text
python harness\compatibility_contract.py
=> {"status":"passed","output":"harness\\compatibility-contract.json","native_clients":"UNVERIFIED"}

python -m unittest discover -s support\antigravity -p test_protocol.py -v
=> Ran 3 tests in 1.551s; OK

python support\production\threat_tests.py
=> {"checks":{"audit_allowlist":"pass","backup_path_traversal_rejected":"pass","health_missing_db_is_safe":"pass","metrics_no_network":"pass","overlay_static_boundary":"pass"},"schema_version":1,"status":"passed"}

python support\production\healthcheck.py --root . --db .zoracleflux\pilot.sqlite3
=> {"checks":{"database_parent":"pass","package_present":"pass","sqlite_integrity":"pass"},"component":"zoracleflux-local-pilot","schema_version":1,"status":"passed"}

python support\production\backup.py backup ...
=> {"cash_usd":"0.00","sqlite_integrity":true,"sha256":"453d4fd4bd959be3c04db59d0295f2c5e56ee639ae7b2cab1a4b9b874a95af98"}

python support\production\backup.py restore ...
=> {"sqlite_integrity":true,"sha256":"453d4fd4bd959be3c04db59d0295f2c5e56ee639ae7b2cab1a4b9b874a95af98"}
```

Antigravity installed-runtime evidence:

```text
installed IDE: 1.107.0
commit: ecfbad74d93962fc8ca485d93ab9b4f3d4cb6cf8
installed CLI wrapper: antigravity-ide.cmd --version => 1.107.0
agy alias: NOT_FOUND
registration: --add-mcp smoke passed
MCP initialize: protocolVersion 2025-06-18
MCP tools: zoracleflux_check, zoracleflux_doctor
native authenticated tools/call: UNVERIFIED — isolated host could not obtain account state
```

## Support matrix

| Surface | Status | Exact boundary |
|---|---|---|
| ZoracleFlux CLI / oracleforge | **Verified** | Clean install; doctor/check/pilot and 22 tests pass |
| Claude Code fallback | **Verified** | Direct CLI, plugin/skill and stdio MCP contract; no native client installed |
| Claude Code native runtime | **Unverified** | `claude` unavailable on PATH; no credentials or fake invocation |
| Codex fallback | **Verified** | Direct CLI, plugin/skill and stdio MCP contract; no native client installed |
| Codex native runtime | **Unverified** | `codex` unavailable on PATH; no credentials or fake invocation |
| Antigravity platform/MCP registration | **Verified** | IDE 1.107.0, commit above; `--add-mcp`, schema and stdio protocol pass |
| Antigravity native authenticated tool call | **Unverified here** | Account-state environment blocker; tested fallback and exact user steps provided |
| Production local pilot | **Verified locally** | Threat 5/5, health, metrics, backup/restore pass |
| Docker/Compose deployment | **Unverified locally** | `docker` not recognized; no hosted deployment claim |

## Signatures, trust, and hashes

Signature command:

```text
python signing\verify_signatures.py --signatures-only
=> exit 0; wheel PASS; sdist PASS; sbom PASS; manifest PASS
fingerprint: SHA256:TwyPworhpQ2AJG0hF8jr3PXF/FIY+Cnm9a7CwVtjKF4
```

The full verifier returns exit `1` by design because the preserved old manifest
has stale generated entries and RC3 integration edits are not in that old
manifest. This is not hidden or repaired by rewriting the signed manifest.
The fresh RC3 manifest excludes mutable `.zoracleflux\` state and `evaluation\results.json`; it verifies independently:

```text
RC3 manifest verify: 0 mismatches; entries=156
```

Trust level: **local out-of-band demonstration key only**. It has no
organization authentication, maintainer identity, timestamp authority,
Sigstore certificate, Rekor transparency entry, or OIDC binding. The private
key was deleted; consumers must authenticate the public key out of band.

| Artifact | SHA-256 |
|---|---|
| `dist\zoracleflux-1.0.0rc2-py3-none-any.whl` | `67142421933973cbc91890eafcb9a6c8345bcc9f578671359a7d9c96ffdc7d8b` |
| `dist\zoracleflux-1.0.0rc2.tar.gz` | `b27f6ce1335c808db2c9181715af198962ea99f17ddeeb8d694f87b50618d33e6` |
| `SBOM.json` | `ee9ccf8abb4a7e7945357fa25a937f2fdee550177face3ee0842b6931625f6bb` |
| `ARTIFACT_MANIFEST.sha256` (preserved signed) | `64bfddf5c0c87a55cbca21da4fcbdac69e37b4af2a06eea074beb596a294e2a1` |
| `RC3_INTEGRATION_MANIFEST.sha256` | `93ded6662ce23cb67f9ac90d5d86a9643ddd3467dcde06b1fa538d4faf1b54da` |
| `signing\zoracleflux-release-signing-key.pub` | `972194c9dfcdde7e6f5850bea6a5204afe53b4ebeba911c86429a7ba6d157e2c` |

## Local deploy status and gaps

**Local deploy:** pilot-ready. Offline CLI, SQLite ledger, audit JSONL,
Prometheus text metrics, health, threat tests, backup/restore and runbooks are
usable without credentials or network. Compose is a configuration shape only;
Docker was unavailable. There is no public endpoint, ingress, DNS/TLS, tenant
identity, managed/HSM secret store, off-host encrypted backup, alert delivery,
on-call team, vulnerability-monitoring process, or uptime measurement.

**Legal/certification/SLA gaps:** privacy policy, terms, security policy, incident
runbook, certification-readiness and SLA files are templates requiring owner,
legal, customer and operational completion. No DPA, legal approval, independent
security review, SOC 2/ISO certification, regulatory assessment, paid support,
SLO/SLA target or availability evidence exists.

**Evidence gaps:** no customer interviews/WTP, public repository evaluation,
production traffic, authenticated native Claude/Codex/Antigravity invocation,
organization-trusted signing, or Sigstore evidence. Current evaluation is
synthetic and bounded; mutation score `1.0` is not a proof of general quality.
See `FINAL_GAP_REGISTER.md` for exact handoffs.

## Accounting

All four workstreams and integration record `$0.00` incremental cash. Local CPU,
storage, electricity, founder time, existing subscriptions, external network
services, legal work and production operations are not treated as funded
capacity. No production credentials were used.




