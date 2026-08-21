# Security and privacy

The default path is local-only and makes zero network or model calls. Source
files passed to `--source` are parsed with `ast` and never imported, compiled,
or executed. Output and audit paths must remain below the current working
directory. Generated tests are review artifacts and are not auto-run by the
CLI. Audit records contain status, timing, and safety flags, not source content,
tokens, or environment variables.

Threat controls include fail-closed relation parsing, bounded deterministic
cases, explicit trusted built-in mutation callables, no shell invocation, no
credentials, and no automatic outbound messages. Do not run the package against
untrusted code expecting a security sandbox; use a disposable OS/container
boundary and resource limits for that use case.

If an incident is suspected: stop local runs, preserve `.zoracleflux\audit.jsonl`
and the exact artifact hash, remove generated output, revert to the prior
wheel, and rotate any credentials that were independently exposed. Gate B still
requires independent security review, managed secrets, isolation, retention,
backup/restore, monitoring, and incident ownership.
