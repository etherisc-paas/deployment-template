# CI templates (ADR 0078 / P24-07 Wave 3)

Scaffold copies for new product apps. Same freeze as
`saas-architecture/scripts/ci/templates/`.

| Path | Purpose |
| --- | --- |
| `scripts/ci/pr_paths.sh` | Path classifier (copy into app; adjust globs) |
| `docs/ci/classify-job.yml.snippet` | Classify job to paste into `ci.yml` |
| `.github/workflows/compliance-nightly.yml` | L4 only — no `pull_request` |
