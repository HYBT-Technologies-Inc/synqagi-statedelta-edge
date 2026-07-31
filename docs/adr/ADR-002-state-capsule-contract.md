# ADR-002: Universal State Capsule Contract

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** AISC TECHNOLOGIES LTD / HYBT Technologies
- **Project:** SYNQAGI — StateDelta Edge

## Decision

SYNQAGI uses a versioned **State Capsule** as the canonical input to the StateDelta pipeline.

“Before and after” means:

> required, expected, baseline, permitted, or previous state compared with measured, observed, completed, or evaluated state.

It is not limited to two images or two moments in time.

```text
Technical specification → manufactured result
Construction requirement → completed work
Normal motor profile → current telemetry
Maintenance baseline → degradation trend
Original AI model → fine-tuned AI model
Safety policy → proposed action
```

The State Capsule is modality-independent. Raw sensor, image, audio, telemetry, or model-evaluation data is normalized by an adapter before entering the common evidence, interpretation, safety, and action pipeline.

## Required Contract Objects

- `contract_version`
- `capsule_id`
- `subject`
- `expected`
- `observed`
- `history`
- `context`
- `policies`
- `provenance`
- `privacy`

## Safety Authority

The model may recommend an action, but deterministic safety validation has final authority over physical execution.

## Versioning

The State Capsule contract follows semantic versioning. Runtimes must reject unsupported major versions.
