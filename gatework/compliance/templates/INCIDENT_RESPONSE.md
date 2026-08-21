# Incident response plan — OPERATIONAL DRAFT / COUNSEL REQUIRED

No on-call or notification commitment exists until contacts, paging, service
boundary and contract are real and tested.

## Roles and severity

Incident commander/deputy: `[NAMES / 24x7 CONTACT]`; security lead:
`[CONTACT]`; legal/privacy: `[CONTACT]`; communications:
`[CONTACT]`; provider escalation: `[CONTACT]`.

| Severity | Example | Internal objective (not SLA) | Notify/update |
|---|---|---|---|
| P1 | Confirmed material confidentiality/integrity or broad outage | Triage `[15m]`, contain `[1h]` | Counsel decides legal/customer/regulator notice |
| P2 | Significant degraded service or limited exposure | Triage `[4h]` | Owner decides customer update |
| P3 | Minor defect/no material exposure | Triage `[2 business days]` | Ticket update |

## Procedure

1. Detect and record UTC time, reporter, affected version/asset, health output,
   hash, and smallest relevant log excerpt; never copy secrets or payloads.
2. Contain safely (disable endpoint/credential, isolate host, preserve a
   read-only copy) and record approvals.
3. Analyze scope, data subjects, integrity, availability, dependencies and
   evidence chain; maintain a timeline and decision log.
4. Eradicate/recover from verified artifacts and tested backup; validate
   controls and customer impact before reopening.
5. Counsel/owner decide notifications, privilege, regulator deadlines and
   wording. Record decision and rationale; do not promise a deadline not in law
   or a signed contract.
6. Close with root cause, corrective actions, owners/dates, and tabletop follow-up.

Exercise date/scenario/evidence: `[TABLETOP RECORD]`; plan approval:
`[OWNER / COUNSEL / DATE]`.
