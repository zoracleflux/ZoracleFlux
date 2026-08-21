"""Verify the preserved RC3 OpenSSH fallback without network access."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


LABELS = ("wheel", "sdist", "sbom", "manifest")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument(
        "--trust",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "fallback",
    )
    args = parser.parse_args()
    files = {
        "wheel": args.candidate / "dist" / "zoracleflux-1.0.0rc2-py3-none-any.whl",
        "sdist": args.candidate / "dist" / "zoracleflux-1.0.0rc2.tar.gz",
        "sbom": args.candidate / "SBOM.json",
        "manifest": args.candidate / "ARTIFACT_MANIFEST.sha256",
    }
    allowed = args.trust / "allowed_signers"
    passed = True
    for label in LABELS:
        artifact = files[label]
        signature = args.trust / "signatures" / f"{label}.sig"
        command = [
            "ssh-keygen",
            "-Y",
            "verify",
            "-f",
            str(allowed),
            "-I",
            "zoracleflux-release",
            "-n",
            "file",
            "-s",
            str(signature),
        ]
        result = subprocess.run(
            command,
            input=artifact.read_bytes(),
            capture_output=True,
            check=False,
        )
        if result.stdout:
            print(result.stdout.decode(errors="replace").strip())
        if result.stderr:
            print(result.stderr.decode(errors="replace").strip(), file=sys.stderr)
        current = result.returncode == 0
        print(f"{label}: {'PASS' if current else 'FAIL'}")
        passed = current and passed
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
