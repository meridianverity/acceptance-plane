"""Deterministic JSON canonicalization used by the public eval profile."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(obj: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes.

    This is intentionally a constrained profile: JSON objects are sorted by key,
    no insignificant whitespace is emitted, and non-string floats are rejected by
    the scenario/profile validators.  It is not a full RFC 8785 implementation.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_json(obj: Any) -> str:
    return sha256_hex(canonical_json(obj))
