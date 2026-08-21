# Contributing and releasing

Run `pytest`, `zoracleflux check --json`, and
`python evaluation\run_evaluation.py` before a change. Keep relation templates
transparent, bounded, and independently testable. Do not add network clients or
credentials to the deterministic path. Update the decision and evidence logs.

Release steps: build a wheel and sdist, install them in a clean environment,
run the commands above, generate `ARTIFACT_MANIFEST.sha256`, and review
`RELEASE_READINESS.md`. A release is a zero-cash developer preview until Gate B
funding, security, privacy, support, and operational controls are approved.
