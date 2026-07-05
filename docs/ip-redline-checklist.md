# IP Redline Checklist

## Core principle

**Publish the category. Protect the mechanism.**

This checklist is designed to keep the public package at the architecture-thesis level while avoiding unnecessary implementation disclosure.

## Public-safe

- Acceptance Plane definition.
- High-level rationale for action acceptance.
- Public workflow: agent proposal -> identity -> runtime -> policy -> scope/freshness/revocation -> acceptance decision -> receipt.
- Conceptual diagrams.
- High-level evidence categories.
- Public examples: coding, finance, healthcare, enterprise data, cloud/platform workflows.
- Receipt concept at the category level.
- Claims style guide.

## Hold back

- Exact API schema.
- Full evidence object model.
- Cryptographic binding method.
- Enforcement pipeline.
- Runtime enforcement internals.
- DPU, accelerator, memory-boundary, or fabric-specific claim maps.
- Partner-specific architectures.
- Deployment topology for a real partner.
- Unpublished patent claim language.
- Scoring, revocation, freshness, target-binding, or replay implementation logic.

## Forbidden public claims

Do not claim:

- unsupported absolute priority claims without formal prior-art/trademark/legal review.
- "patent priority" from Zenodo/GitHub publication alone.
- "formal standard" unless there is an actual standards-body process.
- "compliance certified" unless a certification exists.
- "guarantees safety" or "prevents all unauthorized AI actions."

## Safer public claims

Use:

- "MVG is publishing a public architecture thesis."
- "One way to describe this missing architectural function is the Acceptance Plane."
- "This release provides a public, citable category reference."
- "Identity, attestation, policy, and logs remain necessary, but high-consequence AI actions need acceptance evidence before impact."

## Counsel gate

If the content may affect patentability, filing strategy, partner confidentiality, or trademark posture, obtain counsel review before public publication.
