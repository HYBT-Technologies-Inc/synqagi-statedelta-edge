"""SYNQAGI StateDelta Edge reference implementation."""

from .pipeline import evaluate_capsule
from .schema import CapsuleValidationError, validate_capsule

__all__ = ["evaluate_capsule", "validate_capsule", "CapsuleValidationError"]
__version__ = "0.1.0"
