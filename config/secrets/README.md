# Secrets directory

Nothing except `.gitkeep` should be committed.

Real deployments place environment-specific values here (TLS keys, API tokens, database passwords)
or mount a secrets volume at runtime. Reference **names** of secrets in
`config/deployment-config.json` (integration slots) and resolve them to env vars or files in CI/CD.

Never log secret material. Prefer the platform secret store in production over plain files.
