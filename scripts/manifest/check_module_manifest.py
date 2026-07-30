#!/usr/bin/env python3
"""P22 Stage-1 exit — validate module.manifest.yaml (blocking gate).

Uses the vendored JSON Schema at data/module.manifest.schema.json
(source of truth: @etherisc-paas/manifest). Exit 0 on OK, 1 on fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "path",
        nargs="?",
        default="module.manifest.yaml",
        type=Path,
        help="Path to module.manifest.yaml (default: ./module.manifest.yaml)",
    )
    p.add_argument(
        "--schema",
        type=Path,
        default=None,
        help="Schema path (default: <repo>/data/module.manifest.schema.json)",
    )
    args = p.parse_args(argv)

    repo_root = Path.cwd()
    schema_path = args.schema or (repo_root / "data" / "module.manifest.schema.json")
    manifest_path = args.path if args.path.is_absolute() else repo_root / args.path

    if not manifest_path.is_file():
        print(f"manifest-check: FAIL — missing {manifest_path}", file=sys.stderr)
        return 1
    if not schema_path.is_file():
        print(f"manifest-check: FAIL — missing schema {schema_path}", file=sys.stderr)
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("manifest-check: FAIL — manifest is not a mapping", file=sys.stderr)
        return 1

    try:
        Draft202012Validator(schema).validate(data)
    except ValidationError as exc:
        print(f"manifest-check: FAIL — {manifest_path}", file=sys.stderr)
        print(f"  path: {list(exc.absolute_path) or ['/']}", file=sys.stderr)
        print(f"  {exc.message}", file=sys.stderr)
        return 1

    print(f"manifest-check: OK — {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
