#!/usr/bin/env bash
# Lint every commit message in BASE..HEAD for required trailers (S0-T08).
# Usage: scripts/provenance/check_range.sh [base] [head]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
BASE="${1:-origin/develop}"
HEAD="${2:-HEAD}"
PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY=python3
fi
LINT="${ROOT}/scripts/provenance/commit_trailers.py"

if ! git merge-base --is-ancestor "$BASE" "$HEAD" 2>/dev/null; then
  echo "commit-trailers: base ($BASE) is not an ancestor of head ($HEAD)" >&2
  echo "commit-trailers: refusing to lint — check CI fetch depth (shallow base fetch breaks reachability)" >&2
  exit 1
fi

failed=0
while IFS= read -r sha; do
  [[ -z "$sha" ]] && continue
  msg="$(git log -1 --format=%B "$sha")"
  if ! "$PY" "$LINT" --message "$msg"; then
    echo "FAIL $sha" >&2
    failed=1
  else
    echo "OK   $sha"
  fi
done < <(git rev-list --no-merges "${BASE}..${HEAD}")

if [[ "$failed" -ne 0 ]]; then
  echo "commit-trailers: one or more commits missing Task:/Transcript:" >&2
  exit 1
fi
exit 0
