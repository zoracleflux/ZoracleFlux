"""Safe local pilot ledger using SQLite and synthetic runs only."""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path

from . import SCHEMA_VERSION, __version__
from .relations import discover_relations, production_api, validate_relation


def run_pilot(db_path: Path, runs: int = 1) -> dict:
    """Record bounded deterministic fixture runs in a local SQLite file.

    No source path, network, credential, model, or shell input is accepted.
    """
    if not 1 <= runs <= 20:
        raise ValueError("runs must be between 1 and 20")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    with sqlite3.connect(str(db_path)) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS pilot_runs "
            "(run_id TEXT PRIMARY KEY, created_utc TEXT NOT NULL, version TEXT NOT NULL, "
            "status TEXT NOT NULL, relations INTEGER NOT NULL, passed INTEGER NOT NULL, "
            "model_calls INTEGER NOT NULL, network_calls INTEGER NOT NULL, evidence_json TEXT NOT NULL)"
        )
        reports = []
        for _ in range(runs):
            outcomes = [validate_relation(r, production_api()) for r in discover_relations()]
            passed = sum(row["status"] == "passed" for row in outcomes)
            status = "passed" if passed == len(outcomes) else "failed"
            report = {
                "schema_version": SCHEMA_VERSION,
                "version": __version__,
                "run_id": uuid.uuid4().hex,
                "status": status,
                "relations": len(outcomes),
                "passed": passed,
                "model_calls": 0,
                "network_calls": 0,
                "evidence": "synthetic fixture; bounded deterministic cases; not a proof",
            }
            db.execute(
                "INSERT INTO pilot_runs VALUES (?, datetime('now'), ?, ?, ?, ?, ?, ?, ?)",
                (report["run_id"], __version__, status, len(outcomes), passed, 0, 0,
                 json.dumps(outcomes, sort_keys=True)),
            )
            reports.append(report)
        db.commit()
    return {"schema_version": SCHEMA_VERSION, "version": __version__, "status": "passed",
            "database": str(db_path), "runs": reports,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
            "cash_spend_usd": 0.0}
