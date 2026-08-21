# ZoracleFlux Claude Code and Codex support report

**Build date:** 2026-08-21  
**Source:** `artifacts\zoracleflux\final-release-candidate` (copied; source
candidate was not modified)  
**Cash spend:** `$0.00` (see `SUPPORT_COST_LEDGER.csv`)  
**Native runtime status:** `UNVERIFIED` for both clients; neither executable
was installed on this machine. No client execution or credential simulation was
performed.

## Official current documentation consulted

Fetched on 2026-08-21:

- Claude Code plugins: <https://code.claude.com/docs/en/plugins>
- Claude Code plugin reference: <https://code.claude.com/docs/en/plugins-reference>
- Claude Code skills: <https://code.claude.com/docs/en/skills>
- Claude Code MCP: <https://code.claude.com/docs/en/mcp>
- OpenAI/Codex CLI: <https://developers.openai.com/codex/cli>
- OpenAI/Codex plugin packaging: <https://developers.openai.com/plugins/build/plugins>
- OpenAI/Codex skills: <https://developers.openai.com/codex/skills>
  (currently redirects to `learn.chatgpt.com/docs/build-skills`)
- OpenAI/Codex MCP: <https://developers.openai.com/codex/mcp>
  (currently redirects to `learn.chatgpt.com/docs/extend/mcp?surface=cli`)

The docs confirm the surfaces used here:

- Claude Code plugins use `.claude-plugin/plugin.json`, root-level
  `skills/<name>/SKILL.md`, and optional root `.mcp.json`. Plugin skills are
  namespaced as `/plugin-name:skill-name`; stdio MCP servers are supported.
- Codex plugins use `.codex-plugin/plugin.json`, `skills/`, and optional
  `.mcp.json` referenced by `mcpServers`. Codex also supports repository
  `.agents/skills`, project `.codex/config.toml`, and stdio MCP servers.
- The direct `zoracleflux` executable remains the only product CLI surface. No
  undocumented Claude or Codex command was invented.

## Built artifacts and truth status

| Client | Skill | MCP | Plugin/package | Direct CLI fallback | Native client |
|---|---|---|---|---|---|
| Claude Code | `claude-code\skills\zoracleflux\SKILL.md` | `claude-code\.mcp.json` + dependency-free stdio server | `claude-code\.claude-plugin\plugin.json` | Supported and tested | **UNVERIFIED** |
| Codex | `codex\skills\zoracleflux\SKILL.md`; repo copy under `codex\repo-surface\.agents\skills` | `codex\.mcp.json` + stdio server; project template under `codex\repo-surface\.codex` | `codex\.codex-plugin\plugin.json`; local marketplace copy under `codex\marketplace` | Supported and tested | **UNVERIFIED** |

The MCP server exposes one tool, `zoracleflux_check`, with no arguments. It
calls `python -m zoracleflux.cli check --json` locally, returns the literal
JSON, and rejects unknown tools or arguments. It does not accept source paths,
credentials, model input, or network destinations.

## Exact observed versions and commands

| Tool | Exact command | Literal output |
|---|---|---|
| Python | `C:\Users\ziada\AppData\Local\Programs\Python\Python310\python.exe --version` | `Python 3.10.1` |
| Node | `node --version` | `v22.12.0` |
| npm | `npm.cmd --version` | `10.9.0` |
| ZoracleFlux artifact | `C:\Users\ziada\AppData\Local\Programs\Python\Python310\python.exe -m zoracleflux.cli --version` | `1.0.0rc2` |
| Claude Code | `claude --version` | `executable not found on PATH` — **UNAVAILABLE** |
| Codex | `codex --version` | `executable not found on PATH` — **UNAVAILABLE** |

The complete machine-readable command records are in
`harness\compatibility-contract.json`; the literal installed-CLI fallback
transcript is in `harness\direct-cli-fallback.txt`.

## Tests and literal results

Command:

```powershell
py -3.10 harness\compatibility_contract.py
```

Literal result:

```json
{
  "status": "passed",
  "output": "harness\\compatibility-contract.json",
  "native_clients": "UNVERIFIED"
}
```

The contract executed:

1. Direct local CLI check: exit `0`, `13/13 declared relations passed`,
   `network: false`, `model_calls: 0`.
2. Direct invalid bounded path: exit `2`, exact error
   `ValueError: path must remain inside working directory`.
3. Claude stdio MCP server: initialize, `tools/list`, successful
   `tools/call`, unknown-tool failure (`isError: true`), and unknown-method
   failure (`-32601`).
4. Codex stdio MCP server: the same five protocol assertions.
5. Static manifest, skill, MCP, and local-marketplace discovery checks.

The JSON file preserves the exact request and response transcripts, including
literal CLI JSON emitted inside each MCP response. Timing fields are expected
to vary; status, counts, safety fields, and failure behavior are asserted.

The copied release's existing test suite was also run from this directory:

```powershell
py -3.10 -m pytest
```

Result: `22 passed in 2.69s` (the command is the only test-runner dependency already
declared by the candidate).

## User setup

### Common local install

From this directory, with Python 3.10–3.12:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements.lock
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\Activate.ps1
zoracleflux doctor --json
zoracleflux check --json
```

The fallback command is fully usable without either native client.

### Claude Code

With Claude Code installed and authenticated by the user:

```powershell
claude --plugin-dir .\claude-code
```

Invoke `/zoracleflux-claude-code:zoracleflux`. Inspect `/mcp` to see the
bundled stdio server. Alternatively copy the plugin directory to a Claude
plugin marketplace or use the documented `--plugin-dir` development flow.
Claude's `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PROJECT_DIR}` expansions are
used only where the official MCP/plugin docs document them.

### Codex

For the repo-scoped skill, copy
`codex\repo-surface\.agents\skills\zoracleflux` to the target repository's
`.agents\skills\zoracleflux`. For project-scoped MCP, copy
`codex\repo-surface\.codex\config.toml` to the target repository's
`.codex\config.toml`, replace both absolute placeholders, then run:

```powershell
codex mcp list
```

For the packaged plugin, add the included local marketplace directory with
the documented command:

```powershell
codex plugin marketplace add <absolute-path-to-this-directory>\codex\marketplace
codex plugin marketplace list
```

The current official packaging guide directs local plugin installation/testing
through the ChatGPT desktop Plugins Directory; the installed Codex host then
shares the same MCP configuration. Because Codex was unavailable here, do not
read the discovery listing as a native invocation result. The direct CLI and
the project-scoped MCP template are the deterministic fallback.

## Unsupported or deliberately unclaimed

- No claim that Claude Code or Codex native UI/TUI invocation works on this
  machine: both are **UNVERIFIED**.
- No API endpoint, API key, OAuth login, model provider, cloud execution,
  hosted MCP, plugin marketplace publication, or paid integration is included.
- No Claude/Codex-specific source execution is added. `check --source` remains
  parse-only and never imports or executes external code.
- Claude and Codex plugin installs are not represented by a fake command output.
  Re-run the contract after installing a real client, then record the actual
  client version and its literal install/discovery/invocation output.

## Hashes

`ARTIFACT_HASHES.sha256` records SHA-256 for every immutable support artifact
except generated `harness\compatibility-contract.json`, this report, and the
hash file itself. This exclusion avoids self-reference and makes the manifest
reproducible. The copied release files are hashed too.
