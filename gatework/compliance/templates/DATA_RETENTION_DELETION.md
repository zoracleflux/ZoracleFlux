# Data retention and deletion schedule — DRAFT / PRIVACY COUNSEL REQUIRED

Retention is a product/legal decision, not a default inherited from the local
pilot. Do not promise deletion until backups, replicas, tickets, exports,
subprocessors and legal holds are covered.

| Data class | Purpose | System/location | Retention | Deletion trigger/method | Exception/owner |
|---|---|---|---|---|---|
| Account identifiers | `[PURPOSE]` | `[SYSTEM]` | `[DAYS/MONTHS]` | `[METHOD/VERIFICATION]` | `[LEGAL HOLD/OWNER]` |
| Inputs/outputs | `[PURPOSE]` | `[SYSTEM]` | `[PERIOD]` | `[METHOD/VERIFICATION]` | `[OWNER]` |
| Audit/security logs | Security/accountability | `[SYSTEM]` | `[PERIOD]` | `[ROTATION/ACCESS]` | `[LEGAL HOLD/OWNER]` |
| Backups/replicas | Recovery | `[SYSTEM]` | `[PERIOD]` | Expiry and key destruction `[METHOD]` | `[RPO/RTO OWNER]` |
| Support/billing records | Contract/accounting | `[SYSTEM]` | `[PERIOD]` | `[METHOD]` | `[LAW/OWNER]` |

## Procedure and evidence

1. Verify requester/authority and applicable controller instruction.
2. Search primary, indexes, exports, replicas and subprocessors; preserve legal
   hold; do not delete evidence needed for security or law.
3. Execute deletion/return, expire backups on schedule, and record timestamps,
   operator, systems, result and exception.
4. Verify by independent query/restore test without exposing data; report
   completion or reason for refusal to the authorized requester.

Approval: `[DATA OWNER]`, `[PRIVACY COUNSEL]`, effective `[DATE]`, version
`[VERSION]`. Current RC3 local pilot has bounded local evidence only and does not
establish a customer deletion service.
