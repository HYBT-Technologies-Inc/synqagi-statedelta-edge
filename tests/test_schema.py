import copy
import json
import unittest
from pathlib import Path

from synqagi_statedelta.schema import CapsuleValidationError, validate_capsule


ROOT = Path(__file__).resolve().parents[1]


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.capsule = json.loads((ROOT / "examples/predictive-maintenance/state-capsule.json").read_text())

    def test_valid_capsule(self):
        result = validate_capsule(self.capsule)
        self.assertTrue(result.valid)

    def test_missing_required_field(self):
        capsule = copy.deepcopy(self.capsule)
        del capsule["privacy"]
        with self.assertRaises(CapsuleValidationError):
            validate_capsule(capsule)

    def test_rejects_nonlocal_profile(self):
        capsule = copy.deepcopy(self.capsule)
        capsule["privacy"]["processing"] = "cloud"
        with self.assertRaises(CapsuleValidationError):
            validate_capsule(capsule)


if __name__ == "__main__":
    unittest.main()
