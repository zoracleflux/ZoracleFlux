"""Deterministic compatibility contract harness.

This harness validates package shape and invokes the bundled stdio MCP servers
directly. It never pretends to be Claude Code or Codex and never supplies
credentials or network access.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PYTHONPATH = str(ROOT / "src")


def run(command: list[str], *, cwd: Path = ROOT, input_text: str | None = None) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH
    result = subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    return {
        "command": command,
        "cwd": str(cwd),
        "exit": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mcp_contract(server: Path) -> dict[str, Any]:
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "zoracleflux_check", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "not-a-tool", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 5, "method": "does/not-exist"},
    ]
    transcript = "\n".join(json.dumps(item, sort_keys=True) for item in requests) + "\n"
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH
    env["ZORACLEFLUX_CWD"] = str(ROOT)
    result = subprocess.run(
        [sys.executable, str(server)],
        cwd=ROOT,
        input=transcript,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    replies = [json.loads(line) for line in lines]
    by_id = {item["id"]: item for item in replies if "id" in item and item["id"] is not None}
    assert_true(result.returncode == 0, f"MCP process failed: {result.stderr}")
    assert_true(by_id[1]["result"]["serverInfo"]["name"] == "zoracleflux", "bad initialize")
    assert_true(by_id[2]["result"]["tools"][0]["name"] == "zoracleflux_check", "tool not discovered")
    check_text = by_id[3]["result"]["content"][0]["text"]
    check_payload = json.loads(check_text)
    assert_true(check_payload["status"] == "passed", "MCP check did not pass")
    assert_true(by_id[3]["result"]["isError"] is False, "successful MCP call marked as error")
    assert_true(by_id[4]["result"]["isError"] is True, "unknown tool did not fail closed")
    assert_true(by_id[5]["error"]["code"] == -32601, "unknown method did not fail closed")
    return {
        "server": str(server.relative_to(ROOT)),
        "exit": result.returncode,
        "request_transcript": transcript,
        "response_transcript": result.stdout,
        "stderr": result.stderr,
        "assertions": ["initialize", "tools/list", "tools/call", "unknown tool failure", "unknown method failure"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="harness/compatibility-contract.json")
    args = parser.parse_args()

    direct = run([sys.executable, "-m", "zoracleflux.cli", "check", "--json"])
    direct_payload = json.loads(direct["stdout"])
    assert_true(direct["exit"] == 0, "direct CLI check failed")
    assert_true(direct_payload["status"] == "passed", "direct CLI status was not passed")
    assert_true(direct_payload["network"] is False and direct_payload["model_calls"] == 0, "offline contract changed")

    failure = run([sys.executable, "-m", "zoracleflux.cli", "check", "--source", "..\\outside.py", "--json"])
    failure_payload = json.loads(failure["stdout"])
    assert_true(failure["exit"] == 2, "invalid bounded path did not fail")
    assert_true(failure_payload["status"] == "error", "invalid bounded path had no error status")

    claude_manifest = read_json(ROOT / "claude-code" / ".claude-plugin" / "plugin.json")
    claude_mcp = read_json(ROOT / "claude-code" / ".mcp.json")
    codex_manifest = read_json(ROOT / "codex" / ".codex-plugin" / "plugin.json")
    codex_mcp = read_json(ROOT / "codex" / ".mcp.json")
    for manifest in (claude_manifest, codex_manifest):
        assert_true(manifest["name"].startswith("zoracleflux-"), "invalid plugin name")
        assert_true(manifest["version"] == "1.0.0", "invalid adapter version")
    assert_true("zoracleflux" in claude_mcp["mcpServers"], "Claude MCP server missing")
    assert_true("zoracleflux" in codex_mcp["mcpServers"], "Codex MCP server missing")
    assert_true((ROOT / "claude-code" / "skills" / "zoracleflux" / "SKILL.md").is_file(), "Claude skill missing")
    assert_true((ROOT / "codex" / "skills" / "zoracleflux" / "SKILL.md").is_file(), "Codex skill missing")
    assert_true((ROOT / "codex" / "marketplace" / "plugins" / "zoracleflux" / ".codex-plugin" / "plugin.json").is_file(), "Codex marketplace copy missing")

    mcp_claude = mcp_contract(ROOT / "claude-code" / "mcp_server.py")
    mcp_codex = mcp_contract(ROOT / "codex" / "mcp_server.py")
    versions: dict[str, Any] = {}
    for name, command in (
        ("python", [sys.executable, "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm.cmd", "--version"]),
        ("zoracleflux", [sys.executable, "-m", "zoracleflux.cli", "--version"]),
    ):
        result = run(command)
        versions[name] = {"command": result["command"], "exit": result["exit"], "stdout": result["stdout"], "stderr": result["stderr"]}
    for name, command in (("claude", ["claude", "--version"]), ("codex", ["codex", "--version"])):
        executable = shutil.which(command[0])
        if executable:
            result = run(command)
            versions[name] = {"status": "installed", **result}
        else:
            versions[name] = {"status": "UNAVAILABLE", "command": command, "literal_output": "executable not found on PATH"}

    report = {
        "contract": "deterministic compatibility contract; native clients are never simulated",
        "native_runtime": {"claude_code": "UNVERIFIED", "codex": "UNVERIFIED"},
        "direct_cli": direct,
        "direct_cli_failure": failure,
        "mcp": {"claude_code": mcp_claude, "codex": mcp_codex},
        "versions": versions,
        "network": False,
        "model_calls": 0,
        "cash_spend_usd": "0.00",
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "passed", "output": str(output.relative_to(ROOT)), "native_clients": "UNVERIFIED"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
