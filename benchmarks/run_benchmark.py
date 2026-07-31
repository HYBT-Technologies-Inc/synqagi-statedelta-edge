from __future__ import annotations

import argparse
import json
import statistics
import time
import tracemalloc
from pathlib import Path

from synqagi_statedelta.io import load_json
from synqagi_statedelta.pipeline import evaluate_capsule


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * fraction))))
    return ordered[index]


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark the deterministic StateDelta reference pipeline.")
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.iterations <= 0 or args.warmup < 0:
        raise SystemExit("iterations must be positive and warmup must be non-negative")

    capsule = load_json(args.capsule)
    for _ in range(args.warmup):
        evaluate_capsule(capsule)

    latencies_ms: list[float] = []
    tracemalloc.start()
    for _ in range(args.iterations):
        started = time.perf_counter_ns()
        evaluate_capsule(capsule)
        elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
        latencies_ms.append(elapsed_ms)
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "benchmark": "deterministic-reference-pipeline",
        "capsule": str(Path(args.capsule)),
        "iterations": args.iterations,
        "warmup": args.warmup,
        "latency_ms": {
            "mean": statistics.fmean(latencies_ms),
            "p50": percentile(latencies_ms, 0.50),
            "p95": percentile(latencies_ms, 0.95),
            "min": min(latencies_ms),
            "max": max(latencies_ms)
        },
        "python_tracemalloc_bytes": {
            "current": current_bytes,
            "peak": peak_bytes
        },
        "limitations": [
            "This benchmark does not measure model inference.",
            "This benchmark does not measure Jetson board power.",
            "Run device-specific benchmarks separately under a documented power mode."
        ]
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
