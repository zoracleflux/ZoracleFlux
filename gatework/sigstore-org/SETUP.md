# Exact setup and use

Replace `ORG/REPO` with the real, verified GitHub organization and repository.
Do not use a personal fork for a production trust decision.

## Maintainer setup

1. Put the following gatework files in the repository at the same paths:
   `scripts/create_release_manifest.py`, `scripts/verify_sigstore.py`, and
   `.github/workflows/release-signing.yml`. Keep the workflow path unchanged or
   update the identity in both the workflow and verifier.
2. Commit them through normal review. Require two CODEOWNERS approvals for
   `.github/workflows/**`, `scripts/**`, `SBOM.json`, and packaging files.
   Pin every third-party action to a reviewed commit SHA (the supplied workflow
   already does this for its five unique third-party actions).
3. In the organization, enable Actions OIDC and restrict allowed actions to
   reviewed/pinned actions. Require a verified organization/domain, 2FA, and
   least-privilege repository access.
4. Protect `main`: pull requests, required checks, no force-pushes, and no
   deletion. Restrict creation/update of `v*` release tags to maintainers or a
   release bot. Do not allow an unreviewed workflow from a pull request to sign.
5. Create a `release-signing` environment. Require at least two named
   maintainers as reviewers and allow deployment only from `main` and release
   tags. Do not add secrets; this design intentionally uses none.
6. Commit the reviewed `SBOM.json`. Ensure the build is reproducible or record
   the build inputs. Publish a GitHub Release from a protected `v*` tag.
7. Run `release-signing.yml` from the published release. For a rehearsal,
   manually dispatch it from protected `main`; its certificate identity then
   contains `refs/heads/main`, not a release tag.

The runner needs network access to GitHub OIDC, Fulcio, Rekor, PyPI (for the
pinned clients/build dependency), and GitHub attestations. Public Sigstore and
GitHub Actions use is free; availability and quota are external dependencies.
GitHub's artifact-attestation service has separate repository/plan rules:
GitHub documents public repositories using the public Sigstore instance and
private repositories using GitHub's Sigstore instance (without a public
transparency log). Confirm the current plan/visibility before relying on that
step. For a strict requirement of both a public Rekor record and a GitHub
attestation at $0 cash, use a public repository on a supported free plan (or
confirm an eligible private-repository plan); otherwise keep the Sigstore
Fulcio/Rekor step and treat the GitHub attestation as unavailable. The
Sigstore Python keyless path remains the Fulcio/Rekor trust path.

## Expected online outputs

The run must produce all of the following:

* `*.sigstore.json` beside each wheel, sdist, SBOM, and manifest;
* successful `sigstore-python` identity verification in the workflow log;
* an immutable Rekor entry/inclusion proof referenced by each bundle;
* a GitHub artifact attestation from `actions/attest`;
* the uploaded workflow artifact named
  `zoracleflux-release-signing-<commit-sha>`.

Never create an empty bundle or copy a bundle from another artifact.

## Consumer verification commands

Download the release artifact and install the same client family:

```powershell
python -m pip install --disable-pip-version-check sigstore==4.5.0
python scripts\verify_sigstore.py `
  --repository ORG/REPO `
  --ref refs/tags/v1.0.0rc3 `
  --sha <release-commit-sha> `
  --manifest ARTIFACT_MANIFEST.sha256 `
  --artifact dist\zoracleflux-1.0.0rc2-py3-none-any.whl `
  --artifact dist\zoracleflux-1.0.0rc2.tar.gz `
  --artifact SBOM.json `
  --artifact ARTIFACT_MANIFEST.sha256
```

The script derives the exact identity
`https://github.com/ORG/REPO/.github/workflows/release-signing.yml@refs/tags/v1.0.0rc3`.
For a rehearsal, use `--ref refs/heads/main`. A missing bundle, wrong issuer,
wrong repository, wrong workflow, wrong ref, wrong SHA, or failed Rekor
verification returns non-zero.

Cosign is an independent consumer option for each blob:

```powershell
cosign verify-blob dist\zoracleflux-1.0.0rc2-py3-none-any.whl `
  --bundle dist\zoracleflux-1.0.0rc2-py3-none-any.whl.sigstore.json `
  --certificate-identity "https://github.com/ORG/REPO/.github/workflows/release-signing.yml@refs/tags/v1.0.0rc3" `
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

Repeat for the other three files. Use a current cosign release and its
`--new-bundle-format` defaults appropriate to the bundle. Do not use a broad
identity regular expression.

If GitHub CLI artifact attestations are enabled for the repository:

```powershell
gh attestation verify .\dist\zoracleflux-1.0.0rc2-py3-none-any.whl `
  --repo ORG/REPO `
  --signer-workflow ORG/REPO/.github/workflows/release-signing.yml `
  --source-ref refs/tags/v1.0.0rc3 `
  --source-digest <release-commit-sha>
```

For the CycloneDX SBOM attestation, add
`--predicate-type https://cyclonedx.org/bom` (and use the package subject, not
the SBOM file, as the first argument).

Check `gh attestation verify --help` for CLI-version-specific flag spelling.
The attestation is an additional GitHub provenance control; it is not a
replacement for the Sigstore bundle or Rekor check.

## Offline fallback

If CI is unavailable, verify the preserved RC3 detached signatures without
network access:

```powershell
py -3.10 scripts\local_fallback_verify.py `
  --candidate C:\Users\ziada\.copilot\chats\70b7f34f-e807-4a08-ae86-c1745773252f\artifacts\zoracleflux\final-release-candidate-rc3
```

This proves only the RC3 OpenSSH public-key trust anchor. It is not an
organization identity, Fulcio certificate, or Rekor-backed claim.

## Optional PyPI Trusted Publishing path

Only do this if the package is intended for a real PyPI project:

1. Create or select the PyPI project and configure a GitHub Actions Trusted
   Publisher for the real `ORG/REPO`, workflow
   `.github/workflows/pypi-trusted-publishing.yml`, and environment
   `pypi-release`. This is a PyPI-side configuration, not a repository secret.
2. Protect that environment and restrict the workflow to reviewed release
   refs. Run the optional workflow after review. The official PyPA action
   uses `id-token: write`, uploads wheel/sdist, and generates PyPI digital
   attestations for trusted-publishing flows.
3. Verify a downloaded PyPI distribution with the official
   `pypi-attestations` CLI, for example:

```powershell
python -m pip install pypi-attestations
pypi-attestations verify pypi `
  --repository https://github.com/ORG/REPO `
  https://files.pythonhosted.org/path/to/your.whl
```

This path does not sign or attest the SBOM or release manifest. It is
complementary to the four-file Sigstore workflow, and no PyPI identity or
upload was available locally.

## What cannot be completed locally

Without a real repository in a verified organization, protected environment,
reviewed workflow commit, GitHub Actions run, and network access, it is
impossible to obtain a GitHub OIDC token or honestly produce a Fulcio
certificate, Rekor entry, Sigstore bundle, or GitHub attestation. Local tests
can only validate script behavior, file hashes, and the existing RC3 fallback
signatures.
