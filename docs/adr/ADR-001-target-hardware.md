# ADR-001: Target Hardware Architecture

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** AISC TECHNOLOGIES LTD / HYBT Technologies
- **Project:** SYNQAGI — StateDelta Edge

## Context

SYNQAGI StateDelta Edge requires a reproducible Arm64 deployment target for offline expected-vs-observed intelligence, physical-state conformance analysis, safe structured decisions, and ModelDelta assurance.

The target platform must demonstrate:

- fully local inference without mandatory cloud connectivity;
- privacy-preserving processing of sensitive observations;
- low-power deployment on an accessible edge device;
- measurable improvements in model size, memory use, latency, and energy consumption;
- support for structured State Capsules and constrained decisions;
- integration with telemetry, vision, sensor, and model-evaluation adapters;
- reproducible comparison between baseline and optimized implementations.

Model training, fine-tuning, distillation, evaluation, and export require a separate development platform with substantially greater memory and compute capacity.

## Decision

### Primary deployment target

**NVIDIA Jetson Orin Nano 8GB**

The Jetson Orin Nano 8GB is the primary competition and production-edge target.

The optimized SYNQAGI runtime will be designed first for its memory, power, and deployment constraints.

The primary target configuration is expected to run:

- one compact fine-tuned language or decision model;
- quantized inference;
- short structured State Capsules;
- constrained structured output;
- one active modality adapter;
- the deterministic safety validator;
- telemetry and benchmark collection;
- the local SYNQAGI Evidence Console.

### Extended validation target

**NVIDIA Jetson Orin NX 16GB**

The Jetson Orin NX 16GB is the secondary validation and extended deployment target.

It will be used for:

- compatibility validation;
- memory-intensive multimodal configurations;
- simultaneous vision and language inference;
- larger model candidates;
- parallel adapter pipelines;
- stress testing;
- comparison of deployment scalability.

The Orin NX is not the default competition target unless the Orin Nano fails the defined acceptance gate.

### Training and model-development platform

**NVIDIA DGX Spark**

DGX Spark is the model-development platform for:

- dataset preparation;
- teacher-model inference;
- synthetic scenario generation;
- LoRA and QLoRA fine-tuning;
- knowledge distillation;
- ModelDelta evaluation;
- checkpoint comparison;
- quantization preparation;
- model export and packaging.

DGX Spark benchmark results must not be presented as Jetson deployment results.

Competition performance comparisons will be performed on the same target Jetson device under controlled conditions.

## Nano Acceptance Gate

The Jetson Orin Nano 8GB remains the primary target when the selected optimized model satisfies all mandatory criteria.

### Mandatory functional criteria

- runs without mandatory internet access;
- accepts a valid State Capsule;
- produces schema-valid structured decisions;
- passes the deterministic safety validator;
- supports at least one physical-state adapter;
- supports ModelDelta evaluation results;
- completes a continuous stability test;
- does not expose raw sensitive observations outside the device.

### Initial engineering targets

These are design targets and are not published benchmark claims:

```yaml
target_device: jetson-orin-nano-8gb
offline_required: true
peak_device_memory_gb: 6.5
p95_decision_latency_ms: 1500
structured_output_validity: 0.99
critical_safety_violations: 0
continuous_stability_minutes: 30
```

Measured values will replace these targets only after reproducible testing.

## NX Promotion Conditions

The Jetson Orin NX 16GB may become the primary deployment target only when documented testing shows that the Orin Nano cannot meet a mandatory requirement without unacceptable loss of capability or reliability.

Valid promotion conditions include:

- the required model and runtime cannot operate within the Nano memory limit;
- simultaneous modality adapters cause persistent out-of-memory failures;
- required model reduction causes unacceptable conformance accuracy loss;
- continuous operation is unstable on the Nano;
- required p95 decision latency cannot be reached;
- the final demonstration requires concurrent vision, language, and sensor pipelines beyond the Nano deployment envelope.

A move to the Orin NX must be documented in a new architecture decision record. ADR-001 must not be silently rewritten.

## Runtime Strategy

The deployment pipeline will evaluate:

1. an unmodified baseline runtime;
2. a fine-tuned model in higher precision;
3. an optimized quantized model;
4. an Arm64-compatible edge runtime;
5. constrained structured decoding;
6. event-driven model invocation;
7. deterministic pre-validation and safety validation.

The preferred runtime will be selected by measured compatibility and performance rather than branding or theoretical capability.

## Benchmarking Rules

All baseline and optimized comparisons must use:

- the same physical Jetson device;
- the same input dataset;
- the same State Capsule schema;
- the same evaluation contract;
- documented power mode;
- documented software versions;
- documented model and dataset hashes;
- repeated benchmark runs;
- p50 and p95 latency;
- peak memory;
- average power;
- energy per decision;
- functional quality and safety results.

Results from different hardware platforms must be presented as separate deployment profiles, not as direct optimization claims.

## Consequences

### Positive

- demonstrates optimization on a constrained Arm64 edge platform;
- strengthens the low-power and offline product narrative;
- provides a clear production deployment envelope;
- preserves the NX 16GB as a technically compatible scale-up option;
- separates model development from edge inference;
- enables honest and reproducible benchmark reporting.

### Trade-offs

- the Nano memory limit constrains model size and concurrent adapters;
- quantization may reduce model quality;
- multimodal configurations may require sequential rather than parallel execution;
- the Evidence Console must remain lightweight;
- every additional runtime component must be measured for memory and power impact.

## Final Architecture Position

```text
DGX Spark
Training / Fine-tuning / Distillation / ModelDelta
                         ↓
              Exported Deployment Package
                         ↓
Jetson Orin Nano 8GB
Primary Offline Edge Target
                         ↓
Expected State + Observed State + History + Policy
                         ↓
StateDelta → Evidence → Safety Validation → Action

Jetson Orin NX 16GB
Extended Validation and Scale-Up Target
```

## Review Trigger

This decision must be reviewed when:

- the selected student model has been benchmarked;
- the first multimodal adapter is operational;
- Nano memory and latency results are available;
- the 30-minute stability test is complete;
- the competition demonstration scope is frozen.
