"""Fail-closed verification for Sigstore bundles from the release workflow.

This script deliberately requires an existing bundle for every artifact. It never
creates, downloads, or accepts a signature without checking the GitHub identity.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


ISSUER = "https://token.actions.githubusercontent.com"


def bundle_for(artifact: Path, explicit: Path | None) -> Path:
    return explicit or Path(f"{artifact}.sigstore.json")


def verify_manifest(manifest: Path) -> bool:
    if not manifest.is_file():
        print(f"FAIL {manifest}: manifest missing", file=sys.stderr)
        return False
    ok = True
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, relative = line.split(maxsplit=1)
        except ValueError:
            print(f"FAIL {manifest}: malformed line: {line}", file=sys.stderr)
            ok = False
            continue
        artifact = manifest.parent / Path(relative.replace("\\", "/"))
        if not artifact.is_file():
            print(f"FAIL {manifest}: listed file missing: {artifact}", file=sys.stderr)
            ok = False
            continue
        actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
        current = actual == expected
        print(f"{'PASS' if current else 'FAIL'} manifest {relative}")
        ok = current and ok
    return ok


def verify(
    artifact: Path,
    bundle: Path,
    repository: str,
    identity: str,
    issuer: str,
    ref: str | None,
    sha: str | None,
) -> bool:
    if not artifact.is_file():
        print(f"FAIL {artifact}: artifact missing", file=sys.stderr)
        return False
    if not bundle.is_file():
        print(f"FAIL {artifact}: bundle missing: {bundle}", file=sys.stderr)
        return False

    command = [
        sys.executable,
        "-m",
        "sigstore",
        "verify",
        "github",
        str(artifact),
        "--bundle",
        str(bundle),
        "--repository",
        repository,
        "--cert-identity",
        identity,
    ]
    if ref:
        command.extend(["--ref", ref])
    if sha:
        command.extend(["--sha", sha])

    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0 and (
        "No module named sigstore" in result.stderr
        or "No module named sigstore" in result.stdout
    ):
        print(
            "FAIL sigstore-python is not installed; install the pinned client "
            "with: python -m pip install sigstore==4.5.0",
            file=sys.stderr,
        )
        return False
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    status = result.returncode == 0
    print(f"{'PASS' if status else 'FAIL'} {artifact} identity={identity}")
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, help="ORG/REPO")
    parser.add_argument("--identity", help="exact Fulcio certificate SAN")
    parser.add_argument("--workflow", default="release-signing.yml")
    parser.add_argument("--ref", help="exact refs/heads/... or refs/tags/...")
    parser.add_argument("--sha", help="exact commit SHA, when known")
    parser.add_argument("--issuer", default=ISSUER)
    parser.add_argument("--manifest", type=Path, help="also check listed SHA-256 digests")
    parser.add_argument(
        "--artifact",
        action="append",
        required=True,
        help="artifact path; repeat once per signed file",
    )
    parser.add_argument(
        "--bundle",
        action="append",
        help="bundle path matching each --artifact; repeat in the same order",
    )
    args = parser.parse_args()
    if args.issuer != ISSUER:
        parser.error("this GitHub verifier only accepts the GitHub Actions issuer")

    identity = args.identity
    if not identity:
        if not args.ref:
            parser.error("--ref is required when --identity is omitted")
        identity = (
            f"https://github.com/{args.repository}/.github/workflows/"
            f"{args.workflow}@{args.ref}"
        )
    bundles = args.bundle or []
    if bundles and len(bundles) != len(args.artifact):
        parser.error("--bundle must be supplied once per --artifact")

    ok = verify_manifest(args.manifest) if args.manifest else True
    for index, raw_artifact in enumerate(args.artifact):
        artifact = Path(raw_artifact)
        bundle = Path(bundles[index]) if bundles else bundle_for(artifact, None)
        ok = verify(
            artifact,
            bundle,
            args.repository,
            identity,
            args.issuer,
            args.ref,
            args.sha,
        ) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
