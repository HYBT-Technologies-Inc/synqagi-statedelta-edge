PYTHON ?= python3

.PHONY: install test lint demo modeldelta benchmark inventory

install:
	$(PYTHON) -m pip install -e . --no-build-isolation

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m compileall src benchmarks

demo:
	$(PYTHON) -m synqagi_statedelta evaluate examples/predictive-maintenance/state-capsule.json

modeldelta:
	$(PYTHON) -m synqagi_statedelta modeldelta examples/modeldelta/model-capsule.json

benchmark:
	$(PYTHON) benchmarks/run_benchmark.py --capsule examples/predictive-maintenance/state-capsule.json --iterations 200 --output benchmarks/results/local-reference.json

inventory:
	bash scripts/collect_jetson_info.sh
