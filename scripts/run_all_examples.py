"""Discover and run every Python example in a separate process."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = sorted((root / "examples").rglob("*.py"))
    if not scripts:
        print("No example scripts were found.", file=sys.stderr)
        return 1

    failures: list[tuple[Path, int]] = []
    for script in scripts:
        relative = script.relative_to(root)
        print(f"\n=== Running {relative} ===", flush=True)
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=root,
            check=False,
        )
        if result.returncode != 0:
            failures.append((relative, result.returncode))

    if failures:
        print("\nExample failures:", file=sys.stderr)
        for path, code in failures:
            print(f"- {path}: exit code {code}", file=sys.stderr)
        return 1

    print(f"\nAll {len(scripts)} example scripts completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
