# ZoracleFlux GitHub operations runbook

## Severity and ownership

* **SEV-1:** suspected data exposure, compromised workflow, or total external
  outage. Any maintainer can declare it; stop releases, revoke/rotate exposed
  credentials, preserve logs, and page the external on-call.
* **SEV-2:** sustained endpoint failure or release regression with a workaround.
  Open an `incident` issue, assign an owner, update status every 30 minutes.
* **SEV-3:** isolated bug, dependency alert, or documentation issue. Track in
  Issues/Projects and schedule a normal fix.

GitHub Issues are the system of record for timeline and decisions. Discussions
are for public Q&A/announcements, not secrets or paging. Projects is the
triage board. Configure an external paging channel before claiming on-call.

## Release

1. Merge reviewed code to protected `main`; confirm required CI and CodeQL
   checks are green.
2. Create and push a protected `vX.Y.Z` tag.
3. Inspect the release workflow logs and generated `SHA256SUMS.txt`.
4. A maintainer creates/approves the GitHub Release; verify assets and notes.
5. Publish static docs through Pages; verify the URL and rollback by redeploying
   the previous commit if needed.
6. Announce only verified behavior. RC3 remains an integration/evidence bundle,
   not a new package payload.

## Incident response

1. Open the incident form; set severity, start time, impact, suspected scope,
   and incident commander.
2. For a workflow compromise: disable affected workflow, revoke GitHub tokens
   and external credentials, inspect run logs/artifacts, rotate secrets, and
   review recent commits/actions.
3. For an endpoint incident: check external provider, DNS/TLS, health endpoint,
   database/backup status, and the latest release. Do not use Pages as an API
   workaround.
4. Communicate factual updates in the issue and (if appropriate) a public
   Discussion. Never paste tokens, customer data, or private logs.
5. Restore from a verified external backup; the GitHub artifact is only a
   short-retention staging copy.
6. Close with root cause, timeline, corrective actions, owner and due dates.

## Backup and restore

Run `backup-export.yml` manually after changing repository settings and weekly.
Download the artifact and verify `manifest.json`, `repository.bundle`, and API
JSON exports. The export intentionally excludes secrets. Test a mirror clone
and issue/release metadata import in a disposable repository. For production,
send the bundle to encrypted off-site storage using OIDC and record retention,
immutability and restore evidence.

## Known GitHub limits

Scheduled workflows are best-effort and can be delayed; inactive repositories
can lose scheduled runs. Actions artifacts expire according to repository or
organization policy. GitHub-hosted jobs are not durable workers. Pages is static.
These surfaces provide operational evidence but do not provide an uptime SLA or
an on-call team.
