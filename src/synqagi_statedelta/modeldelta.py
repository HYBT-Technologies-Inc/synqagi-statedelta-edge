from __future__ import annotations

from typing import Any

from .schema import validate_capsule


def evaluate_modeldelta(capsule: dict[str, Any]) -> dict[str, Any]:
    validate_capsule(capsule)
    if capsule.get("subject", {}).get("profile") != "modeldelta":
        raise ValueError("ModelDelta requires subject.profile='modeldelta'.")

    requirements = capsule.get("expected", {}).get("requirements", {})
    observed = capsule.get("observed", {})
    base = observed.get("base_metrics", {})
    candidate = observed.get("candidate_metrics", {})

    checks: list[dict[str, Any]] = []

    def add_check(name: str, base_value: float, candidate_value: float, passed: bool, contract: Any) -> None:
        checks.append(
            {
                "name": name,
                "base": base_value,
                "candidate": candidate_value,
                "delta": round(candidate_value - base_value, 6),
                "contract": contract,
                "passed": passed,
            }
        )

    target_metric = str(requirements.get("target_metric", "target_capability"))
    target_gain_min = float(requirements.get("target_gain_min", 0.0))
    b_target = float(base.get(target_metric, 0.0))
    c_target = float(candidate.get(target_metric, 0.0))
    add_check(target_metric, b_target, c_target, (c_target - b_target) >= target_gain_min, {"gain_min": target_gain_min})

    retention = requirements.get("retention", {})
    for metric, max_regression in retention.items():
        b_value = float(base.get(metric, 0.0))
        c_value = float(candidate.get(metric, 0.0))
        regression = b_value - c_value
        add_check(metric, b_value, c_value, regression <= float(max_regression), {"max_regression": max_regression})

    minimums = requirements.get("candidate_minimums", {})
    for metric, minimum in minimums.items():
        b_value = float(base.get(metric, 0.0))
        c_value = float(candidate.get(metric, 0.0))
        add_check(metric, b_value, c_value, c_value >= float(minimum), {"candidate_minimum": minimum})

    failed = [check for check in checks if not check["passed"]]
    gained = [check for check in checks if check["delta"] > 0 and check["passed"]]
    regressed = [check for check in checks if check["delta"] < 0 and not check["passed"]]

    release_decision = "RELEASE"
    if failed:
        release_decision = "REJECT_FOR_RELEASE"
    elif any(check["delta"] < 0 for check in checks):
        release_decision = "RELEASE_WITH_CONDITIONS"

    recommendations: list[dict[str, str]] = []
    for check in regressed:
        recommendations.append(
            {
                "status": "HYPOTHESIS",
                "metric": check["name"],
                "recommendation": "Test a lower learning rate, fewer update steps, and a retention-data mixture; rerun the paired hidden evaluation before attributing cause.",
            }
        )

    return {
        "certificate_version": "1.0.0",
        "capsule_id": capsule["capsule_id"],
        "release_decision": release_decision,
        "checks": checks,
        "gained": [item["name"] for item in gained],
        "retained": [item["name"] for item in checks if item["passed"] and item["delta"] <= 0],
        "regressed": [item["name"] for item in regressed],
        "failed_contracts": [item["name"] for item in failed],
        "recommendations": recommendations,
    }
