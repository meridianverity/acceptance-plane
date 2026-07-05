"""Public-evaluation helpers for the Acceptance Plane proof overlay.

This package is intentionally small and deterministic.  It is not a product
implementation, standard, certification framework, or patent claim map.  It is a
reviewable reference evaluator for scenario cards used in the public proof
bundle.
"""

from .canonical import canonical_json, sha256_hex
from .evaluator import evaluate_scenario, evaluate_vectors, EvaluationError

__all__ = [
    "canonical_json",
    "sha256_hex",
    "evaluate_scenario",
    "evaluate_vectors",
    "EvaluationError",
]
