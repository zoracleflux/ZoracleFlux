# GitHub operations deployment checklist

## Repository and governance

- [ ] Create/identify a public repository; record owner, URL, default branch,
      repository ID, and a second maintainer.
- [ ] Copy this overlay without editing `final-release-candidate-rc3`.
- [ ] Enable Issues, Projects, Discussions (if desired), dependency graph,
      Dependabot alerts/security updates, CodeQL, and OpenSSF Scorecard.
- [ ] Add `CODEOWNERS` for workflows and security policy; require two-person
      review for workflow, release, and security changes.
- [ ] Protect `main`; require CI and CodeQL checks, review, linear history (if
      compatible), and no force pushes/deletions.
- [ ] Create a Project with fields `Status`, `Priority`, `Severity`, `Owner`,
      `Target date`; link incident issues to it.

## Releases and Pages

- [ ] Configure Pages source **GitHub Actions** and verify the generated site
      URL. Confirm it contains no secrets or user data.
- [ ] Create `github-pages` environment; for public repositories add a
      required reviewer and restrict deployment branches.
- [ ] Decide release tag format (`vMAJOR.MINOR.PATCH`); protect release tags.
- [ ] Require CI, tests, package build, hash verification, and human approval
      before publishing.
- [ ] Verify a release asset download and SHA-256 from a clean machine.

## Security and identity

- [ ] Review every `uses:` reference and pin to a full commit SHA; update via
      Dependabot.
- [ ] Keep workflow-level permissions `contents: read`; grant write only to the
      publishing job.
- [ ] Never use `pull_request_target` to check out untrusted code.
- [ ] If cloud storage is needed, create an OIDC trust policy restricted to
      `repository`, workflow filename, ref, and environment; use no static
      cloud key.
- [ ] Configure `production` environment protection and secrets only after an
      external service exists. Record rotation owner and interval.

## Backup and uptime

- [ ] Run `backup-export.yml` manually; download and verify the artifact,
      manifest, and Git bundle.
- [ ] Treat the GitHub artifact as a short-retention staging copy. Configure
      off-site encrypted object storage and test restore at least quarterly.
- [ ] Set repository variable `HEALTHCHECK_URL` to a real HTTPS health endpoint.
- [ ] Confirm a deliberate failing probe creates a visible failure and that a
      human receives notification. Add external paging for production.
- [ ] Record the schedule caveat: GitHub schedules can be delayed and may be
      disabled after repository inactivity.
- [ ] If using a free external monitor, record its monitor count, interval,
      retention, notification channel, and whether a real human acknowledged
      an alert. Do not call a runbook or email notification “on-call”.

## Runtime and operations

- [ ] Choose external compute, ingress/TLS, identity, database, secret store,
      vulnerability process, and budget. GitHub Pages/Actions are not these.
- [ ] Run `LOCAL_SELF_HOSTED_PILOT.md` and archive literal output and hashes.
- [ ] Define SLO, support hours, severity matrix, on-call rota, escalation,
      customer communication, and post-incident review owner.
- [ ] Obtain legal/privacy/security review before accepting customer data.
- [ ] Repeat the release, restore, endpoint, and incident drills and attach
      evidence to Issues/Projects.

## Evidence still unavailable from this bundle

No real repository, GitHub settings, public endpoint, DNS/TLS, cloud account,
OIDC trust, off-site backup, alert delivery, on-call team, customer traffic,
legal approval, certification, or production spend is proven locally.
