# Superset Strategy: Acceptance Plane, Permit Receipt, and HaltSeal

This note explains how the Acceptance Plane can sit above concrete receipt/gateway proof mechanisms without overclaiming.

## Positioning

- Acceptance Plane: architectural function that decides whether an autonomous action becomes a protected consequence before impact.
- Permit Receipt: a possible action-level receipt and authorization proof mechanism.
- HaltSeal: a possible gateway proof-pack and fail-closed verification mechanism.

The hardened Acceptance Plane package is stronger as a category artifact when it does not compete with those mechanisms. It frames them as examples of how an acceptance boundary can be made verifiable.

## What this overlay adds

Compared with a thesis-only package, the overlay adds:

1. runnable ACCEPT/HOLD/REFUSE scenario vectors;
2. deterministic receipt digests;
3. signed public-eval proof receipt;
4. signed Merkle transparency bundle;
5. independent recomputation script;
6. shape-only Envoy, OPA, and Kubernetes adapter sketches;
7. release archive verification.

## Next step to exceed a single proof pack

The highest-leverage next step is a multi-implementation interop matrix:

```text
Python evaluator -> canonical action digest -> receipt digest
Go verifier      -> same canonical action digest -> same receipt digest
TypeScript demo  -> same canonical action digest -> same receipt digest
OPA adapter      -> same ACCEPT/HOLD/REFUSE boundary outcome
```

That would move the project from a strong public-eval artifact to an interop-ready reference profile.
