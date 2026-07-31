import copy
import json
import unittest
from pathlib import Path

from synqagi_statedelta.pipeline import evaluate_capsule


ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.capsule = json.loads((ROOT / "examples/predictive-maintenance/state-capsule.json").read_text())

    def test_detects_vibration_violation(self):
        result = evaluate_capsule(self.capsule)
        self.assertEqual(result["conformance"], "FAIL")
        self.assertEqual(result["severity"], "HIGH")
        self.assertEqual(result["validated_action"], "REDUCE_LOAD")
        paths = {item["path"] for item in result["delta"]}
        self.assertIn("observed.measurements.vibration_growth_percent", paths)

    def test_passes_normal_state(self):
        capsule = copy.deepcopy(self.capsule)
        capsule["observed"]["measurements"]["vibration_growth_percent"] = 5.0
        result = evaluate_capsule(capsule)
        self.assertEqual(result["conformance"], "PASS")
        self.assertEqual(result["validated_action"], "CONTINUE")

    def test_hard_safety_override(self):
        capsule = copy.deepcopy(self.capsule)
        capsule["observed"]["measurements"]["temperature_c"] = 95.0
        result = evaluate_capsule(capsule)
        self.assertEqual(result["validated_action"], "STOP")
        self.assertTrue(result["safety_overridden"])


if __name__ == "__main__":
    unittest.main()
