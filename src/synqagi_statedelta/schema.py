from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .constants import SUPPORTED_CONTRACT_MAJOR
from .util import major_version


class CapsuleValidationError(ValueError):
    """Raised when a State Capsule violates the supported contract."""


REQUIRED_TOP_LEVEL = (
    "contract_version",
    "capsule_id",
    "subject",
    "expected",
    "observed",
    "history",
    "context",
    "policies",
    "provenance",
    "privacy",
)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]


def validate_capsule(capsule: dict[str, Any], *, raise_on_error: bool = True) -> ValidationResult:
    errors: list[str] = []

    if not isinstance(capsule, dict):
        errors.append("State Capsule must be a JSON object.")
    else:
        for key in REQUIRED_TOP_LEVEL:
            if key not in capsule:
                errors.append(f"Missing required field: {key}")

        version = capsule.get("contract_version")
        if not isinstance(version, str):
            errors.append("contract_version must be a semantic-version string.")
        else:
            try:
                if major_version(version) != SUPPORTED_CONTRACT_MAJOR:
                    errors.append(
                        f"Unsupported contract major version {major_version(version)}; "
                        f"supported major is {SUPPORTED_CONTRACT_MAJOR}."
                    )
            except ValueError as exc:
                errors.append(str(exc))

        subject = capsule.get("subject")
        if not isinstance(subject, dict):
            errors.append("subject must be an object.")
        else:
            for key in ("id", "type", "profile"):
                if not subject.get(key):
                    errors.append(f"subject.{key} is required.")

        privacy = capsule.get("privacy")
        if not isinstance(privacy, dict):
            errors.append("privacy must be an object.")
        else:
            if privacy.get("processing") != "local":
                errors.append("privacy.processing must be 'local' in the current offline profile.")
            for key in ("raw_data_retained", "export_allowed"):
                if not isinstance(privacy.get(key), bool):
                    errors.append(f"privacy.{key} must be boolean.")

        for key in ("expected", "observed", "history", "context", "policies", "provenance"):
            if key in capsule and not isinstance(capsule[key], dict):
                errors.append(f"{key} must be an object.")

    result = ValidationResult(valid=not errors, errors=tuple(errors))
    if errors and raise_on_error:
        raise CapsuleValidationError("; ".join(errors))
    return result
