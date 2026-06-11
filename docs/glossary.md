# Acceptance Plane Glossary

**Version:** v1.0.0
**Canonical DOI:** https://doi.org/10.5281/zenodo.20645907
**Status:** Public architecture vocabulary for the Acceptance Plane thesis.

This glossary defines public terms used by Meridian Verity Group to describe the Acceptance Plane in agentic AI infrastructure.

It is not a formal standard, product specification, API specification, legal opinion, compliance certification, patent claim chart, implementation guide, or implementation disclosure.

---

## Canonical Definition

**The Acceptance Plane™** is an architectural function that determines whether a specific autonomous AI action should be accepted by a protected system before impact, based on current, scope-bound, verifier-ready evidence at the acceptance boundary.

Short form:

> **The Acceptance Plane decides whether an autonomous AI action becomes a real-world consequence.**

---

## Core Terms

### Acceptance Plane

An architectural function that determines whether a specific autonomous AI action should be accepted by a protected system before impact.

The Acceptance Plane does not replace identity, access control, attestation, policy, encryption, or logging. It describes the architectural function for binding relevant trust signals to a specific action at the point where AI intention may become system consequence.

### Autonomous AI Action

An action initiated, proposed, delegated, or executed by an AI agent or agentic workflow that may affect a protected system, workflow, dataset, infrastructure boundary, or operational process.

Examples include tool invocation, workflow execution, record update, privileged API call, deployment action, regulated data movement, or protected egress.

### Action Acceptance

The decision that a specific autonomous AI action may affect a protected system.

Action acceptance is different from general access. A valid identity, permitted tool, attested runtime, or earlier policy check may provide evidence, but does not by itself prove that the final action should be accepted.

### Acceptance Boundary

The point where a proposed autonomous AI action may cross from intention, recommendation, or plan into protected-system consequence.

The acceptance boundary is where the system should ask:

> Should this exact action be accepted before impact?

### Protected System

A system, workflow, environment, dataset, infrastructure boundary, or operational process whose state, data, authority, or downstream effects should not be changed by autonomous action without evidence-bound acceptance.

### Production Consequence

A real operational effect created when an autonomous AI action changes state, moves data, calls a privileged function, triggers a workflow, updates a record, or affects a protected environment.

A recommendation is not yet a production consequence.
A deployment plan is not yet a deployment.
A tool call becomes consequential when the protected system accepts it.

---

## Evidence Terms

### Gate-Time Evidence

Current evidence evaluated at the acceptance boundary before a high-consequence action becomes real.

Gate-time evidence is not merely a post-hoc log. It is evidence checked before impact.

### Runtime Evidence

Evidence about where and how the agent, workload, tool, or service executed.

Runtime evidence may include signals from protected execution, measured environments, workload identity, or attestation systems, depending on system design. It is important evidence, but protected execution is not the same as accepted action.

### Policy State

The relevant policy condition at the time the action reaches the acceptance boundary.

In agentic systems, an earlier policy decision may become stale. The acceptance decision should consider whether the current policy state still supports the action.

### Scope-Bound Authority

Authority limited to a specific action, target, context, user delegation, workflow, environment, data class, or time window.

Scope-bound authority is narrower than broad permission.

### Freshness

The condition that authority, approval, policy state, runtime evidence, or other relevant signals are current enough to support the action at the acceptance boundary.

Freshness matters because an action that was once allowed may no longer be valid.

### Revocation State

The current status of any withdrawal, expiration, cancellation, suspension, or invalidation affecting the action, authority, approval, tool, credential, target, or workflow.

An action should not be accepted if relevant authority has been revoked.

### Target Consistency

The condition that the action is still bound to the intended target, destination, environment, record, workflow, or protected system.

Target consistency helps prevent mismatches, unauthorized redirection, and escalation.

---

## Decision Terms

### ACCEPT

The action may proceed because the evidence is current, scoped, consistent, sufficient, and aligned with the applicable acceptance conditions.

### HOLD

The action pauses before impact because evidence is incomplete, stale, ambiguous, high-risk, or requires step-up review.

HOLD is not failure. It is a fail-closed pause when proof is not yet sufficient.

### REFUSE

The action is blocked because authority, scope, target, freshness, revocation, replay, safety, or verification conditions fail.

REFUSE prevents an unverifiable or unauthorized action from becoming consequence.

### Step-Up Review

Additional human, policy, workflow, or system review required before an action may be accepted.

Step-up review is appropriate when risk is elevated or evidence is not sufficient for autonomous acceptance.

### Fail-Closed Autonomy

An operating posture where autonomous actions proceed when proof is sufficient, hold when proof is incomplete, and refuse when proof fails.

Fail-closed autonomy is not anti-autonomy. It is autonomy with evidence before impact.

---

## Accountability Terms

### Verifier-Ready Receipt

A structured record explaining the action attempted, authority and scope evaluated, evidence checked, policy state used, decision made, and reason for accepting, holding, or refusing.

A verifier-ready receipt is more than a vague log entry. It is intended to support later review of why a protected system accepted, held, or refused an autonomous action.

### Action-Level Accountability

The ability to evaluate and explain why a specific autonomous AI action was accepted, held, or refused at the acceptance boundary.

Action-level accountability is different from general model explainability. The question is not only what the model produced, but why the system accepted, held, or refused the action.

---

## Relationship to Existing Controls

The Acceptance Plane does not replace identity, IAM, workload authentication, runtime attestation, policy engines, encryption, secure channels, observability, or logs.

Those controls remain necessary.

The Acceptance Plane describes the architectural function for binding relevant signals to a specific autonomous AI action before impact.

In short:

> Identity helps answer who is acting.
> Attestation helps answer where execution occurred.
> Policy helps answer what rules apply.
> Logging helps reconstruct what happened.
> The Acceptance Plane asks whether this exact action should be accepted now.

---

## Public Language Guide

Preferred public phrasing:

> The Acceptance Plane is a public architecture thesis for action-level trust in agentic AI infrastructure.

> The Acceptance Plane decides whether an autonomous AI action becomes a real-world consequence.

> Access is not authority. Permission is not proof. Execution is not acceptance.

> The Acceptance Plane describes the architectural function for binding identity, runtime evidence, policy state, scope, freshness, revocation, target consistency, and accountability to a specific action before impact.

Avoid public claims such as:

* “world first”
* “formal standard”
* “compliance guarantee”
* “patent priority”
* “product specification”
* “implementation disclosure”
* “complete security solution”
* “replacement for IAM, attestation, policy, or logging”

---

## Trademark and Rights Notice

“Acceptance Plane” and “The Acceptance Plane” are used as Meridian Verity Group framework identifiers.

This glossary does not grant any trademark license, patent license, product implementation license, certification right, compliance approval, endorsement, or right to use Meridian Verity Group marks as source identifiers.

---

## Canonical Reference

Lee, Scott. Meridian Verity Group. (2026).
**The Acceptance Plane: The Missing Trust Layer for Agentic AI Infrastructure** (v1.0.0). Zenodo.
https://doi.org/10.5281/zenodo.20645907
