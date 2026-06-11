# MVG Acceptance Plane Zenodo + GitHub Launch Runbook

## Canonical provenance package v1.0.0

**Meridian Verity Group**  
**Author:** Scott Lee  
**Release date:** 2026-06-11  
**Canonical DOI:** https://doi.org/10.5281/zenodo.20645907

> **Status:** This runbook is operational guidance for publishing the public architecture thesis. It is not legal advice, patent advice, compliance certification, or implementation disclosure.

---

## 1. Strategic Goal

The goal is not to claim absolute global invention priority or replace patent filing strategy.

The goal is to create a public, citable, timestamped, versioned reference showing that Meridian Verity Group publicly defined **the Acceptance Plane** as an architectural function for evidence-bound acceptance of autonomous AI actions before impact.

Recommended public wording:

> **Meridian Verity Group is publishing a public architecture thesis for the Acceptance Plane in agentic AI infrastructure.**

Avoid unsupported absolute claims such as "first ever in the world," "formal standard," "patent-protected mechanism," or "compliance guarantee."

---

## 2. Provenance Stack

**Zenodo manual technical report DOI:** canonical citation: https://doi.org/10.5281/zenodo.20645907.

**GitHub public repository:** public source, glossary, workflow, diagrams, and citation metadata.

**Immutable GitHub release:** integrity layer for the release assets and associated tag.

**Zenodo GitHub release archive DOI:** versioned source/provenance archive created after GitHub release.

**MVG LinkedIn article and website page:** market narrative and long-term category home.

The clean separation is:

- **Cite this:** Zenodo manual technical report DOI: https://doi.org/10.5281/zenodo.20645907.
- **Verify source/provenance:** GitHub release tag, commit hash, SHA256 manifest, and Zenodo GitHub archive DOI.

---

## 3. Current Reality After LinkedIn Publication

Because the first LinkedIn article has already been published, the launch is now a canonicalization strategy rather than a pre-publication DOI-first strategy.

Use this sequence:

1. LinkedIn article remains the market narrative already live.
2. Zenodo report becomes the canonical citable v1.0.0 record.
3. GitHub release becomes the public source/provenance package.
4. MVG website becomes the long-term category home.
5. LinkedIn article, pinned company post, and partner DMs are updated with DOI/provenance links after publication.

This is still strong. It creates a durable reference point after the initial public thesis.

---

## 4. IP Redline Principle

> **Publish the category. Protect the mechanism.**

Publish:

- Acceptance Plane definition.
- Public architecture thesis.
- Conceptual workflow.
- High-level evidence categories.
- Conceptual diagrams.
- Glossary and FAQ.
- Public claims style guide.

Hold back:

- Exact API schemas.
- Full evidence object model.
- Cryptographic binding method.
- Enforcement pipeline.
- Hardware-specific claim maps.
- Partner-specific architectures.
- Unpublished patent claim language.

If implementation details matter, file first and publish second.

---

## 5. License Decision

This final package uses **CC BY 4.0** for public architecture text, diagrams, and metadata.

Rationale: CC BY 4.0 supports category adoption, citation, quotation, redistribution, and partner sharing while preserving attribution requirements.

Counsel may choose to switch to CC BY-ND 4.0 or another license before public release if derivative-language control is more important than adoption.

The NOTICE file clarifies that the content license does not grant patent rights, trademark rights, implementation rights, confidential mechanisms, or partner-specific rights.

---

## 6. Zenodo Manual Record

Create a manual Zenodo upload for the canonical technical note/report.

Recommended record title:

**The Acceptance Plane: The Missing Trust Layer for Agentic AI Infrastructure**

Recommended resource type:

**Publication / Technical note** or **Publication / Report**

Recommended upload files:

- `dist/MVG_The_Acceptance_Plane_v1.0.0.pdf`
- `dist/MVG_The_Acceptance_Plane_v1.0.0.docx`
- `figures/acceptance-plane-stack.png`
- `figures/acceptance-plane-workflow.png`

DOI discipline:

- For v1.0.0, the canonical DOI has been applied: https://doi.org/10.5281/zenodo.20645907.
- Do not replace this DOI with a GitHub-Zenodo release archive DOI. The GitHub archive DOI is source/provenance, not the canonical citation.

---

## 7. GitHub Repository

Recommended repository:

```text
meridian-verity-group/acceptance-plane
```

Recommended description:

```text
Public architecture thesis and reference workflow for the Acceptance Plane in agentic AI infrastructure.
```

Recommended topics:

```text
agentic-ai
ai-infrastructure
ai-trust
autonomous-agents
acceptance-plane
zero-trust
confidential-computing
remote-attestation
policy-as-code
cybersecurity
devsecops
enterprise-ai
```

Recommended settings:

- README enabled.
- Issues off initially.
- Discussions off initially unless MVG wants public community input.
- Wiki off.
- Branch protection for `main`.
- Signed commits where practical.
- Immutable releases where available/enabled.
- Zenodo GitHub integration enabled after the repo is public.

---

## 8. Release Integrity

Before public release:

1. Confirm no forbidden implementation details are present.
2. Confirm the canonical DOI is present in public citation points: https://doi.org/10.5281/zenodo.20645907.
3. Confirm license and metadata agree.
4. Confirm PDF/DOCX metadata show Scott Lee and Meridian Verity Group.
5. Confirm figures do not clip.
6. Recompute `provenance/MANIFEST.sha256`.
7. Commit with a signed commit where practical.
8. Tag with a signed tag where practical.
9. Publish an immutable GitHub release if available.

Suggested tag:

```text
v1.0.0
```

Suggested release title:

```text
v1.0.0 - The Acceptance Plane: Public Architecture Thesis
```

---

## 9. MVG Pinned Article Caption

Meridian Verity Group is publishing its public architecture thesis for the Acceptance Plane.

Agentic AI is moving from output generation to real system action. That shift changes the trust question.

It is no longer enough to ask whether an agent had access, whether a workload was authenticated, whether an environment was attested, or whether an event was logged after the fact.

The deeper production question is:

**Should this exact autonomous action be accepted into a protected system right now?**

We define the Acceptance Plane as the architectural function that determines whether a specific autonomous AI action should be accepted before impact, based on current, scope-bound, verifier-ready evidence at the acceptance boundary.

Access is not authority. Permission is not proof. Execution is not acceptance.

---

## 10. Scott Repost Caption

Today Meridian Verity Group is publishing its public architecture thesis for the Acceptance Plane.

The core idea is simple:

Access is not authority. Permission is not proof. Execution is not acceptance.

As AI agents move from generating outputs to taking actions, production systems need a boundary that can decide whether a specific autonomous action should be accepted before impact.

MVG calls that architectural function the Acceptance Plane.

---

## 11. Partner DM

Sharing MVG's public architecture thesis for the Acceptance Plane.

The thesis is that agentic AI shifts the trust boundary from output correctness to action acceptance: should this exact autonomous action be accepted into a protected system right now?

We published the thesis as a citable package with a GitHub release/provenance trail so partners can reference a stable version.

Would value your perspective on where this acceptance boundary should live in production AI systems.

---

## 12. Go / No-Go Gate

Public release is a GO only when:

- Counsel/IP redline is complete.
- License is confirmed.
- Canonical DOI is embedded in public citation points: https://doi.org/10.5281/zenodo.20645907.
- Figures render without clipping.
- DOCX and PDF metadata are professional.
- Manifest verifies.
- GitHub repository settings are correct.
- Zenodo manual record metadata is ready.
- MVG knows which URL will be treated as canonical.

If any item fails, publish to a private repository or internal review folder only.
