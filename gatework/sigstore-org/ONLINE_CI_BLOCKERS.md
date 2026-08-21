# Online and CI blockers

## Blocking facts in this environment

* This directory is not a GitHub Actions runner and has no GitHub OIDC
  ambient credential.
* There is no real `ORG/REPO`, protected `release-signing` environment,
  protected tag, reviewed workflow commit, or release run available here.
* There is no PyPI project or configured Trusted Publisher for ZoracleFlux, so
  the optional PyPI workflow was not executed and no PyPI attestation exists.
* `cosign` and the `sigstore` CLI/module were not installed locally.
* A live Fulcio certificate, Rekor inclusion proof, Sigstore bundle, and GitHub
  artifact attestation therefore cannot be produced honestly.
* The public Sigstore docs host intermittently failed DNS/TLS retrieval from
  this host. Official GitHub source pages and GitHub OIDC documentation were
  still inspected; the authoritative URLs are recorded in
  `ORG_TRUSTED_SIGNING.md`.
* GitHub artifact-attestation availability is plan/repository dependent:
  GitHub documents public-repository attestations on the public Sigstore
  instance and private-repository attestations on GitHub's Sigstore instance
  (which has no public transparency log). Confirm the current plan and
  repository visibility before treating the attestation step as available.
  A strict free path requiring both public Rekor and GitHub attestation
  therefore needs a public repository (or an eligible private-repository
  plan); the Fulcio/Rekor keyless signature itself is the primary free path.

## What needs a real run

Only a real, networked Actions job can obtain the OIDC JWT and submit it to
Fulcio/Rekor. Only the GitHub repository can create and retain its artifact
attestation. The exact identity and provenance are unknowable until the run
exists. A local simulation cannot substitute for these facts.

## Non-blocking local checks completed

The deterministic manifest generator compiles and produced hashes for the
three payload inputs without touching RC3. The copied RC3 OpenSSH trust
material verified all four existing detached signatures. The Sigstore verifier
rejected an existing artifact because its sidecar bundle was absent.
