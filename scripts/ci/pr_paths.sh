#!/usr/bin/env bash
# Path classifier for ADR 0078 / P24-07 (Node/pnpm product repos).
# Usage: eval "$(bash scripts/ci/pr_paths.sh)"
# Customize path globs for the consumer repo; keep lane semantics.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BASE="${CI_DIFF_BASE:-}"
HEAD="${CI_DIFF_HEAD:-HEAD}"

if [ -z "${BASE}" ]; then
  if [ -n "${GITHUB_BASE_REF:-}" ]; then
    BASE="origin/${GITHUB_BASE_REF}"
  else
    BASE="origin/develop"
  fi
fi

if ! git rev-parse --verify --quiet "${BASE}" >/dev/null 2>&1; then
  git fetch --depth=1 origin "$(echo "${BASE}" | sed 's#^origin/##')" 2>/dev/null || true
fi

mapfile -t FILES < <(git diff --name-only "${BASE}...${HEAD}" 2>/dev/null || git diff --name-only "${BASE}" "${HEAD}" 2>/dev/null || true)

NEED_CODE=0
NEED_CI_META=0
NEED_DOCS_ONLY=1

for f in "${FILES[@]:-}"; do
  if [[ "$f" == .github/workflows/* || "$f" == scripts/ci/* ]]; then
    NEED_CI_META=1
    NEED_DOCS_ONLY=0
    continue
  fi
  if [[ "$f" == apps/* || "$f" == packages/* || "$f" == scripts/* ||
    "$f" == src/* || "$f" == migrations/* || "$f" == schemas/* ||
    "$f" == entities/* || "$f" == contract/* || "$f" == data/* ||
    "$f" == pnpm-lock.yaml || "$f" == package.json || "$f" == pnpm-workspace.yaml ||
    "$f" == turbo.json || "$f" == tsconfig.json || "$f" == tsconfig.*.json ||
    "$f" == eslint.config.* || "$f" == module.manifest.yaml ]]; then
    NEED_CODE=1
    NEED_DOCS_ONLY=0
    continue
  fi
  if [[ "$f" == docs/* || "$f" == *.md || "$f" == LICENSE* || "$f" == CHANGELOG* ]]; then
    continue
  fi
  NEED_CODE=1
  NEED_DOCS_ONLY=0
done

if [ "${#FILES[@]}" -eq 0 ]; then
  NEED_CODE=1
  NEED_DOCS_ONLY=0
fi

echo "NEED_CODE=${NEED_CODE}"
echo "NEED_CI_META=${NEED_CI_META}"
echo "NEED_DOCS_ONLY=${NEED_DOCS_ONLY}"
echo "CHANGED_COUNT=${#FILES[@]}"
