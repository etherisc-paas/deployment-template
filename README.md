# deployment-template

Forkable starting point for a **customer deployment** repository: thin wrapper that selects
`@etherisc/framework` + one or more `@etherisc/product-*` packages, supplies `deployment-config.json`,
catalog seeds, and runs the **docker-compose** topology from the implementation landscape (Postgres +
HTTP `app` + `app-worker`).

Architectural rationale: [ADR 0042](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/adr/0042-product-framework-implementation-landscape-amended.md).

## Forking for a real deployment

1. Create a new repo (GitHub: *Use this template* once published, or clone and push to a new origin).
2. Rename `package.json` `"name"` to `@etherisc/<your-deployment>`.
3. Copy `config/*.example` to committed/runtime paths you expect (`deployment-config.json`, secrets layout).
4. Replace the placeholder container entrypoint (`infrastructure/docker/entrypoint.mjs`) with the real
   **platform-app** image pipeline (published image or `pnpm` multi-stage build once packages exist).
5. Copy `.env.example` → `.env` and fill integration env vars referenced from `deployment-config.json`.
6. Read the canonical [deployment pattern](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/plans/deployment-pattern.md) and [deployment repository pattern](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/plans/deployment-repo-pattern.md) documents.

## Multi-product tenancy

`config/deployment-config.example.json` includes a `products` array. For more than one product, list
each `@etherisc/product-*` entry (see `"_multiProductExample"` in that file for a second product).

`platform-app` consumption (git tag vs workspace) follows [P1-9](https://github.com/etherisc-paas/saas-architecture/blob/develop/docs/plans/tracks/track-1-product-framework/phases/phase-1/P01-09-investigation-data-layer-integration.md) outcomes — add it to `package.json` when you wire the real host app.

## Smoke test (three containers)

Requires Docker 24+ with Compose v2.

```bash
cp .env.example .env   # defaults work for localhost
docker compose up --build
```

Expect Postgres healthy, HTTP 200 on `http://localhost:3000/health`, worker logs streaming ticks.
`Ctrl+C` stops the stack; `docker compose down -v` removes the named volume.

`pnpm install` against GitHub Packages optional for Phase 1 — placeholder image runs without published tarballs.

## Layout

| Path | Purpose |
| --- | --- |
| `docker-compose.yaml` | Three-service baseline (postgres, app, app-worker). |
| `config/` | Examples for platform-app settings, deployment manifest (`products` array), chart of accounts, secrets dir. |
| `catalog-seed/` | Where versioned catalog artifacts will live (empty in Phase 1). |
| `infrastructure/docker/` | Dockerfile + temporary Node entrypoint for smoke tests. |
| `scripts/` | Commented ops placeholders (`deploy`, `backup`, `restore`). |

See `docs/operations.md` for deploy / rollback / backup expectations.
