# ZoracleFlux free release signing report

**Candidate:** `final-release-candidate`, version `1.0.0rc2`  
**Recorded:** 2026-08-21  
**Cash cost:** **$0.00**  
**Scope:** only `artifacts\zoracleflux\support\signing`; the candidate artifacts
were not rewritten.

## Decision

The executable path in this environment is a local, detached **OpenSSH
Ed25519** signature for each of:

* `dist\zoracleflux-1.0.0rc2-py3-none-any.whl`
* `dist\zoracleflux-1.0.0rc2.tar.gz`
* `SBOM.json`
* `ARTIFACT_MANIFEST.sha256`

This is genuine cryptographic signing, not a placeholder. `ssh-keygen` created
four signatures and `ssh-keygen -Y verify` accepted all four. The generated
private key was deliberately deleted immediately after signing; no production
private key is stored here. The public key, detached signatures, and
`allowed_signers` file are the local trust anchor.

This is **not** a production identity claim: the key is a newly generated
non-production key with no organization, maintainer, timestamp, or
transparency-log binding. A consumer must obtain and authenticate the public
key out of band.

## Verification result

`python verify_signatures.py --signatures-only` returned **0**. Its literal
stdout is preserved in `VERIFY_SIGNATURES_ONLY_OUTPUT.txt`; it reports `PASS`
for wheel, sdist, SBOM, and manifest and the fingerprint
`SHA256:TwyPworhpQ2AJG0hF8jr3PXF/FIY+Cnm9a7CwVtjKF4`.

The full check (`python verify_signatures.py`) returned **1** for a useful
pre-existing integrity finding: the candidate's existing manifest has three
stale entries (`.zoracleflux\audit.jsonl`, `.zoracleflux\pilot.sqlite3`, and
`evaluation\results.json`). All four detached signatures still pass. The
complete literal output is in `VERIFY_OUTPUT.txt`. This task did not alter
those candidate files or silently regenerate the manifest.

## Files produced

| File | Purpose |
|---|---|
| `zoracleflux-release-signing-key.pub` | Ed25519 public key |
| `allowed_signers` | OpenSSH verifier policy for principal `zoracleflux-release` |
| `signatures\wheel.sig` | wheel detached signature |
| `signatures\sdist.sig` | sdist detached signature |
| `signatures\sbom.sig` | SBOM detached signature |
| `signatures\manifest.sig` | manifest detached signature |
| `verify_signatures.py` | dependency-free, offline verifier |
| `SIGN_OUTPUT.txt` | literal signing-command stdout |
| `VERIFY_SIGNATURES_ONLY_OUTPUT.txt` | passing signature-check stdout |
| `VERIFY_OUTPUT.txt` | full signature plus manifest-digest stdout |
| `SIGNING_COMMANDS.txt` | exact commands, versions, and result notes |

The private key is absent by design. `zoracleflux-release-signing-key.pub`
has SHA-256 file hash
`972194C9DFCDDE7E6F5850BEA6A5204AFE53B4EBEBA911C86429A7BA6D157E2C`.

## Why Sigstore keyless was not executed here

Sigstore keyless is the preferred **production** upgrade when a real CI
identity is available:

1. A GitHub Actions job grants `id-token: write`.
2. The job obtains a GitHub OIDC token.
3. Fulcio issues a short-lived certificate binding an ephemeral key to the
   workflow identity.
4. Rekor records the signature/certificate in its public transparency log.
5. Consumers verify the bundle and constrain the certificate identity to the
   expected repository/workflow.

The public Fulcio/Rekor deployment is free public-good infrastructure; it does
not require a purchased signing key. However, this directory is not a running
GitHub Actions job, has no GitHub OIDC token, no repository workflow context,
and has no `cosign`/Sigstore CLI installed. Therefore no keyless signature or
`.sigstore` bundle was fabricated.

The future CI shape is:

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: sigstore/cosign-installer@v3
  - run: |
      for f in dist/*.whl dist/*.tar.gz SBOM.json ARTIFACT_MANIFEST.sha256; do
        cosign sign-blob --yes --bundle "$f.sigstore" "$f"
      done
```

Verification must pin the expected GitHub certificate identity and issuer,
for example `https://token.actions.githubusercontent.com`, rather than merely
accepting any Sigstore certificate. GitHub Actions availability/free quota,
repository policy, Fulcio/Rekor availability, and the workflow definition
remain part of that trust boundary. The relevant references are:

* [Sigstore signing overview](https://docs.sigstore.dev/cosign/signing/overview/)
* [Fulcio OIDC](https://docs.sigstore.dev/certificate_authority/oidc-in-fulcio/)
* [Sigstore public deployment](https://github.com/sigstore/architecture-docs/blob/main/sigstore-public-deployment-spec.md)
* [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect)
* [Rekor](https://github.com/sigstore/rekor)

## Alternatives evaluated

| Option | Local status | Assessment |
|---|---|---|
| GPG | Not installed | Free and widely understood, but requires long-lived private-key custody, distribution, revocation, and does not provide transparency by itself. |
| minisign | Not installed | Free/simple Ed25519 signatures, but requires obtaining a binary and has the same out-of-band identity limitation. |
| SSH `ssh-keygen -Y sign` | **Available and executed** | Best zero-install local fallback; standard Ed25519, detached signatures, offline verification. Trust is only the authenticated public key and policy file. |
| Sigstore keyless | Not executable here | Strongest CI identity/transparency option, but requires GitHub OIDC/CI context and network services; deliberately not simulated. |

## Custody, rotation, and revocation

For production, generate the release key offline or in a hardware-backed
secret manager; never put its private half in the repository or artifact
bundle. Publish the public-key fingerprint through an independently
authenticated project channel. Rotate on a fixed schedule and immediately on
suspected compromise. During rotation, publish both old/new fingerprints and
the cutover version; remove the old key from `allowed_signers` after the
transition. Retain a signed revocation/rotation record or OpenSSH KRL where
operationally appropriate. The local demonstration key cannot be rotated or
used again because its private half was destroyed.

## Offline/local fallback

With the candidate and this directory present, run:

```powershell
python verify_signatures.py --signatures-only
```

No network, paid account, package install, or private key is required. The
full check also detects the three stale manifest entries and intentionally
fails closed; resolve the candidate manifest in a separate release step
before calling the release fully integrity-verified.
