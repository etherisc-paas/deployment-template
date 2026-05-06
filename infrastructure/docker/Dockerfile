# syntax=docker/dockerfile:1
#
# Stage `deps`: when @etherisc packages are available and NODE_AUTH_TOKEN is set, install here and
# copy node_modules into the runtime image. For fork smoke tests, this stage is optional.
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json ./
# RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Minimal runtime used for Phase 1 smoke tests (no registry access required).
FROM node:22-alpine AS runtime
WORKDIR /app
COPY infrastructure/docker/entrypoint.mjs ./entrypoint.mjs
# Once `deps` succeeds: COPY --from=deps /app/node_modules ./node_modules
EXPOSE 3000
USER node
CMD ["node", "/app/entrypoint.mjs"]
