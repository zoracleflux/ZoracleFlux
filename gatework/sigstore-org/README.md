# Sigstore organization-trusted signing gatework

This is a proposed, reusable GitHub Actions pathway for the preserved
ZoracleFlux RC3 payload. It is intentionally isolated from
`final-release-candidate-rc3`.

* **Recommended:** protected GitHub organization/repository/workflow +
  GitHub OIDC + Fulcio + Rekor + Sigstore Python.
* **Additional provenance:** GitHub `actions/attest` artifact attestations.
* **Fallback:** existing RC3 OpenSSH Ed25519 signatures, verified offline.
* **Optional Python registry path:** PyPI Trusted Publishing/attestations for
  wheel and sdist only.
* **Status here:** no GitHub Actions run, OIDC token, Fulcio certificate, Rekor
  entry, or `.sigstore` bundle exists. Nothing is fabricated.

Read `ORG_TRUSTED_SIGNING.md`, then `SETUP.md`. `THREAT_MODEL.md` defines
controls and recovery. `ZERO_COST_OPTIONS.md` compares public GitHub, private
GitHub, PyPI, OpenSSF/SLSA, and grant options. `LOCAL_TEST_OUTPUT.txt` records
the commands actually run in this environment. `RESEARCH_FINDINGS.md` records
the official-source findings and precise local/online boundary.
