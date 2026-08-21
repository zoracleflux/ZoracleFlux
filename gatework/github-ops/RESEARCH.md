# Official GitHub capability and limit review

Reviewed 2026-08-21. Links are official GitHub documentation; limits and plan
terms must be rechecked at deployment.

| Surface | What this bundle uses | Official capability / limit | Boundary |
|---|---|---|---|
| Pages | `pages.yml` | Static sites only; source and published site are recommended/max 1 GB, deployment timeout 10 minutes, soft 100 GB/month bandwidth and soft 10 builds/hour (custom Actions publishing is exempt from the build-rate limit). Pages is not for commercial transactions or SaaS. | Documentation and a browser-downloaded static site only. No Python process, API, database, auth, or background job. |
| Releases | `release.yml` | Releases are Git tags plus notes/assets; up to 1,000 assets/release, each file under 2 GiB, no total-size or bandwidth limit documented. | Release distribution, not package hosting with server execution. |
| Actions | `ci.yml`, `release.yml` | Standard GitHub-hosted runners are free for public repositories and self-hosted runners. Private repositories consume plan quotas and overage can bill. Actions has workflow/job/ concurrency limits. | Jobs are finite and ephemeral; scheduled execution is best effort, not a durable service or SLA. |
| Permissions | all workflows | `GITHUB_TOKEN` defaults should be read-only; grant only job-specific permissions. Third-party actions and untrusted checkout can compromise a job. | Review action source and pin actions to immutable SHAs before production. |
| Environments/secrets | Pages and release gates | GitHub Free can configure environments only for public repositories. Required reviewers (up to six) and environment secrets are supported. Anyone with repository write access can read repository secrets. | Environment protection is a deployment gate, not a managed/HSM secret store. Do not store customer data or structured secret blobs. |
| OIDC | documented optional boundary | Actions can exchange a short-lived JWT with AWS, Azure, GCP, Vault and other providers after an explicit trust policy; no long-lived cloud secret is needed. | OIDC does not create cloud resources or a secret store. Cloud account, role policy, audit and billing remain external. |
| Dependabot | `.github/dependabot.yml` | Version updates are configured per ecosystem and schedule; dependency graph/alerts and security updates use manifest/lock data. | Review and merge PRs; Dependabot is not a substitute for runtime patching or an SBOM attestation. |
| Code scanning | `security.yml` | Code scanning can run on push, PR, and schedule; CodeQL and SARIF tools are supported. It uses Actions minutes; private repositories require a Code Security license. | Public-repository scan results are useful evidence, not a complete penetration test or certification. |
| Scheduled health | `uptime-probe.yml` | `schedule` runs from the default branch. GitHub may delay runs during load; inactive public repositories can have scheduled workflows disabled after 60 days. | Probe is a synthetic check and a failed run; it is not continuous monitoring or paging. |
| Artifacts | CI/backup uploads | Artifacts are immutable in v4, support per-artifact `retention-days`, and cannot exceed the repository/org/enterprise retention setting. Upload returns a SHA-256 digest. | GitHub artifact retention is not an off-site backup or legal retention guarantee. Export to an external store for recovery. |
| Backup/export | `backup-export.yml`, script | Git can mirror branches/tags; REST/GraphQL APIs can export repository metadata. | GitHub does not provide a one-click disaster-recovery copy of all repository settings, secrets, environments, Actions logs, or Discussions. Secrets must never be exported. |
| Issues/Projects | templates and runbook | Issues track bugs/tasks; Projects provide table/board/roadmap views and automation; a Project supports up to 50 fields. | Configure labels, ownership and access in a real repository; this bundle cannot prove team response time. |
| Discussions | runbook guidance | Discussions support announcements, Q&A, decisions and polls, but an administrator must enable them. | Community conversation is not an incident paging channel. |

## Official references

* Pages limits: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>
* Releases and assets: <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>
* Actions billing: <https://docs.github.com/en/actions/concepts/billing-and-usage>
* Workflow syntax/permissions: <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
* Secure use and least privilege: <https://docs.github.com/en/actions/reference/security/secure-use>
* Environments: <https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments>
* Secrets: <https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets>
* OIDC: <https://docs.github.com/en/actions/concepts/security/openid-connect>
* Dependabot options: <https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference>
* Dependency graph/SBOM: <https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph>
* Code scanning: <https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning>
* Scheduled triggers: <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule>
* Artifacts: <https://docs.github.com/en/actions/tutorials/store-and-share-data>
* Repository mirroring: <https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository>
* Issues: <https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues>
* Projects: <https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects>
* Discussions: <https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions>

