# Backup and restore runbook

## Local pilot

1. Stop the pilot process and preserve the release manifest.
2. Run `backup.py backup` against `.zoracleflux\pilot.sqlite3`.
3. Confirm `MANIFEST.json` hash and `sqlite_integrity: true`.
4. Copy the backup only to an operator-controlled, encrypted location.
5. Test restore into a new path with `backup.py restore`; never overwrite the
   only copy.
6. Record date, operator, source hash, destination hash, and result.

## Incident or corruption

Stop writes, retain the original read-only, calculate hashes, and restore only
after an owner approves the target. If credentials were independently exposed,
revoke and rotate them in the approved secret system. This bundle has no
off-host replication, retention guarantee, or recovery-time objective.

## Gate B acceptance

Fund encrypted off-site storage, independent backup credentials, immutable
retention, restore automation, key recovery, RPO/RTO targets, and at least one
witnessed restore test. Record evidence before accepting customer data.

