# Operations (pre-MVP baseline)

## Deploy

1. Fork [deployment-template](https://github.com/etherisc-paas/deployment-template) (this repo's published location) or clone from your monorepo workspace.
2. Copy `config/*.example` to real paths (`deployment-config.json`, mounted `platform-app.json`, etc.).
3. Provide secrets via your platform (`config/secrets/` or env).
4. Build/push an image from `infrastructure/docker/Dockerfile` (after GitHub Packages auth) and point `docker-compose.yaml` at that tag, or keep the Phase 1 placeholder image for demos only.
5. On the host: `docker compose pull && docker compose up -d`.

## Roll back

Tag every release image. To roll back, reset `docker-compose.yaml` image digests (or compose `image:` pins) to the previous tag and run `docker compose up -d --no-build`.

## Backup / restore

Use `pg_dump` / `psql` against the Postgres service. See `scripts/backup.sh` and `scripts/restore.sh` for commented skeletons.

## Monitoring (baseline)

- Compose `healthcheck` blocks in `docker-compose.yaml` for Postgres and HTTP.
- Add external uptime checks and log sinks (Loki/Promtail) in Phase 7+ deployments.

## Related documentation

- [Deployment pattern (canonical) — saas-architecture](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/plans/deployment-pattern.md)
- [ADR 0042 — implementation landscape](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/adr/0042-product-framework-implementation-landscape-amended.md)
