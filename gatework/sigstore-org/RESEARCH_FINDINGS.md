# Official research findings

Research date: 2026-08-21. These findings are about capability and policy;
they are not evidence that ZoracleFlux has a live organization identity.

| Source | Finding relevant to this workstream |
|---|---|
| GitHub OIDC overview | A job receives a unique JWT containing repository, owner, workflow, ref, SHA, environment, event, and issuer claims. `id-token: write` is required. Consumers must enforce exact claim values. |
| Fulcio OIDC documentation | Fulcio uses an OIDC token to bind an ephemeral key to a short-lived certificate. The certificate identity is the CI identity, not a local key or an organization badge. |
| Rekor project documentation | Rekor is an append-only transparency log for signed supply-chain metadata. A signature is not organization-trusted merely because it has a valid certificate; inclusion/transparency evidence and identity policy are required. |
| Cosign official README | `cosign sign-blob --bundle FILE.sigstore.json --yes FILE` and `cosign verify-blob` support keyless blob signing and exact certificate identity/issuer checks. |
| sigstore-python README/docs | `sigstore sign` emits `.sigstore.json` bundles; `sigstore verify identity` requires certificate identity and issuer; `sigstore verify github` checks GitHub-specific claims such as repository, workflow, ref, trigger, name, and SHA. |
| gh-action-sigstore-python v3.4.0 | Official action uses ambient GitHub Actions OIDC credentials, accepts globs/multiple files, and can verify generated signatures with `verify-cert-identity` and `verify-oidc-issuer`. |
| GitHub artifact attestations | `actions/attest@v4` uses `id-token: write`, `contents: read`, and `attestations: write`; it can create SLSA provenance and SBOM predicates. Public repositories use public Sigstore/Rekor; private repositories use GitHub's Sigstore instance without a public transparency log. |
| GitHub billing/plans | Standard hosted runners are free for public repositories. Private repositories receive a plan quota (GitHub Free for organizations currently lists 2,000 minutes/500 MB); overage requires billing or is blocked. Self-hosted runners have no runner charge but introduce custody/isolation risk. |
| SLSA v1.0 | Build L2 means signed provenance from a hosted builder; Build L3 requires hardened builder isolation. GitHub says artifact attestations provide Build L2. |
| slsa-github-generator | Official repository says it is no longer actively maintained and recommends GitHub artifact attestations for new GitHub workflows. |
| PyPI Trusted Publishers | A real PyPI project can trust a specific GitHub repository/workflow/environment. PyPI mints a short-lived upload credential from OIDC, and the official PyPA action generates/uploads digital attestations for wheel and sdist trusted-publishing flows. It does not cover this SBOM or manifest. |
| OpenSSF/Sigstore and Alpha-Omega | Sigstore is public-good grant-supported infrastructure. Alpha-Omega's seasonal grants target open-source security projects and require selection, an open-source license, and an application; a grant is not an instant signing identity, CI quota, or prerequisite for public Sigstore. |

## Cost conclusion

The strongest no-new-cash route is a public repository in a verified
organization, protected release workflow/environment, standard GitHub-hosted
runner, and public Fulcio/Rekor. No purchased key, API token, or grant is
needed. The user must supply the actual organization/repository, governance,
and one real Actions run.

The strict combination “public Rekor + GitHub artifact attestation” is
visibility/plan dependent. For a private free organization, use the
independent public Sigstore workflow if public transparency is required and
verify whether GitHub's private attestation service is available/acceptable.

## Local execution boundary

Executed locally: Python/YAML/JSON validation, deterministic manifest
generation, RC3 hash checks, and 4/4 OpenSSH fallback verification. Not
possible locally: GitHub OIDC token acquisition, protected environment
approval, Fulcio certificate issuance, Rekor inclusion, GitHub attestation,
PyPI Trusted Publisher exchange, or an organization-trust claim. No such
evidence was fabricated.

Sigstore's docs host intermittently failed DNS/TLS retrieval in this
environment. Official GitHub source repositories and GitHub/PyPI/SLSA/OpenSSF
documentation were reachable; all authoritative URLs are listed in
`ORG_TRUSTED_SIGNING.md`.
