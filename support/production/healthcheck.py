"""Offline health check for a local ZoracleFlux pilot."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--db", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    checks: dict[str, str] = {}
    package = root / "src" / "zoracleflux"
    checks["package_present"] = "pass" if package.is_dir() else "fail"
    checks["database_parent"] = "pass" if args.db.resolve().parent.exists() else "fail"
    if args.db.exists():
        try:
            with sqlite3.connect(str(args.db)) as conn:
                result = conn.execute("PRAGMA integrity_check").fetchone()[0]
            checks["sqlite_integrity"] = "pass" if result == "ok" else "fail"
        except sqlite3.Error:
            checks["sqlite_integrity"] = "fail"
    else:
        checks["sqlite_integrity"] = "not_initialized"
    status = "passed" if all(v in {"pass", "not_initialized"} for v in checks.values()) else "failed"
    payload = {"schema_version": 1, "component": "zoracleflux-local-pilot", "status": status, "checks": checks}
    print(json.dumps(payload, sort_keys=True))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
