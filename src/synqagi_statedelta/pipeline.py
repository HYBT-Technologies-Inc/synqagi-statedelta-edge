from __future__ import annotations

from typing import Any

from .constants import DECISION_VERSION, SEVERITY_ORDER
from .delta import evaluate_conformance_rules, violations
from .safety import validate_action
from .schema import validate_capsule


def _max_severity(items: list[Any]) -> str:
    if not items:
        return "NONE"
    return max((item.severity for item in items), key=lambda value: SEVERITY_ORDER.get(value, 0))


def _conformance(severity: str, has_rules: bool) -> tuple[str, str]:
    if not has_rules:
        return "INSUFFICIENT_EVIDENCE", "UNKNOWN"
    if severity == "NONE":
        return "PASS", "NORMAL"
    if severity == "LOW":
        return "PASS_WITH_WARNING", "CHANGED"
    if severity in {"MEDIUM", "HIGH"}:
        return "FAIL", "OUT_OF_TOLERANCE"
    return "CRITICAL_FAIL", "UNSAFE"


def evaluate_capsule(capsule: dict[str, Any]) -> dict[str, Any]:
    validate_capsule(capsule)
    rule_results = evaluate_conformance_rules(capsule)
    failed = violations(rule_results)
    severity = _max_severity(failed)
    conformance, state = _conformance(severity, bool(rule_results))

    recommendation = "CONTINUE"
    if failed:
        # Select the action attached to the most severe failure; keep deterministic order on ties.
        ordered = sorted(
            enumerate(failed),
            key=lambda pair: (SEVERITY_ORDER.get(pair[1].severity, 0), -pair[0]),
            reverse=True,
        )
        recommendation = ordered[0][1].action or capsule.get("policies", {}).get("safe_fallback", "STOP")

    safety = validate_action(capsule, recommendation)

    delta_entries = [
        {
            "rule_id": item.rule_id,
            "path": item.path,
            "expected": item.expected,
            "observed": item.observed,
            "severity": item.severity,
            "message": item.message,
        }
        for item in failed
    ]

    evidence = [
        {
            "type": item.evidence_type,
            "source": capsule.get("provenance", {}).get("adapter", "unknown-adapter"),
            "reference": item.path,
            "classification": "MEASURED" if item.evidence_type.startswith("measured") else "DERIVED",
        }
        for item in failed
    ]

    uncertainty: list[str] = []
    if conformance == "INSUFFICIENT_EVIDENCE":
        uncertainty.append("No conformance rules were supplied.")
    if any(item.evidence_type == "missing_required_evidence" for item in failed):
        uncertainty.append("One or more required observations are missing.")

    total = len(rule_results)
    confidence = 0.0 if total == 0 else round(1.0 - (len(uncertainty) / (total + len(uncertainty))), 4)

    return {
        "decision_version": DECISION_VERSION,
        "capsule_id": capsule["capsule_id"],
        "conformance": conformance,
        "state": state,
        "severity": severity,
        "delta": delta_entries,
        "evidence": evidence,
        "recommended_action": recommendation,
        "validated_action": safety.validated_action,
        "safety_overridden": safety.overridden,
        "safety_reasons": list(safety.reasons),
        "confidence": confidence,
        "uncertainty": uncertainty,
        "requires_human_review": conformance in {"INSUFFICIENT_EVIDENCE", "FAIL"},
    }
