# Threat model and recovery

## Assets and trust anchors

Assets are the wheel, sdist, SBOM, release manifest, their digests, Sigstore
bundles, Rekor inclusion evidence, and GitHub attestation. The keyless trust
anchors are Sigstore's TUF-distributed roots, Fulcio, Rekor, GitHub's OIDC
issuer, and the consumer's exact repository/workflow/ref policy. The local
fallback anchor is the copied RC3 OpenSSH public key and `allowed_signers`.

## Threats and controls

| Threat | Control | Residual risk |
|---|---|---|
| Compromised maintainer account | GitHub 2FA, least privilege, protected branch, environment reviewers, tag restrictions | Account compromise can still approve a release |
| Malicious workflow or build change | CODEOWNERS/two-person review, immutable action SHAs, required checks, reviewed SBOM | A reviewer can approve a malicious change |
| Pull request or fork obtains signing identity | Only protected environment and release/tag path; no pull-request trigger; `id-token: write` scoped to signing job | GitHub policy misconfiguration |
| Replay or artifact substitution | Exact artifact digest in bundle and attestation; verify the exact repository/workflow/ref/SHA | Consumers must actually enforce the policy |
| Fulcio/issuer outage | Retry or use the documented local fallback; do not bypass identity checks | Release may be delayed |
| Rekor log outage or omission | Sigstore action verification is required; reject bundles without transparency evidence | Public service availability |
| Stolen workflow token | Short-lived OIDC token, no long-lived signing key, protected environment, no secrets | A running job can sign during its short lifetime |
| Local fallback key compromise | Keep private key offline, rotate public key/trust policy, revoke old principal | Old signatures remain mathematically valid |
| Malicious dependency/build tool | Lock dependencies, review build output/SBOM, isolate runner, attest provenance | Build compromise before signing |

## Key rotation, revocation, and recovery

Keyless signing has no long-lived release private key to rotate. Every run
creates an ephemeral key and short-lived Fulcio certificate. Rotate the policy
instead: pin a new reviewed workflow commit, update the exact allowed workflow
path/ref, and require fresh environment approvals. Rekor entries are
append-only; a bad release is not erased. Mark the version withdrawn and make
consumers reject its digest or commit.

If the GitHub trust boundary is suspected:

1. Disable the signing workflow and remove `id-token: write`.
2. Disable the `release-signing` environment and revoke/review its approvers.
3. Protect or delete compromised tags/releases; rotate maintainer credentials
   and review Actions audit logs and Rekor entries.
4. Merge a reviewed workflow/build fix, then run a clean release from a new
   commit and tag. Publish the rejected digest and reason.
5. Update consumer policy to the new commit/tag and verify a fresh bundle and
   attestation before republishing.

For the OpenSSH fallback, generate a new Ed25519 key offline, publish its
fingerprint through an independently authenticated channel, update
`allowed_signers`, and keep an old-key revocation/retirement record. If an
OpenSSH KRL is used, distribute it with the policy. Never commit the private
key. The copied RC3 private key was already deleted, so it cannot be rotated
or reused.
