"""Create a deterministic release manifest for the files that will be signed."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("artifacts", nargs="+", type=Path)
    args = parser.parse_args()

    rows: list[str] = []
    for artifact in sorted(args.artifacts, key=lambda item: item.as_posix()):
        if not artifact.is_file():
            parser.error(f"artifact does not exist: {artifact}")
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        rows.append(f"{digest}  {artifact.as_posix()}")

    args.output.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {args.output} ({len(rows)} entries)")
    for row in rows:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
