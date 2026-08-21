# Incident response runbook (template)

This is an operator draft, not an on-call service. There is no public endpoint,
customer data set, paging integration, or contractual response commitment.

1. **Detect:** capture timestamp, command/image hash, host, health output, and
   the smallest relevant audit excerpt. Never paste secrets or source content.
2. **Contain:** stop the process/container, disconnect network access, preserve
   the release candidate and evidence read-only, and prevent further writes.
3. **Triage:** classify availability, integrity, confidentiality, dependency,
   or safety impact; identify affected versions and data subjects if any.
4. **Eradicate/recover:** rotate independently exposed credentials, rebuild from
   a verified hash, restore a verified backup, and rerun health/threat checks.
5. **Notify:** the accountable owner decides whether customers, regulators,
   vendors, or law enforcement must be notified after legal review.
6. **Learn:** record timeline, root cause, evidence, corrective action, owner,
   and due date. Do not claim closure without verification.

Gate B requires named incident commander and deputy, severity matrix, contact
tree, notification deadlines, forensic retention, tabletop evidence, and legal
approval.

