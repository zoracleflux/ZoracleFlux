# ZoracleFlux organization-trusted release signing

Recorded 2026-08-21. This workstream is confined to
`artifacts\zoracleflux\gatework\sigstore-org`; the RC3 directory is unchanged.
Cash spend: **$0**. No production secret or private Sigstore key is used.

## Decision and claim boundary

The recommended production path is GitHub Actions OIDC + public Sigstore:

1. The protected GitHub workflow receives an ephemeral OIDC token
   (`id-token: write`).
2. Fulcio authenticates that token and issues a short-lived certificate for an
   ephemeral signing key.
3. The signature, certificate, and inclusion evidence are recorded in Rekor
   (the workflow pins the official action's Rekor v1 input; update deliberately
   if the repository's approved client moves to Rekor v2).
4. `sigstore-python` verifies the bundle against the exact GitHub workflow
   identity. GitHub's `actions/attest` separately creates an artifact
   attestation/provenance record.

No such OIDC run occurred in this environment. Therefore this directory
contains **no `.sigstore`/`.sigstore.json` bundle** and makes no live identity,
Fulcio certificate, Rekor entry, or GitHub attestation claim. The workflow and
verifier are executable designs, not evidence of a completed CI signing run.

The preserved RC3 payload is:

| Item | SHA-256 |
|---|---|
| `dist\zoracleflux-1.0.0rc2-py3-none-any.whl` | `67142421933973cbc91890eafcb9a6c8345bcc9f578671359a7d9c96ffdc7d8b` |
| `dist\zoracleflux-1.0.0rc2.tar.gz` | `b27f6ce1335c808db2c9181715af198962ea99f17ddeb8d694f87b50618d33e6` |
| `SBOM.json` | `ee9ccf8abb4a7e7945357fa25a937f2fdee550177face3ee0842b6931625f6bb` |
| `ARTIFACT_MANIFEST.sha256` | `64bfddf5c0c87a55cbca21da4fcbdac69e37b4af2a06eea074beb596a294e2a1` |

These are fresh `Get-FileHash` results and are the source of truth for this
report; the RC3 manifest itself records the candidate's historical digest. The
existing RC3 manifest has three stale generated entries, as documented by RC3.
It was not rewritten.

## What “organization trusted” means

It is a policy claim, not a special Sigstore organization key:

* **Workflow identity:** the Fulcio certificate SAN must be exactly
  `https://github.com/ORG/REPO/.github/workflows/release-signing.yml@refs/tags/vX`
  (or the exact protected `refs/heads/main` rehearsal ref). The issuer must be
  `https://token.actions.githubusercontent.com`. Verification must constrain
  both; accepting any Sigstore certificate or any `ORG/*` workflow is not
  organization trust.
* **Protected source:** the workflow file and build scripts are reviewed by
  CODEOWNERS, the default branch is protected, release tags are restricted, and
  Actions are pinned to immutable commit SHAs. A tag/release run is the only
  production trigger.
* **Protected environment:** the `release-signing` environment requires
  organization maintainers as reviewers and is limited to the protected
  branch/tag rules. Approval is a human release authorization, not a secret.
* **Verified organization:** organization ownership/domain verification and
  repository governance let consumers identify the maintainer. They are
  GitHub governance signals; they do not change Fulcio's CA root or make a
  repository name alone trustworthy.
* **Provenance:** the exact commit, ref, workflow path, run, and artifact
  digest are visible in the OIDC claims and GitHub attestation. Rekor provides
  public append-only transparency evidence. Consumers should pin the
  repository, workflow, ref/tag policy, and (for a release) commit SHA.

The certificate proves what GitHub workflow identity signed. The protected
organization/repository proves who was allowed to run that workflow. Both
layers are required for this workstream's trust decision.

## Files in this gatework

* `.github\workflows\release-signing.yml` — reusable build/sign/verify/
  attestation workflow. It signs the wheel, sdist, `SBOM.json`, and a fresh
  deterministic `ARTIFACT_MANIFEST.sha256`.
* `.github\workflows\pypi-trusted-publishing.yml` — optional PyPI
  Trusted Publishing path. It is intentionally separate and covers only
  wheel/sdist registry attestations.
* `scripts\create_release_manifest.py` — does not include itself, so the
  manifest can be signed without a circular digest.
* `scripts\verify_sigstore.py` — fail-closed local/CI verifier. It requires a
  sidecar bundle and exact GitHub identity; it never creates a bundle.
* `provenance-policy.json` — machine-readable consumer policy with placeholders.
* `scripts\local_fallback_verify.py` and `fallback\` — offline RC3 OpenSSH
  fallback trust material copied from RC3. The private key is absent.
* `THREAT_MODEL.md` — threats, controls, and recovery.
* `SETUP.md` — exact organization/repository setup and consumer commands.
* `RESEARCH_FINDINGS.md` and `ZERO_COST_OPTIONS.md` — official-source
  findings, free eligibility, and grants/programs considered.
* `LOCAL_TEST_OUTPUT.txt`, `TOOL_VERSIONS.txt`, and `HASHES.sha256` — literal
  local evidence.

## Official references researched

* GitHub OIDC overview and claims:
  https://docs.github.com/en/actions/concepts/security/openid-connect
* GitHub OIDC hardening:
  https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments
* GitHub artifact attestations:
  https://docs.github.com/en/actions/concepts/security/artifact-attestations
  and
  https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
* GitHub CLI attestation verification:
  https://cli.github.com/manual/gh_attestation_verify
* GitHub Actions billing and plans:
  https://docs.github.com/en/billing/concepts/product-billing/github-actions
  and https://docs.github.com/en/get-started/learning-about-github/githubs-plans
* PyPI Trusted Publishers:
  https://docs.pypi.org/trusted-publishers/
* PyPI digital attestations:
  https://docs.pypi.org/attestations/
* PyPI attestation consumption:
  https://docs.pypi.org/attestations/consuming-attestations/
* PyPA publishing action:
  https://github.com/pypa/gh-action-pypi-publish
* SLSA levels:
  https://slsa.dev/spec/v1.0/levels
* SLSA GitHub generator status:
  https://github.com/slsa-framework/slsa-github-generator
* OpenSSF Sigstore project:
  https://openssf.org/projects/sigstore/
* Linux Foundation/OpenSSF grants announcement:
  https://openssf.org/press-release/2026/03/17/linux-foundation-announces-12-5-million-in-grant-funding-from-leading-organizations-to-advance-open-source-security/
* Alpha-Omega seasonal grants:
  https://alpha-omega.dev/blog/announcing-the-new-alpha-omega-seasonal-grant-program/
* Sigstore Python client:
  https://github.com/sigstore/sigstore-python
  and https://sigstore.github.io/sigstore-python/verify/
* Official Sigstore Python GitHub Action:
  https://github.com/sigstore/gh-action-sigstore-python
* Fulcio OIDC:
  https://docs.sigstore.dev/certificate_authority/oidc-in-fulcio/
* Sigstore signing overview:
  https://docs.sigstore.dev/cosign/signing/overview/
* Cosign blob signing/verification:
  https://github.com/sigstore/cosign
* Rekor transparency log:
  https://github.com/sigstore/rekor
* Sigstore CI quickstart:
  https://docs.sigstore.dev/quickstart/quickstart-ci/

The GitHub pages and GitHub source pages were reachable during research. The
Sigstore docs host intermittently returned DNS/TLS transport errors from this
Windows environment; the URLs are retained as the authoritative references,
and the official GitHub source documentation was inspected where available.
