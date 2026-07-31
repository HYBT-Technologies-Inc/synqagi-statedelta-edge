from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "conformance": {
            "type": "string",
            "enum": [
                "PASS",
                "PASS_WITH_WARNING",
                "FAIL",
                "CRITICAL_FAIL",
            ],
        },
        "state": {
            "type": "string",
            "enum": [
                "NORMAL",
                "CHANGED",
                "DEGRADING",
                "OUT_OF_TOLERANCE",
                "UNSAFE",
            ],
        },
        "severity": {
            "type": "string",
            "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        },
        "recommended_action": {
            "type": "string",
            "enum": ["CONTINUE", "REDUCE_LOAD", "STOP"],
        },
        "requires_human_review": {
            "type": "boolean",
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path": {"type": "string"},
                    "expected_maximum": {"type": "number"},
                    "observed": {"type": "number"},
                },
                "required": [
                    "path",
                    "expected_maximum",
                    "observed",
                ],
            },
        },
    },
    "required": [
        "conformance",
        "state",
        "severity",
        "recommended_action",
        "requires_human_review",
        "evidence",
    ],
}


MESSAGES = [
    {
        "role": "system",
        "content": (
            "You are the SYNQAGI StateDelta interpretation module. "
            "Use only supplied measurements. Do not invent evidence. "
            "Select actions only from the allowed action list. "
            "Your recommendation is advisory and will be checked by "
            "a deterministic safety validator."
        ),
    },
    {
        "role": "user",
        "content": (
            "Expected maximum vibration growth: 8.0 percent. "
            "Observed vibration growth: 14.0 percent. "
            "Allowed actions: CONTINUE, REDUCE_LOAD, STOP. "
            "Return the conformance decision and measured evidence."
        ),
    },
]


def command_output(command: list[str], cwd: Path) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return f"UNAVAILABLE: {exc}"

    output = completed.stdout.strip() or completed.stderr.strip()
    return output or f"exit_code={completed.returncode}"


def invoke_ollama(
    endpoint: str,
    payload: dict[str, Any],
    timeout_seconds: float,
) -> tuple[dict[str, Any], float]:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    started = time.perf_counter()

    with urllib.request.urlopen(
        request,
        timeout=timeout_seconds,
    ) as response:
        result = json.loads(response.read().decode("utf-8"))

    wall_seconds = time.perf_counter() - started
    return result, wall_seconds


def parse_structured_output(result: dict[str, Any]) -> dict[str, Any]:
    message = result.get("message")

    if not isinstance(message, dict):
        raise ValueError("Ollama response does not contain a message object.")

    content = message.get("content")

    if not isinstance(content, str):
        raise ValueError("Ollama message content is not a string.")

    structured_output = json.loads(content)

    if not isinstance(structured_output, dict):
        raise ValueError("Structured output is not a JSON object.")

    return structured_output


def measured_run(
    endpoint: str,
    payload: dict[str, Any],
    timeout_seconds: float,
    run_number: int,
) -> dict[str, Any]:
    result, wall_seconds = invoke_ollama(
        endpoint=endpoint,
        payload=payload,
        timeout_seconds=timeout_seconds,
    )

    structured_output = parse_structured_output(result)

    eval_count = int(result.get("eval_count", 0))
    eval_duration_ns = int(result.get("eval_duration", 0))

    generation_tokens_per_second = (
        eval_count / (eval_duration_ns / 1_000_000_000)
        if eval_count > 0 and eval_duration_ns > 0
        else 0.0
    )

    return {
        "run": run_number,
        "wall_seconds": round(wall_seconds, 6),
        "total_seconds": round(
            int(result.get("total_duration", 0)) / 1_000_000_000,
            6,
        ),
        "load_seconds": round(
            int(result.get("load_duration", 0)) / 1_000_000_000,
            6,
        ),
        "prompt_tokens": int(result.get("prompt_eval_count", 0)),
        "output_tokens": eval_count,
        "generation_tokens_per_second": round(
            generation_tokens_per_second,
            3,
        ),
        "structured_output": structured_output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run a reproducible Ollama structured-output baseline for "
            "the SYNQAGI StateDelta interpretation layer."
        )
    )
    parser.add_argument(
        "--model",
        default="llama3.1:8b",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--endpoint",
        default="http://127.0.0.1:11434/api/chat",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=600.0,
    )
    parser.add_argument(
        "--keep-alive",
        default="10m",
    )
    parser.add_argument(
        "--expected-action",
        default="REDUCE_LOAD",
        choices=["CONTINUE", "REDUCE_LOAD", "STOP"],
    )
    parser.add_argument(
        "--output",
        default="benchmarks/results/ollama-runtime-baseline.json",
    )
    args = parser.parse_args()

    if args.runs <= 0:
        raise SystemExit("--runs must be greater than zero")

    if args.warmup < 0:
        raise SystemExit("--warmup must not be negative")

    repo_root = Path(__file__).resolve().parents[1]

    payload: dict[str, Any] = {
        "model": args.model,
        "messages": MESSAGES,
        "format": DECISION_SCHEMA,
        "stream": False,
        "keep_alive": args.keep_alive,
        "options": {
            "temperature": 0,
            "seed": 42,
            "num_ctx": 4096,
            "num_predict": 256,
        },
    }

    for _ in range(args.warmup):
        invoke_ollama(
            endpoint=args.endpoint,
            payload=payload,
            timeout_seconds=args.timeout,
        )

    runs = [
        measured_run(
            endpoint=args.endpoint,
            payload=payload,
            timeout_seconds=args.timeout,
            run_number=index,
        )
        for index in range(1, args.runs + 1)
    ]

    wall_values = [run["wall_seconds"] for run in runs]
    speed_values = [
        run["generation_tokens_per_second"]
        for run in runs
    ]

    canonical_outputs = {
        json.dumps(
            run["structured_output"],
            sort_keys=True,
            separators=(",", ":"),
        )
        for run in runs
    }

    recommended_actions = sorted(
        {
            str(
                run["structured_output"].get(
                    "recommended_action",
                    "MISSING",
                )
            )
            for run in runs
        }
    )

    policy_alignment = all(
        run["structured_output"].get("recommended_action")
        == args.expected_action
        for run in runs
    )

    report = {
        "benchmark": "ollama-structured-output-runtime-baseline",
        "timestamp_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": command_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
        ),
        "model": args.model,
        "runtime": {
            "endpoint": args.endpoint,
            "ollama_version": command_output(
                ["ollama", "--version"],
                cwd=repo_root,
            ),
            "ollama_processes_after_run": command_output(
                ["ollama", "ps"],
                cwd=repo_root,
            ),
        },
        "configuration": {
            "runs": args.runs,
            "warmup": args.warmup,
            "timeout_seconds": args.timeout,
            "keep_alive": args.keep_alive,
            "temperature": 0,
            "seed": 42,
            "context_length": 4096,
            "maximum_output_tokens": 256,
        },
        "policy_contract": {
            "deterministic_expected_action": args.expected_action,
            "model_recommendation_is_advisory": True,
        },
        "runs": runs,
        "summary": {
            "run_count": len(runs),
            "median_wall_seconds": round(
                statistics.median(wall_values),
                6,
            ),
            "minimum_wall_seconds": round(
                min(wall_values),
                6,
            ),
            "maximum_wall_seconds": round(
                max(wall_values),
                6,
            ),
            "mean_generation_tokens_per_second": round(
                statistics.fmean(speed_values),
                3,
            ),
            "unique_structured_outputs": len(canonical_outputs),
            "fully_repeatable": len(canonical_outputs) == 1,
            "model_recommended_actions": recommended_actions,
            "policy_alignment": policy_alignment,
        },
        "limitations": [
            "The result is specific to the recorded model and runtime.",
            "The model recommendation is not final safety authority.",
            "This run does not measure board-level power consumption.",
            "Jetson before-and-after optimization must be measured separately.",
        ],
    }

    output_path = repo_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nSaved to: {output_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
