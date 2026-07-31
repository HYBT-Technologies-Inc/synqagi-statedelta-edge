# SYNQAGI — StateDelta Edge

**Offline expected-to-observed intelligence and fine-tuned model assurance for Arm64 edge systems.**

SYNQAGI StateDelta Edge is a privacy-preserving AI system designed to compare expected, specified, baseline, or previous states with observed real-world or model states.

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

## Project Objectives

- Run completely offline on an Arm64 edge device.
- Preserve privacy by processing sensitive data locally.
- Support heterogeneous physical and AI-system states.
- Produce measurable and reproducible evidence.
- Reduce model size, memory use, latency, and energy consumption.
- Compare baseline and optimized implementations on the same device.
- Provide reusable schemas, adapters, evaluation tools, and deployment workflows.

## Initial Architecture

```text
Sensors / Telemetry / Images / Model Evaluations
                         ↓
                  Modality Adapters
                         ↓
                    State Capsule
                         ↓
              StateDelta Decision Engine
                         ↓
                  Safety Validator
                         ↓
         Alert / Inspection / Control / Stop
```

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

**Architecture and benchmark implementation are in progress.**

Benchmark results and performance claims will be published only after reproducible testing on the target Jetson hardware.

## Licensing

Source code is licensed under the [Apache License 2.0](LICENSE).

Third-party models, datasets, weights, and dependencies remain subject to their respective licences.

## Trademark

**SYNQAGI** is a registered UK trade mark.

The SYNQAGI name, logo, and associated brand assets are not licensed under the Apache License 2.0. No trade mark licence is granted except for reasonable use necessary to identify the origin of this software.

---

Copyright © AISC TECHNOLOGIES LTD and project contributors.
