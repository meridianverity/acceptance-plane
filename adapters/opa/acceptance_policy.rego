package acceptance_plane.public_eval

# Shape-only OPA/Rego adapter sketch for public discussion.  The runnable
# evaluator in this repository is Python; this file shows how the same
# ACCEPT/HOLD/REFUSE boundary can be projected into policy-as-code.

default decision := {"decision": "HOLD", "reason_code": "AP-101_MISSING_FIELD"}

decision := {"decision": "ACCEPT", "reason_code": "AP-000_ACCEPTED"} if {
  input.evidence.identity_valid == true
  input.evidence.runtime_attested == true
  input.evidence.target_binding == input.action.target
  input.authority.subject == input.action.actor
  input.authority.revoked == false
  input.evidence.policy_digest == input.computed.policy_digest
  input.evidence.transparency_proof_present == true
}
