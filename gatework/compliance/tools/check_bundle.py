#!/usr/bin/env python3
"""No-network structural checks for the compliance bundle."""
from __future__ import annotations

import csv
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        "README.md", "RESEARCH_SOURCES.md", "CONTROL_EVIDENCE_MATRIX.csv",
        "AUDIT_CALENDAR.csv", "FUNDED_APPROVAL_PATH.md",
        "PATHWAYS_AND_FRAMEWORKS.md", "TEMPLATE_CROSSWALK.md",
        "EXTERNAL_HANDOFF_CHECKLIST.md", "EVIDENCE_CONTROL_MAP.csv",
        "NO_CASH_PATHWAY_LEDGER.csv",
        "templates/PRIVACY_NOTICE.md", "templates/TERMS_AND_CUSTOMER_BOUNDARIES.md",
        "templates/DPA.md", "templates/SECURITY_POLICY.md",
        "templates/INCIDENT_RESPONSE.md", "templates/VULNERABILITY_DISCLOSURE.md",
        "templates/SUPPORT_ONCALL.md", "templates/DATA_RETENTION_DELETION.md",
        "templates/SLA_TEMPLATE.md", "templates/SOC2_ISO_READINESS.md",
    ]
    missing = [item for item in required if not (ROOT / item).is_file()]
    if missing:
        print("FAIL missing=" + ",".join(missing))
        return 1
    with (ROOT / "CONTROL_EVIDENCE_MATRIX.csv").open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    if not rows or any(not row.get("id") or not row.get("evidence_expected") for row in rows):
        print("FAIL control-matrix-schema")
        return 1
    with (ROOT / "EVIDENCE_CONTROL_MAP.csv").open(newline="", encoding="utf-8-sig") as stream:
        evidence_rows = list(csv.DictReader(stream))
    if not evidence_rows or any(not row.get("evidence_id") or not row.get("minimum_fields")
                                or not row.get("acceptance_and_limit") for row in evidence_rows):
        print("FAIL evidence-map-schema")
        return 1
    with (ROOT / "NO_CASH_PATHWAY_LEDGER.csv").open(newline="", encoding="utf-8-sig") as stream:
        pathway_rows = list(csv.DictReader(stream))
    if not pathway_rows or any(not row.get("pathway") or not row.get("source")
                               or not row.get("status") for row in pathway_rows):
        print("FAIL pathway-ledger-schema")
        return 1
    placeholders = []
    for template in (ROOT / "templates").glob("*.md"):
        text = template.read_text(encoding="utf-8")
        if "DRAFT" not in text and "SELF-ASSESSMENT" not in text:
            placeholders.append(f"{template.name}:missing-draft-marker")
    if placeholders:
        print("FAIL " + ",".join(placeholders))
        return 1
    tool = ROOT / "tools" / "synthetic_uptime.py"
    result = subprocess.run([sys.executable, str(tool), "generate", "--out",
                             str(ROOT / "evidence" / "check-synthetic.jsonl"),
                             "--samples", "3"], capture_output=True, text=True, check=False)
    if result.returncode:
        print("FAIL synthetic-generator " + result.stdout.strip())
        return 1
    result = subprocess.run([sys.executable, str(tool), "check", "--input",
                             str(ROOT / "evidence" / "check-synthetic.jsonl"),
                             "--target", "0.999"], capture_output=True, text=True, check=False)
    if result.returncode:
        print("FAIL synthetic-checker " + result.stdout.strip())
        return 1
    (ROOT / "evidence" / "check-synthetic.jsonl").unlink(missing_ok=True)
    print(f"PASS files={len(required)} controls={len(rows)} evidence_map={len(evidence_rows)} "
          f"pathways={len(pathway_rows)} templates=10 synthetic=PASS no-network=true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
