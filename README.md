# ZoracleFlux 1.0.0rc4 gate integration

RC4 preserves the RC3 payload and integrates three independently validated gate
bundles under `gatework\`: compliance, GitHub-ops, and Sigstore organization-
trusted signing design. The executable package remains `1.0.0rc2`; RC4 is a
gate/evidence bundle, not a new package payload.

## Verdict

**Zero-cash self-hosted pilot-ready; not funded production-ready.** Compliance,
GitHub-ops and Sigstore workflows are validated designs/local checks. No live
GitHub repository, OIDC token, Fulcio certificate, Rekor entry, Sigstore bundle,
attestation, endpoint, on-call response, legal approval, certification, SLA,
customer validation, or public production deployment is claimed.

## Beginner setup

ZoracleFlux is an offline-first Python package for a local, zero-cash developer
preview. Use Python 3.10, 3.11, or 3.12.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-deps .
zoracleflux doctor --json
zoracleflux check --json
zoracleflux pilot --runs 1 --json
```

The package does not require an account, API key, network access, model, or
managed service. Run `python -m pytest -q` for the local regression suite.
`zoracleflux generate` writes reviewable pytest checks under the working
directory. Claude, Codex, and Antigravity integrations are fallback
adapters/contracts; native authenticated client execution remains explicitly
unverified unless you run and record it yourself.

## Gate bundles

* `gatework\compliance`: 20 files, 17 controls, 15 evidence mappings, 17
  no-cash pathways, 10 templates; bundle check and 24-hash evidence pass.
  Synthetic uptime is explicitly `NON_PRODUCTION_EVIDENCE_ONLY`.
* `gatework\github-ops`: 30 files / 57,992 bytes; supplied SHA manifest
  `a831765aa814cb35efb301336e83d461cedc5c0f34c819376f9a2ef97675a2fa`;
  22 RC3 tests, 12 YAML, syntax, local backup-export, npm adapter and 10/10
  official URL probes are reported pass. GitHub account/settings, Pages,
  branch protection, scheduled workflows and real endpoint remain unproven.
* `gatework\sigstore-org`: pinned OIDC/Fulcio/Rekor and GitHub attestation
  workflows, fail-closed verifier, policy, setup and fallback. JSON/YAML/Python
  checks pass; OpenSSH fallback is 4/4. Sigstore bundles present: `0`
  intentionally; no OIDC run occurred and no organization-trusted claim is made.

## Core regression rerun

```text
python -m pytest -q => 22 passed
python evaluation\run_evaluation.py => relation_passed=13, relation_total=13,
  mutation_score=1.0, false_failure_rate=0.0, network_calls=0,
  model_calls=0, cash_spend_usd=0.0, version=1.0.0rc2
python support\production\threat_tests.py => 5/5 checks passed
python harness\compatibility_contract.py => status=passed; native_clients=UNVERIFIED
python signing\verify_signatures.py --signatures-only => exit 0; wheel/sdist/
  sbom/manifest PASS; fingerprint SHA256:TwyPworhpQ2AJG0hF8jr3PXF/FIY+Cnm9a7CwVtjKF4
```

Gatework local checks:

```text
py -3.10 gatework\compliance\tools\check_bundle.py
=> PASS files=20 controls=17 evidence_map=15 pathways=17 templates=10
   synthetic=PASS no-network=true
PyYAML safe_load GitHub workflows => YAML parsed: 12
node gatework\github-ops\cloudflare-worker-reference\test.mjs
=> health adapter assertions passed
Sigstore provenance-policy JSON => JSON: PASS
Sigstore workflow YAML => YAML: PASS
Sigstore scripts py_compile => PASS
```

## Trust and claim boundary

The preserved RC3 payload's local OpenSSH Ed25519 signatures remain valid, but
trust is only an out-of-band demonstration key. The Sigstore path is a pinned,
fail-closed production design requiring protected GitHub governance, exact
workflow identity, `id-token: write`, Fulcio/Rekor availability and a real CI
run. The GitHub-ops bundle is a copyable overlay, not proof that repository
settings or workflows ran. The compliance bundle is self-assessment/templates,
not legal advice, a DPA, certification, or independent audit.

`RC4_GATE_MANIFEST.sha256` has 237 entries and verifies with 0 mismatches. See `FINAL_GATE_REPORT_RC4.md` for the complete command/output/hash audit and
exact blockers. RC3 remains at `..\final-release-candidate-rc3` unchanged.
