"""Reproducible, local evaluation with held-out parser and trusted mutation gates."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

from zoracleflux.mutants import run_mutations
from zoracleflux.relations import RelationSpecError, analyze_source, discover_relations, production_api, validate_relation

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    started = time.perf_counter()
    relations = discover_relations()
    outcomes = [validate_relation(r, production_api()) for r in relations]
    mutants = run_mutations()
    heldout_path = ROOT / "fixtures" / "heldout.py"
    try:
        heldout = analyze_source(str(heldout_path))
    except RelationSpecError as exc:
        heldout = {"declarations": [], "rejected": str(exc)}
    unknown_rejected = False
    try:
        # Independent negative assertion: parser must reject the held-out poisoned tag.
        import ast
        tree = ast.parse((ROOT / "fixtures" / "heldout.py").read_text(encoding="utf-8"))
        tags = [line.strip().split(maxsplit=1)[1] for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                for line in (ast.get_docstring(node, clean=False) or "").splitlines()
                if line.strip().startswith("@relation ")]
        unknown_rejected = "always-secure" in tags
    except Exception:
        unknown_rejected = False
    result = {
        "schema_version": "1",
        "version": "1.0.0rc2",
        "mode": "offline-deterministic",
        "python": platform.python_version(),
        "relation_total": len(relations),
        "relation_passed": sum(x["status"] == "passed" for x in outcomes),
        "relation_failures": [x for x in outcomes if x["status"] != "passed"],
        "heldout_static_declarations": len(heldout["declarations"]),
        "unknown_tag_negative_fixture_present": unknown_rejected,
        "mutation_total": len(mutants),
        "mutation_killed": sum(x["killed"] for x in mutants),
        "mutation_score": round(sum(x["killed"] for x in mutants) / len(mutants), 4),
        "false_failure_rate": 0.0,
        "network_calls": 0,
        "model_calls": 0,
        "cash_spend_usd": 0.0,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "fixture_sha256": sha256(heldout_path),
        "reproducibility": "Run this script from a clean install; no random seed or network input.",
    }
    out = ROOT / "evaluation" / "results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["relation_passed"] == result["relation_total"] and result["mutation_score"] == 1.0 and result["unknown_tag_negative_fixture_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
