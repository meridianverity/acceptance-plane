# Acceptance Boundary Public-Evaluation Profile v1

This profile gives reviewers a compact, runnable model for the public Acceptance Plane thesis.

## Decision vocabulary

- `ACCEPT`: current, scoped, target-bound, non-revoked, non-replayed evidence is sufficient.
- `HOLD`: evidence is incomplete, stale, or requires step-up review.
- `REFUSE`: evidence fails, authority fails, target binding fails, or replay is detected.

## Required public-eval evidence

A scenario card must include:

1. `action`: actor, operation, service, target, risk, requested time, and optional parameters.
2. `authority`: delegated subject, scopes, expiry, revocation state, and maximum risk.
3. `evidence`: identity validity, runtime attestation, measurement, target binding, freshness window, nonce, approval state, transparency state, and policy digest binding.
4. `policy`: policy identifier, version, trusted measurements, and profile flags.

## Fail-closed ordering

The reference evaluator is intentionally conservative:

1. malformed or incomplete cards hold;
2. identity, authority, scope, target, policy, and replay failures refuse;
3. missing attestation, stale evidence, missing approval, excessive risk, and missing transparency proof hold;
4. only fully sufficient evidence accepts.

## Digest profile

The public-eval profile uses deterministic JSON bytes with sorted keys and no insignificant whitespace, then SHA-256 digests for:

- action digest;
- evidence digest;
- policy digest;
- receipt-core digest;
- public-eval result digest;
- Merkle leaf and node digests.

This is a constrained public-eval canonicalization profile, not a complete JSON canonicalization standard.
