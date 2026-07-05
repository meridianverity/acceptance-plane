"""Deterministic Ed25519 profile for public evaluation receipts.

The private key is intentionally deterministic and public-evaluation only.  It
must never be reused as a production trust root.
"""
from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except Exception as exc:  # pragma: no cover - exercised only without dependency
    ed25519 = None  # type: ignore[assignment]
    serialization = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

PROFILE = "AP-ED25519-PUBLIC-EVAL-v1"
SEED_CONTEXT = b"Acceptance Plane public evaluation Ed25519 seed v1.0.2"


class CryptoUnavailable(RuntimeError):
    """Raised when the optional Ed25519 backend is unavailable."""


def _require_backend() -> None:
    if ed25519 is None:
        raise CryptoUnavailable(f"cryptography Ed25519 backend is unavailable: {_IMPORT_ERROR}")


def seed() -> bytes:
    return hashlib.sha256(SEED_CONTEXT).digest()


def private_key():
    _require_backend()
    return ed25519.Ed25519PrivateKey.from_private_bytes(seed())


def public_key_bytes() -> bytes:
    _require_backend()
    return private_key().public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def public_key_b64() -> str:
    return base64.b64encode(public_key_bytes()).decode("ascii")


def sign(message: bytes) -> str:
    _require_backend()
    return base64.b64encode(private_key().sign(message)).decode("ascii")


def verify(message: bytes, signature_b64: str, public_key_b64_value: str | None = None) -> bool:
    _require_backend()
    key_bytes = base64.b64decode(public_key_b64_value or public_key_b64())
    signature = base64.b64decode(signature_b64)
    key = ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)
    key.verify(signature, message)
    return True


@dataclass(frozen=True)
class PublicEvalKey:
    profile: str
    public_key_base64: str
    seed_sha256: str
    production_use: bool = False


def public_eval_key() -> dict[str, object]:
    return {
        "profile": PROFILE,
        "public_key_base64": public_key_b64(),
        "seed_sha256": hashlib.sha256(seed()).hexdigest(),
        "production_use": False,
        "warning": "Deterministic public-eval key only; not a production trust root.",
    }
