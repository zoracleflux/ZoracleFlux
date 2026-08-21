# RC3 production-template crosswalk

The compliance overlay extends, rather than edits, the existing templates in
`final-release-candidate-rc3\support\production`.

| Existing RC3 template | Overlay artifact | Treatment |
|---|---|---|
| `PRIVACY_POLICY_TEMPLATE.md` | `templates/PRIVACY_NOTICE.md` | Adds role/data/transfer/rights approval fields |
| `TERMS_TEMPLATE.md` | `templates/TERMS_AND_CUSTOMER_BOUNDARIES.md` | Makes self-hosted and no-SLA boundary contractual |
| `SECURITY_POLICY_TEMPLATE.md` | `templates/SECURITY_POLICY.md` | Adds owners, evidence, exceptions and assurance boundary |
| `INCIDENT_RUNBOOK.md` | `templates/INCIDENT_RESPONSE.md` | Adds severity, notification decision and exercise record |
| `SLA_TEMPLATE.md` | `templates/SLA_TEMPLATE.md` | Adds measurement, raw evidence, signatures and no-claim guard |
| `CERTIFICATION_READINESS.md` | `templates/SOC2_ISO_READINESS.md` + matrix | Separates self-assessment from CPA/accredited certification |
| `MONITORING.md` | `tools/synthetic_uptime.py` + SLA template | Keeps local metrics synthetic and non-production |
| `BACKUP_RESTORE_RUNBOOK.md` | `templates/DATA_RETENTION_DELETION.md` | Adds deletion/backup/legal-hold evidence boundary |

The RC3 originals remain authoritative for the RC3 pilot. This overlay is a
planning and evidence layer; it does not silently change runtime behavior.
