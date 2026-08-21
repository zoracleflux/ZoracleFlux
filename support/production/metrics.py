"""Render local audit JSONL as Prometheus text; no HTTP listener is provided."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def label(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")[:64]


def render(path: Path) -> str:
    counts: Counter[tuple[str, str]] = Counter()
    total = 0
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = str(event.get("event", "unknown")).replace("-", "_")
            status = str(event.get("status", "unknown")).replace("-", "_")
            counts[(name, status)] += 1
            total += 1
    lines = [
        "# HELP zoracleflux_audit_events_total Count of valid local audit events.",
        "# TYPE zoracleflux_audit_events_total counter",
        f"zoracleflux_audit_events_total {total}",
        "# HELP zoracleflux_events_by_status_total Count of local audit events by event and status.",
        "# TYPE zoracleflux_events_by_status_total counter",
    ]
    for (name, status), count in sorted(counts.items()):
        lines.append(f'zoracleflux_events_by_status_total{{event="{label(name)}",status="{label(status)}"}} {count}')
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, default=Path(".zoracleflux/audit.jsonl"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = render(args.audit)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
