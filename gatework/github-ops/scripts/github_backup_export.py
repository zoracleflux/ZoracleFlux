"""Export Git refs and non-secret GitHub metadata for disaster recovery staging.

The script has no third-party dependencies. It is safe to run locally with
``--no-api``; API export requires GITHUB_TOKEN/GH_TOKEN and never exports
secrets, variables, environment settings, or token values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.request
import re
from datetime import datetime, timezone
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def api_get(url: str, token: str) -> tuple[object, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response), response.headers.get("Link", "")


def api_get_all(url: str, token: str) -> object:
    """Return one object or concatenate every page of a list endpoint."""
    first, link = api_get(url, token)
    if not isinstance(first, list):
        return first
    items = list(first)
    while link:
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        if not match:
            break
        page, link = api_get(match.group(1), token)
        if not isinstance(page, list):
            raise RuntimeError("paginated endpoint returned a non-list page")
        items.extend(page)
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("backup"))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--api-base", default=os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    parser.add_argument("--no-api", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    run(["git", "bundle", "create", str(output / "repository.bundle"), "--all"], root)

    manifest: dict[str, object] = {
        "schema": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": args.repo or None,
        "includes": ["git refs/branches/tags", "releases", "issues", "actions runs"],
        "excludes": ["secrets", "variables", "environment secrets", "tokens"],
        "api_export": False,
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and args.repo and not args.no_api:
        endpoints = {
            "repository.json": f"/repos/{args.repo}",
            "releases.json": f"/repos/{args.repo}/releases?per_page=100",
            "issues.json": f"/repos/{args.repo}/issues?state=all&per_page=100",
            "actions-runs.json": f"/repos/{args.repo}/actions/runs?per_page=100",
        }
        for filename, path in endpoints.items():
            try:
                data = api_get_all(args.api_base.rstrip("/") + path, token)
            except (urllib.error.URLError, urllib.error.HTTPError) as exc:
                raise SystemExit(f"metadata export failed for {path}: {exc}") from exc
            (output / filename).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        manifest["api_export"] = True
    else:
        (output / "API_EXPORT_SKIPPED.txt").write_text(
            "No token/repository supplied; only the Git bundle was exported.\n",
            encoding="utf-8",
        )
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files = sorted(
        path for path in output.iterdir()
        if path.is_file() and path.name != "SHA256SUMS.txt"
    )
    (output / "SHA256SUMS.txt").write_text(
        "".join(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
            for path in files
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
