"""SQLite backup and restore with a hash manifest, using only stdlib."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def integrity(path: Path) -> bool:
    with sqlite3.connect(str(path)) as conn:
        return conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def backup(db: Path, out: Path) -> int:
    if not db.exists() or not integrity(db):
        raise SystemExit("source database missing or failed integrity_check")
    out.mkdir(parents=True, exist_ok=True)
    destination = out / "pilot.sqlite3"
    with sqlite3.connect(str(db)) as source, sqlite3.connect(str(destination)) as target:
        source.backup(target)
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_name": db.name,
        "file": destination.name,
        "sha256": sha256(destination),
        "sqlite_integrity": integrity(destination),
        "cash_usd": "0.00",
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))
    return 0


def restore(source: Path, target: Path, force: bool) -> int:
    manifest_path = source / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    backup_file = source / manifest["file"]
    if backup_file.resolve().parent != source.resolve():
        raise SystemExit("backup manifest points outside backup directory")
    if sha256(backup_file) != manifest["sha256"] or not integrity(backup_file):
        raise SystemExit("backup hash or integrity check failed")
    if target.exists() and not force:
        raise SystemExit("target exists; pass --force only after preserving it")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".restore-in-progress")
    if temporary.exists():
        temporary.unlink()
    shutil.copy2(backup_file, temporary)
    os.replace(temporary, target)
    print(json.dumps({"restored": str(target), "sha256": sha256(target), "sqlite_integrity": integrity(target)}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    pbackup = sub.add_parser("backup")
    pbackup.add_argument("--db", type=Path, required=True)
    pbackup.add_argument("--out", type=Path, required=True)
    prestore = sub.add_parser("restore")
    prestore.add_argument("--backup-dir", type=Path, required=True)
    prestore.add_argument("--target", type=Path, required=True)
    prestore.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "backup":
        return backup(args.db, args.out)
    return restore(args.backup_dir, args.target, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
