# Zero-cost options investigated

Recorded 2026-08-21. “Free” means no new cash spend for signing services. It
does not remove the need for a real account, repository, maintainer, network,
or policy review.

## Recommended: public GitHub repository + public Sigstore

GitHub documents standard GitHub-hosted runner usage as free for public
repositories. Sigstore's public-good Fulcio/Rekor deployment is the keyless
signing service used by the official Sigstore action. A public repository in a
verified organization, with protected branches/tags and a protected signing
environment, is the cleanest $0 route:

* `release-signing.yml` signs all four files with `sigstore-python`.
* `actions/attest@v4` creates GitHub provenance and an SBOM predicate.
* Consumers verify the exact certificate SAN, issuer, repository, workflow,
  ref, and commit.

Public visibility is not itself organization trust. The organization and
repository controls still have to be configured and reviewed.

## Private GitHub repository

GitHub Actions Free for organizations includes a monthly allowance (the
current GitHub plan documentation lists 2,000 minutes and 500 MB shared
artifact storage); overage requires billing and can be blocked without a
payment method. Self-hosted runners are free, but their hardware and
isolation are not free assumptions and an untrusted persistent runner is not
appropriate for release signing.

GitHub's artifact-attestation documentation says public repositories use the
public Sigstore instance and a publicly readable transparency log, while
private repositories use GitHub's Sigstore instance without a public
transparency log. Confirm current plan/visibility and decide whether the
private attestation meets the consumer requirement. The independent
`sigstore/gh-action-sigstore-python` Fulcio/Rekor path remains the primary
public-transparency signing path, subject to its real CI/network prerequisites.

## PyPI Trusted Publishing (optional)

For a public Python package, PyPI Trusted Publishing is a second no-token
path. Configure a PyPI Trusted Publisher that matches the real GitHub
organization/repository/workflow/environment, then run
`.github\workflows\pypi-trusted-publishing.yml`. The official PyPA action
uses GitHub OIDC, mints a short-lived PyPI credential, and currently generates
and uploads Sigstore-backed digital attestations for wheel and sdist files.
PyPI documents SLSA Provenance and PyPI Publish attestations.

This does **not** attest `SBOM.json` or `ARTIFACT_MANIFEST.sha256`, so it is
complementary to (not a replacement for) `release-signing.yml`. PyPI's
trusted-publisher configuration and a real upload are required; this local
workspace cannot claim them.

## OpenSSF/SLSA programs and grants

* GitHub artifact attestations provide SLSA v1.0 Build Level 2 according to
  GitHub's documentation. Build Level 3 requires stronger builder isolation
  and trusted/reusable workflow controls.
* `slsa-github-generator` is free, but its official repository now says it is
  no longer actively maintained and recommends GitHub artifact attestations.
  It should not be selected for a new release path.
* OpenSSF/Sigstore infrastructure is grant-supported public-good
  infrastructure. The OpenSSF Sigstore project page does not grant an
  individual project a private signing service or an identity.
* The Linux Foundation's March 17, 2026 announcement describes $12.5M of
  grants managed by Alpha-Omega/OpenSSF for ecosystem security. Alpha-Omega's
  July 23, 2026 seasonal-program announcement says projects must be open
  source, and describes quarterly submission/review/decision phases. As of
  this report's date, its Q3 submission window is listed as July 1–31, so it
  is not an immediate funding route. It is not an automatic free CI quota or
  an instant signing grant. A project would need an OSI-approved license,
  broad security impact, selection, and a grant agreement.
  RC3's `pyproject.toml` declares MIT, but that alone does not establish
  eligibility or criticality.
* GitHub Education, GitHub Sponsors, and OpenSSF Scorecard can help eligible
  projects or governance, but none grants an organization-trusted Fulcio
  identity. No grant was assumed or claimed for ZoracleFlux.

Official grant references:

* https://alpha-omega.dev/blog/announcing-the-new-alpha-omega-seasonal-grant-program/
* https://openssf.org/press-release/2026/03/17/linux-foundation-announces-12-5-million-in-grant-funding-from-leading-organizations-to-advance-open-source-security/

## Rejected as organization trust

* Local OpenSSH, GPG, minisign, or cosign key-pair signatures: cryptographically
  valid but only as strong as an out-of-band public-key trust anchor.
* A self-generated Fulcio-like certificate or local “bundle”: not a Sigstore
  production identity and must not be fabricated.
* A free cloud CI account without a protected organization/repository policy:
  it may sign, but the consumer cannot make the requested organization-trust
  claim.
