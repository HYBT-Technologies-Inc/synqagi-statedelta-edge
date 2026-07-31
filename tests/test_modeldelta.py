import json
import unittest
from pathlib import Path

from synqagi_statedelta.modeldelta import evaluate_modeldelta


ROOT = Path(__file__).resolve().parents[1]


class ModelDeltaTests(unittest.TestCase):
    def test_detects_blocking_regressions(self):
        capsule = json.loads((ROOT / "examples/modeldelta/model-capsule.json").read_text())
        report = evaluate_modeldelta(capsule)
        self.assertEqual(report["release_decision"], "REJECT_FOR_RELEASE")
        self.assertIn("target_capability", report["gained"])
        self.assertIn("general_reasoning", report["regressed"])
        self.assertIn("safety", report["failed_contracts"])


if __name__ == "__main__":
    unittest.main()
