# Secret and configuration handling

## Pilot boundary

The release candidate is credential-free and offline-first. The pilot must run
with `provider: none`, no secret file, no environment token, and no outbound
network. `.env.example` is documentation, not a secret store. Never commit
`.env`, private keys, customer data, database backups, or incident evidence.

## Open-source path when Gate B is funded

Choose one owner-approved design and record its exact version and threat model:

1. **SOPS + age** for encrypted configuration in a controlled repository. Keep
   the age private key outside the repository with a separate recovery owner.
2. **OpenBao** (Apache-2.0 Vault-compatible server) for runtime retrieval,
   short-lived credentials, audit device, rotation, and operator access.
3. A managed KMS/HSM may replace the key custody layer, but it is not present
   in this bundle.

No tool is installed or configured here because there are no credentials,
operator identities, or funded secret-hosting controls. Secret values must be
redacted from audit events, metrics, support tickets, crash dumps, and backups.
Rotation, revocation, break-glass access, recovery testing, and access reviews
are Gate B acceptance criteria.

