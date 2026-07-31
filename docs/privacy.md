# Privacy Architecture

Default policy:

```yaml
processing: local
raw_data_retained: false
export_allowed: false
network_required: false
```

Adapters should export normalized evidence, references, or cryptographic hashes instead of raw images, audio, telemetry, or model-evaluation content whenever the raw input is unnecessary.

Privacy configuration must travel with each State Capsule and must not be silently relaxed.
