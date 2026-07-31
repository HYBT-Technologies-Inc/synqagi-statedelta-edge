from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .util import get_path


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    passed: bool
    path: str
    expected: Any
    observed: Any
    severity: str
    action: str | None
    evidence_type: str
    message: str


def _compare(operator: str, observed: Any, expected: Any) -> bool:
    if operator == "eq":
        return observed == expected
    if operator == "ne":
        return observed != expected
    if operator == "lt":
        return observed < expected
    if operator == "lte":
        return observed <= expected
    if operator == "gt":
        return observed > expected
    if operator == "gte":
        return observed >= expected
    if operator == "in":
        return observed in expected
    if operator == "not_in":
        return observed not in expected
    if operator == "between":
        lower, upper = expected
        return lower <= observed <= upper
    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_rule(capsule: dict[str, Any], rule: dict[str, Any]) -> RuleResult:
    rule_id = str(rule.get("id", "unnamed-rule"))
    path = str(rule["path"])
    operator = str(rule.get("operator", "eq"))
    expected = rule.get("value")
    severity = str(rule.get("severity", "MEDIUM")).upper()
    action = rule.get("action")
    evidence_type = str(rule.get("evidence_type", "measured_rule_result"))

    try:
        observed = get_path(capsule, path)
    except KeyError:
        return RuleResult(
            rule_id=rule_id,
            passed=False,
            path=path,
            expected=expected,
            observed=None,
            severity=severity,
            action=action,
            evidence_type="missing_required_evidence",
            message=f"Required value is missing at {path}.",
        )

    try:
        passed = _compare(operator, observed, expected)
        message = f"{path} {operator} {expected!r}: observed {observed!r}."
    except (TypeError, ValueError) as exc:
        passed = False
        message = f"Rule evaluation failed for {path}: {exc}"

    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        path=path,
        expected={"operator": operator, "value": expected},
        observed=observed,
        severity=severity,
        action=action,
        evidence_type=evidence_type,
        message=message,
    )
