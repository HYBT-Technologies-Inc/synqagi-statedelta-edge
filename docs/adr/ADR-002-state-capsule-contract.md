# ADR-002: Universal State Capsule Contract

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** AISC TECHNOLOGIES LTD / HYBT Technologies
- **Project:** SYNQAGI — StateDelta Edge

## Context

SYNQAGI StateDelta Edge must compare what is required, expected, permitted, normal, or previously recorded with what is actually observed.

The comparison is not limited to two images or two moments in time.

The expected side may represent:

- a previous state;
- a technical specification;
- a quality standard;
- a target value;
- a permitted tolerance envelope;
- a maintenance baseline;
- a required construction stage;
- an operating policy;
- an original AI-model capability contract.

The observed side may contain:

- temperature;
- vibration;
- pressure;
- electrical current;
- voltage;
- load;
- sound;
- images;
- video-derived features;
- equipment telemetry;
- controller logs;
- process results;
- AI-model evaluation results;
- other locally acquired or simulated measurements.

A stable universal contract is required so that different modality adapters can use the same StateDelta reasoning, evidence, safety, and action pipeline.

## Decision

SYNQAGI will use a versioned object called a **State Capsule** as the canonical input to the StateDelta decision pipeline.

A State Capsule represents:

```text
Expected State
      +
Observed State
      +
History
      +
Context
      +
Policies and Tolerances
      +
Data Provenance
```

The State Capsule is modality-independent.

Raw sensor, image, audio, telemetry, or model-evaluation data must first be processed by a modality adapter into normalized measurements, features, events, or references.

## Core Principle

In SYNQAGI, “before and after” means:

> required, expected, baseline, permitted, or previous state  
> compared with  
> measured, observed, completed, or evaluated state.

The term does not imply that both sides must be historical observations.

Examples:

```text
Technical specification → manufactured result
Construction requirement → completed work
Normal motor profile → current telemetry
Maintenance baseline → degradation trend
Original AI model → fine-tuned AI model
Safety policy → proposed action
```

## Canonical State Capsule

The canonical structure is:

```json
{
  "contract_version": "1.0.0",
  "capsule_id": "cap-000001",
  "timestamp": "2026-08-01T00:00:00Z",
  "subject": {
    "id": "motor-07",
    "type": "industrial_motor",
    "profile": "predictive-maintenance"
  },
  "expected": {
    "requirements": {},
    "tolerances": {},
    "baseline": {}
  },
  "observed": {
    "measurements": {},
    "features": {},
    "events": {}
  },
  "history": {
    "window": [],
    "summary": {}
  },
  "context": {
    "operating_mode": null,
    "environment": {},
    "task": null
  },
  "policies": {
    "conformance": [],
    "safety": [],
    "allowed_actions": []
  },
  "provenance": {
    "source_type": null,
    "adapter": null,
    "adapter_version": null,
    "data_hash": null
  },
  "privacy": {
    "processing": "local",
    "raw_data_retained": false,
    "export_allowed": false
  }
}
```

## Required Fields

Every valid State Capsule must include:

- `contract_version`;
- `capsule_id`;
- `subject`;
- `expected`;
- `observed`;
- `policies`;
- `provenance`;
- `privacy`.

`history` and `context` may be empty, but their objects must remain present to preserve a stable interface.

## Expected State

The `expected` object may contain one or more of:

- exact required values;
- numeric ranges;
- categorical requirements;
- spatial requirements;
- expected process stages;
- permitted deviations;
- baseline distributions;
- retained AI capabilities;
- safety constraints;
- quality acceptance criteria.

An expected state must identify the origin of each material requirement whenever possible.

## Observed State

The `observed` object contains normalized evidence produced by an approved modality adapter.

Examples:

```json
{
  "measurements": {
    "temperature_c": 67.0,
    "load_percent": 79.0,
    "vibration_growth_percent": 14.0
  },
  "features": {
    "trend": "increasing"
  },
  "events": {
    "threshold_crossed": true
  }
}
```

Raw observations may remain on the local device and do not need to be embedded in the capsule.

## StateDelta Output Contract

StateDelta must return a structured decision object.

```json
{
  "decision_version": "1.0.0",
  "capsule_id": "cap-000001",
  "conformance": "FAIL",
  "state": "DEGRADING",
  "severity": "HIGH",
  "delta": [
    {
      "path": "observed.measurements.vibration_growth_percent",
      "expected": {
        "maximum": 8.0
      },
      "observed": 14.0,
      "deviation": 6.0
    }
  ],
  "evidence": [
    {
      "type": "measured_threshold_violation",
      "source": "telemetry-adapter",
      "reference": "vibration_growth_percent"
    }
  ],
  "recommended_action": "REDUCE_LOAD_AND_INSPECT",
  "confidence": 0.94,
  "uncertainty": [],
  "requires_human_review": false
}
```

## Decision Vocabulary

The initial conformance vocabulary is:

```text
PASS
PASS_WITH_WARNING
INSUFFICIENT_EVIDENCE
FAIL
CRITICAL_FAIL
```

The initial state vocabulary is:

```text
NORMAL
CHANGED
DEGRADING
OUT_OF_TOLERANCE
UNSAFE
UNKNOWN
```

Profiles may define additional domain-specific labels, but they must map to the canonical vocabulary.

## Evidence Requirements

A decision must not rely only on an unsupported natural-language conclusion.

Every material deviation must reference at least one of:

- a measured value;
- a detected feature;
- a recorded event;
- a historical trend;
- a deterministic rule result;
- an evaluation metric;
- a source-data hash;
- a local evidence artifact.

The system must distinguish:

```text
MEASURED
DERIVED
MODEL_INFERRED
POLICY_DETERMINED
UNKNOWN
```

Model-inferred conclusions must not be presented as directly measured facts.

## Safety Authority

The StateDelta model may recommend an action, but it does not have final authority over physical execution.

The deterministic safety validator must:

- verify that the action is permitted;
- verify required evidence;
- apply emergency rules;
- reject malformed or unsupported commands;
- select a safe fallback when confidence or evidence is insufficient;
- prevent the model from overriding a hard safety limit.

Example:

```text
Model recommendation: CONTINUE
Hard safety rule: emergency temperature exceeded
Final validated action: STOP
```

## Privacy Requirements

State Capsules must support local privacy-preserving execution.

Default policy:

```yaml
processing: local
raw_data_retained: false
export_allowed: false
network_required: false
```

Profiles may explicitly permit retention or export, but these settings must not be silently enabled.

For camera, audio, industrial, or model-evaluation data, the preferred exported artifact is a normalized result, evidence reference, or cryptographic hash rather than the full raw input.

## ModelDelta Compatibility

ModelDelta will use the same State Capsule contract.

Example mapping:

```text
Subject:
Fine-tuned AI model

Expected:
Target capability gain
Original capability retention
Safety limits
Structured-output requirements

Observed:
Paired evaluation metrics
Regression results
Robustness results
Latency and memory measurements

Decision:
PASS
PASS WITH CONDITIONS
RETRAIN
REJECT FOR RELEASE
```

This confirms that StateDelta and ModelDelta share one expected-to-observed architecture.

## Adapter Responsibilities

Each modality adapter must:

1. validate its input;
2. normalize units and field names;
3. record adapter name and version;
4. preserve source provenance;
5. identify missing or unreliable data;
6. avoid inventing measurements;
7. produce a valid State Capsule fragment;
8. respect the active privacy policy.

Adapters must not independently perform final safety approval.

## Versioning

The State Capsule contract follows semantic versioning.

```text
MAJOR
Breaking schema or semantic change

MINOR
Backward-compatible field or capability addition

PATCH
Clarification or non-breaking correction
```

A runtime must reject unsupported major contract versions rather than silently interpreting them.

## Consequences

### Positive

- one reasoning contract supports multiple industries and modalities;
- the project is not tied to cameras or any single sensor;
- ModelDelta and physical StateDelta share the same architecture;
- decisions become traceable and auditable;
- privacy rules travel with each capsule;
- adapters can be developed independently;
- benchmark inputs become reproducible.

### Trade-offs

- every adapter must normalize its data correctly;
- schema governance becomes a core responsibility;
- domain profiles still require specific requirements and tolerances;
- an SLM cannot replace deterministic measurement and safety logic;
- incomplete provenance reduces the strength of the final evidence.

## Final Position

SYNQAGI is not a generic image-comparison application.

It is a universal local expected-to-observed intelligence system:

```text
Requirement / Baseline / Previous State
                    ↓
               State Capsule
                    ↑
Measurement / Observation / Evaluation
                    ↓
          Deterministic Delta Evidence
                    ↓
        Contextual StateDelta Interpretation
                    ↓
           Deterministic Safety Validation
                    ↓
      Decision / Alert / Inspection / Control
```

## Review Trigger

This decision must be reviewed when:

- the first JSON Schema is implemented;
- the telemetry adapter is operational;
- the first vision or multimodal adapter is operational;
- ModelDelta produces its first change certificate;
- a breaking contract change is proposed.
