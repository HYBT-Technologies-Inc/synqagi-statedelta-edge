from __future__ import annotations

import argparse
import sys

from .io import dump_json, load_json
from .modeldelta import evaluate_modeldelta
from .pipeline import evaluate_capsule
from .schema import CapsuleValidationError, validate_capsule


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="statedelta", description="SYNQAGI StateDelta Edge reference CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a State Capsule")
    validate_parser.add_argument("capsule")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a physical or operational State Capsule")
    evaluate_parser.add_argument("capsule")

    model_parser = subparsers.add_parser("modeldelta", help="Evaluate a base-vs-fine-tuned model capsule")
    model_parser.add_argument("capsule")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        capsule = load_json(args.capsule)
        if args.command == "validate":
            result = validate_capsule(capsule)
            print(dump_json({"valid": result.valid, "errors": list(result.errors)}))
        elif args.command == "evaluate":
            print(dump_json(evaluate_capsule(capsule)))
        elif args.command == "modeldelta":
            print(dump_json(evaluate_modeldelta(capsule)))
        return 0
    except (CapsuleValidationError, ValueError, FileNotFoundError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
