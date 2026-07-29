"""Commit-trailer parse / lint (S0-T08 / P21-08).

Validates git commit messages against ``data/provenance/commit-trailers.v1.yaml``.
Mainline commits must carry ``Task:`` and ``Transcript:``.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_TRAILER_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):\s*(.+?)\s*$")
_DEFAULT_TAXONOMY = (
    Path(__file__).resolve().parents[2] / "data" / "provenance" / "commit-trailers.v1.yaml"
)


@dataclass(frozen=True)
class TrailerLintResult:
    ok: bool
    trailers: dict[str, str]
    errors: tuple[str, ...]


def load_taxonomy(path: Path | None = None) -> dict[str, Any]:
    target = path or _DEFAULT_TAXONOMY
    raw = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"trailer taxonomy must be a mapping: {target}")
    return raw


def extract_trailers(message: str) -> dict[str, str]:
    """Return last-occurrence map of ``Key: value`` trailers from a commit message.

    Git trailers live in the message body after a blank line. We accept trailers
    anywhere after the subject line so HEREDOC bodies remain valid.
    """

    lines = message.replace("\r\n", "\n").split("\n")
    if not lines:
        return {}
    # Skip subject; scan the rest (and subject if it somehow carries trailers).
    body_lines = lines[1:] if len(lines) > 1 else []
    found: dict[str, str] = {}
    for line in body_lines:
        m = _TRAILER_LINE.match(line)
        if m:
            found[m.group(1)] = m.group(2)
    return found


def lint_message(
    message: str,
    *,
    taxonomy: Mapping[str, Any] | None = None,
    require_mainline: bool = True,
) -> TrailerLintResult:
    tax = dict(taxonomy or load_taxonomy())
    keys_decl = tax.get("keys") or {}
    trailers = extract_trailers(message)
    errors: list[str] = []

    if require_mainline:
        required = list(tax.get("mainline_required") or ["Task", "Transcript"])
        for key in required:
            if key not in trailers or not str(trailers[key]).strip():
                errors.append(f"missing required trailer {key}:")

    for key, value in trailers.items():
        decl = keys_decl.get(key)
        if decl is None:
            # Unknown keys are allowed (git Signed-off-by etc.) but not validated.
            continue
        pattern = decl.get("value_pattern")
        if isinstance(pattern, str) and not re.fullmatch(pattern, value):
            errors.append(f"trailer {key}: value {value!r} does not match {pattern}")

    return TrailerLintResult(ok=not errors, trailers=trailers, errors=tuple(errors))


def aggregate_squash_message(messages: list[str]) -> str:
    """Approximate GitHub ``COMMIT_MESSAGES`` squash body aggregation."""

    parts: list[str] = []
    for idx, msg in enumerate(messages, start=1):
        text = msg.strip()
        if not text:
            continue
        parts.append(f"* commit {idx}:\n\n{text}")
    return "\n\n".join(parts)


def trailers_survive_squash(messages: list[str]) -> TrailerLintResult:
    """Lint the aggregated squash message; required trailers must still parse."""

    return lint_message(aggregate_squash_message(messages), require_mainline=True)


def format_injection_block(env: Mapping[str, str], taxonomy: Mapping[str, Any]) -> str:
    """Build trailer lines from env vars named in the taxonomy ``env_injection`` map."""

    mapping = dict(taxonomy.get("env_injection") or {})
    lines: list[str] = []
    for key, env_name in mapping.items():
        val = (env.get(env_name) or "").strip()
        if val:
            lines.append(f"{key}: {val}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint git commit messages for provenance trailers")
    parser.add_argument(
        "--taxonomy",
        type=Path,
        default=None,
        help="Path to commit-trailers.v1.yaml (default: repo data/provenance/…)",
    )
    parser.add_argument(
        "--message-file",
        type=Path,
        help="Commit message file (commit-msg hook passes $1)",
    )
    parser.add_argument(
        "--message",
        help="Commit message text (alternative to --message-file)",
    )
    parser.add_argument(
        "--allow-empty-trailers",
        action="store_true",
        help="Do not require Task/Transcript (hook dry-run / non-mainline)",
    )
    args = parser.parse_args(argv)

    if args.message_file is None and args.message is None:
        parser.error("pass --message-file or --message")

    text = args.message if args.message is not None else args.message_file.read_text(encoding="utf-8")
    tax = load_taxonomy(args.taxonomy)
    result = lint_message(text, taxonomy=tax, require_mainline=not args.allow_empty_trailers)
    if result.ok:
        return 0
    for err in result.errors:
        sys.stderr.write(f"commit-trailers: {err}\n")
    sys.stderr.write(
        "commit-trailers: mainline commits need Task: Pnn-nn and "
        "Transcript: <run_id|human/…> (see data/provenance/commit-trailers.v1.yaml)\n",
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
