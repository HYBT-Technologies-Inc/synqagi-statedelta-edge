from __future__ import annotations

from typing import Any

from .rules import RuleResult, evaluate_rule


def evaluate_conformance_rules(capsule: dict[str, Any]) -> list[RuleResult]:
    rules = capsule.get("policies", {}).get("conformance", [])
    if not isinstance(rules, list):
        raise ValueError("policies.conformance must be a list.")
    return [evaluate_rule(capsule, rule) for rule in rules]


def violations(results: list[RuleResult]) -> list[RuleResult]:
    return [result for result in results if not result.passed]
