# Support and on-call model — OPERATIONAL DRAFT / NOT AN SLA

RC3 has no hosted endpoint, paid support, paging integration, or staffed
on-call. This is a design to activate only after staffing and a signed contract.

Service/support boundary: `[SERVICES / REGIONS / HOURS / EXCLUSIONS]`  
Channels and ticket retention: `[URL / EMAIL / SYSTEM / RETENTION]`  
Primary/deputy/manager: `[NAMES / TIME ZONES / ESCALATION]`

| Priority | Customer impact | Acknowledge objective | Update objective | Restore/workaround objective |
|---|---|---|---|---|
| P1 | Broad outage or material security impact | `[TARGET]` | `[TARGET]` | `[TARGET]` |
| P2 | Major degradation | `[TARGET]` | `[TARGET]` | `[TARGET]` |
| P3 | Limited defect/question | `[TARGET]` | `[TARGET]` | `[TARGET]` |

These are not promises until copied into a signed SLA/order form. Test
escalation quarterly; retain ticket, page, acknowledgement, timeline,
communications, and post-incident review. Record holidays, maintenance,
customer prerequisites, and provider dependencies explicitly.
