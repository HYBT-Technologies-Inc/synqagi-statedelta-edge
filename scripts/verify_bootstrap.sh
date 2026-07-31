#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=src python3 -m compileall -q src benchmarks
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m synqagi_statedelta validate examples/predictive-maintenance/state-capsule.json >/dev/null
PYTHONPATH=src python3 -m synqagi_statedelta evaluate examples/predictive-maintenance/state-capsule.json >/dev/null
PYTHONPATH=src python3 -m synqagi_statedelta modeldelta examples/modeldelta/model-capsule.json >/dev/null

echo "SYNQAGI bootstrap verification passed."
