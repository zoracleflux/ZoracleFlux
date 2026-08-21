#!/usr/bin/env python3
"""Generate and validate clearly synthetic uptime evidence (stdlib only)."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

SCHEMA = {"schema": "zoracleflux.synthetic-uptime.v1", "synthetic": True}


def iso(minute: int) -> str:
    return (dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc) +
            dt.timedelta(minutes=minute)).isoformat().replace("+00:00", "Z")


def generate(path: pathlib.Path, samples: int, fail_every: int) -> int:
    if samples < 1 or fail_every < 0:
        raise ValueError("samples must be positive and fail-every non-negative")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for n in range(samples):
            ok = fail_every == 0 or (n + 1) % fail_every != 0
            stream.write(json.dumps({
                **SCHEMA, "sample": n + 1, "timestamp": iso(n),
                "endpoint": "synthetic://zoracleflux/health", "status": 200 if ok else 503,
                "latency_ms": 10 if ok else 1000, "ok": ok
            }, sort_keys=True) + "\n")
    print(f"GENERATED synthetic=true samples={samples} path={path}")
    return 0


def check(path: pathlib.Path, target: float) -> int:
    rows = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"ERROR line={line_number} invalid-json={exc}")
                return 2
            required = {"schema", "synthetic", "sample", "timestamp", "endpoint", "status", "ok"}
            if not required.issubset(row) or row["schema"] != SCHEMA["schema"] or row["synthetic"] is not True:
                print(f"ERROR line={line_number} schema-or-synthetic-marker-invalid")
                return 2
            if (not isinstance(row["sample"], int) or row["sample"] < 1
                    or not isinstance(row["status"], int)
                    or not isinstance(row["ok"], bool)
                    or row["ok"] != (200 <= row["status"] < 300)):
                print(f"ERROR line={line_number} type-invalid")
                return 2
            try:
                dt.datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            except (TypeError, ValueError):
                print(f"ERROR line={line_number} timestamp-invalid")
                return 2
            rows.append(row)
    if not rows:
        print("ERROR no samples")
        return 2
    available = sum(1 for row in rows if row["ok"])
    rate = available / len(rows)
    status = "PASS" if rate >= target else "FAIL"
    print(f"{status} synthetic=true samples={len(rows)} available={available} "
          f"availability={rate:.6f} target={target:.6f} NON_PRODUCTION_EVIDENCE_ONLY")
    return 0 if status == "PASS" else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--out", type=pathlib.Path, required=True)
    gen.add_argument("--samples", type=int, default=24)
    gen.add_argument("--fail-every", type=int, default=0)
    chk = sub.add_parser("check")
    chk.add_argument("--input", type=pathlib.Path, required=True)
    chk.add_argument("--target", type=float, default=0.999)
    args = parser.parse_args(argv)
    try:
        return generate(args.out, args.samples, args.fail_every) if args.command == "generate" else check(args.input, args.target)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
