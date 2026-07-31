from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .constants import SEVERITY_ORDER
from .rules import evaluate_rule


@dataclass(frozen=True)
class SafetyResult:
    recommended_action: str
    validated_action: str
    overridden: bool
    reasons: tuple[str, ...]


def validate_action(capsule: dict[str, Any], recommended_action: str) -> SafetyResult:
    policies = capsule.get("policies", {})
    allowed = policies.get("allowed_actions", [])
    fallback = str(policies.get("safe_fallback", "STOP"))
    reasons: list[str] = []

    action = recommended_action
    if not isinstance(allowed, list) or action not in allowed:
        reasons.append(f"Action {action!r} is not in allowed_actions; using safe fallback {fallback!r}.")
        action = fallback

    strongest = "NONE"
    strongest_action: str | None = None
    for rule in policies.get("safety", []):
        result = evaluate_rule(capsule, rule)
        # Safety rules describe a safe condition. A failed rule triggers its action.
        if not result.passed:
            reasons.append(f"Safety rule {result.rule_id} failed: {result.message}")
            if SEVERITY_ORDER.get(result.severity, 0) >= SEVERITY_ORDER.get(strongest, 0):
                strongest = result.severity
                strongest_action = result.action or fallback

    if strongest_action is not None:
        action = strongest_action

    return SafetyResult(
        recommended_action=recommended_action,
        validated_action=action,
        overridden=action != recommended_action,
        reasons=tuple(reasons),
    )
