# Contributing

## Development Principles

- Preserve the expected-to-observed architecture.
- Do not present model-inferred claims as directly measured facts.
- Keep raw sensitive data local by default.
- Add deterministic safety checks for every executable action.
- Do not publish benchmark claims without reproducible evidence.
- Document licences for models, datasets, and dependencies.

## Local Checks

```bash
python -m unittest discover -s tests -v
python -m compileall src benchmarks
```

## Commits

Use clear conventional prefixes such as `feat:`, `fix:`, `docs:`, `test:`, `bench:`, and `legal:`.
