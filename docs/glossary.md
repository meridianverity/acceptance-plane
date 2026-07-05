# Glossary

This glossary supports the Acceptance Plane public architecture thesis and v1.0.1-public-eval overlay.

## Acceptance Plane

The architectural function that determines whether a specific autonomous AI action should be accepted by a protected system before impact, based on current, scope-bound, verifier-ready evidence at the acceptance boundary.

## Acceptance Boundary

The point where a proposed autonomous action may become a protected-system consequence.

## Action Envelope

A structured description of the action being attempted: actor, operation, service, target, risk, time, and parameters.

## Authority Envelope

The delegated authority being relied on: subject, scopes, expiry, revocation state, and risk ceiling.

## Evidence Envelope

The verifier-ready evidence available at the boundary, including identity validity, runtime attestation, target binding, freshness, nonce, approval state, transparency state, and policy digest binding.

## Policy Digest Binding

A deterministic hash binding evidence to the policy state that was evaluated.

## ACCEPT

The evidence is current, scoped, consistent, non-revoked, non-replayed, target-bound, and sufficient.

## HOLD

The evidence is incomplete, stale, ambiguous, high-risk, or requires step-up review. HOLD is not failure; it is a fail-closed pause when proof is not yet sufficient.

## REFUSE

The action is outside authority, mismatched, revoked, replayed, unverifiable, untrusted, or not bound to the intended target.

## Fail-Closed Autonomy

An operating posture where autonomous actions proceed when proof is sufficient, hold when proof is incomplete, and refuse when proof fails.

## Scenario Card

A compact JSON object used by the public-eval overlay to describe one proposed action, its authority, evidence, policy, and expected ACCEPT/HOLD/REFUSE result.

## Verifier-Ready Receipt

A structured record of what action was attempted, what evidence and policy state were evaluated, what decision was made, why, and under which boundary.

## Transparency Bundle

A public-eval Merkle tree over vector results, with selected inclusion proofs and a signed tree head.

## Public-Eval Key

A deterministic Ed25519 key used only to make the proof overlay locally reproducible. It is not a production trust root.

## Canonical Reference

Lee, Scott. Meridian Verity Group. (2026). **The Acceptance Plane: The Missing Trust Layer for Agentic AI Infrastructure** (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.20645907

Access is not authority. Permission is not proof. Execution is not acceptance.
