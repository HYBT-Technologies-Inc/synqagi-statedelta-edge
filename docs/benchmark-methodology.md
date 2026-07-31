# Benchmark Methodology

## Rules

- Compare baseline and optimized implementations on the same physical target device.
- Record device, JetPack/L4T, CUDA, TensorRT, Python, power mode, model revision, dataset hash, and code commit.
- Use warm-up runs followed by repeated timed runs.
- Report p50 and p95 latency, peak memory, average power, energy per decision, quality, valid-output rate, and safety results.
- Separate hardware-profile comparisons from optimization claims.
- Publish raw machine-readable results together with summaries.

## Reference Bootstrap Benchmark

`benchmarks/run_benchmark.py` measures the deterministic reference pipeline. It is not a model-inference benchmark and must not be described as one.
