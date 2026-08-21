# ZoracleFlux compliance and operational-readiness bundle

**Scope:** assessment and operator templates for `final-release-candidate-rc3`.
RC3 is preserved byte-for-byte; this directory is an overlay and contains no
hosted service, customer data, legal opinion, certification, monitoring
history, or effective SLA.

## Status vocabulary

* **Implemented/local:** demonstrable on this workstation only.
* **Designed:** a control or runbook exists, but operating evidence is absent.
* **Blocked:** requires a real entity, service, people, contract, or funded tool.
* **External approval:** only qualified counsel, an accredited certification
  body, or an independent auditor can issue the relevant opinion/certificate.

Every public-facing statement must remain a draft until its owner fills all
`[PLACEHOLDER]` values and obtains the review named in the matrix.

## Contents

| Path | Purpose |
|---|---|
| `RESEARCH_SOURCES.md` | Official/credible sources and conservative interpretation |
| `CONTROL_EVIDENCE_MATRIX.csv` | Requirement, control, evidence, owner, and gate |
| `EVIDENCE_CONTROL_MAP.csv` | GitHub, uptime, incident, SLA and privacy evidence crosswalk |
| `NO_CASH_PATHWAY_LEDGER.csv` | Eligibility, boundaries and proof for no-cash routes |
| `GITHUB_ISSUES_WORKFLOWS.md` | Issue labels, acceptance criteria, and workflow mapping |
| `AUDIT_CALENDAR.csv` | Recurring evidence and review schedule |
| `PATHWAYS_AND_FRAMEWORKS.md` | Pro bono, open, self-assessment, badge and credit routes |
| `EXTERNAL_HANDOFF_CHECKLIST.md` | Redacted packet and approval/certification/SLA gates |
| `FUNDED_APPROVAL_PATH.md` | Exact path from $0 self-assessment to external approval |
| `templates/` | Privacy, terms, DPA, security, IR, VDP, support, retention, SLA |
| `tools/synthetic_uptime.py` | Deterministic synthetic evidence generator/checker |
| `tools/check_bundle.py` | No-network schema/placeholder/control checks |
| `evidence/` | Literal local outputs, versions, and hashes |

## Run locally (PowerShell)

From the artifact root:

```powershell
py -3 .\gatework\compliance\tools\synthetic_uptime.py generate `
  --out .\gatework\compliance\evidence\synthetic-uptime.jsonl --samples 24
py -3 .\gatework\compliance\tools\synthetic_uptime.py check `
  --input .\gatework\compliance\evidence\synthetic-uptime.jsonl `
  --target 0.999
py -3 .\gatework\compliance\tools\check_bundle.py
```

The generator labels its output `synthetic=true`; the checker refuses to
describe it as production uptime. A synthetic pass is a tool test, not an
availability claim. See `evidence/LOCAL_CHECKS.md` for the captured run.

## Boundary

This bundle is operational documentation, not legal advice. GDPR/UK GDPR,
state privacy, breach, employment, export, accessibility, sectoral, and
consumer-law applicability must be determined by counsel for the actual entity,
jurisdictions, data, and customers. SOC 2 is an attestation by an independent
CPA firm; ISO/IEC 27001 certification is issued by an accredited certification
body. Neither is created by this self-assessment.
