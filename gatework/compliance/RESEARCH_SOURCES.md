# Requirements research (accessed 2026-08-21)

These are starting points, not a legal opinion. The scope and jurisdiction of
the real entity and customer contract control.

| Source | Relevant requirement or guidance | Operational implication |
|---|---|---|
| [EUR-Lex GDPR consolidated text](https://eur-lex.europa.eu/eli/reg/2016/679/oj), arts. 5, 13-14, 28, 30, 32-34 | Transparency, processor contract, records, risk-appropriate security, breach notification; a processor informs its controller without undue delay. | Complete data map, privacy notice, DPA schedule, records of processing, incident clock and deletion/return instructions with counsel. |
| [EDPB Guidelines 07/2020 on controller/processor](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-072020-concepts-controller-and-processor-gdpr_en) | Roles depend on actual purposes and means; labels alone do not decide controller/processor status. | Revisit role per feature/customer; do not publish a blanket DPA before review. |
| [NIST CSF 2.0](https://www.nist.gov/cyberframework) | Govern, Identify, Protect, Detect, Respond, Recover outcomes; framework is voluntary guidance. | Use outcomes for owners, risk register, evidence, exercises and improvement; do not call alignment certification. |
| [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final) | Incident handling preparation, detection/analysis, containment/eradication/recovery, and post-incident activity. | Maintain severity matrix, timeline, evidence preservation, communications and lessons learned. |
| [AICPA Trust Services Criteria](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022) | SOC 2 criteria cover security; availability, processing integrity, confidentiality and privacy are scoped as applicable. | Define system description, control owners and period evidence; independent CPA examination is required. |
| [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) | Certifiable ISMS requirements (clauses 4-10); independent accredited certification audit. | Establish ISMS scope, risk treatment, Statement of Applicability, internal audit and management review before certification body. |
| [CISA Vulnerability Disclosure Policy template](https://www.cisa.gov/resources-tools/resources/vulnerability-disclosure-policy-template) | A public intake, safe-harbor boundaries, authorization, disclosure and response process. | Publish only after a monitored mailbox, triage owner and safe-harbor language exist. |
| [FTC Privacy and Security](https://www.ftc.gov/business-guidance/privacy-security) | Privacy/security promises must be truthful and followed; collect only what is needed, protect it, dispose securely. | Retention statements require deletion evidence and exception handling; no unsupported security or uptime claims. |
| [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) | Standard semantics for HTTP response/status behavior. | Define health endpoint semantics and measurement point for any future real service. |

## Additional no-new-cash pathways

| Source | What was verified | Boundary |
|---|---|---|
| [USPTO Patent Pro Bono](https://www.uspto.gov/patents/basics/using-legal-services/pro-bono/patent-pro-bono-program) | Nationwide independently operated network; common requirements include financial need, patent-system knowledge and ability to describe the invention. | IP assistance only; regional intake/eligibility varies. |
| [USPTO Law School Clinic Certification](https://www.uspto.gov/learning-and-resources/ip-policy/public-information-about-practitioners/law-school-clinic-1) | Supervised student practice for patent/trademark matters; each clinic sets acceptance criteria. | Not privacy, commercial, SOC 2 or ISO review. |
| [Stanford Entrepreneurship Clinic](https://law.stanford.edu/mills-legal-clinic/entrepreneurship-clinic/) | Pro bono transactional clinic for eligible under-resourced startups/nonprofits. | Intake, conflicts and scope control access; student work is supervised but not an assurance report. |
| [Harvard Law Entrepreneurship Project](https://clinics.law.harvard.edu/hlep/apply/) | Supervised legal research for eligible Harvard/MIT-affiliated founders. | Research does not replace transactional counsel or entity approval. |
| [Pro Bono Net opportunities guide](https://www.probono.net/oppsguide/) and [LawHelp](https://www.lawhelp.org/) | Directories/referrals for local clinics and small-business help. | No guarantee of acceptance, jurisdiction, confidentiality or technology expertise. |
| [SBA SBDC resource partners](https://www.sba.gov/local-assistance/resource-partners/small-business-development-centers-sbdc) | Free/low-cost business counseling and referrals. | Counselors do not act as the startup's attorney. |
| [European Commission Decision 2021/915](https://eur-lex.europa.eu/eli/dec_impl/2021/915/oj/eng) and [2021/914](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj/eng) | Official EU controller-processor and international-transfer SCC texts. | Counsel must select scope, modules, roles, annexes, transfers and local law. |
| [CNIL GDPR toolkit](https://www.cnil.fr/en/my-compliance-tools/gdpr-toolkit) | Official PIA/templates and accountability guidance. | Tooling/guidance, not a DPA generator or approval. |
| [CSA STAR Level 1 CAIQ](https://cloudsecurityalliance.org/artifacts/star-level-1-security-questionnaire-caiq-v4-1/) | Free self-assessment questionnaire/registry route for eligible cloud providers. | Self-attestation, not certification or an audit opinion. |
| [OpenSSF Best Practices Badge](https://openssf.org/projects/best-practices-badge/) and [Scorecard Action](https://github.com/ossf/scorecard-action) | Free open-source practice checklist and automated repository checks. | Project signals only; not a legal, penetration-test, SOC 2 or ISO result. |
| [GitHub code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning) and [secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | Public-repository availability is documented; private-repository features depend on plan. | Detection evidence is bounded and cannot prove absence of vulnerabilities. |
| [NSF SBIR budget instructions](https://seedfund.nsf.gov/solicitation-budget/) and [SBIR eligible expenses](https://www.sbir.gov/tutorials/accounting-finance/tutorial-4) | Project-related professional/legal costs may require justification and program-officer/award approval; general corporate costs are not assumed allowable. | A proposal or credit is not cash; ask the program officer and accountant before budgeting counsel. |
| [AWS Activate](https://aws.amazon.com/startups/credits/), [Google Cloud Startups](https://startup.google.com/cloud/), [Microsoft for Startups](https://www.microsoft.com/en-us/startups), [Cloudflare Startups](https://www.cloudflare.com/startups/) | Conditional infrastructure/technical benefits with provider-specific eligibility and terms. | Credits are not legal-review or audit funding and do not create an SLA. |

## Conservative reading

* A template, policy, test, hash, or synthetic sample is evidence of a document
  or local control test only. It is not proof of legal compliance, certification,
  security, availability, or customer protection.
* An SLA is a negotiated contract. The provider, service boundary, monitoring
  source, maintenance/exclusions, remedies, support window, and signatures must
  exist before it is effective.
* Do not copy legal text from these sources into customer terms. Counsel should
  draft/adapt the contract and choose governing law, transfer mechanism, rights,
  sectoral obligations, and liability allocation.
