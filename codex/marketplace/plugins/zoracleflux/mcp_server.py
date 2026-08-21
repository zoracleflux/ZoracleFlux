"""Dependency-free stdio MCP server for ZoracleFlux.

This copy is packaged for the Codex plugin surface. It intentionally exposes
only the deterministic local check and never accepts source or credentials.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


PROTOCOL_VERSION = "2024-11-05"
TOOL_NAME = "zoracleflux_check"


def _reply(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _tool(text: str, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def _check() -> tuple[int, str]:
    cwd = os.environ.get("ZORACLEFLUX_CWD") or os.getcwd()
    result = subprocess.run(
        [sys.executable, "-m", "zoracleflux.cli", "check", "--json"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    return result.returncode, (result.stdout.strip() or result.stderr.strip())


def _handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        requested = (message.get("params") or {}).get("protocolVersion")
        version = requested if requested in {PROTOCOL_VERSION, "2025-03-26", "2025-06-18"} else PROTOCOL_VERSION
        return _reply(
            request_id,
            {
                "protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "zoracleflux", "version": "1.0.0"},
                "instructions": "Use zoracleflux_check for bounded local checks. No network or model calls.",
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return _reply(request_id, {})
    if method == "tools/list":
        return _reply(
            request_id,
            {
                "tools": [
                    {
                        "name": TOOL_NAME,
                        "description": "Run the trusted built-in ZoracleFlux relations and return JSON evidence.",
                        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                    }
                ]
            },
        )
    if method == "tools/call":
        params = message.get("params") or {}
        if params.get("name") != TOOL_NAME:
            return _reply(request_id, _tool("unknown tool", True))
        if (params.get("arguments") or {}):
            return _reply(request_id, _tool("arguments are not accepted", True))
        try:
            return_code, output = _check()
        except (OSError, subprocess.SubprocessError) as exc:
            return _reply(request_id, _tool(f"{type(exc).__name__}: {exc}", True))
        return _reply(request_id, _tool(output, return_code != 0))
    if method == "shutdown":
        return _reply(request_id, {})
    return _error(request_id, -32601, f"method not found: {method}")


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("JSON-RPC message must be an object")
            result = _handle(message)
        except (ValueError, json.JSONDecodeError) as exc:
            result = _error(None, -32700, f"parse error: {exc}")
        if result is not None:
            sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
