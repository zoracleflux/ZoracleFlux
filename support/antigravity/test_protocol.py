from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent


class McpProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.process = subprocess.Popen(
            [sys.executable, "-u", str(ROOT / "server.py")],
            cwd=ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def tearDown(self) -> None:
        assert self.process.stdin is not None
        self.process.stdin.close()
        self.process.wait(timeout=5)
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        self.process.stdout.close()
        self.process.stderr.close()

    def exchange(self, message: dict) -> dict:
        assert self.process.stdin is not None
        assert self.process.stdout is not None
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        self.assertTrue(line, "server closed stdout")
        return json.loads(line)

    def notify(self, message: dict) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def test_initialize_list_and_check(self) -> None:
        initialized = self.exchange(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "compatibility-test", "version": "1"},
                },
            }
        )
        self.assertEqual(initialized["result"]["protocolVersion"], "2025-06-18")
        self.notify({"jsonrpc": "2.0", "method": "notifications/initialized"})
        tools = self.exchange({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(
            [tool["name"] for tool in tools["result"]["tools"]],
            ["zoracleflux_check", "zoracleflux_doctor"],
        )
        checked = self.exchange(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "zoracleflux_check", "arguments": {}},
            }
        )
        self.assertFalse(checked["result"]["isError"])
        payload = checked["result"]["structuredContent"]
        self.assertEqual(payload["status"], "passed")
        self.assertFalse(payload["network"])
        self.assertEqual(payload["model_calls"], 0)

    def test_invalid_tool_arguments_are_rejected(self) -> None:
        self.exchange(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {}},
            }
        )
        result = self.exchange(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "zoracleflux_check", "arguments": {"timeout_ms": 0}},
            }
        )
        self.assertEqual(result["error"]["code"], -32602)


class RuntimeConfigTests(unittest.TestCase):
    def test_installed_schema_compatible_config_shapes(self) -> None:
        config = json.loads((ROOT / "mcp_config.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "runtime-mcp-schema.json").read_text(encoding="utf-8"))
        allowed = set(schema["properties"]["mcpServers"]["additionalProperties"]["properties"])
        self.assertIn("zoracleflux", config["mcpServers"])
        server = config["mcpServers"]["zoracleflux"]
        self.assertTrue(set(server).issubset(allowed))
        self.assertIsInstance(server["command"], str)
        self.assertIsInstance(server["args"], list)
        self.assertIsInstance(server["cwd"], str)
        cli_config = json.loads((ROOT / "cli_mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(set(cli_config), {"servers", "inputs"})
        self.assertIn("zoracleflux", cli_config["servers"])


if __name__ == "__main__":
    unittest.main()
