# The Acceptance Plane in One Workflow

## A production deployment example for agentic AI infrastructure

**Meridian Verity Group**  
**Author:** Scott Lee  
**Release date:** 2026-06-11  
**Canonical DOI:** https://doi.org/10.5281/zenodo.20645907  
**Version:** v1.0.0

> **Status:** This release is a public architecture thesis. It is not a formal standard, product specification, legal opinion, compliance certification, patent claim chart, or implementation disclosure.

Abstract trust models become real when they touch production.

So consider one workflow: an AI coding agent proposes a production deployment.

At first glance, this can look like a normal automation problem. The agent generated a change. The identity is valid. The runtime is protected. The policy engine checked the rules. The deployment system has logs.

But none of that, by itself, answers the most important production question:

> **Should this exact deployment action be accepted into production right now?**

That is the role of the Acceptance Plane.

---

## Canonical Reference

> Lee, Scott. Meridian Verity Group. (2026). The Acceptance Plane: The Missing Trust Layer for Agentic AI Infrastructure (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.20645907

## The Workflow

```text
AI agent proposes deployment
-> identity validated
-> runtime attested
-> policy checked
-> target, scope, freshness, and revocation verified
-> acceptance decision
-> ACCEPT / HOLD / REFUSE
-> verifier-ready receipt
```

The workflow is intentionally simple.

The point is not that every AI action needs the same amount of ceremony. The point is that high-consequence actions need proof before they become real.

A suggested patch is not the same as a production change. A deployment plan is not the same as a deployment. A valid credential is not the same as valid authority. An attested runtime is not the same as accepted action.

The protected system still needs to decide whether the action should cross the boundary.

![Acceptance Plane workflow](../figures/acceptance-plane-workflow.png)

---

## 1. The Agent Proposes an Action

The agent proposes a deployment. It may have generated a fix, updated an infrastructure file, prepared a release plan, or requested a deployment API call.

At this point, the agent has produced intent. But intent is not consequence.

The system should not treat a proposed deployment as acceptable simply because the agent is useful, the code looks reasonable, or the tool call is syntactically valid.

> **AI output can be reviewed. AI action changes state.**

The Acceptance Plane begins where output becomes action.

---

## 2. Identity Is Validated

The system checks identity: user delegation, agent identity, service account, workload identity, and tool credential.

This matters. Without identity, there is no accountability.

But identity alone is not enough. A valid identity can still attempt the wrong action. A permitted agent can still operate outside current scope. A recognized workload can still use authority that has become stale.

Identity can answer who or what is acting. It does not fully answer whether this action should be accepted.

---

## 3. Runtime Is Attested

The system may verify where the agent or workload ran: approved environment, measured runtime, protected execution, and expected system state.

This also matters. Attestation can provide critical evidence that the system is interacting with the workload it expected, in the environment it expected.

But protected execution is not the same as accepted action. An attested runtime can still produce an action that is out of scope, stale, or aimed at the wrong production target.

Runtime evidence helps answer where the action came from. It does not fully answer whether production should accept it now.

---

## 4. Policy Is Checked

The system checks policy: allowed deployment type, agent permissions, target environment restrictions, approval requirements, risk flags, and step-up conditions.

Policy is necessary. But policy should not be treated as a one-time blessing detached from the final action.

In agentic systems, there can be a gap between an earlier policy decision and the moment an action reaches production. The approval may have expired. The target may have changed. The deployment window may have closed. The scope may no longer match. A revocation may have occurred.

The better question is:

> **Is the current policy state still sufficient for this exact action at the gate?**

---

## 5. The Acceptance Plane Verifies the Action

This is where the Acceptance Plane becomes visible.

The system binds the proposed action to the evidence that matters before production accepts it: action, initiator, target, scope, current policy state, freshness, revocation, and required step-up condition.

A deployment should not be accepted merely because the agent had access. It should be accepted because the action is still authorized, scoped, fresh, consistent, and verifiable at the acceptance boundary.

That is the difference between permission and proof.

---

## 6. ACCEPT, HOLD, or REFUSE

The Acceptance Plane does not need to make every workflow complicated. It needs to make the decision explicit.

**ACCEPT:** the evidence is current, scoped, consistent, and sufficient. The deployment can proceed.

**HOLD:** the evidence is incomplete, stale, ambiguous, high-risk, or requires step-up review. The deployment pauses before impact.

**REFUSE:** the action is outside authority, mismatched, revoked, replayed, unverifiable, or unsafe. The deployment is blocked.

A better pattern is:

> **Let agents move fast where proof is sufficient. Pause them where proof is incomplete. Stop them where proof fails.**

---

## 7. The Receipt

After the decision, the system should produce more than a vague log entry.

It should produce a verifier-ready receipt: a structured record of the action, authority, scope, evidence, policy state, decision, and reason.

This matters because production accountability cannot begin only after harm. In agentic AI, the question will not only be what the AI did. It will also be why the system accepted it.

---

## Why This Workflow Matters

The deployment example is only one workflow. The same pattern applies anywhere AI agents interact with protected systems: privileged APIs, regulated data, enterprise documents, financial actions, clinical records, infrastructure changes, sensitive context, or cross-boundary workflows.

The exact placement of the acceptance boundary will vary. The function will not.

Before an AI action becomes real, the system must be able to ask:

> **Is this action acceptable now?**

And it must be able to answer with evidence.
