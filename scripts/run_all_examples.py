"""Discover and run lightweight Python examples in separate processes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

OPTIONAL_EXAMPLES = {
    Path("examples/small-vlm-tool-inventory/sft_training_skeleton.py"),
}


def discover_examples(root: Path) -> list[Path]:
    """Return runnable examples, excluding GPU or external-data training scripts."""
    scripts = sorted((root / "examples").rglob("*.py"))
    return [script for script in scripts if script.relative_to(root) not in OPTIONAL_EXAMPLES]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    scripts = discover_examples(root)
    if not scripts:
        print("No runnable example scripts were found.", file=sys.stderr)
        return 1

    print("Skipping optional examples:")
    for optional in sorted(OPTIONAL_EXAMPLES):
        print(f"- {optional}")

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
