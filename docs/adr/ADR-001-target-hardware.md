# ADR-001: Target Hardware Architecture

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** AISC TECHNOLOGIES LTD / HYBT Technologies
- **Project:** SYNQAGI — StateDelta Edge

## Context

SYNQAGI StateDelta Edge requires a reproducible Arm64 deployment target for offline expected-vs-observed intelligence, physical-state conformance analysis, safe structured decisions, and ModelDelta assurance.

## Decision

### Primary deployment target

**NVIDIA Jetson Orin Nano 8GB** is the primary competition and production-edge target.

### Extended validation target

**NVIDIA Jetson Orin NX 16GB** is the secondary validation, multimodal, and scale-up target.

### Training and model-development platform

**NVIDIA DGX Spark** is used for dataset preparation, teacher inference, fine-tuning, distillation, ModelDelta evaluation, quantization preparation, export, and packaging.

DGX Spark benchmark results must not be presented as Jetson deployment results. Competition performance comparisons must run on the same target Jetson device under controlled conditions.

## Nano Acceptance Gate

```yaml
target_device: jetson-orin-nano-8gb
offline_required: true
peak_device_memory_gb: 6.5
p95_decision_latency_ms: 1500
structured_output_validity: 0.99
critical_safety_violations: 0
continuous_stability_minutes: 30
```

These are engineering targets, not published benchmark claims.

## NX Promotion Conditions

The Orin NX may become the primary target only when documented testing shows that the Nano cannot satisfy a mandatory capability, memory, latency, stability, or concurrent-adapter requirement without unacceptable quality loss.

A promotion must be recorded in a new ADR. ADR-001 must not be silently rewritten.

## Benchmarking Rules

All baseline and optimized comparisons must use the same physical device, input dataset, schema, evaluation contract, power mode, software versions, hashes, and repeated measurements.
