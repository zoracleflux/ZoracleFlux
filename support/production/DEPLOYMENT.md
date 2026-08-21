# Self-hosted pilot deployment

## Supported zero-cash mode

Run from a disposable local checkout with the exact release artifact hash in
`ARTIFACT_MANIFEST.sha256`. Use an isolated virtual environment and the commands
in `README.md`. Keep the working directory private, set filesystem permissions
for the operator only, and use a local encrypted disk if available. The CLI
does not provide an HTTP service or tenant boundary.

## Compose mode

`compose.yaml` is a production-shaped *local pilot* only. It drops Linux
capabilities, uses a non-root UID, read-only root filesystem, no network, a
small `/tmp`, and a named local volume. It does not provide TLS, identity,
multi-tenancy, encrypted off-host storage, image signing, patch management, or
an uptime monitor. Building may require a cached `python:3.12-slim` image.

Before any real customer data is considered, stop and obtain Gate B approval,
complete isolation and retention design, and perform independent security
review. The safe release candidate's AST-only source boundary is not an OS
sandbox.

