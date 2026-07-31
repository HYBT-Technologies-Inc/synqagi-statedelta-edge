# Architecture

## Control Flow

```text
Input source
  ↓
Modality adapter
  ↓
State Capsule validation
  ↓
Deterministic delta extraction
  ↓
Evidence classification
  ↓
Optional compact-model interpretation
  ↓
Deterministic safety validation
  ↓
Structured decision and action adapter
```

## Trust Boundary

Measured and deterministic results must remain distinguishable from model-inferred conclusions.

The compact model must not directly control low-level actuator signals. It may recommend only whitelisted high-level actions.

## Current Bootstrap

The current implementation provides the schema, deterministic delta engine, safety validator, ModelDelta evaluator, CLI, tests, examples, and benchmark scaffold. Model runtime adapters are intentionally deferred until device inventory and baseline measurements are complete.
