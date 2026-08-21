"""Small, offline MCP stdio adapter for the ZoracleFlux release candidate."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")
SERVER_INFO = {"name": "zoracleflux-antigravity", "version": "1.0.0"}


def _error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        result["error"]["data"] = data
    return result


def _tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "zoracleflux_check",
            "description": "Run ZoracleFlux's bounded deterministic relation checks offline.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "timeout_ms": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10000,
                        "default": 250,
                    }
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "zoracleflux_doctor",
            "description": "Report ZoracleFlux local capability and safety defaults.",
            "inputSchema": {"type": "object", "additionalProperties": False},
        },
    ]


class Adapter:
    def __init__(self, release_root: Path, work_root: Path) -> None:
        self.release_root = release_root.resolve()
        self.work_root = work_root.resolve()
        self.initialized = False
        self.protocol_version = SUPPORTED_PROTOCOLS[0]

    def _run_cli(self, command: str, *extra: str) -> tuple[int, str, str]:
        source = self.release_root / "src"
        if not source.is_dir():
            raise FileNotFoundError(f"release source directory not found: {source}")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(source) + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            [sys.executable, "-m", "zoracleflux.cli", command, *extra, "--json"],
            cwd=self.work_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return completed.returncode, completed.stdout, completed.stderr

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "zoracleflux_check":
            timeout_ms = arguments.get("timeout_ms", 250)
            if (
                isinstance(timeout_ms, bool)
                or not isinstance(timeout_ms, int)
                or not 1 <= timeout_ms <= 10000
            ):
                raise ValueError("timeout_ms must be an integer from 1 through 10000")
            code, stdout, stderr = self._run_cli("check", "--timeout-ms", str(timeout_ms))
        elif name == "zoracleflux_doctor":
            if arguments:
                raise ValueError("zoracleflux_doctor accepts no arguments")
            code, stdout, stderr = self._run_cli("doctor")
        else:
            raise LookupError(f"unknown tool: {name}")
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"CLI did not return JSON: {exc}") from exc
        if stderr:
            payload["adapter_stderr"] = stderr[-2000:]
        payload["adapter_exit_code"] = code
        return payload

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        request_id = message.get("id")
        if "id" not in message:
            return None
        if method == "initialize":
            requested = message.get("params", {}).get("protocolVersion")
            self.protocol_version = (
                requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
            )
            self.initialized = True
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": self.protocol_version,
                    "capabilities": {"tools": {}},
                    "serverInfo": SERVER_INFO,
                    "instructions": "Offline ZoracleFlux checks; no network or model calls.",
                },
            }
        if not self.initialized:
            return _error(request_id, -32002, "Server not initialized")
        if method == "ping":
            return {"jsonrpc": "2.0", "id": request_id, "result": {}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": _tool_definitions()}}
        if method == "tools/call":
            params = message.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            if not isinstance(name, str) or not isinstance(arguments, dict):
                return _error(request_id, -32602, "name and object arguments are required")
            try:
                payload = self._call_tool(name, arguments)
            except LookupError as exc:
                return _error(request_id, -32601, str(exc))
            except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
                return _error(request_id, -32602, f"{type(exc).__name__}: {exc}")
            failed = payload.get("status") in {"error", "failed"} or payload.get("adapter_exit_code", 0) != 0
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(payload, sort_keys=True)}],
                    "isError": failed,
                    "structuredContent": payload,
                },
            }
        return _error(request_id, -32601, f"Method not found: {method}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-root", type=Path)
    args = parser.parse_args(argv)
    here = Path(__file__).resolve().parent
    release_root = args.release_root or here.parents[1]
    adapter = Adapter(release_root, here)
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("message must be a JSON object")
            response = adapter.handle(message)
        except (json.JSONDecodeError, ValueError) as exc:
            response = _error(None, -32700, f"Invalid request: {exc}")
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

