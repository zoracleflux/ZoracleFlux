# Certification readiness checklist

This is a readiness backlog, not SOC 2, ISO 27001, or other certification.

| Area | Evidence required | Current status |
|---|---|---|
| Scope and system boundary | Approved architecture, assets, data flows, regions | Not started |
| Governance | Named control owners, risk register, review cadence | Not started |
| Identity/access | MFA, least privilege, joiner/mover/leaver, access reviews | Not available |
| Secrets/keys | SOPS/age or OpenBao design, rotation and recovery evidence | Not available |
| Secure SDLC | Code review, dependency/advisory process, release approvals | Partial/local only |
| Vulnerability management | Pinned scanners, triage SLAs, remediation evidence | Not available |
| Availability/resilience | Monitoring, backups, restore tests, RPO/RTO, DR exercise | Local backup only |
| Logging/IR | Central tamper-evident logs, alerting, tabletop, notifications | Local JSONL only |
| Privacy/vendor | DPA, subprocessors, retention/deletion, legal review | Not started |
| Independent assessment | Qualified auditor and report/attestation | Not funded |

