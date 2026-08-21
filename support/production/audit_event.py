"""Append a deliberately small, redacted, structured local audit event."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SECRET = re.compile(r"(?i)(token|secret|password|api[_-]?key|authorization|credential)")
ALLOWED = {"event", "status", "duration_ms", "schema_version", "version", "safety"}
SAFE_TEXT = re.compile(r"^[A-Za-z0-9_.:-]{1,64}$")


def append(path: Path, event: dict[str, object]) -> None:
    safe = {key: value for key, value in event.items() if key in ALLOWED and not SECRET.search(key)}
    for key, value in list(safe.items()):
        if isinstance(value, str) and (not SAFE_TEXT.fullmatch(value) or SECRET.search(value)):
            safe[key] = "[REDACTED]"
    safe.setdefault("schema_version", 1)
    safe["timestamp"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(safe, sort_keys=True, separators=(",", ":")) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path(".zoracleflux/audit.jsonl"))
    parser.add_argument("--event", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--duration-ms", type=float, default=0)
    args = parser.parse_args()
    append(args.path, {"event": args.event, "status": args.status, "duration_ms": args.duration_ms})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
