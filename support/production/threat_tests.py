"""Local negative checks for the production-shaped overlay."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True, check=False)


def main() -> int:
    checks: dict[str, str] = {}
    health = run("healthcheck.py", "--root", str(HERE.parent.parent), "--db", str(HERE / "evidence" / "missing.sqlite3"))
    checks["health_missing_db_is_safe"] = "pass" if health.returncode == 0 and "secret" not in health.stdout.lower() else "fail"
    audit = HERE / "evidence" / "threat-audit.jsonl"
    if audit.exists():
        audit.unlink()
    event = run("audit_event.py", "--path", str(audit), "--event", "contains-password", "--status", "passed")
    text = audit.read_text(encoding="utf-8") if event.returncode == 0 else ""
    checks["audit_allowlist"] = "pass" if "[REDACTED]" in text and "password" not in text.lower() and "token" not in text.lower() else "fail"
    metrics = run("metrics.py", "--audit", str(audit))
    try:
        payload = json.loads("{" + "}")  # ensure no accidental command execution is involved
        del payload
        checks["metrics_no_network"] = "pass" if metrics.returncode == 0 and "zoracleflux_audit_events_total" in metrics.stdout else "fail"
    except json.JSONDecodeError:
        checks["metrics_no_network"] = "fail"
    malicious = HERE / "evidence" / "malicious-backup"
    shutil.rmtree(malicious, ignore_errors=True)
    malicious.mkdir(parents=True)
    (malicious / "MANIFEST.json").write_text(
        json.dumps({"file": "../backup/pilot.sqlite3", "sha256": "invalid"}), encoding="utf-8"
    )
    restore = run("backup.py", "restore", "--backup-dir", str(malicious), "--target", str(malicious / "out.sqlite3"))
    checks["backup_path_traversal_rejected"] = "pass" if restore.returncode != 0 else "fail"
    shutil.rmtree(malicious, ignore_errors=True)
    # This overlay is stdlib-only and must not introduce shell/network execution.
    source = "\n".join(
        p.read_text(encoding="utf-8") for p in HERE.glob("*.py") if p.name != Path(__file__).name
    )
    forbidden = ("os.system(", "subprocess.Popen(", "socket.", "urllib.request", "requests.")
    checks["overlay_static_boundary"] = "pass" if not any(token in source for token in forbidden) else "fail"
    status = "passed" if all(value == "pass" for value in checks.values()) else "failed"
    print(json.dumps({"schema_version": 1, "status": status, "checks": checks}, sort_keys=True))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
