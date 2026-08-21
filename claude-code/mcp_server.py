"""Dependency-free stdio MCP server for ZoracleFlux.

The server exposes only the deterministic local check. It never accepts a
source path, credentials, network destination, or model input.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


PROTOCOL_VERSION = "2024-11-05"
TOOL_NAME = "zoracleflux_check"


def response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def tool_result(text: str, *, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def run_check() -> tuple[int, str]:
    cwd = os.environ.get("ZORACLEFLUX_CWD") or os.getcwd()
    completed = subprocess.run(
        [sys.executable, "-m", "zoracleflux.cli", "check", "--json"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    output = completed.stdout.strip() or completed.stderr.strip()
    return completed.returncode, output


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        requested = (message.get("params") or {}).get("protocolVersion")
        version = requested if requested in {PROTOCOL_VERSION, "2025-03-26", "2025-06-18"} else PROTOCOL_VERSION
        return response(
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
        return response(request_id, {})
    if method == "tools/list":
        return response(
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
            return response(request_id, tool_result("unknown tool", is_error=True))
        arguments = params.get("arguments") or {}
        if arguments:
            return response(request_id, tool_result("arguments are not accepted", is_error=True))
        try:
            return_code, output = run_check()
        except (OSError, subprocess.SubprocessError) as exc:
            return response(request_id, tool_result(f"{type(exc).__name__}: {exc}", is_error=True))
        return response(request_id, tool_result(output, is_error=return_code != 0))
    if method == "shutdown":
        return response(request_id, {})
    return error(request_id, -32601, f"method not found: {method}")


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("JSON-RPC message must be an object")
            result = handle(message)
        except (ValueError, json.JSONDecodeError) as exc:
            result = error(None, -32700, f"parse error: {exc}")
        if result is not None:
            sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
