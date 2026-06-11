# FAQ

## Is the Acceptance Plane a product specification?

No. This package is a public architecture thesis, not a product specification, formal standard, API contract, compliance certification, legal opinion, patent claim chart, or implementation disclosure.

## Does this replace IAM, policy, attestation, confidential computing, encryption, or logs?

No. Those controls remain necessary. The Acceptance Plane describes the architectural function that binds relevant evidence to a specific action before protected system impact.

## Why not just log agent actions and review later?

For many high-consequence actions, review after impact is too late. The Acceptance Plane focuses on evidence-bound acceptance before the action becomes real.

## Does every AI action need the same level of proof?

No. Low-risk actions may use lightweight controls. High-consequence actions require stronger evidence, clearer scope, and fail-closed behavior.

## Where should the acceptance boundary live?

Placement depends on system design and risk: agent runtime, gateway, policy layer, application boundary, data layer, or deeper infrastructure boundary. The function should exist wherever autonomous action may affect a protected system.

## Does Zenodo/GitHub publication prove patent priority?

No. Zenodo/GitHub can create public, citable, timestamped provenance. It does not replace patent filing strategy or legal priority analysis.


## Canonical Reference

Canonical DOI: https://doi.org/10.5281/zenodo.20645907
