# Information security policy — OPERATIONAL DRAFT / OWNER REVIEW

This is an operating policy, not a security guarantee or certification.
Applicability, exceptions, and control design require an accountable owner.

## Scope and governance

System boundary/assets/data flows/regions: `[LINKED INVENTORY]`  
Risk owner and security contact: `[NAMES / CONTACTS]`  
Review cadence and exception expiry: `[CADENCE / REGISTER]`

## Minimum control statements

1. Access is unique, least-privilege, MFA where supported, reviewed monthly,
   and removed on role change/termination.
2. Secrets are never committed or pasted into tickets; use the approved secret
   store `[NAME]`, rotate on exposure and at `[INTERVAL]`, and test recovery.
3. Changes require peer review, tests, dependency/advisory review, release
   approval, rollback plan, and an immutable artifact hash.
4. Vulnerabilities receive severity, owner, due date, fix/mitigation and
   verification evidence. Targets are internal objectives, not an SLA.
5. Logs are minimized, access-controlled, time-synchronized, retained for
   `[PERIOD]`, forwarded tamper-evidently to `[DESTINATION]`, and reviewed.
6. Backups are encrypted off-host, access-controlled, retention-labeled, and
   restored at the tested RPO/RTO. RC3 local-only backup does not satisfy this.
7. Incidents follow `INCIDENT_RESPONSE.md`; legal/customer notifications are
   decided by qualified counsel and the accountable owner.
8. Suppliers, subprocessors, data transfers, and changes are approved before
   access; customer contract controls prevail where stricter.

## Evidence and approval

Evidence index: `[LINK]`; control owners: `[REGISTER]`; exceptions:
`[REGISTER]`; last review: `[DATE]`; next review: `[DATE]`.

Approver `[NAME/ROLE]` signs only for the stated scope and period. Do not use
“SOC 2”, “ISO 27001”, “secure”, or “highly available” as a marketing claim
without the corresponding independent evidence and counsel review.
