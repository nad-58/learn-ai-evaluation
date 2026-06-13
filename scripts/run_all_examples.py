"""Discover and run lightweight Python examples in separate processes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

OPTIONAL_MARKER = "ci: optional-example"


def is_optional_example(path: Path) -> bool:
    """Return True when an example declares heavy or external requirements."""
    try:
        header = path.read_text(encoding="utf-8")[:1024].lower()
    except (OSError, UnicodeDecodeError):
        return False
    return OPTIONAL_MARKER in header


def discover_examples(root: Path) -> tuple[list[Path], list[Path]]:
    """Return runnable and optional examples found under the examples directory."""
    scripts = sorted(
        path
        for path in (root / "examples").rglob("*.py")
        if not path.name.startswith("_")
    )
    optional = [path for path in scripts if is_optional_example(path)]
    runnable = [path for path in scripts if path not in optional]
    return runnable, optional


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts, optional = discover_examples(root)
    if not scripts:
        print("No runnable example scripts were found.", file=sys.stderr)
        return 1

    if optional:
        print("Skipping optional examples:")
        for path in optional:
            print(f"- {path.relative_to(root)}")

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

    print(f"\nAll {len(scripts)} lightweight example scripts completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
