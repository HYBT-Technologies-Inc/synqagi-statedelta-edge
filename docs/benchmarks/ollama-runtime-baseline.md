# Ollama Model Runtime Baseline

## Classification

Local structured-output model-inference baseline for the
SYNQAGI StateDelta interpretation layer.

This is not a deterministic pipeline, Jetson Orin, TensorRT-LLM,
board-power, fine-tuned model, or competition benchmark.

## Execution Record

- Timestamp UTC: 2026-07-31T21:29:07.784323Z
- Repository commit recorded during execution: 1505083882c61d3c38b75e42223e280388a95b75
- Benchmark runner merged in commit: bdef1b6
- Runner: benchmarks/run_ollama_baseline.py
- Model: llama3.1:8b
- Ollama: ollama version is 0.20.4
- Warm-up requests: 1
- Measured requests: 5

## Runtime Environment

- System: NVIDIA DGX Spark
- Architecture: aarch64
- GPU: NVIDIA GB10
- CUDA runtime: 13.0
- Unified memory: approximately 121 GiB
- Ollama processor allocation: 100% GPU
- Loaded model footprint: 5.5 GB
- Context length: 4096
- Temperature: 0
- Seed: 42

## Test State

- Expected maximum vibration growth: 8.0 percent
- Observed vibration growth: 14.0 percent
- Allowed actions: CONTINUE, REDUCE_LOAD, STOP
- Deterministic expected action: REDUCE_LOAD

## Model Result

- Conformance: FAIL
- State: OUT_OF_TOLERANCE
- Severity: HIGH
- Recommended action: STOP
- Human review required: true

## Runtime Results

| Metric | Result |
|---|---:|
| Measured requests | 5 |
| Minimum wall latency | 2.744252 s |
| Median wall latency | 2.754106 s |
| Maximum wall latency | 2.858974 s |
| Mean generation speed | 42.284 tokens/s |
| Unique structured outputs | 1 |
| Fully repeatable | true |
| Policy alignment | false |

## Interpretation

The model produced schema-constrained and measurement-grounded
output identically across all five measured requests.

It correctly identified failed conformance, an out-of-tolerance
state, high severity, measured evidence, and the requirement for
human review.

The model recommended STOP while the deterministic StateDelta
policy required REDUCE_LOAD. The language-model recommendation
therefore remains advisory. The deterministic safety validator
is the final authority for operational action selection.

## Reproduction

Run:

    .venv/bin/python benchmarks/run_ollama_baseline.py \
      --model llama3.1:8b \
      --runs 5 \
      --warmup 1 \
      --expected-action REDUCE_LOAD \
      --output benchmarks/results/llama31-8b-structured-baseline.json

Raw JSON results remain local under benchmarks/results and are
excluded from Git.

## Limitations

- Specific to the recorded model, prompt, schema, and runtime.
- Does not establish correctness on a broad evaluation dataset.
- Does not measure board-level power consumption.
- Does not represent Jetson Orin deployment performance.
- Does not represent TensorRT-LLM optimization.
- Does not represent a fine-tuned SYNQAGI model.
