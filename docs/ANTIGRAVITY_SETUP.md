# Antigravity setup and status

**Platform verified:** Antigravity IDE 1.107.0, commit
`ecfbad74d93962fc8ca485d93ab9b4f3d4cb6cf8`, wrapper `antigravity-ide.cmd`.
The installed CLI accepted `--add-mcp` and registration smoke passed.

**ZoracleFlux adapter:** verified dependency-free MCP stdio framing, handshake,
tool discovery, bounded check/doctor calls, and fail-closed invalid arguments.
**Native authenticated Antigravity `tools/call`: UNVERIFIED HERE.** The isolated
host could not obtain account state and exposes no unauthenticated tools/call
command. This is an environment blocker, not an unsupported claim.

From this RC3 directory, copy or merge `support\antigravity\mcp_config.json` into
the active Antigravity MCP configuration, update its `cwd` to the copied
`support\antigravity` directory, and run the documented `--add-mcp` command in
`support\antigravity\REPORT.md`. Then use an authenticated Antigravity session
to select `zoracleflux` and call `zoracleflux_check`; record literal output and
client version before upgrading the status to native runtime verified.

Tested fallback (always available):

```powershell
.\.venv\Scripts\zoracleflux.exe check --json
```

Expected shape: `{"counts":{"failed":0,"passed":13,"total":13},..."network":false,"status":"passed"...}`.
