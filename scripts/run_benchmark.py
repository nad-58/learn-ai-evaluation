"""Run the repository benchmark and enforce regression thresholds."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.benchmark_regression import (  # noqa: E402
    aggregate_track_scores,
    all_passed,
    evaluate_regressions,
    load_benchmark_scores,
    load_regression_rules,
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "track",
        "current_score",
        "baseline_score",
        "minimum_score",
        "allowed_floor",
        "delta",
        "passed",
        "reason",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], passed: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Automated Benchmark Report",
        "",
        f"Overall regression status: **{'PASS' if passed else 'FAIL'}**",
        "",
        "| Track | Current | Baseline | Allowed floor | Delta | Status | Reason |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        lines.append(
            "| {track} | {current_score:.6f} | {baseline_score:.6f} | "
            "{allowed_floor:.6f} | {delta:+.6f} | {status} | {reason} |".format(
                status=status,
                **row,
            )
        )
    lines.extend(
        [
            "",
            "The overall score is an equal-weight mean of the individual track means.",
            "Thresholds are defined in `data/benchmark_baseline.csv`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "data" / "synthetic_benchmark.csv",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=ROOT / "data" / "benchmark_baseline.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "reports",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    grouped = load_benchmark_scores(args.benchmark)
    scores = aggregate_track_scores(grouped)
    rules = load_regression_rules(args.baseline)
    results = evaluate_regressions(scores, rules)
    passed = all_passed(results)
    rows = [asdict(result) for result in results]

    payload: dict[str, object] = {
        "benchmark": str(args.benchmark),
        "baseline": str(args.baseline),
        "passed": passed,
        "track_scores": scores,
        "regression_results": rows,
    }

    write_json(args.output_dir / "benchmark_results.json", payload)
    write_csv(args.output_dir / "benchmark_results.csv", rows)
    write_markdown(args.output_dir / "benchmark_report.md", rows, passed)

    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        print(
            f"{status:4} {row['track']:8} current={row['current_score']:.6f} "
            f"floor={row['allowed_floor']:.6f} delta={row['delta']:+.6f}"
        )

    print(f"\nBenchmark regression status: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
