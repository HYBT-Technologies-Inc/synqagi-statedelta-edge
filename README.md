# SYNQAGI — StateDelta Edge

**Offline expected-to-observed intelligence and fine-tuned model assurance for Arm64 edge systems.**

SYNQAGI StateDelta Edge is a privacy-preserving AI system designed to compare expected, specified, baseline, permitted, or previous states with observed real-world or model states.

It detects meaningful deviations, produces traceable evidence, evaluates conformance and risk, and generates safe structured actions locally on NVIDIA Jetson Orin devices without requiring cloud connectivity.

## Core Modules

### StateDelta

A universal expected-vs-observed intelligence engine for:

- industrial equipment and predictive maintenance;
- manufacturing and quality control;
- construction progress and specification verification;
- warehouses, logistics, assets, and infrastructure;
- multimodal sensor, telemetry, image, audio, and event data.

### ModelDelta

An evidence-based assurance layer for comparing base and fine-tuned AI models.

It evaluates:

- target capability gains;
- retention of original capabilities;
- regressions and catastrophic forgetting;
- structured-output reliability;
- robustness and safety;
- deployment readiness after fine-tuning or quantization.

### Edge Runtime

An optimized offline inference runtime for Arm64 edge devices, initially targeting:

- NVIDIA Jetson Orin Nano 8GB — primary deployment target;
- NVIDIA Jetson Orin NX 16GB — extended and validation target.

Training, distillation, experimentation, and model preparation are performed on NVIDIA DGX Spark.

## System Principle

```text
Expected State
      +
Observed State
      +
History and Policy
      ↓
Measured Delta
      ↓
Evidence-Based Interpretation
      ↓
Safety Validation
      ↓
Structured Decision or Physical Action
```

In SYNQAGI, “before and after” means **required, expected, baseline, permitted, or previous state compared with measured, observed, completed, or evaluated state**. It is not limited to two images or two moments in time.

## Repository Status

This bootstrap contains a working deterministic StateDelta reference pipeline, a ModelDelta evaluator, versioned JSON Schemas, examples, tests, benchmark scaffolding, Jetson inventory scripts, CI, legal notices, and architecture decisions.

It intentionally does **not** publish unmeasured performance claims. Model inference adapters and device-specific acceleration will be added after hardware inventory and reproducible baseline testing.

## Quick Start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e . --no-build-isolation
python -m unittest discover -s tests -v
```

Validate and evaluate the predictive-maintenance example:

```bash
statedelta validate examples/predictive-maintenance/state-capsule.json
statedelta evaluate examples/predictive-maintenance/state-capsule.json
```

Run ModelDelta:

```bash
statedelta modeldelta examples/modeldelta/model-capsule.json
```

Run the deterministic benchmark scaffold:

```bash
python benchmarks/run_benchmark.py \
  --capsule examples/predictive-maintenance/state-capsule.json \
  --iterations 200 \
  --output benchmarks/results/local-reference.json
```

Collect a read-only Jetson inventory:

```bash
bash scripts/collect_jetson_info.sh
```

## Initial Architecture

```text
Sensors / Telemetry / Images / Model Evaluations
                         ↓
                  Modality Adapters
                         ↓
                    State Capsule
                         ↓
              Deterministic Delta Engine
                         ↓
        Contextual StateDelta Interpretation
                         ↓
                  Safety Validator
                         ↓
         Alert / Inspection / Control / Stop
```

## Project Objectives

- Run completely offline on an Arm64 edge device.
- Preserve privacy by processing sensitive data locally.
- Support heterogeneous physical and AI-system states.
- Produce measurable and reproducible evidence.
- Reduce model size, memory use, latency, and energy consumption.
- Compare baseline and optimized implementations on the same device.
- Provide reusable schemas, adapters, evaluation tools, and deployment workflows.

## Competition

This repository is being developed for the **Arm AI Optimization Challenge 2026**, under the **Physical AI** track.

The project will include:

- a reproducible baseline;
- a fine-tuned compact model;
- Arm64 edge deployment;
- measurable optimization results;
- offline physical-state demonstrations;
- ModelDelta fine-tuning assurance;
- public source code and setup instructions.

## Current Status

**Architecture, deterministic reference implementation, and benchmark scaffolding are available. Hardware-specific inference and measured optimization work are in progress.**

Benchmark results and performance claims will be published only after reproducible testing on the target Jetson hardware.

## Licensing

Source code is licensed under the [Apache License 2.0](LICENSE).

Third-party models, datasets, weights, and dependencies remain subject to their respective licences. See [MODEL_LICENSES.md](MODEL_LICENSES.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Trademark

**SYNQAGI** is a registered UK trade mark.

The SYNQAGI name, logo, and associated brand assets are not licensed under the Apache License 2.0. See [TRADEMARKS.md](TRADEMARKS.md).

---

Copyright © AISC TECHNOLOGIES LTD and project contributors.
