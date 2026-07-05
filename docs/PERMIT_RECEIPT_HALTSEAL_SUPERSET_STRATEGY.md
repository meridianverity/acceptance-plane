# Public Relationship Note: Acceptance Plane, Permit Receipt, and HaltSeal

This note is intentionally public-safe. It explains conceptual layering without disclosing private licensing strategy, partner mappings, production deployment details, claim charts, evidence-of-use material, or confidential implementation mechanisms.

## Public positioning

- Acceptance Plane: the architectural function that decides whether an autonomous action becomes accepted impact at a protected boundary.
- Permit Receipt: an example of an action-level authorization and receipt proof pattern.
- HaltSeal: an example of a gateway-level fail-closed proof and verification pattern.

The Acceptance Plane does not depend on any one concrete receipt or gateway mechanism. It provides the category-level boundary: action acceptance before impact. Concrete proof systems can instantiate that boundary in different environments.

## What remains deliberately out of scope

This public package does not include:

- private licensing analysis;
- patent claim charts;
- evidence-of-use mapping;
- customer or partner architectures;
- production enforcement pipelines;
- live payment, wallet, PSP, or regulated rails;
- production keys or production trust roots;
- confidential commercial terms.

## Public-eval contribution

The public-eval overlay shows that an acceptance-boundary artifact can be reviewed by deterministic vectors, receipt digests, a signed proof receipt, a transparency bundle, independent recomputation, and release archive verification.

That is enough for public technical review without revealing private commercialization or deployment strategy.
