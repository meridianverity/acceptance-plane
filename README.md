# The Acceptance Plane™
**Action acceptance before impact.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20645907.svg)](https://doi.org/10.5281/zenodo.20645907)

Public architecture thesis and hardened public-evaluation proof overlay for the Acceptance Plane™ in agentic AI infrastructure.

**Prepared by:** Meridian Verity Group  
**Author:** Scott Lee  
**Canonical thesis version:** v1.0.0  
**Public-eval overlay:** v1.0.1-public-eval  
**Release date:** 2026-06-11  
**Canonical DOI:** https://doi.org/10.5281/zenodo.20645907

## Canonical Definition

**The Acceptance Plane™ is an architectural function that determines whether a specific autonomous AI action should be accepted by a protected system before impact, based on current, scope-bound, verifier-ready evidence at the acceptance boundary.**

Short form:

> **The Acceptance Plane™ decides whether an autonomous AI action becomes a real-world consequence.**

## Repository Status

This repository contains a public architecture thesis, provenance package, and bounded public-evaluation proof overlay. It is not a formal standard, product specification, legal opinion, compliance certification, patent claim chart, implementation disclosure, endorsement, deployment guarantee, or complete security solution.

## What changed in the hardened overlay

The original v1.0.0 package was thesis/provenance oriented. The v1.0.1 public-eval overlay adds runnable verification:

```bash
python scripts/verify_manifest.py
python tools/run_public_eval.py
python tools/verify_transparency_bundle.py
python tools/verify_proof_receipt.py --verify-manifest
python tools/independent_recompute.py
python tools/release_gate.py
```

Expected headline result:

```text
Acceptance Plane public eval: 64 / 64 PASS
independent recomputation: 13 / 13 PASS
release gate: PASS
```

## Fast path

```bash
python -m pip install -e . --no-deps
python -m pip install cryptography pytest
make qa-full
python -m pytest -q
```

`cryptography` is used for the deterministic public-eval Ed25519 receipt profile. The key is intentionally public-eval only and is not a production trust root.

## Contents

- `docs/acceptance-plane-whitepaper.md` - canonical public architecture thesis.
- `docs/acceptance-plane-in-one-workflow.md` - production deployment workflow explainer.
- `docs/ACCEPTANCE_BOUNDARY_SPEC_v1.md` - runnable public-eval decision profile.
- `docs/PROOF_CHAIN.md` - proof-chain verification guide.
- `docs/HARDENING_NOTES_v1_0_1.md` - hardening and integrity notes.
- `docs/RELEASE_ARTIFACT_VERIFICATION.md` - source/archive verification guide.
- `docs/PERMIT_RECEIPT_HALTSEAL_SUPERSET_STRATEGY.md` - positioning against concrete receipt/gateway mechanisms.
- `tools/` - public-eval runner, proof receipt verifier, release verifier, and independent recomputation.
- `acceptance_plane_eval/` - deterministic public-eval reference evaluator.
- `vectors/` - 64 ACCEPT/HOLD/REFUSE scenario vectors.
- `receipts/` - generated public-eval results, transparency bundle, and proof receipt.
- `examples/scenario_cards/` - linter-ready scenario cards.
- `schemas/` - JSON schema profile for scenario cards, evidence, actions, decisions, and receipts.
- `adapters/` - shape-only OPA, Envoy, and Kubernetes adapter sketches.
- `dist/` - original v1.0.0 PDF/DOCX release assets.
- `metadata/` - Zenodo/GitHub metadata and publication copy.
- `provenance/` - file tree, QA report, and SHA256 manifest.

## Scenario-card linter

```bash
python tools/lint_scenario_card.py examples/scenario_cards/deploy_accept.json
python tools/lint_scenario_card.py examples/scenario_cards/hold_approval_required.json
python tools/lint_scenario_card.py examples/scenario_cards/refuse_revoked.json
```

The linter checks basic card completeness, verifies policy digest binding, evaluates ACCEPT/HOLD/REFUSE, and prints a deterministic receipt digest.

## Canonical Citation

> Lee, Scott. Meridian Verity Group. (2026). The Acceptance Plane™: The Missing Trust Layer for Agentic AI Infrastructure (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.20645907

The v1.0.1 overlay is source/provenance and public-evaluation material for the same canonical thesis. It does not replace the canonical DOI.

## Source and Provenance

The GitHub release package is intended as a source/provenance package for public architecture materials and bounded public-evaluation artifacts, not a product software release.

Repository URL:

```text
https://github.com/meridianverity/acceptance-plane
```

## Scope Boundaries

The materials are intended for public discussion, citation, education, review, and provenance.

They are not a formal standard, product specification, API specification, legal opinion, compliance certification, patent claim chart, implementation disclosure, endorsement, deployment guarantee, or complete security solution.

## License and Notices

This package uses Creative Commons Attribution 4.0 International (CC BY 4.0) for the public architecture thesis, related documentation, figures, and public-evaluation materials.

See the NOTICE file for trademark, patent, and scope notices.

The license applies only to copyrightable public materials included in this release.

It does not grant patent rights, trademark rights, service mark rights, product implementation rights, certification rights, compliance approvals, endorsements, confidential mechanisms, partner-specific rights, or rights to use Meridian Verity Group marks as source identifiers.

“Acceptance Plane™” and “The Acceptance Plane™” are used as Meridian Verity Group framework identifiers and source-identifying marks.

## Short Public Description

The Acceptance Plane™ describes the architectural function for deciding whether a specific autonomous AI action should be accepted by a protected system before impact.

Access is not authority.  
Permission is not proof.  
Execution is not acceptance.

Not a product implementation. Not a standard. No certification right. No patent license.
