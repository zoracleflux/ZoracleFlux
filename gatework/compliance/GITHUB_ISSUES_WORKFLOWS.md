# GitHub issue and workflow mapping

These are proposed controls; they do not operate until copied to the repository,
owners are assigned, and workflow permissions/secrets are reviewed.

## Labels and issue templates

Create labels `compliance`, `legal-review`, `privacy`, `security`, `availability`,
`evidence`, `blocked-funded`, and `external-assurance`. Each issue must include
owner, scope/jurisdiction, control ID, evidence path, due date, risk/exception,
and reviewer. Never put personal data, credentials, privileged legal advice, or
incident details in a public issue.

| Issue | Control IDs | Acceptance criteria | Blocking gate |
|---|---|---|---|
| Establish entity, jurisdictions, data map | L-01,L-02,L-03 | Counsel scope memo, inventory, role decision, approved notice/DPA | Legal review |
| Approve terms and customer boundaries | L-05,A-03 | Signed order form and schedules; no placeholders | Counsel + customer |
| Operate retention/deletion | L-04 | Primary/backup/subprocessor tests and ledger | Privacy counsel |
| Staff incident/support rota | S-02,A-02 | Named 24x7 contacts, page test, tabletop | Operations sponsor |
| Establish VDP and vulnerability process | S-03 | Monitored channel, safe harbor, triage evidence | Security review |
| Build real availability evidence | A-01 | Hosted endpoint, independent checks, monthly hash/report | Operations + contract |
| Prepare SOC 2/ISO engagement | C-01,C-02 | Scope, controls, period evidence, signed engagement | Funded assurance |

## Workflow mapping

| Workflow (sample path) | Trigger | Safe checks | Required protections |
|---|---|---|---|
| `compliance-structure.yml` | PR touching `gatework/compliance/**` | `py -3 tools/check_bundle.py`; CSV parse; placeholder scan | Read-only, no secrets, no network |
| `compliance-synthetic.yml` | Manual/PR | Generate/check synthetic JSONL; upload as artifact | Label artifact `synthetic`; never publish as uptime |
| `evidence-hash.yml` | Release tag | SHA-256 all evidence and templates | Protected environment and signed release approval |
| `security-advisory-triage.yml` | Security event | Create private ticket and notify owner | Least privilege; never echo payloads |

Workflow result is evidence of a check run only. A green check is not legal
approval, certification, production uptime, or an SLA.

## Evidence path convention

| GitHub location/type | Matrix/evidence IDs | Required handling |
|---|---|---|
| `docs/compliance/` PRs and protected reviews | L-02,L-03,L-05,S-01; `GH-PR` | Version drafts, record reviewers and scope; never merge a placeholder-free document as “approved” without the named gate |
| `evidence/uptime/YYYY-MM/` release artifact | A-01,A-03; `UP-RAW`,`SLA-MONTHLY` | Store raw monitor export, UTC window, endpoint/regions, formula, exclusions, SHA-256 and approver; synthetic JSONL goes in a separate non-production path |
| Private incident issue/project | S-02; `INC-TKT`,`INC-NOTICE` | Restrict access; avoid secrets/PII; preserve timeline, decisions, legal review and notification receipts |
| `evidence/tabletops/` | S-02; `INC-EX` | Record scenario, participants, injects, actions, owners and due dates; tabletop is not a real incident |
| `evidence/retention/` | L-04; `RET-LEDGER` | Pseudonymous request ID, systems, method, result and legal-hold exception; no personal data in public repository |
| `docs/contracts/` restricted repository | L-03,A-03; `DPA-SIGNED`,`SLA-DRAFT` | Store signed DPA/SLA only in access-controlled location; public repo may contain redacted placeholders and hashes |
| `evidence/ossf/` | `GH-SCORE`,`GH-SLSA` | Pin action versions, record commit/tool/provenance; badge/attestation is a bounded supply-chain signal |

The control crosswalk in `EVIDENCE_CONTROL_MAP.csv` is the source of truth for
minimum fields and non-claims. GitHub retention, visibility, runner,
permissions, artifact expiry and legal hold must be configured and tested before
these paths are treated as audit evidence.
