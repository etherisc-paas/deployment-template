#!/usr/bin/env bash
# Lint every commit message in BASE..HEAD for required trailers (S0-T08).
# Usage: scripts/provenance/check_range.sh [base] [head]
set -euo pipefail
# INF-021: missing Task/Transcript warns. Malformed values still fail.
# TRAILER_MODE=fail restores a hard failure for a missing trailer.

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
  if err="$("$PY" "$LINT" --message "$msg" 2>&1)"; then
    echo "OK   $sha"
  else
    printf '%s\n' "$err" >&2
    if grep -q 'does not match' <<<"$err"; then
      echo "FAIL $sha" >&2
      failed=1
    elif [[ "${TRAILER_MODE:-warn}" == "warn" ]] && grep -q 'missing required trailer' <<<"$err"; then
      echo "WARN $sha" >&2
    else
      echo "FAIL $sha" >&2
      failed=1
    fi
  fi
done < <(git rev-list --no-merges "${BASE}..${HEAD}")

if [[ "$failed" -ne 0 ]]; then
  echo "commit-trailers: one or more commits failed the trailer check" >&2
  exit 1
fi
exit 0
