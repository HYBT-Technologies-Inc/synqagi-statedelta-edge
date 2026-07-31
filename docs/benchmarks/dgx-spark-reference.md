# DGX Spark Reference Benchmark

## Classification

This is a deterministic StateDelta reference-pipeline benchmark.

It is not:

- a model-inference benchmark;
- a Jetson Orin benchmark;
- a board-power benchmark;
- an Arm AI Optimization Challenge result.

## Execution Record

- Timestamp UTC: `2026-07-31T21:04:50Z`
- Git commit: `b2e7deca59264a6fa5f9893bc4c9daaebd373727`
- Capsule: `examples/predictive-maintenance/state-capsule.json`
- Iterations: `1000`
- Warm-up iterations: `100`
- Python: `3.12.3`

## Hardware and Software Environment

- System: NVIDIA DGX Spark
- Architecture: `aarch64`
- Operating system: Ubuntu `24.04.4 LTS`
- Kernel: `6.17.0-1014-nvidia`
- CPU cores: `20`
- CPU families: Arm Cortex-X925 and Cortex-A725
- GPU: NVIDIA GB10
- NVIDIA driver: `580.142`
- CUDA runtime: `13.0`
- CUDA compiler: `13.0.88`
- Unified system memory: approximately `121 GiB`

## Results

| Metric | Result |
|---|---:|
| Mean latency | `0.058761374 ms` |
| p50 latency | `0.058016 ms` |
| p95 latency | `0.061168 ms` |
| Minimum latency | `0.056928 ms` |
| Maximum latency | `0.138432 ms` |
| Python traced peak allocation | `34,213 bytes` |

## Interpretation

The result confirms that the deterministic rule, delta, evidence, and safety pipeline introduces negligible processing latency on the DGX Spark reference environment.

The result must not be used as evidence of model-inference performance or Jetson deployment performance.

Competition measurements will be performed separately on the same physical Jetson target before and after optimization, using documented power mode, model revision, dataset hash, and code commit.
