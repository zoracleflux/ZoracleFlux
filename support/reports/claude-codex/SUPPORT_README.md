# ZoracleFlux Claude Code and Codex support

This directory is an isolated support build copied from
`final-release-candidate`. The candidate itself is unchanged. The package
remains the direct CLI fallback; `claude-code\` and `codex\` are separate
client artifacts.

Run the no-client compatibility contract:

```powershell
Set-Location <this-directory>
py -3.10 harness\compatibility_contract.py
```

The harness invokes the local CLI and bundled stdio MCP processes directly. It
does **not** simulate Claude Code or Codex. Native client status is recorded as
`UNVERIFIED` when the executable is absent.

See `SUPPORT_REPORT.md` for official documentation findings, setup steps,
literal transcripts, versions, hashes, and cost accounting.
