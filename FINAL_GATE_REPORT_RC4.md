# ZoracleFlux RC4 final gate integration and audit

**Artifact path:** `C:\Users\ziada\.copilot\chats\70b7f34f-e807-4a08-ae86-c1745773252f\artifacts\zoracleflux\final-release-candidate-rc4`

**Date:** 2026-08-21. **Cash:** `$0.00`. **Credentials/accounts:** none used.
**Prior RC3:** preserved unchanged at sibling path. **Payload:**
`ZoracleFlux 1.0.0rc2`; RC4 is a gate/evidence bundle, not a new package
release.

## Final verdict

**ZERO-CASH SELF-HOSTED PILOT-READY — NOT FUNDED PRODUCTION-READY.** The three
new gate bundles are locally validated designs and evidence mappings. They do
not prove live GitHub governance, OIDC/Sigstore identity, production uptime,
legal approval, certification, SLA, customer validation, or public deployment.
No 100% or public-production claim is made.

## Gate-bundle inventory and literal validation

### Compliance

Path: `gatework\compliance`.

```text
files=20
controls=17
evidence_map=15
pathways=17
templates=10
cash=$0.00
```

Commands and final output:

```text
py -3.10 gatework\compliance\tools\check_bundle.py
=> PASS files=20 controls=17 evidence_map=15 pathways=17 templates=10 synthetic=PASS no-network=true

py -3.10 -m py_compile gatework\compliance\tools\check_bundle.py gatework\compliance\tools\synthetic_uptime.py
=> exit 0
```

The captured compliance evidence also records:

```text
GENERATED synthetic=true samples=24
PASS synthetic=true samples=24 available=24 availability=1.000000 target=0.999000 NON_PRODUCTION_EVIDENCE_ONLY
PASS manifest_entries=24
Python 3.12.3
git version 2.53.0.windows.4
```

The 10 templates are explicitly drafts. GDPR/UK GDPR/state privacy, breach,
employment, export, accessibility, sectoral and consumer-law applicability
remain counsel decisions. SOC 2 requires an independent CPA attestation; ISO
27001 certification requires an accredited certification body. Synthetic uptime
is a tool test and **not production availability evidence**.

### GitHub-ops

Path: `gatework\github-ops`. Supplied bundle: 30 files, 57,992 bytes; supplied
SHA manifest digest:
`a831765aa814cb35efb301336e83d461cedc5c0f34c819376f9a2ef97675a2fa`.

The supplied validation report records:

```text
Python 3.10.1
pytest 9.1.1
PyYAML 6.0.2
Node v22.12.0
Git 2.53.0.4
python -m pytest -q => 22 passed
python -m compileall -q src tests harness evaluation support => compileall=passed
python evaluation\run_evaluation.py => 13/13, mutation_score=1.0,
  false_failure_rate=0.0, network_calls=0, model_calls=0, cash_spend_usd=0.0
python support\production\threat_tests.py => 5/5 checks passed
python harness\compatibility_contract.py => status=passed; native_clients=UNVERIFIED
PyYAML safe_load of all .yml/.yaml files => all parsed (12 in expanded check)
node cloudflare-worker-reference\test.mjs => health adapter assertions passed
```

RC4 rerun outputs:

```text
PyYAML workflow parse => YAML parsed: 12
node gatework\github-ops\cloudflare-worker-reference\test.mjs
=> health adapter assertions passed
py_compile github_backup_export.py => exit 0
compileall scripts => exit 0
```

The bundle contains CI/release/Pages/security/backup/uptime workflows,
Dependabot, issue/PR templates, pinned Scorecard, static Pages documentation,
backup/export and a health-only Cloudflare reference. It does **not** prove a
real repository's branch protection, Pages/environment settings, workflow run,
secrets redaction, OIDC trust, artifact retention, backup restore, endpoint,
DNS/TLS, alert delivery, free-tier eligibility or on-call response. The
Cloudflare adapter does not execute ZoracleFlux.

### Sigstore organization-trusted signing

Path: `gatework\sigstore-org`.

```text
py -3.10 -c "import json; json.load(open('gatework/sigstore-org/provenance-policy.json')); print('JSON: PASS')"
=> JSON: PASS
py -3.10 -m py_compile create_release_manifest.py verify_sigstore.py local_fallback_verify.py
=> PASS
YAML release-signing.yml + pypi-trusted-publishing.yml
=> YAML: PASS
Sigstore bundles present: 0 (intentional)
```

Copied manifest checks: compliance `HASHES.sha256` = 24 entries / 0 mismatches; GitHub-ops `SHA256SUMS.txt` = 29 entries / 0 mismatches. Sigstore `HASHES.sha256` intentionally retains RC3-relative and fallback provenance paths as documented.\n\nThe fail-closed missing-bundle test is preserved:

```text
verify_sigstore.py ...
=> FAIL ... bundle missing: ...zoracleflux-1.0.0rc2-py3-none-any.whl.sigstore.json
=> exit 1 (expected fail-closed result)
```

No GitHub OIDC run occurred. Therefore there is no Fulcio certificate, Rekor
entry, `.sigstore` bundle, GitHub attestation or organization-trusted claim.
The recommended path is protected GitHub workflow + `id-token: write` + exact
Fulcio/Rekor identity policy; the workflow is a design, not completed CI
identity evidence. Optional PyPI Trusted Publishing is also unexecuted.

## RC4 regression and preserved release trust

```text
python -m pytest -q
=> ...................... [100%] 22 passed

python evaluation\run_evaluation.py
=> relation_passed=13, relation_total=13, mutation_score=1.0,
   false_failure_rate=0.0, network_calls=0, model_calls=0,
   cash_spend_usd=0.0, version=1.0.0rc2

python support\production\threat_tests.py
=> 5/5 checks passed

python harness\compatibility_contract.py
=> {"status":"passed","native_clients":"UNVERIFIED"}

python signing\verify_signatures.py --signatures-only
=> exit 0; wheel PASS; sdist PASS; sbom PASS; manifest PASS
fingerprint SHA256:TwyPworhpQ2AJG0hF8jr3PXF/FIY+Cnm9a7CwVtjKF4
```

Payload hashes remain:

| Item | SHA-256 |
|---|---|
| wheel | `67142421933973cbc91890eafcb9a6c8345bcc9f578671359a7d9c96ffdc7d8b` |
| sdist | `b27f6ce1335c808db2c9181715af198962ea99f17ddeeb8d694f87b50618d33e6` |
| SBOM | `ee9ccf8abb4a7e7945357fa25a937f2fdee550177face3ee0842b6931625f6bb` |
| preserved signed manifest | `64bfddf5c0c87a55cbca21da4fcbdac69e37b4af2a06eea074beb596a294e2a1` |
| RC3 public key | `972194c9dfcdde7e6f5850bea6a5204afe53b4ebeba911c86429a7ba6d157e2c` |


RC4 integration manifest:

```text
RC4 gate manifest entries: 237
RC4 gate manifest verify: 0 mismatches; entries=237
RC4_GATE_MANIFEST.sha256 => d4147da74c185a15f6471aee647a9cf0c987bb0cd62b8dac2601ba3c00b1a366
```

The RC4 manifest excludes mutable `.zoracleflux\` state, `evaluation\results.json`,
transient caches and this report itself. It is a fresh integrity manifest, not
an organization-trusted signature.

Signing trust remains **local out-of-band demonstration key only**. The private
key was deleted; there is no organization identity or transparency binding.
The preserved RC3 manifest has known stale generated entries; RC4 gate manifests
are evidence bundles, not organization-signed release manifests.

## Support and deployment matrix

| Surface | Status | Boundary |
|---|---|---|
| Core package/CLI | verified locally | 22 tests, 13/13 bounded evaluation; payload 1.0.0rc2 |
| Claude fallback | verified | direct CLI/plugin/skill/MCP contract |
| Claude native | unverified | executable absent from PATH |
| Codex fallback | verified | direct CLI/plugin/skill/MCP contract |
| Codex native | unverified | executable absent from PATH |
| Antigravity platform/MCP | verified | IDE 1.107.0 registration/schema/stdio |
| Antigravity authenticated native call | unverified here | isolated account-state blocker; fallback tested |
| Compliance | local/design verified | self-assessment/templates; no legal or audit opinion |
| GitHub-ops | locally validated overlay | no live repo/settings/workflow/endpoint evidence |
| Sigstore | policy/workflow/fail-closed verifier validated | zero live bundles; no OIDC/Fulcio/Rekor evidence |
| Local production-shaped pilot | verified locally | threat/health/backup/restore pass; Docker unavailable |
| Hosted production | not ready | no public endpoint, identity, managed secrets, on-call or SLA |

## Legal, certification, SLA and operational gaps

Still absent: counsel-approved privacy/terms/DPA, data retention and deletion
controls in operation, signed customer contracts, vulnerability disclosure
ownership, incident response ownership, support/on-call rota, independent
security review, SOC 2/ISO certification, regulatory assessment, real endpoint
and uptime history, alert delivery, backup restore off-host, tenant isolation,
managed/HSM-backed secrets, DNS/TLS, funded compute, customer traffic,
customer interviews/WTP, authenticated native client evidence, protected GitHub
repository governance, OIDC identity run, Fulcio/Rekor inclusion, attestations,
and organization-trusted RC4 release signing.

## Accounting and preserved artifacts

Incremental cash across RC3 and all three gate bundles: **$0.00**. No accounts,
credentials, production secrets, customer data, paid services, live endpoints,
public hosting, legal advice or certification services were used. RC3 is
preserved; RC4 contains copied gatework provenance and the fresh gate report.




