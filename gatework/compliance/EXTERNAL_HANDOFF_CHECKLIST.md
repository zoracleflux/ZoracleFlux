# External handoff packet and decision gates

The packet is designed so a volunteer, paid attorney, CPA, certification body,
or customer can validate scope without treating self-authored material as
approval.

## Handoff packet (redacted)

1. Entity, ownership, jurisdictions, intended customers and regulator profile.
2. RC3 hash/manifests and a separate hosted-service architecture/data-flow
   diagram (if one exists); list what is deliberately out of scope.
3. Data inventory/ROPA hypothesis, controller/processor decision questions,
   subprocessors, locations, transfer mechanism and retention/deletion map.
4. Current drafts: privacy notice, terms, DPA, security policy, IR, VDP, support,
   SLA; show version, owner, placeholders and requested legal decisions.
5. Control matrix, GitHub evidence index, risk register, exceptions, local
   check output and SHA-256 manifest.
6. Real monitoring design/export, incident/tabletop records, backup/restore,
   access reviews, vulnerability results and customer contract (when applicable).
7. Funding/eligibility evidence: clinic intake, grant/credit award, engagement
   letter, conflict check, scope, confidentiality and deliverables.

## Decision gates

| Gate | Decision-maker | Evidence required | Allowed statement after pass |
|---|---|---|---|
| G0 self-assessment | Owner + peer | This bundle and reproducible checks | “Draft/readiness work completed for stated scope” |
| G1 legal advice | Licensed attorney/clinic supervisor | Engagement/intake, written advice or marked drafts | “Counsel advised on [scope/date]” (not blanket approval) |
| G2 legal approval/publication | Authorized entity + counsel | Final jurisdiction-specific documents, sign-off/version | “Approved for publication by [entity/counsel]” only within scope |
| G3 assurance readiness | Management | Operated evidence period, system description, exceptions | “Prepared for independent assessment” |
| G4 SOC 2 | Independent CPA firm | Issued report and period/criteria | “SOC 2 [type/criteria] report issued by [firm]” |
| G5 ISO 27001 | Accredited certification body | Stage 1/2 results and certificate/scope | “ISO/IEC 27001:2022 certified by [body]” within certificate scope |
| G6 SLA | Provider + customer | Real service, monitoring, signed order/SLA | “Contractual SLA effective [date]” with exact terms |

No gate can be inferred from a green GitHub workflow, badge, local uptime
fixture, volunteer advice without engagement scope, or unawarded credit.
