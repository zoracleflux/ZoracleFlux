"""Verify the local release signatures and the candidate's existing manifest."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SIGNING = Path(__file__).resolve().parent
ALLOWED_SIGNERS = SIGNING / "allowed_signers"
PRINCIPAL = "zoracleflux-release"
SIGNED = {
    "wheel": ROOT / "dist" / "zoracleflux-1.0.0rc2-py3-none-any.whl",
    "sdist": ROOT / "dist" / "zoracleflux-1.0.0rc2.tar.gz",
    "sbom": ROOT / "SBOM.json",
    "manifest": ROOT / "ARTIFACT_MANIFEST.sha256",
}


def verify_signature(label: str, artifact: Path) -> bool:
    signature = SIGNING / "signatures" / f"{label}.sig"
    result = subprocess.run(
        [
            "ssh-keygen",
            "-Y",
            "verify",
            "-f",
            str(ALLOWED_SIGNERS),
            "-I",
            PRINCIPAL,
            "-n",
            "file",
            "-s",
            str(signature),
        ],
        input=artifact.read_bytes(),
        capture_output=True,
        check=False,
    )
    stdout = result.stdout.decode(errors="replace").strip()
    stderr = result.stderr.decode(errors="replace").strip()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    status = "PASS" if result.returncode == 0 else "FAIL"
    print(f"{label} signature: {status}")
    return result.returncode == 0


def verify_manifest() -> bool:
    failures = 0
    for line in (ROOT / "ARTIFACT_MANIFEST.sha256").read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        artifact = ROOT / Path(relative.replace("\\", "/"))
        actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
        status = "OK" if actual == expected else "FAIL"
        print(f"{expected}  {relative}  {status}")
        failures += status == "FAIL"
    print(f"manifest digest entries: {failures} failed")
    return failures == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--signatures-only",
        action="store_true",
        help="verify detached signatures without checking the candidate manifest",
    )
    args = parser.parse_args()
    signature_results = [
        verify_signature(label, artifact) for label, artifact in SIGNED.items()
    ]
    signatures_ok = all(signature_results)
    manifest_ok = args.signatures_only or verify_manifest()
    return 0 if signatures_ok and manifest_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

