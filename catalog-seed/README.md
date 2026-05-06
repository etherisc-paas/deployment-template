# Catalog seed files

Deployment-owned artifacts (Specifications, Offerings, parties) land here as versioned JSON or YAML.

## Conventions

- **Format:** match the schema versions referenced by your deployed framework + products (Phase 2+ publishes the exact schemas).
- **Loading:** first-run ingestion should be a CLI entry (to be wired when `loadProduct` and catalog ingestion exist); the template ships empty to show folder placement only.
- **Versioning:** keep a `manifest.json` in later phases listing files and target environments.

Nothing is loaded automatically in Phase 1 — this folder exists so Phase 7 deployments know where artifacts belong.
