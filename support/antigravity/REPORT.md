# ZoracleFlux Antigravity support report

**Evidence date:** 2026-08-21. Official pages were fetched at
`2026-08-21T07:06:38.2049655Z`. **Cash spent:** `$0`. No credentials, paid
services, public deployment, or screenshots were used.

## Bottom line

The Antigravity platform is installed here and its MCP registration surface was
invoked without credentials or spend: **Antigravity IDE 1.107.0**, commit
`ecfbad74d93962fc8ca485d93ab9b4f3d4cb6cf8`, with the Google
`google.antigravity` extension at `0.2.0`. Its installed CLI wrapper accepts
`--add-mcp <json>` and successfully registered this server in an isolated
profile.

This directory also contains a real, offline MCP stdio server for the ZoracleFlux
`1.0.0rc2` release candidate. It exposes two tools:

* `zoracleflux_check` — runs the release candidate's deterministic checks.
* `zoracleflux_doctor` — reports its local/offline capability state.

The MCP protocol handshake, tool discovery, tool call, notification handling,
and an invalid-argument failure were tested directly. **Platform capability is
present. ZoracleFlux native host tool-call compatibility is unverified here:**
the installed IDE has no unauthenticated command-line `tools/call` surface, and
its isolated agent host could not obtain account state. This is a host
authentication/e2e limitation, not a claim that Antigravity lacks MCP.

## Official surfaces found

| Surface | Official evidence and exact current details |
|---|---|
| Antigravity 2.0 / IDE | [Getting started](https://antigravity.google/docs/getting-started) documents Projects and Local/New Worktree modes. |
| Antigravity CLI | [CLI overview](https://antigravity.google/docs/cli/overview) calls it the terminal TUI and documents shared settings with Antigravity 2.0. [Install](https://antigravity.google/docs/cli/install) documents `agy` installation scripts for Windows/macOS/Linux. No binary version was supplied by the docs. |
| MCP | [MCP guide](https://antigravity.google/docs/cli/mcp) documents local `stdio` and remote HTTP/SSE servers, `/mcp`, `mcpServers`, `command`, `args`, `env`, `cwd`, `serverUrl`, `disabled`, and `disabledTools`. It documents `~/.gemini/config/mcp_config.json` and workspace `.agents/mcp_config.json`. |
| MCP plugin | [Plugins and skills](https://antigravity.google/docs/cli/plugins) documents `~/.gemini/antigravity-cli/plugins/<plugin_name>/` with `plugin.json`, optional `mcp_config.json`, `hooks.json`, `skills/`, `agents/`, and `rules/`. It documents `agy plugin list`, `agy plugin install /path/to/local/plugin`, `agy plugin disable <name>`, `agy plugin enable <name>`, and `agy plugin uninstall <name>`. |
| Skill | The same page documents Markdown skills in workspace `.agents/skills/` or global `~/.gemini/antigravity-cli/skills/`, exposed as slash commands. |
| Google Workspace MCP config | [Configure Workspace MCP servers](https://developers.google.com/workspace/guides/configure-mcp-servers) and [Drive MCP](https://developers.google.com/workspace/drive/api/guides/configure-mcp-server) document `~/.gemini/antigravity/mcp_config.json`, an `mcpServers` object, remote `serverUrl`, and OAuth credentials. These require Google Cloud APIs and OAuth; they were not used. |
| MCP protocol | [MCP 2025-06-18 specification](https://modelcontextprotocol.io/specification/2025-06-18) defines JSON-RPC, capability negotiation, tools, and security consent. [stdio transport](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) requires newline-delimited UTF-8 JSON-RPC and forbids any non-protocol stdout. |

The installed IDE also supplies an actual local schema at
`resources\app\extensions\antigravity\schemas\mcp_config.schema.json`. It
accepts `mcpServers` entries with `command`, `args`, `env`, `cwd`,
`serverUrl`, `headers`, OAuth, `disabled`, `disabledTools`, and per-tool
`background`/`eager` settings. The installed CLI's `--add-mcp` surface writes a
separate profile file using a top-level `servers` object; both exact forms are
included here as `mcp_config.json` and `cli_mcp.json`.

The official pages are not perfectly consistent about the global path:
the Antigravity MCP page says `~/.gemini/config/mcp_config.json`, while the
Google Workspace pages say `~/.gemini/antigravity/mcp_config.json`. The latter
also matches an existing local Antigravity state directory observed here
(not modified and not copied). The fixture uses the documented
`mcpServers` shape and is intended to be imported/merged into whichever path
the installed client reports.

The plugin schema URL printed by the official plugin page,
`https://antigravity.google/schemas/v1/plugin.json`, returned HTTP 404 when
fetched. `plugin.json` was therefore checked against the inline schema in the
official page (required `name`, allowed characters, optional `description`),
not against a downloadable schema.

## Files in this directory

* `server.py` — dependency-free MCP stdio adapter. It invokes the release
  candidate through `PYTHONPATH`, keeps audit output under this support
  directory, never sends network requests, and never requires credentials.
* `mcp_config.json` — syntactically valid Antigravity `mcpServers` fixture.
  Its `cwd` is the exact current Windows support path; update that value when
  copying the directory elsewhere.
* `cli_mcp.json` — exact `User\mcp.json` shape produced by the installed
  `antigravity-ide.cmd --add-mcp` command.
* `runtime-mcp-schema.json` — copy of the installed IDE schema used for
  validation.
* `plugin.json` — documented Antigravity plugin manifest.
* `skills/zoracleflux-check.md` — documented workspace/global skill contract.
* `contract.json` — machine-readable protocol and safety contract.
* `test_protocol.py` — compatibility tests using only Python's standard
  library.
* `verification-output.txt` — literal outputs from the final verification
  run.
* `runtime-smoke.txt` — exact installed-runtime version, registration, status,
  and host limitation evidence.
* `STATUS.json` — first-class integrator status.
* `SHA256SUMS.txt` — SHA-256 hashes for the implementation and evidence files.

## How an Antigravity user can use this today

1. Copy this directory without changing the release candidate.
2. Update `cwd` in `mcp_config.json` to the copied directory.
3. Ensure Python `>=3.10` is on `PATH`.
4. In the IDE, merge the `zoracleflux` entry into the active
   `mcp_config.json` using **Manage MCP Servers > View raw config**. The
   installed schema is the source of truth for this client.
5. For the installed CLI wrapper, register without credentials in the current
   profile:

   ```powershell
   $exe = 'C:\Users\ziada\AppData\Local\Programs\Antigravity IDE\bin\antigravity-ide.cmd'
   $json = Get-Content .\cli_mcp.json -Raw
   & $exe --add-mcp $json
   ```

   On Windows PowerShell, if quoting strips JSON punctuation, invoke the same
   command through `cmd.exe` as demonstrated in `runtime-smoke.txt`. The CLI
   writes `User\mcp.json` with the `servers` shape.
6. Start the IDE/agent and use its MCP manager to refresh and inspect
   `zoracleflux`. A real agent tool call still requires the user's normal
   Antigravity account session; do not provide credentials to this adapter.
7. If the plugin surface is desired, use the documented
   `agy plugin install <path-to-this-directory>` after installing that separate
   CLI. The skill can instead be copied into `.agents\skills\`.

The no-host fallback is always available:

```powershell
Set-Location C:\Users\ziada\.copilot\chats\70b7f34f-e807-4a08-ae86-c1745773252f\artifacts\zoracleflux\support\antigravity
$env:PYTHONPATH = 'C:\Users\ziada\.copilot\chats\70b7f34f-e807-4a08-ae86-c1745773252f\artifacts\zoracleflux\final-release-candidate\src'
python -m zoracleflux.cli check --json
```

If the package script is installed, the shorter fallback is `zoracleflux check
--json` from this support directory. The observed result was:

```json
{"counts":{"failed":0,"passed":13,"total":13},"model_calls":0,"network":false,"status":"passed","summary":"13/13 declared relations passed","version":"1.0.0rc2"}
```

## Verification and literal failures

Final local verification:

```text
installed IDE: 1.107.0
installed CLI wrapper: antigravity-ide.cmd --version => 1.107.0
agy alias: NOT_FOUND
python: 3.10.1
py_compile: exit 0
JSON parse: valid (5 files)
schema-compatible config: passed
Ran 3 tests ... OK
MCP initialize: protocolVersion 2025-06-18
MCP tools: zoracleflux_check, zoracleflux_doctor
```

The complete literal output, including the exact JSON handshake and tool
schemas, is in `verification-output.txt`.
The installed-runtime registration/status output and the exact host
authentication failure are in `runtime-smoke.txt`.

SHA-256 (also recorded in `SHA256SUMS.txt`):

```text
cli_mcp.json 57578FB404DC71361CD66F6545C89C60C59EC81A47D11FE689F61E4F27D6C0FD
contract.json 9ADF7F6FB96A6737356C8577FB93DD03CD4E1D67D7BB051BA9AD2C5A418B4E1F
mcp_config.json AF5D79C337D2E0311A5ED8CE5206BC8947B262D24C1DD8AD8B80955FC2B0849E
plugin.json 28FC10BEE91D904EE3840C3E1191A5EAF07CF544A7DDD007E581061F9C8077E8
runtime-mcp-schema.json 2F1DD2DDE6B99FBAA6EB2442E8D441D57F2AD5DE88AB9BC56A462FB97A26A690
runtime-smoke.txt 8F1C997F759508A2B1C87EC6D850B234D063EADCACE07F81B56EA24A442E04C3
server.py E2166C0CED6CACA2D0BE08AAB5734C40AE88AF9E3B4647AEB46937B8365026E3
STATUS.json 159ECB7A04F51DF7B526B3E714203AFB521F085E7E892F2D8452987E98D1E898
test_protocol.py 706C371560A0536121C7030C86F580486DFF10404D5953BAF3074462DD512358
verification-output.txt FD17482DAA004EA9847FFB149E52AAD24B7CF6F7D8C35064441C55FB7D032FDA
skills/zoracleflux-check.md E1CD1E356A43E5E61A8C6874FD789B7694CE728A39BDB3567974BD42876CF1C9
cli_mcp.json TBD
runtime-mcp-schema.json TBD
runtime-smoke.txt TBD
STATUS.json TBD
```

Verified failure cases:

```text
timeout_ms=0
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"ValueError: timeout_ms must be an integer from 1 through 10000"}}

missing release source
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"FileNotFoundError: release source directory not found: C:\\does-not-exist\\src"}}
```

The adapter does not silently substitute an installed package when the
specified release source is absent.

## Support boundary

**Platform verified:** Antigravity IDE 1.107.0 launches, reports status, its
CLI wrapper accepts `--add-mcp`, writes the profile `servers` shape, and its
installed `mcp_config` schema validates the documented `mcpServers` fixture.

**ZoracleFlux verified:** local MCP stdio framing, protocol negotiation, tool
listing, bounded checks, deterministic offline behavior, and fail-closed
validation.

**ZoracleFlux native adapter status:** unverified here. The remaining step is a
real authenticated Antigravity agent session selecting `zoracleflux` and
executing `tools/call`; the isolated no-credential run reached the host but
could not obtain account state. This is the precise blocker. Remote Google MCP
services were intentionally not used.
